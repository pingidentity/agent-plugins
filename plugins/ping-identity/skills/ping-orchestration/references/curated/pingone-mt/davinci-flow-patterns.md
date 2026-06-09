---
title: "PingOne — DaVinci Flow Patterns"
product_family: pingone-mt
products: ["davinci", "pingone"]
capabilities: ["orchestration"]
services: []
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/davinci/flows/davinci_flows.html"
---

# PingOne — DaVinci Flow Patterns

Common DaVinci flow designs for authentication, registration, MFA step-up, progressive profiling, and error handling.

## Scope

**Covers:** Common DaVinci flow design patterns, branching logic, error paths, and reusable subflow composition.
**Does NOT cover:** DaVinci concepts and setup — see `references/curated/pingone-mt/davinci-overview.md`. PingOne environment setup — see `ping-foundation`.

---

## Login flow pattern

**Minimal username/password login:**

1. **HTTP** (start) — receives the authorization request from the application
2. **PingOne** (Read User) — look up the user by `username`; branch `Not Found` → error
3. **PingOne** (Check Password) — validate submitted password; branch `Failed` → retry or lock
4. **Flow Control** (Success) — set user token and redirect to application

**Key decisions:**
- Use **PingOne Read User** before password check so you can branch on account status before credential validation
- Cap retries with a **Variables** counter node and branch to account lock after N failures

---

## Registration flow pattern

**Self-service registration with email verification:**

1. **HTTP** (start)
2. **PingOne** (Read User) — check for existing account; `Found` → duplicate-account error
3. **HTML Template** — collect username, password, and profile attributes
4. **PingOne** (Create User) — create the managed object; `Failed` → error
5. **PingOne Notifications** (Send Email) — send OTP or magic link
6. **HTML Template** — collect OTP input
7. **PingOne** (Verify OTP) — validate OTP; `Failed` → retry or cancel
8. **Flow Control** (Success) — redirect

**Key constraints:**
- On Create User failure, delete the partially created user before routing to the error path
- OTP expiry should match the HTML Template timeout; do not allow stale codes to succeed

---

## MFA step-up pattern

**Risk-triggered step-up using PingOne Protect and PingOne MFA:**

1. Complete username/password login (see Login flow)
2. **PingOne Protect** (Evaluate) — get risk score; `LOW` → skip MFA; `MEDIUM`/`HIGH` → MFA subflow
3. **[Subflow]** MFA Authentication:
   - **PingOne MFA** (Send OTP) — send to registered device
   - **HTML Template** — collect OTP
   - **PingOne MFA** (Verify OTP) — validate; `Failed` → retry loop; `No Device` → device registration subflow
4. **Flow Control** (Success) — set elevated token

**Key decisions:**
- Always send the Protect result back after success AND failure to maintain the risk model
- Use a dedicated MFA subflow so it can be reused across login, registration, and step-up flows

---

## Progressive profiling pattern

**Collect additional attributes on subsequent logins:**

1. Complete login (see Login flow)
2. **PingOne** (Read User) — check profile completeness attribute or last-prompted date
3. **Flow Control** — branch: `Complete` → skip to success; `Incomplete` → profiling
4. **HTML Template** — collect missing attributes
5. **PingOne** (Update User) — patch the managed object
6. **Flow Control** (Success)

**Key decisions:**
- Store a `profileComplete` flag or `lastProfilePromptDate` on the user object to gate repeat prompts
- Only collect what is necessary for the current session context — avoid collecting all attributes at once

---

## Error handling pattern

Every DaVinci flow should handle three error categories:

| Category | Cause | Handling |
|---|---|---|
| **User error** | Invalid input, wrong password, expired OTP | Re-render the HTML Template with an inline error message; do not terminate the flow |
| **System error** | Connector failure, API timeout | Log via a Variables node; redirect to a generic error page with a correlation ID |
| **Security block** | Account locked, risk threshold exceeded, fraud signal | Terminate with a clear user message; do not expose the reason beyond "account unavailable" |

**Anti-pattern:** Terminating the flow on every error without user-visible feedback causes silent dead ends. Always ensure the user receives a visible message and a next step (retry, contact support, etc.).

---

## Subflow composition

Use subflows (Flow Connector) to share logic across multiple top-level flows:

| Subflow | Use |
|---|---|
| MFA Authentication | Reusable MFA challenge with retry and recovery code support |
| Risk Evaluation | PingOne Protect init + eval + result reporting |
| Device Registration | Enroll a new MFA device (TOTP, push, SMS) |
| Email Verification | Send OTP, collect code, verify — used in registration and recovery |

Map subflow output variables explicitly. All subflows should have a defined success path and a defined failure path that the parent flow handles.

---

## Prerequisites

- PingOne environment with DaVinci enabled
- At least one DaVinci connector configured
- PingOne application with DaVinci policy assigned (see `references/curated/pingone-mt/davinci-overview.md`)

## Common variants

- **Workforce flows:** use PingFederate or Okta connectors for upstream federation; MFA step-up triggers on resource access
- **CIAM flows:** progressive registration, social login with local account linking, consent collection on first login

## Related references

- `references/curated/pingone-mt/davinci-overview.md`

## Source

[DaVinci flows](https://docs.pingidentity.com/davinci/flows/davinci_flows.html)
[Getting started with flows](https://docs.pingidentity.com/davinci/flows/davinci_getting_started.html)
[DaVinci connectors](https://docs.pingidentity.com/davinci/connectors/davinci_connections.html)
[Best practices](https://docs.pingidentity.com/davinci/davinci_best_practices/davinci_best_practices.html)
