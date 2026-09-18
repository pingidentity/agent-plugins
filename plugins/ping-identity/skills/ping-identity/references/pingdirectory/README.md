# PingDirectory

## Overview
PingDirectory is a high-performance LDAP directory for centrally managing consumer, user, subscriber, application-configuration, and credential data. It helps organizations serve identity data across enterprise and virtualized environments.

## Core Concepts
- **LDAP directory service:** LDAP v3 support provides a standards-based directory for applications and identity data.
- **Distributed replication:** N-way multi-primary replication supports continuity and helps avoid a single point of failure.
- **Fine-grained security:** Attribute-level access controls, encrypted connections, StartTLS, password policies, SASL, and certificate-based authentication protect directory access and data.
- **Operations and administration:** Command-line utilities, scheduled tasks, backups, imports, exports, monitoring, and auditing support repeatable administration and operational visibility.
- **Integration interfaces:** Directory REST API, SCIM servlet extension, Java LDAP SDK, and Server SDK options connect applications and enable server extensions.

## When to use
- Centralize user, consumer, subscriber, credential, or application-configuration data for LDAP-connected applications.
- Build a replicated directory deployment that needs secure access and operational monitoring.

## When not to use
- Do not treat PingDirectory as the proxy, synchronization, or delegated-administration products in the broader PingDirectory suite; use those product areas for those concerns.
- Do not use the Self Service Account Manager project for supported production deployments; the documentation identifies it as testing and development only.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/pingdirectory/11.1/pd_ds_intro_pindirectory_server.md)
