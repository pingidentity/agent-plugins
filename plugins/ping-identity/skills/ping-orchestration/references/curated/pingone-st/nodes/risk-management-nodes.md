---
title: "PingOne ST — Risk Management Nodes"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: ["protect"]
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: reference
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/auth-node-ref/latest/overview.html"
---

# PingOne ST — Risk Management Nodes

Nodes for evaluating authentication risk, enforcing account lockout, CAPTCHA, auth level routing, and transaction-level authorization.

## Scope

**Covers:** PingOne Protect integration, account lockout, CAPTCHA, auth level routing, PingOne Authorize, and production-observed configuration.
**Does NOT cover:** MFA enrollment triggered by risk — compose with `nodes/mfa-nodes.md`. PingOne Protect service setup — see `ping-universal-services`.

---

## PingOne Protect (Risk Evaluation)

The PingOne Protect integration uses a consistent triple-node pattern across all production journeys. Always wrap this pattern in a dedicated inner journey called via `InnerTreeEvaluatorNode`.

### PingOne Protect Initialize node (`product-PingOneProtectInitializeNode`)
Initializes the PingOne Protect SDK session on the client side. Must run before any Evaluation node in the same user session.

**Production configuration:**

| Field | Observed value |
|---|---|
| `behavioralDataCollection` | `true` |
| `enableTrust` | `false` |
| `disableTags` | `false` |
| `consoleLogEnabled` | `false` |
| `deviceKeyRsyncIntervals` | `14` |
| `disableHub` | `false` |
| `lazyMetadata` | `false` |
| `deviceAttributesToIgnore` | `[]` |

- Cannot be placed inside a Page node
- Outcomes: **true** / **false** — `false` routes to FailureNode in all observed patterns

### PingOne Protect Evaluation node (`product-PingOneProtectEvaluationNode`)
Calls PingOne to calculate a risk score and recommended mitigations.

**Production configuration:**

| Field | Observed values | Notes |
|---|---|---|
| `flowType` | `AUTHENTICATION` / `AUTHORIZATION` / `REGISTRATION` | Set via shared state from preceding ScriptedDecisionNode |
| `pauseBehavioralData` | `true` | |
| `storeEvaluateResult` | `true` | |
| `deviceSharingType` | `SHARED` | |
| `scoreThreshold` | `300` | Numeric threshold for exceed outcome |
| `userId` | `protectUserId` | Shared state key pre-populated by "Set UserId and Username For Protect" script |
| `username` | `protectUsername` | Shared state key |
| `userType` | `EXTERNAL` | |
| `recommendedActions` | `[BOT_MITIGATION, AITM_MITIGATION, TEMP_EMAIL_MITIGATION]` | |

- Outcomes: **low** / **medium** / **high** / **exceed** / **failure** / **BOT_MITIGATION** / **AITM_MITIGATION** / **TEMP_EMAIL_MITIGATION** / **clientError**
- Multiple instances per journey are allowed for different `flowType` values (Authentication vs. Authorization vs. Registration)
- `userId` and `username` must be pre-loaded into shared state by a `ScriptedDecisionNode` before this node runs

**Standard outcome routing:**
- `low` → continue journey (no step-up)
- `medium` → step-up MFA inner journey
- `high` → `ModifyAuthLevelNode` → `AccountActiveDecisionNode` → `AccountLockoutNode` (disable) → notification email → FailureNode
- `BOT_MITIGATION` / `AITM_MITIGATION` / `TEMP_EMAIL_MITIGATION` / `failure` / `clientError` / `exceed` → FailureNode

### PingOne Protect Result node (`product-PingOneProtectResultNode`)
Reports the authentication outcome back to PingOne Protect to update the risk model.

- Outcomes: single
- **Must be called at BOTH the success path and the failure path** — call it before SuccessNode AND before FailureNode. Omitting it on one path degrades the Protect risk model.

---

## Protect Triple-Node Pattern

Standard sequence used in all four complex journey suites:

```
ScriptedDecisionNode ("P1 Protect Action?", outcomes: init / eval)
  → init: product-PingOneProtectInitializeNode → true → SuccessNode
  → eval: IdentifyExistingUserNode
        → ScriptedDecisionNode ("Set UserId and Username For Protect")
        → ScriptedDecisionNode ("Determine Flow Type", outcomes: Authentication / Authorization / Registration)
        → product-PingOneProtectEvaluationNode (per flow type)
          → low: ... → product-PingOneProtectResultNode (SUCCESS) → SuccessNode
          → high/medium: ModifyAuthLevelNode → ...
          → mitigation/failure/clientError/exceed: product-PingOneProtectResultNode (FAILED) → FailureNode
```

The `P1 Protect Action?` script checks a shared state flag (`p1ProtectAction`) to distinguish between the initialization call and the evaluation call — allowing the same inner journey to handle both phases within a session.

---

## New Device Detection Pattern

Observed in Financial Services and Money Transfer threat detection inner journeys:

```
product-PingOneProtectEvaluationNode
  → ScriptedDecisionNode ("Extract Protect Activity Params",
      outcomes: highRisk / newDevice / low_medRisk)
  → newDevice: ScriptedDecisionNode ("Notify New Device Detected",
      outcomes: sent / noMail / error)
      → all outcomes → SuccessNode (notification is best-effort; does not block)
  → highRisk: ScriptedDecisionNode ("Send Suspicious Activity Mail",
      outcomes: sent / noMail / error)
      → all outcomes → AccountLockoutNode (disable) → SuccessNode
```

Notification failure (noMail, error) does not block the journey — notification is best-effort. Account disable applies only on confirmed high-risk.

---

## PingOne Authorize (`PingOneAuthorizeNode`)

Used for fine-grained, per-transaction authorization policy decisions. Distinct from authentication — evaluates whether the user is permitted to perform a specific action given current context.

- Outcomes: **permit** / **deny** / **indeterminate** / **clientError** + action-specific outcomes
- Action-specific outcomes observed: `PUSH_REQ` (send push approval notification), `APPROVAL_REQ` (email approval), `KBA_REQUIRED` (require KBA challenge)
- `permit` → allow the transaction
- `deny` → block with user-facing message
- `indeterminate` / `clientError` → FailureNode (must handle explicitly)

**Pattern — transaction authorization gate (Make Payment, Money Transfer):**
```
PageNode (collect transaction details)
  → PingOneAuthorizeNode
      → permit: PatchObjectNode (update balance/record)
      → PUSH_REQ: ScriptedDecisionNode ("Push Approval Notification")
      → APPROVAL_REQ: EmailSuspendNode (suspend journey; user approves via email)
      → deny / indeterminate / clientError: FailureNode
```

**Pattern — policy-driven KBA (Enhanced KBA):**
```
PingOneAuthorizeNode
  → KBA_REQUIRED: ScriptedDecisionNode ("Calculate KBA Threshold")
                → PageNode ("Display Questions")
```

PingOne Authorize requires a license and external policy configuration. All `indeterminate` and `clientError` outcomes must have explicit fallback handling — do not leave them unwired.

---

## Account Lockout

### Account Lockout node
Locks or unlocks a user's account.

- Configuration: `lockAction: LOCK` or `UNLOCK`
- Outcomes: single (modifies account status and proceeds)
- Used to **disable** accounts after high-risk Protect evaluation (Financial Services, Money Transfer)
- Used to **enable** accounts in registration cleanup paths (removing partial users)

### Account Active Decision node
Checks whether the current user's account is active.

- Outcomes: **True** (account active) / **False** (account inactive/locked)
- Place early in the journey, after user lookup, to gate locked-out users before credential validation
- Observed placement: always after `IdentifyExistingUserNode` or `IdentityStoreDecisionNode`

### Retry Limit Decision node
Tracks retry attempts within a journey loop and routes when the limit is exceeded.

- `retryLimit: 3`, `incrementUserAttributeOnFailure: true`
- Outcomes: **True** (within limit; retry allowed) / **False** (limit exceeded; reject)
- Core node in the **retry-loop-with-lockout pattern** used in all MFA input flows (see `nodes/mfa-nodes.md`)

---

## CAPTCHA

### reCAPTCHA Enterprise node
Integrates Google reCAPTCHA Enterprise. Requires a Google Cloud project and API key.

- Outcomes: **Success** / **Failure**

### CAPTCHA node (legacy)
Legacy CAPTCHA integration. Prefer reCAPTCHA Enterprise for new journeys.

- Outcomes: **Success** / **Failure**

---

## Authentication Level

### Auth Level Decision node
Routes the journey based on the current session authentication level.

- Outcomes: **True** (level meets threshold) / **False** (level below threshold)
- Use in combination with `ModifyAuthLevelNode` to implement risk-driven step-up: Protect evaluation sets the level, this node decides whether MFA is needed
- Observed placement in Financial Services and Money Transfer: after Protect evaluation chain, before MFA inner journey

### Modify Auth Level node
Increments or sets the session authentication level.

- `authLevelIncrement: 1` — increments the current level
- Outcomes: single
- Place after a successful authentication factor, or after high/medium Protect evaluation to flag that step-up is needed

---

## Common patterns

| Pattern | Nodes |
|---|---|
| PingOne Protect (full inner journey) | ScriptedDecision("P1 Protect Action?") → init path / eval path → PingOneProtectResultNode at both terminations |
| Risk-based step-up | Protect Evaluation(medium/high) → ModifyAuthLevel → AuthLevelDecision(true) → MFA inner journey |
| New device notification | Extract Protect Activity Params(newDevice) → Notify New Device Detected → SuccessNode (best-effort) |
| Lockout after 3 MFA failures | OTPCollector(false) → RetryLimitDecision(false) → AccountLockout(LOCK) → FailureNode |
| Transaction authorization | PingOneAuthorize(permit) → proceed / (PUSH_REQ) → push notification / (deny) → FailureNode |
| Block locked accounts | AccountActiveDecision(false) → FailureNode / (true) → credential collection |

## Prerequisites

- PingOne Protect service enabled in the PingOne environment.
- PingOne Authorize license required for `PingOneAuthorizeNode` and policy-driven KBA.
- Protect SDK initialized before `PingOneProtectEvaluationNode` runs — the Initialize node must precede it in the same session.

## Common variants

- **Registration risk evaluation:** set `flowType: REGISTRATION` on the Evaluation node; use a separate inner journey from the authentication path.
- **Transaction authorization only (no login risk):** invoke the Protect pattern from within a post-login inner journey triggered by a specific action (e.g., payment, profile change).

## Related references

- `nodes/mfa-nodes.md`
- `nodes/basic-auth-nodes.md`
- `nodes/utility-nodes.md`
- `journey-use-cases/pingone-protect-risk-integration.md`
- `journey-use-cases/financial-services-step-up.md`

## Source

[Risk management nodes](https://docs.pingidentity.com/auth-node-ref/latest/overview.html)
[PingOne Protect Evaluation node](https://docs.pingidentity.com/auth-node-ref/latest/pingone/pingone-protect-evaluation.html)
[Account Lockout node](https://docs.pingidentity.com/auth-node-ref/latest/account-lockout.html)
