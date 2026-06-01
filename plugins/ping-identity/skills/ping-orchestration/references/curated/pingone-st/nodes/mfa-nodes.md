---
title: "PingOne ST — MFA Nodes"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: ["mfa"]
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: reference
status: current
canonical: true
last_updated: "2026-05-21"
slug: "https://docs.pingidentity.com/auth-node-ref/latest/overview.html"
---

# PingOne ST — MFA Nodes

Nodes for registering and verifying second factors: WebAuthn/passkeys, OATH/TOTP, push, OTP, and recovery codes.

## Scope

**Covers:** All built-in MFA node types, their configuration, outcomes, and composition patterns — including production-observed settings from live journey exports.
**Does NOT cover:** Risk-based MFA step-up routing — see `nodes/risk-management-nodes.md`. PingOne Verify (identity proofing) — see `ping-universal-services`.

---

## WebAuthn / Passkeys

### WebAuthn Registration node
Registers a FIDO2/WebAuthn authenticator (passkey, security key, platform authenticator) for a user.

**Production configuration:**

| Field | Observed value | Notes |
|---|---|---|
| `userVerificationRequirement` | `PREFERRED` | Allows devices without UV but prefers it |
| `authenticatorAttachment` | `UNSPECIFIED` | Platform or cross-platform authenticators accepted |
| `generateRecoveryCodes` | `true` | Always enable; recovery codes displayed immediately after |
| `maxSavedDevices` | `0` | Unlimited registered devices per user |
| `attestationPreference` | `NONE` | No attestation statement required |
| `acceptedSigningAlgorithms` | `[ES256, RS256]` | Covers most device types |
| `timeout` | `60` | Seconds before registration attempt expires |
| `asScript` | `true` | Required for hosted pages; injects WebAuthn as a script |

- Outcomes: **success** / **unsupported** / **failure** / **error**
- On `success`: route immediately to `RecoveryCodeDisplayNode` before proceeding
- On `unsupported`, `failure`, `error`: route to FailureNode or back to device selection
- Requires HTTPS. Configure Relying Party Identifier (defaults to tenant domain).

### WebAuthn Authentication node
Authenticates a user with a previously registered FIDO2 device.

**Production configuration:**

| Field | Observed value | Notes |
|---|---|---|
| `userVerificationRequirement` | `PREFERRED` | |
| `isRecoveryCodeAllowed` | `true` | Exposes `recoveryCode` outcome |
| `timeout` | `60` | |
| `detectSignCountMismatch` | `false` | Set `true` in high-security deployments to detect cloned authenticators |
| `asScript` | `true` | |

- Outcomes: **success** / **unsupported** / **noDevice** / **failure** / **error** / **recoveryCode**
- Route `noDevice` to device registration inner journey, not directly to Failure
- Route `recoveryCode` to a dedicated PageNode embedding `RecoveryCodeCollectorDecisionNode` (type: `WEB_AUTHN`)
- Route `No Device Registered` / `noDevice` to the same failure handling as `failure` to prevent username enumeration

### WebAuthn Device Storage node
Persists the registered WebAuthn device credential to the user's profile.

- Place after WebAuthn Registration `success` outcome, before RecoveryCodeDisplayNode.

---

## OATH / TOTP

### OATH Registration node
Registers a TOTP/HOTP authenticator app by generating and displaying a QR code shared secret.

**Production configuration:**

| Field | Observed value | Notes |
|---|---|---|
| `algorithm` | `TOTP` | Standard time-based OTP |
| `passwordLength` | `SIX_DIGITS` | |
| `totpTimeInterval` | `30` | Standard 30-second window |
| `addChecksum` | `false` | |
| `generateRecoveryCodes` | `true` | Always enable |
| `minSharedSecretLength` | `32` | |
| `accountName` | `USERNAME` | Displayed in the authenticator app |
| `issuer` | `ForgeRock` or tenant name | Displayed in the authenticator app |
| `bgColor` | `032b75` | QR code background color |

- Outcomes: single (on success; display OATH device QR code)
- Always preceded by `GetAuthenticatorAppNode` when the user may not have an authenticator app installed
- On `successOutcome`: route to `RecoveryCodeDisplayNode`

### Get Authenticator App node
Displays download links for the ForgeRock Authenticator (Play Store + App Store) before OATH or Push registration. Used when `OathTokenVerifierNode` or `PushAuthenticationSenderNode` returns `notRegisteredOutcome` / `NOT_REGISTERED`.

- Outcomes: single (user has acknowledged; proceed to registration)
- ForgeRock Authenticator URLs: Play Store `com.forgerock.authenticator`, App Store ID `1038442926`

### OATH Token Verifier node
Verifies the OTP entered by the user against the registered OATH device.

**Production configuration:**

| Field | Observed value | Notes |
|---|---|---|
| `algorithm` | `TOTP` | |
| `totpTimeInterval` | `30` | |
| `totpHashAlgorithm` | `HMAC_SHA1` | |
| `totpTimeSteps` | `2` | Clock drift allowance: ±1 window |
| `maximumAllowedClockDrift` | `5` | Minutes |
| `hotpWindowSize` | `100` | For HOTP counter drift |
| `isRecoveryCodeAllowed` | `true` | Exposes `recoveryCodeOutcome` |

- Outcomes: **successOutcome** / **failureOutcome** / **notRegisteredOutcome** / **recoveryCodeOutcome**
- `notRegisteredOutcome`: route to `GetAuthenticatorAppNode` → OATH Registration
- `recoveryCodeOutcome`: route to dedicated recovery code PageNode
- Must be embedded as a PageNode child, alongside a `ScriptedDecisionNode` ("Validate Verification Code") for client-side input validation
- On `failureOutcome`: route to `RetryLimitDecisionNode` (see retry-loop-with-lockout pattern below)

### OATH Device Storage node
Persists the OATH device to the user's profile. Place after OATH Registration before proceeding.

### HOTP Generator node
Generates an HMAC-based OTP for delivery via a side channel (email script, SMS).

- `length: 6` — stores OTP in transient state as `oneTimePassword`
- Outcomes: single
- Used in email-delivered OTP flows where `OTPEmailSenderNode` is not used (e.g., when delivery is handled by a custom `ScriptedDecisionNode` calling IDM `openidm.action()`)

---

## Push Authentication

### Push Registration node
Registers the user's mobile device for push-based authentication.

- Outcomes: **successOutcome** / **failureOutcome** / **timeoutOutcome**
- On `successOutcome`: route to `RecoveryCodeDisplayNode`
- Always preceded by `GetAuthenticatorAppNode` when device may not be enrolled

### Push Sender node
Sends a push notification to the user's registered device.

**Production configuration:**

| Field | Observed value | Notes |
|---|---|---|
| `pushType` | `DEFAULT` | |
| `mandatory` | `true` | Requires a response |
| `messageTimeout` | `120000` | Milliseconds (2 minutes) |
| `captureFailure` | `false` | |
| `contextInfo` | `false` | |

- Outcomes: **SENT** / **NOT_REGISTERED**
- `NOT_REGISTERED`: route to `GetAuthenticatorAppNode` → Push Registration

### Push Wait node
Polls for the result of a sent push notification.

- `secondsToWait: 5`
- Outcomes: **DONE** (polling complete; proceed to `PushResultVerifierNode`) / **EXITED** (user chose to enter a code instead)
- `EXITED`: route to an OTP/OATH verification PageNode as a fallback when the user dismisses the push wait screen

### Push Result Verifier node
Verifies the final push authentication result.

- Outcomes: **TRUE** (approved) / **FALSE** (denied) / **WAITING** (not yet responded) / **EXPIRED** (timed out)
- `WAITING`: loop back through `PushWaitNode` → `DONE` → return to PushResultVerifierNode
- `EXPIRED`: route to `RetryLimitDecisionNode` → `Retry` → re-send push; `Reject` → FailureNode
- `FALSE` (denied): route directly to FailureNode

---

## OTP via Email / SMS

### OTP Email Sender node
Generates a one-time password and sends it to the user's registered email address.

- Outcomes: single (OTP stored in transient state)

### OTP SMS Sender node (`OneTimePasswordSmsSenderNode`)
Generates and sends an OTP to the user's phone via SMS.

- Outcomes: single
- Used in phone-based MFA device registration (phone-number verification before enrollment)

### OTP Collector Decision node
Collects and validates the OTP entered by the user.

- `passwordExpiryTime: 5` (minutes)
- Outcomes: **True** (OTP valid) / **False** (OTP invalid or expired)
- On `False`: route to `RetryLimitDecisionNode` (see retry-loop-with-lockout pattern)

> **PageNode required:** `OTP Collector Decision` must always be a PageNode child. A standalone instance renders no input field. Always embed it in a PageNode with a `ScriptedDecisionNode` for input validation (see `nodes/utility-nodes.md` → PageNode Rule 3).

---

## Recovery Codes

### Recovery Code Display node
Generates and displays recovery codes to the user immediately after MFA enrollment. Codes are stored in the user's profile.

- Outcomes: single
- **Always place immediately after the MFA registration node's success outcome** — before any other step. If the user exits without seeing the codes, they lose access to them.

### Recovery Code Collector Decision node
Prompts for and validates a recovery code as an alternative to the primary MFA factor.

- `recoveryCodeType`: set to the MFA method — `OATH` / `WEB_AUTHN` / `PUSH`
- Outcomes: **True** (code valid) / **False** (code invalid)
- Must be a PageNode child alongside a `ScriptedDecisionNode` ("Validate Recovery Code") for client-side input validation

---

## Recovery Code Architecture

The following pattern appears consistently across all production MFA journeys:

```
Registration:
  [MFA Registration node] (generateRecoveryCodes: true)
    → successOutcome → RecoveryCodeDisplayNode → proceed

Authentication:
  [MFA Verifier node] (isRecoveryCodeAllowed: true)
    → recoveryCodeOutcome → PageNode(RecoveryCodeCollectorDecisionNode, ScriptedDecisionNode)
      → True → Success
      → False → RetryLimitDecisionNode
```

Each `RecoveryCodeCollectorDecisionNode` must be typed to the MFA method via `recoveryCodeType`. Mixing types (e.g., using an OATH-typed collector with a WebAuthn authentication flow) causes validation failures.

---

## Combined Registration

### Combined MFA Registration node
Registers both OATH (TOTP) and Push simultaneously in a single step.

**Production configuration:** `algorithm: TOTP`, `passwordLength: SIX_DIGITS`, `totpTimeInterval: 30`, `generateRecoveryCodes: true`

- Outcomes: **successOutcome** / **failureOutcome** / **timeoutOutcome**
- `timeoutOutcome`: route to `RetryLimitDecisionNode` for retry
- On `successOutcome`: route to `RecoveryCodeDisplayNode`
- Use when the device selection PageNode offers an `OATH+PUSH` combined option

### MFA Registration Options node
Allows users to select which MFA factors to register.

### Enable Device Management node
Enables device management capabilities for subsequent device binding nodes.

---

## Device Binding

### Device Binding node
Binds the current device to the authenticated user using a device-specific key.

- Outcomes: **Success** / **Failure** / **Unsupported**

### Device Binding Storage node
Persists device binding data to the user's profile.

### Device Signing Verifier node
Verifies a device signature created by a previously bound device.

- Outcomes: **Success** / **Failure** / **No Device Bound**

---

## Retry-Loop-With-Lockout Pattern

Every MFA input path in production journeys uses a consistent retry loop:

```
[Input PageNode]
  → failure outcome
  → RetryLimitDecisionNode (retryLimit: 3, incrementUserAttributeOnFailure: true)
    → Retry → ScriptedDecisionNode ("Set Invalid Code Error Message")
             → [Input PageNode] (reads invalidCodeErrorMessage from shared state via callbacksBuilder.textOutputCallback)
    → Reject → FailureNode
```

The `ScriptedDecisionNode` sets `invalidCodeErrorMessage` in shared state. The PageNode script reads it and displays the error inline on the next render without an extra round-trip. This pattern applies to OATH, OTP, recovery code, and Push-expired retry flows.

---

## Common patterns

| Pattern | Nodes |
|---|---|
| WebAuthn login | WebAuthn Authentication → (noDevice) → WebAuthn Registration |
| TOTP registration | GetAuthenticatorAppNode → OATH Registration → OATH Device Storage → Recovery Code Display |
| TOTP authentication | PageNode(OathTokenVerifierNode + ScriptedDecisionNode) → (successOutcome) Success |
| OTP email step-up | OTP Email Sender → PageNode(OTP Collector Decision) → (True) Success |
| Push authentication | Push Sender → (SENT) Push Wait → (DONE) Push Result Verifier → (TRUE) Success |
| Push with EXITED fallback | Push Wait(EXITED) → PageNode(OathTokenVerifierNode) → retry loop |
| Combined MFA enrollment | Combined MFA Registration → Recovery Code Display → Success |
| Recovery code fallback (OATH) | OathTokenVerifierNode(recoveryCodeOutcome) → PageNode(RecoveryCodeCollectorDecisionNode[OATH]) → (True) Success |

## Prerequisites

- FIDO2/WebAuthn registration and authentication require HTTPS and a configured Relying Party.
- OATH/TOTP requires the ForgeRock Authenticator or a compatible TOTP app on the user's device.
- Push authentication requires the ForgeRock Authenticator app and a configured push service (APNs/FCM).
- Twilio SMS/voice OTP requires a Twilio account SID, auth token, and Verify service SID.

## Common variants

- **FIDO2 enterprise deployment:** set `userVerificationRequirement: REQUIRED` and `authenticatorAttachment: CROSS_PLATFORM` for security key policies.
- **SMS-only fallback:** use `OTPSMSSenderNode` + `OTPCollectorDecisionNode` when device-based MFA is not available.

## Related references

- `nodes/basic-auth-nodes.md`
- `nodes/risk-management-nodes.md`
- `nodes/utility-nodes.md`
- `journey-use-cases/mfa-authentication-multi-method.md`
- `journey-use-cases/passwordless-mfa-registration.md`

## Source

[MFA nodes overview](https://docs.pingidentity.com/auth-node-ref/latest/overview.html)
[WebAuthn Authentication node](https://docs.pingidentity.com/auth-node-ref/latest/webauthn-authentication.html)
[OATH nodes](https://docs.pingidentity.com/auth-node-ref/latest/oath-registration.html)
