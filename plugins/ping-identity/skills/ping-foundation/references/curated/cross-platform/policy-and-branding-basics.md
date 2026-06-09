---
title: "Policy and Branding Basics"
product_family: cross-platform
products: ["pingone", "pingone-st"]
capabilities: ["foundation"]
audience: ["admin"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/pingone/authentication/p1_authenticationpolicies.html"
---

# Policy and Branding Basics

Core configuration decisions for authentication policy and UI branding across PingOne (multi-tenant cloud) and PingOne Advanced Identity Cloud (AIC).

## Scope

Covers: sign-on policies, MFA policies, themes, and hosted page customization.
Does NOT cover: DaVinci flow design or AIC journey logic — see `ping-orchestration`.

---

## PingOne (multi-tenant cloud) — Authentication Policies

**Sign-on policy structure:**
- An ordered list of actions evaluated at sign-in
- Actions: Login, MFA, Identity Verification, Progressive Profiling, Agreement
- Policies attach to one or more applications; each app can reference a different policy

**Action conditions:** always, risk-based (requires PingOne Protect), or device-based

**MFA policy:**
- Controls which MFA methods are allowed: TOTP, SMS, email OTP, FIDO2, passkeys
- Configured at environment level; can be overridden per application
- Must be assigned to a sign-on policy's MFA action to take effect

**Admin surface:** Policies → Sign-on → + Add Policy

---

## PingOne (multi-tenant cloud) — Branding

| Setting | Location |
|---|---|
| Logo, colors, favicon | Branding → Edit |
| Email / SMS notification templates | Branding → Email / SMS templates |
| Custom domain (required for branded hosted pages) | Settings → Custom Domains |

---

## AIC — Policies

- Authentication policies are realm-scoped
- Auth trees/journeys define the login flow — see `ping-orchestration` for journey design
- Policy sets apply authorization rules after authentication completes

**Journey-as-policy:** In AIC, the journey itself is the authentication policy. Bind a journey to the realm default or to a specific application to control which flow is used.

**Admin surface:** Realm → Authentication → Trees or Journeys

---

## AIC — Theming

For AIC theming configuration, see `references/curated/pingone-st/themes-and-customization.md`.

---

## Notification templates

Both PingOne (multi-tenant cloud) and AIC support custom email and SMS notification templates.

### PingOne (multi-tenant cloud)

| Template type | Admin surface |
|---|---|
| Email templates | Branding → Email Templates |
| SMS templates | Branding → SMS Templates |
| Notification sender | Settings → Notifications → Senders |

Email templates support HTML with merge variables (e.g., `${user.username}`, `${user.name.given}`). Verify sender domain ownership before go-live; unverified domains use Ping's default sending address.

### AIC

Notification templates are managed at the realm level. AIC supports locale-specific templates — add locale variants under the template editor to serve translated content based on the user's browser language.

---

## Branding checklist (pre-go-live)

| Item | PingOne (multi-tenant cloud) | AIC |
|---|---|---|
| Custom domain configured and DNS verified | Settings → Custom Domains | Tenant Settings → Custom Domains |
| Logo uploaded | Branding → Logo | Theme Editor → Logo |
| Brand colors set | Branding → Colors | Theme Editor → Colors |
| Email/SMS sender verified | Settings → Notifications | Notifications → Email provider |
| Notification templates customized | Branding → Email / SMS templates | Realm → Notifications → Templates |
| Error page branding applied | Branding (limited control) | Custom CSS in Theme Editor |

---

## Common gotchas

| Gotcha | Applies to | Fix |
|---|---|---|
| Notification sent from Ping default address | PingOne (multi-tenant cloud) | Verify sender domain under Settings → Notifications → Senders before testing emails |
| MFA policy not taking effect despite being configured | PingOne (multi-tenant cloud) | Policy must be referenced inside an MFA action in a sign-on policy, and that policy must be attached to the application |
| Journey is not branded | AIC | Assign the theme to the realm (default) or to the specific journey in journey settings |
| Custom font not loading | AIC | Add font origin to Content Security Policy (CSP) settings; CSP blocks unconfigured external origins |
| Policy change affects all apps silently | PingOne (multi-tenant cloud) | Apps with no explicit policy assignment use the environment default — change to default affects all such apps simultaneously |

## Prerequisites

Admin access to the target platform (PingOne organization admin for MT; AIC tenant admin for ST).

## Common variants

| Variant | Note |
|---|---|
| Workforce vs. CIAM | Workforce MFA policy typically uses TOTP/push; CIAM policies often add risk-based conditions and progressive enrollment |
| Multi-application policies | PingOne (multi-tenant cloud) supports per-application policy override; AIC uses per-journey auth assignment |
| Layered branding | PingOne (multi-tenant cloud) supports global branding overridden per environment; AIC supports realm and journey-level theme override |

---

## PingFederate — Authentication policies (on-premises)

PingFederate 10+ replaces per-SP adapter configuration with centralized authentication policies — directed graphs of authentication sources and contract mappings.

| Concept | Description |
|---|---|
| Authentication policy | Directed graph; nodes are adapters or IdP connections; branches are outcomes |
| Contract | Set of attributes passed through the policy; mapped to SAML assertions or OIDC claims at the SP end |
| Selector | Evaluates context (IP, device, claim) to route to different authentication paths |
| Composite adapter | Chains two adapters (e.g., HTML Form + PingID) to implement MFA within a single policy node |

---

## Related references

- `references/curated/cross-platform/foundation-overview.md`
- `references/curated/cross-platform/tenant-and-environment-setup.md`
- `references/curated/cross-platform/core-admin-patterns.md`

## Source

[PingOne sign-on policies](https://docs.pingidentity.com/pingone/latest/platformconsole/p1_c_sign_on_policies.html)
[PingOne branding](https://docs.pingidentity.com/pingone/latest/platformconsole/p1_c_branding.html)
[AIC authentication journeys](https://docs.pingidentity.com/pingoneaic/am-journey-guide/journey-overview.html)
