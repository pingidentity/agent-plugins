---
title: "Tenant and Environment Setup"
product_family: cross-platform
products: ["pingone", "pingone-st"]
capabilities: ["foundation"]
audience: ["admin"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/pingone/environments/p1_c_environments.html"
---

# Tenant and Environment Setup

Provisioning requirements and key configuration decisions for a new PingOne environment or PingOne ST tenant.

## Scope

Covers: initial provisioning and configuration of environments/tenants.
Does NOT cover: on-prem server installation (see `references/curated/cross-platform/core-admin-patterns.md`).

## PingOne MT — New Environment

**Admin surface:** console.pingone.com → Environments → + Add Environment

**Required decisions:**
- Environment type: Sandbox, Development, or Production — determines SLA and capability profile
- Region selection: affects data residency
- Services to enable: MFA, Verify, DaVinci, Risk, etc. must be explicitly activated per environment
- Initial population: create an admin population or connect an external directory before adding users

**Key settings to establish before adding apps or users:**

| Setting | Location |
|---|---|
| Custom domain | Settings → Custom Domains |
| Notification sender (email/SMS) | Settings → Notifications |
| Default sign-on policy | Policies → Sign-on |

---

## PingOne ST — New Tenant

**Admin surface:** Your PingOne ST tenant URL (provided by Ping during onboarding)

**Required decisions:**
- Identity store: PingDS (default, no setup needed) or external LDAP/AD (requires additional configuration)
- Realm usage: `alpha` and `bravo` realms exist by default; decide which to use for customer-facing vs. internal flows before registering apps
- Custom domain: must be configured before go-live for production tenants

**Key settings to establish before adding journeys or apps:**

| Setting | Location |
|---|---|
| Identity store selection | Realm → Identity Stores |
| Custom domain | Tenant Settings → Custom Domains |
| Email provider | Email → SMTP or Ping-managed |
| Default theme | Themes → create or edit per realm |

**Common post-setup tasks:**
- Import users or configure LDAP sync
- Enable social providers (Google, Apple, etc.)
- Configure federation (SAML SP or OIDC RP)

## Pre-go-live checklist (both platforms)

Complete these before routing live users to the environment:

| Item | PingOne MT | PingOne ST |
|---|---|---|
| Custom domain configured | Settings → Custom Domains | Tenant Settings → Custom Domains |
| Email sender verified | Settings → Notifications → Senders | Notifications → Email provider |
| MFA / authentication policy in place | Policies → Sign-on | Realm → Authentication → Journeys |
| Application registered with correct redirect URIs | Applications → + Add Application | Applications → OAuth 2.0 Clients |
| Branding applied (logo, colors) | Branding | Realm → Theming |
| Population / identity store configured | Directory → Populations | Realm → Identity Stores |
| Notification templates customized | Branding → Email / SMS templates | Realm → Notifications → Templates |

---

## Configuration-as-code and promotion patterns

| Pattern | PingOne MT | PingOne ST | Ping Software Suite |
|---|---|---|---|
| Export configuration | Admin API export; or `frodo-cli` | Admin API export; or frodo-cli | Git-backed server profile; or archive ZIP |
| Import to another environment | Admin API import; or frodo-cli push | Admin API import; or frodo-cli push | Redeploy from server profile Git branch |
| CI/CD integration | Worker app (client credentials) to authenticate pipeline API calls | AM/IDM service accounts from pipeline | Server profile Git push triggers config rebuild |
| Secrets management | Store client secret in pipeline secret store; never in source code | ESV (Environment-Specific Variables) for runtime secrets | Vault integration or environment variable injection at container startup |
| Secrets management | Store client secret in pipeline secret store; never in source code | ESV (Environment-Specific Variables) in PingOne ST for secrets and config values |

---

## Common gotchas

| Gotcha | Applies to | Fix |
|---|---|---|
| Environment type immutable after creation | PingOne MT | Verify type (Sandbox / Development / Production) before creating; cannot be changed |
| Region immutable after environment creation | PingOne MT | Select data residency region at creation time; cannot be changed after |
| Services must be explicitly activated per environment | PingOne MT | DaVinci, Verify, Protect, etc. must be toggled on per environment — they are not on by default |
| Custom domain required for production hosted login | Both | Users see Ping's default domain without a custom domain configuration |
| Realms in PingOne ST cannot be merged | PingOne ST | Plan realm architecture (alpha vs. bravo vs. additional) before onboarding users; migrating users between realms is manual |

## Prerequisites

- **PingOne MT:** PingOne organization account with admin access. Admin role: Environment Admin or Organization Admin. DNS control for custom domain configuration.
- **PingOne ST:** PingOne ST subscription; tenant URL and initial superadmin credentials from onboarding email. Custom domain DNS control for production tenants.
- **Ping Software Suite:** Java 11 or 17 JRE; license file from Ping Identity; Linux or Windows server meeting minimum hardware requirements per product.

## Common variants

| Variant | Note |
|---|---|
| Multi-region HA tenants | PingOne ST production tenants support multi-region high availability; configured during Ping Identity onboarding |
| Sandbox-to-production promotion | Export configuration from dev/staging using frodo-cli or admin API; import to production tenant |
| Environment-per-pipeline | PingOne MT supports multiple environments (dev, staging, prod) within one organization; use environment types to control SLA |
| Blue/green deployment (Ping Software) | Run two server profile branches; switch load balancer to the new profile after validation; rollback by switching back |
| Secrets rotation without downtime | Store secrets in a vault (HashiCorp Vault, AWS Secrets Manager); configure products to read secrets at startup; rotate in vault first, then restart |

## Ping Software Suite — Server provisioning overview

On-premises Ping software requires manual provisioning steps beyond cloud platform onboarding. License files must be obtained from Ping Identity before installation; the server will not start without a valid license.

| Product | Provisioning steps | Documentation anchor |
|---|---|---|
| PingFederate | Install, license, configure admin console, LDAP data store | `references/curated/ping-software/pingfederate-basics.md` |
| PingDirectory | Install, setup wizard (non-interactive via `--cli`), replication | `references/curated/ping-software/pingdirectory-basics.md` |
| PingAccess | Install, license, configure token provider (PingFederate or PingOne) | `references/curated/ping-software/pingaccess-basics.md` |

All three products support Git-backed server profiles for configuration-as-code deployments. Server profiles are the recommended approach for container-based (Docker/Kubernetes) deployments.

---

## Related references

- `references/curated/cross-platform/foundation-overview.md` — platform family orientation and capability comparison
- `references/curated/cross-platform/policy-and-branding-basics.md` — authentication policy and branding once tenant is provisioned
- `references/curated/pingone-mt/tenant-and-environment-setup.md` — PingOne MT-specific environment configuration details
- `references/curated/pingone-st/foundation-overview.md` — PingOne ST tenant architecture and admin surfaces

## Common gotchas across platforms

| Gotcha | Applies to | Fix |
|---|---|---|
| License file missing before first start | Ping Software Suite | Obtain a valid license file from Ping Identity support before installation; the server will not start |
| Admin pop-up blocks service activation prompt | PingOne MT | Service activation requires an explicit step in the environment settings; it is not triggered automatically when creating apps |
| Config promotion missing schema extensions | PingOne ST | Export schema changes from IDM first; import them before importing managed object data |

## Source

[PingOne environments](https://docs.pingidentity.com/pingone/environments/p1_c_environments.html)
[PingOne ST tenant administration](https://docs.pingidentity.com/pingoneaic/getting_started/getting_started-create_tenant.html)
[PingOne MT environment types](https://docs.pingidentity.com/pingone/environments/p1_environment_types.html)
[frodo-cli for PingOne config export](https://github.com/rockcarver/frodo-cli)
