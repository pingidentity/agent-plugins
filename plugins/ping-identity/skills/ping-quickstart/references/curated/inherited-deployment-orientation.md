---
title: "Orienting Yourself in an Inherited Ping Identity Deployment"
product_family: cross-platform
products: ["pingone", "pingone-aic", "pingfederate", "pingone-st"]
capabilities: ["quickstart", "foundation"]
services: []
audience: ["admin", "architect"]
use_cases: ["workforce", "customer", "cross-platform"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-01"
slug: "https://docs.pingidentity.com/pingoneforenterprise/p14e_which_p14e_am_i_using.html"
---

# Orienting Yourself in an Inherited Ping Identity Deployment

How to identify which Ping Identity product you have been given access to, discover what is already configured, and determine your next step.

## Scope

**Covers:** identifying the Ping product variant from access credentials or console URLs; running a discovery checklist for PingOne (multi-tenant cloud), AIC, and PingFederate; understanding environment types and realm constraints in an inherited tenant.

**Does NOT cover:** creating new tenants, environments, or applications (see `ping-foundation` skill); designing authentication journeys or DaVinci flows (see `ping-orchestration` skill); migrating from a legacy ForgeRock deployment (see `forgerock-to-ping-journey-migration` skill).

---

## Step 1: Identify which product you have

Use the admin console URL or tenant URL you were given to determine which product family applies before reading any further.

| Console URL or URL pattern | Product | Notes |
|---|---|---|
| `console.pingone.com` | **PingOne (multi-tenant cloud)** | Multi-tenant SaaS. Organizations, environments, and a flat admin hierarchy. |
| `admin.pingone.com` | **PingOne for Enterprise (P14E)** | Older SaaS product. Four sub-variants — see table below. |
| `openam-<base>-<region>.id.forgerock.io` | **AIC (Production)** | Single-tenant managed cloud. ForgeRock lineage. |
| `openam-<sandbox>-<region>.forgeblocks.com` | **AIC (Sandbox)** | Sandbox environment on Rapid channel. |
| `https://<host>:9999/pingfederate/app` | **PingFederate** | On-premises or customer-managed. Not SaaS. |

### P14E sub-variant identification

Log in to `admin.pingone.com` and inspect the top navigation items.

| Top nav items present | Sub-variant |
|---|---|
| Dashboard / Apps / Users / Setup / Account | Standard P14E |
| Above + **Customers** | P14E for MSPs |
| Above (no Customers) + **Customer Connections** | PingOne SSO for SaaS Apps |
| Above + **Customer Connections** + **Managed Accounts** | PingOne SSO for SaaS Apps with Managed Accounts |

P14E is a mature product with limited new feature investment. If the organization is planning expansion, confirm whether a migration to PingOne (multi-tenant cloud) or AIC is on the roadmap.

---

## Step 2: PingOne discovery checklist

Work through these areas in order. All are configuration facts — no step-by-step UI procedures.

**Organization Settings**
- License type assigned to the organization (ADMIN, TRIAL, SOLUTION, JIT_TRIAL, or a Combo license such as MFA-Protect).
- One license is enforced per environment; confirm which environments hold which license types.
- Note whether an **Administrators environment** exists as a dedicated environment — best practice is to isolate admin users from production environments. Older organizations may co-locate admins in a general-purpose environment.

**Environment inventory**
- List all environments. For each, note: environment type (Sandbox / Development / UAT / Staging / Production), the license attached, and whether it is a production-tier environment with an SLA.
- Sandbox environments are for exploration; they are not in a promotion pipeline. Development environments are the lowest pipeline-member tier.
- A TRIAL license indicates the organization is still in evaluation mode (up to 5 environments, 30 days, 1 000 active identities).

**Applications**
- List registered OAuth/OIDC applications in each environment. Note client IDs, grant types, and redirect URIs.
- Custom domain configured on any environment is a paid-tier indicator (custom domains are not available on trial).

**Sign-on policies**
- List active sign-on policies per environment. Note whether MFA factors are enrolled and which factor types are active (TOTP, SMS, email, FIDO2).

**Integration readiness**
- Check whether PingOne Protect or PingOne Verify are licensed (these are add-ons, not in the base bundle).
- Check whether DaVinci is enabled in any environment. DaVinci licensing is either identity-based (MAU/AAU) or transaction-based (flow invocations) — confirm which model applies.

---

## Step 3: AIC discovery checklist

**Realms**
- Confirm which realms exist. The hard limit is exactly two configurable end-user realms: **Alpha** and **Bravo**. The top-level realm is reserved for tenant administrators only and cannot hold end-user identities.
- If more than two end-user realms appear to exist, verify with your Ping account team — this would be an unusual custom configuration.
- Alpha supports delegated administration and IGA (add-on). Bravo does not. Workloads requiring delegated admin must use the Alpha realm.

**Identity stores**
- For each realm, check the identity store type: built-in managed identities, PingDirectory (DS), or external LDAP.
- PingDirectory integration is common in enterprise deployments and affects password policy, schema extensions, and backup/restore procedures.

**Authentication journeys**
- List authentication journeys (trees) in each realm. Note which journeys are bound to which applications.
- Identify journeys that use custom scripting nodes — these require scripting knowledge to maintain.

**OAuth clients and redirect URIs**
- List OAuth 2.0 clients per realm. For each client, note: client type (confidential vs public), grant types, and redirect URIs.
- Redirect URIs require exact match — adding a new environment requires updating the client.

**Branding and themes**
- Check whether custom themes are applied in each realm. Custom themes affect the hosted login pages.

**FQDN and channel**
- Note the tenant FQDN. Production tenants use `.id.forgerock.io`; sandbox tenants use `.forgeblocks.com`.
- Confirm whether the tenant is on Rapid channel (sandbox, no HA, config not in a pipeline) or Regular channel (dev/uat/staging/prod, promotable).

---

## AIC environment types

| Type | Included / Add-on | HA | In pipeline | Identity cap | SLA | Intended use |
|---|---|---|---|---|---|---|
| Sandbox | Included | No | No | 10 000 | No | Exploration, proof of concept |
| Development | Included | No | Yes | 10 000 | No | Active development |
| UAT | Paid add-on | Yes | Yes | No cap | No | Pre-production; pen/load testing permitted |
| Staging | Included | Yes | Yes | No cap | No | Pre-production validation |
| Production | Included | Yes | Yes | No cap | Yes | Live traffic |

Sandbox is on the Rapid channel and is isolated from the promotion pipeline. Configuration changes made in Sandbox cannot be promoted to Development or beyond without manual re-creation. UAT and additional Sandbox environments are paid add-ons; Development, Staging, and Production are included in the base tenant.

---

## Step 4: PingFederate discovery checklist

**License**
- Verify the license expiry date in the admin console. An expired license blocks runtime operations.
- PingFederate licensing tiers are not published in public documentation; contact your account team for details.

**SP connections**
- List all Service Provider (SP) connections. For each connection, note: protocol (SAML 2.0, WS-Federation, OAuth), enabled state, and whether it has active signing certificate bindings. Inactive connections with expired certificates are a common inherited problem.

**IdP adapters**
- List IdP adapters configured (HTML Form, Kerberos, X.509, etc.). Adapters implement the authentication mechanism presented to users.
- Custom adapter JARs require Java compatibility verification if a PingFederate version upgrade is planned.

**Data stores**
- List data store connections (LDAP/AD, JDBC, PingDirectory). Note the connection status and whether the bind credentials have been rotated recently.
- Stale LDAP bind credentials are a frequent cause of authentication failures in inherited deployments.

**Topology**
- Note whether PingFederate is running standalone or in a cluster. Clustered deployments require all nodes to have consistent configuration and synchronized keystores.
- Check whether PingDirectory is integrated as the identity store or as the OAuth authorization server backing store.

---

## Realm isolation reminder (AIC)

Realm isolation in AIC is complete. An identity in Alpha cannot authenticate to an application registered in Bravo. OAuth clients, sign-on policies, and user populations are fully separated between realms. If users report "access denied" errors after an environment handover, confirm the application is registered in the correct realm and the user exists in that realm's identity store.

---

## What to do next

| What you found | Next step |
|---|---|
| PingOne with no applications configured | Use `ping-foundation` skill to register your first application and configure a sign-on policy |
| PingOne with applications already registered, need to add a flow | Use `ping-orchestration` skill (DaVinci) |
| AIC with journeys in place, need to render them in a mobile app | Use `ping-orchestration-sdks` skill for iOS or Android |
| AIC with journeys, need to render in a web app | Use `ping-orchestration-sdks` skill (JavaScript/React path) |
| PingFederate standalone, need to federate with PingOne | Use `ping-foundation` skill — PingFederate as external IdP pattern |
| Legacy ForgeRock SDK in mobile or web app | Use `forgerock-to-ping-journey-migration` skill |
| PingFederate + PingOne migration in scope | See Cloud Acceleration Toolset reference below |
| AIC tenant, need to understand the migration phases | See AIC planning reference below |

---

## Prerequisites

- Admin or read-only admin credentials for the console you are accessing.
- For AIC: the base FQDN of the tenant (provided by Ping Identity when the tenant was provisioned).
- For PingFederate: network access to port 9999 on the admin node and an admin account.

---

## Common variants

**P14E with directory sync**: Some P14E deployments are backed by an on-premises Active Directory via the PingOne Gateway. Check Setup → Identity Repositories for configured directories before making user management changes.

**AIC with custom top-level domain**: Tenants configured with a custom vanity FQDN (e.g., `login.example.com`) will not match the `.id.forgerock.io` or `.forgeblocks.com` patterns. Inspect the TLS certificate or DNS CNAME chain to confirm the underlying platform.

**PingOne with Rate groups**: As of September 2025, PingOne enforces rate groups on API and flow-invocation traffic. Inherited deployments at high request volumes may be subject to throttling if the rate group baseline was not established before that date. Additional capacity requires the Maximum Throughput Assurance add-on.

**AIC Sandbox not in pipeline**: A common inherited confusion — Sandbox configuration changes cannot be promoted. If you need changes to flow to Dev/UAT/Staging/Prod, they must be made in the Development environment, not in Sandbox.

---

## Related references

- `references/curated/choose-the-right-ping-platform.md` — use when you need to compare platforms before picking one, rather than orienting in an existing one
- `references/curated/getting-started-overview.md` — high-level entry point for brand-new deployments
- `references/curated/common-starting-patterns.md` — task patterns once you have completed orientation

---

## Source

- Which PingOne am I using: https://docs.pingidentity.com/pingoneforenterprise/p14e_which_p14e_am_i_using.html
- PingOne getting started: https://docs.pingidentity.com/pingone/getting_started_with_pingone/p1_getting_started.html
- PingOne license types: https://docs.pingidentity.com/pingone/getting_started_with_pingone/p1_license_types.html
- PingOne platform limits: https://docs.pingidentity.com/pingone/getting_started_with_pingone/p1_platform_limits.html
- AIC environments: https://docs.pingidentity.com/pingoneaic/tenants/environments.html
- AIC realms: https://docs.pingidentity.com/pingoneaic/realms/alpha-bravo-realms.html
- AIC getting started: https://docs.pingidentity.com/pingoneaic/getting-started/getting-started-about.html
- Cloud Acceleration Toolset (PF → PingOne): https://docs.pingidentity.com/pingone/migration-tools/p1_cloud_acceleration_toolset.html
- AIC planning/migration: https://docs.pingidentity.com/pingoneaic/planning/plan-identity-cloud.html
- PingFederate landing: https://docs.pingidentity.com/pingfederate/13.0/pf_pf_landing_page.html
