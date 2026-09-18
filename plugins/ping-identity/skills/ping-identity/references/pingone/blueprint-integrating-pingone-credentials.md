# Researching PingOne Credentials integrations

## Scope

Use this as a focused research brief for **PingOne Credentials**, the PingOne service for creating and delivering verifiable credentials to compatible wallet applications. Keep the service boundary explicit: PingOne Credentials manages issuer-side credential resources and delivery-related administration; the wallet application and any connected application own wallet-side handling and business use of a credential.

### Covers

- **Administrative/interface plane:** organization and environment scope, credential and credential-profile ownership, issuer readiness, lifecycle administration, notification-template responsibility, and operational monitoring.
- **Runtime/integration plane:** credential issuance and delivery to compatible wallet applications, wallet application registration and native SDK handoff, and documented API, connector, Marketplace, and notification resources.

### Does NOT cover

- Tenant mutations, credential authoring procedures, API payloads or schemas, native SDK code, executable wallet applications, connector configuration, notification-channel guarantees, or deployment commands.
- Verification, storage, presentation, revocation, or trust-model behavior unless the selected current documentation explicitly covers it. Do not infer wallet capabilities from the existence of an issuer or SDK resource.
- PingOne Neo as a separate product boundary. Use the relevant Neo documentation when the request concerns broader verified-identity or wallet capabilities rather than PingOne Credentials issuance.

Treat this as orientation, not configuration authority. Confirm current PingOne Credentials, API, connector, Marketplace, and wallet SDK documentation for the target release and tenant.

## Research brief

Research the integration as two related planes:

- **Administrative/interface plane:** identify the target PingOne organization and environment, credential program and issuer, credential or credential-profile ownership, populations and scenarios, notification-template responsibility, wallet application registration, credentials and secret boundary, and monitoring or support ownership. Credential configuration in one environment does not establish readiness in another.
- **Runtime/integration plane:** determine how the issuer creates or manages the credential, which issuance or delivery experience is in scope, how the compatible wallet application receives it, and where a direct API, Credentials Connector, or other documented integration is used. A wallet native SDK is a development handoff, not proof that a wallet app is registered, compatible, or production-ready.

A common documented lifecycle is: establish the issuer and credential model; create or manage the credential resource; prepare the supported wallet application and communications; initiate documented delivery; and verify operational ownership for the resulting credential experience. Exact issuance messages, wallet behavior, API contracts, connector inputs and outputs, notification triggers, and lifecycle semantics are surface- and release-sensitive.

## Resource index

### PingOne Credentials administration and APIs

- [Product Index](https://docs.pingidentity.com/product-index.html)
- [PingOne Credentials overview](https://docs.pingidentity.com/pingone/digital_credentials_using_pingone_credentials/p1_credentials_start.html)
- [PingOne API onboarding](https://developer.pingidentity.com/pingone-api/getting-started/introduction.html)
- [Credentials API](https://developer.pingidentity.com/pingone-api/credentials/introduction.html)
- [Credential issuer resources](https://developer.pingidentity.com/pingone-api/credentials/credential-profiles.html)
- [Notification templates](https://docs.pingidentity.com/pingone/digital_credentials_using_pingone_credentials/p1_credentials_customizing_notification_templates.html)

### Wallet, connector, and Marketplace surfaces

- [PingOne wallet native SDKs](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-neo-native-sdks/pingone-wallet-native-sdks.html)
- [PingOne Credentials Connector](https://docs.pingidentity.com/connectors/p1_credentials_connector.html)
- [Ping Identity Marketplace: Credentials](https://marketplace.pingone.com/browse?products=credentials)
- [PingOne Credentials reference](./README.md)
- [PingOne Neo reference](../pingone-neo/README.md)
- [Developer tools handoff](../developer-tools/README.md)
- [Terraform handoff](../terraform/README.md)

Use the current documentation for the chosen issuer, wallet, API, connector, or Marketplace path. Do not infer that a connector, SDK, or Marketplace listing provides the same lifecycle or security boundary as direct API integration.

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Service boundary | Is the request for PingOne Credentials issuance, a wallet application, PingOne Neo, or broader verified-identity behavior? Which organization, environment, issuer, population, and scenario are in scope? | Stop and clarify an ambiguous product or platform boundary. |
| Administrative readiness | Are the credential model, issuer resources, credential profiles, notification templates, wallet registration, credentials, and monitoring ownership ready in the target environment? | Verify entitlement, permissions, environment, issuer state, and promotion requirements. |
| Integration surface | Is the design direct Credentials API, the Credentials Connector, wallet native SDK, Marketplace resource, or a combination? | Use the matching current documentation; do not combine issuer-, connector-, and wallet-specific assumptions. |
| Runtime | What issuance and delivery event is in scope? Which wallet app, SDK-supported surface, recipient context, and communications are available? | Check the selected API, connector, SDK, and notification contracts; distinguish documented behavior from inference. |
| Credential lifecycle | Which create, edit, manage, deliver, or notification operations are supported for the requested scenario? | Verify current lifecycle and status semantics; do not infer presentation, verification, storage, or revocation behavior. |
| Promotion and operations | What credential resources, issuer settings, wallet bindings, templates, credentials, endpoints, and audit evidence move or must be recreated? | Recheck target environment, secret handling, wallet compatibility, delivery channels, monitoring, and configuration drift. |

## Guardrails and report

Keep these distinctions visible:

- PingOne Credentials is an issuer-side digital-credential service; a compatible wallet application is a separate runtime surface, and PingOne Neo is a separate product context.
- Credential resources, credential profiles, notification templates, wallet applications, API credentials, and connector bindings are related but distinct dependencies. A successfully created credential does not prove delivery or wallet readiness.
- Direct API integration, the Credentials Connector, and wallet native SDK development can have different credentials, input mappings, lifecycle behavior, and promotion requirements.
- Do not infer wallet storage, presentation, verification, revocation, supported platforms, notification delivery guarantees, or trust semantics from this orientation page. Treat those as documented, tenant-specific, or release-sensitive only when verified.
- An active issuer, registered wallet app, successful API response, or installed SDK does not prove that target credentials, templates, delivery, monitoring, and operational ownership are complete.

Report: (1) the PingOne Credentials issuer and wallet boundary; (2) verified administrative, issuer, and credential readiness; (3) documented issuance and delivery behavior and selected surface; (4) wallet, connector, API, and notification handling; (5) promotion, operations, and unresolved checks; (6) documented facts versus inference, tenant-specific observations, and release-sensitive claims; and (7) the appropriate handoff to the [PingOne Credentials reference](./README.md), selected current API, connector, or wallet SDK documentation, [developer tools](../developer-tools/README.md), [Terraform](../terraform/README.md), or [PingOne Neo](../pingone-neo/README.md). Do not turn the report into a configuration runbook.
