# Researching a PingAM–PingOne Protect integration

## Scope

Use this as a focused research brief for **self-managed PingAM** and **PingOne Protect**. Keep it separate from Advanced Identity Cloud: both can expose Protect authentication nodes, but their administration, service, realm, release, and promotion boundaries are not interchangeable.

### Covers

- **Administrative/interface plane:** PingAM-to-PingOne connection, PingOne environment and Worker application readiness, Worker Service and secret scope, realm and journey ownership, Protect policy readiness, and promotion checks.
- **Runtime/client plane:** Protect Signals initialization, evaluation inputs and outcomes, risk-based journey routing, recommended mitigation or step-up behavior, client/service errors, and terminal Result feedback.

### Does NOT cover

- Tenant mutations, API/CLI/Terraform commands, SDK code, exact environment IDs, client secrets, endpoint values, node configuration values, or executable authentication journeys.
- Advanced Identity Cloud product-connection, Worker Service, or journey administration. Use the AIC-specific blueprint and product skill for that platform.
- A claim that an AM realm, Worker Service, active journey, or connected PingOne environment is production-ready without verifying the target release and tenant.

Treat this as orientation, not a PingAM configuration runbook. Use the current PingAM and authentication-node references for implementation details.

## Research brief

Research two related planes:

- **Administrative/interface plane:** confirm the self-managed AM deployment and release, target realm, PingOne organization/environment, Protect entitlement and policy, Worker application and role, secret-store boundary, Worker Service configuration, regional endpoints, and the journey that owns the transaction. The documented PingAM prerequisite is a connection from AM to PingOne before creating a Protect journey. A Worker application belongs to a PingOne environment; a Worker Service is realm-scoped in AM. Treat those as separate dependencies.
- **Runtime/client plane:** the documented Protect node lifecycle is Initialize → Evaluation → Result. Initialize makes the client-side Signals collection available; Evaluation sends client and authentication-event data to Protect and receives risk information; the journey uses the outcomes to select its path; Result can update the in-progress evaluation or report terminal transaction outcome where supported. The exact placement, outcome set, shared state, and client callback behavior are release-sensitive.

The Evaluation node reference documents risk-level, score-threshold, recommended-action, failure, and client-error branches, but the branch names and precedence must be checked against the target node release. A journey can use those results to require stronger authentication or another mitigation; that response is journey design, not a universal Protect decision. Do not infer that a successful node evaluation means the client, policy, realm service, and terminal feedback are all healthy.

## Resource index

### PingAM and Protect integration

- [PingAM Protect integration](https://docs.pingidentity.com/pingam/latest/integrations/pingone-protect.md)
- [Connect PingAM to PingOne](https://docs.pingidentity.com/pingam/latest/integrations/connect-am-to-pingone.html)
- [Protect Initialize node](https://docs.pingidentity.com/auth-node-ref/latest/pingone/pingone-protect-initialize.html)
- [Protect Evaluation node](https://docs.pingidentity.com/auth-node-ref/latest/pingone/pingone-protect-evaluation.html)
- [Protect Result node](https://docs.pingidentity.com/auth-node-ref/latest/pingone/pingone-protect-result.html)
- [PingOne Protect overview](https://docs.pingidentity.com/pingone/threat_protection_using_pingone_protect/p1_protect_overview.html)
- [PingOne Protect API](https://developer.pingidentity.com/pingone-api/protect/introduction.html)
- [PingOne Signals SDK](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-risk-sdks/risk_evaluation_sdk.html)

### Local handoffs and platform boundary

- [PingAM reference](README.md)
- [PingOne Protect reference](../pingone-protect/README.md)
- [Developer tools handoff](../developer-tools/README.md)
- [AIC Protect blueprint](../pingone-advanced-identity-cloud/blueprint-integrating-pingone-protect.md) — compare platform boundaries only.

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Platform boundary | Is this self-managed PingAM, AIC, or another host? Which AM release, realm, journey, population, and transaction are in scope? | Stop and clarify ambiguity before applying node guidance. |
| AM-to-PingOne readiness | Which PingOne environment and Worker application are used? Which Worker Service, secret store, region, and realm hold the connection? | Verify role, secret label, endpoints, connection status, and realm scope in the target release. |
| Protect readiness | Is Protect entitled and configured with the policy, predictors, and monitoring needed for this population? | Check target tenant and policy; do not infer from AM connection success. |
| Journey topology | How are Initialize, Evaluation, and Result arranged, and what client callback or nested-journey constraints apply? | Use canonical node references; check placement and release-specific outcomes. |
| Runtime | What user, device, event, external-device, and session context is available? What risk or recommended-action result is returned? | Distinguish documented node inputs/outputs from journey-specific mappings. |
| Decision and feedback | Which outcomes route to normal authentication, step-up, mitigation, failure, or client-error handling? When is Result sent? | Verify outcome precedence, terminal feedback, retries, and error semantics. |
| Promotion and operations | What moves between AM environments or realms, and what must be recreated or verified? | Recheck secrets/ESVs, Worker Service, journey bindings, node versions, Protect policy, egress, and audit visibility. |

## Guardrails and report

Keep these distinctions visible:

- Self-managed PingAM and Advanced Identity Cloud are different platforms. Similar Initialize/Evaluation/Result names do not imply identical service configuration, promotion, or runtime behavior.
- PingOne Protect readiness, the PingOne Worker application, the AM Worker Service, the AM secret store, and the authentication journey are separate dependencies with different scopes.
- Evaluation risk and recommended-action results inform journey routing; they do not inherently perform step-up, account recovery, or authorization changes.
- Score thresholds, policy selection, shared-state keys, callback behavior, error statuses, and node outcome precedence are release-sensitive or tenant-specific. Prefer canonical node references over local examples.
- Promotion of a journey does not prove that target-realm secrets, services, product entitlements, Protect policies, client versions, endpoints, or egress are ready.

Report: (1) the self-managed AM boundary and realm scope; (2) verified PingOne, Worker Service, secret, and Protect readiness; (3) documented Initialize/Evaluation/Result behavior; (4) journey routing, step-up, failure, client-error, and terminal feedback handling; (5) promotion, operations, and unresolved checks; (6) facts versus inference, tenant-specific observations, and release-sensitive claims; and (7) the appropriate handoff to the [PingAM reference](README.md), [PingOne Protect reference](../pingone-protect/README.md), canonical node documentation, or [developer tools](../developer-tools/README.md). Do not turn the report into a journey configuration runbook.
