---
title: "PingOne Advanced Identity Cloud (AIC) — PingOne Protect Risk Integration"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: ["protect"]
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/auth-node-ref/latest/overview.html"
---

# AIC — PingOne Protect Risk Integration

Design patterns for integrating PingOne Protect risk evaluation into AIC journeys, derived from four production journey suites (CIAM Passwordless, Financial Services, Money Transfer, Threat Detection).

## Scope

**Covers:** Triple-node pattern, init/eval separation via shared state, production configuration, outcome routing, new device detection, account disable on high risk, ModifyAuthLevelNode step-up chain.
**Does NOT cover:** PingOne Protect service setup — see `ping-universal-services`. Transaction authorization — see `journey-use-cases/financial-services-step-up.md`.

---

## Architecture: Inner Journey Wrapping

PingOne Protect is always wrapped in a **dedicated "Threat Detection" inner journey** called from the main journey:

```
Main journey
  → ScriptedDecisionNode ("Is Protect Analysis Required?", outcome: true/false)
  → [true] InnerTreeEvaluatorNode ("Initialize P1 Protect")   ← first call: init
  → [after init] InnerTreeEvaluatorNode ("Protect Evaluation & Mitigation")  ← second call: eval
```

Keeping Protect in an inner journey allows it to be reused across multiple main journeys (sign-on, registration, authorization) and updated independently.

---

## Init/Eval Separation Pattern

A single inner journey handles both initialization and evaluation via a shared state flag (`p1ProtectAction`):

```
Inner journey entry:
ScriptedDecisionNode ("P1 Protect Action?", reads p1ProtectAction from shared state)
  → "init" → product-PingOneProtectInitializeNode
                → true → SuccessNode
                → false → FailureNode
  → "eval" → [evaluation branch — see below]
```

The calling journey sets `p1ProtectAction` to `"init"` before the first call and `"eval"` before the second. This prevents duplicating the inner journey for two slightly different calls.

---

## Evaluation Branch

```
"eval" path:
IdentifyExistingUserNode
  → ScriptedDecisionNode ("Set UserId and Username For Protect")
        [sets protectUserId and protectUsername in shared state]
  → ScriptedDecisionNode ("Determine Flow Type",
        outcomes: Authentication / Authorization / Registration)
  → product-PingOneProtectEvaluationNode (per flow type)
```

**PingOneProtectEvaluationNode production configuration:**

| Field | Value | Notes |
|---|---|---|
| `flowType` | `AUTHENTICATION` / `AUTHORIZATION` / `REGISTRATION` | Set from ScriptedDecisionNode output |
| `pauseBehavioralData` | `true` | |
| `storeEvaluateResult` | `true` | |
| `deviceSharingType` | `SHARED` | |
| `scoreThreshold` | `300` | Numeric threshold for `exceed` outcome |
| `userId` | `protectUserId` | Shared state key |
| `username` | `protectUsername` | Shared state key |
| `userType` | `EXTERNAL` | |
| `recommendedActions` | `[BOT_MITIGATION, AITM_MITIGATION, TEMP_EMAIL_MITIGATION]` | |

---

## Standard Outcome Routing

```
product-PingOneProtectEvaluationNode
  → low → product-PingOneProtectResultNode (SUCCESS) → SuccessNode
  → medium → step-up MFA inner journey → (on MFA success) PingOneProtectResultNode (SUCCESS)
  → high → ModifyAuthLevelNode (increment: 1)
         → AccountActiveDecisionNode
         → AccountLockoutNode (LOCK)
         → EmailTemplateNode ("Send Account Disabled Email")
         → product-PingOneProtectResultNode (FAILED) → FailureNode
  → exceed / failure / clientError / BOT_MITIGATION / AITM_MITIGATION / TEMP_EMAIL_MITIGATION
         → product-PingOneProtectResultNode (FAILED) → FailureNode
```

**Critical:** `product-PingOneProtectResultNode` must be called at **both** success and failure termination paths. Omitting it on one path degrades the Protect risk model over time.

---

## New Device Detection Pattern

Used in Financial Services and Money Transfer to send notifications without blocking the journey:

```
product-PingOneProtectEvaluationNode
  → [after low/medium routing]
  → ScriptedDecisionNode ("Extract Protect Activity Params",
        outcomes: highRisk / newDevice / low_medRisk)
  → newDevice: ScriptedDecisionNode ("Notify New Device Detected",
        outcomes: sent / noMail / error)
        → all outcomes → SuccessNode  ← notification is best-effort
  → highRisk: ScriptedDecisionNode ("Send Suspicious Activity Mail",
        outcomes: sent / noMail / error)
        → all outcomes → AccountLockoutNode (LOCK) → SuccessNode
  → low_medRisk → SuccessNode
```

All notification outcomes route forward — a failed notification email never blocks the user.

---

## ModifyAuthLevelNode + AuthLevelDecisionNode Step-Up Chain

Used to trigger MFA only when risk warrants it:

```
product-PingOneProtectEvaluationNode
  → medium / high → ModifyAuthLevelNode (authLevelIncrement: 1)

[Back in main journey, after Threat Detection ITE:]
AuthLevelDecisionNode (threshold: 1)
  → true (level elevated) → InnerTreeEvaluatorNode (MFA Authentication)
  → false (level normal)  → SuccessNode (skip MFA)
```

This decouples the risk signal (set in the inner journey) from the step-up decision (evaluated in the main journey).

---

## PingOneProtectInitializeNode Configuration

| Field | Production value |
|---|---|
| `behavioralDataCollection` | `true` |
| `enableTrust` | `false` |
| `disableTags` | `false` |
| `consoleLogEnabled` | `false` |
| `deviceKeyRsyncIntervals` | `14` |
| `disableHub` | `false` |
| `lazyMetadata` | `false` |
| `deviceAttributesToIgnore` | `[]` |

Cannot be placed inside a PageNode.

---

## Multiple Flow Types in One Journey

Production journeys use multiple `product-PingOneProtectEvaluationNode` instances for different flow types:
- `AUTHENTICATION` — for login flows
- `AUTHORIZATION` — for transaction/step-up flows
- `REGISTRATION` — for new user registration

The `Determine Flow Type` ScriptedDecisionNode routes to the correct instance based on a shared state flag set earlier in the journey.

## Prerequisites

- PingOne Protect service enabled in the tenant environment
- Worker service ID configured in the Protect node
- Risk policy configured in PingOne Protect
- PingOne SDK 4.4.0+ on the client (required for behavioral data collection)
- `IdentifyExistingUserNode` run before evaluation (to populate `userId` for Protect)

## Common variants

| Variant | Note |
|---|---|
| Registration only | Use `flowType: REGISTRATION`; medium risk may block registration rather than trigger MFA |
| No account disable on high risk | Remove `AccountLockoutNode` from high-risk path; route to MFA step-up or FailureNode instead |
| Evaluation without init (returning session) | Set `p1ProtectAction: "eval"` without init for users with an existing Protect session |

## Related references

- `journey-use-cases/mfa-authentication-multi-method.md`
- `journey-use-cases/financial-services-step-up.md`
- `nodes/risk-management-nodes.md`

## Source

[PingOne Protect Evaluation node](https://docs.pingidentity.com/auth-node-ref/latest/pingone/pingone-protect-evaluation.html)
[Authentication nodes — PingOne AIC](https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html)
