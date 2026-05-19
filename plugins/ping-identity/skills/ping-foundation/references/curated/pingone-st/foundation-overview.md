---
title: "PingOne ST — Foundation Overview"
product_family: pingone-st
products: ["pingone-aic", "pingam", "pingidm", "pingds"]
capabilities: ["foundation"]
services: []
audience: ["admin", "architect"]
use_cases: ["workforce", "customer"]
doc_type: concept
status: current
canonical: true
last_updated: "2026-05-19"
slug: "https://docs.pingidentity.com/pingoneaic/latest/index.html"
---

# PingOne ST — Foundation Overview

Conceptual orientation for PingOne ST (Advanced Identity Cloud): what it is, how it is structured, and what each component does before any configuration begins.

## Scope

**Covers:** Tenant architecture, core components, realm model, admin control plane.
**Does NOT cover:** Step-by-step setup tasks — see:
- `references/curated/pingone-st/app-setup.md` for application registration
- `references/curated/pingone-st/authentication-fundamentals.md` for journeys
- `references/curated/pingone-st/directory-setup.md` for identity stores and users
- `references/curated/pingone-st/themes-and-customization.md` for branding

## Key steps / content

### What PingOne ST is

PingOne ST (formerly ForgeRock Identity Cloud) is a fully managed, single-tenant SaaS identity platform. It runs a complete identity stack — authentication, identity management, and directory services — inside a dedicated tenant owned by Ping Identity but configured by the customer.

It is distinct from PingOne MT (multi-tenant cloud) in:
- Deployment model: single-tenant per customer, not shared infrastructure
- Control plane: AIC admin console at a customer-specific URL, not apps.pingone.com
- Customization depth: full journey/tree authoring, schema extension, custom scripts
- Component model: three integrated products (PingAM, PingIDM, PingDS) vs. PingOne's service-based model

### Core components

| Component | Role |
|---|---|
| **PingAM** | Authentication and access management. Handles OAuth 2.0, OIDC, SAML 2.0, session management, and journey execution. |
| **PingIDM** | Identity management. Manages users, roles, groups, organizations, and provisioning to external systems. |
| **PingDS** | Directory services. Backend data store for identity data. PingDS ships as the default identity store. |

These three components are pre-integrated in every PingOne ST tenant. They share a common data plane but expose separate admin surfaces.

### Tenant architecture

```
Tenant (one per customer)
└── Realm (one or more logical identity domains)
    ├── Identity Store (PingDS or external LDAP/AD)
    ├── Applications (OIDC/SAML clients)
    ├── Journeys / Auth Trees (authentication flows)
    ├── Policies (authorization rules)
    └── Themes (hosted page branding)
```

**Tenant:** The top-level isolated environment. All configuration is scoped to a tenant. Tenants come in types: development, staging, production, sandbox — each with different SLA and capability profiles.

**Realm:** A logical partition inside a tenant for grouping identities, applications, and authentication configuration. The default realms are `alpha` (typically customer-facing) and `bravo` (typically internal/workforce). Additional realms can be created.

**Identity Store:** The backend user data repository associated with a realm. PingDS is the default. External LDAP/AD can be configured as an additional or replacement store.

### Admin control plane surfaces

| Surface | What it controls |
|---|---|
| AIC tenant admin console | Realm management, journeys, apps, themes, users, audit |
| AM admin console | Low-level OAuth2/SAML configuration, realms, advanced auth settings |
| IDM admin console | Managed objects, schema, connectors, provisioning mappings |
| REST APIs | All above surfaces; preferred for automation |

Most day-to-day admin work happens in the AIC tenant admin console. The AM and IDM consoles are used for advanced configuration not yet surfaced in the unified console.

### Environment types

| Type | Purpose |
|---|---|
| Development | Feature development and testing |
| Staging | Pre-production validation |
| Production | Live traffic; highest SLA |
| Sandbox | Isolated exploration; no production data |
| UAT | User acceptance testing |

Production tenants support multi-region high availability.

## Prerequisites

- PingOne ST subscription provisioned by Ping Identity
- Tenant URL and initial superadmin credentials from onboarding email
- Understanding of OAuth 2.0, OIDC, or SAML 2.0 for application integration planning

## Common variants

| Variant | Note |
|---|---|
| ForgeRock Identity Cloud | Previous branding; same product. Documentation and community content may use this name. |
| Multiple realms | Large deployments often use separate realms for workforce vs. customer identity domains. |
| Custom domains | Production tenants should configure a custom domain before going live. |

## Related references

- `references/curated/pingone-st/app-setup.md`
- `references/curated/pingone-st/authentication-fundamentals.md`
- `references/curated/pingone-st/directory-setup.md`
- `references/curated/pingone-st/themes-and-customization.md`

## Source

[PingOne ST Documentation](https://docs.pingidentity.com/pingoneaic/latest/index.html)
