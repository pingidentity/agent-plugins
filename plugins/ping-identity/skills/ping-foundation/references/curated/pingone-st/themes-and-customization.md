---
title: "PingOne ST — Themes and Customization"
product_family: pingone-st
products: ["pingone-aic"]
capabilities: ["foundation"]
services: []
audience: ["admin", "developer"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-05-19"
slug: "https://docs.pingidentity.com/pingoneaic/latest/ui-customization-guide/ui-theming.html"
---

# PingOne ST — Themes and Customization

Apply branding to PingOne ST hosted pages using the Theme Editor and custom CSS.

## Scope

**Covers:** Theme creation, visual configuration, custom CSS, theme assignment to realms and journeys, hosted page coverage.
**Does NOT cover:** Email template customization — configured separately under Notifications. Custom journey UI nodes — that is a `ping-orchestration` scripting task.

---

## Theming model

Themes are applied in layers:

```
Tenant
└── Realm (realm-level default theme)
    └── Journey (journey-level override)
        └── Hosted pages served to end users
```

A single tenant can serve distinct branding to different user populations by assigning different themes to different realms or journeys.

**Admin surface:** AIC admin console → Realm → Theming → Themes → + New Theme

---

## Theme configuration fields

| Field | Notes |
|---|---|
| Logo | Appears on login, enrollment, and account pages |
| Favicon | Browser tab icon |
| Colors | Primary, secondary, link, background — hex values |
| Font | Web-safe fonts or custom font family; CDN fonts require CSP update |
| Layout | Card layout (centered, default) or full-page |

---

## Custom CSS

**Access:** Theme Editor → Custom CSS tab

Custom CSS class names are subject to change with product updates; validate against the current rendered output before deploying overrides.

**CSP constraint:** PingOne ST hosted pages enforce a Content Security Policy. External fonts or assets loaded from custom CSS require the origin to be added to the CSP configuration.

**CSP admin surface:** AIC admin console → Security → Content Security Policy

**Social button positioning:** social login buttons appear above username/password fields by default. CSS controls visual stacking only — the actual flow order is controlled by Social Provider Handler node placement in the journey.

---

## Theme assignment

| Level | Effect | Admin surface |
|---|---|---|
| Realm default | All journeys in the realm use this theme unless overridden | Realm → Theming → Set Default Theme |
| Journey override | All pages shown during that journey use this theme | Journey editor → (journey settings) → Theme |

---

## Hosted pages covered by themes

| Page type | Themed |
|---|---|
| Login / sign-on | Yes |
| Registration | Yes |
| Password reset | Yes |
| MFA enrollment | Yes |
| Account (end-user self-service) | Yes |
| Consent | Yes |
| Error pages | Partial — system errors may not be fully themed |

---

## Localization

- Hosted page strings are driven by the browser's `Accept-Language` header
- Custom locale files can be added for supported languages
- Admin console and hosted pages support localization independently

---

## Prerequisites

- PingOne ST tenant with at least one realm
- Admin access to Theming
- If using CDN fonts: CSP must allow the font origin before the theme is applied

## Common variants

| Variant | Note |
|---|---|
| Multi-brand | One theme per brand; assign each to the appropriate realm or journey |
| Workforce vs. CIAM | Use realm-level themes to separate internal and external page branding |
| Dark mode | Not natively supported; achievable via custom CSS overriding color variables |
| Account pages | End-user account management at `/am/XUI/` is also themed but configured separately under Account pages |

## Related references

- `references/curated/pingone-st/foundation-overview.md`
- `references/curated/pingone-st/authentication-fundamentals.md`
- `references/curated/pingone-st/app-setup.md`

## Source

[UI theming — PingOne ST](https://docs.pingidentity.com/pingoneaic/latest/ui-customization-guide/ui-theming.html)
[UI customization overview](https://docs.pingidentity.com/pingoneaic/latest/ui-customization-guide/ui-overview.html)
[Getting started: apply basic branding](https://docs.pingidentity.com/pingoneaic/latest/getting_started/getting_started-apply_branding.html)
