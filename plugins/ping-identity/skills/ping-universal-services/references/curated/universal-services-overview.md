---
title: "Ping Universal Services — Overview"
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
  - admin
use_cases:
  - customer
  - workforce
  - cross-platform
doc_type: concept
status: current
canonical: true
last_updated: "2026-06-03"
slug: ""
---

# Ping Universal Services — Overview

Strategic services that are invoked from PingOne MT, PingOne ST (AIC), or Ping Software flows rather than administered as standalone products.

## Scope

Covers: what each Universal Service is, when to invoke this skill family vs adjacent skills, and a summary matrix of all six services with their typical flow placement.

Does NOT cover: detailed invocation syntax, platform-specific configuration steps, or service-by-service API reference — see `references/curated/service-invocation-patterns.md` and `references/curated/choosing-the-right-service.md` for those.

---

## What are Universal Services?

Universal Services are capabilities that sit above any single platform. They are:

- **Consumed from multiple platforms** — the same service (e.g., PingOne Protect) can be invoked from a DaVinci flow, an AIC journey node, or a PingFederate API call.
- **Not tied to a single admin surface** — you do not "administer" PingOne Protect in one console and then deploy it elsewhere; you configure the service once and reference it from whichever flow needs it.
- **Strategic value layers** — they add capabilities (risk scoring, identity proofing, credential issuance, governance, authorization, single sign-on) that are orthogonal to flow orchestration itself.

This is the key criterion that separates Universal Services from product-specific features:

> **If the capability is consumed from two or more platform families, it is a Universal Service.**

---

## The six Universal Services

| Service | What it does | Invoked from | Typical flow stage |
|---|---|---|---|
| **PingOne Protect** | Evaluates authentication risk using device signals, behavior analytics, IP reputation, and threat intelligence; returns a risk score and recommended action | PingOne MT (DaVinci), PingOne ST (AIC journey node), Ping Software (REST API) | Post-credential-collection, pre-MFA decision |
| **PingOne Verify** | Identity proofing — document capture, liveness check, and data match against a government-issued ID; returns a proofing outcome (VERIFIED / UNVERIFIED / REQUIRES_REVIEW) | PingOne MT (DaVinci), PingOne ST (AIC journey node) | Registration, step-up, high-assurance re-auth |
| **PingOne Credentials** | Issues, presents, and revokes W3C Verifiable Credentials bound to a PingOne user; integrates with digital wallet apps | PingOne MT (DaVinci), PingOne ST (AIC journey node) | Post-registration, credential exchange at relying party |
| **PingOne IGA** | Identity Governance and Administration — access requests, access reviews, role-based access, provisioning, and entitlement management | PingOne MT (Admin API, DaVinci), PingOne ST (AIC governance module) | Joiner/mover/leaver flows, periodic access certification |
| **PingOne Authorize** | Fine-grained, policy-based authorization — attribute-based access control (ABAC) policies evaluated at runtime; separates authorization logic from application code | PingOne MT (DaVinci connector, REST API), PingOne ST (AIC journey node), PingFederate (policy enforcement point) | Post-authentication, before resource access |
| **PingOne SSO** | Cross-application and cross-domain single sign-on; session management, token issuance (OIDC/SAML), and centralized logout | PingOne MT, PingOne ST, PingFederate | Entry point of every authenticated session |

---

## Skill selection: this skill vs adjacent skills

| Question | Correct skill |
|---|---|
| "Which platform should I use?" | `ping-quickstart` |
| "How do I set up my PingOne environment / register an app?" | `ping-foundation` |
| "How do I design a login journey or DaVinci flow (no specific service)?" | `ping-orchestration` |
| "How do I invoke Protect / Verify / Credentials / IGA / Authorize in my flow?" | `ping-universal-services` ← this skill |
| "How do I integrate an SDK / app with Ping?" | `ping-app-integration` |

The most common routing error is sending Universal Service questions to `ping-orchestration`. The deciding factor: if the question involves **a named Universal Service** (Protect, Verify, Credentials, IGA, Authorize, SSO as a cross-platform capability), route here.

---

## When to load multiple curated anchors

Load at most 3 curated anchors per interaction. Typical combinations:

| Scenario | Anchors to load |
|---|---|
| "Which service do I need?" | `universal-services-overview.md` + `choosing-the-right-service.md` |
| "How do I invoke Protect in DaVinci?" | `service-invocation-patterns.md` |
| "Can I use Verify in a PingFederate flow?" | `service-invocation-patterns.md` + `cross-platform-service-usage.md` |
| "Protect + Verify together in AIC" | `service-invocation-patterns.md` + `cross-platform-service-usage.md` |

---

## Licensing

Universal Services are individually licensed. SSO is included in every PingOne base license. All other services (Protect, Verify, Credentials, IGA, Authorize) require separate add-on licenses or SKUs purchased through Ping Identity. Licensing is tied to the PingOne organization, not to individual environments — a licensed service can be enabled in any environment within that organization.

Key licensing rules:
- A service that is licensed at the organization level must still be **enabled per environment** before flows in that environment can invoke it.
- DaVinci connector availability and AIC journey node availability are gating concerns for the orchestration layer, not for the Universal Services themselves — a service can be licensed even if DaVinci is not.
- PingOne IGA has a separate tenant provisioning step that goes beyond enabling a feature flag. Coordinate with Ping Identity support when provisioning IGA for the first time.

---

## Prerequisites

- A PingOne organization with at least one environment provisioned.
- The specific Universal Service (Protect, Verify, Credentials, IGA, Authorize) must be licensed and enabled in the environment before it can be invoked from a flow. SSO is included in the base PingOne license.
- Platform-specific prerequisites (DaVinci license, AIC tenant) apply to the orchestration layer, not to the Universal Services themselves.

---

## Common variants

- **Risk-gated identity proofing**: Protect evaluates risk first; if score exceeds threshold, Verify is invoked to confirm identity before allowing access.
- **Credential-gated access**: IGA grants entitlement; Credentials issues a verifiable credential encoding that entitlement; Authorize evaluates the credential at resource access time.
- **Federated SSO with adaptive access**: PingFederate handles SSO federation; PingOne Protect evaluates each authentication attempt; PingOne Authorize enforces resource-level policy.
- **Step-up re-verification**: A user with an active SSO session triggers a high-value transaction; Protect re-evaluates risk for the new event; if risk is elevated, Verify is invoked for document + liveness confirmation before the transaction proceeds.

---

## Failure modes and fallback behavior

Each Universal Service should be treated as a fallible external call. The recommended fallback policy per service:

| Service | Recommended fallback when unavailable |
|---|---|
| **Protect** | Treat as LOW risk (fail-open with logging); never block users on a risk-service outage |
| **Verify** | Route to manual review queue; do not silently deny the user |
| **Credentials** | Queue the issuance for retry; inform the user the credential will be issued shortly |
| **IGA** | Fail the access request with a clear error; do not grant access when IGA is unreachable |
| **Authorize** | Deny by default (fail-closed); an authorization outage must never result in unauthorized access |
| **SSO** | Surface the outage to the user; do not silently redirect to an error page with no explanation |

In chained patterns (e.g., Protect → Verify), the fallback policy of the first service determines whether the second is invoked. If Protect is unavailable and the fallback is LOW risk, the Verify step will not be triggered for high-risk events — plan for this gap explicitly in the flow design.

---

## Related references

- `references/curated/choosing-the-right-service.md`
- `references/curated/service-invocation-patterns.md`
- `references/curated/cross-platform-service-usage.md`

---

## Source

[PingOne Universal Services documentation](https://docs.pingidentity.com/pingone)
[PingOne Protect overview](https://docs.pingidentity.com/pingone/protect)
[PingOne Verify overview](https://docs.pingidentity.com/pingone/verify)
[PingOne Credentials overview](https://docs.pingidentity.com/pingone/credentials)
[PingOne Authorize overview](https://docs.pingidentity.com/pingone/authorize)
