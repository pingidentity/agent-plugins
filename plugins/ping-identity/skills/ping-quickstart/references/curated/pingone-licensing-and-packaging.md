---
title: "PingOne Licensing and Packaging"
product_family: pingone-mt
products: ["pingone"]
capabilities: ["quickstart", "foundation"]
services: ["identity-management", "mfa", "davinci", "protect", "verify"]
audience: ["admin", "architect"]
use_cases: ["workforce", "customer"]
doc_type: reference
status: current
canonical: true
last_updated: "2026-06-01"
slug: https://docs.pingidentity.com/pingone/getting_started_with_pingone/p1_license_types.html
---

# PingOne Licensing and Packaging

Reference for PingOne MT license types, the one-license-per-environment constraint, identity limits, DaVinci pricing models, key add-ons, and platform limits — everything a new user needs to avoid confusing quota errors.

## Scope

Covers:
- PingOne MT license types (ADMIN, TRIAL, SOLUTION, JIT_TRIAL, Combo)
- One-license-per-environment rule and combo license upgrade path
- Identity soft and hard limits (MAU/AAU-based)
- DaVinci pricing models (identity-based vs transaction-based)
- Key add-ons: PingOne Verify, PingOne Protect, PingID, custom domains, email customisation
- Platform limits for trial and paid orgs
- Trial gotchas and license expiry behaviour

Does NOT cover:
- Per-SKU pricing tables — these are not published; contact your Account Executive
- PingFederate licensing tiers — not published publicly
- Purchasing, contract terms, or renewal procedures — Sales/AE only

---

## License types

| License type | What it is | When you encounter it |
|---|---|---|
| ADMIN | Reserved for the Administrators environment; grants org-level console access | Present in every org; do not use for end-user workloads |
| TRIAL | Self-service evaluation license; 30-day term, 1,000 active identities, up to 5 environments in 1 geography | Default for new sign-ups; auto-applied at org creation |
| SOLUTION | Production-grade license purchased per bundle (e.g., SSO, MFA, SSO+MFA) | Applied to each paid environment; one per environment |
| JIT_TRIAL | Just-in-time trial for a specific feature or add-on (e.g., Protect); short-lived | Provisioned automatically when previewing a new capability |
| Combo | A SOLUTION license that bundles two or more services (e.g., MFA+Protect, SSO+MFA+DaVinci) | Required when adding a second licensed service to an existing environment |

**Rule of thumb:** If your environment was created with an MFA license and you want to add Protect, you do not get a second license — you upgrade to an MFA+Protect combo license on the existing environment.

---

## The one-license-per-environment constraint

Each PingOne environment holds exactly one license. This is a hard system constraint and cannot be overridden.

**Practical consequence:** Adding a new billable service to an environment does not stack a second license alongside the first. Instead, the existing license must be replaced with a combo license that covers both services.

| Scenario | Correct path |
|---|---|
| MFA environment; want to add Protect | Upgrade to MFA+Protect combo license (requires AE) |
| SSO environment; want DaVinci | Upgrade to SSO+DaVinci combo license |
| Want MFA and Protect in separate environments | Each environment needs its own combo or standalone license |

Attempting to enable a service not covered by the current license produces a capability error in the console. This is the most common source of confusion for new admins.

---

## Identity limits

PingOne identity limits are derived from the licensed Monthly Active Users (MAU) or Annual Active Users (AAU) figure on the SOLUTION license.

| Limit tier | Value |
|---|---|
| Soft limit | 12 × licensed MAU/AAU |
| Hard limit | Soft limit + 10%, capped at 100 million identities |

When the soft limit is reached, PingOne generates a warning in the admin console. When the hard limit is reached, new identity creation is blocked. Existing users continue to authenticate.

During trial, the hard identity limit is 1,000 active identities regardless of the 12× formula.

---

## DaVinci licensing models

DaVinci can be licensed in two ways. The model is determined at purchase time and reflected on the SOLUTION or Combo license.

### Identity-based (MAU/AAU)

- Metered against the same MAU/AAU pool as the rest of PingOne
- Fair-use cap: up to 80 connector executions per flow invocation
- Subflows are excluded from the connector execution count

### Transaction-based (flow invocations)

- Metered per flow invocation, not per identity
- Fair-use cap: 80 connector executions per flow invocation
- Subflows are excluded from the invocation count
- Applies to the **PingOne for Customers Passwordless bundle** (Protect + SSO + MFA via DaVinci)

### PingOne for Customers Passwordless bundle

- Licensed per flow invocation
- Includes Protect + SSO + MFA capabilities
- All end-user authentication **must** go through DaVinci flows; direct Journey or standalone MFA calls are not supported under this bundle
- Mixing direct API calls with DaVinci-based flows violates fair-use terms

---

## Key add-ons

The following capabilities are add-ons — they are not included in the base Essential or Plus bundles and require a separate purchase or upgrade.

| Add-on | Metering model | Notes |
|---|---|---|
| PingOne Verify | Per verification transaction | Covers document and biometric verification; not in any base bundle |
| PingOne Protect | Per MAU or bundle inclusion | Requires Ping Professional Services **Threat Protection QuickStart** as a mandatory attach ($26,000, 2-week engagement) |
| PingID | Separate license; starts on trial | Remains on trial until explicitly upgraded via AE; trial PingID does not expire on the same schedule as the org trial |
| Custom domains | Paid environments only | Not available in trial; DNS ownership verification required |
| Email customisation | Paid environments only | Custom sender domain and branded templates unavailable in trial |

---

## Platform limits

### Trial organisations

| Limit | Value |
|---|---|
| Duration | 30 days |
| Environments | 5 maximum, 1 geography |
| Active identities | 1,000 |
| Features excluded | Custom domains, email customisation, rate assurance add-ons |

### Paid organisations

| Limit | Value |
|---|---|
| Environments per org | 500 |
| Applications per environment | 4,000 |
| Identity providers per environment | 1,000 |
| Gateways per environment | 20 |
| Sign-on policies per environment | 100 |
| Webhooks per environment | 50 |

### Rate limits

Rate groups are enforced in PingOne MT as of **September 2025**. Each environment is assigned a rate group based on its license tier. Additional throughput capacity is available via the **Maximum Throughput Assurance** add-on (contact AE).

---

## Trial gotchas

**What works in trial:**
- Full PingOne MT console access
- Up to 5 environments (including the mandatory Administrators environment)
- Core SSO, MFA, and DaVinci flow authoring
- API access with the same permissions as paid

**What does not work in trial:**
- Custom domains (DNS branding)
- Custom email sender domains and branded templates
- PingOne Verify (add-on, not provisioned in trial)
- Rate assurance guarantees

**License expiry behaviour:**
When a paid SOLUTION license expires:
- Admin console access is retained
- Configuration changes are paused (no new apps, IdPs, or policy changes)
- End-user authentication and self-service flows continue uninterrupted until the grace period ends

When a TRIAL license expires after 30 days:
- End-user flows stop immediately
- Admin access is retained to allow export or upgrade
- Environments are not deleted but enter a suspended state

---

## Prerequisites

- A PingOne organisation created at [console.pingone.com](https://console.pingone.com)
- ADMIN-level access to the organisation (Environment Admin role minimum)
- For add-on purchases or combo license upgrades: an active relationship with a Ping Identity Account Executive

---

## Common variants

**Inherited deployment with unknown license type**
Check Organisation Settings in the PingOne console: each environment lists its assigned license name. The ADMIN license on the Administrators environment is always present and does not count against your SOLUTION entitlements.

**DaVinci appears grayed out in the console**
The current environment license does not include DaVinci. The environment needs a combo license upgrade (e.g., SSO → SSO+DaVinci). Raise a request with your AE.

**PingID stays on trial after org upgrade**
PingID is licensed separately from PingOne MT. An org-level upgrade does not automatically upgrade PingID. Contact your AE to add PingID to the contract.

**Rate limit errors after September 2025**
Rate groups are now enforced. Verify the environment's rate group assignment in Organisation Settings. Purchase the Maximum Throughput Assurance add-on if limits are insufficient for production traffic.

---

## Related references

- `skills/ping-quickstart/references/curated/getting-started-overview.md` — platform family selection and first-step orientation
- `skills/ping-quickstart/references/curated/choose-the-right-ping-platform.md` — decision guide for PingOne MT vs AIC vs PingFederate
- `skills/ping-foundation/references/` — environment configuration, applications, and IdP setup

---

## Source

- PingOne license types: https://docs.pingidentity.com/pingone/getting_started_with_pingone/p1_license_types.html
- PingOne licenses and identities: https://docs.pingidentity.com/pingone/getting_started_with_pingone/p1_licenses_and_identities.html
- PingOne license FAQ: https://docs.pingidentity.com/pingone/getting_started_with_pingone/p1_license_faq.html
- PingOne platform limits: https://docs.pingidentity.com/pingone/getting_started_with_pingone/p1_platform_limits.html
