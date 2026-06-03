---
title: "Agent Gateway — Securing MCP Servers with PingGateway"
product_family: cross-platform
products: ["pinggateway", "pingone-aic", "pingone", "pingfederate"]
capabilities: ["identity-for-ai"]
services: []
audience: ["developer", "architect"]
use_cases: ["ai-identity"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-03"
slug: "https://docs.pingidentity.com/pinggateway/2026/mcp/index.html"
---

# Agent Gateway — Securing MCP Servers with PingGateway

How to use PingGateway's Agent Gateway module as an MCP security gateway — protecting Model Context Protocol servers from unauthorized AI agent access using OAuth 2.0 resource server semantics.

## Scope

**Covers:** What the Agent Gateway module does, the three MCP filters (McpAuditFilter, McpProtectionFilter, McpValidationFilter), OAuth AS choices, RFC 8707 resource indicator requirement, version requirements, and architecture placement.

**Does NOT cover:** OAuth 2.0 AS configuration (PingOne, AIC, PingFederate) — see `ping-foundation`. Agent token scoping and client credentials patterns — see `references/curated/agent-security-patterns.md`. DaVinci flow design — see `ping-orchestration`.

> **Stability note:** The Agent Gateway module has **Evolving interface stability** — it is subject to change without notice even in minor or maintenance releases. Plan for configuration updates when upgrading PingGateway.

---

## What the Agent Gateway module does

MCP (Model Context Protocol) is an open standard for connecting AI agents to servers that expose tools and data. Without a security layer, MCP servers must implement their own OAuth 2.0 validation, audit logging, and throttling — inconsistently, per server.

PingGateway's Agent Gateway module sits between the MCP client (AI agent) and the MCP server, acting as a centralized security proxy. A single PingGateway route protects every MCP server behind it without requiring per-server security code.

```
AI Agent (MCP client)
  │
  ▼
PingGateway (Agent Gateway module)
  ├─ McpValidationFilter  — validates MCP message format + protocol version
  ├─ McpProtectionFilter  — enforces OAuth 2.0 Bearer token, binds resource scopes (RFC 8707)
  └─ McpAuditFilter       — records structured audit trail of all agent requests
  │
  ▼
MCP Server (backend tools / data)
```

PingGateway acts as an **OAuth 2.0 resource server** (RS). It validates access tokens issued by the configured AS, enforces coarse-grained access control, and passes authorized requests to the MCP server.

---

## The three MCP filters

### McpProtectionFilter

Enforces OAuth 2.0 security on inbound MCP requests.

| Responsibility | Detail |
|---|---|
| Bearer token validation | Validates the agent's access token against the configured OAuth AS (introspection or local JWT verification) |
| Resource indicator binding (RFC 8707) | Binds the scope check to the specific MCP resource server; prevents token reuse across services |
| Coarse-grained access control | Enforces scope requirements; grants or denies access based on token claims |
| Token introspection caching | Caches introspection results to reduce per-request AS calls |

**RFC 8707 requirement:** The OAuth AS must support Resource Indicators (RFC 8707). For AIC, an OAuth 2.0 Access Token Modification script must be configured to include the resource indicator in the token. Tokens without the correct resource indicator are rejected.

### McpValidationFilter

Validates the structure and version of inbound MCP messages.

| Check | Detail |
|---|---|
| MCP client message format | Validates message structure, excluding tool schemas |
| Protocol version rewrite | Rewrites the `initialize` request to PingGateway's supported MCP protocol version (`2025-06-18`) |
| SSE support | If the MCP server uses server-sent events (SSE), enable streaming in PingGateway |

### McpAuditFilter

Records centralized audit trail entries for all MCP agent requests.

| Audit field | Source |
|---|---|
| Agent identity | Extracted from the validated access token (`sub` or `client_id`) |
| MCP action | Tool called, resource accessed |
| Timestamp | PingGateway request time (UTC) |
| Outcome | Success / failure / authorization denial |

Configure `McpAuditFilter` with an `AuditService` reference defined in the PingGateway heap. Both `AuditService` inline and named references are supported.

---

## OAuth AS choices

PingGateway works with any OAuth 2.0 AS. For MCP protection, the three Ping-native options are:

| AS | Use when |
|---|---|
| **PingOne Advanced Identity Cloud (AIC)** | AIC-managed workloads; agent registered as AIC AI Agent client (`/aiagent/register`); Journey-based step-up available |
| **PingOne MT** | Cloud-first; PingOne OAuth AS; agent registered as a Worker application |
| **PingFederate** | On-premises or hybrid; PingFederate AS with RFC 8707 resource indicator support; supports `private_key_jwt` and mTLS |

All three require RFC 8707 support on the AS side. Verify before deployment.

---

## Architecture placement

```
[AI Agent]
  └─ MCP request + Bearer token
       ↓
[PingGateway — Agent Gateway module]
  ├─ Introspect / validate token → [OAuth AS: AIC / PingOne / PingFederate]
  ├─ Check resource indicator (RFC 8707) scope
  ├─ Audit log entry
  └─ Forward if valid
       ↓
[MCP Server — backend tools/data]
```

**PingGateway as reverse proxy:** PingGateway intercepts all traffic to the MCP server. The MCP server requires no OAuth logic; it trusts requests that pass through PingGateway.

**Multiple MCP servers:** Deploy one PingGateway route per MCP server endpoint. Each route uses the same filter configuration pattern with server-specific resource indicators.

---

## Version requirements

| PingGateway version | MCP support status |
|---|---|
| 2026.3.0 (2026.x train — current) | MCP gateway + Agent Gateway module GA |
| 2025.11.2 (2025.x train — latest maintenance) | MCP gateway available (introduced 2025.11.1) |
| Earlier than 2025.11.1 | No MCP support |

Use the 2026.x train for new deployments. The 2025.11.x train remains supported under the 2025 maintenance schedule.

The Agent Gateway module is independent of other PingGateway modules — no other modules are prerequisites.

---

## Common failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| 401 on all MCP requests | Bearer token missing or expired | Verify agent requests include `Authorization: Bearer <token>`; check AS token TTL |
| 403 after token validation | Resource indicator scope mismatch | Confirm RFC 8707 resource indicator in token matches the MCP server's registered resource; check AS script |
| Protocol version error from MCP server | MCP protocol version mismatch | McpValidationFilter rewrites to `2025-06-18`; verify MCP server supports this version |
| Audit records missing | McpAuditFilter not in route, or AuditService misconfigured | Verify filter order and AuditService heap reference |
| SSE connections dropping | Streaming not enabled in PingGateway | Enable streaming in the PingGateway route for SSE-based MCP servers |

---

## Prerequisites

- PingGateway 2025.11.1+ or 2026.x installed and network-accessible from AI agent clients
- OAuth AS (AIC, PingOne, or PingFederate) with RFC 8707 Resource Indicators support enabled
- MCP server accessible from PingGateway
- Agent client registration completed (see `references/curated/agent-security-patterns.md`)
- For AIC: OAuth 2.0 Access Token Modification script configured to support RFC 8707

## Common variants

| Variant | Notes |
|---|---|
| Multiple MCP servers | One route per server; same filter pattern; different resource indicators per server |
| PingOne Authorize integration | Add PingOne Authorize call inside the route for fine-grained ABAC policy on top of OAuth scope control |
| PingOne Protect integration | Add Protect evaluation in the route to detect agentic bot activity and block high-risk agent requests |
| Cloudflare Workers MCP server | PingGateway route proxies to Cloudflare Workers endpoint; same token validation applies |
| AWS Bedrock agents | Bedrock agent obtains token via client credentials; PingGateway validates before forwarding to MCP tools |

## Related references

- `references/curated/agent-security-patterns.md` — token scoping, client credentials, revocation
- `references/curated/identity-for-ai-overview.md` — 5-pillar ID4AI architecture
- `references/curated/workforce-helpdesk-ai.md` — delegation and HITL patterns

## Source

- https://docs.pingidentity.com/pinggateway/2026/mcp/index.html
- https://docs.pingidentity.com/pinggateway/2026/reference/McpAuditFilter.html
- https://docs.pingidentity.com/pinggateway/2026/reference/McpProtectionFilter.html
- https://docs.pingidentity.com/pinggateway/2026/reference/McpValidationFilter.html
- https://docs.pingidentity.com/platform/8/platform-guide/edge-security.html
- https://developer.pingidentity.com/identity-for-ai/release-notes/idai-whats-new.html
- https://docs.pingidentity.com/pinggateway/release-notes/whats-new.html
