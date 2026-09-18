# Researching a PingOne Verify integration

## Scope

Use this as a focused research brief for **PingOne Verify** identity-proofing integrations. Keep the service boundary explicit: Verify performs identity verification and records transaction outcomes; the host journey, flow, federation integration, API client, or mobile application owns the surrounding user experience and business response.

### Covers

- **Administrative/interface plane:** verification-policy ownership, supported channel, host integration, credentials, environment or tenant scope, and outcome visibility.
- **Runtime/client plane:** document and facial capture, liveness and comparison checks, transaction state, result handling, and the handoff to the host application or orchestration surface.

### Does NOT cover

- Tenant mutations, policy authoring, API or SDK code, request payloads, exact configuration values, secrets, or executable journeys and flows.
- Claims about supported documents, jurisdictions, policy fields, transaction states, quotas, or release behavior without checking current Verify documentation.
- A claim that a policy, credential, journey, flow, API client, or SDK is ready merely because another integration or environment is ready.

Treat this as orientation, not configuration authority. For implementation, use the linked product, API, connector, journey, and SDK documentation.

## Research brief

Research the integration as two related planes:

- **Administrative/interface plane:** identify the target PingOne environment or host product, user population, verification policy, launch channel, service identity or connector, regional endpoint, and monitoring or review responsibility. Confirm whether the design uses PingOne DaVinci, an AIC or self-managed PingAM journey, PingFederate, a REST API, or an iOS or Android SDK. These are different execution surfaces even when they invoke the same Verify service.
- **Runtime/client plane:** establish how the transaction starts, which document and live-capture steps are available, where capture occurs, how the host receives status and result information, and which application or journey branch interprets the outcome. A verification result is an input to an access, onboarding, or recovery decision; it is not by itself a universal approval or account action.

A common documented lifecycle is: select the intended verification policy and host surface; start a transaction; collect the supported document and facial or liveness evidence through the selected channel; evaluate the transaction; expose the documented result and audit information to the authorized host; and apply an application-specific next step. The exact checks, inputs, outcomes, and review behavior are surface- and release-sensitive.

## Resource index

### Verify and platform documentation

- [PingOne Verify overview](https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_start.html)
- [Verify introduction](https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_introduction.html)
- [Verify policies](https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_policies.html)
- [Verify transaction management](https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_managing_verification.html)
- [Verify API](https://developer.pingidentity.com/pingone-api/verify/introduction.html)
- [Verify transactions](https://developer.pingidentity.com/pingone-api/verify/verify-transactions.html)
- [Verified data](https://developer.pingidentity.com/pingone-api/verify/verified-data.html)
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [PingOne Platform documentation](https://docs.pingidentity.com/pingone/p1_cloud__platform_main_landing_page.md)

### Host and channel contexts

- [PingOne DaVinci reference](../pingone-davinci/README.md)
- [PingOne DaVinci documentation](https://docs.pingidentity.com/davinci/davinci_introduction.md)
- [PingOne Advanced Identity Cloud reference](../pingone-advanced-identity-cloud/README.md)
- [PingAM reference](../pingam/README.md)
- [PingFederate reference](../pingfederate/README.md)
- [Developer tools reference](../developer-tools/README.md)
- [Orchestration SDKs reference](../orchestration-sdks/README.md)

### Related composition example

- [Verified Trust help desk with PingOne](https://docs.pingidentity.com/solution-guides/verified-trust/verified-trust-helpdesk-pingone.html) — a documented PingOne and DaVinci composition using Verify for proofing.
- [Verified Trust help desk with Advanced Identity Cloud](https://docs.pingidentity.com/solution-guides/verified-trust/verified-trust-helpdesk-aic.html) — use to distinguish the AIC journey and Worker Service boundary.

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Product and platform boundary | Is the request for PingOne Verify in a PingOne environment, or for Verify invoked by AIC, self-managed PingAM, PingFederate, DaVinci, an API client, or a mobile app? | Stop and clarify an ambiguous host or deployment model. |
| Policy and readiness | Which verification policy, population, environment, channel, and review responsibility are in scope? | Check current policy, entitlement, supported document and jurisdiction coverage, and release. |
| Credentials and ownership | Which application, connector, journey service, or API client starts or reads the transaction, and where are its credentials managed? | Verify scopes, roles, endpoint region, rotation, and least-privilege requirements in current documentation. |
| Capture and runtime | Which document, facial, liveness, and transaction steps are available through the selected channel? | Check the current API, connector, journey, or SDK contract; distinguish documented fields from inference. |
| Outcome and business response | What status, result metadata, audit information, retry, or manual-review behavior is returned? Which host branch handles it? | Do not map a result to approval, denial, recovery, or provisioning without application-specific evidence. |
| Promotion and operations | What moves between environments, and what must be recreated or verified in the target? | Recheck policies, credentials, host bindings, endpoints, SDK versions, audit visibility, and drift. |

## Guardrails and report

Keep these distinctions visible:

- PingOne Verify is an identity-proofing service; PingOne DaVinci, AIC journeys, PingAM, PingFederate, APIs, and mobile SDKs are host or execution surfaces with their own boundaries.
- A DaVinci connector, a journey integration, a federation integration, a direct API client, and an SDK can have different credentials, input mappings, capture behavior, outcome handling, and promotion requirements.
- Document and biometric checks produce verification information; the host application or orchestration surface owns the business response unless the selected integration documents otherwise.
- Supported documents, jurisdictions, policy checks, transaction states, manual review, endpoints, and SDK behavior are release-sensitive or tenant-specific. Do not promote local examples into defaults.
- Do not treat an active journey or flow, a successful transaction response, or an installed SDK as proof that policy, credentials, capture channel, egress, and monitoring are production-ready.

Report: (1) the Verify and host-platform boundary; (2) administrative, policy, and credential readiness; (3) verified capture and transaction behavior; (4) application, journey, or flow outcome handling; (5) promotion, operations, and unresolved checks; (6) documented facts versus inference, tenant-specific observations, and release-sensitive claims; and (7) the appropriate handoff to the [PingOne Verify reference](./README.md), the selected host reference, [developer tools](../developer-tools/README.md), [orchestration SDKs](../orchestration-sdks/README.md), or current official documentation. Do not turn the report into a configuration runbook.
