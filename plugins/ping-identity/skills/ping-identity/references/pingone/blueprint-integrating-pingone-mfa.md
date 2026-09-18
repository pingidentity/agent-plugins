# Researching a PingOne MFA integration

## Scope

Use this as a focused research brief for **PingOne MFA (Strong Authentication)**. Keep the product and environment boundary explicit: PingOne MFA is a PingOne service for Customer and Workforce environments, while PingID is a separately administered Workforce MFA service with different integrations and policy behavior.

### Covers

- **Administrative/interface plane:** target PingOne organization and environment, Customer or Workforce population, entitlement and license, MFA settings and policies, methods, application or flow ownership, and promotion or drift checks.
- **Runtime/client plane:** enrollment or pairing, device registration, device selection, OTP or push confirmation, native-mobile application behavior, authentication outcomes, and the application or flow that interprets them.
- **Host integration choices:** PingOne APIs, native mobile SDKs, and PingOne DaVinci flows; where relevant, the boundary to PingFederate, PingID, or Workforce integrations.

### Does NOT cover

- Tenant mutations, policy authoring, API/CLI/Terraform commands, SDK code, exact environment values, secrets, request payloads, or executable DaVinci flows.
- Workforce PingID desktop, RADIUS, SSH, or other service-specific setup; those paths have separate ownership and documentation.
- A claim that an MFA method, policy, device, native application, connector, or flow is available merely because another environment or population supports it.

Treat this as orientation, not configuration authority. For implementation, use the linked product, API, CLI, Terraform, SDK, or orchestration documentation.

## Research brief

Research the integration as two related planes:

- **Administrative/interface plane:** establish the target environment and population first. Confirm the MFA product and license, supported methods, environment-level settings, device-authentication policies, application push credentials where applicable, administrator or worker authorization, and ownership of the application or flow that invokes MFA. Confirm whether the design uses direct PingOne MFA APIs, a native mobile SDK, or an orchestrated DaVinci flow. These are different execution surfaces even when they use the same MFA service.
- **Runtime/client plane:** identify whether the flow is enrolling or authenticating a device, which device and user context is available, and where the application or orchestration flow handles device selection, OTP, assertion, or push confirmation. A successful MFA operation is an authentication result for the selected flow; it does not by itself establish application authorization or replace a separately administered PingID integration.

A common documented lifecycle is: confirm environment and policy support; configure the relevant MFA settings and device-authentication policy; register or pair the user's device when required; start the selected device-authentication flow; complete the documented OTP, assertion, or push-confirmation step; and have the application or flow handle the terminal result. The exact methods, fields, statuses, and availability are environment-, geography-, license-, and surface-sensitive.

## Resource index

### PingOne MFA administration and runtime

- [PingOne Strong Authentication overview](https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_strong_authentication_start.html)
- [Customer and Workforce environment differences](https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_pid_what_is_the_difference.html)
- [PingOne Strong Authentication integrations](https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_strong_authentication_integrations.html)
- [PingOne MFA API introduction](https://developer.pingidentity.com/pingone-api/mfa/introduction.html)
- [PingOne MFA Native SDK overview](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-mfa-mobile-sdks.html)
- [PingOne MFA mobile SDK flows](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-mfa-mobile-sdks/pingone-mfa-mobile-sdk-flows.html)

### Configuration and execution handoffs

- [PingOne MFA API handoff](api.md)
- [PingOne MFA CLI handoff](cli.md)
- [PingOne MFA Terraform handoff](terraform.md)
- [PingOne MFA Native SDK handoff](sdk.md)
- [PingOne DaVinci reference](../pingone-davinci/README.md)
- [PingFederate reference](../pingfederate/README.md)
- [PingID reference](../pingid/README.md)

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Environment boundary | Is the target a PingOne Customer or Workforce environment? Which organization, environment, population, geography, and license are in scope? | Do not transfer methods or integrations between Customer and Workforce environments without checking current support. |
| MFA readiness | Which MFA product, settings, methods, policies, and native-app prerequisites are enabled? | Check current bill of materials, policy support, geography, and release; do not infer readiness from another environment. |
| Credentials and ownership | Which worker, user, native application, application push credential, connector, or flow invokes MFA, and where are secrets managed? | Verify authorization, scopes, roles, rotation, and least-privilege requirements in current documentation. |
| Enrollment and device state | Is the journey registering, pairing, enabling, or authenticating a user device? | Check the selected API, SDK, or flow contract and distinguish documented state from inference. |
| Runtime authentication | Which device-authentication path applies: device selection, OTP, assertion, or push confirmation? | Verify request/response schemas, status handling, timeout and retry behavior, and supported methods for the target population. |
| Decision and handoff | Where does the application, PingFederate integration, or DaVinci flow interpret the MFA result and continue, retry, or stop? | MFA completion does not by itself define application authorization; confirm the host integration's documented behavior. |
| Promotion and operations | What moves between environments, and what must be recreated or verified? | Recheck policies, push credentials, application or flow bindings, SDK versions, endpoints, audit visibility, and drift. |

## Guardrails and report

Keep these distinctions visible:

- PingOne MFA is the strong-authentication service; PingID is a separate Workforce MFA service. Do not use the products or their integration paths as synonyms.
- Customer and Workforce environments can differ in supported methods and integrations. Geography, license, policy, and release can change applicability.
- A direct API integration, native mobile SDK integration, and DaVinci connector or flow can have different credentials, inputs, device state, outcome handling, and promotion requirements.
- PingOne Protect evaluates risk and can inform MFA decisions, but it does not enroll or authenticate an MFA factor. PingOne Verify performs identity verification, not sign-on MFA.
- Do not treat an installed SDK, registered device, successful API response, or active flow as proof that policy, credentials, push delivery, application bindings, and monitoring are production-ready.

Report: (1) the PingOne environment and Customer/Workforce boundary; (2) administrative, policy, and credential readiness; (3) the verified enrollment or device-authentication behavior; (4) application or flow result handling; (5) promotion, operations, and unresolved checks; (6) documented facts versus inference, tenant-specific observations, and release-sensitive claims; and (7) the appropriate handoff to the [PingOne MFA reference](./README.md), [API](api.md), [CLI](cli.md), [Terraform](terraform.md), [Native SDK](sdk.md), [PingOne DaVinci reference](../pingone-davinci/README.md), or current official documentation.
