# AIC Passkey and Passwordless Journeys

Building passkey (FIDO2/WebAuthn) and passwordless journeys in AIC journeys. For product-neutral design guidance (vocabulary, friction tiers, pattern trade-offs, recovery assurance matching), use portfolio-level passkey design guidance; this reference covers the AIC node-level implementation.

## Scope

**Covers:** AIC journey nodes for passkey registration, authentication, and recovery; AIC-specific gotchas and prerequisites.
**Does NOT cover:** WebAuthn protocol internals; SDK-side passkey wiring in native apps — see `aic-config/webauthn-mobile-setup.md` for the AIC-side prerequisites those apps require; DaVinci connector implementations.

---

## AIC journey nodes

| Node | Purpose |
|---|---|
| `WebAuthnRegistrationNode` | Run WebAuthn `create()` ceremony; persists credential to user object |
| `WebAuthnAuthenticationNode` | Run WebAuthn `get()` ceremony; verifies assertion |
| `WebAuthnDeviceStorageNode` | Persist device metadata (display name, last-used, AAGUID) for user-facing device list |
| `RecoveryCodeDisplayNode` | Generate and display N recovery codes at enrollment |
| `RecoveryCodeCollectorDecisionNode` | Validate a recovery code at sign-in |

Detail on each node (config fields, outcomes, gotchas): `nodes/mfa-nodes.md`.

---

## Patterns with AIC implementation

### Pattern A — Inline at sign-up

- `WebAuthnRegistrationNode` — `relyingPartyName`, `userVerification: required` for higher assurance, `attachmentType: cross-platform | platform | unspecified`
- Pair with a magic-link or password fallback per the chosen friction tier

### Pattern B — Deferred at next login

- Track a `passkeyEnrolled` attribute on the managed user object
- Gate sensitive actions on enrollment after a soft deadline (e.g. via `ScriptedDecisionNode` + attribute-present decision)

### Pattern C — Opportunistic upgrade

- Detect WebAuthn-capable device, inline prompt, `WebAuthnRegistrationNode`
- Do not re-prompt for N days after decline (e.g. LoginCount AT-based decision)

### Pattern 1 — Passkey-first with auto-fill

- Discoverable credentials at registration (`residentKey: required` or `preferred`)
- Modern-browser detection with a non-conditional fallback button

### Pattern 2 — Username-then-passkey

- Branch on device-enrollment state before choosing passkey or password/OTP path

### Pattern 4 — Passkey + step-up for sensitive actions

- `RiskAdvisorNode` (PingOne Protect) → `WebAuthnAuthenticationNode` with `userVerification: required`

---

## AIC-specific gotchas

| Gotcha | Symptom | Fix |
|---|---|---|
| Passkey enrolled in wrong realm | Passkey created in `bravo` realm but user signs into `alpha` | Each realm has its own RP ID; do not cross-realm enroll passkeys |
| Discoverable credential not requested at registration | Conditional UI shows no passkeys for the user | Set `residentKey: required` or `preferred` at registration-node config |
| Recovery-code display skipped | If the user exits before seeing the codes, they permanently lose access to them | Wire `RecoveryCodeDisplayNode` so the user cannot exit before codes are shown |

---

## Prerequisites

- Identity store user objects support a `webauthnDeviceProfile` attribute
- Application's redirect URI domain matches the WebAuthn `rpId` configured for the relying party
- AM services: WebAuthn Profile Encryption / Metadata services, Device Profiles Service, and (for recovery codes) Device Binding Service configured
- **For native Android/iOS apps:** Android asset links, Apple app site association, and CORS must be configured before mobile WebAuthn will work — see `aic-config/webauthn-mobile-setup.md`

---

## Common variants

| Variant | Note |
|---|---|
| Workforce + device-bound | Force `attachmentType: platform` at registration; reject roaming authenticators |
| Consumer + opt-in passkey | Deferred enrollment; allow password fallback indefinitely |
| Hybrid passkey + OTP | Username-first with passkey OR OTP branching |
| Cross-realm | One realm per brand or workforce/CIAM split; do NOT share passkeys between realms |

---

## Source

- [Authentication nodes — PingOne AIC](https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html)
- [PingAM authentication node reference](https://docs.pingidentity.com/auth-node-ref/latest/overview.html)
