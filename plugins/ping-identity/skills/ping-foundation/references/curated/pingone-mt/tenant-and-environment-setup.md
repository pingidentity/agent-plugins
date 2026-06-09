---
title: "PingOne — Tenant and Environment Setup"
product_family: pingone-mt
products: ["pingone"]
capabilities: ["foundation"]
audience: ["admin"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-04"
slug: "https://docs.pingidentity.com/pingone/platformconsole/p1_c_environments.html"
---

# PingOne — Tenant and Environment Setup

Provisioning and initial configuration for PingOne environments, including environment types, service activation, and key pre-app settings.

## Scope

**Covers:** PingOne organization structure, environment types, service activation, populations, and pre-app configuration.
**Does NOT cover:** On-prem server installation — see `references/curated/cross-platform/core-admin-patterns.md`. PingOne Advanced Identity Cloud (AIC) tenants — see `references/curated/cross-platform/tenant-and-environment-setup.md`.

---

## Organization and environment model

```
PingOne Organization
└── Environment (one or more per org)
    ├── Population (user store)
    ├── Applications (OIDC, SAML, Worker)
    ├── Connections (external directories, identity providers)
    ├── Sign-on Policies
    └── Services (MFA, Verify, DaVinci, Risk, Credentials)
```

**Organization:** Top-level billing and admin unit. One organization per PingOne customer.

**Environment:** Logical container for a project, workload, or deployment stage (dev, staging, prod). All resources are environment-scoped.

---

## Environment types

| Type | SLA | Intended use |
|---|---|---|
| Sandbox | Best-effort | Isolated experimentation; no production data |
| Development | Best-effort | Feature development and integration testing |
| Production | SLA-backed | Live user traffic; highest availability |

Environment type is immutable after creation. Provision separate environments for each stage.

---

## Creating a new environment

**Required fields:**

| Field | Notes |
|---|---|
| Environment name | Human-readable identifier; not user-visible |
| Environment type | Sandbox, Development, or Production |
| Region | Affects data residency; cannot be changed after creation |
| License | Select which org license to use for this environment |
| Services | Select services to activate (MFA, Verify, DaVinci, Risk, Credentials, IGA) — can be added later |
| Generate sample populations and users | Optional (Sandbox only) — adds 2 sample populations and 40 sample users for testing; useful for hands-on exploration |

**API:** `POST /v1/environments`

**Service setup after creation:** Some products (e.g., PingFederate) require additional deployment steps after the environment is created. On the environment's Overview page, locate a grayed-out service and expand View Setup Instructions to complete setup. Cloud products are best deployed via Docker images (see Ping Identity DevOps site). PingOne services activate automatically at environment creation.

---

## Key settings to configure before adding apps or users

| Setting | Location | Notes |
|---|---|---|
| Custom domain | Settings → Custom Domains | Required for branded hosted pages; DNS CNAME to Ping |
| Notification sender | Settings → Notifications | Email/SMS sender; verify domain ownership |
| Default sign-on policy | Policies → Sign-on | Applied to all apps unless overridden per app |
| Admin population | Directory → Populations | Create before provisioning admin users |

---

## MFA policy setup (PingOne)

MFA policies are environment-scoped and control which authentication methods are permitted.

**Required decisions before configuring:**
- Which MFA methods to allow: TOTP authenticator, SMS OTP, email OTP, FIDO2/passkeys, push notification
- Default enrollment policy: optional, required on next login, or required immediately
- Grace period: number of days before enforcement after policy is applied

**MFA policy attachment:** A sign-on policy's MFA action references the MFA device policy. The policy must be assigned to the sign-on policy to take effect — creating the policy alone does not enable MFA.

**Admin surface:** Policies → MFA → + Add MFA Device Policy

---

## OIDC application (client credentials, M2M)

For a backend service using client credentials grant:

| Field | Notes |
|---|---|
| Application type | Worker (M2M) or OIDC Web App with Client Credentials grant |
| Grant type | Client Credentials only — no redirect URI needed |
| Token endpoint | `https://auth.pingone.com/{envId}/as/token` |
| Scopes | Minimum: none required; add resource scopes as needed |
| Client authentication | Client Secret Basic or Client Secret Post |

**Token endpoint authentication:** POST with `grant_type=client_credentials&client_id=<id>&client_secret=<secret>` (for `client_secret_post`) or HTTP Basic header (for `client_secret_basic`).

---

---

## Service activation reference

Services must be explicitly activated per environment before flows can use them. Activation is not inherited from other environments.

| Service | License tier | Activation effect |
|---|---|---|
| SSO | Base | Always active; cannot be disabled |
| MFA | Base or add-on | Enables MFA methods in sign-on policies and MFA device policies |
| DaVinci | Add-on | Enables DaVinci flow designer and DaVinci policy attachment to apps |
| Risk (PingOne Protect) | Add-on | Enables risk predictors, risk policies, and risk-based MFA conditions |
| Verify | Add-on | Enables PingOne Verify identity proofing actions in sign-on policies |
| Credentials | Add-on | Enables verifiable credential issuance and revocation |
| IGA | Add-on (separate onboarding) | Requires additional provisioning step by Ping Identity support |

---

## Environment URLs

Each PingOne environment exposes three distinct URLs, all visible under Settings > Environment Properties.

| URL | Purpose |
|---|---|
| Console Login URL | Direct sign-in to the admin console for this specific environment; share with new admins so they land on the correct environment |
| Self-Service URL | End-user self-service portal (profile management, password reset, MFA enrollment) |
| Application Portal URL | Application launcher for end users; lists all apps the user is entitled to access |

The Console Login URL is environment-specific — it differs from the global `console.pingone.com` entry point. Provide this URL, not the global one, when onboarding environment-scoped admins.

---

## Administrators environment

PingOne automatically creates an **Administrators environment** when the organization is first provisioned. This environment is distinct from all user-created environments.

| Property | Detail |
|---|---|
| Created by | Ping Identity at org provisioning; cannot be deleted |
| Purpose | Houses administrator identities; keeps admin accounts isolated from end-user populations |
| Best practice | Create all admin identities here; grant them environment-scoped roles on other environments from here |
| Getting Started Guide toggle | Settings > Environment Properties > Getting Started Guides — controls whether the admin wizard appears on the Environments page |

Administrator role assignments cross environment boundaries: a user in the Administrators environment can hold Environment Admin or Identity Data Admin for any other environment in the org.

---

## License and operational status

**Viewing licenses:** The Environments page > Licenses menu shows Admin License, Active Licenses, and Expired Licenses. Details include organization name, number of environments, and license type (e.g., INTERNAL, TRIAL, MFA TRIAL).

**Operational status:** Subscribe to real-time alerts for all Ping Identity services at [status.pingidentity.com](https://status.pingidentity.com/). Alerts cover PingOne, PingID, and other services; opt into email notifications from the status page.

---

## Common gotchas

| Gotcha | Symptom | Fix |
|---|---|---|
| Environment type immutable | Created sandbox instead of production | Provision a new environment with the correct type; no conversion path |
| Region immutable | Environment created in wrong region | Provision a new environment; migrate config and users |
| Service not activated | DaVinci flow designer not visible; risk conditions absent from policy editor | Activate the service in the environment's service management settings |
| Multiple populations on one app | Users in secondary population denied access | Add all relevant populations to the app's Allowed Populations list |
| Default policy changes affect all apps | Unintended behavior change after policy edit | Explicitly attach named policies to each app; avoid relying on the environment default |
| Worker app secret not saved at creation | Cannot retrieve secret later; all API calls fail | Rotate the secret immediately; copy the new value before closing the dialog |

## Prerequisites

- PingOne organization account with admin access
- Admin role assigned: Environment Admin or Organization Admin
- DNS control (for custom domain configuration)

## Common variants

| Variant | Note |
|---|---|
| Multiple environments per org | Supported; each environment is isolated; use environment clone for faster setup of staging/prod |
| Worker application for API automation | Create a Worker app with client credentials; assign admin roles to the worker app for API-driven config |
| Populations for multi-tenant use cases | Create separate populations to segment user groups; policies and apps can target specific populations |

## Related references

- `references/curated/cross-platform/foundation-overview.md`
- `references/curated/cross-platform/tenant-and-environment-setup.md`
- `references/curated/cross-platform/policy-and-branding-basics.md`

## Source

[PingOne environments](https://docs.pingidentity.com/pingone/platformconsole/p1_c_environments.html)
[PingOne MFA device policies](https://docs.pingidentity.com/pingone/mfa/p1_c_mfa_device_policies.html)
[PingOne OIDC application setup](https://docs.pingidentity.com/pingone/platformconsole/p1_c_apps.html)
[PingOne API reference](https://apidocs.pingidentity.com/pingone/platform/v1/api/)
