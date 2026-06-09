---
title: "PingOne Advanced Identity Cloud (AIC) — Account Recovery and Username Reminder"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: []
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/auth-node-ref/latest/overview.html"
---

# AIC — Account Recovery and Username Reminder

Design patterns for the OOTB account recovery and username reminder journey family, derived from live AIC journey exports.

## Scope

**Covers:** Anti-enumeration wiring, EmailSuspendNode resume URI pattern, DisplayUserNameNode, in-browser vs. email-body username delivery, email template variables.
**Does NOT cover:** Password reset or password update — see `journey-use-cases/password-reset-and-update.md`. MFA reset — compose with `nodes/mfa-nodes.md`.

---

## Account Recovery (Username Recovery)

The OOTB Account Recovery journey recovers a **username** (not a password) by looking up the account by email address and displaying the username in the browser after email verification.

**Node sequence:**
```
PageNode (collect mail)
  → IdentifyExistingUserNode (identityAttribute: mail, identifier: userName)
      → true AND false → EmailSuspendNode (anti-enumeration)
  → DisplayUserNameNode (shows recovered username in browser)
  → InnerTreeEvaluatorNode (tree: Login)
      → true → SuccessNode
      → false → FailureNode
```

**Email template:** `emailVerification` — contains `{{object.resumeURI}}` as the resume link. 24-hour expiry. English only in OOTB.

**Key decision:** Username is shown in the browser after email verification (via `DisplayUserNameNode`). The user then proceeds directly to Login. This is suitable when you want the user to see their username and immediately authenticate.

---

## Forgotten Username (Email Delivery)

The OOTB Forgotten Username journey sends the username inside the email body rather than displaying it in the browser.

**Node sequence:**
```
PageNode (collect mail, validateInputs: false)
  → IdentifyExistingUserNode (identityAttribute: mail, identifier: userName)
      → true AND false → EmailSuspendNode (anti-enumeration)
  → InnerTreeEvaluatorNode (tree: Login)
      → true → SuccessNode
      → false → FailureNode
```

**Email template:** `forgottenUsername` — contains `{{object.userName}}` inline in the email body; also provides `{{object.resumeURI}}` as a login link. Bilingual (English + French) in OOTB — the only bilingual template in the standard set.

**Key decision:** No `DisplayUserNameNode` — the username never appears in the browser. The user receives it by email and then follows the resume link to the Login journey.

---

## Anti-Enumeration Pattern

**Critical:** Both `true` and `false` outcomes from `IdentifyExistingUserNode` must connect to the **same** `EmailSuspendNode`. The user-facing message must be identical regardless of whether an account was found.

```
IdentifyExistingUserNode
  → true ─┐
           ├─→ EmailSuspendNode ("If the details provided match our records...")
  → false ─┘
```

**User-facing message (OOTB):** `"If the details provided match our records, you will receive an email with further instructions."`

**Never route `true` and `false` to different messages** — that leaks account existence and violates the OWASP recommendation against username enumeration.

**Rate limiting:** The anti-enumeration message alone does not prevent abuse. Add rate limiting at the WAF or API gateway level for production deployments.

---

## EmailSuspendNode Configuration

| Field | Value | Notes |
|---|---|---|
| `emailTemplateName` | `emailVerification` or `forgottenUsername` | Template must contain `{{object.resumeURI}}` |
| `objectLookup` | `true` | Required for the template to access managed object attributes |
| Message | User-facing browser message | Shown while the user waits for the email |

**Resume URI behavior:** When the user clicks the link in the email, the journey resumes at the node immediately after `EmailSuspendNode`. The resume URI is single-use and time-limited (24 hours in OOTB templates).

---

## Email Template Variables

| Variable | Available in | Notes |
|---|---|---|
| `{{object.resumeURI}}` | Both templates | Journey resume link; required for email-gated flows |
| `{{object.userName}}` | `forgottenUsername` | Embeds the username in the email body; use `{{#if object.userName}}` conditional |
| `{{object.mail}}` | Available | User's email address |

---

## DisplayUserNameNode vs. email-body delivery

| Approach | When to use |
|---|---|
| `DisplayUserNameNode` (Account Recovery) | User should see their username in the browser and immediately log in; in-person or single-device flow |
| Email body delivery (Forgotten Username) | Username delivered out-of-band; user may be on a different device when reading the email |

---

## Inner Journey Handoff

Both OOTB journeys end with `InnerTreeEvaluatorNode(tree: Login)` — the user is routed into the Login journey after recovery. This avoids duplicating authentication logic in the recovery journey.

**Configuration:** The Login inner journey must exist and be activated in the same realm.

## Prerequisites

- Email notification service configured in the tenant
- Email templates (`emailVerification`, `forgottenUsername`) present in IDM notification templates
- `managed/alpha_user` with `mail` and `userName` attributes accessible

## Related references

- `journey-use-cases/password-reset-and-update.md`
- `nodes/identity-management-nodes.md`
- `nodes/utility-nodes.md`

## Source

[Authentication nodes — PingOne AIC](https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html)
