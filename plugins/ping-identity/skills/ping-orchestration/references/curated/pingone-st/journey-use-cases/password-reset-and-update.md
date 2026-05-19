---
title: "PingOne ST — Password Reset and Authenticated Update"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: []
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-05-21"
slug: "https://docs.pingidentity.com/auth-node-ref/latest/overview.html"
---

# PingOne ST — Password Reset and Authenticated Update

Design patterns for unauthenticated password reset (email-gated) and authenticated password update (session-gated), derived from live AIC journey exports.

## Scope

**Covers:** Unauthenticated reset via email, authenticated password change with passwordless user branch, ValidatedPasswordNode settings, PatchObjectNode for password write.
**Does NOT cover:** Username recovery — see `journey-use-cases/account-recovery-and-username-reminder.md`. MFA reset — compose with `nodes/mfa-nodes.md`.

---

## Pattern 1 — Unauthenticated Password Reset (Email-Gated)

Used when the user does not have an active session. Identity is verified via email before a new password is accepted.

**Node sequence:**
```
PageNode (collect mail, required: true)
  → IdentifyExistingUserNode (identityAttribute: mail, identifier: userName)
      → true AND false → EmailSuspendNode (anti-enumeration)
  → [journey suspends — user clicks link in email to resume]
  → PageNode (collect new password, ValidatedPasswordNode, validateInput: true)
  → PatchObjectNode (identityResource: managed/alpha_user)
      → PATCHED → SuccessNode
      → FAILURE → FailureNode
```

**Email template:** `resetPassword` — contains `{{object.resumeURI}}` as the reset link. Bilingual (English + French) in OOTB.

**Anti-enumeration:** Both `IdentifyExistingUserNode` outcomes (`true` and `false`) route to the same `EmailSuspendNode`. User sees: `"If the details provided match our records, you will receive an email with further instructions."`

**PatchObjectNode configuration:**
- `identityResource: managed/alpha_user`
- `patchAsObject: false`
- `ignoredFields: []`

**ValidatedPasswordNode:** `validateInput: true` — new password is validated against the realm's password policy before `PatchObjectNode` writes it.

---

## Pattern 2 — Authenticated Password Update (Session-Gated)

Used when the user has an active session. No login form — the user is identified from the session. Handles both password-based and passwordless users.

**Node sequence:**
```
SessionDataNode (sessionDataKey: UserToken, sharedStateKey: userName)
  → AttributePresentDecisionNode (presentAttribute: password)
      → true (password user): PageNode ("Verify Existing Password")
            → ValidatedPasswordNode (validateInput: false)
            → DataStoreDecisionNode
                → true: PageNode ("Update Password")
                → false: FailureNode
      → false (passwordless user): EmailSuspendNode
            → [resume after email click]
            → PageNode ("Update Password")
  → PageNode ("Update Password")
        → ValidatedPasswordNode (validateInput: true)
        → single outcome
  → PatchObjectNode (ignoredFields: [userName])
      → PATCHED → SuccessNode
      → FAILURE → FailureNode
```

**SessionDataNode** is the canonical entry for authenticated journeys — identifies the current user from the active session without a login form.

**AttributePresentDecisionNode** branches on `password` attribute presence:
- `true` (password set) → require current-password verification before allowing change
- `false` (passwordless user) → gate with email verification instead

**Two ValidatedPasswordNode instances:**

| Instance | `validateInput` | Purpose |
|---|---|---|
| "Verify Existing Password" | `false` | Old credential — no policy enforcement |
| "Update Password" | `true` | New credential — policy enforced |

**PatchObjectNode:** `ignoredFields: [userName]` — prevents the username from being changed via this flow.

---

## Decision: Reset vs. Update

| Criterion | Use Reset | Use Update |
|---|---|---|
| User has an active session | No | Yes |
| User forgot their password | Yes | No |
| Passwordless users need support | Both | Yes (via email gate) |
| Identity verification method | Email (resume URI) | Session (SessionDataNode) or email (passwordless branch) |

---

## Security Considerations

- Email resume URIs are single-use and time-limited — do not extend expiry without increasing rate limiting
- Password change should invalidate or re-issue the session (configure via `SetSessionProperties` or session termination post-patch)
- The `DataStoreDecisionNode` verify step in authenticated update prevents session hijacking from allowing a password change without knowing the current password
- Add `RetryLimitDecisionNode` after `DataStoreDecisionNode(false)` if you want to limit failed current-password attempts before locking

## Prerequisites

- Email notification service configured
- `resetPassword` email template present with `{{object.resumeURI}}`
- `managed/alpha_user` with `password`, `mail`, `userName` attributes accessible
- For authenticated update: active session with `UserToken` session property

## Related references

- `journey-use-cases/account-recovery-and-username-reminder.md`
- `nodes/basic-auth-nodes.md`
- `nodes/identity-management-nodes.md`
- `nodes/utility-nodes.md`

## Source

[Authentication nodes — PingOne AIC](https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html)
