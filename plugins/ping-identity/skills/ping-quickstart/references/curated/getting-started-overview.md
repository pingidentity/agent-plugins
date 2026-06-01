---
title: "Getting Started with Ping Identity"
product_family: cross-platform
products: ["pingone", "pingone-st", "pingfederate"]
capabilities: ["quickstart"]
audience: ["admin", "developer"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-05-29"
---

# Getting Started with Ping Identity

Orientation anchor for new users and inherited deployments. Covers the three primary platform families and the right entry point for each.

## Scope

Covers: which platform to use, what to set up first, and how to get your bearings in each Ping Identity environment.
Does NOT cover: detailed configuration steps — see `ping-foundation` for those; flow or journey design — see `ping-orchestration`.

---

## The three platform families

| Platform | When to use it | Admin entry point |
|---|---|---|
| PingOne MT | SaaS-hosted identity for new cloud-first deployments | apps.pingone.com |
| PingOne ST | Fully managed, highly customizable identity cloud (ForgeRock lineage) | Your PingOne ST tenant URL |
| Ping Software Suite | On-premises or self-managed: PingFederate, PingAccess, PingDirectory | Deployed server admin consoles |

---

## Setup sequence by platform

### PingOne MT

1. Create or access a PingOne environment (trial at `pingone.com` or production).
2. Add an application — choose OIDC (authorization code), SAML, or worker (client credentials).
3. Connect a directory: PingOne Directory (built-in), LDAP gateway, or external IdP via social connection.
4. Configure a sign-on policy: define MFA requirements, risk thresholds, or step-up conditions.
5. Assign the sign-on policy to the application and test the flow.

Key config fields for a new PingOne app:
| Field | Value guidance |
|---|---|
| Grant type | Authorization Code + PKCE for SPAs/mobile; Client Credentials for M2M |
| Redirect URI | Must exactly match what the client sends |
| Token lifetime | Default 60 min; set shorter for high-risk apps |
| MFA policy | Attach directly to sign-on policy for step-up |

### PingOne ST

1. Access the PingOne ST tenant; locate the `alpha` and `bravo` realms.
2. Configure the realm identity store (LDAP, PingDirectory, or built-in datastore).
3. Register an OAuth 2.0 / OIDC or SAML application under Realm → Applications.
4. Create or activate an authentication journey (tree) or DaVinci flow.
5. Test with a user account in the realm's identity store.

Realm configuration options:
| Option | Details |
|---|---|
| `alpha` realm | Default consumer-facing realm; used for CIAM patterns |
| `bravo` realm | Default workforce realm; used for employee patterns |
| Custom realm | Supported; requires manual DNS and certificate setup |
| Identity store | PingDirectory recommended for production; in-memory for evaluation |

### Ping Software Suite

1. Identify which products are deployed: PingFederate, PingAccess, PingDirectory.
2. In PingFederate: configure data stores, adapters (HTML Form, PingID, Kerberos), and SP/IdP connections.
3. In PingAccess: define sites, applications, virtual hosts, and web session policies.
4. In PingDirectory: configure schema extensions, password policy, and replication.
5. Test federation or access control end-to-end before opening to users.

Common adapter types in PingFederate:
| Adapter | Use case |
|---|---|
| HTML Form | Username/password login against LDAP or database |
| PingID | MFA via PingID mobile or FIDO2 |
| Kerberos | Windows Integrated Auth / SSO in AD environments |
| Composite | Chain multiple adapters with conditional logic |

---

## Decision point — when to stay in this skill vs hand off

| Situation | Action |
|---|---|
| User does not know their platform | Stay in `ping-quickstart`; ask one clarifying question |
| User knows platform but not configuration | Hand off to `ping-foundation` |
| User knows platform and needs to design a flow | Hand off to `ping-orchestration` |
| User needs MFA, risk, or verification services | Hand off to `ping-universal-services` |
| User is wiring a mobile or web SDK | Hand off to `ping-app-integration` |
| User is building AI agent identity patterns | Hand off to `ping-identity-for-ai` |

---

## Prerequisites

Before acting on this guide, you need:

- A Ping Identity account or active trial subscription.
- Admin role on the target tenant or deployment:
  - PingOne MT: Environment Admin or Organization Admin at `apps.pingone.com`.
  - PingOne ST: Tenant Administrator on your PingOne ST tenant.
  - Ping Software Suite: Server admin credentials for PingFederate/PingAccess/PingDirectory.
- For PingOne MT: network access to `apps.pingone.com` and `auth.pingone.com`.
- For PingOne ST: your tenant's base URL (format: `https://<tenant>.forgeblocks.com` or custom domain).
- For Software Suite: server access to deployed nodes; admin console TCP port (default 9999 for PingFederate).
- A registered application (OAuth client) for any flow that issues tokens; note the client ID and redirect URIs before starting.
- DNS entries or `/etc/hosts` overrides if testing with custom domain names in a local environment.
- For SDK-based app integration: a development environment for the target platform (Android Studio, Xcode, or Node.js); see `ping-app-integration` for details.
- For risk-based or MFA flows: a PingOne MFA or PingOne Protect license; confirm entitlements before configuring policies.
- For identity verification (KYC): a PingOne Verify license; see `ping-universal-services` → verify branch.

---

## Common variants

**Trial vs production environment:**
- Trial environments have reduced rate limits, no SLA, and may expire after 30–60 days.
- Production tenants require formal provisioning through Ping Identity sales or your cloud marketplace listing.
- Start with trial for evaluation; plan a separate production tenant rather than promoting a trial.

**Workforce vs CIAM starting points:**
- Workforce: start with an SSO application connection and AD/LDAP adapter; focus on the `bravo` realm in PingOne ST or a PingFederate SP connection.
- CIAM: start with a self-registration journey or DaVinci flow; focus on the `alpha` realm in PingOne ST or a PingOne MT customer-facing environment.

**Multi-environment setup:**
- PingOne MT uses separate environments per stage (Dev, QA, Prod) within the same org.
- PingOne ST uses separate tenant instances per stage; configuration promotion is manual or via CI/CD pipelines using the PingOne ST REST API or Ping Platform Config Manager.
- Ping Software Suite uses deployment topology (cluster) separation per stage.

**Migrating from ForgeRock / legacy deployment:**
- PingOne ST is the primary migration target from ForgeRock AM/IDM.
- Import existing journey trees using PingOne ST's export/import tooling.
- See `ping-orchestration` for journey migration patterns and `ping-foundation` → `pingone-st` branch for tenant setup.

---

## Related references

- `plugins/ping-identity/skills/ping-quickstart/references/curated/choose-the-right-ping-platform.md`
- `plugins/ping-identity/skills/ping-quickstart/references/curated/common-starting-patterns.md`

## Source

[Ping Identity Documentation](https://docs.pingidentity.com)
