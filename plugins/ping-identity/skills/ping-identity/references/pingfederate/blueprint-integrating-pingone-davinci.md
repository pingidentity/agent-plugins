# Researching a PingFederate–PingOne DaVinci integration

## Scope

Use this as a focused research brief for **PingFederate** and **PingOne DaVinci**. DaVinci orchestrates identity and access flows; PingFederate hosts federation and authentication-policy decisions. The documented PingFederate-side boundary includes the PingOne DaVinci IdP Adapter, while DaVinci applications and flow policies expose selected flows through their own launch surfaces.

### Covers

- **Administrative/interface plane:** PingFederate deployment and adapter ownership, DaVinci tenant and environment, flow and revision, application and flow-policy bindings, credentials, redirect and endpoint ownership, and promotion or monitoring responsibilities.
- **Runtime/host plane:** adapter or application launch, OIDC/SAML/API or SDK surface selection, flow variables and connector outcomes, authentication-policy routing, and the handoff of terminal results to PingFederate or the host application.

### Does NOT cover

- Tenant mutations, adapter installation commands, executable flow definitions, connector-specific payloads, API/CLI/Terraform commands, SDK code, exact environment values, or secrets.
- A claim that the bundled adapter, a generic OIDC/SAML launch, an orchestration SDK, or a DaVinci flow has identical token, callback, variable, or error behavior.
- A claim that a DaVinci flow automatically authenticates, authorizes, provisions, performs MFA, or mitigates risk without a documented flow and host contract.
- PingOne MFA, Protect, Verify, Credentials, or other connected-product administration; those services retain their own references and integration boundaries.

Treat this as orientation, not configuration authority. Confirm current PingFederate adapter, authentication-policy, DaVinci application, flow, protocol, and SDK documentation for the target release.

## Research brief

Research two connected planes:

- **Administrative/interface plane:** identify the PingFederate deployment and version, the PingOne DaVinci tenant and environment, the selected flow and revision, the application and flow policy, the PingOne DaVinci IdP Adapter or other launch surface, credentials and secret boundary, redirect or endpoint ownership, and operations responsibility. Confirm whether the design uses the bundled adapter or a generic OIDC, SAML, API, widget, or orchestration-SDK path; these are distinct contracts.
- **Runtime/host plane:** determine how PingFederate or the application starts the flow, which inputs and variables are available, how nodes and connectors branch, how the flow reports success, failure, retry, or cancellation, and where PingFederate's authentication policy or the host application consumes the result. A flow outcome is not automatically a federation assertion, authorization decision, or application action.

A common documented lifecycle is: configure the DaVinci flow and revision; attach it to an application and flow policy or select the PingOne DaVinci IdP Adapter; expose the intended launch surface; start the flow from PingFederate or the application; collect inputs and invoke nodes; return the documented terminal outcome; and let PingFederate or the host application continue, retry, or stop. Exact token, callback, variable, adapter, and failure behavior is release- and surface-sensitive.

## Resource index

### PingFederate host and adapter

- [PingFederate reference](README.md)
- [PingFederate IdP adapters](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf_managing_idp_adapters.html)
- [PingFederate authentication policies](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf_authentication_policies.html)

### DaVinci flow and launch surfaces

- [PingOne DaVinci reference](../pingone-davinci/README.md)
- [PingOne DaVinci documentation](https://docs.pingidentity.com/davinci/davinci_introduction.md)
- [DaVinci applications and flow policies](https://docs.pingidentity.com/davinci/applications/davinci_applications.html)
- [How to implement a DaVinci flow](https://docs.pingidentity.com/davinci/integrating_flows_into_applications/davinci_how_to_implement_a_flow.md)
- [DaVinci Ping connectors](https://docs.pingidentity.com/davinci/connectors/davinci_ping_connectors.md)
- [Generic DaVinci integration research](../pingone/blueprint-integrating-pingone-davinci.md)
- [Orchestration SDKs reference](../orchestration-sdks/README.md)

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Product and tenant boundary | Which PingFederate deployment, PingOne DaVinci tenant/environment, population, application, flow, and revision are in scope? | Do not transfer flow, connector, or policy behavior between tenants or releases. |
| Host and launch surface | Is the design using the PingOne DaVinci IdP Adapter, an application launch endpoint, OIDC, SAML, API, widget, or orchestration SDK? | Do not combine adapter-specific and generic protocol assumptions; verify current adapter and launch documentation. |
| Flow readiness | Which flow policy, allowed flow/revision, connections, connectors, variables, and traffic-distribution settings are required? | Check current application and flow contracts; a published flow does not prove dependent connections are ready. |
| Credentials and endpoints | Which adapter, application, connection, client, redirect, certificate, endpoint, and secret owners participate? | Verify scopes, roles, rotation, redirect values, endpoint region, certificate trust, and network access. |
| Runtime and outcomes | What inputs, variables, node outcomes, connector errors, retries, callbacks, and terminal results are documented? | Treat token claims, callback parameters, statuses, and failure routing as surface- and release-sensitive. |
| Policy handoff | How does PingFederate's authentication policy or the host application map flow completion or failure to authentication, step-up, retry, or stop? | A DaVinci outcome does not itself establish authorization, claims, session state, or provisioning. |
| Promotion and operations | What flows, revisions, applications, policies, adapters, connections, secrets, endpoints, and audit evidence move or must be recreated? | Recheck bindings, redirect settings, credentials, monitoring, dependent products, and configuration drift. |

## Guardrails and report

Keep these distinctions visible:

- DaVinci is an orchestration platform, while PingFederate is the federation and authentication-policy host. The PingOne DaVinci IdP Adapter, DaVinci application, flow policy, and generic protocol launch are related but distinct integration surfaces.
- A widget, redirect, API, OIDC, SAML, SDK, and bundled adapter path can have different rendering, callback, token, input, error, and result responsibilities.
- Connectors and nodes return configured outcomes; PingFederate or the host application owns the authentication, authorization, and business response unless the selected flow contract documents otherwise.
- Flow versions, variables, connector behavior, adapter compatibility, application policies, redirect settings, token claims, limits, and protocol details are release-sensitive or tenant-specific. Do not promote examples into defaults.
- Do not treat a deployed flow, configured adapter, successful test, or registered application as proof that dependent products, credentials, redirects, policies, network access, and monitoring are production-ready.

Report: (1) the PingFederate and DaVinci tenant, flow, adapter, and execution-surface boundary; (2) flow, application, policy, credential, and endpoint readiness; (3) verified launch and runtime behavior; (4) PingFederate or application handling of outcomes and errors; (5) promotion, operations, and unresolved checks; (6) documented facts versus inference, tenant-specific observations, and release-sensitive claims; and (7) the appropriate handoff to the [PingFederate reference](README.md), [PingOne DaVinci reference](../pingone-davinci/README.md), [orchestration SDKs](../orchestration-sdks/README.md), or current official documentation. Do not turn the report into a configuration runbook.
