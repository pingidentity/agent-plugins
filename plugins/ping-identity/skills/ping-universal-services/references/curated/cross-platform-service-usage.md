---
title: "Cross-Platform Universal Service Usage Rules"
product_family: cross-platform
products:
  - pingone-protect
  - pingone-verify
  - pingone-credentials
  - pingone-authorize
  - pingone-iga
  - pingfederate
  - pingaccess
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

# Cross-Platform Universal Service Usage Rules

Availability constraints, anti-patterns, service chaining patterns, and API versioning differences when using Ping Universal Services across PingOne (multi-tenant cloud), AIC, and Ping Software Suite.

## Scope

Covers: platform-support matrix, known constraints per platform and per service, anti-patterns to avoid, service chaining patterns (Protect + Verify, IGA + Authorize, Verify + Credentials), and API versioning differences between PingOne (multi-tenant cloud) and AIC.

Does NOT cover: step-by-step invocation syntax — see `references/curated/service-invocation-patterns.md`. Does NOT cover which service to select — see `references/curated/choosing-the-right-service.md`.

---

## Platform-support matrix

| Service | PingOne (multi-tenant cloud) (DaVinci) | AIC | PingFederate | PingAccess | PingDirectory |
|---|---|---|---|---|---|
| **Protect** | Native connector | Native journey node | REST API (custom adapter required) | No native support | No |
| **Verify** | Native connector | Native journey node | REST API (custom adapter required) | No native support | No |
| **Credentials** | Native connector | Native journey node | REST API (custom adapter required) | No native support | No |
| **IGA** | Native connector; governance UI in PingOne admin | Governance module in AIC | No native integration | No | No |
| **Authorize** | Native connector | Native journey node | Policy enforcement point (dedicated Authorize integration) | Policy enforcement point | No |
| **SSO** | Native (PingOne OIDC/SAML app registration) | Native (AIC OAuth2/SAML service) | Primary use case (federation hub) | Reverse proxy / access control | Partial (directory backend for federation) |

Legend:
- **Native connector / node** — a supported, pre-built integration; no custom code required.
- **REST API** — the service API is callable but the integration point is custom-built.
- **Policy enforcement point** — PingFederate or PingAccess acts as PEP; PingOne Authorize acts as PDP.
- **No native support** — the service cannot be invoked from this platform without a custom integration that is outside normal supported patterns.

---

## Known constraints by platform

### PingOne (multi-tenant cloud) (DaVinci)

- **Protect**: The DaVinci connector requires the PingOne Protect JavaScript SDK to be embedded in the user-facing application to collect device signals. Without the SDK, the risk evaluation runs with reduced signal fidelity (IP and network signals only).
- **Verify**: The Verify connector initiates a transaction and returns a transaction ID. The user must complete verification on a mobile device. DaVinci flows must implement a **polling loop** (using the Loop connector or recursive sub-flow) to check transaction status; there is no push callback to DaVinci.
- **IGA**: IGA is not intended for real-time login flows. The IGA connector is suited for asynchronous provisioning and access-request flows, not for evaluating entitlements during a sub-second login transaction. Use Authorize for runtime entitlement enforcement.
- **Credentials**: Credential issuance requires the user to have a compatible digital wallet installed on their device. The DaVinci flow must handle the case where the user does not have a wallet (branch to an enrollment or download step).

### AIC

- **Protect**: The `_pingProtect` context object must be collected by the AIC tree's client-side script node before the Protect Evaluation node runs. If the client script fails to execute (e.g., the browser blocks JavaScript), the Protect node receives no device signals and may fall back to a default risk level.
- **Verify**: The Verify node has a `Waiting` outcome that the journey designer must explicitly handle. Failing to wire the `Waiting` outcome to a polling or waiting page results in users being dropped to the `Error` outcome prematurely.
- **Authorize**: The PingOne Authorize Evaluation node in AIC requires the Authorize service to be configured with the AIC tenant's `client_id` as a trusted caller. This configuration is done in the PingOne Authorize admin console, not in AIC.
- **IGA**: IGA governance in AIC is administered through the AIC governance module UI. API calls from journey nodes are supported but require a service account with IGA-specific scopes.

### Ping Software Suite (PingFederate / PingAccess)

- **General**: All Universal Service calls from Ping Software are REST API calls; there are no pre-built adapters. Integration requires a custom IDP adapter (PingFederate) or a custom rule (PingAccess).
- **Protect**: PingFederate does not have a Protect SDK for server-side signal collection. Risk evaluations from PingFederate are network-signal-only unless the user-facing application embeds the Protect JavaScript SDK independently.
- **Verify**: PingFederate-initiated Verify flows require a browser redirect to a hosted verification page or a deep link to the user's mobile device. Coordinating this within PingFederate's adapter model requires a stateful session pattern.
- **Authorize**: PingFederate can act as a policy enforcement point calling PingOne Authorize as the policy decision point using the standard OAuth 2.0 token introspection or a custom policy action. PingAccess can enforce Authorize decisions at the resource endpoint level.

---

## Anti-patterns to avoid

| Anti-pattern | Why it is wrong | Correct pattern |
|---|---|---|
| Invoking Verify twice in the same flow for the same user | Creates two competing transactions; the second may fail or conflict with the first; doubles user friction unnecessarily | Invoke Verify once; store the `transactionId` and outcome in the user's session; check the stored outcome on subsequent flow entries |
| Using Protect without a signal aggregation step | Risk evaluation with no device signals produces LOW risk scores for all requests, rendering the evaluation meaningless | Embed the Protect JS/mobile SDK in the user-facing app; ensure `_pingProtect` is populated before the Protect node/connector runs |
| Treating IGA as a real-time enforcement mechanism | IGA access reviews and provisioning are asynchronous and governance-oriented; invoking IGA in a sub-second login transaction introduces latency and fragile timing dependencies | Use PingOne Authorize for runtime enforcement; use IGA for entitlement lifecycle management |
| Ignoring the `REQUIRES_REVIEW` outcome from Verify | Users whose verification requires manual review are silently failed or looped indefinitely | Wire the `REQUIRES_REVIEW` / `Waiting` outcome to a notification step and a holding page; provision a manual review workflow |
| Calling Authorize with stale token attributes | Authorize evaluates the attributes present in the token or the request at decision time; stale attributes lead to incorrect permit/deny decisions | Ensure the attributes passed to Authorize are refreshed at the time of access, not cached from initial login |
| Hardcoding the Protect risk threshold in flow logic | Hardcoded thresholds bypass the Protect policy engine and must be changed by updating the flow itself | Use the recommendation value returned by Protect (`ALLOW`, `CHALLENGE`, `BLOCK`) rather than comparing numeric scores; let the Protect policy control the thresholds |
| Using SSO session management as an authorization mechanism | An active SSO session proves authentication; it does not prove the user is authorized to access the requested resource | Combine SSO with Authorize; the SSO session establishes identity; Authorize enforces resource-level policy |

---

## Service chaining patterns

### Pattern 1: Protect + Verify (risk-gated identity proofing)

Use when: a high-risk authentication event should trigger identity re-verification.

```
Flow:
  1. Collect credentials (username + password)
  2. Invoke Protect  →  evaluate risk
     ├─ LOW / ALLOW     →  proceed to application
     ├─ MEDIUM / CHALLENGE  →  invoke MFA (ping-orchestration concern)
     └─ HIGH / BLOCK    →  invoke Verify
  3. (HIGH branch) Invoke Verify  →  document + liveness
     ├─ APPROVED        →  allow with step-up assurance, update Protect risk signal
     ├─ DECLINED        →  block session, notify user
     └─ REQUIRES_REVIEW →  hold session, trigger manual review
```

Notes:
- The Protect `BLOCK` threshold is configured in the Protect risk policy, not in the flow.
- The Verify outcome should update the user's Protect risk signal store (`VERIFIED` signal) to reduce future risk scores for the same user on trusted devices.

---

### Pattern 2: Verify + Credentials (progressive identity assurance)

Use when: completing identity proofing should result in the issuance of a verifiable credential.

```
Flow:
  1. Invoke Verify  →  document + liveness
     ├─ APPROVED        →  proceed to credential issuance
     └─ DECLINED / ERROR  →  end with error
  2. (APPROVED branch) Invoke Credentials  →  issue verifiable credential
     - Credential type encodes: verified name, DOB, document type, issuer DID, expiry
     - Credential is bound to the user's PingOne identity
     - Wallet deep-link or QR code presented to user
```

Notes:
- The credential issued encodes the identity assurance level (`IAL2` for government-ID + liveness).
- Subsequent relying parties can verify the credential without re-invoking Verify.

---

### Pattern 3: IGA + Authorize (entitlement lifecycle + runtime enforcement)

Use when: entitlements are managed by IGA governance workflows and enforced at resource access time by Authorize.

```
Lifecycle (asynchronous — IGA):
  1. User requests access to resource R via IGA access request workflow
  2. Approver certifies the request
  3. IGA provisions the entitlement to the user's PingOne profile
     (e.g., sets custom attribute: canAccess_R = true)

Runtime (synchronous — Authorize):
  1. Authenticated user attempts to access resource R
  2. API gateway calls Authorize decision API
     - Input: user token attributes (including canAccess_R), resource identifier, request context
  3. Authorize evaluates ABAC policy:
     ├─ canAccess_R == true AND user.department == "Finance"  →  PERMIT
     └─ otherwise  →  DENY
```

---

## API versioning differences between PingOne (multi-tenant cloud) and AIC

PingOne (multi-tenant cloud) and AIC share the same underlying PingOne platform APIs for Universal Services (Protect, Verify, Credentials, Authorize). However, there are differences in:

| Dimension | PingOne (multi-tenant cloud) | AIC |
|---|---|---|
| **Protect API version** | v1 (stable) | v1 (same endpoint) |
| **Verify API version** | v1 (stable) | v1 (same endpoint) |
| **Journey node vs DaVinci connector version** | DaVinci connector version is managed in the DaVinci connector library; updates are pushed by Ping | AIC node version is tied to the AIC release train; updated with AIC version upgrades |
| **Token format passed to Authorize** | PingOne access token (JWT); claims populated by DaVinci flow | AIC `id_token` or scripted session attribute map; mapped to Authorize input |
| **Device signal collection** | Protect JS SDK embedded in the application; signals sent to PingOne endpoint | `_pingProtect` context object collected by an AIC client-side script node; same underlying Protect endpoint |
| **Polling for Verify result** | DaVinci loop connector polls `GET /v1/environments/{envId}/users/{userId}/verifyTransactions/{transactionId}` | AIC `Polling Wait` node re-enters the Verify journey node; same underlying API |

---

## Prerequisites

- A PingOne organization with the relevant Universal Service(s) licensed and provisioned.
- For chained service patterns: each service in the chain must be independently configured before the chain is assembled.
- For Ping Software REST integration: a service account OAuth 2.0 client with the required scopes for each service API.
- Network connectivity from PingFederate / PingAccess servers to PingOne API endpoints (`api.pingone.com`, `api.pingone.eu`, `api.pingone.ca`, etc.) on port 443.

---

## Common variants

- **Multi-environment chaining**: A PingOne DaVinci flow calling a Verify service configured in a separate PingOne environment (e.g., a shared services environment). Supported, but the flow connector must reference the service environment's `environmentId`.
- **Fallback when a service is unavailable**: Each Universal Service call should include a timeout and a fallback outcome. The recommended fallback policy: Protect unavailable → treat as LOW risk; Verify unavailable → route to manual review; Authorize unavailable → deny by default (fail-closed).
- **Audit trail correlation**: Each service invocation returns a unique transaction/evaluation ID. Store these IDs in the user's session and in audit logs to correlate risk evaluations, verification outcomes, and authorization decisions across services.

---

## Related references

- `references/curated/universal-services-overview.md`
- `references/curated/choosing-the-right-service.md`
- `references/curated/service-invocation-patterns.md`

---

## Source

[PingOne Protect developer guide](https://docs.pingidentity.com/pingone/protect)
[PingOne Verify developer guide](https://docs.pingidentity.com/pingone/verify)
[PingOne Authorize developer guide](https://docs.pingidentity.com/pingone/authorize)
[PingOne IGA developer guide](https://docs.pingidentity.com/pingone/iga)
[AIC journey node reference](https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html)
[DaVinci connector library](https://docs.pingidentity.com/davinci/connectors)
