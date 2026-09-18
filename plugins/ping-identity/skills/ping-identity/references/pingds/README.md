# PingDS

## Overview
PingDS is a Java-based, LDAPv3 directory service for securely storing organizational identities. It provides high-performance, highly available directory access through LDAP and HTTP-based HDAP.

## Core Concepts
- **Directory service:** Stores and manages organizational identity data, providing a central identity store.
- **LDAPv3 access:** Supports LDAP authentication, search, comparison, and entry updates through LDAP operations and command-line utilities.
- **HDAP:** Maps JSON resources to LDAP entries and translates HTTP operations into LDAP operations for REST-based access.
- **Replication:** Supports data replication between PingDS instances, including cross-region replication scenarios.
- **Access control:** Access-control instructions can allow or deny user operations, helping govern directory access.
- **Operations:** Documentation covers deployment, configuration, maintenance, monitoring, logging, upgrades, backup, restoration, and disaster recovery.

## When to use
- Use PingDS when an application or identity platform needs a secure LDAP directory for organizational identities.
- Use LDAP or HDAP for directory-native or REST/HTTP access, respectively.
- Consider replicated deployments and disaster-recovery planning.

## When not to use
- Do not treat HDAP as a fully stable interface; the documentation classifies it as evolving.
- Redirect application-integration or access-management questions to their product-specific documentation.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/pingds/latest/index.md)
