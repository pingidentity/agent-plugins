---
title: "Choose the Right Ping Platform"
product_family: cross-platform
products: ["pingone", "pingone-st", "pingfederate", "pingaccess", "pingdirectory"]
capabilities: ["quickstart"]
services: []
audience: ["admin", "architect"]
use_cases: ["workforce", "customer", "cross-platform"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-01"
slug: "https://docs.pingidentity.com/pingone/introduction_to_pingone/p1_introduction.html"
---

# Choose the Right Ping Platform

Decision guide for selecting between PingOne (multi-tenant cloud), PingOne Advanced Identity Cloud (AIC), and the Ping Software Suite.

## Scope

Covers: platform selection decision criteria, differentiators, protocol support, licensing model, and common edge cases including hybrid and migration scenarios.
Does NOT cover: configuration steps — see `ping-foundation`; journey or flow design — see `ping-orchestration`.

---

## Decision matrix

| Need | Best platform |
|---|---|
| New deployment, SaaS-managed, low ops overhead | PingOne (multi-tenant cloud) |
| Deep customization, journey/tree orchestration, ForgeRock migration | AIC |
| Existing on-prem or hybrid, PingFederate/PingAccess/PingDirectory | Ping Software Suite |
| CIAM with DaVinci orchestration | PingOne (multi-tenant cloud) + DaVinci |
| Complex authentication trees and self-service | AIC |
| Federation hub for enterprise apps (SAML, WS-Fed) | PingFederate (Software Suite) |
| API and web application protection | PingAccess (Software Suite) |
| Authoritative LDAP/SCIM directory | PingDirectory (Software Suite) |
| Workforce SSO with existing AD | PingFederate or PingOne (multi-tenant cloud) SSO |
| CIAM registration and login flows | AIC or PingOne + DaVinci |

---

## Orchestration layer decision

| Scenario | Use |
|---|---|
| DaVinci flows on PingOne (multi-tenant cloud) | DaVinci SDK / DaVinci orchestration |
| AIC / PingAM journey trees | Journey SDK / orchestration |
| OIDC-compliant server (PingFederate, any IdP) | OIDC Sign-on — server-side journey changes reflected without app rebuild |

Source: https://developer.pingidentity.com/orchsdks/index.html

---

## Key differentiators

### PingOne (multi-tenant cloud) vs AIC

| Dimension | PingOne (multi-tenant cloud) | AIC |
|---|---|---|
| Management model | SaaS console (console.pingone.com) | Fully managed tenant; REST/UI admin |
| Orchestration | DaVinci flows (no-code/low-code) | Journey trees (node-based, highly scriptable) |
| Customization depth | Moderate — DaVinci connectors and policies | High — custom nodes, scripts, Groovy, JavaScript |
| ForgeRock migration path | Limited — best for greenfield | Primary target — journey/tree import supported |
| Self-service | PingOne self-service app | Configurable self-service journeys |
| Pricing model | Per-user/per-MAU subscription | Managed service; AIC includes Dev/Staging/Prod; UAT and additional Sandbox are paid add-ons. |

### Identifying your P14E variant

PingOne for Enterprise (P14E) has four variants, identifiable by the top navigation bar:

| Variant | Top nav indicators |
|---|---|
| Standard P14E | Dashboard / Apps / Users / Setup / Account |
| P14E for MSPs | Adds Customers menu |
| PingOne SSO for SaaS Apps | Adds Customer Connections |
| PingOne SSO for SaaS Apps with Managed Accounts | Adds Customer Connections + Managed Accounts |

Admin entry point for P14E: `admin.pingone.com`.
Source: https://docs.pingidentity.com/pingoneforenterprise/p14e_which_p14e_am_i_using.html

### Cloud vs Software Suite

| Dimension | Cloud (PingOne / AIC) | Ping Software Suite |
|---|---|---|
| Infrastructure management | Ping Identity manages | Customer manages |
| Upgrade cadence | Continuous / automatic | Quarterly; customer-controlled |
| Deployment topology | Multi-tenant or dedicated tenant | Customer-defined cluster |
| Customization | Via APIs, DaVinci, journey nodes | Full code-level; adapter/plugin model |
| Licensing | Subscription | Perpetual or subscription |
| Compliance controls | Ping SOC2/ISO27001 certified | Customer responsible for compliance posture |

---

## Protocol support by platform

| Protocol | PingOne (multi-tenant cloud) | AIC | PingFederate | PingAccess | PingDirectory |
|---|---|---|---|---|---|
| OAuth 2.0 / OIDC | Yes | Yes | Yes | Token-based authz | No |
| SAML 2.0 | Yes | Yes | Yes (IdP + SP) | No | No |
| WS-Federation | No | Limited | Yes | No | No |
| LDAP / LDAPS | Via gateway | Built-in | Via datastore | No | Primary protocol |
| SCIM 2.0 | Yes | Yes | Limited | No | Yes |
| FIDO2 / WebAuthn | Yes | Yes | Via PingID adapter | No | No |
| Kerberos / SPNEGO | No | Limited | Yes | No | No |

---

## Edge-case decision rules

### Hybrid on-premises + cloud

Use PingFederate as the federation hub bridging on-premises systems to cloud apps. PingFederate can act as an IdP for PingOne (multi-tenant cloud) or AIC, allowing a phased migration where on-prem identity stores are accessed via PingFederate adapters while the cloud platform handles app-facing flows.

### Existing Active Directory

- If AD is authoritative and you need Windows Integrated Authentication: PingFederate with a Kerberos adapter is the fastest path.
- If you want to keep AD but add cloud orchestration: connect PingOne (multi-tenant cloud) to AD via an LDAP gateway or the PingOne Gateway for AD.
- For AIC: use the LDAP identity store connector pointed at AD DS.

### Multi-region requirements

- PingOne (multi-tenant cloud): single global tenant; region selection (NA, EU, APAC) at environment creation time. Cross-region federation requires separate environments.
- AIC: single-region tenant by default; geo-redundant options depend on contract.
- Ping Software Suite: full control over multi-region topology; deploy cluster nodes in each region with load balancer.

### Compliance constraints

| Constraint | Guidance |
|---|---|
| Data residency (GDPR, data sovereignty) | PingOne (multi-tenant cloud): choose EU region at creation; AIC: confirm tenant region with Ping; Software Suite: full control |
| FedRAMP | PingFederate on-prem in a FedRAMP boundary; consult Ping for cloud FedRAMP status |
| HIPAA | Business Associate Agreement available for PingOne (multi-tenant cloud); on-prem gives full control |
| PCI DSS | On-prem Software Suite preferred for cardholder data environments |

### SLA characteristics

| Platform | Availability SLA | Notes |
|---|---|---|
| PingOne (multi-tenant cloud) | 99.99% (enterprise tier) | Consult contract for base tier |
| AIC | 99.9% typical | Varies by contract |
| Ping Software Suite | Customer-defined | Depends on deployment HA design |

---

## Prerequisites

Before making a platform selection decision, have the following inputs ready:

- Deployment model preference: SaaS/managed vs self-managed.
- Use case type: workforce identity (employees, contractors) vs CIAM (customers, partners) vs both.
- Existing infrastructure inventory: AD, LDAP directories, SAML-federated apps, on-prem identity providers.
- Compliance or data residency requirements (GDPR, FedRAMP, HIPAA, PCI).
- Operational capacity: team size and expertise for managing self-hosted identity infrastructure.
- Migration context if applicable: ForgeRock AM/IDM, legacy PingFederate version, or other IdP.

---

## Common variants

### Evaluation / PoC context vs production selection

- For a PoC: start with PingOne (multi-tenant cloud) trial (fastest to stand up); use the PoC to validate use cases and skill requirements before committing.
- For production selection: run a formal requirements-to-criteria mapping using the decision matrix above; involve architecture and security teams.

### Greenfield vs migration context

- Greenfield (no existing identity infrastructure): PingOne (multi-tenant cloud) is lowest-friction; AIC if journey complexity is anticipated.
- Migration from ForgeRock AM/IDM: AIC is the primary migration target; journey trees import directly.
- Migration from legacy PingFederate: upgrade in place (major version) or lift to PingOne (multi-tenant cloud) / AIC for the orchestration layer while PingFederate continues as a federation bridge.

---

## Related references

- `plugins/ping-identity/skills/ping-quickstart/references/curated/getting-started-overview.md`
- `plugins/ping-identity/skills/ping-quickstart/references/curated/common-starting-patterns.md`

## Source

- Decision matrix: https://docs.pingidentity.com/pingone/introduction_to_pingone/p1_introduction.html
- P14E disambiguation: https://docs.pingidentity.com/pingoneforenterprise/p14e_which_p14e_am_i_using.html
- SDK decision matrix: https://developer.pingidentity.com/orchsdks/index.html
- Solution guides: https://docs.pingidentity.com/solution-guides/htg_overview.html
