# Researching an AIC–PingOne Protect integration

## Scope

Use this as a focused research brief for **PingOne Advanced Identity Cloud (AIC)** and **PingOne Protect**. Research two planes without turning the result into an implementation guide:

- **Administrative/interface plane:** environment mapping, Protect readiness, the AIC product connection and Worker Service, realm scope, and journey topology.
- **Runtime/client plane:** Signals/Protect initialization, evaluation inputs and outcomes, mitigation or step-up behavior, and terminal feedback.

Confirm the target is AIC before researching. Do not combine AIC, PingOne multi-tenant, or self-managed PingAM guidance without an explicit platform distinction.

## Research brief

Research only the topics relevant to the request:

- **Boundary:** target tenant, environment, realm, user population, journey, and intended behavior; distinguish AIC from PingOne multi-tenant and self-managed PingAM.
- **Administrative readiness:** AIC-to-PingOne environment mapping, Protect readiness, product-connection state, worker application or credential relationship, documented egress/allowlisting, and environment-specific values.
- **AIC service scope:** the responsible AIC administration surface, PingOne Worker Service realm, current authentication and endpoint behavior, secret/ESV handling, and connection status.
- **Journey topology:** availability and current behavior of Initialize, Evaluation, and Result; placement restrictions; nested-journey use; activation/preview; and all relevant success, failure, threshold, mitigation, client-error, and step-up branches.
- **Runtime behavior:** client initialization and acknowledgement, evaluation inputs, risk and mitigation precedence, callback/error behavior, and Result feedback on terminal paths.
- **Promotion:** source and target environments, realm scope, journey configuration, ESVs/secrets, service and product-connection objects, Protect policy readiness, and configuration drift.

Capture exact current claims with their supporting URLs. Label material findings as **documented**, **inferred**, **tenant-specific**, or **release-sensitive**; preserve conflicts instead of silently normalizing them.

## Resource index

Use the relevant entries as research starting points; the available skill, Docs MCP, or web retrieval determines how they are consulted.

### AIC integration and administration

- [AIC documentation index](https://docs.pingidentity.com/pingoneaic/llms.txt)
- [PingOne services integration](https://docs.pingidentity.com/pingoneaic/integrations/pingone.md)
- [Set up AIC environments](https://docs.pingidentity.com/pingoneaic/integrations/pingone-set-up-environments.html)
- [Set up product connections](https://docs.pingidentity.com/pingoneaic/integrations/pingone-set-up-product-connections.html)
- [PingOne Protect integration](https://docs.pingidentity.com/pingoneaic/integrations/pingone-protect.html)
- [AIC service configuration](https://docs.pingidentity.com/pingoneaic/am-reference/services-configuration.html)
- [PingOne Worker Service](https://docs.pingidentity.com/pingoneaic/am-reference/pingone-worker-service.html)

### Journeys, promotion, and boundary checks

- [AIC journeys](https://docs.pingidentity.com/pingoneaic/journeys/journeys.html)
- [Authentication nodes and journeys](https://docs.pingidentity.com/pingoneaic/am-authentication/auth-nodes-and-journeys.html)
- [Configure authentication journeys](https://docs.pingidentity.com/pingoneaic/am-authentication/configure-authentication-trees.html)
- [Authentication-node index](https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html)
- [AIC environments](https://docs.pingidentity.com/pingoneaic/tenants/environments-development-staging-production.html)
- [Self-service promotions](https://docs.pingidentity.com/pingoneaic/tenants/self-service-promotions.html)
- [PingAM Protect integration](https://docs.pingidentity.com/pingam/latest/integrations/pingone-protect.md) — use only to distinguish self-managed behavior.

### Canonical Protect and node references

- [Initialize node](https://docs.pingidentity.com/auth-node-ref/latest/pingone/pingone-protect-initialize.html)
- [Evaluation node](https://docs.pingidentity.com/auth-node-ref/latest/pingone/pingone-protect-evaluation.html)
- [Result node](https://docs.pingidentity.com/auth-node-ref/latest/pingone/pingone-protect-result.html)
- [PingOne Protect overview](https://docs.pingidentity.com/pingone/threat_protection_using_pingone_protect/p1_protect_overview.html)
- [PingOne Protect API](https://developer.pingidentity.com/pingone-api/protect/introduction.html)

## Research matrix

Use only the rows needed for the question. Do not assume a value is universal because it appears in a local playbook or example.

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Platform boundary | Is this AIC, PingOne multi-tenant, or self-managed PingAM? What tenant, environment, realm, and user population are in scope? | Stop and clarify ambiguity. |
| Environment and Protect readiness | How are AIC and PingOne environments related? What Protect, worker-application, credential, policy, or egress prerequisites are documented? | Check target environment, permissions, and release. |
| Product connection and Worker Service | What is managed by the AIC product connection versus the realm-scoped Worker Service? How are authentication, endpoints, secrets/ESVs, and connection status represented? | Check realm and environment scope. |
| Journey topology | What do Initialize, Evaluation, and Result require? Where may they be placed, and how do their documented outcomes connect? | Check canonical node reference, activation, preview, and nested-journey behavior. |
| Runtime | When are client signals, identity, device, and event inputs available? What are the documented risk, mitigation, error, step-up, and terminal-feedback behaviors? | Check client and tenant version; distinguish inference from documentation. |
| Promotion | What moves between environments, and what must be recreated or verified in the target? | Check target realm, ESVs/secrets, service objects, product connection, and Protect policy. |

## Guardrails and report

Keep these distinctions visible in the findings:

- Protect readiness, a PingOne worker application or credential, the AIC product connection, and the AIC Worker Service are separate dependencies; verify which are managed together and which are not.
- A worker application is associated with a PingOne environment, while the Worker Service is realm-scoped in AIC. Configuration in one realm or environment does not imply configuration in another.
- Initialization, evaluation, and result are a lifecycle. A journey being active or previewable does not prove client, policy, credential, or egress readiness.
- Promotion does not by itself prove that target-environment ESVs, secrets, services, product connections, or Protect policies are ready.
- Prefer current canonical node and administration references over conflicting tutorials or local examples. Do not promote local thresholds, field names, shared-state names, or status spellings into defaults.

Report: (1) the platform boundary and concise finding; (2) administrative readiness; (3) verified journey/runtime behavior; (4) promotion and unresolved checks; (5) facts versus inference or tenant-specific observations; and (6) the appropriate handoff. Stop when the requested planes are supported; do not turn the answer into a configuration runbook.
