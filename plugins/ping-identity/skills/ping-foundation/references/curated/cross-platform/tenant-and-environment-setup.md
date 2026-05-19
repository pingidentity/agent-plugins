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
last_updated: ""
slug: ""
---

# Tenant and Environment Setup

Provisioning requirements and key configuration decisions for a new PingOne environment or PingOne ST tenant.

## Scope

Covers: initial provisioning and configuration of environments/tenants.
Does NOT cover: on-prem server installation (see `core-admin-patterns.md`).

## PingOne MT — New Environment

**Admin surface:** apps.pingone.com → Environments → + Add Environment

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

**Prerequisites:** PingOne organization account with admin access.

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

**Prerequisites:** PingOne ST subscription; tenant URL and initial superadmin credentials from onboarding email.

## Related references

- `foundation-overview.md`
- `policy-and-branding-basics.md`

## Source

[PingOne Documentation](https://docs.pingidentity.com/pingone/)
[PingOne ST Documentation](https://docs.pingidentity.com/pingoneaic/)
