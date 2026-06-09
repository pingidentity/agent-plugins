---
title: "Agent Security Patterns — Securing AI Agents with Ping Identity"
product_family: cross-platform
products: ["pingone", "pingfederate"]
capabilities: ["identity-for-ai", "foundation"]
services: []
audience: ["developer", "architect"]
use_cases: ["ai-identity"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-03"
slug: "https://docs.pingidentity.com/pingone/ai_agents/p1_ai_agents.html"
---

# Agent Security Patterns — Securing AI Agents with Ping Identity

Patterns for securing autonomous and semi-autonomous AI agents that call Ping Identity OAuth-protected APIs or downstream resources, covering machine-to-machine auth, token scoping, rotation, revocation, and audit.

## Scope

Covers: OAuth 2.0 client credentials flow as the default machine-to-machine pattern for AI agents, token scoping strategy, short-lived token rotation, revocation on compromise, and correlatable audit patterns.
Does NOT cover: human-in-the-loop delegation (see `references/curated/workforce-helpdesk-ai.md`), Verified Trust signal issuance (see `references/curated/verified-trust-overview.md`), or standard OIDC application registration for user-facing apps (see `ping-foundation`).

---

## Pattern 0: Register the agent as a managed identity

Before any token is issued, the AI agent should be registered as a first-class identity — not just an anonymous OAuth2 client. This enables lifecycle management, ownership tracking, and audit.

### PingOne — AI Agents feature

PingOne supports registering AI agents as managed identities via the **AI Agents** admin surface (requires Agent IAM Core license; contact Ping Identity Sales).

| Registration field | Notes |
|---|---|
| Agent name | Human-readable label; appears in audit logs and admin console |
| Owner | The human or team responsible for the agent |
| Client ID | Auto-generated OAuth 2.0 client ID |
| Client authentication method | `private_key_jwt` (recommended) or `client_secret_basic` |
| Scopes | Minimum required; configured at registration |

Registered agents appear in the AI Agents list (Directory > AI Agents in the PingOne console) alongside human identities.

### PingOne AIC — Dynamic agent onboarding via `/aiagent/register`

AIC provides a dedicated DCR endpoint for AI agents: `/aiagent/register` (in addition to the standard `/register`). This endpoint onboards AI agents as dynamic OAuth 2.0 clients with agent-specific defaults.

> **Availability:** Production-ready as of 2026-06-03. Currently available on the **Rapid channel** only; Regular channel promotion is planned.

AIC AI agents can perform tasks on behalf of end users through a delegated token exchange process (RFC 8693), maintaining distinct accountability and granular access control.

### Agent detection — know your agents

- Track all agent registrations in a registry (admin console, IDP admin API, or CMDB).
- Each agent should have a documented owner and expiry/renewal date.
- Disable agents that are decommissioned — do not leave them in a dormant but active state.

---

## Pattern 1: Machine-to-machine auth with client credentials

The OAuth 2.0 client credentials grant is the default pattern for AI agents that operate without a human in the loop. The agent authenticates directly to the authorization server using its own client identity — no user is involved.

### How it works

```
AI Agent ──► POST /token (client_id, client_secret or private_key_jwt)
                │
                ▼
         Ping OAuth AS (PingOne / PingFederate)
                │
                ▼
         Access Token (JWT, short TTL)
                │
AI Agent ──► API call with Bearer token
                │
                ▼
         Resource Server (validates token)
```

### Client authentication methods — comparison

| Method | When to use | Credential type | Key constraint |
|---|---|---|---|
| `client_secret_post` | Dev / low-assurance only | Shared secret in request body | Secret must be rotated on any exposure; never use in production multi-agent deployments |
| `client_secret_basic` | Dev / low-assurance only | HTTP Basic auth header | Same constraints as `client_secret_post` |
| `private_key_jwt` | Production agents | Asymmetric key pair; agent holds private key | Preferred for production; key material never leaves the agent; supports key rotation without AS coordination |
| mTLS (`tls_client_auth`) | High-assurance or regulated environments | X.509 certificate | Requires mTLS-capable infrastructure; eliminates secret-in-flight; supported by PingFederate and PingOne |

**Decision rule:** Use `private_key_jwt` or mTLS for any agent running in production. `client_secret_*` is acceptable only for local development or test environments where the secret lifetime is controlled.

---

## Pattern 2: Token scoping strategy

Each AI agent must receive the minimum set of scopes required for its specific capability. Broad scopes create blast-radius risk if an agent is compromised or misconfigured.

### Scoping principles

| Principle | Rationale |
|---|---|
| One agent registration per distinct capability | Prevents a compromised component from using scopes it does not need |
| No wildcard scopes for agents | Even if the AS supports wildcard grants, agents must enumerate required scopes at registration time |
| Separate read and write scopes | An agent that only reads data must not hold a write scope |
| Resource indicator scopes (RFC 8707) | Bind a scope to a specific resource server — prevents token reuse across services |

### Scope model example

| Agent | Required scope | Forbidden scope |
|---|---|---|
| AI helpdesk read agent | `directory:read profile:read` | `directory:write admin:*` |
| AI provisioning agent | `directory:write group:assign` | `admin:environment` |
| AI audit agent | `audit:read events:read` | Any write scope |

---

## Pattern 3: Short-lived token rotation

Agent access tokens must have a shorter TTL than tokens issued to human users, because agents operate continuously and may be compromised without immediate human detection.

| Token type | Recommended TTL | Rationale |
|---|---|---|
| Agent access token | 5–15 minutes | Limits the window a stolen token remains valid |
| Refresh token (if used) | 1–4 hours with rotation | Each use issues a new refresh token and invalidates the old one; detect replay attacks |
| Service account token (PingFederate) | 10–30 minutes | Same principle; refresh via client credentials, not long-lived token storage |

**Anti-pattern:** Caching an agent access token until it expires and reusing it across many requests over hours. Even if the token is technically valid, long-lived token reuse increases exposure window.

**Implementation:** Use the `expires_in` field in the token response. Proactively refresh when `expires_in < refresh_threshold` (recommended: 20% of TTL remaining).

---

## Pattern 4: Revocation

When an AI agent is decommissioned, compromised, or misbehaving, access must be cut immediately — not at token expiry.

### Revocation mechanisms

| Mechanism | Latency | Scope |
|---|---|---|
| Client credential deactivation (PingOne / PingFederate) | Immediate at AS; propagates to resource servers at next token introspection | Prevents new token issuance; existing tokens valid until TTL |
| Token introspection + blacklist | ~50–100 ms per call | Resource server calls AS to validate each token; blacklist entry blocks immediately |
| Short TTL + no refresh token | Max token TTL | Simplest approach; no revocation infrastructure needed; requires short TTL discipline |
| Delete application / client registration | Immediate — all tokens orphaned | Decommissions agent entirely; use for permanent removal |

**Decision rule:**
- For immediate revocation during an incident: disable the client registration and add the agent's `client_id` to a token introspection blacklist.
- For routine decommissioning: delete the client registration and let outstanding tokens expire.
- For compromised tokens: require introspection at every resource server call (trade latency for security).

---

## Pattern 5: Audit trail

Every API call made by an AI agent must be attributable to that agent, the action taken, and when it happened. Audit trail requirements exist independent of the auth pattern.

### Audit fields per agent request

| Field | Source | How to carry it |
|---|---|---|
| `agent_id` | Agent's `client_id` or `sub` claim in access token | JWT claim; resource server extracts from token |
| `request_id` | Generated by agent per request (UUID v4) | `X-Request-ID` header or `jti` (JWT ID) in a request-bound token |
| `user_id` (if delegated) | Subject claim from delegated token | JWT `sub` or `act.sub` (RFC 8693 token exchange) |
| `action` | Resource + HTTP method | Logged by resource server |
| `timestamp` | UTC ISO 8601 | `iat` claim in token + resource server log |
| `ip` or `agent_node` | Agent runtime environment | `X-Forwarded-For` or custom header |

**Constraint:** The `request_id` must be stable across retries of the same logical request — use a correlation ID that survives retry loops, not a new UUID per HTTP attempt.

---

## Auth pattern comparison table

| Auth pattern | When to use | Ping product | Token type | Notes |
|---|---|---|---|---|
| Client credentials (`private_key_jwt`) | Production autonomous agent, no user | PingOne, PingFederate | Short-lived JWT | Default recommendation for agents |
| Client credentials (mTLS) | Regulated or high-assurance agent environments | PingFederate | Short-lived JWT | Requires certificate infrastructure |
| Token exchange (RFC 8693) | Agent acting on behalf of a user (delegated) | PingFederate | Delegated JWT | See `references/curated/workforce-helpdesk-ai.md` |
| Device authorization grant | Agent on constrained device with no browser | PingOne, PingFederate | JWT | Human must complete device flow at enrollment |
| JWT bearer (RFC 7523) | Agent-to-agent trust with pre-established keys | PingFederate | JWT assertion | Agent presents a JWT signed with its private key; AS issues access token |

---

## Pattern 6: Human-in-the-loop (HITL) approvals via CIBA

For high-risk agent actions (fund transfers, privileged access grants), the agent should pause execution and request explicit human approval before proceeding — without requiring the human to be present in the original session.

**CIBA (Client Initiated Backchannel Authentication)** is the OAuth 2.0 pattern for this:

```
AI Agent → CIBA authorization request (POST /bc-authorize)
              → Ping AS sends push notification to user's mobile app
              → User approves or denies on device
              → Ping AS returns approval signal to agent
AI Agent → Token exchange (RFC 8693) for elevated token
AI Agent → Performs high-risk action with HITL-approved token
```

| HITL scenario | Mechanism |
|---|---|
| Fund transfer approval | Agent pauses; CIBA push to approver (user or manager); agent proceeds only on explicit approval |
| Privileged access grant | Same pattern; approver may be the user or a separate admin identity |
| Account disable (admin) | Full admin re-authentication; not delegation |

**CIBA support:** PingFederate (native CIBA endpoint); PingOne AIC (Journey-based backchannel auth). CIBA requires a registered push delivery mechanism (PingID mobile, APNs/FCM push) on the approver's device.

**Constraint:** CIBA polling timeout must be shorter than the agent's operation timeout. If the human does not respond within the CIBA timeout, the authorization is abandoned — the agent must handle this as a failure, not a retry.

## Pattern 7: Bot and agent detection

PingOne Protect's **bot detection predictor** explicitly identifies agentic AI automation, CUAs (computer-using agents), and automated frameworks as high-risk activity. This enables flows to:
- Block agents masquerading as human users
- Flag unexpected agentic activity from known human sessions
- Identify specific agent types in the risk evaluation response

**Integration:** Wire Protect into the authentication flow for any application that handles both human and agent traffic. Branch on `result.recommendation.value`:
- `ALLOW` — proceed normally
- `CHALLENGE` — step-up (or CIBA approval for agents)
- `BLOCK` — deny; agent should not be authenticating through a human flow

**For legitimate non-human flows:** Register agents via `private_key_jwt` client credentials — they bypass the Protect flow entirely. Bot detection fires when an agent incorrectly uses a human-facing authentication endpoint.

See `ping-universal-services` → `protect-configuration.md` for the full bot detection predictor configuration.

---

## Anti-patterns

| Anti-pattern | Risk | Correct alternative |
|---|---|---|
| Long-lived API keys embedded in agent code or config | Key compromise is undetectable; blast radius is unlimited until manual rotation | `private_key_jwt` or mTLS with short-lived tokens |
| Shared token across multiple agent instances | One compromised instance exposes all | One client registration per agent instance or agent type |
| No scope restrictions on agent token | Compromised agent can perform any action the AS allows | Enumerate exact required scopes at registration |
| Refresh tokens with no rotation | Stolen refresh token grants indefinite access | Enable refresh token rotation; short absolute lifetime |
| No `request_id` correlation | Cannot attribute agent actions in audit logs | Add `X-Request-ID` or use `jti` in request-bound tokens |

---

## Prerequisites

- A PingOne (multi-tenant cloud) or AIC environment, or a PingFederate deployment, with an OAuth 2.0 AS configured.
- An application registered in the Ping AS with `client_credentials` grant type enabled.
- For `private_key_jwt`: a JWKS URI registered on the client; the agent holds the corresponding private key.
- For mTLS: X.509 certificate provisioned for the agent; PingFederate mTLS endpoint enabled.
- Resource servers must support Bearer token validation (JWT introspection or local JWT verification with JWKS).

---

## Common variants

| Variant | Notes |
|---|---|
| PingOne (multi-tenant cloud) | Client credentials supported natively; JWKS URI registration available in the app settings |
| PingFederate | Supports `private_key_jwt`, mTLS, and RFC 7523 JWT bearer; dynamic client registration available for agent self-enrollment |
| PingOne AIC | OAuth AS provided by the AIC tenant; same client credentials flow; token introspection endpoint available |
| Multi-agent mesh | Each agent pair has a dedicated client registration; tokens are not shared; each agent's scope is narrowly tailored |

---

## Related references

- `references/curated/identity-for-ai-overview.md`
- `references/curated/verified-trust-overview.md`
- `references/curated/workforce-helpdesk-ai.md`

## Source

- https://docs.pingidentity.com/pingone/ai_agents/p1_ai_agents.html
- https://docs.pingidentity.com/pingoneaic/release-notes/rapid-channel/ai-agents.html
- https://docs.pingidentity.com/pingoneaic/release-notes/rapid-channel/ai-agents-configure-on-behalf-of-authentication-flow.html
- https://docs.pingidentity.com/pingoneaic/release-notes/rapid-channel/ai-agents-configure-dcr-onboarding-flow.html
- https://docs.pingidentity.com/pingone/threat_protection_using_pingone_protect/p1_protect_risk_predictors.html
- https://datatracker.ietf.org/doc/html/rfc8693
- https://datatracker.ietf.org/doc/html/rfc7523
