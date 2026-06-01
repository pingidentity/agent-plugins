---
title: "PingDirectory — Administration Basics"
product_family: ping-software
products: ["pingdirectory"]
capabilities: ["foundation"]
audience: ["admin", "operator"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-05-19"
slug: "https://docs.pingidentity.com/pingdirectory/latest/pd-directory-server-administration-guide/pd-ds-admin-overview.html"
---

# PingDirectory — Administration Basics

Initial installation, configuration, and operation patterns for PingDirectory on Linux.

## Scope

**Covers:** Linux installation, initial setup wizard, replication, schema extension, backup/restore, and connection profiles for PingFederate integration.
**Does NOT cover:** PingDirectoryProxy or PingDataSync (separate products). PingFederate SP connection setup — see `references/curated/ping-software/pingfederate-basics.md`.

---

## Installation on Linux

**Supported platforms:** Red Hat Enterprise Linux, CentOS, Ubuntu, Debian (see release notes for exact version support).

**Prerequisites:**
- Java 11 or 17 JRE (set `JAVA_HOME`)
- Minimum 4 GB RAM for production; 2 GB for development
- Sufficient file descriptor limits (`ulimit -n` should be ≥65535)

**Install steps:**

| Step | Command / Notes |
|---|---|
| Extract archive | `unzip PingDirectory-<version>.zip -d /opt/` |
| Run setup wizard | `/opt/PingDirectory/setup` |
| Accept license | Interactive prompt; or use `--acceptLicense` for non-interactive |
| Specify base DN | e.g., `dc=example,dc=com` — base DN is created during setup |
| Set LDAP/LDAPS ports | Default: LDAP 389, LDAPS 636, admin LDAP 4444 |
| Create initial admin user | Specify Directory Manager DN and password |
| Enable replication (optional) | Configure after primary server is running |

**Non-interactive setup example:**
```
/opt/PingDirectory/setup --cli \
  --acceptLicense \
  --baseDN dc=example,dc=com \
  --ldapPort 389 \
  --ldapsPort 636 \
  --adminConnectorPort 4444 \
  --rootUserPassword <password> \
  --hostname localhost
```

---

## Server management tools

| Tool | Path | Purpose |
|---|---|---|
| `start-ds` | `bin/start-ds` | Start the server |
| `stop-ds` | `bin/stop-ds` | Stop the server |
| `status` | `bin/status` | Check server status and connection handlers |
| `ldapmodify` | `bin/ldapmodify` | Apply LDIF changes to directory data |
| `ldapsearch` | `bin/ldapsearch` | Query directory data |
| `dsconfig` | `bin/dsconfig` | Modify server configuration (connection handlers, backends, etc.) |
| `manage-topology` | `bin/manage-topology` | Manage replication topology |

---

## Schema extension

Add custom attributes or object classes via LDIF schema files:

1. Create a custom schema file: `/opt/PingDirectory/config/schema/99-custom.ldif`
2. Define `attributeTypes` and `objectClasses` in LDIF format
3. Restart the server or use `dsconfig` to reload schema online

**Important:** PingFederate and PingIDM expect specific attribute names. Align custom attribute names with the consuming application's configuration before extending schema.

---

## Replication

PingDirectory uses multi-master replication. All servers in a topology are equal peers.

**Enable replication:**
```
bin/dsreplication enable \
  --host1 <host1> --port1 4444 --bindDN1 "cn=Directory Manager" --bindPassword1 <pw> \
  --host2 <host2> --port2 4444 --bindDN2 "cn=Directory Manager" --bindPassword2 <pw> \
  --replicationPort1 8989 --replicationPort2 8989 \
  --baseDN dc=example,dc=com --adminUID admin --adminPassword <pw>
```

**Initialize replication data:**
```
bin/dsreplication initialize-all --baseDN dc=example,dc=com --adminUID admin --adminPassword <pw>
```

---

## Backup and restore

| Operation | Command |
|---|---|
| Backup | `bin/backup --backupAll --backupDirectory /opt/backups/$(date +%Y%m%d)` |
| Restore | `bin/restore --backupDirectory /opt/backups/20260519 --task` |
| Encrypt backups | Add `--encrypt` to backup command (requires server encryption settings) |

Schedule backups via `dsconfig` recurring tasks or an external scheduler.

---

## Connection profile for PingFederate

When PingFederate connects to PingDirectory as its data store:

| PingFederate data store field | Value |
|---|---|
| LDAP type | PingDirectory |
| Host | `<pingdirectory-host>` |
| Port | 636 (LDAPS) |
| Bind DN | Service account DN with read-only access |
| Base DN | `dc=example,dc=com` |
| Username attribute | `uid` (or `mail` for email login) |
| User search filter | `(uid=*)` |

---

## Prerequisites

- Linux server with Java 11 or 17 JRE installed
- PingDirectory license file
- `JAVA_HOME` set to the Java installation directory
- File descriptor limits raised (`ulimit -n 65535` or persistent via `/etc/security/limits.conf`)

## Common variants

| Variant | Note |
|---|---|
| Replicated pair | Two PingDirectory servers in active-active replication for HA; typical minimum for production |
| PingDirectory + PingFederate | Standard workforce SSO topology; PingDirectory is the LDAP data store for PingFederate's HTML Form Adapter |
| External users (SCIM inbound) | PingIDM provisions users to PingDirectory via SCIM 2.0 or LDAP connector |
| Container deployment | Official Docker image available; mount configuration volume; `--acceptLicense` required for non-interactive startup |

## Related references

- `references/curated/cross-platform/core-admin-patterns.md`
- `references/curated/ping-software/pingfederate-basics.md`

## Source

[PingDirectory Administration Guide](https://docs.pingidentity.com/pingdirectory/latest/pd-directory-server-administration-guide/pd-ds-admin-overview.html)
[PingDirectory setup guide](https://docs.pingidentity.com/pingdirectory/latest/pd-directory-server-admin-guide/pd-ds-installing.html)
[PingDirectory replication](https://docs.pingidentity.com/pingdirectory/latest/pd-directory-server-administration-guide/pd-ds-replication-overview.html)
