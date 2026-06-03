---
title: "PingOne ST — Multi-Method MFA Authentication"
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

# PingOne ST — Multi-Method MFA Authentication

Design patterns for the multi-method MFA authentication inner journey, supporting up to 8 factors with per-method retry loops and recovery code fallbacks. Derived from CIAM Passwordless, Financial Services, and Threat Detection journey exports.

## Scope

**Covers:** Device selection, per-method authentication nodes, retry-loop-with-lockout, recovery code paths per method, inner journey structure.
**Does NOT cover:** MFA device registration — see `journey-use-cases/passwordless-mfa-registration.md`. Risk-based step-up routing — see `journey-use-cases/pingone-protect-risk-integration.md`.

---

## Structure Overview

MFA authentication is always implemented as a **dedicated inner journey** called from the main journey via `InnerTreeEvaluatorNode`. This keeps MFA logic reusable and independently updatable.

**Main journey call:**
```
InnerTreeEvaluatorNode (tree: MFA Authentication)
  → true → proceed (MFA passed)
  → false → FailureNode
```

---

## Device Selection

**Entry pattern:** A `PageNode` presents the device selector. The selection drives outcomes via an embedded `ScriptedDecisionNode` ("Select MFA Device") that reads the user's registered device state from shared state and returns the chosen method as its outcome.

**Observed outcomes:** `EMAIL` / `SMS` / `VOICE` / `FIDO2` / `OATH` / `PUSH` / `Magic Link` / `Error`

Each outcome routes to a per-method authentication sub-path.

---

## Per-Method Authentication Paths

### OATH (TOTP)

```
PageNode ("Enter Verification Code")
  children: ScriptedDecisionNode ("Validate Verification Code Input Script")
          + OathTokenVerifierNode (isRecoveryCodeAllowed: true)
  → successOutcome → SuccessNode
  → failureOutcome → RetryLimitDecisionNode
  → notRegisteredOutcome → GetAuthenticatorAppNode → OATH Registration inner journey
  → recoveryCodeOutcome → PageNode ("Enter Recovery Code") → [recovery code path]
```

**OathTokenVerifierNode config:** `totpTimeInterval: 30`, `totpHashAlgorithm: HMAC_SHA1`, `totpTimeSteps: 2`, `maximumAllowedClockDrift: 5`, `isRecoveryCodeAllowed: true`

### Push

```
PushAuthenticationSenderNode (mandatory: true, messageTimeout: 120000)
  → SENT → PushWaitNode (secondsToWait: 5)
      → DONE → PushResultVerifierNode
          → TRUE → SuccessNode
          → FALSE → FailureNode
          → WAITING → loop back to PushWaitNode
          → EXPIRED → RetryLimitDecisionNode → Retry → re-send push / Reject → FailureNode
      → EXITED → PageNode (OTP fallback for users who dismiss the push)
  → NOT_REGISTERED → GetAuthenticatorAppNode → Push Registration inner journey
```

### WebAuthn (FIDO2)

```
WebAuthnAuthenticationNode (isRecoveryCodeAllowed: true, asScript: true)
  → success → SuccessNode
  → unsupported → FailureNode
  → noDevice → GetAuthenticatorAppNode → WebAuthn Registration inner journey
  → failure → RetryLimitDecisionNode
  → error → FailureNode
  → recoveryCode → PageNode ("Enter Recovery Code") → [recovery code path, WEB_AUTHN typed]
```

### Email OTP

```
OneTimePasswordGeneratorNode (length: 6)
  → ScriptedDecisionNode ("Send OTP Email")   [calls IDM openidm.action() to deliver via email]
  → PageNode ("Collect OTP")
      children: ScriptedDecisionNode (UI validator) + OneTimePasswordCollectorDecisionNode (passwordExpiryTime: 5)
      → true → SuccessNode
      → false → RetryLimitDecisionNode → retry loop / Reject → FailureNode
```

### SMS / VOICE (Twilio Verify)

```
VerifyAuthIdentifierNode (identifierAttribute: telephoneNumber)
  → True → VerifyAuthSenderNode (channel: SMS or CALL)
      → true → PageNode ("Collect OTP")
            children: VerifyAuthCollectorDecisionNode
            → true → SuccessNode
            → false → RetryLimitDecisionNode → retry loop
            → error → FailureNode
  → False / Error → FailureNode
```

### Magic Link (Email Suspend)

```
EmailSuspendNode (emailTemplateName: magicLinkTemplate, objectLookup: true)
  → outcome → SuccessNode
```

The simplest path — journey suspends, user clicks the link in the email, journey resumes at SuccessNode.

---

## Retry-Loop-With-Lockout Pattern

Every code-entry path (OATH, OTP, recovery codes) uses this consistent retry loop:

```
[Failure outcome from verifier]
  → RetryLimitDecisionNode (retryLimit: 3, incrementUserAttributeOnFailure: true)
      → True (Retry) → ScriptedDecisionNode ("Set Invalid Code Error Message")
                     → [Input PageNode]  ← reads invalidCodeErrorMessage from shared state
      → False (Reject) → FailureNode
```

The `ScriptedDecisionNode` writes `invalidCodeErrorMessage` to shared state. The PageNode script reads it via `callbacksBuilder.textOutputCallback(2, invalidCodeErrorMessage)` and renders it inline on the next page load — no extra round-trip.

---

## Recovery Code Paths

Every MFA method that supports recovery codes follows the same recovery sub-path:

```
[MFA verifier node] → recoveryCodeOutcome
  → PageNode ("Enter Recovery Code")
      children: ScriptedDecisionNode ("Validate Recovery Code Input Script")
              + RecoveryCodeCollectorDecisionNode (recoveryCodeType: <method>)
      → True → SuccessNode
      → False → RetryLimitDecisionNode → retry / Reject → FailureNode
```

**`recoveryCodeType` values by method:**

| MFA method | recoveryCodeType |
|---|---|
| OATH / TOTP | `OATH` |
| WebAuthn | `WEB_AUTHN` |
| Push | `PUSH` |

Mismatching `recoveryCodeType` to the authentication method causes validation failures.

---

## Inner Journey Composition

MFA authentication is kept as a separate inner journey. Never embed all MFA paths directly in the main journey graph — the resulting node count makes the journey unmanageable and prevents reuse.

**Recommended structure:**
```
Main journey
  → InnerTreeEvaluatorNode (ThreatDetection)   ← risk evaluation
  → InnerTreeEvaluatorNode (MFADeviceRegistration)  ← register device if not enrolled
  → InnerTreeEvaluatorNode (MFAAuthentication)  ← challenge with registered device
  → SuccessNode
```

The `MFADeviceRegistration` inner journey is only needed in journeys that allow just-in-time registration. If all users must pre-enroll, it can be omitted.

## Prerequisites

- User must have at least one MFA device registered (or device registration inner journey must be in the chain before this one)
- Email notification service configured for Email OTP and Magic Link methods
- Twilio Verify credentials configured for SMS/VOICE methods
- FIDO2 requires HTTPS

## Related references

- `journey-use-cases/passwordless-mfa-registration.md`
- `journey-use-cases/pingone-protect-risk-integration.md`
- `nodes/mfa-nodes.md`
- `nodes/federation-contextual-nodes.md`

## Source

[Authentication nodes — PingOne AIC](https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html)
