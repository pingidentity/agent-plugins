# OpenICF

## Overview
OpenICF is Ping Identity’s Identity Connector Framework for linking Ping Identity products with external resources. It synchronizes customer data across directories, databases, SaaS platforms, and other systems.

## Core Concepts
- **Connector framework:** Links Ping Identity products with external resources through a common integration layer.
- **Resource integrations:** The catalog includes LDAP, Active Directory, Google Apps, Marketo, CSV, databases, Salesforce, ServiceNow, MongoDB, SCIM, SAP, Workday, and Microsoft Graph API.
- **Synchronization:** Connectors synchronize data across systems to help maintain consistent identity information.
- **PingIDM and RCS operation:** Connectors operate with PingIDM directly or through Remote Connector Servers (RCS).
- **Advanced Identity Cloud connectivity:** Advanced Identity Cloud uses connectors through RCS; selected connectors are also offered directly or as applications.
- **Custom development:** Organizations can develop connectors for resources outside the provided catalog.

## When to use
- Integrate identity data with directories, databases, SaaS services, or enterprise applications.
- Extend PingIDM or Advanced Identity Cloud connectivity to an external resource.

## When not to use
- For non-identity data flows, use a better-fit integration area rather than OpenICF.
- When a target resource is unsupported and custom development is unsuitable, use its documented integration method.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/openicf/index.md)
