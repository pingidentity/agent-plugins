# Researching a PingOne DaVinci integration

## Scope

Use this as a focused research brief for **PingOne DaVinci** orchestration integrations. Keep the product boundary explicit: DaVinci composes identity and access journeys from flows, nodes, connectors, applications, and policies; the connected Ping product or external service remains responsible for its own configuration and runtime contract.

### Covers

- **Administrative/interface plane:** tenant and environment scope, flow and version ownership, connector and connection configuration, application or policy launch surface, and promotion or monitoring responsibility.
- **Runtime/application plane:** how a flow is launched, how nodes and connectors exchange variables and outcomes, which UI or API surface renders the interaction, and how the host handles completion or failure.

### Does NOT cover

- Tenant mutations, executable flow definitions, connector-specific payloads, API commands, SDK code, exact environment values, secrets, or provider-specific policy authoring.
- Claims about connector availability, supported providers, flow limits, variable scope, protocol behavior, or release-sensitive features without checking current DaVinci documentation.
- A claim that a flow, application, connector, connection, or policy is ready merely because another environment or flow is ready.

Treat this as orientation, not configuration authority. For implementation, use the linked DaVinci, connector, product, API, and SDK documentation.

## Research brief

Research the integration as two related planes:

- **Administrative/interface plane:** identify the DaVinci tenant and environment, flow and version, connector and connection objects, application or flow policy, launch pattern, user population, credentials, and operational ownership. Confirm whether the application uses a redirect, widget, API, OIDC, SAML 2.0, or an orchestration SDK surface. These surfaces can expose different responsibilities even when they invoke the same flow.
- **Runtime/application plane:** establish how the host starts and continues the flow, which inputs and variables are collected, how nodes branch on connector or operator outcomes, how errors and retries are represented, and where the final result is consumed. A flow outcome is not automatically an authentication decision, account change, provisioning action, or risk mitigation unless the configured flow and host contract establish that behavior.

A common documented lifecycle is: configure reusable connections and connectors; compose and version a flow; expose an allowed flow through an application or policy; launch it through the selected surface; collect inputs and invoke nodes; interpret success, failure, and completion outcomes; and retain or act on the result in the host application. Exact node behavior, variable names, connector inputs, and result contracts are flow- and release-sensitive.

## Resource index

### DaVinci documentation

- [PingOne DaVinci documentation](https://docs.pingidentity.com/davinci/davinci_introduction.md)
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [PingOne DaVinci reference](./README.md)

### Host and service contexts

- [PingOne Platform reference](../pingone/README.md)
- [PingOne Verify reference](../pingone-verify/README.md)
- [PingOne Protect reference](../pingone-protect/README.md)
- [PingOne MFA reference](../pingone-mfa/README.md)
- [Orchestration SDKs reference](../orchestration-sdks/README.md)
- [Developer tools reference](../developer-tools/README.md)

### Documented composition example

- [Verified Trust help desk with PingOne](https://docs.pingidentity.com/solution-guides/verified-trust/verified-trust-helpdesk-pingone.html) — a PingOne SSO, DaVinci, and Verify composition; use it as an example of boundaries, not as a general flow template.
- [PingOne for Customers Plus reference](../pingone-for-customers-plus/README.md) — a solution/flow-pack handoff, not a substitute for current DaVinci documentation.

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Product and tenant boundary | Which DaVinci tenant, environment, population, flow, and version are in scope? Which connected Ping or external services remain separate? | Stop and clarify the platform or tenant when ambiguous. |
| Flow and connector readiness | Which flow version, nodes, connectors, connections, variables, and policies are required? | Check current product and connector documentation; do not infer availability from a different tenant or release. |
| Application and launch | How is the flow exposed through an application or policy, and is the intended surface redirect, widget, API, OIDC, SAML, or SDK? | Verify launch, allowed-flow, traffic-distribution, and application behavior in current docs. |
| Credentials and ownership | Which connection or service identity invokes the connected product, and where are secrets managed? | Verify scope, role, region, rotation, and least-privilege requirements. |
| Runtime and outcomes | What inputs, variables, node outcomes, connector errors, retries, and terminal results are documented? | Check the selected flow and connector contract; distinguish configuration from inference. |
| Promotion and operations | What moves between environments, and what must be recreated or verified in the target? | Recheck flow versions, connections, secrets, applications, policies, endpoints, observability, and drift. |

## Guardrails and report

Keep these distinctions visible:

- DaVinci is an orchestration platform, not a replacement for PingOne, PingOne Verify, PingOne Protect, PingOne MFA, or an external provider; those services retain their own product and credential boundaries.
- A widget, redirect, API, OIDC, SAML, and SDK launch can have different rendering, callback, token, input, error, and result responsibilities.
- Connectors and nodes perform configured actions and return outcomes; the host application or flow owns the business response unless the selected flow documents otherwise.
- Flow versions, variable scopes, connector behavior, application policies, provider endpoints, limits, and protocol details are release-sensitive or tenant-specific. Do not promote examples into defaults.
- Do not treat a deployed flow, successful test, or configured connection as proof that all dependent products, credentials, redirect settings, policies, and monitoring are production-ready.

Report: (1) the DaVinci tenant, flow, and execution-surface boundary; (2) flow, connector, application, and credential readiness; (3) verified launch and runtime behavior; (4) host handling of outcomes and errors; (5) promotion, operations, and unresolved checks; (6) documented facts versus inference, tenant-specific observations, and release-sensitive claims; and (7) the appropriate handoff to the [PingOne DaVinci reference](./README.md), the selected connected-product reference, [developer tools](../developer-tools/README.md), [orchestration SDKs](../orchestration-sdks/README.md), or current official documentation. Do not turn the report into a configuration runbook.
