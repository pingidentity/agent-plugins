---
title: "Universal Service Invocation Patterns"
product_family: cross-platform
products:
  - pingone-protect
  - pingone-verify
  - pingone-credentials
  - pingone-authorize
  - pingone-iga
  - pingone-davinci
  - pingone-aic
  - pingfederate
  - pingaccess
capabilities:
  - universal-services
  - orchestration
services:
  - protect
  - verify
  - credentials
  - iga
  - authorize
audience:
  - developer
  - architect
use_cases:
  - customer
  - workforce
  - cross-platform
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-01"
slug: ""
---

# Universal Service Invocation Patterns

How each Ping Universal Service is invoked from PingOne MT (DaVinci), PingOne ST / AIC (journey nodes), and Ping Software (PingFederate / PingAccess REST API calls).

## Scope

Covers: invocation mechanisms, configuration artifacts, typical placement in the authentication or access flow, and the handoff pattern (how a service returns a result and how the flow branches on it). Also notes which services require an additional license or separate tenant configuration.

Does NOT cover: which service to select for a given requirement — see `references/curated/choosing-the-right-service.md`. Does NOT cover platform availability constraints — see `references/curated/cross-platform-service-usage.md`.

---

## PingOne MT — DaVinci flow connectors

DaVinci flows invoke Universal Services through **connectors** — pre-built integration units configured in the DaVinci connector library. Each connector maps to one service. A connector instance is configured once per environment and reused across flows.

| Service | Invocation mechanism | Config artifact | Typical placement in flow |
|---|---|---|---|
| Protect | PingOne Protect connector | Connector configuration references the PingOne Protect policy ID; the flow passes the user's device profile and session context | After credential collection (username + password), before MFA decision |
| Verify | PingOne Verify connector | Connector references the Verify transaction policy; the flow passes the user's PingOne user ID | At registration or step-up; before granting access to high-assurance resources |
| Credentials | PingOne Credentials connector | Connector references the credential type; the flow passes the verified user identity | After successful Verify or as a post-registration step |
| IGA | PingOne IGA connector | Connector uses the IGA API; the flow passes the user ID and the requested entitlement | In provisioning or access-request flows; not typically in real-time login flows |
| Authorize | PingOne Authorize connector | Connector references the policy name and the enforcement point; the flow passes user attributes and the requested resource | After authentication, before redirecting to the application |

### DaVinci result handoff

DaVinci connectors return a JSON result object. The flow uses **branch conditions** to evaluate the result:

```
Protect result object:
  riskEvaluationId  — unique ID for this evaluation
  result.level      — LOW | MEDIUM | HIGH
  result.recommendation.value  — ALLOW | CHALLENGE | BLOCK

Flow branch condition: result.level == "HIGH"  →  challenge branch
                       result.level != "HIGH"  →  allow branch
```

```
Verify result object:
  transactionId      — unique ID
  status             — VERIFICATION_SUBMITTED | IN_PROGRESS | APPROVED | DECLINED | REQUIRES_REVIEW
  verificationData   — extracted document fields (name, DOB, etc.)

Flow branch condition: status == "APPROVED"   →  verified branch
                       status == "DECLINED"   →  decline / fallback branch
                       status == "REQUIRES_REVIEW"  →  manual review branch
```

```
Authorize result object:
  decision           — PERMIT | DENY
  obligations        — array of obligations (e.g., step-up required)

Flow branch condition: decision == "PERMIT"  →  allow branch
                       decision == "DENY"    →  deny branch
```

---

## PingOne ST / AIC — Journey nodes

AIC journeys invoke Universal Services through **journey nodes** — server-side tree nodes installed in the AIC journey engine. Each service has a dedicated node or set of nodes.

| Service | Invocation mechanism | Config artifact | Typical placement in journey |
|---|---|---|---|
| Protect | PingOne Protect Evaluation node | Node config references the Protect risk policy ID; the node reads the client-side `_pingProtect` context object collected by the Protect SDK | After `Platform Username` and `Platform Password` nodes, before MFA |
| Verify | PingOne Verify node (or PingOne Verify Registration node) | Node config references the Verify transaction policy; inputs the current user's PingOne subject | At end of registration tree or in a step-up sub-journey |
| Credentials | PingOne Credentials Issuance node | Node config references the credential type and issuance policy | After identity verification is complete; near end of registration |
| IGA | PingOne IGA connector (scripted or dedicated node where available) | API call using the IGA REST API; requires service account credentials in a secret store | In provisioning journeys; not in real-time login journeys |
| Authorize | PingOne Authorize Evaluation node | Node config references the policy store name and decision point URL | After authentication success, in a step-up or resource-access sub-journey |

### AIC journey result handoff

AIC nodes route flow execution through **outcomes** — named exit connections from a node. The journey designer connects each outcome to the next node or leaf (success / failure).

```
Protect node outcomes:
  Allow         — risk level within policy thresholds
  Challenge     — risk level triggers step-up MFA
  Deny          — risk level exceeds block threshold
  Failure       — service call failed (treat as Allow or soft-fail per policy)

Verify node outcomes:
  Verified      — proofing approved
  Not Verified  — proofing declined
  Expired       — transaction timed out
  Error         — service error
  Waiting       — user has not yet completed the mobile verification step

Authorize node outcomes:
  Permit        — policy permits access
  Deny          — policy denies access
  Indeterminate — policy could not be evaluated (treat as Deny)
```

The `Waiting` outcome on the Verify node is important: the journey must poll or provide a waiting page while the user completes the verification on their mobile device. A common pattern is a `Polling Wait` node that re-enters the Verify node every N seconds.

---

## Ping Software Suite — REST API invocation

PingFederate and PingAccess do not have native connectors to PingOne Universal Services. Invocation requires an explicit REST API call, typically from:
- A custom adapter in PingFederate (Java-based IDP adapter or authentication selector)
- A PingAccess rule / agent policy that calls an external service
- A custom policy script within PingFederate's policy contract

| Service | Invocation mechanism | Config artifact | Typical placement |
|---|---|---|---|
| Protect | HTTP POST to PingOne Protect Risk Evaluation API | Service account client credentials stored in PingFederate credential vault; REST API URL configured in adapter | Custom authentication adapter, after credential validation |
| Verify | HTTP POST to PingOne Verify API to create a transaction; poll for result | Service account credentials; Verify transaction policy ID | Custom adapter or HTML Form adapter with redirect to Verify mobile flow |
| Credentials | HTTP POST to PingOne Credentials API to issue a credential | Service account credentials; credential type ID | Post-authentication policy action |
| Authorize | HTTP POST to PingOne Authorize decision API | Authorize endpoint URL; client credentials | PingAccess policy rule or PingFederate post-authentication mapping |

### REST API result handoff for PingFederate / PingAccess

PingFederate routes are determined by **authentication policy contracts** — the API response is parsed and mapped to contract attributes. A policy step evaluates the mapped attribute and routes to the appropriate authentication path.

```
Protect REST response (abbreviated):
  POST /v1/environments/{envId}/riskEvaluations
  →  { "result": { "level": "LOW|MEDIUM|HIGH", "recommendation": { "value": "ALLOW|CHALLENGE|BLOCK" } } }
  PingFederate maps: result.recommendation.value  →  policy contract attribute  →  policy branch condition

Authorize REST response (abbreviated):
  POST /environments/{envId}/decisions
  →  { "decision": "PERMIT|DENY", "obligations": [...] }
  PingAccess maps: decision  →  allow or deny rule outcome
```

---

## Licensing and tenant configuration notes

| Service | Additional license required? | Additional tenant config required? |
|---|---|---|
| Protect | Yes — PingOne Protect must be enabled for the environment | Risk policies must be configured before a flow can reference them |
| Verify | Yes — PingOne Verify must be provisioned for the environment | Verify transaction policies (document types, liveness settings) must be configured |
| Credentials | Yes — PingOne Credentials must be enabled | Credential types and issuance policies must be defined |
| IGA | Yes — PingOne IGA is a separately licensed module | IGA instance must be provisioned and correlated with the PingOne environment |
| Authorize | Yes — PingOne Authorize must be enabled | Policy store, decision point, and enforcement point must be configured |
| SSO | No — included in the base PingOne license | No additional tenant config beyond standard application registration |

---

## Prerequisites

- A PingOne organization with the target environment provisioned.
- The Universal Service licensed and enabled in that environment (see table above).
- For DaVinci: a DaVinci license and at least one DaVinci flow created in the environment.
- For AIC: a PingOne ST (AIC) tenant and access to the journey designer.
- For Ping Software REST calls: a service account with an OAuth 2.0 client credential grant in PingOne; network access from PingFederate/PingAccess to PingOne API endpoints.
- PingOne Protect requires the Protect JavaScript SDK (or mobile SDK) to be included in the user-facing application to collect device signals before the flow invokes the risk evaluation.

---

## Common variants

- **Silent risk evaluation**: Protect is invoked without presenting any UI to the user; the flow branches silently based on the risk score.
- **Async identity proofing (AIC)**: The Verify node transitions to the `Waiting` outcome; a `Polling Wait` node loops back every 5 seconds; the journey completes once the outcome changes to `Verified` or `Not Verified`.
- **Policy-driven step-up**: Authorize returns a `CHALLENGE_REQUIRED` obligation; the flow invokes MFA before re-evaluating the Authorize decision.
- **Multi-step service chain**: Protect → (if MEDIUM/HIGH) → Verify → (if APPROVED) → Credentials issuance, all within a single DaVinci flow or AIC journey.

---

## Related references

- `references/curated/universal-services-overview.md`
- `references/curated/choosing-the-right-service.md`
- `references/curated/cross-platform-service-usage.md`

---

## Source

[PingOne DaVinci connector library](https://docs.pingidentity.com/davinci/connectors)
[PingOne Protect API reference](https://apidocs.pingidentity.com/pingone/platform/v1/api/#post-create-risk-evaluation)
[PingOne Verify API reference](https://apidocs.pingidentity.com/pingone/verify/v1/api/)
[PingOne Authorize API reference](https://apidocs.pingidentity.com/pingone/authorize/v1/api/)
[AIC journey node reference](https://docs.pingidentity.com/pingone-st/journey-nodes)
