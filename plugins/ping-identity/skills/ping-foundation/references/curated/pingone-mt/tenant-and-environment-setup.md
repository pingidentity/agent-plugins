---
title: "PingOne MT — Tenant and Environment Setup"
product_family: pingone-mt
products: ["pingone"]
capabilities: ["foundation"]
audience: ["admin"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-05-19"
slug: "https://docs.pingidentity.com/pingone/latest/platformconsole/p1_c_environments.html"
---

# PingOne MT — Tenant and Environment Setup

Provisioning and initial configuration for PingOne MT environments, including environment types, service activation, and key pre-app settings.

## Scope

**Covers:** PingOne MT organization structure, environment types, service activation, populations, and pre-app configuration.
**Does NOT cover:** On-prem server installation — see `references/curated/cross-platform/core-admin-patterns.md`. PingOne ST tenants — see `references/curated/cross-platform/tenant-and-environment-setup.md`.

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

**Organization:** Top-level billing and admin unit. One organization per PingOne MT customer.

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
| Services | Select services to activate (MFA, Verify, DaVinci, Risk, Credentials, IGA) — can be added later |

**API:** `POST /v1/environments`

---

## Key settings to configure before adding apps or users

| Setting | Location | Notes |
|---|---|---|
| Custom domain | Settings → Custom Domains | Required for branded hosted pages; DNS CNAME to Ping |
| Notification sender | Settings → Notifications | Email/SMS sender; verify domain ownership |
| Default sign-on policy | Policies → Sign-on | Applied to all apps unless overridden per app |
| Admin population | Directory → Populations | Create before provisioning admin users |

---

## MFA policy setup (PingOne MT)

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

[PingOne environments](https://docs.pingidentity.com/pingone/latest/platformconsole/p1_c_environments.html)
[PingOne MFA device policies](https://docs.pingidentity.com/pingone/latest/mfa/p1_c_mfa_device_policies.html)
[PingOne OIDC application setup](https://docs.pingidentity.com/pingone/latest/platformconsole/p1_c_apps.html)
[PingOne API reference](https://apidocs.pingidentity.com/pingone/platform/v1/api/)
