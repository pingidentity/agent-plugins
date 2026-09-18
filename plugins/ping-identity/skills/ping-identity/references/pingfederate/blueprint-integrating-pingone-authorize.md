# Researching a PingFederate–PingOne Authorize integration

## Scope

Use this as a focused research brief when **PingFederate** participates in an application, API, gateway, or OAuth/OIDC topology that also uses **PingOne Authorize**. PingFederate owns federation and authentication; PingOne Authorize evaluates authorization policies; the integrating application, API, gateway, or orchestration flow enforces the returned decision. Current product documentation does not establish a native PingFederate Authorize adapter or Integration Kit, so the exact host-mediated topology must be verified before implementation.

### Covers

- **Administrative/interface plane:** PingFederate deployment and token or application context, PingOne Authorize organization and environment, Trust Framework and policy ownership, API definitions and protected operations, selected decision-evaluation surface, credentials and key material, and promotion or monitoring responsibilities.
- **Runtime/decision plane:** subject, resource, action, and context mapping; direct or supported gateway/API/OAuth decision evaluation; returned decision handling; and the handoff to the PingFederate-hosted application or API.

### Does NOT cover

- Tenant mutations, policy-authoring procedures, API payloads or schemas, gateway configuration steps, OAuth administration commands, executable DaVinci flows, application code, exact environment values, or secrets.
- A claim that PingFederate is a native PingOne Authorize adapter, policy engine, gateway integration, or decision client. Current official documentation must establish the selected topology.
- PingAuthorize Server or another authorization product. Use the separate [PingAuthorize reference](../pingauthorize/README.md) when that product is in scope.
- A claim that an authorization decision authenticates a user, performs MFA, creates a PingFederate session, issues a token, or automatically changes a PingFederate authentication policy.

Treat this as orientation, not configuration authority. Confirm current PingOne Authorize, PingFederate, OAuth/OIDC, gateway, API, and selected integration documentation for the target release.

## Research brief

Research two connected planes:

- **Administrative/interface plane:** identify the PingFederate deployment and application/API context, the PingOne Authorize organization and environment, Trust Framework and policy versions, API definitions and protected operations, selected direct API, gateway, DaVinci, edge, or external-OAuth surface, credentials and signing keys, issuer/JWKS or endpoint ownership, and monitoring responsibility. Generic external OAuth or gateway support does not by itself establish a PingFederate-specific integration.
- **Runtime/decision plane:** determine which subject, resource, action, token, and contextual data are available; where the decision request is evaluated; how any PingFederate-issued or consumed token participates in the selected documented topology; and where the application, API, gateway, or flow maps the result to allow, deny, step-up, retry, or mitigation. An Authorize result is an input to enforcement; it is not automatically a PingFederate authentication result.

A common documented lifecycle is: model protected resources and operations; configure the applicable Trust Framework and policy; establish the selected decision-evaluation or gateway boundary; submit a decision with the documented subject, resource, action, and context; interpret the returned result; and enforce the application-specific response. If PingFederate participates as an issuer, relying party, or authentication host, verify the issuer, audience, signature, JWKS, claims, credential, and token-handling contract from the selected integration documentation rather than inference.

## Resource index

### PingOne Authorize administration and decisions

- [PingOne Authorize overview](https://docs.pingidentity.com/pingone/authorization_using_pingone_authorize/p1az_overview.md)
- [PingOne Authorize external OAuth servers](https://docs.pingidentity.com/pingone/authorization_using_pingone_authorize/p1_az_external_oauth_servers.html)
- [PingOne Authorize gateway integrations](https://docs.pingidentity.com/pingone/integrations/p1_authz_gateways.html)
- [Authorization Decisions API](https://developer.pingidentity.com/pingone-api/authorize/authorization-decisions.html)
- [API Access Management API](https://developer.pingidentity.com/pingone-api/authorize/api-access-management.html)
- [PingOne Authorize DaVinci connector](https://docs.pingidentity.com/connectors/p1az_connector.html)
- [PingOne Authorize reference](../pingone-authorize/README.md)
- [Generic Authorize integration research](../pingone/blueprint-integrating-pingone-authorize.md)

### PingFederate host and handoffs

- [PingFederate reference](README.md)
- [PingFederate authentication policies](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf_authentication_policies.html)
- [PingFederate IdP adapters](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf_managing_idp_adapters.html)
- [PingGateway reference](../pinggateway/README.md)
- [PingAuthorize reference](../pingauthorize/README.md)

The selected current documentation must identify whether PingFederate is an issuer, relying party, application-access host, or merely adjacent to the gateway or API that calls Authorize. Do not merge surface-specific token validation, request mapping, caching, or failure behavior.

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Product and responsibility boundary | Is the request for PingOne Authorize, PingAuthorize, or another decision service? Which PingFederate transaction, application, API, gateway, and population are in scope? | PingFederate authenticates/federates; Authorize evaluates policy; the host enforces the decision. Stop on an ambiguous product boundary. |
| Policy and administrative readiness | Which Trust Framework, policy version, API definition, protected operation, environment, and monitoring owner are required? | Verify entitlement, permissions, policy state, publication, environment, and promotion requirements. |
| Evaluation surface | Is the design direct decision API, supported gateway/edge integration, DaVinci connector, or external OAuth arrangement? | Current evidence does not name a native PF–Authorize adapter; verify the selected documented surface before claiming a PF integration. |
| Token and credential boundary | Does PingFederate issue or consume a token in the selected arrangement? Which issuer, audience, time claims, signing keys, JWKS, client credentials, and endpoint are required? | Do not infer token acceptance, claims, exchange, or validation rules from generic OAuth support. |
| Runtime decision | Which subject, resource, action, and context reach Authorize, and what decision or metadata returns? | Check the current API, connector, gateway, or external-OAuth contract; distinguish documented fields from inference. |
| Enforcement and policy handoff | How does the application, API, gateway, or flow map the result to allow, deny, step-up, retry, or mitigation? | An Authorize decision does not authenticate, perform MFA, issue a session, or automatically alter PingFederate policy. |
| Promotion and operations | What policies, API definitions, credentials, keys, gateway/application bindings, endpoints, logs, and audit evidence move or must be recreated? | Recheck secret rotation, JWKS, endpoint reachability, caching/failure behavior, monitoring, and configuration drift. |

## Guardrails and report

Keep these distinctions visible:

- PingFederate is the federation and authentication-policy host; PingOne Authorize is an authorization decision service; the application, API, gateway, or flow owns enforcement. Do not collapse authentication, token issuance, authorization, and business response.
- Trust Framework elements, policies, policy versions, API definitions, protected operations, tokens, and gateway bindings are distinct dependencies. A successful authentication or decision test does not prove the complete topology is ready.
- Direct API evaluation, gateway/edge integrations, DaVinci, and external OAuth arrangements can have different credentials, input mappings, token validation, caching, failure, and promotion requirements.
- Current reviewed documentation does not establish a first-party PingFederate Authorize adapter or Integration Kit. Treat any PF relationship as an explicitly verified host-mediated topology, and fail closed when the selected contract is unclear.
- Do not promote policy thresholds, decision fields, token claims, gateway behavior, fallback mappings, or failure handling into universal defaults.

Report: (1) the PingFederate, PingOne Authorize, application/API/gateway, and execution-surface boundary; (2) verified policy, API-definition, credential, token, key, and network readiness; (3) documented decision request and response behavior; (4) application, API, gateway, or flow enforcement handling; (5) promotion, operations, and unresolved checks; (6) documented facts versus inference, tenant-specific observations, and release-sensitive claims; and (7) the appropriate handoff to the [PingFederate reference](README.md), [PingOne Authorize reference](../pingone-authorize/README.md), selected current Authorize documentation, [PingGateway](../pinggateway/README.md), or [PingAuthorize](../pingauthorize/README.md). Do not turn the report into a configuration runbook.
