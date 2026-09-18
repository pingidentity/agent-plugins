# Researching an AIC–PingOne Verify integration

## Scope

Use this as a focused research brief for **PingOne Advanced Identity Cloud (AIC)** and **PingOne Verify**. Research two planes without turning the result into an implementation guide:

- **Administrative/interface plane:** AIC and PingOne environment mapping, product-connection readiness, Verify policy and transaction ownership, Worker Service and realm scope, and journey placement.
- **Runtime/journey plane:** Verify Evaluation and Completion Decision behavior, capture and verification outcomes, retry or failure handling, and the handoff to the application or journey branch that consumes the result.

Confirm the target is AIC before researching. Do not combine AIC, PingOne multi-tenant, self-managed PingAM, or PingOne Recognize guidance without an explicit platform distinction.

## Research brief

Research only the topics relevant to the request:

- **Boundary:** target AIC tenant, environment, realm, user population, journey, verification policy, and intended business behavior. Distinguish identity proofing from AIC authentication and MFA.
- **Administrative readiness:** AIC-to-PingOne environment mapping, product-connection state, Verify entitlement and policy readiness, worker application or credential relationship, and environment-specific values.
- **AIC service scope:** identify the AIC administration surface, selected Worker Service or product connection, realm scope, secret or ESV handling, and connection status. Verify the current service and endpoint behavior in official documentation.
- **Journey topology:** establish how the Verify Evaluation and Completion Decision nodes are placed, how the transaction is started and completed, which outcomes are exposed, and where failure, retry, cancellation, or alternate branches go.
- **Runtime behavior:** identify the capture channel and client responsibility, the verification transaction and policy context, the data available to the journey, and the documented result consumed by the application or journey.
- **Promotion:** distinguish journey promotion from recreation or verification of target-environment product connections, policies, credentials, ESVs/secrets, endpoints, capture configuration, and monitoring.

Capture exact current claims with their supporting URLs. Label material findings as **documented**, **inferred**, **tenant-specific**, or **release-sensitive**; preserve conflicts instead of silently normalizing them.

## Resource index

### AIC integration and administration

- [AIC documentation index](https://docs.pingidentity.com/pingoneaic/llms.txt)
- [PingOne services integration](https://docs.pingidentity.com/pingoneaic/integrations/pingone.md)
- [Set up AIC environments](https://docs.pingidentity.com/pingoneaic/integrations/pingone-set-up-environments.html)
- [Set up product connections](https://docs.pingidentity.com/pingoneaic/integrations/pingone-set-up-product-connections.html)
- [PingOne Verify integration for AIC](https://docs.pingidentity.com/pingoneaic/integrations/pingone-verify.html)
- [AIC journeys](https://docs.pingidentity.com/pingoneaic/journeys/journeys.html)
- [AIC environments and promotion](https://docs.pingidentity.com/pingoneaic/tenants/environments-development-staging-production.html)
- [Self-service promotions](https://docs.pingidentity.com/pingoneaic/tenants/self-service-promotions.html)

### Verify and host surfaces

- [PingOne Verify reference](../pingone-verify/README.md)
- [Verify API and transaction documentation](https://developer.pingidentity.com/pingone-api/verify/introduction.html)
- [Verified Trust with Advanced Identity Cloud](https://docs.pingidentity.com/solution-guides/verified-trust/verified-trust-helpdesk-aic.html) — use as a composition example, not a general journey template.
- [Orchestration SDKs reference](../orchestration-sdks/README.md)
- [Developer tools reference](../developer-tools/README.md)

### Canonical AIC node references

- [PingOne Verify Evaluation node](https://docs.pingidentity.com/auth-node-ref/latest/pingone/pingone-verify-evaluation.html)
- [PingOne Verify Completion Decision node](https://docs.pingidentity.com/auth-node-ref/latest/pingone/pingone-verify-completion-decision.html)

Use the current AIC and node documentation for supported capture channels, transaction states, fields, and outcomes. Do not infer a runtime contract from the existence of a product connection or a successful test transaction.

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Platform boundary | Is this AIC, PingOne multi-tenant, or self-managed PingAM? What tenant, environment, realm, population, and journey are in scope? | Stop and clarify ambiguity. |
| Environment and product connection | Which AIC environment maps to which PingOne environment? Is the product connection present and owned in the target environment? | Verify each environment and current product-connection behavior; do not assume promotion carries the connection. |
| Worker and credentials | Which Worker Service, worker application, credential, endpoint, secret, or ESV is used, and what is its realm/environment scope? | Confirm current AIC service behavior, authorization, rotation, and least-privilege requirements. |
| Verify policy and transaction | Which Verify policy, population, capture channel, transaction, and review responsibility are in scope? | Check current Verify support, geography, entitlement, policy, and release. |
| Journey topology | How do Verify Evaluation and Completion Decision participate in the journey? Which success, failure, timeout, cancellation, retry, or alternate outcomes are documented? | Check the canonical node references and the target AIC release; do not copy local field names or outcome spellings as defaults. |
| Host and capture boundary | Does capture occur in a hosted page, browser, mobile application, API client, or another supported surface? Which component owns callbacks, permissions, and user experience? | Verify the selected channel and SDK/API contract; keep client implementation out of this brief. |
| Result and business response | What verification result or metadata is exposed to the journey or host, and what branch consumes it? | A verification result does not by itself authenticate, authorize, provision, or approve a business action. |
| Promotion and operations | What moves between environments, and what must be recreated or checked? | Recheck journeys, product connections, policies, credentials, ESVs/secrets, capture setup, endpoints, load-test planning, audit visibility, and drift. |

## Guardrails and report

Keep these distinctions visible in the findings:

- PingOne Verify is an identity-proofing service. AIC journeys are the host orchestration surface, while the application, browser, mobile client, or API owns the selected capture and user-experience responsibilities.
- AIC authentication and MFA are separate from Verify. Do not substitute Verify for native AIC MFA, and do not add PingOne MFA merely because a Verify integration uses a PingOne product connection.
- PingOne Recognize is a separate biometric product boundary. Do not infer Recognize support from an AIC Verify integration or treat the products as synonyms.
- Environment mapping, product-connection readiness, Worker Service or credential readiness, Verify policy readiness, and journey activation are separate dependencies. A successful test does not prove production readiness.
- Promotion of a journey does not by itself promote target-environment connections, policies, credentials, ESVs/secrets, capture configuration, endpoint access, or monitoring.
- Prefer current official AIC integration and canonical node references over conflicting tutorials or local examples. Do not promote local thresholds, field names, shared-state names, or status spellings into defaults.

Report: (1) the AIC and Verify boundary; (2) environment, product-connection, worker, policy, and credential readiness; (3) verified Evaluation and Completion Decision behavior; (4) capture and host handling; (5) promotion, operations, and unresolved checks; (6) documented facts versus inference, tenant-specific observations, and release-sensitive claims; and (7) the appropriate handoff to the implementation sources.
