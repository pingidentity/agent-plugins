---
title: "PingOne MT — Sign-On Policies and MFA Configuration"
product_family: pingone-mt
products: ["pingone"]
capabilities: ["foundation"]
audience: ["admin", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/pingone/authentication/p1_authenticationpolicies.html"
---

# PingOne MT — Sign-On Policies and MFA Configuration

Configuring authentication (sign-on) policies and MFA device policies in PingOne MT to control how users prove identity at sign-in.

## Scope

**Covers:** Authentication policy structure, action types and their conditions, MFA device policy configuration, step-up authentication, risk-based MFA conditions (Protect integration), policy attachment to applications, and common configuration gotchas.
**Does NOT cover:** DaVinci flow design — see `skills/ping-orchestration/SKILL.md`. PingOne Protect service setup (risk predictors, risk policy scoring) — see `skills/ping-universal-services/SKILL.md`. PingOne ST journey-based policy — see `skills/ping-orchestration/SKILL.md`. FIDO2 device registration flows.

---

## Sign-on policy structure

An authentication policy is an ordered sequence of **actions** (steps) evaluated top-to-bottom at sign-in. Each action executes in sequence. Conditions on an action determine whether it runs; if no condition matches, the action is skipped or enforced depending on action type.

Key constraints:
- The first action in a policy cannot carry conditions. If you reorder and promote the second action to position 1, its conditions are automatically stripped.
- Up to 20 policies can be assigned per application.
- Policies execute in listed order — all assigned policies are evaluated, not just the first.

---

## Action types

| Action | What it does | When to add it |
|---|---|---|
| Login | Collects username and password (or identifier). Always the first action. | Required for all password-based flows. Cannot be omitted if users authenticate with credentials. |
| Multi-Factor Authentication | Prompts for a second factor. Can be conditional (trigger only when risk or context conditions match). | Any flow requiring step-up or mandatory MFA. References an MFA device policy. |
| Identity Verification | Invokes PingOne Verify to verify a government ID or biometric. Requires PingOne Verify add-on license. | High-assurance onboarding or re-verification flows. Cannot be the first action. |
| Progressive Profiling | Prompts authenticated users for additional attributes (e.g., phone number, address). | Post-registration attribute collection. Cannot be the first action. |
| Agreement | Presents terms of service or consent text. User must accept to proceed. | Compliance consent flows. Cannot be the first action. |
| External Identity Provider | Delegates authentication to a configured external IdP (SAML, OIDC, social). | Federated login; social sign-in. |
| Identifier First | Identifies the user before presenting auth options. Used for home-realm discovery. | Multi-IdP environments where IdP is determined by domain or attribute. |

---

## MFA action conditions

Conditions on the MFA action determine when MFA is triggered. Conditions combine with Boolean OR — any matching condition triggers the MFA step.

| Condition | License requirement |
|---|---|
| Last sign-on older than N hours | None |
| IP address outside allowed CIDR range | None |
| User belongs to a specific population | None |
| User attribute matches a value (e.g., postal code) | None |
| IP reputation is high risk | PingOne Protect or Passwordless |
| Geovelocity anomaly detected | PingOne Protect or Passwordless |
| Anonymous network detected (VPN / Tor / proxy) | PingOne Protect or Passwordless |

When no conditions are set, the MFA action always runs for every sign-in.

---

## MFA device policy configuration

An MFA device policy is a separate, environment-scoped object that the MFA action references. Creating the policy alone does not enable MFA — the policy must be selected inside the MFA action of a sign-on policy, and the sign-on policy must be attached to an application.

### Allowed MFA methods

| Method | Environment | Key notes |
|---|---|---|
| Authenticator app (TOTP) | Both | Standard TOTP; any authenticator app supported |
| Email OTP | Both | OTP valid 30 min; SMTP sender configured in Settings > Notification Senders |
| SMS OTP | Customer | OTP valid 30 min; requires Twilio, Syniverse, or custom gateway; virtual numbers not supported |
| Voice OTP | Customer | OTP valid 30 min; China disabled by regulation |
| FIDO2 / Passkeys | Both | Requires a FIDO policy object; legacy FIDO2 devices require separate migration |
| Mobile push (PingID app) | Workforce | Biometrics, push with number matching, offline OTP |
| Desktop (PingID app) | Workforce | Windows/macOS passwordless |

### Top-level MFA policy fields

| Field | Options | Notes |
|---|---|---|
| Method selection | User selects default / Prompt user to select / Always display (Workforce) | Controls which method the UI presents first |
| Notification policy | Default or named policy | Controls delivery channel priority for OTP messages |
| New device pairing notification | No notification / Email then SMS / SMS then Email | Alert sent to user when a new device is paired |
| Skip user lock verification | Checkbox | Bypasses lockout check during device pairing |
| Remember device | Off / 1 hour – 90 days | Reduces friction on trusted devices; see gotchas for geo restrictions |

### Device pairing and enrollment

| Setting | Options | Notes |
|---|---|---|
| Allow pairing | Enabled / Disabled | Disable to block new device registrations (e.g., freeze enrollment after provisioning) |
| Auto enrollment | On / Off | Triggers enrollment at sign-in if user has no enrolled devices |
| Auto enrollment bypass | Must set MFA action "None or Incompatible Methods" → Bypass | Required for auto-enrollment to work with zero devices |
| Admin pre-provisioning | Via PingOne API or DaVinci | Device registered by admin before user first logs in |

### Bypass codes

Admin-generated single-use codes that bypass MFA for locked-out or unenrolled users. Issued via the PingOne API or admin console per-user. Expire after single use or a configurable TTL.

### FIDO2 / passkey policy fields

| Field | Options | Notes |
|---|---|---|
| Discoverable credentials | Discouraged / Preferred (default) / Required | Must be Required for usernameless / passkey flows |
| User verification | Discouraged / Preferred (default) / Required | Must be Required for usernameless flows |
| Authenticator attachment | Both (default) / Platform / Cross-platform | Platform = device biometrics; Cross-platform = hardware security key |
| Relying party ID | PingOne default / Custom domain / Manual | Must match the app's origin exactly; sandbox allows localhost |
| Device aggregation | Yes / No | Yes collapses multiple FIDO keys into one listed method |

---

## Step-up authentication

Step-up enforces stronger authentication for sensitive resources without requiring a full re-login.

### Per-application policy (native PingOne)

Attach a stricter sign-on policy (with an unconditional MFA action) to the sensitive application. The less-sensitive app uses a weaker policy. Token claims `acr` and `auth_time` carry the satisfied policy identifier and authentication timestamp.

### Claim-based step-up (API / resource server pattern)

1. User authenticates at basic level; access token includes `acr` and `auth_time`.
2. Resource server checks whether `acr` and `auth_time` meet its requirements.
3. If insufficient, resource server returns `401` with challenge header:
   ```
   WWW-Authenticate: Bearer error="insufficient_user_authentication",
     acr_values="strong_authentication_policy", max_age=300
   ```
4. Client re-authorizes with `acr_values` and `max_age` on the authorization request:
   ```
   GET /{envId}/as/authorize?client_id=<id>&scope=secret
     &acr_values=strong_authentication_policy&max_age=300
   ```
5. User completes the stronger sign-on policy; a new access token is issued.

Standards: RFC 9470 (OAuth 2.0 Step-Up Authentication), RFC 6750 (Bearer Token).

### Risk-based step-up (requires PingOne Protect)

Set the MFA action condition to trigger on "IP reputation is high risk", "Geovelocity anomaly", or "Anonymous network". Risk is evaluated per sign-in; MFA is only triggered when the risk threshold is met. See MFA action conditions table above for license requirements.

---

## Policy attachment to applications

A sign-on policy has no effect until explicitly attached to an application. Unattached applications fall back to the **environment default authentication policy**.

| Constraint | Detail |
|---|---|
| Maximum policies per app | 20 |
| Execution order | Policies run in listed order; drag to reorder |
| DaVinci vs. PingOne policies | Mutually exclusive per application — cannot mix native PingOne policies and DaVinci flow policies on the same app |
| Admin console application | Cannot be assigned a custom policy; system policy is fixed |
| Environment default policy | Applies to all apps with no explicit policy assignment; may not enforce MFA — always verify |

**API for policy assignment:**
```
POST https://api.pingone.com/v1/environments/{envId}/applications/{appId}/signOnPolicyAssignments
```

---

## Common gotchas

| Gotcha | Symptom | Fix |
|---|---|---|
| MFA policy not referenced in MFA action | MFA action is present in policy but user is never prompted for a second factor | Open the MFA action settings and confirm an MFA device policy is selected |
| Policy not attached to application | Environment default policy used silently; may skip MFA | Always explicitly attach the sign-on policy to each application |
| Auto enrollment not triggering | User with no devices reaches MFA action and it fails or errors | Set the MFA action "None or Incompatible Methods" option to Bypass; confirm auto enrollment is on in MFA policy |
| FIDO2 not completing on mobile or web | Registration or assertion fails with origin mismatch | FIDO2 relying party ID must exactly match the application's domain; check for scheme or path mismatches |
| Usernameless / passkey flow fails | Credential not found or user verification error | Set FIDO policy Discoverable Credentials = Required and User Verification = Required |
| Protect-licensed MFA conditions not visible | IP reputation, geovelocity, anonymous network conditions absent from MFA action condition list | Environment requires PingOne Protect or Passwordless license; verify service activation |
| Remember device unavailable in Singapore | Feature unavailable in Singapore region for PingOne Customer | Use DaVinci flow with explicit session management instead |
| MFA lockout settings not in MFA policy | Cannot find lockout threshold in MFA device policy | Lockout lives in Authentication > MFA Settings, not in the MFA device policy |
| Legacy FIDO2 devices fail on new MFA policy | Existing FIDO2 security key or biometrics users cannot authenticate | Run the FIDO2 legacy device migration before switching to the new MFA policy |
| Risk mitigations not auto-enforced | Risk policy recommends "block" but users are not blocked | Risk mitigations are advisory; wire the recommended action into DaVinci or auth policy conditions explicitly |

---

## Prerequisites

- PingOne environment with at minimum an Identity Authentication license
- Admin role: Environment Admin or Organization Admin
- For risk-based MFA conditions: PingOne Protect or Passwordless license activated on the environment
- For FIDO2: FIDO policy object created before assigning to MFA device policy
- For PingID push (Workforce): PingID service activated and adapter version 2.17+ (for Remember Me)

---

## Common variants

| Variant | Pattern |
|---|---|
| Workforce MFA (PingID push) | MFA device policy enables Mobile (PingID app) and Desktop (PingID app); method selection = "User selected default"; remember device up to 90 days |
| Customer CIAM MFA (low friction) | Email OTP or SMS OTP primary; FIDO2 optional; auto enrollment on; "None or Incompatible Methods" = Bypass with enrollment redirect |
| High-assurance CIAM | FIDO2 Required + User Verification Required; no SMS/voice as fallback; separate strict sign-on policy attached only to sensitive apps |
| Step-up for API resources | Basic policy on standard apps; strict policy (unconditional MFA) on API resource app; resource server checks `acr` claim and issues 401 challenge |
| Risk-adaptive MFA | Protect license required; MFA action conditioned on IP reputation / geovelocity / anonymous network; low-risk sessions skip MFA entirely |
| DaVinci orchestrated flow | Attach a DaVinci flow policy instead of a native sign-on policy; cannot coexist with native policies on same app |
| Registration policy (self-service sign-up) | Create a sign-on policy with a Login action; enable the "Enable Registration" checkbox; select the target population — users can self-register at sign-in time. Attach this policy to the registration application. Separate from the sign-in policy; attach each to its respective app. |
| Passwordless SMS OTP | Sign-on policy with a Multi-Factor Authentication action (no Login action); SMS method enabled in the MFA device policy; attach to the passwordless app; users authenticate with a one-time passcode delivered by SMS |

---

## Related references

- `references/curated/pingone-mt/tenant-and-environment-setup.md`
- `references/curated/cross-platform/policy-and-branding-basics.md`
- `references/curated/cross-platform/foundation-overview.md`

---

## Source

[PingOne authentication policies](https://docs.pingidentity.com/pingone/authentication/p1_authenticationpolicies.html)
[PingOne MFA device policies](https://docs.pingidentity.com/pingone/authentication/p1_mfa_policies.html)
[PingOne FIDO policies](https://docs.pingidentity.com/pingone/authentication/p1_fido_policies.html)
[PingOne step-up authentication for APIs](https://docs.pingidentity.com/pingone/authentication/p1_stepup_authentication_for_apis.html)
[PingOne Protect risk policies](https://docs.pingidentity.com/pingone/threat_protection_using_pingone_protect/p1_protect_risk_policies.html)
[Attach authentication policy to application](https://docs.pingidentity.com/pingone/applications/p1_apply_auth_policy_to_applications.html)
