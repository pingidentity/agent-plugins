---
title: "PingOne MT — Themes, Branding, and Notifications"
product_family: pingone-mt
products: ["pingone", "davinci"]
capabilities: ["foundation", "branding"]
services: []
audience: ["admin", "developer"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-03"
slug: "https://docs.pingidentity.com/pingone/branding/p1_branding.html"
---

# PingOne MT — Themes, Branding, and Notifications

UI customization for PingOne MT hosted pages and DaVinci-hosted flow pages: branding assets, custom domains, notification templates, and DaVinci UI Studio.

## Scope

**Covers:** PingOne hosted-page branding (logo, colors, custom domain, error pages); email and SMS notification templates and senders; DaVinci UI Studio for flow pages; CSP/font constraints; multi-environment branding strategy.

**Does NOT cover:** PingOne ST theming — see `references/curated/pingone-st/themes-and-customization.md`. DaVinci flow logic — see `ping-orchestration`. End-app UI customization — see `ping-app-integration`.

---

## Branding scope — what you can theme in PingOne MT

| Surface | Themed via | Notes |
|---|---|---|
| PingOne hosted sign-on / consent pages | Branding admin (Settings → Branding) | Logo, colors, favicon, footer text |
| PingOne self-service app | Same Branding admin | Inherits the environment's branding |
| Email notification templates | Email Templates admin | HTML editor with merge variables; per-environment |
| SMS notification templates | SMS Templates admin | Plain text with merge variables |
| DaVinci-hosted flow pages | DaVinci UI Studio | Per-flow or per-tenant DaVinci theme; separate from PingOne branding |
| End-app login UI (rendered in your app) | Your application code via Ping SDK | Not branded by Ping; use SDK collectors |

**Critical:** PingOne hosted-page branding and DaVinci-hosted page branding are **separate systems**. A flow that redirects from PingOne to DaVinci will show two different branded surfaces unless both are configured to match.

---

## PingOne branding configuration

**Admin surface:** PingOne admin console → Settings → Branding

| Field | Notes |
|---|---|
| Logo | PNG or SVG; max 2 MB; appears in headers of all hosted pages |
| Brand colors | Primary, secondary, link, button — hex values applied via CSS variables |
| Favicon | PNG or ICO; appears in browser tabs |
| Footer text | Optional; supports basic HTML for legal/privacy links |
| Background image | Optional; full-page background on consent and confirmation pages |
| Font | Web-safe stack only; custom CDN fonts require CSP update (see below) |

**Per-environment:** Each PingOne environment has its own branding. Set Dev / Staging / Production environments separately. Trial and Sandbox environments default to Ping branding until customized.

---

## Custom domains

Required for branded hosted pages — without a custom domain, hosted pages render at `auth.pingone.com` (Ping's neutral domain).

**Admin surface:** Settings → Custom Domains → Add Custom Domain

| Step | Notes |
|---|---|
| Add domain | e.g., `id.example.com` |
| DNS verification | Add the CNAME record provided by PingOne; verify before proceeding |
| TLS certificate | PingOne automatically provisions a certificate via Let's Encrypt or accepts a customer-provided certificate |
| Domain activation | After verification + cert issuance, hosted pages render at the custom domain |

**Constraint:** When you switch to a custom domain, **all redirect URIs registered against existing applications must be updated** to use the new hostname. The change is not automatic.

---

## Email notification templates

**Admin surface:** Settings → Email Templates

PingOne sends transactional emails for: account creation, password reset, MFA OTP, identity verification, account locked, and custom journey notifications.

| Field | Notes |
|---|---|
| Subject line | Supports merge variables (e.g., `${user.username}`) |
| Body (HTML) | Full HTML editor; embedded images must be hosted at an externally accessible URL |
| Plain-text fallback | Required for deliverability; auto-generated from HTML if blank |
| Locale | Multiple template variants per locale; PingOne selects based on `Accept-Language` |

**Merge variables:**

| Variable | Source |
|---|---|
| `${user.username}` | User identity store |
| `${user.name.given}` | User profile |
| `${user.email}` | User profile |
| `${otp}` | Generated for OTP/verification templates |
| `${recoveryCode}` | Generated for password reset |
| `${magicLink}` | Generated for magic link sign-in flows |
| `${environment.name}` | PingOne environment metadata |

---

## Email senders

**Admin surface:** Settings → Notifications → Senders

| Sender option | Notes |
|---|---|
| PingOne default | `noreply@pingidentity.com` — works out of box; no domain verification |
| Verified custom domain | Required for branded sender (e.g., `noreply@id.example.com`); requires SPF + DKIM + DMARC records |
| Third-party SMTP | Configure outbound relay through SendGrid, Mailgun, etc. — use for high-volume environments |

**Production recommendation:** Always verify a custom sender domain before go-live. Unverified senders use Ping's neutral domain; users see "noreply@pingidentity.com" instead of your brand.

---

## SMS notification templates

**Admin surface:** Settings → SMS Templates

| Field | Notes |
|---|---|
| Body (plain text) | Limited to 160 characters per segment; longer messages are split |
| Merge variables | Same set as email templates |
| Locale | Multiple variants supported |

**SMS sender configuration:** Settings → Notifications → SMS Provider — Twilio is the default; alternative providers configurable per environment.

---

## DaVinci UI Studio

DaVinci flows that use HTML Template nodes render at DaVinci-hosted URLs. UI Studio is the visual editor for these page templates.

**Admin surface:** DaVinci console → UI Studio

| Capability | Notes |
|---|---|
| Per-flow themes | Each flow can use a different theme; useful for multi-brand tenants |
| Tenant-default theme | Falls back to this theme when a flow does not specify one |
| Custom HTML/CSS | Full HTML editor; images can be uploaded to DaVinci asset storage or referenced externally |
| Form components | Pre-built component library (input, button, link, error message, etc.) |
| Variable binding | Bind component fields to DaVinci flow variables |

**Important:** UI Studio themes apply to **DaVinci-hosted pages only**. They do NOT affect PingOne-hosted pages (which use PingOne branding). Both systems must be configured if a flow redirects between them.

---

## Custom CSS / fonts and CSP

PingOne hosted pages enforce a Content Security Policy.

| Asset type | Where to allow |
|---|---|
| External fonts (Google Fonts, custom CDN) | Settings → Domains and Branding → Content Security Policy → `font-src` |
| External images (in email templates) | No CSP restriction (email is rendered by the recipient's mail client) |
| External CSS overrides | Not supported — PingOne does not allow custom CSS injection on hosted pages; use brand colors and logos instead |
| Inline styles in DaVinci HTML Template | Allowed; DaVinci pages have a separate CSP managed in DaVinci settings |

**Hard limit:** PingOne hosted pages do NOT support customer-supplied CSS. If you need pixel-level control, host the page in your own application using the Ping SDK (see `ping-app-integration`).

---

## Branding strategy patterns

### Pattern A — Single brand, all environments
- One custom domain, one logo, one color set
- Apply identical branding to Dev, Staging, Production environments
- Best for: workforce identity; single-product CIAM

### Pattern B — Per-environment differentiation
- Distinct logo or color treatment for Dev (e.g., yellow border) vs Production
- Helps prevent operator confusion (don't accidentally make changes in Production)
- Same custom domain pattern: `id-dev.example.com`, `id.example.com`

### Pattern C — Multi-brand single tenant
- Separate PingOne environments per brand
- Each environment has its own custom domain, branding, email templates
- Each application is registered in the brand's environment
- Best for: parent companies with distinct consumer brands; B2B2C platforms

### Pattern D — Co-existing PingOne + DaVinci surfaces
- Configure PingOne branding to match
- Configure DaVinci UI Studio theme to use the same logo/colors/fonts
- Verify visual continuity by walking the user-facing flow end-to-end before go-live

---

## Pre-go-live branding checklist

| Item | PingOne MT | DaVinci |
|---|---|---|
| Custom domain configured + DNS verified | Yes — Settings → Custom Domains | N/A (DaVinci uses its own subdomain) |
| TLS certificate active | Yes — auto-provisioned or customer-uploaded | Yes — DaVinci-managed |
| Logo uploaded | Settings → Branding | UI Studio → Theme |
| Brand colors set | Settings → Branding | UI Studio → Theme |
| Favicon uploaded | Settings → Branding | Not applicable for DaVinci hosted pages |
| Email sender verified | Settings → Notifications → Senders | DaVinci uses PingOne Notifications connector — verified at PingOne level |
| Email templates customized | Settings → Email Templates | N/A — DaVinci uses PingOne Notifications connector |
| SMS templates customized | Settings → SMS Templates | Same as email |
| Hosted page branding tested | Walk a sign-on flow through hosted pages | Walk the DaVinci flow end-to-end |
| CSP entries for any custom fonts | Settings → CSP → `font-src` | UI Studio → Theme settings |

---

## Common gotchas

| Gotcha | Symptom | Fix |
|---|---|---|
| Logo shows but colors don't apply | Cached CSS in browser | Hard refresh; CDN cache TTL is 5 minutes globally |
| Custom font fails to load | Falls back to web-safe font | Add font origin to CSP `font-src` |
| Emails arrive from `noreply@pingidentity.com` despite custom sender | Sender domain not verified | Complete SPF + DKIM verification at Settings → Notifications → Senders |
| DaVinci flow looks unbranded after PingOne redirect | DaVinci theme not configured | Set tenant-default theme in DaVinci UI Studio; assign theme to flow |
| Custom domain redirect URI mismatch | Apps fail with `redirect_uri_mismatch` after domain switch | Update each app's redirect URIs to use the new custom domain hostname |
| HTML email template breaks in Outlook | Modern CSS (flexbox, grid) doesn't render | Use table-based layouts and inline CSS for email; test with Litmus or similar |
| Trial environment shows trial badge in branding | Cannot remove via Branding admin | Trial badge is enforced; go to a Production environment for full branding |

---

## Prerequisites

- Environment Admin role on the target PingOne environment
- For custom domains: DNS administrative access to the domain
- For verified senders: DNS administrative access to add SPF, DKIM, DMARC records
- For DaVinci UI Studio: DaVinci admin role; DaVinci service activated on the environment

---

## Common variants

| Variant | Note |
|---|---|
| Workforce default | Use environment branding only; no DaVinci flows |
| CIAM with DaVinci | Configure both PingOne and DaVinci themes; verify visual continuity |
| Multi-brand CIAM | One PingOne environment per brand; separate domains, branding, email senders |
| Hybrid PingOne + on-prem | Customer's web app (or SDK) handles its own branding; PingOne branding only matters for hosted-page redirects |

---

## Related references

- `references/curated/pingone-mt/tenant-and-environment-setup.md` — environment provisioning
- `references/curated/cross-platform/policy-and-branding-basics.md` — branding overview
- `references/curated/pingone-st/themes-and-customization.md` — PingOne ST theming (separate platform)

## Source

- [PingOne branding](https://docs.pingidentity.com/pingone/branding/p1_branding.html)
- [PingOne custom domains](https://docs.pingidentity.com/pingone/custom_domains/p1_custom_domains.html)
- [PingOne email templates](https://docs.pingidentity.com/pingone/notifications/p1_notifications_email_templates.html)
- [PingOne notifications](https://docs.pingidentity.com/pingone/notifications/p1_notifications.html)
- [DaVinci UI Studio](https://docs.pingidentity.com/davinci/davinci_uistudio/davinci_uistudio_overview.html)
