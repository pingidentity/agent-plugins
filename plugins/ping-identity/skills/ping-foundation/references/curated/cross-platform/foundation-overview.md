---
title: "Ping Foundation Overview"
product_family: cross-platform
products: ["pingone", "pingone-st", "pingfederate", "pingaccess", "pingdirectory"]
capabilities: ["foundation"]
audience: ["admin", "architect"]
use_cases: ["workforce", "customer"]
doc_type: concept
status: current
canonical: true
last_updated: "2026-05-19"
slug: ""
---

# Ping Foundation Overview

Core concepts for platform setup and administration across all Ping Identity platforms.

## Scope

Covers: the shared administrative model across PingOne MT, PingOne ST, and Ping Software Suite.
Does NOT cover: flow design (see `ping-orchestration`) or app integration code (see `ping-app-integration`).

## Core concepts

### PingOne MT

- **Environment**: top-level container; maps to an org or project. Holds apps, populations, policies, and connections.
- **Population**: user store within an environment. Users belong to one population.
- **Application**: OIDC or SAML app registered in PingOne. Policies attach to apps.
- **Sign-on Policy**: ordered set of authentication rules applied to app sign-in.
- **Directory**: user data store; default is PingOne Directory; external LDAP can be connected.

### PingOne ST

- **Tenant**: top-level admin unit. One tenant per PingOne ST deployment.
- **Realm**: identity domain inside a tenant. Each realm has its own identity store, policies, and journeys.
- **Identity Store**: PingDS (default) or external LDAP/AD.
- **Journey / Auth Tree**: orchestrated authentication or registration flow. Core orchestration primitive.
- **Theme**: UI customization applied to hosted pages within a realm.

### Ping Software Suite

- **Server Profile**: configuration-as-code pattern for PingFederate and PingAccess.
- **Connection**: SP connection (PingFederate) or resource (PingAccess) defines a federation or protection relationship.
- **Adapter**: PingFederate authentication adapter for a specific credential type (HTML form, RADIUS, Kerberos, etc.).
- **Virtual Host**: PingAccess per-site routing configuration.
- **Backend**: PingAccess upstream application definition.

## Setup sequence (generic)

1. Provision the platform (environment / tenant / server)
2. Configure identity store / directory
3. Register applications
4. Define authentication policy / journey / adapter chain
5. Test sign-in

## Prerequisites

Valid for any administrator with access to the relevant Ping Identity platform (PingOne organization account, PingOne ST subscription, or on-premises server access).

## Common variants

| Variant | Note |
|---|---|
| PingOne MT | Multi-tenant cloud; environments managed via apps.pingone.com; no infrastructure to operate |
| PingOne ST | Single-tenant SaaS; customer-specific URL; deeper customization, PingAM/IDM/DS stack |
| Ping Software Suite | Self-managed on-prem or IaaS; full infrastructure responsibility; use server profiles for config-as-code |

## Related references

- `references/curated/cross-platform/tenant-and-environment-setup.md`
- `references/curated/cross-platform/policy-and-branding-basics.md`
- `references/curated/cross-platform/core-admin-patterns.md`

## Source

[Ping Identity Documentation](https://docs.pingidentity.com/)
