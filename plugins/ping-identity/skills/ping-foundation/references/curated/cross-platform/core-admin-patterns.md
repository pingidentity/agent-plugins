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
last_updated: ""
slug: ""
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

## Related references

- `foundation-overview.md`
- `tenant-and-environment-setup.md`
