# Researching a PingFederate–PingOne Verify integration

## Scope

Use this as a focused research brief for **PingFederate** as a host surface for **PingOne Verify** identity-proofing transactions. Verify performs document and biometric verification and records transaction outcomes; PingFederate and the integrating application or flow retain responsibility for the surrounding federation transaction, authentication policy, and business response.

### Covers

- **Administrative/interface plane:** PingFederate deployment and transaction boundary, PingOne Verify environment and policy ownership, supported launch channel, service identity or connector, endpoint and credential scope, and promotion or review responsibilities.
- **Runtime/transaction plane:** verification launch, document and facial capture, liveness or comparison checks, transaction status and result handling, and the handoff back to the PingFederate authentication or application path.

### Does NOT cover

- Tenant mutations, policy-authoring procedures, API or SDK code, request payloads, exact configuration values, secrets, executable journeys or flows, or PingFederate adapter installation steps.
- AIC journeys, self-managed PingAM, PingOne DaVinci, direct REST clients, or native mobile SDK implementation. Those are separate host or execution boundaries with their own documentation.
- A claim that identity verification automatically authenticates a user, performs MFA, authorizes an application, provisions an account, or approves a business transaction.
- Claims about supported documents, jurisdictions, capture channels, transaction states, manual review, or release behavior without checking current Verify and PingFederate documentation.

Treat this as orientation, not configuration authority. Confirm the current PingOne Verify, PingFederate, and selected channel documentation for the target release, region, and population.

## Research brief

Research two connected planes:

- **Administrative/interface plane:** identify the PingFederate deployment and federation or authentication transaction, the PingOne Verify environment and verification policy, the population and region, the PingOne Verify Integration Kit for PingFederate, the service identity or connector, the credential and secret boundary, and the owner of policy and review operations. Confirm the documented kit and release boundary rather than assuming that a generic Verify API, SDK, or flow is interchangeable with the PingFederate path. The presence of a Verify policy or PingFederate connection in one environment does not establish readiness in another.
- **Runtime/transaction plane:** determine how the IdP Adapter starts the transaction, where mobile-web or Verify Mobile SDK v2 capture occurs, what transaction and user context is available, how status and result information return through the PingFederate Authentication API or supported widget, and which authentication-policy or application branch interprets success, failure, retry, or manual review. A verification result is evidence for a host decision; it is not by itself a universal authentication or approval result.

A common documented lifecycle is: select the supported Verify policy and PingFederate Integration Kit path; invoke the IdP Adapter during registration or sign-on; present the supported mobile-web or Mobile SDK v2 challenge; evaluate the transaction; expose the documented status through the PingFederate Authentication API or supported widget; and continue, retry, review, or stop according to the PingFederate transaction and application contract. The current kit documentation identifies PingFederate 11.3 or newer and regional PingOne API and authorization endpoint requirements; exact adapter, callback, capture, status, and failure behavior remains release-sensitive.

## Resource index

### Verify administration and runtime

- [PingOne Verify overview](https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_start.html)
- [Verify introduction](https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_introduction.html)
- [Verify policies](https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_policies.html)
- [Verify transaction management](https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_managing_verification.html)
- [PingOne Verify Integration Kit for PingFederate](https://docs.pingidentity.com/integrations/pingone/pingone_verify_integration_kit/pf_p1_verify_ik.html)
- [Verify API](https://developer.pingidentity.com/pingone-api/verify/introduction.html)
- [Verify reference](../pingone-verify/README.md)
- [Generic Verify integration research](../pingone/blueprint-integrating-pingone-verify.md)

### PingFederate host and handoffs

- [PingFederate reference](README.md)
- [PingFederate IdP adapters](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf_managing_idp_adapters.html)
- [PingFederate authentication policies](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf_authentication_policies.html)
- [Single sign-on and federation use cases](../single-sign-on-use-cases/README.md)
- [Developer tools reference](../developer-tools/README.md)

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Host and product boundary | Which PingFederate deployment, protocol, authentication transaction, population, and PingOne Verify environment are in scope? Is Verify invoked by a documented PingFederate path or by a separate application/flow? | Stop and clarify an ambiguous host or platform. Do not transfer AIC, PingAM, DaVinci, API, or SDK assumptions to PingFederate. |
| Policy and administrative readiness | Which Verify policy, entitlement, region, capture channel, review responsibility, PingFederate binding, and application owner are required? | Verify supported documents, jurisdictions, channel, policy, release, and tenant configuration in current documentation. |
| Credentials and network | Which service identity, connector, API client, adapter, endpoint, certificate, and outbound network path starts or reads the transaction? | Verify scopes, roles, endpoint region, rotation, certificate trust, firewall rules, and least-privilege requirements. |
| Capture and runtime | Which document, facial, liveness, comparison, and transaction steps are available through the selected channel? Where are they rendered? | Check the current Verify and host contract; distinguish documented fields, statuses, callbacks, and UI behavior from inference. |
| Result and policy handoff | What status, result metadata, audit information, retry, failure, or manual-review outcome reaches PingFederate? Which authentication-policy or application branch handles it? | Identity verification is not sign-on MFA or authorization. Confirm the host mapping for every terminal outcome. |
| Promotion and operations | What policies, bindings, credentials, endpoints, capture assets, review settings, and audit evidence move or must be recreated? | Recheck environment-specific values, secrets, endpoint reachability, SDK or channel versions, privacy controls, monitoring, and drift. |

## Guardrails and report

Keep these distinctions visible:

- PingOne Verify is an identity-proofing service; PingFederate is a federation and authentication-policy host. Neither boundary should be collapsed into a generic “verification equals authentication” claim.
- Verify policies, transactions, capture channels, credentials, PingFederate bindings, and application responses are distinct components. A successful capture or transaction response does not prove that the host policy or federation flow is ready.
- A direct API client, DaVinci flow, AIC or PingAM journey, native SDK, and PingFederate-hosted path can have different credentials, inputs, capture behavior, callback contracts, and promotion requirements.
- Supported documents, jurisdictions, policy checks, transaction states, manual review, endpoint behavior, and host integration details are release-sensitive or tenant-specific. Do not promote local examples into defaults.
- Do not treat an active policy, successful test transaction, configured binding, or installed client as proof that credentials, egress, capture, privacy, review, monitoring, and terminal-result handling are production-ready.

Report: (1) the PingFederate transaction, Verify environment, policy, population, and host/channel boundary; (2) verified administrative, policy, credential, network, and capture readiness; (3) documented transaction and result behavior; (4) PingFederate authentication-policy or application handling for success, failure, retry, and review; (5) promotion, operations, privacy, and unresolved checks; (6) documented facts versus inference, tenant-specific observations, and release-sensitive claims; and (7) the appropriate handoff to the [PingFederate reference](README.md), [PingOne Verify reference](../pingone-verify/README.md), [single sign-on and federation use cases](../single-sign-on-use-cases/README.md), [developer tools](../developer-tools/README.md), or current official documentation. Do not turn the report into a configuration or policy-authoring runbook.
