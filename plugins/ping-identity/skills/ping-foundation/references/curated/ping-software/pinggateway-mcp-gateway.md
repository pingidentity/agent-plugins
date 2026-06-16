---
title: "PingGateway — MCP Security Gateway Deployment and Configuration"
product_family: ping-software
products: ["pinggateway", "pingone-aic", "pingone", "pingfederate"]
capabilities: ["foundation", "identity-for-ai"]
services: []
audience: ["developer", "architect", "admin"]
use_cases: ["ai-identity"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-16"
slug: "https://docs.pingidentity.com/pinggateway/2026/mcp/index.html"
---

# PingGateway — MCP Security Gateway Deployment and Configuration

How to deploy and configure PingGateway as an MCP security gateway in front of one or more existing MCP servers. Covers route patterns, token validation, token exchange, Docker/Kubernetes deployment, PingAuthorize integration, and troubleshooting.

For the conceptual overview (what the Agent Gateway module does, filter responsibilities, OAuth AS selection, version requirements), see `ping-identity-for-ai/references/curated/agent-gateway-mcp.md`.

## Scope

**Covers:** Topology decisions, route patterns (single server and multi-server), inbound token validation (PingAM stateless JWT and introspection), token exchange, API key backend hop, Docker localhost deployment, Kubernetes deployment, PingAuthorize/PingOne Authorize integration (2026+), common gotchas, and implementation workflow.

**Does NOT cover:** OAuth AS setup (PingOne, AIC, PingFederate) — see `ping-foundation`. Agent token scoping and client credentials patterns — see `ping-identity-for-ai/references/curated/agent-security-patterns.md`.

---

## What PingGateway MCP gateway is

PingGateway's Agent Gateway module sits between an AI agent (MCP client) and one or more MCP servers, acting as a centralized security enforcement proxy. It validates Bearer tokens, enforces OAuth 2.0 scope and resource indicator requirements (RFC 8707), audits every agent request, and optionally applies fine-grained policy via PingOne Authorize or PingAuthorize — all without requiring any security code in the MCP servers themselves.

The key operational consequence: PingGateway owns the well-known OAuth 2.0 protected resource registration for MCP endpoints. This creates a single-registration constraint that determines how routes are structured when multiple MCP servers are protected by the same gateway instance.

---

## Version requirements

| PingGateway version | MCP support status |
|---|---|
| 2026.3.0+ (2026.x train) | MCP gateway + Agent Gateway module GA; PingAuthorize integration available |
| 2025.11.1–2025.11.2 (2025.x train) | MCP gateway available; no PingAuthorize filter |
| Earlier than 2025.11.1 | No MCP support |

Use the 2026.x train for new deployments. The Agent Gateway module has **Evolving interface stability** — plan for configuration updates when upgrading PingGateway.

---

## Four decisions before configuring

| Decision | Options |
|---|---|
| **Topology** | Single MCP server vs. multiple MCP servers |
| **Deployment** | Docker localhost vs. Kubernetes |
| **Inbound token validation** | PingAM stateless JWT vs. non-AM token introspection |
| **Policy layer** | None, PingOne Authorize (P1AZ), or standalone PingAuthorize (PAZ) — requires 2026+ |

---

## Filter chain — single MCP server

```
admin.json: "streamingEnabled": true  ← required for SSE-based MCP servers

UriPathRewriteFilter
  → McpProtectionFilter          (validates Bearer token, registers well-known endpoint)
  → McpValidationFilter          (validates MCP message format, rewrites protocol version)
  → [PingAuthorizeFilter]        (optional; 2026+ only; MUST run before McpValidationFilter)
  → [OAuth2TokenExchangeFilter]  (optional; exchange inbound token for backend token)
  → ReverseProxyHandler
```

**Key constraint:** `McpProtectionFilter.resourceId` must equal the public HTTPS gateway URL. The inbound token `aud` claim must match this value exactly.

---

## Inbound token validation

### PingAM stateless JWT

PingGateway validates the JWT locally against the AIC/AM JWKS endpoint — no introspection round-trip per request. Only available when PingAM or AIC is the OAuth AS.

### Non-AM token introspection (rsFilter heap pattern)

Use when the AS is PingFederate, PingOne, or any non-AM issuer. Requires these heap objects:

| Heap object | Type |
|---|---|
| `IntrospectionProviderHandler` | Chain: `ClientSecretBasicAuthenticationFilter` + `ClientHandler` |
| `RsFilterTokenResolver` | `TokenIntrospectionAccessTokenResolver` referencing the handler |
| `rsFilter` | `OAuth2ResourceServerFilter` referencing the resolver |

Reference `rsFilter` in the filter chain as a **bare string** — inline object instantiation can re-trigger registration conflicts.

---

## Backend hop authentication

### Token exchange (OAuth2TokenExchangeFilter)

Use when the backend MCP server requires a different token than the one the agent presented inbound.

**Required heap objects:**

| Heap object | Type |
|---|---|
| `SecretsStore` | `SystemAndEnvSecretStore` with `format: PLAIN` |
| `TokenExchangeEndpointHandler` | Chain: `ClientSecretBasicAuthenticationFilter` + `ClientHandler` |
| `TokenExchangeFailureHandler` | `StaticResponseHandler` (401) |

**Secret ID naming with format PLAIN:** dots become underscores, letters uppercased.
- `te.client.secret` → `TE_CLIENT_SECRET`
- `oauth.introspect.client.secret` → `OAUTH_INTROSPECT_CLIENT_SECRET`

### API key backend hop (skip token exchange)

When the backend uses a static API key instead of a Bearer token, skip `OAuth2TokenExchangeFilter` entirely:
- Use `HeaderFilter` to remove `Authorization` and inject `X-Api-Key`
- Store key in a Kubernetes Secret or env var; reference via `secretKeyRef`

**Filter chain:** `UriPathRewriteFilter → rsFilter → McpValidationFilter → HeaderFilter → ReverseProxyHandler`

---

## Multiple MCP server route patterns

### Pattern A — Path-based split (preferred)

One route per backend: `/mcp/server-a`, `/mcp/server-b`, etc. Each route has its own backend URL, audience, scope, and optional exchange config. Preferred because it requires no host-routing infrastructure.

### Pattern B — Host-based split

Only use if the existing architecture already routes by hostname.

### Primary vs. secondary routes — critical constraint

`McpProtectionFilter` registers a `/.well-known/oauth-protected-resource/<path>` endpoint. **Only one route in the gateway may use it.** A second route using `McpProtectionFilter` throws `AlreadyRegisteredException` at startup.

| Route type | Filter used | Notes |
|---|---|---|
| Primary | `McpProtectionFilter` | Owns the well-known OAuth registration |
| Secondary | `rsFilter` (named `OAuth2ResourceServerFilter`) | Direct RS filter; no well-known registration |

**Primary route condition** — use a negative lookahead to exclude secondary paths so both routes can coexist:
```
"condition": "${find(request.uri.path, '^/mcp(?!/server-b)')}"
```

**Secondary route filter chain:**
```
UriPathRewriteFilter → "rsFilter" → [PingAuthorizeFilter] → McpValidationFilter → [HeaderFilter / OAuth2TokenExchangeFilter] → ReverseProxyHandler
```

---

## Docker localhost deployment

| Requirement | Detail |
|---|---|
| Config mounting | Mount config directory as a volume; do not rebuild image for config changes |
| Secrets | Pass as environment variables; reference via `SystemAndEnvSecretStore` |
| Minimum assets | `admin.json` (with `streamingEnabled: true`), route JSON, optional `logback.xml`, optional `.env` |
| Streaming | Docker Compose: expose gateway port; verify `streamingEnabled` in `admin.json` |

---

## Kubernetes deployment

### PingGateway image

No public image exists. Build from the distribution's `docker/` directory Dockerfile and push to an accessible registry. Detect the actual instance directory from existing manifests — do not assume `.openig`.

### Secrets and ConfigMaps

| Resource type | What to store |
|---|---|
| ConfigMap | Non-secret files: route JSON, `admin.json`, `logback.xml` |
| Kubernetes Secret | Credentials **and** non-secret URLs (token endpoints, introspection endpoints) — use `secretKeyRef` consistently; do not mix with plain `value:` entries |

### Required Deployment fields

- `spec.selector.matchLabels` and `spec.template.metadata.labels` must both be present and match exactly.
- An `emptyDir` volume at the instance root (e.g. `/var/gateway`) is **always required** alongside ConfigMap mounts for individual files — omitting it causes startup failure.

### Backend target

Prefer internal Service DNS (`http://mcp-server-svc`) over the public ingress hostname to avoid routing loops and ingress complications.

---

## PingAuthorize / PingOne Authorize integration

**Requires PingGateway 2026 or later.**

### Filter placement — critical

`PingAuthorizeFilter` **must run before `McpValidationFilter`**. `McpValidationFilter` consumes the request body stream. If P1AZ/PAZ runs after it, the policy engine receives an empty body and cannot evaluate tool-level decisions.

### Configuration

| Field | Notes |
|---|---|
| `gatewayServiceUri` | Must use `&{VARNAME}` property substitution, not `${env['VARNAME']}`. Validated as `java.net.URI` at route build time; runtime EL causes `URISyntaxException`. |
| `P1AZDenyHandler` | `StaticResponseHandler` (403) required in every route using the filter |
| P1AZ URI source | Console → Authorization → API gateways → Service URL |
| PAZ standalone URI | `http://<paz-host>:<paz-sideband-port>` (default sideband port: 6080) |

### Body forwarding

Setting `"includeBodyContentTypes": ["application/json"]` forwards the full JSON-RPC body to the policy engine, enabling decisions on MCP method (`tools/call`, `tools/list`), tool name (`params.name`), and full arguments (`params.arguments`). Without this, policy can only evaluate token claims and URL path. Latency impact is negligible for typical MCP payloads; no effect on GET/SSE requests.

---

## Common gotchas

| Gotcha | Symptom | Fix |
|---|---|---|
| Inbound token `aud` mismatch | 401 on all MCP requests despite valid token | Verify `McpProtectionFilter.resourceId` matches the public gateway HTTPS URL; confirm RFC 8707 resource indicator script on the AS |
| Second route uses `McpProtectionFilter` | Gateway fails to start: `AlreadyRegisteredException` | Secondary routes must use `rsFilter` (`OAuth2ResourceServerFilter`) directly, not `McpProtectionFilter` |
| Secret ID contains dots | Token exchange or introspection fails with secret lookup error | Convert dots to underscores and uppercase with `format: PLAIN` (e.g. `te.client.secret` → `TE_CLIENT_SECRET`) |
| `PingAuthorizeFilter` after `McpValidationFilter` | P1AZ/PAZ receives empty body; policy denies all tool calls | Move `PingAuthorizeFilter` before `McpValidationFilter` in the filter chain |
| `gatewayServiceUri` uses `${env[...]}` EL | Route fails to load: `URISyntaxException` | Use `&{VARNAME}` property substitution instead |
| Missing `emptyDir` volume in Kubernetes | PingGateway container crashes at startup | Add `emptyDir` volume at the instance root alongside ConfigMap mounts |
| Backend target is public ingress hostname | 401 responses loop back through gateway; routing loop | Use internal Kubernetes Service DNS instead of public hostname |
| `streamingEnabled` not set in `admin.json` | SSE connections drop immediately | Set `"streamingEnabled": true` in `admin.json` |
| `capture: "all"` in production config | Full Bearer tokens logged in plaintext | Remove `capture: "all"`; use targeted logging levels for debug |

---

## Prerequisites

- PingGateway 2025.11.1+ or 2026.x installed and network-accessible from AI agent clients
- `admin.json` with `"streamingEnabled": true` (required for SSE-based MCP servers)
- OAuth AS (AIC, PingOne, or PingFederate) with RFC 8707 Resource Indicators support enabled
- MCP server(s) accessible from PingGateway
- Agent client credentials registered on the OAuth AS
- For AIC: OAuth 2.0 Access Token Modification script configured to include the RFC 8707 resource indicator in the token

---

## Common variants

| Variant | Notes |
|---|---|
| Single MCP server (Docker) | One route with `McpProtectionFilter`; secrets via env vars; config mounted as a volume |
| Single MCP server (Kubernetes) | ConfigMap + Secret; `emptyDir` at instance root; internal Service DNS as backend target |
| Multiple MCP servers (path-split) | One primary route with `McpProtectionFilter`; secondary routes with `rsFilter`; negative lookahead on primary condition |
| API key backend | Replace token exchange with `HeaderFilter` injecting `X-Api-Key`; remove `Authorization` header before forwarding |
| PingOne Authorize (P1AZ) | `PingAuthorizeFilter` before `McpValidationFilter`; `includeBodyContentTypes: ["application/json"]` for tool-level decisions; 2026+ only |
| Standalone PingAuthorize (PAZ) | Same as P1AZ but `gatewayServiceUri` points to PAZ sideband port (6080) |

---

## Implementation workflow

1. Inspect existing Deployment/Compose manifests, Services, Ingress, image, config paths, and token provider
2. Choose route pattern: single server or path-based split per backend
3. Choose inbound token validation: PingAM stateless JWT or non-AM introspection
4. Choose backend hop auth: OAuth 2.0 token exchange or API key `HeaderFilter`
5. Choose backend target: local container hostname or internal Kubernetes Service DNS
6. Generate deployable files with full contents, environment variable list, and secret names
7. Add validation steps: startup log checks, `curl` / Postman verification, rollout commands, troubleshooting notes for the chosen topology

---

## Related references

- `ping-identity-for-ai/references/curated/agent-gateway-mcp.md` — module overview, three MCP filters, OAuth AS choices, version matrix
- `references/curated/ping-software/pingfederate-basics.md` — PingFederate as OAuth AS for inbound token validation
- `ping-identity-for-ai/references/curated/agent-security-patterns.md` — token scoping, client credentials, revocation

---

## Source

- https://docs.pingidentity.com/pinggateway/2026/mcp/index.html
- https://docs.pingidentity.com/pinggateway/2026/reference/McpProtectionFilter.html
- https://docs.pingidentity.com/pinggateway/2026/reference/McpValidationFilter.html
- https://docs.pingidentity.com/pinggateway/2026/reference/McpAuditFilter.html
- https://docs.pingidentity.com/pinggateway/2026/reference/PingAuthorizeFilter.html
- https://docs.pingidentity.com/pinggateway/2026/gateway-guide/oauth2-rs-introspect.html
- https://docs.pingidentity.com/pinggateway/2026/gateway-guide/token-exchange.html
- https://docs.pingidentity.com/pinggateway/release-notes/whats-new.html
