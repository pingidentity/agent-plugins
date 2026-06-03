---
title: "PingOne MT Directory Options and Population Management"
product_family: pingone-mt
products: ["pingone"]
capabilities: ["foundation"]
services: []
audience: ["admin", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/pingone/directory/p1_aboutusers.html"
---

# PingOne MT Directory Options and Population Management

Configure the user directory model and population structure for a PingOne MT environment before creating applications or sign-on policies.

## Scope

**Covers:** PingOne Directory (built-in cloud store), LDAP Gateway (proxy to on-premises LDAP/AD), external identity providers (OIDC, SAML, social), and population management in PingOne MT environments.

**Does NOT cover:**
- PingOne ST directory configuration — see `references/curated/pingone-st/directory-setup.md`
- Provisioning workflow design (inbound/outbound SCIM, HR sync) — use the `ping-orchestration` skill
- SDK-level user management (create/update users via API in an app) — use the `ping-app-integration` skill
- Sign-on policy design — see `references/curated/pingone-mt/sign-on-policies.md`
- Administrator role assignment — see `references/curated/pingone-mt/admin-roles-and-access.md`

---

## Directory options

| Option | Description | Typical use case | Sync model |
|---|---|---|---|
| **PingOne Directory** | Built-in cloud directory; user records stored natively in PingOne per environment | New deployments; cloud-first; no existing enterprise directory | None — PingOne is the system of record |
| **LDAP Gateway** | Agent deployed on-premises proxies authentication and optional user sync to an existing LDAP or AD directory | Enterprise with existing AD; no data migration required immediately | Read-through (auth delegates; no copy) or Import (copy on first auth or scheduled sync) |
| **External IdP (OIDC/SAML/Social)** | PingOne acts as SP/RP; external IdP authenticates; JIT provisioning creates a local record on first login | Federation with corporate SSO, partner IdP, or consumer identity provider | JIT — record created in PingOne on first successful authentication |

Multiple directory options can coexist in one environment (e.g., PingOne Directory for employees and Google social IdP for customers).

---

## Populations

### What populations are

A population is the primary organizational unit for users within a PingOne environment. Every user belongs to **exactly one** population at any time.

Populations determine:
- Which password policy applies to the user
- Which applications the user can access (via the app's **Allowed Populations** setting)
- Which sign-on policy conditions evaluate (policies can branch on population membership)
- Which administrator can manage the user (an Identity Admin role can be scoped to a single population)
- Which default identity provider applies when a user has no authoritative IdP set

### Population assignment rules

- A user cannot belong to more than one population simultaneously.
- At least one population must exist before any user can be created.
- New users with no explicit population assignment are placed in the **default population**.
- Any population can be designated the default; only one default exists at a time.
- Users can be moved between populations after creation.

### Population strategy patterns

| Pattern | Configuration |
|---|---|
| Single audience (e.g., workforce only) | One population; rename the auto-created default to reflect its purpose |
| Multiple audiences (employees + customers) | Separate population per audience; assign each app to the correct population |
| Multi-region or multi-brand | One population per region or brand; scope admin roles to each population |
| Delegated admin | Create a population per business unit; assign Identity Admin role scoped to that population |

**Silent failure warning:** A user who exists in the directory but is not in the population allowed by the application will be denied access with no error surfaced to the user. Verify the app's Allowed Populations list when debugging unexpected access denials.

---

## PingOne Directory configuration

PingOne Directory requires no external components. A default population is created automatically with each new environment.

### Password policy

Password policies are assigned at the population level. Each population can have a distinct policy.

| Field | Constraint |
|---|---|
| Minimum length | 8–255 characters |
| Complexity rules | Uppercase, lowercase, number, special character toggles |
| Expiry | Days until password expires; 0 = never expires |
| Lockout threshold | Number of failed attempts before account lock |
| Lockout duration | Minutes; 0 = manual admin unlock required |

### Custom user attributes

Custom attributes extend the PingOne user schema beyond built-in fields (name, email, username, address, etc.).

| Field | Constraint |
|---|---|
| Name | Unique identifier; used in token mappings |
| Display Name | UI label |
| Type | String (with optional uniqueness, multivalued, enumerated, or regex validation) or JSON (with optional JSON Schema validation) |
| Max custom attributes | 200 string or JSON attributes per environment |
| Multivalued | Once set, cannot be changed to single-valued |
| Unique | Value must be unique across the entire environment |

**Admin surface:** Environment → Directory → User Attributes

Custom attributes are mapped to OIDC claims, SAML assertions, or access tokens via application-level attribute mapping configuration.

---

## LDAP gateway

The LDAP gateway is a software agent deployed on-premises, adjacent to the LDAP or AD directory. It communicates outbound to PingOne over WebSocket Secure (WSS) — no inbound firewall rule is required.

### Supported directory types

PingDirectory, Microsoft Active Directory, Oracle Directory Server Enterprise Edition, Oracle Unified Directory, CA Directory, IBM Security Directory Server, and any LDAP v3-compliant server.

### Gateway connection fields

| Field | Requirement | Notes |
|---|---|---|
| Name | Required | Unique within the environment |
| LDAP Directory Type | Required | Determines available features (e.g., Kerberos for AD) |
| LDAP Host Name | Required | Multiple hosts supported for failover; tried in order |
| Port | Required | Default 389; use 636 for LDAPS (required in production) |
| Connection Security | Required | TLS (recommended), StartTLS, or None |
| Bind DN | Required | Service account with user search permissions |
| Bind Password | Required | Read-only sufficient for auth-only; write access needed for provisioning back to LDAP |
| Follow LDAP Referrals | Optional | Relevant for multi-domain AD forests |

**AD-only additional fields:** Kerberos authentication toggle, Service Account UPN (case-sensitive), Service Account Password, Retain Previous Credentials (up to five), Retention Duration (default 610 minutes).

### User type fields (per gateway)

| Field | Notes |
|---|---|
| Password Authority | PingOne or LDAP — determines which system validates credentials |
| User Search Base DN | Scope to the smallest required subtree |
| User Link Attributes | Attributes used to match LDAP user to PingOne record (e.g., `dn`, `sAMAccountName`; evaluated as OR chain) |
| Enable migration on first auth | Copies user into PingOne Directory on first successful LDAP authentication |
| LDAP Filter | Narrows which users are eligible for migration |
| Target Population | PingOne population where imported users are placed |
| Update PingOne attributes on sign-on | Syncs mapped attributes on each authentication; if any attribute update fails, the authentication also fails |
| Attribute Mappings | Maps LDAP attributes to PingOne schema fields (e.g., `mail` → `email`, `sAMAccountName` → `username`) |

### Gateway agent prerequisites

| Requirement | Specification |
|---|---|
| CPU | 2 vCPUs |
| RAM | 1 GB |
| Storage | 1 GB |
| Runtime | Docker, standalone Java 21 LTS, or Windows application |
| Outbound network | WSS to PingOne regional gateway endpoint (e.g., `wss://gateways.pingone.com/`) |
| Directory account | Bind DN + password with user search permissions |
| Admin role | Environment Admin in PingOne |

---

## External identity providers

External IdPs federate authentication into PingOne. Users are auto-provisioned (JIT) into a designated population on first login.

### Supported types

| Type | Configuration source |
|---|---|
| OIDC | Discovery Document URI or manual endpoint entry |
| SAML 2.0 | Metadata URL or manual entity ID + SSO URL + certificate |
| Social: Google, Apple, Facebook, GitHub, LinkedIn, Microsoft, Amazon, PayPal, X, Yahoo | App credentials from the provider's developer console |

### OIDC IdP required fields

| Field | Constraint |
|---|---|
| Client ID | Required |
| Client Secret | Required |
| Discovery Document URI | Recommended — auto-populates issuer, JWKS, authorization, and token endpoints |
| Issuer | Must use `https` |
| Authorization Endpoint | Must use `https` |
| Token Endpoint | Must use `https` |
| Token Endpoint Authentication Method | None, Client Secret Basic, or Client Secret Post |
| Requested Scopes | Space-separated, case-sensitive |
| Target Population | Population where JIT-provisioned users are created |

### SAML IdP required fields

| Field | Constraint |
|---|---|
| IdP Entity ID | Required |
| SSO Endpoint | Required |
| SSO Binding | HTTP POST or HTTP Redirect |
| Verification Certificate | Required |
| Signing Algorithm | RSA_SHA256/384/512 or EC variants |
| Target Population | Population where JIT-provisioned users are created |

### Attribute mapping

Both OIDC and SAML IdPs support attribute mapping (provider attribute → PingOne schema field). The **Update Condition** controls whether PingOne overwrites the local value: `Empty Only` (only when the PingOne field has no value) or `Always` (overwrite on every login).

---

## Groups

Groups are collections of users that share something in common (department, region, role). A user can belong to **multiple groups** but only one population at a time. Groups are secondary to populations; populations are the primary organizational unit.

### Group types

| Type | Icon in console | How members are managed |
|---|---|---|
| Internal | Internal Group | Created and managed entirely in PingOne; add/remove members directly |
| External | External Group | Created through a connected external IdP or LDAP gateway; membership flows from the external source |

### Group membership modes

| Mode | How members are added | When to use |
|---|---|---|
| Static | Manually added or removed | Fixed, known set of users (e.g., a pilot group) |
| Dynamic | Filter expression on user attributes (e.g., `countryCode = US`) | Auto-include users matching criteria; membership updates automatically as attributes change |
| Combined | Both static additions and a dynamic filter | Base membership via filter; manually add exceptions |

**Dynamic filter behavior:** When the filter expression changes, group membership updates immediately. When a user's attributes change to match or no longer match the filter, they are added or removed automatically — no manual step required.

### Group-level role assignment

Groups can be granted administrator roles, so all group members inherit the role. See `references/curated/pingone-mt/admin-roles-and-access.md` for the full procedure.

### Group creation fields

| Field | Notes |
|---|---|
| Group Name | Must be unique within the environment (for environment groups) or within the population (for population groups) |
| Population | Optional — assign to scope group to a population; required when Identity Admin role is used instead of Environment Admin |
| Dynamic filter | Attribute + operator + value (e.g., `country Equals US`); preview shows matching count before saving |

**Group creation prerequisites:** Identity Data Admin role (or equivalent) required to create or edit groups.

---

## Common failure modes

| Symptom | Likely cause | Resolution |
|---|---|---|
| LDAP gateway shows as disconnected | Gateway agent not running, or outbound WSS blocked by firewall | Verify agent process is running; confirm port 443/WSS to regional gateway endpoint is open |
| User authenticated but denied by app | User's population is not in the app's Allowed Populations list | Add the user's population to the app's Allowed Populations setting |
| External IdP attribute not appearing in token | Provider attribute not mapped to a PingOne schema field | Add the mapping in the IdP's attribute mapping configuration |
| New user creation fails with schema error | Custom attribute limit reached or unique constraint violated | Check environment's attribute count; verify uniqueness requirement against existing data |
| Password policy not enforced for new users | Policy not assigned to the user's population | Assign the password policy to the correct population |
| JIT provisioning fails | Target population not set on the IdP configuration | Set the Population field on the IdP to the intended registration population |
| `Update PingOne attributes on sign-on` causes auth failure | An LDAP attribute update fails (field conflict, type mismatch) | Audit attribute mappings; fix the conflicting field or disable the sync-on-auth option |

---

## Prerequisites

- PingOne environment created with at least one population (auto-created as "Default Population")
- For LDAP Gateway: service account in the target directory; gateway agent host meeting the hardware requirements above; outbound WSS network path confirmed
- For External IdP: app registration completed with the provider (client ID and secret or SAML metadata available)
- Administrator role: Environment Admin for gateway and IdP configuration; Identity Admin for population and user management

---

## Common variants

**Multiple populations with scoped admins:** Create one population per business unit. Assign Identity Admin roles scoped to individual populations. Admins in each population cannot see or modify users in other populations.

**Hybrid directory model:** PingOne Directory for new cloud users alongside an LDAP Gateway for existing on-premises users. Both populations coexist in the same environment; applications allow both populations.

**Social + enterprise federation:** External IdP (corporate SAML/OIDC) for employees, Google/Apple social for customers. Each IdP targets a different population; applications allow only the relevant population.

**LDAP read-through without migration:** Disable migration on first auth. Users authenticate against LDAP indefinitely; no PingOne user record is created. Suitable when the LDAP directory must remain the sole system of record.

---

## Related references

- `references/curated/pingone-mt/tenant-and-environment-setup.md` — environment creation and initial configuration
- `references/curated/pingone-mt/sign-on-policies.md` — configure authentication policies that reference populations
- `references/curated/cross-platform/foundation-overview.md` — cross-platform identity concepts

---

## Source

- https://docs.pingidentity.com/pingone/directory/p1_aboutusers.html
- https://docs.pingidentity.com/pingone/directory/p1_populations.html
- https://docs.pingidentity.com/pingone/directory/p1_groups_vs_populations.html
- https://docs.pingidentity.com/pingone/integrations/p1_ldap_gateways.html
- https://docs.pingidentity.com/pingone/integrations/p1_add_ldap_gateway.html
- https://docs.pingidentity.com/pingone/integrations/p1_add_a_user_type.html
- https://docs.pingidentity.com/pingone/integrations/p1_external_idps.html
- https://docs.pingidentity.com/pingone/directory/p1_user_attributes.html
- https://docs.pingidentity.com/pingone/directory/p1_groups.html
- https://docs.pingidentity.com/pingone/directory/p1_groups_vs_populations.html
