---
title: "Choosing the Right Ping Universal Service"
product_family: cross-platform
products:
  - pingone-protect
  - pingone-verify
  - pingone-credentials
  - pingone-authorize
  - pingone-iga
  - pingone-davinci
  - pingone-aic
capabilities:
  - universal-services
services:
  - protect
  - verify
  - credentials
  - iga
  - authorize
  - sso
audience:
  - architect
  - developer
use_cases:
  - customer
  - workforce
  - cross-platform
doc_type: reference
status: current
canonical: true
last_updated: "2026-06-03"
slug: ""
---

# Choosing the Right Ping Universal Service

Decision guide for matching a stated requirement to the correct Universal Service before loading invocation patterns.

## Scope

Covers: intent-to-service mapping, disambiguation between services that are commonly confused (Verify vs MFA, Protect vs Authorize, IGA vs Authorize), and a matrix of which services are available on each platform.

Does NOT cover: how to configure or invoke a service once selected — see `references/curated/service-invocation-patterns.md` for that.

---

## Intent-to-service mapping

| User intent / requirement | Correct service | Key differentiator |
|---|---|---|
| "Detect that this login attempt is risky and challenge the user" | **PingOne Protect** | Evaluates signals to produce a risk score; does not verify identity |
| "Block or allow based on device posture, IP, or behavior" | **PingOne Protect** | Signal aggregation + risk policy engine |
| "Verify that the user is who they claim to be using a government ID" | **PingOne Verify** | Document capture + liveness; produces a proofing outcome |
| "Check identity before high-value account action" | **PingOne Verify** | Step-up verification, not just authentication |
| "Issue a digital wallet credential after a user completes KYC" | **PingOne Credentials** | W3C Verifiable Credential issuance bound to a PingOne user |
| "Let a user present a credential to a relying party" | **PingOne Credentials** | Credential presentation and revocation |
| "Manage who has access to what, request access, certify entitlements" | **PingOne IGA** | Governance lifecycle: joiner/mover/leaver, access reviews, entitlement management |
| "Provision or deprovision accounts across downstream systems" | **PingOne IGA** | Provisioning connectors and joiner/mover/leaver workflows |
| "Enforce fine-grained access rules based on attributes at resource access time" | **PingOne Authorize** | ABAC policy evaluation; separated from the authentication flow |
| "Control which API endpoint a user can call based on role and context" | **PingOne Authorize** | Policy enforcement point (PEP) + policy decision point (PDP) |
| "Let a user sign in once and access multiple applications" | **PingOne SSO** | Cross-app session management, OIDC/SAML token issuance |

---

## Disambiguation: commonly confused pairs

### Verify vs MFA

| Dimension | PingOne Verify | MFA (second factor) |
|---|---|---|
| **Purpose** | Confirm a user's real-world identity against a government-issued document | Add a second authentication factor to confirm the user knows/has something |
| **Evidence collected** | Photo ID (passport, driver's license) + selfie liveness check | OTP, push notification, hardware key, biometric (device-side) |
| **Result** | VERIFIED / UNVERIFIED / REQUIRES_REVIEW (identity assurance) | Pass / Fail (authentication step completion) |
| **When to invoke** | At registration for KYC/AML compliance, or at step-up for high-value actions | Every login session as part of the standard authentication policy |
| **Replaces MFA?** | No. Verify establishes identity assurance; MFA provides ongoing authentication factors | No. MFA does not establish the user's real-world identity |
| **Correct skill** | `ping-universal-services` | `ping-orchestration` (the MFA step is a journey/flow design concern) |

**Rule**: If the task involves capturing a photo of an ID document or running a liveness check, the answer is Verify. If the task involves OTP, push, TOTP, or FIDO2 as a login factor, it is MFA and belongs in `ping-orchestration`.

---

### Protect vs Authorize

| Dimension | PingOne Protect | PingOne Authorize |
|---|---|---|
| **When it runs** | During authentication, on the authentication event | After authentication, on the resource-access request |
| **Input** | Device signals, behavioral analytics, IP reputation, threat intel | User attributes, resource attributes, environment context, entitlements |
| **Output** | Risk score (LOW / MEDIUM / HIGH) + recommended action | Permit / Deny + optional obligations |
| **Policy model** | Risk policies (thresholds, predictors, overrides) | ABAC / XACML-style policies managed in PingOne Authorize |
| **Typical placement** | Post-credential-collection, pre-MFA decision | At API gateway or resource server, post-authentication |

**Rule**: Protect asks "is this authentication event suspicious?"; Authorize asks "is this authenticated user allowed to access this specific resource with these attributes?"

---

### IGA vs Authorize

| Dimension | PingOne IGA | PingOne Authorize |
|---|---|---|
| **Focus** | Who has access to what (entitlement lifecycle) | Whether to grant access right now (runtime decision) |
| **Operates on** | Access requests, certifications, roles, provisioning | Attributes, policies, tokens at access time |
| **Result** | Entitlement granted or revoked (provisioning action) | Permit or Deny (runtime enforcement) |
| **Human in the loop?** | Often — access reviews, approvals | No — fully automated policy evaluation |

**Rule**: IGA manages the lifecycle of access rights. Authorize enforces those rights at runtime. Both can be used together: IGA determines who is entitled; Authorize enforces the entitlement at resource access time.

---

## Platform support matrix

For the full platform-support matrix (including PingAccess column, connector vs REST API distinctions, and legend) see `references/curated/cross-platform-service-usage.md`.

---

## Decision flowchart (text form)

1. Is the user completing an **authentication event** and the question is about event-level risk? → **Protect**
2. Is the user being asked to **prove their real-world identity** with a document? → **Verify**
3. Is a **digital credential** (W3C VC) being issued or presented? → **Credentials**
4. Is the question about **who is entitled to access what** over time (access requests, reviews, provisioning)? → **IGA**
5. Is the question about **enforcing a policy at resource access time** based on attributes? → **Authorize**
6. Is the question about **maintaining a session across applications** or token issuance? → **SSO**
7. None of the above and involves flow/journey design without a named service? → `ping-orchestration`
8. None of the above and involves platform setup? → `ping-foundation`

---

## Prerequisites

- The intended service must be licensed for the target PingOne organization.
- For Protect: at least one authentication policy must exist to attach the risk evaluation to.
- For Verify: the PingOne Verify service must be enabled in the environment; the mobile SDK or web component must be deployed to the user-facing app.
- For Credentials: a PingOne Credentials-enabled digital wallet flow must be configured.
- For IGA: the IGA module must be provisioned for the environment; identity correlation must be configured.
- For Authorize: a policy store must be configured in PingOne Authorize; the enforcement point (API gateway, DaVinci node, or AIC node) must be connected to the Authorize service.

---

## Common variants

- **Protect + Verify together**: Risk-gated identity proofing — Protect evaluates risk first; if risk is MEDIUM or HIGH, Verify is invoked to re-establish identity assurance before continuing.
- **IGA + Authorize together**: Entitlement lifecycle and runtime enforcement — IGA manages who is granted access; Authorize evaluates that entitlement at resource access time.
- **Verify + Credentials together**: Progressive identity assurance — Verify confirms real-world identity; Credentials issues a verifiable credential encoding that assurance for use at relying parties.

---

## Related references

- `references/curated/universal-services-overview.md`
- `references/curated/service-invocation-patterns.md`
- `references/curated/cross-platform-service-usage.md`

---

## Source

[PingOne Protect product page](https://docs.pingidentity.com/pingone/protect)
[PingOne Verify product page](https://docs.pingidentity.com/pingone/verify)
[PingOne Credentials product page](https://docs.pingidentity.com/pingone/credentials)
[PingOne Authorize product page](https://docs.pingidentity.com/pingone/authorize)
[PingOne IGA product page](https://docs.pingidentity.com/pingone/iga)
