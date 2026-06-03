---
title: "PingAccess — Administration Basics"
product_family: ping-software
products: ["pingaccess"]
capabilities: ["foundation"]
services: []
audience: ["admin", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/pingaccess/9.0/pa_landing_page.html"
---

# PingAccess — Administration Basics

Reverse-proxy policy enforcement point that protects web applications and APIs by validating tokens issued by a connected authorization server before forwarding requests to backend sites.

## Scope

**Covers:** PingAccess deployment models, core entities (Virtual Host, Site, Application, Web Session, Resource, Rule), token provider setup, end-to-end web app and API protection configuration, common gotchas.
**Does NOT cover:** PingFederate federation configuration (see `references/curated/ping-software/pingfederate-basics.md`), PingDirectory (separate anchor), OAuth/OIDC client design on PingOne MT/ST (ping-foundation MT/ST anchors), PingID MFA configuration.

---

## What PingAccess is

PingAccess is a reverse proxy and policy enforcement point. It sits in front of web applications and APIs, intercepts inbound requests, and enforces authentication and authorization based on tokens issued by a connected authorization server — PingFederate, PingOne, or PingOne Advanced Identity Cloud. PingAccess does not issue tokens; it validates them via introspection or JWT signature verification, then either forwards the request to the backend site or rejects/redirects the caller.

---

## Core architecture

| Component | Role |
|---|---|
| Token Provider (PingFederate or PingOne) | Issues tokens; PingAccess validates them via introspection or JWKS-based JWT verification |
| Virtual Host | Hostname:port that PingAccess listens on for inbound client requests |
| Site | Backend target URL (upstream application or API server) |
| Application | Maps a virtual host + context root to a site; access policies and rules attach here |
| Resource | Path-level rule entry within an application; controls which URL patterns require which level of authentication |
| Web Session | OIDC-based cookie session for browser flows; manages token acquisition and lifecycle |
| Access Token Validator (ATV) | Validates OAuth bearer tokens for API protection flows |
| Rule / Rule Set | Access control logic (OAuth scope checks, header assertions, network range, time range, Groovy scripts) |
| Identity Mapping | Passes identity attributes downstream to the backend as HTTP headers or JWTs |
| Agent | Lightweight module (Apache, NGINX, IIS, Java SDK) that offloads policy decisions to a PingAccess policy server without a full proxy hop |

---

## Deployment models

| Model | Description | Pros | Cons |
|---|---|---|---|
| Gateway | PingAccess proxies all traffic; enforces policy before forwarding to backend | Full feature set; centralized audit logging; simplest troubleshooting | Requires network restructuring; adds a request hop |
| Agent | Lightweight module on the web server coordinates with PA policy server | No network changes; cached decisions can reduce latency | Per-server maintenance; agents must be upgraded independently; URL/response rewriting unavailable |
| Sideband | API gateway (Kong, Apigee) makes a backchannel call to PA for policy decisions | No network changes; centralized logging | Integration kits must be maintained per gateway; feature availability depends on gateway |

Gateway is the recommended starting point for new deployments. Use Agent or Sideband when network topology prevents a proxy insertion.

---

## Setup sequence — protecting a web app (gateway)

Steps must be completed in this order; later steps depend on objects created earlier.

| Step | Object | Key fields |
|---|---|---|
| 1 | **Token Provider** | Connection to PingFederate or PingOne; issuer URL; trusted certificate group; introspection endpoint or JWKS URI |
| 2 | **Site** | Name; Targets (`hostname:port`); Secure (HTTPS requires Trusted Certificate Group); Load Balancing Strategy |
| 3 | **Virtual Host** | Host (e.g., `app.corp.com`); Port (e.g., `443`); TLS certificate association |
| 4 | **Web Session** | Name; Cookie Type; Audience; Client ID; Client Credentials; Idle Timeout; Max Timeout |
| 5 | **Rule** (optional) | Name; Type (e.g., OAuth Scope, HTTP Request Header); assertion logic |
| 6 | **Identity Mapping** (optional) | Name; Type (Header Identity Mapping); Attribute → Header mapping |
| 7 | **Application** | Name; Context Root (starts `/`, no trailing `/`); Virtual Host; Application Type = Web; Web Session; Destination = Site |
| 8 | **Resource** | Path Patterns (start `/`); Resource Authentication = Standard or Anonymous; Methods |

**Verification:** Access the virtual host URL without a session; PingAccess should redirect the browser to the authorization server login page.

---

## Web session configuration

| Field | Recommended value | Notes |
|---|---|---|
| Cookie Type | Encrypted JWT | Authenticated encryption (confidentiality + integrity + authenticity); default |
| Audience | Match RP client ID or agreed string (1–32 chars) | Tokens not matching this value are rejected and trigger reauthentication |
| OpenID Connect Login Type | Code | Standard authorization code flow; most compatible |
| Idle Timeout | 30–60 min | Resets on activity; default is 60 min |
| Max Timeout | 8–12 h for workforce | Absolute limit regardless of activity; default is 240 min |
| Cookie Domain | `.parent-domain.com` | Set to parent domain for multi-subdomain apps; omitting causes per-host token regeneration |
| Secure Cookie | `true` in all production environments | Must be HTTPS or authentication fails |
| HTTP-Only Cookie | `true` | Blocks JavaScript access to session cookie |
| SameSite | Lax (default) | Use `None` only for cross-site API consumers requiring cookies |
| Enable PKCE | `true` (default) | SHA-256 code challenge; do not disable |
| Cache User Attributes | Enable if cookie size approaches 4096 bytes | Stores attributes server-side; reduces cookie payload |

---

## API protection vs. web app protection

| Scenario | Use Web Session? | Token validation method | Auth challenge response |
|---|---|---|---|
| Browser app (user-facing) | Yes | OIDC authorization code flow; Web Session manages cookie lifecycle | Redirect to AS login page |
| API — machine-to-machine | No | JWT bearer validation (local JWKS) or token introspection | 401 / 403 |
| API — SPA with bearer token | No | JWT bearer validation or introspection via ATV | 401 / 403 |
| Mixed app (browser routes + API routes) | Conditional | Web Session for `/app/*` paths; Bearer/ATV for `/api/*` paths | Per route type |

For API protection: create Application Type = **API**, configure an Access Token Validator under Access > Token Validation, and attach it to the application. Introspection requires a configured introspection endpoint in the token provider.

---

## Token provider configuration

Two validation modes; choose based on token type and latency requirements.

| Mode | Mechanism | Token types supported | Latency | Configuration |
|---|---|---|---|---|
| Introspection | PingAccess calls AS `/introspect` per request | Opaque tokens and JWTs | Higher (network call per request) | Token Provider > introspection endpoint URL + client credentials |
| JWT verification | PingAccess validates JWT locally using JWKS | JWTs only | Lower (no per-request network call) | Token Provider > JWKS URI; AS must publish JWKS endpoint |

**PingFederate token provider — required configuration objects on the PF side (in order):**

1. Password credential validator
2. IdP adapter
3. Default scope definition
4. Access token manager
5. IdP adapter mapping and access token mapping
6. OpenID Connect policy
7. Resource server client (grant type: Access Token Validation)
8. Web session client (used for browser OIDC flows in PA)

After PF configuration: export PF runtime certificate → import into PA → add to Trusted Certificate Group → configure Settings > Token Provider > PingFederate Runtime.

**Constraint:** Saving a new PingFederate runtime configuration overwrites any existing one. There is no merge.

---

## Common gotchas

| Gotcha | Symptom | Fix |
|---|---|---|
| Token introspection endpoint not configured | 401 on every request despite valid session | Verify introspection endpoint URL and client credentials under Token Provider; check connectivity from PA to AS |
| Web session cookie domain too narrow | Login loop when navigating between subdomains | Set Cookie Domain to `.parent-domain.com`; invalid domain value causes endless reauthentication |
| Site URL missing context root | 404 on all requests forwarded to backend | Verify Site Targets includes any required base path; context root in the Application is a listener path, not forwarded to backend unless the site URL accounts for it |
| CORS errors on API routes | API clients receive CORS rejection | PingAccess does not add CORS headers automatically; add a Cross-Origin Request Rule explicitly; do not use wildcard `*` in Allowed Origins (insecure) |
| Expired web session not refreshing | Users see repeated login prompts | Check Max Timeout vs. refresh token expiry; enable "Validate Session" if PF session state synchronisation is needed |
| Cookie size exceeds 4096 bytes | Browser silently drops cookie; session lost | Disable "Send Token" on Site; enable "Cache User Attributes" in Web Session; simplify crypto algorithms (ECDSA P-256, AES-128-CBC+HMAC-SHA256) |
| Secure Cookie enabled in non-HTTPS environment | Authentication always fails | Disable Secure Cookie in dev/non-TLS environments; never disable in production |
| Context Root `/pa` conflicts | Application fails to save or path unreachable | `/pa` is reserved for PingAccess internal resources; choose a different context root or enable "Use context root as reserved resource base path" in advanced settings |
| API app type introspection not available | Error: "Cannot use remote validation as authorization server does not have an Introspection endpoint" | Configure introspection endpoint in PF OAuth settings; ensure the resource server client has the correct grant type |
| PF runtime config overwritten | Existing PF token provider configuration disappears | Saving a new PingFederate runtime configuration is destructive; back up existing config before making changes |

---

## Prerequisites

- PingAccess 9.x license installed
- Java 17 JRE (verify version matrix for target release)
- A configured token provider: PingFederate (minimum 10.x for authentication policies), PingOne, or PingOne AIC
- TLS certificate for the Virtual Host listener; trusted certificate group for backend Site if Site uses HTTPS
- OAuth client credentials (Client ID + Secret or Mutual TLS key pair) registered on the token provider for the Web Session

---

## Common variants

| Variant | Note |
|---|---|
| High availability (HA) | Multiple PA engine nodes behind a load balancer; shared operational database (PostgreSQL); console node separate from engine nodes |
| Agent-based deployment | Deploy PA agents on Apache, NGINX, or IIS when full proxy insertion is not possible; agents offload policy decisions to a central PA policy server |
| Sideband with Kong or Apigee | PA acts as a policy decision point; API gateway integration kit makes backchannel calls; no proxy hop required |
| Container / Kubernetes | Environment variable overrides for all configuration settings; recommended with PingAccess server profile (Git-backed config) |
| FIPS mode | Supported; restricts available crypto algorithms; verify token provider crypto compatibility before enabling |

---

## Related references

- `references/curated/ping-software/pingfederate-basics.md` — PingFederate adapter chains, SP/IdP connections, OAuth client configuration
- `references/curated/cross-platform/foundation-overview.md`
- `references/curated/cross-platform/core-admin-patterns.md`

---

## Source

[PingAccess 9.0 Landing Page](https://docs.pingidentity.com/pingaccess/9.0/pa_landing_page.html)
[How PingAccess works](https://docs.pingidentity.com/pingaccess/9.0/introduction_to_pingaccess/pa_how_does_pa_work.html)
[Choosing a deployment model](https://docs.pingidentity.com/pingaccess/9.0/introduction_to_pingaccess/pa_choose_a_deployment_model.html)
[Creating web sessions](https://docs.pingidentity.com/pingaccess/9.0/pingaccess_user_interface_reference_guide/pa_creating_web_sessions.html)
[Advanced web session settings](https://docs.pingidentity.com/pingaccess/9.0/pingaccess_user_interface_reference_guide/pa_advanced_web_session_settings.html)
[Application field descriptions](https://docs.pingidentity.com/pingaccess/9.0/pingaccess_user_interface_reference_guide/pa_application_field_descriptions.html)
[Site field descriptions](https://docs.pingidentity.com/pingaccess/9.0/pingaccess_user_interface_reference_guide/pa_site_field_descriptions_ref.html)
[Protecting a web app (gateway)](https://docs.pingidentity.com/pingaccess/9.0/pingaccess_use_cases/pa_protecting_a_web_app_with_pa_in_a_gateway_deployment.html)
[Protecting an API (gateway)](https://docs.pingidentity.com/pingaccess/9.0/pingaccess_use_cases/pa_protecting_an_api_with_pa_in_a_gateway_deployment.html)
[Minimizing cookie size](https://docs.pingidentity.com/pingaccess/9.0/troubleshooting/pa_minimizing_the_pa_cookie_size.html)
