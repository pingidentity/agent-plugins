---
title: "Server-Side App Integration — Backend OIDC and Token Handling"
product_family: cross-platform
products: ["pingone", "pingone-aic", "pingfederate"]
capabilities: ["app-integration"]
services: []
audience: ["developer", "architect"]
use_cases: ["workforce", "customer", "cross-platform"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-03"
slug: "https://developer.pingidentity.com/pingone-api/platform/"
---

# Server-Side App Integration — Backend OIDC and Token Handling

Implementation patterns for backend / server-side applications integrating with Ping Identity: confidential OIDC clients, machine-to-machine auth, token validation, refresh, and resilience under load. Covers Node.js, Java, Python, .NET, and Go using standard OIDC client libraries — not the Ping native SDKs (which target end-user apps).

## Scope

**Covers:**
- Confidential OIDC client setup (Authorization Code + PKCE, Client Credentials, Refresh Token)
- Server-side token validation (JWT verification, introspection, signing key rotation)
- Token refresh and silent renewal patterns
- M2M / worker-to-worker auth via Client Credentials
- Backchannel patterns (CIBA, Token Exchange) for delegated access
- Retry, 429 handling, circuit-breaker patterns for token endpoint resilience
- Multi-environment configuration management (Dev / Staging / Prod)

**Does NOT cover:**
- End-user mobile/web SDK integration — see `references/curated/mobile-integration-basics.md` and `references/curated/web-integration-basics.md`
- Designing the journey/flow that issues the token — see `ping-orchestration`
- Platform-side OAuth client registration — see `ping-foundation`
- AI agent identity patterns (CIBA for HITL, agent-to-agent) — see `ping-identity-for-ai`

---

## Pick the correct grant type

| Use case | Grant type | Notes |
|---|---|---|
| End-user logs into a web app rendered by your server | Authorization Code + PKCE | Server holds the secret; PKCE adds defense-in-depth |
| End-user logs in via SPA, your backend exchanges/refreshes tokens (BFF pattern) | Authorization Code + PKCE (in BFF) | SPA never sees the secret; BFF handles token storage |
| Backend service calls another backend service on behalf of itself | Client Credentials | No user; opaque or JWT access token |
| Backend service acts on behalf of a user via delegation | Token Exchange (RFC 8693) | Exchange a user token for a downstream-scoped token |
| Backend initiates auth for a user out-of-band (push/SMS to phone) | CIBA (Client Initiated Backchannel Authentication) | Used for IVR, AI agent HITL, transaction approval |
| Constrained device with no browser | Device Authorization Grant | User completes auth on a separate device with a browser |

**Anti-patterns to avoid:**
- Implicit grant — deprecated; tokens in URL fragment
- ROPC (Resource Owner Password Credentials) — exposes user password to the client; allowed only in legacy migration scenarios
- Refresh tokens stored in browser storage — use HttpOnly cookies via a BFF instead

---

## Library selection

Use a maintained OIDC-compliant library — do not hand-roll OAuth.

| Language | Recommended library | Notes |
|---|---|---|
| Node.js / TypeScript | `openid-client` | Spec-compliant; supports discovery, PKCE, token exchange |
| Java | Spring Security OAuth2 / Nimbus OAuth2 SDK | Spring for full apps; Nimbus for libraries |
| Python | `authlib` | Sync + async; supports discovery, PKCE, JWT validation |
| .NET | Microsoft.Identity.Web / IdentityModel | Use IdentityModel for non-Microsoft scenarios |
| Go | `golang.org/x/oauth2` + `github.com/coreos/go-oidc` | Combine for full OIDC flow |

**OIDC discovery:** Always start from the well-known endpoint:
- PingOne (multi-tenant cloud): `https://auth.pingone.com/{envId}/as/.well-known/openid-configuration`
- PingOne Advanced Identity Cloud (AIC): `https://<tenant>.forgerock.io/am/oauth2/realms/root/realms/<realm>/.well-known/openid-configuration`
- PingFederate: `https://<pf-host>:9031/.well-known/openid-configuration`

The discovery document defines the AS endpoints and supported algorithms. Do not hardcode token / userinfo / JWKS URLs.

---

## Authorization Code + PKCE pattern (server-rendered web app)

### Sequence

```
Browser → /login on your server
  → Server: generate code_verifier, code_challenge, state, nonce
  → 302 redirect to AS authorize endpoint with PKCE + state + nonce
Browser → AS hosted login page (or DaVinci flow / AIC journey)
  → User authenticates
AS → 302 to your /callback?code=...&state=...
  → Server: verify state matches stored value
  → Server: POST to AS token endpoint with code + code_verifier + client_secret (or PKCE-only if public)
  → Receives id_token, access_token, refresh_token
  → Verify id_token signature, issuer, audience, nonce, exp
  → Establish server session; set HttpOnly + SameSite=Lax cookie
  → Store refresh token server-side (encrypted at rest)
  → Redirect to original URL or /home
```

### Required server-side checks

| Check | Why |
|---|---|
| State parameter matches stored value | Prevents CSRF attacks on the redirect |
| Nonce in id_token matches stored value | Prevents replay attacks |
| Issuer matches discovery `issuer` | Token came from the expected AS |
| Audience matches your client_id | Token issued for this app |
| Token expiry not in the past | Token still valid |
| Signature verified against JWKS | Token not tampered with |
| `acr_values` and `auth_time` claims, if requested | Confirms requested authentication context met |

---

## Token validation

### JWT access token (preferred)

PingOne supports JWT access tokens. Validate locally — do NOT introspect on every request.

```
1. Fetch JWKS from discovery `jwks_uri` (cache for 1 hour; refresh on `kid` mismatch)
2. Parse JWT header, find matching `kid`
3. Verify signature with the corresponding public key
4. Validate claims: iss, aud, exp, nbf, sub
5. Optional: validate `client_id`, `scope`, custom claims
```

### Opaque access token

Some configurations use opaque tokens that require introspection.

```
POST {introspection_endpoint}
  client_id, client_secret (HTTP Basic)
  token=<opaque_token>
Response: { active: true|false, sub, scope, exp, ... }
```

**Caching:** Cache positive introspection results until a few seconds before `exp`. Cache negative results briefly (1-5s) to absorb scan attempts without flooding the AS.

### Token rotation and key rollover

Ping platforms rotate signing keys periodically. Your library MUST:

- Cache JWKS with a TTL no longer than 1 hour
- On `kid` mismatch, refresh JWKS once before failing
- Tolerate `kid` overlap (multiple keys valid simultaneously) during rollover

---

## Refresh token handling

Server-side apps SHOULD store refresh tokens encrypted at rest, scoped to the user's session.

### Pattern — silent renewal

```
On API request:
  if access_token.exp < now + 60s:
      POST token endpoint with grant_type=refresh_token
      → receive new access_token (and possibly new refresh_token if rotation enabled)
      → atomically replace stored tokens
  proceed with API request
```

### Refresh token rotation

When the AS issues a new refresh token on every refresh, treat it as a single-use replacement.

- Persist the new refresh token before the next request uses it
- If a refresh fails with `invalid_grant`, force the user to re-authenticate (refresh token may have been revoked or already consumed elsewhere)
- Configure a small grace period (`refresh_token_rolling_grace`) on the AS to absorb concurrent requests during rotation

### Reuse detection

If the AS rejects an already-used refresh token, the user's tokens may be compromised. Best practice:

- Log the event with user_id and IP
- Revoke all sessions for the user
- Force re-authentication

---

## Client Credentials (M2M)

Backend-to-backend without a user.

```
POST {token_endpoint}
  client_id (public)
  client_secret (HTTP Basic) OR private_key_jwt assertion
  grant_type=client_credentials
  scope=<requested scope>
Response: { access_token, expires_in, token_type, scope }
```

**Token caching:** Cache the access token for `expires_in - 60s`. Re-fetch only on expiry. Most clients refresh too aggressively; this hammers the AS.

**Worker / service principal model:**
- PingOne (multi-tenant cloud): register a "Worker app"; assign admin roles directly to it
- AIC: create an OAuth 2.0 client with the `client_credentials` grant; use service-account-style scopes
- PingFederate: register an OAuth client with `client_credentials` grant in PingFederate AS

**Recommendation — `private_key_jwt` over `client_secret_basic`:** asymmetric keys eliminate shared-secret leakage. Generate a key pair, register the public key (or its JWKS URL) with the AS, sign a JWT assertion at request time.

---

## CIBA (Client Initiated Backchannel Authentication)

For human-in-the-loop or out-of-band auth where the user is not at the same device as the requesting client.

```
Backend → AS bc-authorize endpoint
  scope, login_hint or login_hint_token, binding_message
Response: auth_req_id, expires_in, interval

[Backend polls OR receives push notification]

Backend → AS token endpoint
  grant_type=urn:openid:params:grant-type:ciba
  auth_req_id=<id>
Response: tokens (when user has approved on their device)
```

**Use CIBA for:**
- IVR / call-center step-up: customer approves a transaction on their phone while talking to an agent
- AI agent HITL: agent requests user approval before executing a sensitive action — see `ping-identity-for-ai`
- Server-initiated transaction confirmation

CIBA support varies by platform. Check `backchannel_authentication_endpoint` in the discovery document.

---

## Token Exchange (RFC 8693)

Used to swap one token for another with reduced scope, different audience, or different actor context.

```
POST {token_endpoint}
  grant_type=urn:ietf:params:oauth:grant-type:token-exchange
  subject_token=<original_token>
  subject_token_type=urn:ietf:params:oauth:token-type:access_token
  audience=<downstream_service>
  scope=<reduced_scope>
```

**Common patterns:**
- Service A receives a user token, exchanges it for a service-B-scoped token
- AI agent acts on behalf of a user with a delegated, restricted token
- Long-running job exchanges a session token for a long-lived task token

PingOne supports token exchange via the standard token endpoint. Worker apps may need explicit token-exchange enablement at the OAuth provider level.

---

## Resilience patterns

Token endpoints are critical-path. Backend integrations must handle failures gracefully.

### 429 (Rate limiting)

PingOne and AIC apply per-environment rate limits.

| Header | Action |
|---|---|
| `Retry-After` | Wait the indicated seconds before retry |
| Absent | Use exponential backoff: 1s, 2s, 4s, 8s, max 60s |

**Do NOT:** spin in a tight retry loop — you will be temporarily blocked.

### Transient 5xx

| Code | Cause | Action |
|---|---|---|
| 502 / 503 / 504 | Upstream / AS warming after deploy / network blip | Retry with exponential backoff; max 3 retries |
| 500 | Server error; could be persistent | Retry once; on second failure, fail the request and alert |

### Circuit breaker

For high-volume services, wrap the token endpoint in a circuit breaker:

- Open circuit after N consecutive failures (e.g., 5 in 10s)
- Reject calls fast for cooldown period (e.g., 30s)
- Half-open: allow one trial; on success, close circuit

This prevents cascading failures when the AS is briefly unavailable.

### Token caching strategy

| Scope | TTL | Rationale |
|---|---|---|
| Access token (M2M) | `expires_in - 60s` | Always have a buffer for the request to complete |
| JWKS | 1 hour, refresh on `kid` mismatch | Match Ping rotation cadence |
| Discovery document | 24 hours | Endpoints rarely change; refresh on schema mismatch |
| Introspection result (positive) | until `exp` | Avoid hammering AS |
| Introspection result (negative) | 5s | Limit damage from rejected tokens |

---

## Multi-environment configuration

Production-grade backends MUST keep environment-specific config out of code:

| Setting | Source |
|---|---|
| `client_id`, `client_secret` | Env-specific secret store (Vault, AWS Secrets Manager, K8s secrets) |
| `discovery_url` | Env-specific config map |
| `redirect_uri` | Env-specific config; never hardcoded |
| Signing keys (private_key_jwt) | Env-specific KMS / HSM |

**Per-environment registration:** Register a separate OAuth client per environment (Dev / Staging / Prod). Do NOT share client IDs across environments — a compromised dev secret should not affect production.

---

## Common gotchas

| Gotcha | Symptom | Fix |
|---|---|---|
| `redirect_uri` mismatch | `redirect_uri_mismatch` error | Register exact URI; trailing slash + path case matters; register dev/staging/prod separately |
| Clock skew on JWT validation | Random `exp` failures during peak load | Allow ±60s `leeway` on `exp` and `nbf`; sync NTP on all servers |
| JWKS cache too long | After AS key rotation, signature verification fails | TTL ≤ 1 hour; refresh on `kid` miss before failing |
| Scope creep | Request more scopes than needed | Start minimal; add scopes only when a use case requires them |
| ROPC for backend "convenience" | Password leaked to backend; legacy compromise vector | Migrate to Authorization Code or Client Credentials |
| Refresh token in cookie + leak | Token stolen via XSS | Use HttpOnly + SameSite=Strict cookies for refresh tokens; never expose to JS |
| Hardcoded discovery / token endpoints | Breaks when AS hostname changes | Resolve via discovery; cache for 24h |
| `iat` / `nbf` validation rejecting valid tokens | Token issued slightly in future | Apply leeway; check NTP |
| Multiple worker apps for same service | Hard to audit; secrets sprawl | One worker app per service per environment; rotate secrets quarterly |
| 429 retry loop | Service degraded; AS blocking | Honor `Retry-After`; circuit-breaker; never tight-loop |

---

## Prerequisites

- OAuth client registered in the target Ping environment with the required grant types and redirect URIs (see `ping-foundation`)
- Network access from the backend to the AS token / introspection / JWKS endpoints
- Secret storage for `client_secret` or signing keys (private_key_jwt)
- Time sync (NTP) to keep server clocks within ±60s

## Common variants

| Variant | Note |
|---|---|
| BFF (Backend-For-Frontend) | Server holds tokens; SPA receives only HttpOnly session cookie |
| Microservices with mesh | Sidecar proxy validates tokens at the edge; service code reads claims from headers |
| FaaS / serverless | Cache JWKS in module scope to survive cold starts; minimize discovery latency |
| Multi-tenant SaaS | One AS issuer per tenant or shared AS with `tenant` claim; design before scaling |
| Hybrid PingFederate + PingOne | PF as identity bridge; backend trusts PF-issued tokens with PingOne federation |

## Cross-skill routing

| If the task is also... | Skill |
|---|---|
| Registering the OAuth client / configuring scopes | `ping-foundation` |
| Designing what the user sees during sign-in | `ping-orchestration` |
| Adding risk evaluation or step-up | `ping-universal-services` |
| AI agent identity / CIBA HITL / token exchange for agent | `ping-identity-for-ai` |
| End-user mobile/web SDK | `references/curated/mobile-integration-basics.md`, `references/curated/web-integration-basics.md` |

## Related references

- `references/curated/app-integration-overview.md`
- `references/curated/web-integration-basics.md`
- `references/curated/integration-troubleshooting-basics.md`

## Source

- [PingOne OIDC overview](https://docs.pingidentity.com/pingone/openid_connect/p1_oidc_overview.html)
- [PingOne token exchange](https://docs.pingidentity.com/pingone/use_cases/p1_oauth_2_token_exchange.html)
- [AIC OAuth 2.0 guide](https://docs.pingidentity.com/pingoneaic/am-oauth2-guide/oauth2-introduction.html)
- [PingFederate OAuth 2.0](https://docs.pingidentity.com/pingfederate/13.0/administrators_reference_guide/pf_oauth_overview.html)
- [RFC 7636 — PKCE](https://datatracker.ietf.org/doc/html/rfc7636)
- [RFC 8693 — Token Exchange](https://datatracker.ietf.org/doc/html/rfc8693)
- [OpenID CIBA Core](https://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0.html)
