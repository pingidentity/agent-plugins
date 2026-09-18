# Passkeys and Passwordless Design

Design-level patterns for passkey (FIDO2 / WebAuthn) and passwordless experiences, applicable across Ping orchestration platforms. Platform-specific node, connector, and authentication-policy detail lives in each product's documentation and product skills; this page is the what/why.

## Scope

**Covers:** Terminology, assurance-vs-friction tiers, registration and authentication pattern trade-offs, and recovery assurance matching.
**Does NOT cover:** WebAuthn protocol internals (see the W3C WebAuthn specification); SDK-side passkey wiring in applications (see client-side app integration documentation); node and connector configuration.

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
| **Balanced** | Passkey OR password+OTP, user choice | Step-up to MFA on sensitive action | Multi-channel (email + SMS); admin reset | Most consumer identity apps; mixed-risk apps |
| **Higher assurance** | Passkey (device-bound preferred) | Mandatory step-up for any privileged action | Admin-mediated; identity proofing re-run on full reset | Workforce; financial; healthcare; regulated industries |

**Friction tier choice drives:**
- Whether discoverable credentials (resident keys) are required at registration
- Whether device-bound (non-syncable) authenticators are mandatory
- Whether step-up is policy-driven (risk score) or always-on
- What recovery pathways are exposed in the experience

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

### Pattern B — Deferred at next login (balanced + higher-assurance)

```
Initial sign-up → Account created with password (still required)
  → Authenticated session
  → Banner / interstitial: "Set up a passkey for faster sign-in"
      Accept → WebAuthn create ceremony → record passkey, optionally disable password fallback per policy
      Decline / Skip → Continue with password; re-prompt on Nth subsequent login
```

**Trade-off:** Lower drop-off at registration; opt-in adoption. Risk: many users never enroll without an incentive.

**Tip:** Track enrollment state as a user attribute; gate sensitive actions on enrollment after a soft deadline.

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

**Trade-off:** No client-side cryptography required; works on any device. Risk: phishing-resistant ONLY if the link is bound to the device that initiated the request.

**Caution:** Not phishing-resistant in the strict FIDO2 sense. Acceptable for the low-friction tier; not for higher assurance.

### Pattern 4 — Passkey + step-up for sensitive actions

```
User signs in with passkey (low friction)
  → Performs sensitive action (transfer, role change, profile update)
  → Step-up evaluation
      Risk LOW → Allow without re-auth
      Risk MEDIUM/HIGH → Re-run WebAuthn assertion OR push notification
```

---

## Recovery and fallback

A passkey may be unavailable when the user changes phones, loses access to the credential manager, or the device is lost. Every passkey-based flow MUST expose at least one recovery path.

| Recovery method | Assurance |
|---|---|
| Email OTP | Low |
| SMS OTP | Low (vulnerable to SIM swap) |
| Recovery codes (printed at enrollment) | Medium |
| Identity proofing | High |
| Admin-mediated reset | Highest |

**Rule:** Match the recovery method's assurance to the friction tier. Higher-assurance tiers should NOT expose SMS OTP as the only recovery — it weakens the security posture below what passkeys provide.

---

## Design gotchas

| Gotcha | Why it matters |
|---|---|
| `userVerification` mismatch | Registration and authentication must agree on verification strictness; a mismatch is rejected at the relying party |
| AAGUID allowlist too strict | Users with synced cross-platform passkeys are rejected; decide whether policy requires device-bound credentials |
| Discoverable credential not requested at registration | Conditional (auto-fill) UI cannot offer passkeys at sign-in |
| Magic link reused across devices | Phishable: email forwarding can leak the link; bind or single-use with short TTL |
| Cross-realm / cross-RP-ID enrollment | Each relying party (and realm) has its own RP ID; a passkey enrolled under one does not assert for another |
| Redirect URI domain must match the WebAuthn RP ID | Application origins that don't match the RP ID fail WebAuthn ceremonies for native and web clients |

---

## Common variants

| Variant | Note |
|---|---|
| Workforce + device-bound | Require platform-attached authenticators; reject roaming authenticators |
| Consumer + opt-in passkey | Deferred enrollment; allow password fallback indefinitely |
| Hybrid passkey + OTP | Username-first with passkey OR OTP branching |
| Cross-realm | One realm per brand or workforce/consumer split; do NOT share passkeys between realms |
| Migration from password | Opportunistic upgrade; do not force-disable passwords until adoption is high |

---

## Source

- [W3C WebAuthn specification](https://www.w3.org/TR/webauthn/)
- [Advanced Identity Cloud journeys documentation](https://docs.pingidentity.com/pingoneaic/home.md)
- [PingOne DaVinci documentation](https://docs.pingidentity.com/davinci/davinci_introduction.md)
- [PingFederate documentation](https://docs.pingidentity.com/pingfederate/latest/index.md)
