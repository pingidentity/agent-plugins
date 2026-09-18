# Researching a PingOne Recognize integration

## Scope

Use this as a focused research brief for **PingOne Recognize**, a biometric enrollment and authentication service. Keep the product boundary explicit: this brief concerns Recognize enrollment, biometric authentication, account recovery, transaction authentication, workforce use, and the mobile, web, server, and IDV Bridge surfaces documented for those scenarios.

### Covers

- **Administrative/interface plane:** Recognize tenant and application scope, user and device lifecycle ownership, mobile or web SDK selection, server API responsibilities, IDV Bridge deployment, and OIDC/SAML or workforce integration boundaries.
- **Runtime/client plane:** enrollment, client and device state, biometric authentication with liveness, step-up or payment authentication, recovery or new-device activation, and the handling of documented results and telemetry.

### Does NOT cover

- Tenant mutations, SDK code, API payloads, secrets, exact application values, executable mobile/web flows, or production biometric-policy decisions.
- Government-document identity proofing as a substitute for Recognize; use the PingOne Verify reference when document verification is the primary concern.
- A claim that a user, device, biometric association, SDK, IDV Bridge, or authentication result is ready or valid merely because another integration surface is configured.

Treat this as orientation, not an enrollment or authentication implementation guide. Confirm the current Recognize documentation for the target SDK, browser, platform, and release.

## Research brief

Research two related planes:

- **Administrative/interface plane:** identify the Recognize tenant, user population, application channel, and intended scenario. Select the documented mobile SDK, Web SDK, server API, or IDV Bridge surface. If an existing KYC or identity-verification process supplies a portrait or selfie, determine whether the SaaS or on-premises IDV Bridge boundary applies. For workforce use, identify whether the Recognize Authenticator app, Web SDK, OIDC, or SAML wrapper is the host surface. Establish ownership for user/device lifecycle, secrets, client state, telemetry, and result verification.
- **Runtime/client plane:** determine whether the user is already enrolled, where face and device checks occur, what liveness or transaction context is available, and which application or host flow interprets the result. Enrollment establishes the biometric association before authentication. Authentication can support sign-on, step-up, and documented payment scenarios; account recovery and new-device activation are separate lifecycle paths. The exact callback, error, device, transaction, and result contract is SDK- and release-sensitive.

A documented high-level lifecycle is: prepare the selected client or server boundary; enroll the user through live enrollment or an IDV Bridge path; authenticate against the enrolled association; optionally extend the transaction with step-up, payment/dynamic-linking, PIN, signed-result, recovery, or new-device behavior; and manage device, telemetry, and lifecycle state. The exact inputs, callbacks, cryptographic handling, and terminal status behavior must come from the current Recognize references.

## Resource index

### Recognize overview and lifecycle

- [Recognize introduction](https://docs.pingidentity.com/recognize/introduction/introduction_to_p1recognize.html)
- [Enrollment](https://docs.pingidentity.com/recognize/introduction/enrollment.html)
- [Authentication](https://docs.pingidentity.com/recognize/introduction/authentication.html)
- [Account recovery](https://docs.pingidentity.com/recognize/introduction/account_recovery.html)
- [Component interoperability](https://docs.pingidentity.com/recognize/introduction/component-interoperability.html)

### Client and server integration surfaces

- [Mobile SDK guide](https://docs.pingidentity.com/recognize/mobile-sdk/mobile-sdk-guide.md)
- [Mobile SDK integration flows](https://docs.pingidentity.com/recognize/mobile-sdk/mobile-sdk-integration-flows.md)
- [Web SDK getting started](https://docs.pingidentity.com/recognize/web-sdk/web-sdk-getting-started.md)
- [Web SDK integration flows](https://docs.pingidentity.com/recognize/web-sdk/web-sdk-introduction-integration-flows.md)
- [Server API introduction](https://docs.pingidentity.com/recognize/mobile-sdk/mobile-sdk-server-api-getting-started.md)
- [Server API users, devices, and operations](https://docs.pingidentity.com/recognize/mobile-sdk/mobile-sdk-server-api-users.md)
- [JWT verification guidance](https://docs.pingidentity.com/recognize/mobile-sdk/mobile-sdk-jwt-best-practice.md)

### IDV Bridge and host boundaries

- [IDV Bridge introduction](https://docs.pingidentity.com/recognize/idv-bridge/idv-bridge-introduction.md)
- [IDV Bridge SaaS](https://docs.pingidentity.com/recognize/idv-bridge/idv-bridge-saas.md)
- [IDV Bridge on-premises](https://docs.pingidentity.com/recognize/idv-bridge/idv-bridge-on-premise.md)
- [IDV Bridge endpoints](https://docs.pingidentity.com/recognize/idv-bridge/idv-bridge-p1recognize-agent-endpoints.md)
- [PingOne Verify reference](../pingone-verify/README.md) — use to distinguish document and identity-proofing flows.
- [PingOne platform reference](../pingone/README.md) — use when the host request is PingOne platform administration rather than Recognize integration.

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Product boundary | Is the request biometric enrollment/authentication with Recognize, or document identity proofing with Verify? Which population and scenario are in scope? | Stop and clarify when Recognize and Verify boundaries are mixed. |
| Integration surface | Is the host mobile, web, server, workforce, OIDC/SAML, or an existing KYC/IDV process? Is the path live enrollment or IDV Bridge? | Verify the SDK, browser, platform, bridge deployment, and release support. |
| Enrollment readiness | Is the user enrolled, and who owns biometric association, device binding, client state, and recovery? | Authentication depends on the documented enrollment boundary; do not infer enrollment from account existence. |
| Runtime authentication | What face, device, liveness, session, and transaction context is available? Which result does the host application consume? | Check the selected SDK/API contract and distinguish documented result fields from inference. |
| Step-up and payments | Is this sign-on, sensitive-action step-up, payment authentication, or dynamic linking? Where are transaction details and signed results verified? | Verify current mobile/web support, cryptographic handling, and relying-party responsibilities. |
| Recovery and lifecycle | Does the design include device removal, new-device activation, backup, PIN, external IDs, or telemetry? | Treat lifecycle APIs and client behavior as separate from authentication. |
| Promotion and operations | What moves between environments, and what must be recreated or verified for SDKs, bridge agents, secrets, domains, and monitoring? | Recheck versions, browser/device support, keys, endpoints, data handling, and drift. |

## Guardrails and report

Keep these distinctions visible:

- Recognize provides biometric enrollment and authentication capabilities; PingOne Verify addresses a different document and identity-proofing boundary.
- Enrollment, authentication, account recovery, device lifecycle, IDV Bridge, and server administration are related but distinct surfaces. A configured SDK does not prove that a user is enrolled or that a device is trusted.
- Mobile SDK, Web SDK, server API, OIDC/SAML wrapper, workforce Authenticator, and IDV Bridge can have different ownership, inputs, callbacks, result verification, and promotion requirements.
- Liveness, biometric matching, signed transaction details, device state, and result statuses are release-sensitive. Do not promote local examples or UI behavior into universal defaults.
- Protect biometric data, keys, client state, telemetry, and recovery operations according to the current Recognize documentation and applicable privacy/security requirements; this brief does not establish retention or compliance commitments.

Report: (1) the Recognize scenario and host-surface boundary; (2) verified enrollment, device, client, bridge, and credential readiness; (3) documented runtime authentication and result behavior; (4) recovery, step-up/payment, promotion, operations, and unresolved checks; (5) facts versus inference, tenant-specific observations, and release-sensitive claims; and (6) the appropriate handoff to the [PingOne Recognize reference](./README.md), the [PingOne Verify reference](../pingone-verify/README.md), or current official documentation. Do not turn the report into an SDK or authentication runbook.
