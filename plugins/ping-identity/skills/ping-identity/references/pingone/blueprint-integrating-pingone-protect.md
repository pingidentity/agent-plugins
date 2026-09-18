# Researching a PingOne–PingOne Protect integration

## Scope

Use this as a focused research brief for the **PingOne multi-tenant platform** and **PingOne Protect**. Keep the platform boundary explicit: this brief is for Protect capabilities administered as part of a PingOne organization and environment, with an optional PingOne DaVinci orchestration path.

### Covers

- **Administrative/interface plane:** organization and environment scope, Protect entitlement and readiness, risk predictors and policies, application or connector ownership, and promotion or drift checks.
- **Runtime/client plane:** Signals collection, direct Protect API or DaVinci connector evaluation, risk outcomes, application-controlled step-up or mitigation, and terminal feedback or observability.

### Does NOT cover

- Tenant mutations, policy authoring, API/CLI/Terraform commands, SDK code, exact environment values, secrets, request payloads, or executable DaVinci flows.
- Advanced Identity Cloud, self-managed PingAM, or PingFederate configuration. Those products have separate integration boundaries and handoffs.
- A claim that a PingOne environment, Protect policy, DaVinci flow, client SDK, or API credential is ready merely because another environment or integration is ready.

Treat this as orientation, not configuration authority. For implementation, use the linked product, API, connector, and SDK documentation.

## Research brief

Research the integration as two related planes:

- **Administrative/interface plane:** establish the target organization, environment, population, application or DaVinci flow, Protect entitlement, risk-policy ownership, service credentials, regional endpoints, and monitoring responsibility. Confirm whether the design uses native PingOne orchestration, the DaVinci Protect connector, or a direct Protect API/Signals SDK integration. These are different execution surfaces even when they evaluate the same Protect service.
- **Runtime/client plane:** identify when the client can collect Signals, what identity and event context is available, where the risk evaluation occurs, and which application or orchestration branch interprets the result. A risk result is an input to an access decision; it is not by itself a universal allow, deny, MFA, or account-recovery action.

A common documented lifecycle is: configure Protect predictors and policies; collect available device, network, identity, and transaction signals; submit an evaluation through the chosen surface; interpret the returned risk information; apply an application-specific mitigation or step-up; and report or retain the terminal outcome where the selected integration supports feedback. The exact inputs, outcomes, and feedback contract are surface- and release-sensitive.

## Resource index

### PingOne and Protect administration

- [PingOne platform documentation](https://docs.pingidentity.com/pingone/p1_cloud__platform_main_landing_page.md)
- [PingOne Protect overview](https://docs.pingidentity.com/pingone/threat_protection_using_pingone_protect/p1_protect_overview.html)
- [PingOne Protect API](https://developer.pingidentity.com/pingone-api/protect/introduction.html)
- [Create a risk evaluation](https://developer.pingidentity.com/pingone-api/protect/risk-evaluations/create-risk-evaluation.html)
- [PingOne Protect connector](https://docs.pingidentity.com/connectors/p1_protect_connector.html)

### Client and orchestration surfaces

- [PingOne Signals SDK](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-risk-sdks/risk_evaluation_sdk.html)
- [PingOne DaVinci documentation](https://docs.pingidentity.com/pingone-davinci/home.md)
- [PingOne Protect reference](../pingone-protect/README.md)
- [PingOne DaVinci reference](../pingone-davinci/README.md)
- [PingOne API handoff](api.md)
- [Developer tools handoff](../developer-tools/README.md)

### Boundary references

- [AIC Protect integration](https://docs.pingidentity.com/pingoneaic/integrations/pingone-protect.html) — use only to distinguish AIC service and journey behavior.
- [PingAM Protect integration](https://docs.pingidentity.com/pingam/latest/integrations/pingone-protect.md) — use only to distinguish self-managed AM behavior.
- [PingFederate Protect Integration Kit](https://docs.pingidentity.com/integrations/pingone/pingone_protect_integration_kit/pf_p1_protect_ik.html) — use only for the federation-product path.

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Platform boundary | Which organization, environment, population, application, and region are in scope? Is the request native PingOne, DaVinci, or direct API/SDK? | Stop when the target is AIC, self-managed AM, or PingFederate instead. |
| Protect readiness | Is Protect entitled and enabled? Which predictors, policies, staging data, and monitoring responsibilities apply? | Check target environment and release; do not infer readiness from another environment. |
| Credentials and ownership | Which application, connector, or service identity submits evaluations, and where are secrets managed? | Verify scopes, roles, region, rotation, and least-privilege requirements in current docs. |
| Runtime | Which Signals, identity, device, and event data are available at evaluation time? What risk information is returned? | Check the selected API, connector, or SDK contract; distinguish documented fields from inference. |
| Decision and feedback | How does the application or flow map risk to step-up, mitigation, retry, deny, or allow? Is terminal feedback supported? | Treat thresholds and action mappings as policy- and tenant-specific. |
| Promotion and operations | What moves between environments, and what must be recreated or verified? | Recheck policies, credentials, connector/flow bindings, SDK versions, endpoints, audit visibility, and drift. |

## Guardrails and report

Keep these distinctions visible:

- PingOne is the multi-tenant platform; PingOne Protect is a reusable threat-protection service within it. DaVinci is an orchestration surface, not a replacement for the Protect service or a second tenant boundary.
- A direct API/Signals SDK integration, a DaVinci connector, and a native PingOne flow can have different credentials, input mappings, outcome handling, and promotion requirements.
- Risk predictors and policies produce evaluation information; the host application or orchestration flow owns the business response unless the selected integration documents otherwise.
- Policy thresholds, recommended mitigations, SDK behavior, regional endpoints, and feedback status values are release-sensitive or tenant-specific. Do not promote local examples into defaults.
- Do not treat an active flow, a successful API response, or an installed SDK as proof that Protect policy, egress, credentials, and monitoring are production-ready.

Report: (1) the platform and execution-surface boundary; (2) administrative and credential readiness; (3) verified Signals/evaluation behavior; (4) application or flow decision and feedback handling; (5) promotion, operations, and unresolved checks; (6) documented facts versus inference, tenant-specific observations, and release-sensitive claims; and (7) the appropriate handoff to the [PingOne Protect reference](../pingone-protect/README.md), [PingOne API handoff](api.md), [DaVinci reference](../pingone-davinci/README.md), or current official documentation. Do not turn the report into a configuration runbook.
