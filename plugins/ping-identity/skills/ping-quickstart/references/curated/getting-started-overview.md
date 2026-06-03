---
title: "Getting Started with Ping Identity"
product_family: cross-platform
products: ["pingone", "pingone-st", "pingfederate"]
capabilities: ["quickstart"]
services: []
audience: ["admin", "developer"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-01"
slug: "https://docs.pingidentity.com/pingone/getting_started_with_pingone/p1_getting_started.html"
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
| PingOne MT | SaaS-hosted identity for new cloud-first deployments | console.pingone.com |
| PingOne ST (AIC) | Fully managed, highly customizable identity cloud (ForgeRock lineage) | Your PingOne ST tenant URL |
| Ping Software Suite | On-premises or self-managed: PingFederate, PingAccess, PingDirectory | Deployed server admin consoles |

---

## Setup sequence by platform

### PingOne MT

1. Create or access a PingOne environment (trial via `pingidentity.com` → Try Ping button, or production).
2. Add an application — choose OIDC (authorization code), SAML, or worker (client credentials).
3. Connect a directory: PingOne Directory (built-in), LDAP gateway, or external IdP via social connection.
4. Configure a sign-on policy: define MFA requirements, risk thresholds, or step-up conditions.
5. Assign the sign-on policy to the application and test the flow.

Trial gotcha: PingOne MT trial enforces mandatory MFA enrollment at trial setup (email passcode, authenticator app, or passkey — one is required before the trial environment is accessible).

Session behavior: The admin console requires re-authentication after 30 minutes of inactivity. MFA is re-prompted if the last sign-on was more than 12 hours ago. These thresholds are not configurable.

Key config fields for a new PingOne app:
| Field | Value guidance |
|---|---|
| Grant type | Authorization Code + PKCE for SPAs/mobile; Client Credentials for M2M |
| Redirect URI | Must exactly match what the client sends |
| Token lifetime | Default 60 min; set shorter for high-risk apps |
| MFA policy | Attach directly to sign-on policy for step-up |

### PingOne ST (AIC)

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
| Identity store | PingDirectory recommended for production; in-memory for evaluation |

Realm hard limit: Every AIC tenant has exactly 2 configurable end-user realms (Alpha and Bravo). The top-level realm is reserved for tenant admins only and cannot be used for end-user authentication. Alpha supports delegated administration and IGA; Bravo does not. Realm names are fixed — they cannot be renamed.

### AIC (PingOne Advanced Identity Cloud)

AIC getting started sequence (9 tasks):
1. Get access — obtain tenant credentials from Ping Identity.
2. Explore platform — review environment types (Sandbox, Dev, UAT, Staging, Production).
3. Add end users — create identities in the Alpha realm identity store.
4. Design user self-registration experiences.
5. Design user authentication experiences.
6. Design account recovery experiences.
7. Design profile management experiences.
8. Apply basic branding to journey and account pages.
9. Integrate an OIDC application for SSO.

Administrator roles: Tenant administrator (most settings, cannot manage other admins), Super administrator (full access), Tenant auditor (read-only), Brand administrator (hosted pages only).

Source: https://docs.pingidentity.com/pingoneaic/getting-started/getting-started-about.html

### PingFederate

PingFederate getting started sequence (7 steps):
1. Install Java — PingFederate requires a supported JDK; consult the release notes for the required version.
2. Install PingFederate — extract the distribution archive to the installation directory.
3. Start PingFederate — use the provided start script for the target OS.
4. Open admin console — `https://<host>:9999/pingfederate/app` (default port 9999).
5. Run setup wizard — configure the federation server base URL, admin credentials, and initial settings.
6. Configure protocols and federation info — set entity ID, SAML/WS-Fed role (IdP, SP, or both), and certificates.
7. Install license key — place the license file in `<PF_HOME>/server/default/conf/` and restart.

Source: https://docs.pingidentity.com/pingfederate/13.0/pf_pf_landing_page.html

### Ping Software Suite (legacy path)

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
  - PingOne MT: Environment Admin or Organization Admin at `console.pingone.com`.
  - PingOne ST: Tenant Administrator on your PingOne ST tenant.
  - Ping Software Suite: Server admin credentials for PingFederate/PingAccess/PingDirectory.
- For PingOne MT: network access to `console.pingone.com` and `auth.pingone.com`.
- For PingOne ST: your tenant's base URL (format: `https://<tenant>.forgeblocks.com` or custom domain).
- For Software Suite: server access to deployed nodes; admin console TCP port (default 9999 for PingFederate).
- A registered application (OAuth client) for any flow that issues tokens; note the client ID and redirect URIs before starting.
- For SDK-based app integration: a development environment for the target platform (Android Studio, Xcode, or Node.js); see `ping-app-integration` for details.
- For risk-based or MFA flows: a PingOne MFA or PingOne Protect license; confirm entitlements before configuring policies.
- For identity verification (KYC): a PingOne Verify license; see `ping-universal-services` → verify branch.

---

## Common variants

**Trial vs production environment:**
- Trial environments have reduced rate limits, no SLA, and expire after 30 days.
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

- PingOne MT: https://docs.pingidentity.com/pingone/getting_started_with_pingone/p1_getting_started.html
- PingOne for Enterprise (P14E): https://docs.pingidentity.com/pingoneforenterprise/pingone_for_enterprise/p14e_getting_started.html
- AIC: https://docs.pingidentity.com/pingoneaic/getting-started/getting-started-about.html
- PingFederate: https://docs.pingidentity.com/pingfederate/13.0/pf_pf_landing_page.html
