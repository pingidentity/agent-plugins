---
title: "Passkeys and Passwordless Authentication"
product_family: cross-platform
products: ["pingone", "pingone-aic", "davinci", "pingam"]
capabilities: ["orchestration", "mfa", "passwordless"]
services: ["mfa"]
audience: ["developer", "architect", "admin"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-03"
slug: "https://docs.pingidentity.com/pingone/authentication/p1_passkeys_overview.html"
---

# Passkeys and Passwordless Authentication

Design patterns for passkey (FIDO2 / WebAuthn) and passwordless flows across PingOne (DaVinci), AIC journeys, and the Ping Software Suite. Covers registration, authentication, recovery, fallback, and the three friction tiers (low / balanced / higher-assurance).

## Scope

**Covers:**
- Passkey vs passwordless terminology and the WebAuthn ceremonies
- Registration patterns (inline at sign-up, deferred at next login, opportunistic upgrade)
- Authentication patterns (passkey-first, magic link, OTP-only, push-only)
- Friction tier matrix: low / balanced / higher-assurance
- Recovery and fallback when the passkey is unavailable
- Platform-specific node and connector references for AIC, DaVinci, and PingFederate

**Does NOT cover:**
- WebAuthn protocol internals — see external W3C WebAuthn spec
- SDK-side passkey wiring — see `ping-app-integration`
- Risk-based step-up logic — see `references/curated/pingone-st/journey-use-cases/financial-services-step-up.md` (AIC) or DaVinci registration anchor
- Hardware key (YubiKey) procurement / lifecycle

---

## Vocabulary

| Term | Meaning |
|---|---|
| **WebAuthn** | W3C standard for browser-mediated cryptographic authentication |
| **FIDO2** | Authentication framework that includes WebAuthn + CTAP2; used interchangeably with WebAuthn for passkey discussions |
| **Passkey** | A FIDO2 credential, typically synced across the user's devices via the platform credential manager (Apple iCloud Keychain, Google Password Manager, 1Password) |
| **Device-bound credential** | FIDO2 credential that does not sync — tied to the device's secure enclave |
| **Discoverable credential** | A passkey the authenticator can list without the relying party providing a hint; enables "username-less" sign-in |
| **Resident key** | Older WebAuthn term for discoverable credential |
| **Passwordless** | Authentication without a knowledge factor (no password). Can use passkeys, magic links, OTP, or push |

> **Rule:** "Passkey" implies WebAuthn / FIDO2. "Passwordless" is broader — it includes magic links and OTP-only flows that are not WebAuthn-based.

---

## Friction tiers

Use this matrix to match the assurance the user actually needs to the friction they will tolerate:

| Tier | Primary factor | Step-up | Recovery | Best for |
|---|---|---|---|---|
| **Low friction** | Passkey (auto-fill, conditional UI) or magic link | None unless risk elevates | Email OTP, SMS OTP | Consumer apps; high abandonment risk; no high-value actions |
| **Balanced** | Passkey OR password+OTP, user choice | Step-up to MFA on sensitive action | Multi-channel (email + SMS); admin reset | Most CIAM apps; mixed-risk consumer apps |
| **Higher assurance** | Passkey (device-bound preferred) | Mandatory step-up for any privileged action | Admin-mediated; identity proofing (PingOne Verify) re-run on full reset | Workforce; financial; healthcare; regulated industries |

**Friction tier choice drives:**
- Whether discoverable credentials (resident keys) are required at registration
- Whether device-bound (non-syncable) authenticators are mandatory
- Whether step-up is policy-driven (Protect risk score) or always-on
- What recovery pathways are exposed in the journey

---

## Registration patterns

### Pattern A — Inline at sign-up (low + balanced tiers)

```
Registration form (collect username, email)
  → Account created (no password requested)
  → Passkey enrollment ceremony (WebAuthn create)
      Success → Account active; user lands on app
      Cancel / Failed → Magic-link fallback OR password fallback (per tier)
```

**Trade-off:** Highest conversion-friendly path; user sees one flow. Risk: user closes the tab before completing the WebAuthn ceremony — leaves a partially provisioned account.

**Implementation:**
- AIC: `WebAuthnRegistrationNode` — `relyingPartyName`, `userVerification: required` for higher assurance, `attachmentType: cross-platform | platform | unspecified`
- DaVinci: PingOne MFA connector → `Initiate Passkey Registration` capability; pair with HTML Form for fallback
- PingFederate: PingID adapter → FIDO2 / WebAuthn enrollment via PingID Mobile or browser

### Pattern B — Deferred at next login (balanced + higher-assurance)

```
Initial sign-up → Account created with password (still required)
  → Authenticated session
  → Banner / interstitial: "Set up a passkey for faster sign-in"
      Accept → WebAuthn create ceremony → record passkey, optionally disable password fallback per policy
      Decline / Skip → Continue with password; re-prompt on Nth subsequent login
```

**Trade-off:** Lower drop-off at registration; opt-in adoption. Risk: many users never enroll without an incentive.

**Tip:** Track `passkeyEnrolled` attribute on the user object; gate sensitive actions on enrollment after a soft deadline.

### Pattern C — Opportunistic upgrade (balanced)

```
Existing user logs in with password + OTP
  → Detect WebAuthn-capable browser/device
  → Inline prompt: "Add this device as a passkey"
      Accept → WebAuthn create → next login uses passkey
      Decline → Continue with password; do not re-prompt for N days
```

**Use when:** rolling out passkeys to an existing user base; minimizes disruption.

---

## Authentication patterns

### Pattern 1 — Passkey-first with auto-fill (best UX)

```
Sign-in page renders WebAuthn conditional UI
  → User taps username field; browser surfaces enrolled passkeys
  → Single tap completes WebAuthn assertion
  → Token issued
```

**Required:** Discoverable credentials at registration; modern browser (Safari 16+, Chrome 108+, Firefox 119+). For older browsers or fallback: explicit "Sign in with passkey" button that triggers the same ceremony non-conditionally.

### Pattern 2 — Username-then-passkey

```
User enters username
  → Server checks if passkey enrolled
      Enrolled → WebAuthn assertion ceremony
      Not enrolled → Password / OTP / magic link
```

**Use when:** mixed user base; some users have passkeys, some don't.

### Pattern 3 — Magic link (passwordless without WebAuthn)

```
User enters email
  → System sends single-use signed link
  → User clicks link in email client
  → Token issued
```

**Trade-off:** No client-side cryptography required; works on any device. Risk: phishing-resistant ONLY if the link is bound to the device that initiated the request (use `loginHint` + browser fingerprint to soft-bind).

**Caution:** Not phishing-resistant in the strict FIDO2 sense. Acceptable for low-friction tier; not for higher assurance.

### Pattern 4 — Passkey + step-up for sensitive actions

```
User signs in with passkey (low friction)
  → Performs sensitive action (transfer, role change, profile update)
  → Step-up evaluation
      Risk LOW → Allow without re-auth
      Risk MEDIUM/HIGH → Re-run WebAuthn assertion (UV: required) OR push notification
```

**Implementation:**
- AIC: `RiskAdvisorNode` (PingOne Protect) → `WebAuthnAuthenticationNode` with `userVerification: required`
- DaVinci: `PingOne Protect Evaluate` node → if MEDIUM/HIGH, branch to `PingOne MFA — Authenticate (Passkey)` capability

---

## Recovery and fallback

A passkey may be unavailable when the user changes phones, loses access to the credential manager, or the device is lost. Every passkey-based flow MUST expose at least one recovery path.

| Recovery method | Assurance | Skill / node |
|---|---|---|
| Email OTP | Low | AIC `OTPCollectorDecisionNode`, DaVinci `PingOne Notifications → Send OTP` |
| SMS OTP | Low (vulnerable to SIM swap) | Same as email; configure SMS provider |
| Recovery codes (printed at enrollment) | Medium | AIC `RecoveryCodeDisplayNode` + `RecoveryCodeCollectorDecisionNode`; DaVinci subflow |
| Identity proofing (PingOne Verify) | High | `ping-universal-services` → `verify-configuration.md`; invoke from journey/flow |
| Admin-mediated reset | Highest | Out-of-band admin action; notification to user + audit trail |

**Rule:** Match the recovery method's assurance to the friction tier. Higher-assurance tiers should NOT expose SMS OTP as the only recovery — it weakens the security posture below what passkeys provide.

---

## Platform-specific implementation reference

### AIC — Journey nodes

| Node | Purpose |
|---|---|
| `WebAuthnRegistrationNode` | Run WebAuthn `create()` ceremony; persists credential to user object |
| `WebAuthnAuthenticationNode` | Run WebAuthn `get()` ceremony; verifies assertion |
| `WebAuthnDeviceStorageNode` | Persist device metadata (display name, last-used, AAGUID) for user-facing device list |
| `RecoveryCodeDisplayNode` | Generate and display N recovery codes at enrollment |
| `RecoveryCodeCollectorDecisionNode` | Validate a recovery code at sign-in |

Reference: `references/curated/pingone-st/nodes/mfa-nodes.md`

### PingOne (DaVinci) — Connector capabilities

| Connector | Capability | Purpose |
|---|---|---|
| PingOne MFA | Initiate Passkey Registration | WebAuthn `create()` from DaVinci-hosted page |
| PingOne MFA | Authenticate Passkey | WebAuthn `get()` from DaVinci-hosted page |
| PingOne | Update User | Set `passkeyEnrolled: true` after successful registration |
| PingOne Notifications | Send OTP | Email OTP fallback / recovery |

Reference: `references/curated/pingone-mt/davinci-registration-and-mfa.md`

### Ping Software Suite — PingFederate

| Component | Role |
|---|---|
| PingID adapter | FIDO2 / WebAuthn via PingID; configure under PingFederate authentication policies |
| Composite adapter | Chain HTML Form + PingID (with FIDO2) for password+passkey transitional flows |

Reference: `plugins/ping-identity/skills/ping-foundation/references/curated/ping-software/pingfederate-basics.md`

---

## Common gotchas

| Gotcha | Symptom | Fix |
|---|---|---|
| `userVerification` mismatch | WebAuthn ceremony succeeds but assertion is rejected at the relying party | Match `userVerification` between registration and authentication; `required` at one end and `discouraged` at the other will fail |
| AAGUID allowlist too strict | Users with cross-platform passkeys (iCloud, Google) are rejected | Decide whether your relying party policy requires device-bound; if not, allow any AAGUID |
| Discoverable credential not requested at registration | Conditional UI shows no passkeys for the user | Set `residentKey: required` or `preferred` at `WebAuthnRegistrationNode` config |
| Browser compatibility — older Safari | Conditional UI fails silently; explicit button works | Detect support with `navigator.credentials.conditionalGet?.()` and fall back to explicit button |
| Email OTP exposed as only recovery for higher-assurance tier | Users in regulated industry can be reset via SMS-recoverable email | Require identity proofing (PingOne Verify) re-run for higher-assurance recovery |
| Magic link reused across devices | Phishable: email forwarding can leak the link | Bind link to client fingerprint or limit to single-use within short TTL |
| Passkey enrolled in wrong realm | AIC: passkey created in `bravo` realm but user signs into `alpha` | Each realm has its own RP ID; do not cross-realm enroll passkeys |

---

## Prerequisites

- Identity store user objects support a `webauthnDeviceProfile` attribute (AIC) or equivalent (the PingOne user object includes this by default)
- Application's redirect URI domain matches the WebAuthn `rpId` configured for the relying party
- For higher-assurance tiers: PingOne Verify or another identity-proofing service licensed and configured (see `ping-universal-services`)
- For DaVinci flows: PingOne MFA service activated in the environment
- **For native Android/iOS apps (AIC):** Android asset links, Apple app site association, and CORS must be configured before mobile WebAuthn will work — see `references/curated/pingone-st/journey-use-cases/webauthn-mobile-setup.md`

---

## Common variants

| Variant | Note |
|---|---|
| Workforce + device-bound | Force `attachmentType: platform` at registration; reject roaming authenticators |
| CIAM + opt-in passkey | Pattern B (deferred enrollment); allow password fallback indefinitely |
| Hybrid passkey + OTP | Pattern 2 (username-first) with passkey OR OTP branching |
| Cross-realm | One realm per brand or workforce/CIAM split; do NOT share passkeys between realms |
| Migration from password | Pattern C (opportunistic upgrade); do not force-disable passwords until adoption is high |

---

## Routing back to other skills

| If the task is also... | Skill |
|---|---|
| Configuring the platform-level MFA policy or sign-on policy | `ping-foundation` |
| Wiring the passkey registration UI into a mobile or web app | `ping-app-integration` |
| Risk-based step-up using PingOne Protect signals | `ping-universal-services` (Protect) |
| Identity proofing as part of higher-assurance recovery | `ping-universal-services` (Verify) |

---

## Related references

- `references/curated/pingone-st/nodes/mfa-nodes.md` — WebAuthn node details
- `references/curated/pingone-st/journey-use-cases/passwordless-mfa-registration.md` — passwordless registration journey
- `references/curated/pingone-st/journey-use-cases/mfa-authentication-multi-method.md` — MFA authentication patterns
- `references/curated/pingone-mt/davinci-registration-and-mfa.md` — DaVinci registration + MFA flows
- `plugins/ping-identity/skills/ping-foundation/references/curated/cross-platform/policy-and-branding-basics.md` — MFA policy configuration

## Source

- [PingOne (multi-tenant cloud) — Passkeys overview](https://docs.pingidentity.com/pingone/authentication/p1_passkeys_overview.html)
- [AIC — WebAuthn node reference](https://docs.pingidentity.com/auth-node-ref/latest/auth-node-webauthn-authentication.html)
- [DaVinci — PingOne MFA connector](https://docs.pingidentity.com/davinci/connectors/davinci_pingone_mfa_connector.html)
- [W3C WebAuthn Level 3](https://www.w3.org/TR/webauthn-3/)
- [Passkeys.dev — RP guidance](https://passkeys.dev/docs/use-cases/)
