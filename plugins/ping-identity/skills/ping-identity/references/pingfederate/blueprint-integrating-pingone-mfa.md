# Researching a PingFederate–PingOne MFA integration

## Scope

Use this as a focused research brief for **PingFederate** and **PingOne MFA (Strong Authentication)** in a Customer environment. The integration boundary is a PingFederate federation or authentication transaction that invokes the PingOne MFA Integration Kit, with PingFederate retaining ownership of the authentication policy and application-access result.

### Covers

- **Administrative/interface plane:** PingFederate and PingOne MFA product and environment boundary, Customer-versus-Workforce applicability, Integration Kit and version compatibility, adapter and policy ownership, credentials, endpoint reachability, and promotion dependencies.
- **Runtime/authentication plane:** the selected MFA enrollment or authentication path, device and factor state, the result exposed to PingFederate, authentication-policy routing, step-up or failure handling, and transaction completion.

### Does NOT cover

- Tenant mutations, Integration Kit installation commands, adapter or policy field values, API/CLI/Terraform commands, SDK code, exact credentials or regional values, or executable authentication policies.
- The separately administered Workforce **PingID** integration, including legacy federation or identity-bridge paths, desktop, RADIUS, SSH, or other PingID-specific setup. Use the [PingID reference](../pingid/README.md) for that boundary.
- A claim that successful MFA automatically authorizes an application, establishes a session, or replaces PingFederate authentication-policy evaluation.
- A claim that a Customer Integration Kit path applies to every Workforce environment, geography, license, factor, or release.

Treat this as orientation, not an installation or administration guide. Confirm current PingOne Strong Authentication, Integration Kit, PingFederate, and PingID documentation for the target release and population.

## Research brief

Research two connected planes:

- **Administrative/interface plane:** identify the PingFederate deployment and version, the PingOne organization and Customer environment, the MFA entitlement and supported methods, the applicable PingOne MFA Integration Kit, adapter and authentication-policy ownership, service identity and secret boundary, and outbound endpoint or firewall requirements. Confirm that the design is a Customer PingOne MFA path rather than a Workforce federation or identity-bridge path that uses PingID. Kit behavior and supported combinations are release-, geography-, and environment-sensitive.
- **Runtime/authentication plane:** determine whether the transaction is enrolling or authenticating a factor, which user and device state is available, where the selected adapter or integration surface invokes MFA, and how the resulting success, failure, retry, timeout, or cancellation is exposed to the PingFederate authentication policy. The policy then maps the MFA result to the documented authentication treatment and application-access response.

A documented high-level lifecycle is: establish the Customer environment and supported MFA policy; connect PingOne to PingFederate and configure the applicable PingOne MFA Integration Kit; invoke the selected enrollment or device-authentication path; complete the supported factor interaction; return the documented result to the PingFederate transaction; and continue, step up, retry, or stop according to the authentication policy. The exact adapter topology, factor methods, enrollment state, callback behavior, and failure handling must come from current product and kit documentation rather than inference.

## Resource index

### PingOne MFA and population boundary

- [PingOne Strong Authentication overview](https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_strong_authentication_start.html)
- [PingOne Strong Authentication integrations](https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_strong_authentication_integrations.html)
- [Customer and Workforce environment differences](https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_pid_what_is_the_difference.html)
- [PingOne MFA Integration Kit for PingFederate](https://docs.pingidentity.com/integrations/pingone/pingone_mfa_integration_kit/pf_p1_mfa_ik.html)
- [PingOne MFA reference](../pingone-mfa/README.md)
- [PingOne MFA research brief](../pingone/blueprint-integrating-pingone-mfa.md)

### PingFederate administration and handoffs

- [PingFederate reference](README.md)
- [PingFederate IdP adapters](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf_managing_idp_adapters.html)
- [PingFederate authentication policies](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf_authentication_policies.html)
- [PingID reference](../pingid/README.md)
- [MFA use cases](../mfa-use-cases/README.md)

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Product and population boundary | Is the transaction for a PingOne Customer environment using the PingOne MFA Integration Kit, or a Workforce federation or identity-bridge deployment using PingID? Which PingFederate deployment, population, and protocol are in scope? | Do not transfer Customer MFA-kit assumptions to Workforce PingID paths. Verify geography, license, release, and supported population. |
| Kit and administrative readiness | Which Integration Kit and PingFederate version are supported? Which adapter, authentication policy, application binding, factor policy, and administrator ownership are required? | Confirm current compatibility, entitlement, policy support, and installation or upgrade lifecycle in official documentation. |
| Credentials and network | Which application, worker, adapter, or service identity invokes the service, and where are secrets, certificates, regional endpoints, and outbound firewall rules managed? | Verify scopes, roles, certificate trust, rotation, endpoint region, and least-privilege requirements. |
| Enrollment and device state | Is the flow registering, pairing, enabling, or authenticating a factor? Which user, device, and policy state is available to the integration? | Check the selected kit and MFA contract; do not infer enrollment readiness from a registered user or device. |
| Authentication result | What documented result, status, callback, or error reaches PingFederate, and how are timeout, retry, cancellation, and unavailable-factor cases represented? | Verify kit and PingFederate release behavior; distinguish documented fields from policy inference. |
| Policy and application handoff | How does the PingFederate authentication policy map MFA completion or failure to normal authentication, step-up, retry, or stop? | MFA completion does not itself define authorization, claims, session policy, or application access. |
| Promotion and operations | Which adapters, policies, bindings, certificates, templates, endpoints, and PingOne-side settings move or must be recreated? What evidence is retained for support and audit? | Revalidate secrets, factor policy, endpoint reachability, logging, monitoring, release compatibility, and drift in the target. |

## Guardrails and report

Keep these distinctions visible:

- PingOne MFA is the PingOne Strong Authentication service; PingID is a separately administered Workforce MFA service. A PingFederate integration must name the applicable product and population rather than treating them as synonyms.
- The PingOne MFA Integration Kit, PingFederate adapters, authentication policies, user/device state, and application bindings are distinct components. A configured component does not by itself prove that the transaction can complete.
- Customer and Workforce environments can have different methods and integration paths. Geography, license, policy, and release can change applicability; the documented Singapore and legacy-PingID boundaries must not be generalized.
- MFA authenticates a factor. PingFederate owns the surrounding federation transaction and authentication-policy response; the host application owns authorization and business actions unless current documentation states otherwise.
- Do not treat an installed kit, registered device, successful test, or returned MFA result as proof that credentials, factor policy, network access, policy routing, monitoring, and promotion are production-ready.

Report: (1) the PingFederate transaction, PingOne environment, population, and MFA/PingID boundary; (2) verified kit, version, entitlement, policy, credential, and network readiness; (3) documented enrollment or authentication behavior; (4) PingFederate policy handling for success, failure, retry, and step-up; (5) promotion, operations, and unresolved checks; (6) documented facts versus inference, tenant-specific observations, and release-sensitive claims; and (7) the appropriate handoff to the [PingFederate reference](README.md), [PingOne MFA reference](../pingone-mfa/README.md), [PingID reference](../pingid/README.md), [MFA use cases](../mfa-use-cases/README.md), or current official documentation. Do not turn the report into an installation or policy-authoring runbook.
