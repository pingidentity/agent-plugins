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
last_updated: "2026-05-19"
slug: ""
---

# Policy and Branding Basics

Core configuration decisions for authentication policy and UI branding across PingOne MT and PingOne ST.

## Scope

Covers: sign-on policies, MFA policies, themes, and hosted page customization.
Does NOT cover: DaVinci flow design or PingOne ST journey logic — see `ping-orchestration`.

---

## PingOne MT — Authentication Policies

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

## PingOne MT — Branding

| Setting | Location |
|---|---|
| Logo, colors, favicon | Branding → Edit |
| Email / SMS notification templates | Branding → Email / SMS templates |
| Custom domain (required for branded hosted pages) | Settings → Custom Domains |

---

## PingOne ST — Policies

- Authentication policies are realm-scoped
- Auth trees/journeys define the login flow — see `ping-orchestration` for journey design
- Policy sets apply authorization rules after authentication completes

**Journey-as-policy:** In PingOne ST, the journey itself is the authentication policy. Bind a journey to the realm default or to a specific application to control which flow is used.

**Admin surface:** Realm → Authentication → Trees or Journeys

---

## PingOne ST — Theming

For PingOne ST theming configuration, see `references/curated/pingone-st/themes-and-customization.md`.

## Prerequisites

Admin access to the target platform (PingOne organization admin for MT; AIC tenant admin for ST).

## Common variants

| Variant | Note |
|---|---|
| Workforce vs. CIAM | Workforce MFA policy typically uses TOTP/push; CIAM policies often add risk-based conditions and progressive enrollment |
| Multi-application policies | PingOne MT supports per-application policy override; PingOne ST uses per-journey auth assignment |
| Layered branding | PingOne MT supports global branding overridden per environment; PingOne ST supports realm and journey-level theme override |

## Related references

- `references/curated/cross-platform/foundation-overview.md`
- `references/curated/cross-platform/tenant-and-environment-setup.md`
- `references/curated/cross-platform/core-admin-patterns.md`

## Source

[PingOne sign-on policies](https://docs.pingidentity.com/pingone/latest/platformconsole/p1_c_sign_on_policies.html)
[PingOne branding](https://docs.pingidentity.com/pingone/latest/platformconsole/p1_c_branding.html)
[PingOne ST authentication journeys](https://docs.pingidentity.com/pingoneaic/latest/am-journey-guide/journey-overview.html)
