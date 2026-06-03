---
title: "PingOne ST — Passwordless MFA Device Registration"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: ["mfa"]
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/auth-node-ref/latest/overview.html"
---

# PingOne ST — Passwordless MFA Device Registration

Design patterns for the MFA device registration inner journey, supporting 7 factor types with per-method registration paths. Derived from CIAM Passwordless and Threat Detection journey exports.

## Scope

**Covers:** Device selection, per-method registration inner journeys (WebAuthn, OATH, Push, Combined OATH+PUSH, SMS, VOICE), RecoveryCodeDisplayNode placement, GetAuthenticatorAppNode usage, Twilio phone validation.
**Does NOT cover:** MFA authentication after registration — see `journey-use-cases/mfa-authentication-multi-method.md`.

---

## Structure Overview

Device registration is always a **dedicated inner journey** called from the registration or sign-on journey:

```
InnerTreeEvaluatorNode (tree: MFA Device Registration)
  → true → proceed (device registered)
  → false → FailureNode
```

The device registration inner journey delegates each method to its own nested inner journey via `InnerTreeEvaluatorNode`. This keeps registration paths independently updatable.

---

## Device Selection

**Entry:** A `PageNode` presents the device selection screen. The selection drives an embedded `ScriptedDecisionNode` or `ChoiceCollector` that returns the chosen method as its outcome.

**Observed outcomes:** `Error` / `FIDO2` / `OATH` / `OATH+PUSH` / `PUSH` / `SMS` / `VOICE`

Each outcome routes to a per-method registration inner journey.

---

## Per-Method Registration Paths

### FIDO2 / WebAuthn

```
InnerTreeEvaluatorNode (tree: Register WebAuthn Method)
  → true → EmailTemplateNode ("Notify User On Email") → SuccessNode
  → false → FailureNode
```

**Register WebAuthn Method inner journey:**
```
WebAuthnRegistrationNode (userVerificationRequirement: PREFERRED, asScript: true,
                           generateRecoveryCodes: true, maxSavedDevices: 0,
                           acceptedSigningAlgorithms: [ES256, RS256], timeout: 60)
  → success → RecoveryCodeDisplayNode → SuccessNode
  → unsupported → FailureNode
  → failure → FailureNode
  → error → FailureNode
```

**`unsupported`, `failure`, and `error` all route to FailureNode** — no method fallback in the registration path. The device selection PageNode handles method fallback upstream.

### OATH (TOTP)

```
InnerTreeEvaluatorNode (tree: Register OATH MFA)
```

**Register OATH MFA inner journey:**
```
GetAuthenticatorAppNode
  → outcome → OathRegistrationNode (algorithm: TOTP, passwordLength: SIX_DIGITS,
                                     totpTimeInterval: 30, generateRecoveryCodes: true,
                                     accountName: USERNAME, issuer: ForgeRock)
  → OathDeviceStorageNode
  → PageNode ("Collect Verification Code")
      children: ScriptedDecisionNode (UI validator) + OathTokenVerifierNode
      → successOutcome → RecoveryCodeDisplayNode → SuccessNode
      → failureOutcome → RetryLimitDecisionNode → retry / Reject → FailureNode
```

**`GetAuthenticatorAppNode`** displays ForgeRock Authenticator download links before showing the QR code, ensuring the user has an app capable of scanning it.

**Verification at registration:** After displaying the QR code, the user must enter a valid TOTP code to confirm the device was enrolled correctly. This prevents registration of misconfigured devices.

### Push

```
InnerTreeEvaluatorNode (tree: Register Push MFA)
```

**Register Push MFA inner journey:**
```
PushAuthenticationSenderNode (pushType: DEFAULT, mandatory: true, messageTimeout: 120000)
  → NOT_REGISTERED → GetAuthenticatorAppNode
                   → OathRegistrationNode (registers push device)
                   → PushRegistrationNode
                       → successOutcome → RecoveryCodeDisplayNode → SuccessNode
                       → failureOutcome → FailureNode
                       → timeoutOutcome → RetryLimitDecisionNode → retry / Reject → FailureNode
  → SENT → PushWaitNode → DONE → PushResultVerifierNode
        → TRUE → SuccessNode (already registered, flow completes)
```

### Combined OATH + Push

```
InnerTreeEvaluatorNode (tree: Register OATH & PUSH)
```

**Register OATH & PUSH inner journey:**
```
PushAuthenticationSenderNode
  → NOT_REGISTERED → GetAuthenticatorAppNode
                   → CombinedMultiFactorRegistrationNode (algorithm: TOTP,
                       passwordLength: SIX_DIGITS, generateRecoveryCodes: true)
                       → successOutcome → RecoveryCodeDisplayNode → SuccessNode
                       → failureOutcome → FailureNode
                       → timeoutOutcome → RetryLimitDecisionNode → retry / Reject → FailureNode
  → SENT → PushWaitNode → DONE → PushResultVerifierNode → TRUE → SuccessNode
```

`CombinedMultiFactorRegistrationNode` registers both TOTP and Push simultaneously in a single QR scan.

### SMS / VOICE (Twilio Verify)

```
AttributePresentDecisionNode (presentAttribute: telephoneNumber)
  → True → VerifyAuthLookupNode (phone number format/carrier validation)
      → True → VerifyAuthSenderNode (channel: SMS or CALL)
          → true → PageNode ("Collect OTP")
                children: VerifyAuthCollectorDecisionNode
                → true → PatchObjectNode ("Update User") → SuccessNode
                → false → RetryLimitDecisionNode → retry / Reject → FailureNode
          → error → FailureNode
      → False / Error → FailureNode
  → False → FailureNode (no phone number on file)
```

**`VerifyAuthLookupNode`** validates the phone number before sending — catches invalid numbers before incurring Twilio delivery cost.

**`PatchObjectNode`** at the end of SMS/VOICE registration updates the user's profile with device enrollment metadata.

---

## RecoveryCodeDisplayNode Placement

**Rule:** `RecoveryCodeDisplayNode` must appear immediately after the registration node's `successOutcome`, before any other routing step. If the user exits before seeing the codes, they permanently lose access to them.

```
[Registration node] → successOutcome → RecoveryCodeDisplayNode → SuccessNode
```

This applies to: WebAuthn, OATH, Push, and Combined OATH+PUSH registrations.

---

## EmailTemplateNode Post-Registration Notification

After successful device registration, a non-blocking notification email is sent:

```
SuccessNode path
  → EmailTemplateNode ("Notify User On Email", emailTemplateName: ...)
      → EMAIL_SENT → SuccessNode
      → EMAIL_NOT_SENT → SuccessNode  ← notification is best-effort; does not block
```

Both `EMAIL_SENT` and `EMAIL_NOT_SENT` route to SuccessNode — notification failure does not block registration completion.

---

## Prerequisites

- User must be authenticated before device registration
- ForgeRock Authenticator app available to the user (links provided by `GetAuthenticatorAppNode`)
- Twilio Verify credentials configured for SMS/VOICE methods
- `telephoneNumber` attribute populated in the user's profile for SMS/VOICE enrollment
- HTTPS required for WebAuthn

## Common variants

| Variant | Note |
|---|---|
| Mandatory registration at first login | Place `MFA Device Registration` ITE after `CreateObjectNode(CREATED)` in registration journey |
| Optional registration | Wrap registration ITE with a `ChoiceCollector` offering "Register now" / "Skip" |
| Limit to one method | Remove method outcomes from device selection PageNode |
| Require verification code confirmation for OATH | Already in the OOTB pattern — `OathTokenVerifierNode` in the registration inner journey |

## Related references

- `journey-use-cases/mfa-authentication-multi-method.md`
- `nodes/mfa-nodes.md`
- `nodes/federation-contextual-nodes.md`

## Source

[Authentication nodes — PingOne AIC](https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html)
