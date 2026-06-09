---
title: "PingOne Advanced Identity Cloud (AIC) — Social and Local Registration and Authentication"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: []
audience: ["developer", "architect"]
use_cases: ["customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/auth-node-ref/latest/overview.html"
---

# AIC — Social and Local Registration and Authentication

Design patterns for CIAM registration and authentication journeys supporting both local credentials and social identity providers. Derived from CIAM Passwordless and basic registration journey exports.

## Scope

**Covers:** Social + local choice entry, `SocialProviderHandlerNodeV2` outcomes, social registration profile collection, `CreateObjectNode` with cleanup, email verification gate, T&C lifecycle, `AttributeValueDecisionNode`.
**Does NOT cover:** MFA registration after account creation — see `journey-use-cases/passwordless-mfa-registration.md`. Progressive profiling — see `journey-use-cases/progressive-profiling.md`.

---

## Entry: Social + Local Choice

```
PageNode (outcomes: localAuthentication / socialAuthentication)
  → localAuthentication → Platform Username → Platform Password → DataStoreDecisionNode
  → socialAuthentication → SocialProviderHandlerNodeV2
```

The entry `PageNode` embeds a `ScriptedDecisionNode` or `ChoiceCollector` that drives the `localAuthentication` / `socialAuthentication` outcomes. This pattern allows a single journey to serve both local and social users.

---

## SocialProviderHandlerNodeV2

**Configuration:**
- Select from IdPs registered in the realm's Social Identity Provider service
- `transformScript`: maps incoming IdP claims to managed object attributes

- Outcomes: **ACCOUNT_EXISTS** / **NO_ACCOUNT** / **SOCIAL_AUTH_INTERRUPTED**

**Per outcome routing:**

| Outcome | Action |
|---|---|
| `ACCOUNT_EXISTS` | Continue to authentication or profile completion |
| `NO_ACCOUNT` | Route to social registration profile collection |
| `SOCIAL_AUTH_INTERRUPTED` | Route to FailureNode |

---

## Social Registration Path

When `NO_ACCOUNT`: collect a minimal profile and create the user object.

```
SocialProviderHandlerNodeV2 → NO_ACCOUNT
  → PageNode (social registration profile fields)
      children: AttributeCollectorNode (mail, givenName, sn — required: false, validateInputs: false)
              + [optional: ValidatedUsernameNode, AcceptTermsAndConditionsNode]
  → RequiredAttributesPresentNode
      → True → CreateObjectNode (identityResource: managed/alpha_user)
                  → CREATED → IncrementLoginCountNode → proceed
                  → FAILURE → ScriptedDecisionNode ("Delete User Entry") → FailureNode
      → False → [re-display form or FailureNode]
```

**`RequiredAttributesPresentNode`** guards `CreateObjectNode` — prevents partial user creation when required fields are missing.

**`CreateObjectNode(FAILURE)` cleanup:** Always follow `FAILURE` with a `ScriptedDecisionNode` that deletes any partial record (`openidm.delete("managed/alpha_user", ...)`) before routing to FailureNode. Prevents orphaned partial accounts from blocking future registrations with the same email.

---

## Local Registration Path (Basic)

```
PageNode (single screen)
  children: AttributeCollectorNode (mail, givenName, sn)
          + ValidatedUsernameNode (validateInput: true)
          + ValidatedPasswordNode (validateInput: true)
          + AcceptTermsAndConditionsNode
  → CreateObjectNode (identityResource: managed/alpha_user)
      → CREATED → IncrementLoginCountNode → SuccessNode
      → FAILURE → FailureNode
```

**Notes:**
- Co-locating `AcceptTermsAndConditionsNode` in the registration PageNode records T&C acceptance at the point of signup
- `validateInput: true` on both Username and Password enforces policy before object creation
- OOTB registration has no email verification — add `EmailSuspendNode` after `CreateObjectNode(CREATED)` if email verification is required

---

## Email Verification Gate (Authentication Journey)

After registration without email verification, the authentication journey gates unverified users:

```
AttributeValueDecisionNode ("Is Email Verified?", attribute: emailVerified, value: true)
  → false → [email verification sub-journey]
              → EmailSuspendNode (emailTemplateName: emailVerification)
              → ScriptedDecisionNode ("Set Email Verification Status To True")
              → PatchObjectNode (set emailVerified: true)
              → continue
  → true → continue
```

The `ScriptedDecisionNode` after `EmailSuspendNode` updates the flag before `PatchObjectNode` writes it — do not rely on `PatchObjectNode` alone.

---

## T&C Lifecycle in Authentication

Authentication journeys enforce current T&C version at each sign-in:

```
TermsAndConditionsDecisionNode
  → false (not accepted or outdated version) → AcceptTermsAndConditionsNode → continue
  → true (accepted and current) → continue
```

When a new T&C version is published, all existing users are prompted on their next login. Users who skip login are not prompted until they return.

---

## Write Federation Information node

After social authentication with an existing account, persist the federation link:

```
SocialProviderHandlerNodeV2 → ACCOUNT_EXISTS
  → WriteFederationInformationNode → continue
```

This stores the external IdP subject identifier linked to the local account, enabling future social logins to resolve to the same user without re-prompting for profile data.

---

## Duplicate Account Handling

The OOTB `CreateObjectNode(FAILURE)` path does not distinguish between "email already in use" and other failures. For production CIAM:

1. Run `IdentifyExistingUserNode` (by `mail`) before `CreateObjectNode`
2. If `true` (account exists): route to account-linking flow or error message
3. If `false` (new user): proceed to `CreateObjectNode`

This prevents confusing failure messages and enables account linking for users who previously registered locally and now attempt social registration.

---

## Prerequisites

- Social Identity Providers configured in realm Social Identity Provider service
- `managed/alpha_user` schema includes `mail`, `givenName`, `sn`, `userName`, `emailVerified` attributes
- Email notification service configured for email verification flow
- `emailVerification` email template present with `{{object.resumeURI}}`

## Common variants

| Variant | Notes |
|---|---|
| Email verification required at registration | Add `EmailSuspendNode` immediately after `CreateObjectNode(CREATED)` before `SuccessNode` |
| Social-only (no local) | Remove `localAuthentication` branch from entry PageNode |
| Profile completion after social login | Add `AttributeCollectorNode` after `ACCOUNT_EXISTS` if profile is incomplete |
| Multiple social providers | Add outcomes to entry `PageNode` per provider; each routes to a separate `SocialProviderHandlerNodeV2` instance |

## Related references

- `journey-use-cases/passwordless-mfa-registration.md`
- `journey-use-cases/progressive-profiling.md`
- `nodes/identity-management-nodes.md`
- `nodes/basic-auth-nodes.md`

## Source

[Authentication nodes — PingOne AIC](https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html)
[Social Provider Handler node](https://docs.pingidentity.com/auth-node-ref/latest/social-provider-handler.html)
