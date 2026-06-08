---
title: "PingOne ST — Directory Setup (User Management)"
product_family: pingone-st
products: ["pingone-aic", "pingidm", "pingds"]
capabilities: ["foundation"]
services: []
audience: ["admin", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-05"
slug: "https://docs.pingidentity.com/pingoneaic/getting_started/getting_started-identity_store.html"
---

# PingOne ST — Directory Setup (User Management)

Identity store options, schema configuration, and provisioning patterns for PingOne ST.

## Scope

**Covers:** PingDS identity store, external LDAP/AD connection, managed objects and schema, provisioning and reconciliation.
**Does NOT cover:** Authentication journey configuration — see `references/curated/pingone-st/authentication-fundamentals.md`. Deep provisioning flow design — see `ping-orchestration`.

---

## Identity store options

Each realm must be associated with an identity store.

| Option | When to use |
|---|---|
| PingDS (default) | New deployments; cloud-native, fully managed by Ping Identity |
| External LDAP / AD | Migrating from on-prem directory; AD remains authoritative |
| Multiple stores | Advanced: route different user populations to different stores |

PingDS requires no additional setup — users created via PingIDM are stored here automatically.

**Admin surface:** AM admin console → Realm → Identity Stores → + Add Identity Store

---

## External LDAP / Active Directory configuration

**Required fields:**

| Field | Example / Notes |
|---|---|
| LDAP server URL | `ldaps://ad.example.com:636` — TLS strongly recommended |
| Bind DN | `uid=pingbind,ou=service,dc=example,dc=com` |
| Bind password | Use a secret/ESV rather than plaintext |
| Base DN | `dc=example,dc=com` |
| User search filter | `(uid=*)` for LDAP; `(sAMAccountName=*)` for AD |
| Group search filter | `(objectClass=groupOfNames)` |

**Active Directory specifics:**
- Username attribute: `sAMAccountName` (not `uid`)
- Account enable/disable: controlled via `userAccountControl`
- Object identifier: GUID — configure `objectGUID` as the DS object identifier
- Kerberos pass-through auth: supported via LDAP gateway

**Constraint:** The DS certificate must be shared with the AM container before TLS connectivity will succeed.

---

## Managed objects and user schema (PingIDM)

**Default managed object types:**

| Object type | Purpose |
|---|---|
| `user` | End-user identity |
| `role` | Access role assigned to users |
| `assignment` | Maps a role to an entitlement |
| `group` | User group |
| `organization` | Org hierarchy node (B2B / delegated admin) |

**Critical:** Do not delete default managed objects. Removing them can break the tenant.

**Schema extension:**
- Custom attributes on `user` must be added via the IDM admin console before they can be set or queried
- **Admin surface:** IDM admin console → Managed Objects → user → Properties → + Add Property
- Properties not defined in schema will not appear in the UI and their sub-properties cannot be configured
- Custom object types (e.g., IoT devices, contracts) are supported

### Custom attributes must be pre-created before journey use

Scripted Decision nodes that read or write a custom attribute (e.g. `custom_mfaDevices`) will fail at runtime if the attribute does not exist in the managed object schema.

- `openidm.patch` can write the attribute without it being in the schema, but `openidm.read` will not return it, and downstream scripts that expect it will receive null.
- **Before deploying any journey that stores custom data on users**, add the attribute via the IDM admin console or via `patchManagedObjectDefinition` MCP tool with operation `add` on `/schema/properties/<attributeName>`.

Recommended schema shape for a string-array custom attribute (e.g. `custom_mfaDevices`):

```json
{
  "type": "array",
  "items": { "type": "string" },
  "title": "MFA Devices",
  "description": "Enrolled MFA method identifiers for this user",
  "returnByDefault": false,
  "searchable": false,
  "userEditable": false,
  "viewable": false,
  "isPersonal": false
}
```

`returnByDefault: false` keeps it out of default profile reads for performance. Scripts that need it must request it explicitly:

```javascript
var result = openidm.read("managed/alpha_user/" + userId, null, ["custom_mfaDevices"]);
```

**Core user properties:** `userName`, `password`, `mail`, `givenName`, `sn`, `telephoneNumber`, `displayName`, `accountStatus`

---

## Provisioning and reconciliation

PingIDM uses **mappings** to move identity data between systems.

**Mapping components:**

| Component | Purpose |
|---|---|
| Source | Where data originates (e.g., `system/ldap/account`) |
| Target | Where data is written (e.g., `managed/alpha_user`) |
| Attribute map | Source attribute → target attribute |
| Conditions | JavaScript expression to control whether the mapping fires (e.g., active accounts only) |
| Transforms | JavaScript function to reshape values (e.g., combine first + last → displayName) |

**Reconciliation phases:**
1. Source reconciliation — identifies changes in the source
2. Target reconciliation — detects orphaned target objects (handles deletions)

**LDAP/AD connector key settings:**

| Setting | Notes |
|---|---|
| `objectClassesToSynchronize` | `inetOrgPerson` for LDAP; `user` for AD |
| `attributesToSynchronize` | Leave empty to sync all; restrict for performance |
| `accountSynchronizationFilter` | LDAP filter to scope which accounts sync |
| `changeLogBlockSize` | Default 100; increase for high-volume directories |

**Outbound provisioning:** 40+ connectors available (Microsoft Entra ID, Salesforce, Workday, Active Directory, ServiceNow). Admin surface: IDM admin console → Connectors → + New Connector.

---

## User creation methods

| Method | Notes |
|---|---|
| IDM admin console | Manual; Managed Objects → user → + New User |
| Self-registration journey | User-initiated via authentication journey (see `ping-orchestration`) |
| SCIM inbound | External HR/provisioning system pushes via SCIM 2.0 endpoint |
| Reconciliation | PingIDM pulls from external directory on schedule |
| REST API | `POST /openidm/managed/alpha_user` |

---

## Prerequisites

- PingOne ST tenant with at least one realm
- For external LDAP/AD: LDAPv3-compliant server; TLS certificate shared with AM container; service account credentials
- For PingDS multi-server replication: same encryption passphrase on all nodes

## Common variants

| Variant | Note |
|---|---|
| Alpha realm users | Stored as `managed/alpha_user`; realm prefix is part of the path |
| Multiple realms | Each realm has its own user store path: `bravo_user`, `alpha_user`, etc. |
| Hybrid: PingDS + AD | PingDS as primary; AD connector syncs a subset of attributes on schedule |
| Delegated administration | Use `organization` managed objects to scope admin access to a subset of users |

## Related references

- `references/curated/pingone-st/foundation-overview.md`
- `references/curated/pingone-st/authentication-fundamentals.md`
- `references/curated/pingone-st/app-setup.md`
- `references/curated/pingone-st/am-services.md` — User Service, Validation Service, and the OAuth 2.0 Provider's claim mappings reference managed object attributes

## Source

[Identity store setup — PingOne ST](https://docs.pingidentity.com/pingoneaic/getting_started/getting_started-identity_store.html)
[Managed objects — PingIDM](https://docs.pingidentity.com/pingoneaic/idm-guide/managed-objects.html)
[LDAP connector configuration](https://docs.pingidentity.com/pingoneaic/idm-connector-reference/ldap-connector.html)
[Provisioning and reconciliation](https://docs.pingidentity.com/pingoneaic/idm-guide/provisioning-overview.html)
