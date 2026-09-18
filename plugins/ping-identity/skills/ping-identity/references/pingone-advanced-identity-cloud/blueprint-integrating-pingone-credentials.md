# Researching an AIC–PingOne Credentials integration

## Scope

Use this as a focused research brief for **PingOne Advanced Identity Cloud (AIC)** and **PingOne Credentials**. Research two planes without turning the result into an implementation guide:

- **Administrative/interface plane:** AIC and PingOne environment mapping, product-connection readiness, credential and issuer ownership, Worker Service and realm scope, and journey placement.
- **Runtime/journey plane:** wallet discovery and pairing, credential issue/update/revoke/verification lifecycle, transaction outcomes, and the handoff to the wallet or application that consumes the result.

Confirm the target is AIC before researching. Keep PingOne Credentials, PingOne Neo, wallet applications, and self-managed PingAM as distinct product or platform boundaries.

## Research brief

Research only the topics relevant to the request:

- **Boundary:** target AIC tenant, environment, realm, user population, journey, credential scenario, wallet, and intended business behavior. Distinguish issuer-side credential management from wallet-side storage, presentation, and application use.
- **Administrative readiness:** AIC-to-PingOne environment mapping, product-connection state, credential and issuer readiness, worker application or credential relationship, and environment-specific values.
- **AIC service scope:** identify the AIC administration surface, selected Worker Service or product connection, realm scope, secret or ESV handling, and connection status. Verify current service and endpoint behavior in official documentation.
- **Journey topology:** establish how Find Wallets, Pair Wallet, Delete Wallet, Issue, Update, Revoke, and Verification nodes participate in the journey; what precedes or follows them; and which success, failure, cancellation, retry, or alternate outcomes are documented.
- **Runtime and wallet boundary:** identify what the journey requests from the wallet, what the wallet or client must render or approve, which credential transaction state is returned, and where the application or journey consumes the result. Wallet SDK and API implementation belong to their owning references.
- **Promotion:** distinguish journey promotion from recreation or verification of target-environment product connections, issuer and credential resources, wallet configuration, credentials, ESVs/secrets, endpoints, and monitoring.

Capture exact current claims with their supporting URLs. Label material findings as **documented**, **inferred**, **tenant-specific**, or **release-sensitive**; preserve conflicts instead of silently normalizing them.

## Resource index

### AIC integration and administration

- [AIC documentation index](https://docs.pingidentity.com/pingoneaic/llms.txt)
- [PingOne services integration](https://docs.pingidentity.com/pingoneaic/integrations/pingone.md)
- [Set up AIC environments](https://docs.pingidentity.com/pingoneaic/integrations/pingone-set-up-environments.html)
- [Set up product connections](https://docs.pingidentity.com/pingoneaic/integrations/pingone-set-up-product-connections.html)
- [PingOne Credentials integration for AIC](https://docs.pingidentity.com/pingoneaic/integrations/pingone-credentials.html)
- [AIC journeys](https://docs.pingidentity.com/pingoneaic/journeys/journeys.html)
- [AIC environments and promotion](https://docs.pingidentity.com/pingoneaic/tenants/environments-development-staging-production.html)
- [Self-service promotions](https://docs.pingidentity.com/pingoneaic/tenants/self-service-promotions.html)

### Credentials, wallet, and host surfaces

- [PingOne Credentials reference](../pingone-credentials/README.md)
- [PingOne Neo reference](../pingone-neo/README.md)
- [PingOne Credentials API](https://developer.pingidentity.com/pingone-api/credentials/introduction.html)
- [PingOne wallet native SDKs](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-neo-native-sdks/pingone-wallet-native-sdks.html)
- [Developer tools reference](../developer-tools/README.md)
- [Orchestration SDKs reference](../orchestration-sdks/README.md)

### Canonical AIC node references

- [PingOne Credentials node overview](https://docs.pingidentity.com/auth-node-ref/latest/pingone/pingone-cred-overview.html)

Use the current AIC and node documentation for supported wallet types, credential states, fields, outcomes, and client behavior. Do not infer a runtime contract from the existence of a product connection or a successfully created issuer resource.

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Platform boundary | Is this AIC, PingOne multi-tenant, self-managed PingAM, PingOne Credentials, PingOne Neo, or a wallet application? What tenant, environment, realm, population, and journey are in scope? | Stop and clarify ambiguity. |
| Environment and product connection | Which AIC environment maps to which PingOne environment? Is the product connection present and owned in the target environment? | Verify each environment and current product-connection behavior; do not assume promotion carries the connection. |
| Worker and credentials | Which Worker Service, worker application, credential, endpoint, secret, or ESV is used, and what is its realm/environment scope? | Confirm current AIC service behavior, authorization, rotation, and least-privilege requirements. |
| Issuer and credential readiness | Which issuer, credential model, credential profile, wallet registration, notification, and monitoring responsibilities are in scope? | Verify entitlement, issuer state, credential lifecycle, wallet compatibility, and environment-specific readiness. |
| Journey topology | How do Find Wallets, Pair Wallet, Delete Wallet, Issue, Update, Revoke, and Verification participate in the journey? Which outcomes and prerequisites are documented? | Check the canonical node reference and target AIC release; do not copy local field names or outcome spellings as defaults. |
| Wallet and host boundary | Which wallet or client receives, stores, presents, or approves the credential operation? Which component owns callbacks and user experience? | Verify the selected wallet/API/SDK contract; keep wallet implementation out of this brief. |
| Credential lifecycle | Is the requested operation discovery, pairing, issuance, update, revocation, or verification? What state and terminal result are returned? | Do not infer presentation, trust, storage, revocation, or business approval semantics beyond the selected current documentation. |
| Promotion and operations | What moves between environments, and what must be recreated or checked? | Recheck journeys, product connections, issuer and credential resources, wallet bindings, credentials, ESVs/secrets, notifications, endpoints, audit visibility, load-test planning, and drift. |

## Guardrails and report

Keep these distinctions visible in the findings:

- PingOne Credentials is an issuer-side digital-credential service. AIC journeys provide the host orchestration surface; wallet applications and PingOne Neo have separate runtime and product boundaries.
- AIC authentication, MFA, and SSO are separate native capabilities. Do not add a PingOne MFA or PingOne SSO integration merely because Credentials uses a PingOne product connection.
- Environment mapping, product-connection readiness, Worker Service or credential readiness, issuer and credential resources, wallet readiness, and journey activation are separate dependencies. A successful issue or verification test does not prove production readiness.
- Promotion of a journey does not by itself promote target-environment connections, issuer resources, credential profiles, wallet bindings, credentials, ESVs/secrets, notifications, endpoint access, or monitoring.
- Direct API, connector, wallet SDK, and AIC journey paths can have different credentials, inputs, lifecycle behavior, and promotion requirements. Do not combine them into one execution contract.
- Prefer current official AIC integration and canonical node references over conflicting tutorials or local examples. Do not promote local field names, shared-state names, status spellings, wallet assumptions, or trust semantics into defaults.

Report: (1) the AIC and Credentials issuer/wallet boundary; (2) environment, product-connection, worker, issuer, credential, and wallet readiness; (3) verified node and credential lifecycle behavior; (4) wallet and host handling; (5) promotion, operations, load-test, and unresolved checks; (6) documented facts versus inference, tenant-specific observations, and release-sensitive claims; and (7) the appropriate handoff to implementation references.
