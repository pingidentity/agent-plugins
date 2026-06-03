---
title: "PingOne MT — DaVinci Registration and MFA Flow Patterns"
product_family: pingone-mt
products: ["davinci", "pingone"]
capabilities: ["orchestration"]
services: ["mfa"]
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/davinci/flows/davinci_getting_started.html"
---

# PingOne MT — DaVinci Registration and MFA Flow Patterns

Complete flow designs for user registration with email verification, and MFA step-up using PingOne MFA and PingOne Protect — the two most common DaVinci use cases.

## Scope

**Covers:** Self-service registration with email OTP verification, MFA device enrollment, risk-triggered step-up, subflow composition, and error path patterns for both scenarios.
**Does NOT cover:** DaVinci concepts and setup — see `references/curated/pingone-mt/davinci-overview.md`. Generic flow patterns — see `references/curated/pingone-mt/davinci-flow-patterns.md`. PingOne app and environment setup — see `ping-foundation`.

---

## Registration with email verification

**Goal:** Create a PingOne user, send a verification OTP, and gate progression on OTP confirmation.

### Flow structure

```
[HTTP — Start]
  → PingOne (Read User by username)
      If Found → [Error: Account already exists]
      If Not Found →
  → HTML Form (collect: username, password, given name, family name, email)
  → PingOne (Create User)
      If Failed → [Delete partial user if created] → [Error]
      If Success →
  → PingOne Notifications (Send OTP to email)
  → HTML Form (collect OTP input)
  → PingOne (Verify OTP)
      If False → Retry loop (max 3) → [Error: Too many attempts]
      If True →
  → PingOne (Update User — set emailVerified: true)
  → [Success — redirect to application]
```

### Key decisions and constraints

| Decision point | Rule |
|---|---|
| Check for existing user before Create | Prevents duplicate account errors from the Create User node; surfaced early with a clean error message |
| Delete partial user on Create failure | If Create User fails mid-flow, delete the partial record before routing to error to prevent orphaned accounts |
| OTP expiry alignment | Set OTP validity in PingOne Notifications to match the HTML Form session timeout; expired OTPs cause false `Invalid code` errors |
| Retry cap | Track attempt count with a Company Variable or Functions connector; redirect to error after 3 failures to prevent OTP brute force |
| Post-verification attribute | Set `emailVerified: true` on the user object via Update User after OTP success; downstream flows can gate on this attribute |

### Subflow recommendation

Extract the OTP verification steps (Send → Collect → Verify) into a reusable `Email Verification` subflow. It can be called from registration, recovery, and email-change flows without duplication.

---

## MFA enrollment at registration

**Goal:** Require users to enroll a second factor during or immediately after registration.

### Inline enrollment (end of registration flow)

```
[After PingOne Create User succeeds]
  → PingOne MFA (Get Devices)
      If no devices → [MFA Enrollment subflow]
      If devices exist → [skip enrollment, proceed to success]
  → [Success]
```

**MFA Enrollment subflow:**
```
[HTML Form — method selection: TOTP / SMS / Email OTP]
  → PingOne MFA (Send Pairing Key or initiate enrollment)
  → HTML Form (collect enrollment confirmation)
  → PingOne MFA (Verify enrollment)
      If Failed → Retry → [Error after max retries]
      If Success →
  → [Return to parent — enrolled]
```

### Deferred enrollment (on next login)

```
[Login flow — after credential verification]
  → PingOne MFA (Get Devices)
      If no devices → [MFA Enrollment subflow] (above)
      If devices exist → [MFA Authentication subflow]
  → [Success]
```

**Use deferred enrollment** when MFA adoption is being rolled out gradually or when the registration flow is already complex.

---

## MFA step-up with PingOne Protect

**Goal:** Evaluate risk at sign-in and require MFA only when risk is elevated.

### Flow structure

```
[HTTP — Start]
  → PingOne Protect (Initialize)  ← always first; sets up the risk session
  → HTML Form (collect username + password)
  → PingOne (Read User + Check Password)
      If Failed → PingOne Protect (Update — failed auth) → [Error]
      If Success →
  → PingOne Protect (Evaluate)
      LOW risk   → PingOne Protect (Update — success, no MFA) → [Success]
      MEDIUM risk → [MFA subflow]
      HIGH risk   → [MFA subflow] or [Block]
  → PingOne Protect (Update — success, with MFA)
  → [Success]
```

### PingOne Protect initialization rules

| Rule | Reason |
|---|---|
| Initialize before credential collection | The risk session must be open before any user signals are captured |
| Always call Update after success or failure | Risk model degrades if result is never reported back; the Update call closes the risk session |
| Use HIGH risk → block for admin or privileged accounts | High-risk admin sessions should not be salvageable with MFA alone |

### MFA subflow (reusable)

```
[PingOne MFA — Get Devices]
  If no devices → [MFA Enrollment subflow]
  If devices → [Choose method or use default]
    → PingOne MFA (Send OTP / initiate push)
    → HTML Form (collect OTP or poll push result)
    → PingOne MFA (Verify)
        If Failed → Retry loop (max 3) → [Block]
        If Success → [Return to parent — MFA passed]
```

Extract this into a `MFA Authentication` subflow. Reference it from both login and step-up flows to ensure consistent behavior.

---

## Error handling

| Category | DaVinci pattern |
|---|---|
| User input error (wrong password, invalid OTP) | Re-render HTML Form with inline error message via a Variables node; set error message in flow variable before looping back |
| System error (connector failure, API timeout) | Log with Functions connector; redirect to generic error page with a correlation ID stored in a flow variable |
| Security block (account locked, risk HIGH + no MFA) | Terminate via Flow Control with a user-visible message; do not expose the specific reason |
| Partial state cleanup | On Create User failure or mid-enrollment abort, explicitly call Delete User or cleanup node before routing to error |

**Anti-pattern:** Routing every error outcome to a blank dead-end (no message, no next step). Always set a user-visible error message before terminating.

---

## Prerequisites

- PingOne MT environment with DaVinci and PingOne MFA services activated
- PingOne connector instance configured with environment-appropriate credentials
- PingOne Notifications (email) configured and sender domain verified
- For risk step-up: PingOne Protect service activated and PingOne Protect connector instance configured

## Common variants

| Variant | Pattern |
|---|---|
| Social login + local registration | SelectIdP node routes social users to PingOne Social Provider connector; new users auto-provisioned via Create User |
| Progressive profiling after login | After login success, check profile completeness attribute; route incomplete users to attribute collection HTML Form |
| Workforce MFA with Push | Replace TOTP enrollment with PingOne MFA Push; same subflow structure; requires PingID Mobile app |
| Delegated admin enrollment | Admin creates user via PingOne API, sets `mustChangePassword: true`; first login triggers MFA enrollment before password change |

## Related references

- `references/curated/pingone-mt/davinci-overview.md` — DaVinci concepts, versioning, invocation methods
- `references/curated/pingone-mt/davinci-flow-patterns.md` — generic flow patterns (login, registration, step-up, error handling)

## Source

[Getting started with DaVinci flows](https://docs.pingidentity.com/davinci/flows/davinci_getting_started.html)
[DaVinci best practices](https://docs.pingidentity.com/davinci/davinci_best_practices/davinci_best_practices.html)
[DaVinci subflows](https://docs.pingidentity.com/davinci/davinci_best_practices/davinci_best_practices_subflows.html)
[Implementing a flow in an application](https://docs.pingidentity.com/davinci/integrating_flows_into_applications/davinci_how_to_implement_a_flow.html)
