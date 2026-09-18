# Researching PingOne Authorize integrations

## Scope

Use this as a focused research brief for **PingOne Authorize**, the PingOne service for centralized authorization of applications and APIs. Keep the service boundary explicit: Authorize evaluates configured policies and returns authorization decisions; the calling application, API, gateway, or orchestration flow owns the surrounding transaction and business response.

### Covers

- **Administrative/interface plane:** organization and environment scope, authorization-service readiness, Trust Framework building blocks, policy and policy-version ownership, API definitions, protected operations, and decision review or monitoring.
- **Runtime/integration plane:** authorization decision requests for applications and APIs, individual or bulk evaluation, and documented gateway, edge, DaVinci, and external OAuth integration surfaces.

### Does NOT cover

- Tenant mutations, policy authoring procedures, API payloads or schemas, gateway configuration steps, CLI/Terraform commands, executable DaVinci flows, or application code.
- A claim that a returned decision automatically authenticates a user, performs MFA, or implements a business action. The integrating application, API, gateway, or flow must define that response.
- PingAuthorize or another authorization product. Those products have separate product boundaries and documentation.

Treat this as orientation, not configuration authority. Confirm current PingOne Authorize and integration documentation for the target release and tenant.

## Research brief

Research the integration as two related planes:

- **Administrative/interface plane:** identify the target PingOne organization and environment, the populations and applications in scope, the Trust Framework and policy ownership, API definitions and protected operations, the selected integration surface, credentials and secret boundary, and monitoring responsibility. An API definition or policy in one environment does not establish readiness in another.
- **Runtime/integration plane:** determine which application, API, gateway, edge function, DaVinci flow, or external OAuth arrangement requests the decision; which subject, resource, action, and context are available at evaluation time; and where the result is interpreted. Individual and bulk decision evaluation are documented surfaces, but the exact request and response contract is surface- and release-sensitive.

A common documented lifecycle is: model protected APIs or resources; configure reusable Trust Framework and policy building blocks; publish or otherwise make the applicable policy available; submit an authorization evaluation through the selected surface; interpret the returned decision; and apply the host application's access or mitigation response. The exact promotion, caching, failure, and observability behavior must come from the current product or integration documentation rather than inference.

## Resource index

### PingOne Authorize administration and decisions

- [Product Index](https://docs.pingidentity.com/product-index.html)
- [PingOne Authorize overview](https://docs.pingidentity.com/pingone/authorization_using_pingone_authorize/p1az_overview.md)
- [Authorization decisions API](https://developer.pingidentity.com/pingone-api/authorize/authorization-decisions.html)
- [API Access Management API](https://developer.pingidentity.com/pingone-api/authorize/api-access-management.html)
- [Bulk decision evaluation](https://developer.pingidentity.com/pingone-api/authorize/authorization-decisions/decision-evaluation/execute-a-bulk-decision-request.html)

### Integration surfaces and handoffs

- [PingOne Authorize connector](https://docs.pingidentity.com/connectors/p1az_connector.html)
- [PingGateway authorization integration](https://docs.pingidentity.com/pinggateway/latest/pingone/aam.html)
- [PingOne DaVinci reference](../pingone-davinci/README.md)
- [Developer tools handoff](../developer-tools/README.md)
- [Terraform handoff](../terraform/README.md)

The Authorize documentation also indexes integrations for AWS, Apigee, Kong Gateway, Kong Konnect, Amazon CloudFront Lambda@Edge, and external OAuth authorization servers. Use the current product documentation for the selected surface; do not infer one gateway's configuration, token handling, or deployment behavior from another.

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Service boundary | Is the request for PingOne Authorize, PingAuthorize, or another product? Which organization, environment, application, API, population, resource, and action are in scope? | Stop and clarify an ambiguous product or platform boundary. |
| Administrative readiness | Are the Trust Framework, policies, versions, API definitions, protected operations, credentials, and monitoring ownership ready in the target environment? | Verify entitlement, permissions, environment, policy state, and promotion requirements. |
| Integration surface | Is the design direct API evaluation, a supported gateway or edge integration, the DaVinci connector, or an external OAuth arrangement? | Use the matching current integration guide; do not combine surface-specific assumptions. |
| Runtime | What subject, resource, action, and contextual data are available when the decision is requested? Is evaluation individual or bulk? | Check the selected API or connector contract and release; distinguish documented fields from inference. |
| Decision handling | How does the host application, API, gateway, or flow map the returned decision to allow, deny, step-up, or another response? | Treat thresholds, mappings, fallback, caching, and failure behavior as policy-, integration-, and tenant-specific. |
| Promotion and operations | What policies, API definitions, credentials, gateway or connector bindings, endpoints, dashboards, and audit evidence move or must be recreated? | Recheck target environment, secret handling, endpoint reachability, logging, and configuration drift. |

## Guardrails and report

Keep these distinctions visible:

- PingOne Authorize is an authorization decision service; it is not a general-purpose identity provider, authentication policy engine, or automatic MFA mechanism.
- Trust Framework elements, policies, policy versions, API definitions, and protected operations are related but distinct administrative objects. A configured object does not by itself prove that the selected runtime integration is ready.
- Direct API evaluation, gateway or edge integrations, the DaVinci connector, and external OAuth arrangements can have different credentials, input mappings, decision handling, and promotion requirements.
- A decision result is an input to the host application's access response. Do not promote local policy thresholds, decision fields, token claims, gateway behavior, or failure mappings into universal defaults.
- An active policy, successful test response, or deployed gateway component does not prove that target credentials, API bindings, egress, monitoring, and operational ownership are complete.

Report: (1) the PingOne Authorize and host-integration boundary; (2) verified administrative and credential readiness; (3) documented evaluation behavior and selected surface; (4) application, API, gateway, or flow decision handling; (5) promotion, operations, and unresolved checks; (6) documented facts versus inference, tenant-specific observations, and release-sensitive claims; and (7) the appropriate handoff to the [PingOne Authorize reference](./README.md), the selected current integration documentation, [developer tools](../developer-tools/README.md), [Terraform](../terraform/README.md), or [PingOne DaVinci](../pingone-davinci/README.md). Do not turn the report into a configuration runbook.
