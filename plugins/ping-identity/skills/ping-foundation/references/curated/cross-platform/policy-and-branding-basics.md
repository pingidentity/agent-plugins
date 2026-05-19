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
last_updated: ""
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

- Themes are realm-scoped; one theme can serve as the realm default, others can override per journey
- Customize: logo, colors, fonts, layout (card or full-page), custom CSS

**Admin surface:** Realm → Theming → Themes → + New Theme

**Assignment levels:**

| Level | Effect |
|---|---|
| Realm default | All journeys in the realm use this theme unless overridden |
| Journey override | Overrides realm default for all pages shown during that journey |

## Related references

- `foundation-overview.md`
- `tenant-and-environment-setup.md`
- `core-admin-patterns.md`
