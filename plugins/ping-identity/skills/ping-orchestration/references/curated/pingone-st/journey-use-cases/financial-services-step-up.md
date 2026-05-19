---
title: "PingOne ST — Financial Services Step-Up and Transaction Authorization"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: ["protect"]
audience: ["developer", "architect"]
use_cases: ["customer", "workforce"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-05-21"
slug: "https://docs.pingidentity.com/auth-node-ref/latest/overview.html"
---

# PingOne ST — Financial Services Step-Up and Transaction Authorization

Design patterns for financial-grade authentication journeys: full lifecycle credential outcomes, PingOne Authorize for per-transaction policy, step-up MFA, KBA, and operational routing. Derived from the Financial Services and Money Transfer journey exports.

## Scope

**Covers:** `IdentityStoreDecisionNode` lifecycle outcomes, `PingOneAuthorizeNode` transaction authorization, PUSH_REQ/APPROVAL_REQ/KBA_REQUIRED action responses, Enhanced KBA, `ConfigProviderNode`, `SetSuccessUrlNode`, `PollingWaitNode`.
**Does NOT cover:** PingOne Protect risk integration — see `journey-use-cases/pingone-protect-risk-integration.md`. MFA device registration — see `journey-use-cases/passwordless-mfa-registration.md`.

---

## Main Journey Structure

```
ScriptedDecisionNode ("Prerequisites & Init Variables")
  → ScriptedDecisionNode ("Is Protect Analysis Required?")
  → InnerTreeEvaluatorNode (Initialize P1 Protect)
  → InnerTreeEvaluatorNode (Protect Evaluation & Mitigation)
  → InnerTreeEvaluatorNode (SignOn)
  → AuthLevelDecisionNode ("MFA Based On Risk Level?")
      → true → InnerTreeEvaluatorNode (MFA Authentication)
      → false → continue
  → InnerTreeEvaluatorNode (Manage Account)
  → SetSuccessUrlNode ("Redirect to Manage Account Page")
  → PollingWaitNode
```

The `AuthLevelDecisionNode` after SignOn checks whether risk evaluation elevated the auth level — only triggers MFA if needed. This is the risk-driven step-up pattern.

---

## IdentityStoreDecisionNode — Full Lifecycle Outcomes

Used in the SignOn inner journey instead of `DataStoreDecisionNode` to handle account lifecycle states explicitly.

- Outcomes: **TRUE** / **FALSE** / **LOCKED** / **EXPIRED** / **CANCELLED**

**Required wiring per outcome:**

| Outcome | Recommended routing |
|---|---|
| `TRUE` | Continue journey (authentication success) |
| `FALSE` | Retry limit → FailureNode |
| `LOCKED` | Message node ("Account locked") → account recovery flow or FailureNode |
| `EXPIRED` | Password change inner journey → re-authenticate |
| `CANCELLED` | FailureNode (user cancelled the authentication) |

Never leave `LOCKED` or `EXPIRED` routing to a generic FailureNode in production — users cannot self-service their way out.

---

## Transaction Authorization: PingOneAuthorizeNode

Used to enforce fine-grained policy on individual transactions. Evaluates an authorization policy in PingOne Authorize, distinct from authentication.

**Standard payment/transfer pattern:**
```
PageNode (collect transaction details)
  → PingOneAuthorizeNode
      → permit → PatchObjectNode (update balance/record) → SuccessNode
      → deny → message or FailureNode
      → PUSH_REQ → ScriptedDecisionNode ("Push Approval Notification")
                       → continue / error / noMail → PageNode ("Transfer Success")
      → APPROVAL_REQ → EmailSuspendNode ("Transfer Approval via Email")
                      → [user approves by clicking link]
                      → PatchObjectNode → SuccessNode
      → indeterminate → FailureNode
      → clientError → FailureNode
```

**`indeterminate` and `clientError` must have explicit handlers.** Do not leave them unwired — an indeterminate authorization should fail safe (deny), not silently succeed.

**KBA-based authorization (Enhanced KBA):**
```
PingOneAuthorizeNode
  → KBA_REQUIRED → ScriptedDecisionNode ("Calculate KBA Threshold")
                 → PageNode ("Display Questions")
                       outcomes: error / limitExceeded / noQuestions / questions
                 → questions: PageNode (KBA answers)
                            → SuccessNode / FailureNode
  → permit → proceed without KBA
```

`PingOneAuthorizeNode` determines *whether* KBA is required via policy — the journey then presents the appropriate questions.

---

## ConfigProviderNode for Externalized Messaging

Used to decouple user-facing message text from journey scripting.

- Outcomes: **outcome** / **CONFIGURATION_FAILED**
- Reads from ESV (environment-level secret/variable) or configuration store
- `CONFIGURATION_FAILED` must be handled — use a fallback hardcoded message rather than routing to FailureNode

**Pattern:**
```
ConfigProviderNode ("Set Success Message")
  → outcome → [next node uses successMessage from shared state]
  → CONFIGURATION_FAILED → [proceed with fallback message]
```

---

## SetSuccessUrlNode — Post-Journey Redirect

Used to redirect the user to an application page after the journey completes, rather than the default OIDC redirect.

- Single `outcome`
- Place after the last journey step, before `PollingWaitNode` if async provisioning is needed

**Observed use:** Financial Services and Money Transfer redirect to the application's account management or transfer page after session establishment.

---

## PollingWaitNode at Journey End

Used to wait for asynchronous provisioning or account operations to complete before declaring success.

- `secondsToWait: 5`
- Outcomes: **DONE** / **EXITED**
- Observed at the end of: registration journeys (waiting for IDM to complete provisioning), financial services main journey (waiting for session enrichment)
- `EXITED`: route to SuccessNode — user has dismissed the wait screen; do not block on polling

---

## T&C Enforcement in Authenticated Journeys

Authentication journeys in financial-grade use cases enforce current T&C version on each login:

```
TermsAndConditionsDecisionNode
  → false (not accepted or outdated) → AcceptTermsAndConditionsNode → continue
  → true (accepted and current) → continue
```

This ensures users who have not accepted a new T&C version are prompted on the next sign-in, not just at registration.

---

## Email Verification Gate in SignOn

```
AttributeValueDecisionNode ("Is Email Verified?")
  → false → [email verification inner journey]
          → [verified] → continue
  → true → continue
```

Users who registered without completing email verification are gated on each subsequent login until they verify.

---

## Security Considerations

- `IdentityStoreDecisionNode(LOCKED)` must route to a meaningful UX — do not silently fail locked accounts
- `PingOneAuthorizeNode(indeterminate)` must fail safe — deny by default
- High-risk Protect outcomes should disable the account and send an admin notification before routing to Failure
- All `PingOneProtectResultNode` calls must appear at both success and failure paths
- Session should be re-evaluated or re-issued after a privilege change or step-up MFA event

## Prerequisites

- PingOne Protect service enabled (for risk integration)
- PingOne Authorize service enabled with transaction policies configured (for PingOneAuthorizeNode)
- Twilio Verify credentials configured (for SMS/VOICE MFA paths)
- Email notification templates: `disabledAccountRecovery`, `magicLinkTemplate`, transaction approval templates

## Related references

- `journey-use-cases/pingone-protect-risk-integration.md`
- `journey-use-cases/mfa-authentication-multi-method.md`
- `nodes/risk-management-nodes.md`
- `nodes/identity-management-nodes.md`

## Source

[Authentication nodes — PingOne AIC](https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html)
[PingOne Authorize](https://docs.pingidentity.com/pingoneauthorize/latest/overview.html)
