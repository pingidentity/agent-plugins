---
title: "PingOne MFA — Region and Service Model"
product_family: cross-platform
products:
  - pingone
capabilities:
  - universal-services
  - mfa
services:
  - mfa
audience:
  - admin
  - architect
use_cases:
  - customer
  - workforce
  - cross-platform
doc_type: reference
status: current
canonical: true
last_updated: "2026-06-08"
slug: "https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_pid_what_is_the_difference.md"
---

# PingOne MFA — Region and Service Model

Before configuring MFA for a Workforce environment, two decisions must be made in order:

1. **Environment type** — Customer or Workforce?
2. **Service model for the region** — PingOne MFA (native) or PingOne MFA for Workforce (hybrid, via PingID service)?

These are separate decisions with a strict dependency: the service model is only relevant for Workforce environments, and it depends on the admin's PingOne region.

## Scope

**Covers:** How to identify environment type (Customer vs Workforce), how to determine the correct MFA service model based on PingOne region, the available authentication methods per environment type and region, and routing to `mfa-configuration.md` for policy setup.

**Does NOT cover:** MFA policy fields, device management, AMR codes, or pairing keys — see `references/curated/mfa-configuration.md`. MFA node wiring in flows or journeys — see `ping-orchestration`.

---

## Step 1 — Identify environment type

| Environment type | Used for | MFA admin surface |
|---|---|---|
| **Customer** | External consumers / CIAM | PingOne MFA service in PingOne admin console |
| **Workforce** | Employees and contractors | Depends on region — see Step 2 |

If the prompt does not specify Customer or Workforce, ask before proceeding. The available authentication methods and admin surfaces differ between the two.

---

## Step 2 — Identify the region (Workforce only)

For **Workforce** environments, the MFA service model varies by PingOne region. Ask the admin which region their environment is in, or have them check their admin console URL (the domain suffix identifies the region):

| Region | Console domain suffix | Service model |
|---|---|---|
| Singapore | `.pingone.sg` | **PingOne MFA (native)** — no PingID service required |
| All other regions | `.pingone.com`, `.pingone.eu`, `.pingone.asia` | **PingOne MFA for Workforce (hybrid)** — uses PingID service |

> **Note on region expansion:** Singapore is currently the only native V2 region. Canada is planned to join in Q3 2026. Additional regions will follow. Maintain the list in this file as new native regions are confirmed — do not hardcode geography assumptions in the skill description.

### Native regions (PingOne MFA, no PingID service)

Currently: **Singapore** (`apps.pingone.sg`)

In these regions, the admin selects PingOne MFA directly. The legacy PingID admin portal is not used. Available integrations are currently limited (see note below).

### Hybrid regions (PingOne MFA for Workforce, via PingID service)

Currently: **all regions except Singapore**

In these regions, Workforce environments use the PingID service. Some configuration remains in the legacy PingID admin portal during the ongoing transition into the PingOne console. The full range of PingID integrations is available: Windows login, Mac login, RADIUS Gateway, SSH.

> **Transition note:** The PingID service is being renamed to "PingOne MFA for Workforce" (hybrid). The term "PingID" is being retired as a service name and will remain only for PingID mobile and desktop authentication apps and PingID device trust. Until this transition is complete, admins in hybrid regions will still see "PingID" in the console.

---

## Step 3 — Select authentication methods

Methods available depend on environment type and service model:

| Method | Customer | Workforce (native SG) | Workforce (hybrid) |
|---|---|---|---|
| Email OTP | ✓ | ✓ | ✓ |
| SMS OTP | ✓ | ✓ | ✓ |
| TOTP (authenticator apps) | ✓ | ✓ | ✓ |
| WebAuthn / passkeys | ✓ | ✓ | ✓ |
| PingID mobile app push | — | ✓ | ✓ (PingID service) |
| PingID desktop app | — | — | ✓ (PingID service) |
| YubiKey OTP | — | — | ✓ (PingID service) |
| Windows / Mac login | — | — | ✓ (PingID service) |
| RADIUS Gateway (VPN) | — | ✓ | ✓ |

> **Native region note:** Availability of some PingID integrations (Windows/Mac login, desktop app, YubiKey OTP) varies by region and is expanding over time. Check `docs.pingidentity.com/pingone/strong_authentication_mfa/` for the methods available in the target region before designing around them.

---

## Routing from here

After establishing environment type, region, and required methods:

| Next task | Reference |
|---|---|
| Configure MFA policy (device enrollment, policy thresholds, AMR codes) | `references/curated/mfa-configuration.md` |
| Wire MFA into a DaVinci flow or AIC journey | `ping-orchestration` → `references/curated/pingone-st/nodes/mfa-nodes.md` or `references/curated/pingone-mt/davinci-registration-and-mfa.md` |
| PingID service administration (hybrid regions) | PingID admin portal — `https://admin.pingid.com` |

---

## Source

- PingOne MFA vs PingID — differences overview: https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_pid_what_is_the_difference.md
- PingOne strong authentication start: https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_strong_authentication_start.html
