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
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/pingoneaic/ui-customization-guide/ui-theming.html"
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

---

## Email notification templates

Email templates are separate from visual themes but affect the end-user branding experience.

| Template category | Admin surface |
|---|---|
| Registration / welcome | Realm → Notifications → Email → Registration |
| Password reset | Realm → Notifications → Email → Password Reset |
| MFA enrollment | Realm → Notifications → Email → MFA Enrollment |
| Custom journey notifications | Realm → Notifications → Email → + New Template |

Template editor supports HTML with Freemarker expressions for dynamic values (e.g., `${user.givenName}`, `${resetLink}`). Test templates using the preview function before saving.

CSP note: images embedded in email templates must be hosted on an externally accessible URL — PingOne ST does not host email images; reference them via absolute URL in the template HTML.

---

## Common gotchas

| Gotcha | Symptom | Fix |
|---|---|---|
| Theme change not visible to end users | Hosted page still shows old branding | Theme must be set as default in the realm, or assigned explicitly to the journey or app |
| Custom font blocked by CSP | Font request fails; fallback font renders instead | Add the font CDN origin to Security → Content Security Policy → `font-src` directive |
| Social button CSS override does not reorder buttons | Social buttons appear in unexpected position despite CSS | Social button position is controlled by the Social Provider Handler node position in the journey; CSS controls visual style only |
| Account pages not themed | End-user account page shows default Ping branding | Account page theming is managed under Realm → Theming → Account Theme — different from the main Login theme |
| Dark mode not applying | Custom CSS `prefers-color-scheme` media query ignored | CSP or class name changes between product versions may break CSS selectors; re-inspect rendered DOM after each product update |
| Error pages partially themed | System error pages (500-level) still show Ping default theme | PingAM system error pages are not fully themeable; customize error messages via AM admin console → Realm → General Settings → Error Page |

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
- `references/curated/pingone-st/am-services.md` — CORS Service governs which origins can load themed hosted pages from custom UIs

## Source

[UI theming — PingOne ST](https://docs.pingidentity.com/pingoneaic/ui-customization-guide/ui-theming.html)
[UI customization overview](https://docs.pingidentity.com/pingoneaic/ui-customization-guide/ui-overview.html)
[Getting started: apply basic branding](https://docs.pingidentity.com/pingoneaic/getting_started/getting_started-apply_branding.html)
