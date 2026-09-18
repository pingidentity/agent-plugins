# DaVinci Passkey and Passwordless Flows

Building passkey (FIDO2/WebAuthn) and passwordless flows in PingOne DaVinci: connector capabilities, flow patterns, and prerequisites. For product-neutral design guidance (vocabulary, friction tiers, pattern trade-offs, recovery assurance matching), use portfolio-level passkey design guidance.

## Scope

**Covers:** DaVinci connector capabilities for passkeys, flow-pattern implementations, and DaVinci-specific prerequisites.
**Does NOT cover:** WebAuthn protocol internals; SDK-side passkey wiring in native apps (see client-side app integration documentation); diagnosing an existing flow execution — use DaVinci execution history and debug logging.

---

## Connector capabilities

| Connector | Capability | Purpose |
|---|---|---|
| PingOne MFA | Initiate Passkey Registration | WebAuthn `create()` from a DaVinci-hosted page |
| PingOne MFA | Authenticate Passkey | WebAuthn `get()` from a DaVinci-hosted page |
| PingOne | Update User | Set `passkeyEnrolled: true` after successful registration |
| PingOne Notifications | Send OTP | Email OTP fallback / recovery |

---

## Patterns with DaVinci implementation

### Pattern A — Inline at sign-up

- PingOne MFA connector → `Initiate Passkey Registration` capability after user creation
- Pair with HTML Form for magic-link or password fallback per the chosen friction tier
- On ceremony failure, route to fallback rather than terminating — the user already has an account

### Pattern B — Deferred at next login

- Track `passkeyEnrolled` on the user object (PingOne `Update User`)
- Gate sensitive actions on enrollment after a soft deadline

### Pattern 1 — Passkey-first with auto-fill

- Discoverable credentials at registration (`residentKey: required` or `preferred`)
- For older browsers, explicit "Sign in with passkey" button triggering the same capability non-conditionally

### Pattern 4 — Passkey + step-up for sensitive actions

- `PingOne Protect Evaluate` node → if MEDIUM/HIGH, branch to `PingOne MFA — Authenticate (Passkey)` capability
- Always report the Protect result back on both success and failure paths

---

## Prerequisites

- PingOne environment with the PingOne MFA service activated
- Application's redirect URI domain matches the WebAuthn `rpId`

---

## Common variants

| Variant | Note |
|---|---|
| Consumer + opt-in passkey | Deferred enrollment (Pattern B); allow password fallback indefinitely |
| Hybrid passkey + OTP | Username-first with passkey OR OTP branching |
| Migration from password | Opportunistic upgrade (Pattern C); do not force-disable passwords until adoption is high |

---

## Source

- [DaVinci connector documentation](https://docs.pingidentity.com/connectors/)
- [Implementing a flow in an application](https://docs.pingidentity.com/davinci/integrating_flows_into_applications/davinci_how_to_implement_a_flow.html)
