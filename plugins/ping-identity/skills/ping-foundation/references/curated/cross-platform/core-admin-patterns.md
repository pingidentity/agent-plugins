---
title: "Core Admin Patterns"
product_family: cross-platform
products: ["pingone", "pingone-st", "pingfederate", "pingaccess", "pingdirectory", "pingid"]
capabilities: ["foundation"]
audience: ["admin", "operator"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/pingone/integrations/p1_ldap_gateways.html"
---

# Core Admin Patterns

Recurring administration patterns across PingOne MT, PingOne ST, and Ping Software Suite.

## Scope

Covers: common admin patterns that apply broadly across platforms.
Does NOT cover: deep per-product reference — see generated shortlists for product-specific detail.

---

## Pattern: Connecting an external directory (LDAP/AD)

**Required fields across all platforms:**

| Field | Notes |
|---|---|
| LDAP server URL | Use `ldaps://` (TLS); plain LDAP only acceptable in isolated dev environments |
| Bind DN / principal | Service account with read access; write access required if provisioning back |
| Bind password | Store in a secret/ESV, not plaintext config |
| Base DN | Scope the search to the smallest subtree that contains the target users |
| Username attribute | `uid` for LDAP; `sAMAccountName` for AD |
| User search filter | `(uid=*)` for LDAP; `(&(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))` to exclude disabled AD accounts |

**Admin surfaces:**
- PingOne MT: Connections → External Directories → + Add Directory
- PingOne ST: Realm → Identity Stores → + Add Identity Store (type: LDAP) via AM admin console
- PingFederate: System → Data Stores → + Add Data Store → LDAP

---

## Pattern: Registering an OIDC application

**Required fields across all platforms:**

| Field | Notes |
|---|---|
| Client ID | Unique identifier; auto-generated or custom |
| Client Secret | Required for confidential clients (web apps, M2M); omit for public clients (SPA, native) |
| Redirect URIs | Exact match required; add all environments upfront |
| Grant Types | Authorization Code (web apps), Client Credentials (M2M); avoid Implicit in new apps |
| Scopes | Minimum: `openid`; add `profile`, `email` as needed |

**Client type decision:** confidential (can hold a secret) vs. public (cannot — SPA or native app). Public clients require PKCE.

**Admin surfaces:**
- PingOne MT: Applications → + Add Application → OIDC Web App
- PingOne ST: Realm → Applications → OAuth 2.0 → + Create Client (AIC console) or AM console → OAuth 2.0 → Clients
- PingFederate: Applications → OAuth → Clients → + Add Client

---

## Pattern: API-driven configuration

All platforms expose REST APIs for automation:

| Platform | Base URL pattern |
|---|---|
| PingOne MT | `https://api.pingone.com/v1/environments/{envId}/...` |
| PingOne ST | `https://<tenant>/am/json/...` or `https://<tenant>/openidm/...` |
| PingFederate | `https://<host>:9999/pf-admin-api/v1/...` |
| PingAccess | `https://<host>:9000/pa-admin-api/v3/...` |

**Authentication per platform:**
- PingOne MT: Worker app (client credentials grant)
- PingOne ST: AM OAuth2 client or IDM service account
- PingFederate / PingAccess: HTTP Basic against the admin API (or OAuth2 if configured)

---

## Pattern: Backup and restore

| Platform | Mechanism |
|---|---|
| PingOne MT | Admin API environment export; or use frodo-lib / frodo-cli for config export |
| PingOne ST | Admin API exports; or environment-level export from AIC admin console |
| PingFederate | Server → Archive Configuration (ZIP); Git-backed server profiles recommended |
| PingAccess | System → Backup → Export Configuration |
| PingDirectory | `backup` and `restore` CLI tools |

---

## Pattern: Secret and credential rotation

Rotating client secrets without downtime:

| Step | Notes |
|---|---|
| 1. Generate new secret in the platform | PingOne MT: app → Client Secret → Rotate; PingFederate: client record → regenerate secret |
| 2. Configure retention window | Keep old secret valid for a rolling period (grace period) while consumers update |
| 3. Update consumers (apps, pipelines) | Deploy new secret to all services using the client |
| 4. Verify old secret is no longer in use | Check access logs for tokens issued with old client secret |
| 5. Remove old secret (or let it expire) | After all consumers are updated |

For PingOne MT Worker apps: the secret can be retrieved only at creation time; if lost, rotate immediately.

---

## Pattern: Monitoring and health checks

| Platform | Health check endpoint |
|---|---|
| PingOne MT | No direct health check endpoint; use OIDC discovery document to verify availability: `https://auth.pingone.com/<envId>/as/.well-known/openid-configuration` |
| PingOne ST | AM health: `https://<tenant>/am/json/health/live`; IDM health: `https://<tenant>/openidm/info/ping` |
| PingFederate | `https://<host>:9031/pf/heartbeat.ping` (returns HTTP 200 with body `SERVER_ALIVE`) |
| PingAccess | `https://<host>:3000/pa/heartbeat.ping` (engine node; requires PA version-specific path) |
| PingDirectory | `bin/status` CLI; or LDAP search on `cn=monitor` for operational data |

---

## Pattern: Audit log access

| Platform | Audit log access |
|---|---|
| PingOne MT | Admin console → Reports → Audit; or Admin API `GET /v1/environments/{envId}/activities` |
| PingOne ST | AM audit log: `https://<tenant>/am/json/audit/access`; IDM audit: `/openidm/audit/access` |
| PingFederate | Log files in `<pf-home>/log/` — `audit.log`, `server.log`; or syslog forward |
| PingAccess | Log files in `<pa-home>/log/` — `audit.log`; or syslog forward |
| PingDirectory | `<pd-home>/logs/access` — LDAP access log; filterable by operation type |

## Prerequisites

Admin access to the relevant platform: PingOne organization admin, PingOne ST superadmin, or server administrator credentials for on-premises products.

## Common variants

| Variant | Note |
|---|---|
| API-only configuration | Prefer the REST API for all platforms; use the admin UI only for initial bootstrapping or when an API endpoint is not available |
| Console-driven configuration | Use for one-off tasks, diagnostics, or platform features not yet exposed via API |
| Config-as-code (Ping Software Suite) | Use server profiles (Git-backed) for PingFederate and PingAccess; use frodo-cli for PingOne MT/ST exports |

## Related references

- `references/curated/cross-platform/foundation-overview.md`
- `references/curated/cross-platform/tenant-and-environment-setup.md`

## Source

[PingOne API Reference](https://apidocs.pingidentity.com/pingone/platform/v1/api/)
[PingFederate Admin API](https://docs.pingidentity.com/pingfederate/latest/admin-api-reference/pf-admin-api-reference.html)
[PingAccess Admin API](https://docs.pingidentity.com/pingaccess/latest/pa-admin-api/pa-admin-api.html)
[PingDirectory Admin Guide](https://docs.pingidentity.com/pingdirectory/latest/pd-directory-server-administration-guide/pd-ds-admin-overview.html)
