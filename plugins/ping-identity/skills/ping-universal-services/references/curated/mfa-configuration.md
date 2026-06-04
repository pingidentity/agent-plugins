---
title: "PingOne MFA — Configuration and Device Management"
product_family: cross-platform
products:
  - pingone
  - pingone-aic
capabilities:
  - universal-services
  - mfa
services:
  - mfa
audience:
  - admin
  - developer
  - architect
use_cases:
  - customer
  - workforce
  - cross-platform
doc_type: reference
status: current
canonical: true
last_updated: "2026-06-04"
slug: "https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_strong_authentication_start.html"
---

# PingOne MFA — Configuration and Device Management

PingOne MFA is the shared MFA service for PingOne MT and AIC. This anchor covers service-level configuration — MFA policies, device management, the enrollment API, and authentication method reference. For MFA node/connector wiring within a flow or journey, see `ping-orchestration`.

## Scope

**Covers:** License prerequisite, environment type differences, MFA policy configuration, supported authentication methods (AMR codes), device management, pairing keys for push MFA, self-service via MyAccount, per-user bypass, headless MFA endpoint, and routing split between service config and flow design.

**Does NOT cover:** MFA node/connector wiring in DaVinci flows or AIC journeys — see `ping-orchestration` and `references/curated/pingone-st/nodes/mfa-nodes.md`. SDK integration code — see `ping-app-integration/references/curated/mobile-integration-basics.md`.

---

## Prerequisites — License check

PingOne MFA requires `PING_ONE_MFA` in the environment's **Bill of Materials (BOM)**.

```
GET /pingone/platform/v1/environments/{envId}/billOfMaterials
```

If `PING_ONE_MFA` is absent, the service cannot be configured and administrator intervention is required to confirm license eligibility. Check the BOM before building any MFA configuration.

---

## Workforce vs Customer environments

PingOne MFA has distinct configuration surfaces depending on environment type:

| Environment type | MFA admin surface | Typical use |
|---|---|---|
| **Workforce** | Workforce-specific MFA policy + PingID policy | Employee MFA, device binding, PingID mobile |
| **Customer** | Standard MFA policy | CIAM registration, step-up flows, email/SMS OTP |

Both types use the same underlying API but expose different policy options in the admin console. Configure PingID-specific features (Offline MFA, Windows login passwordless) only for Workforce environments.

---

## MFA policy configuration

MFA policies in PingOne are called **Device Authentication Policies** in the API (the admin console labels them "MFA Policies"). Each policy defines which authentication methods are allowed and their settings.

**Admin surface:** PingOne admin console → Authentication → MFA → Device Authentication Policies

**Policy scope:** Per-environment. A policy is then referenced by sign-on policies or DaVinci/AIC flow connectors.

**Key policy fields:**

| Field | Purpose |
|---|---|
| Policy name | Identifier referenced by sign-on policies and flow connectors |
| Enabled methods | Which of the supported methods are permitted for this policy |
| Default method | Method pre-selected for users with multiple devices enrolled |
| FIDO2 settings | Allowed authenticator types, UV requirement, RP ID |
| Email/SMS settings | OTP validity window, resend delay, max attempts |
| Push settings | Approval timeout, auto-approve for low-risk, biometric binding |

---

## Supported authentication methods (AMR codes)

| AMR code | Method | Notes |
|---|---|---|
| `EMAIL` | OTP via email | Standard delivery; no native app required |
| `SMS` | OTP via SMS | Carrier-dependent delivery; vulnerable to SIM swap |
| `TEL` | OTP via phone call | Voice delivery; fallback for SMS failures |
| `OTP` | TOTP via authenticator app or mobile OTP | Google Authenticator, Authy, PingID TOTP |
| `MCA` | Mobile push (interactive or silent) | Requires PingOne MFA native app + pairing key |
| `USER` | Interactive push with user presence test | Subset of MCA; user must actively approve |
| `SWK` | Software-secured key / trusted device | Device-bound credential via PingOne MFA SDK |

**`USER` vs `MCA` distinction:** `USER` requires an active approval tap (user presence test); `MCA` includes both interactive and silent push modes. Use `USER` when explicit human confirmation is required for high-risk actions.

Custom AMR strings (`face`, `pin`, `ftp`) can be passed via the PingOne MFA SDK's `approve()` method on Android for biometric-gated approvals — see `ping-app-integration/references/curated/mobile-integration-basics.md`.

---

## Device management

### Pairing keys (push MFA prerequisite)

Push notification MFA (`MCA`, `USER`) requires a native device + application linked to the user via a **pairing key**. This is the binding step that associates the mobile app installation with the PingOne user record.

**Flow:**
1. Generate a pairing key via the PingOne MFA API for the target user
2. User enters or scans the pairing key in the PingOne MFA mobile app
3. Device is registered and appears in the user's device list
4. Push notifications are now deliverable to that device

**API endpoint:** `POST /environments/{envId}/users/{userId}/mfaUserAuthClientPairingKeys`

Without a pairing key, push MFA cannot be initiated — the flow will fall through to a fallback method.

### Headless / non-authorize MFA endpoint

For MFA initiated outside of the PingOne authorize service (headless flows, custom apps, IVR):

```
POST /environments/{envId}/deviceAuthentications
```

This endpoint initiates and completes MFA without requiring an OAuth/OIDC authorization code flow. Supports device type selection and OTP validation. Used in: IVR step-up, AI agent HITL (CIBA alternative), backend-triggered MFA challenges.

### Per-user MFA management

| Operation | Where |
|---|---|
| Enable/disable MFA for a user | API: `PUT /environments/{envId}/users/{userId}/mfaEnabled`; or admin console |
| View enrolled devices | Admin console → Users → (user) → MFA Devices; or API |
| Remove a device | Admin console or `DELETE /environments/{envId}/users/{userId}/devices/{deviceId}` |
| Bypass MFA for a user | Admin console → Users → (user) → Bypass MFA toggle |
| User self-service device management | MyAccount portal (`/myaccount`) — requires self-service to be enabled |

---

## PingID-specific configuration (Workforce only)

PingID is the enterprise MFA application for Workforce environments. It has a separate policy surface from standard PingOne MFA policies.

| PingID capability | Notes |
|---|---|
| PingID policy | Separate from Device Authentication Policy; controls PingID-specific behaviour |
| Offline MFA | Windows login app with offline authentication; configured separately |
| Passwordless Windows login | PingID app-based Windows login; requires Windows login app deployment |

For PingID admin tasks beyond initial configuration, refer to the PingID Administration Guide.

---

## Routing split — MFA config vs MFA in flows

This is the most common routing confusion for MFA tasks:

| Task | Correct skill |
|---|---|
| Configure MFA policy (Device Authentication Policy), method settings, PingID policy | `ping-universal-services` (this skill) |
| Manage MFA devices, pairing keys, enrollment API, per-user bypass | `ping-universal-services` (this skill) |
| Wire an MFA step into a DaVinci flow (PingOne MFA connector) | `ping-orchestration` |
| Wire an MFA node into an AIC journey (WebAuthn, OATH, Push nodes) | `ping-orchestration` |
| Embed the PingOne MFA SDK in a mobile app | `ping-app-integration` |
| Understand MFA method disambiguation (Verify vs MFA) | `references/curated/choosing-the-right-service.md` |

---

## Common gotchas

| Gotcha | Impact | Fix |
|---|---|---|
| `PING_ONE_MFA` not in BOM | Service unavailable; API returns 403 | Verify BOM before configuring; contact admin if missing |
| Pairing key missing for push MFA | Push silently falls back to OTP or fails | Always check `mfaEnabled` and device list before initiating push |
| Device Authentication Policy not assigned | MFA not enforced despite policy existing | Assign policy to the sign-on policy's MFA action (MT) or reference it in the flow connector (DaVinci) |
| Bypass MFA toggle left on | User permanently skips MFA | Audit bypass toggles; remove after troubleshooting |
| `USER` AMR required but `MCA` returned | Compliance check fails for explicit approval flows | Specify `USER` in the policy; confirm app version supports interactive push |
| Workforce vs Customer policy mismatch | PingID features unavailable in Customer environment | Configure PingID policies only in Workforce environments |

---

## Prerequisites

- `PING_ONE_MFA` present in environment BOM
- Environment Admin or MFA Admin role
- For push MFA: users must have the PingOne MFA mobile app installed and a pairing key generated
- For PingID: Workforce environment; PingID license active

## Common variants

| Variant | Note |
|---|---|
| Workforce MFA | Typically PingID + TOTP; Offline MFA and Windows login available |
| CIAM MFA | Email OTP + SMS OTP + FIDO2; enrollment during registration journey |
| Step-up MFA | Triggered mid-session by risk score or resource sensitivity; always configure a fallback method |
| Headless MFA | `/deviceAuthentications` endpoint; no browser redirect required |
| MFA SDK integration | Pairing key + PingOne MFA SDK; custom AMR strings via `approve()` |

## Related references

- `references/curated/choosing-the-right-service.md` — MFA vs Verify disambiguation
- `references/curated/service-invocation-patterns.md` — invoking MFA from DaVinci or AIC
- `plugins/ping-identity/skills/ping-orchestration/references/curated/pingone-st/nodes/mfa-nodes.md` — AIC MFA journey nodes
- `plugins/ping-identity/skills/ping-orchestration/references/curated/pingone-mt/davinci-registration-and-mfa.md` — DaVinci MFA flow patterns
- `plugins/ping-identity/skills/ping-app-integration/references/curated/mobile-integration-basics.md` — PingOne MFA SDK, pairing keys, push integration

## Source

- [PingOne MFA getting started](https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_strong_authentication_start.html)
- [PingOne MFA API reference](https://developer.pingidentity.com/pingone-api/mfa/introduction.html)
