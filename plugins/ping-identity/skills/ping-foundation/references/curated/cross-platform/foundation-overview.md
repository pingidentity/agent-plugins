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
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/pingone/introduction_to_pingone/p1_introduction.html"
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

## Platform capability comparison

| Capability | PingOne MT | PingOne ST (AIC) | Ping Software Suite |
|---|---|---|---|
| Tenant provisioning | Self-service via admin console | Provided by Ping during onboarding | Self-managed installation |
| Flow authoring | DaVinci flow designer | Journey/tree editor (PingAM) | PingFederate authentication policies + adapters |
| Identity store | PingOne Directory or LDAP Gateway | PingDS (built-in) or external LDAP/AD | PingDirectory or external LDAP/AD |
| Schema extension | Custom attributes (up to 200 per env) | Managed object schema in PingIDM | LDAP schema extension files |
| Customization depth | Moderate — theming, scopes, policies | Deep — custom scripts, nodes, full schema control | Full — server-level config and plugins |
| SLA | Ping-managed per environment type | Ping-managed, production multi-region HA | Customer-managed |
| Data residency | Region selection at env creation | Dedicated instance per customer | Fully customer-controlled |

## Platform selection decision rules

| Condition | Recommended platform |
|---|---|
| New greenfield deployment, no data residency requirement | PingOne MT |
| Requires PingAM-native journey nodes or deep scripting customization | PingOne ST (AIC) |
| Existing on-premises infrastructure or strict data residency mandate | Ping Software Suite |
| Hybrid enterprise: cloud SSO + on-prem directory | PingOne MT + LDAP Gateway, or PingFederate + PingDirectory |
| Regulated industry requiring dedicated compute | PingOne ST (AIC) — single-tenant, no shared infrastructure |

## Setup sequence (generic)

1. Provision the platform (environment / tenant / server)
2. Configure identity store / directory
3. Register applications
4. Define authentication policy / journey / adapter chain
5. Test sign-in

## Common gotchas

| Gotcha | Applies to | Fix |
|---|---|---|
| Redirect URI trailing-slash mismatch | All platforms | Register exact URI; add both forms if the app may send either |
| Environment type is immutable after creation | PingOne MT | Provision the correct type (Sandbox / Development / Production) from the start |
| Realm-scoped resources not visible across realms | PingOne ST | Clients, journeys, and users in `alpha` realm are not accessible in `bravo` |
| Admin API port exposed to internet | Ping Software Suite | Restrict PingFederate port 9999 and PingAccess port 9000 to management CIDR only |
| Service not enabled in environment | PingOne MT | DaVinci, Verify, Protect, etc. must be explicitly activated per environment before use |

## Prerequisites

Valid for any administrator with access to the relevant Ping Identity platform (PingOne organization account, PingOne ST subscription, or on-premises server access).

## Common variants

| Variant | Note |
|---|---|
| PingOne MT | Multi-tenant cloud; environments managed via console.pingone.com; no infrastructure to operate |
| PingOne ST | Single-tenant SaaS; customer-specific URL; deeper customization, PingAM/IDM/DS stack |
| Ping Software Suite | Self-managed on-prem or IaaS; full infrastructure responsibility; use server profiles for config-as-code |

## Licensing and feature availability

| Feature | PingOne MT | PingOne ST (AIC) | Ping Software Suite |
|---|---|---|---|
| Base SSO | Included | Included | PingFederate license |
| MFA | Add-on (PingOne MFA) | Included in AIC | PingID add-on |
| Risk scoring | PingOne Protect add-on | PingProtect node | PingFederate + external risk API |
| Identity proofing | PingOne Verify add-on | PingVerify node (AIC) | Third-party integration |
| SCIM provisioning | Outbound via PingOne | PingIDM connectors | PingDirectory + SCIM plugin |
| Fine-grained authorization | PingOne Authorize add-on | PingAuthorize node | PingAuthorize standalone |

Licensing is per organization for PingOne MT (enabled per environment). PingOne ST licensing is per tenant subscription. Ping Software Suite products are individually licensed.

---

## Key terminology cross-reference

| PingOne MT term | PingOne ST equivalent | Ping Software Suite equivalent |
|---|---|---|
| Organization | Tenant | Server installation |
| Environment | Realm | N/A (single server context) |
| Population | User store (managed object type, e.g. `alpha_user`) | LDAP base DN |
| Application | OAuth 2.0 Client | PingFederate SP connection / OAuth client |
| Sign-on policy | Authentication journey / auth tree | Authentication policy (PF 10+) / adapter chain |
| Worker app | Service account (IDM or AM OAuth2 client) | PingFederate OAuth client with client credentials |

---

## Skill routing quick reference

When a request is about Ping Identity, route through ping-foundation first, then compose with:

| Next need | Skill |
|---|---|
| Authentication flow or journey logic | `ping-orchestration` |
| Risk scoring, MFA step-up, Verify, IGA, Credentials | `ping-universal-services` |
| App/SDK integration code | `ping-app-integration` |
| AI agent identity | `ping-identity-for-ai` |
| Platform selection / getting started | `ping-quickstart` |

## Related references

- `references/curated/cross-platform/tenant-and-environment-setup.md`
- `references/curated/cross-platform/policy-and-branding-basics.md`
- `references/curated/cross-platform/core-admin-patterns.md`

## Source

[Ping Identity Documentation](https://docs.pingidentity.com/)
[PingOne MT Documentation](https://docs.pingidentity.com/pingone)
[PingOne ST (AIC) Documentation](https://docs.pingidentity.com/pingoneaic)
[PingFederate Documentation](https://docs.pingidentity.com/pingfederate)
