# Verified Trust

## Overview
Verified Trust is a cross-product solution guide, not a standalone product. It combines identity verification, authentication, authorization, and real-time threat detection to establish confidence that a person is genuinely using their identity.

The official solution examples document workforce help-desk implementations on [PingOne](https://docs.pingidentity.com/solution-guides/verified-trust/verified-trust-helpdesk-pingone.html) and [PingOne Advanced Identity Cloud](https://docs.pingidentity.com/solution-guides/verified-trust/verified-trust-helpdesk-aic.html).

For a high-level fulfillment sequence and critical configuration concepts, see the [workforce help-desk blueprint](blueprint.md). Use the owning product skills for platform-specific configuration and tool execution.

## Core Concepts
- **Identity security:** Authentication and authorization for the requested access.
- **Identity fraud prevention:** Protection against impersonation, synthetic identities, account takeover, and deepfake-based attacks.
- **Identity assurance:** Government-document checks, liveness, and biometric or facial binding that increase confidence in a claimed identity.
- **Contextual verification:** Repeated or risk-aware checks when authentication alone is not sufficient.
- **Reusable credentials:** Digital credentials can support verification across relevant interactions.

## When to use
- Verify candidates during hiring and onboarding before granting system access.
- Strengthen account recovery and workforce help-desk interactions.
- Apply a unified identity approach where authentication alone does not provide sufficient assurance.

## When not to use
- Do not treat this overview as an API, pricing, quota, release-state, or configuration reference.
- Do not assume that all platforms implement the solution identically.
- Do not use an external IdP as a substitute for Verify or infer unsupported product integrations.

## Capability Mapping

Use this as a routing hint. `Core` means the capability is shown in the documented help-desk solution; `Adjacent` means the portfolio has a related capability, but the Verified Trust help-desk flows do not establish it as required.

| Capability | PingOne composition | Advanced Identity Cloud composition |
|---|---|---|
| Operator access and orchestration | **Core:** PingOne SSO and PingOne DaVinci | **Core:** AIC journeys and backchannel journeys |
| Operator eligibility and user lookup | **Core:** DaVinci flow controls, PingOne groups, and user lookup | **Core:** AIC journey controls, groups, and identity matching |
| Identity proofing | **Core:** PingOne Verify for government ID, selfie, liveness, and facial/document comparison | **Core:** PingOne Verify invoked from AIC journeys through the PingOne Worker Service |
| Recovery outcome | **Core:** Verification result is returned; account reset is a separate flow | **Core:** The documented journey can continue to password or MFA-device recovery |
| Threat or contextual risk | **Adjacent:** PingOne Protect; not required by the documented help-desk flow | **Adjacent:** PingOne Protect; not required by the documented help-desk flow |
| Reusable digital credentials | **Adjacent:** PingOne Credentials; not shown in the help-desk flow | **Not established by the Verified Trust guide** |

Do not infer that PingOne Authorize, PingOne Protect, PingOne Credentials, Neo, or Recognize is required unless the selected implementation documents that integration.

## Platform/Product Integrations

- **PingOne:** Start with [PingOne](../pingone/README.md). The documented composition is [PingOne SSO](../pingone-sso/README.md) plus [PingOne DaVinci](../pingone-davinci/README.md) for operator access, lookup, orchestration, and outcome handling, and [PingOne Verify](../pingone-verify/README.md) for proofing. The flow also documents optional external-IdP, Jira, and ServiceNow integrations.
- **PingOne Advanced Identity Cloud:** Start with [Advanced Identity Cloud](../pingone-advanced-identity-cloud/README.md). The documented composition uses AIC journeys, backchannel processing, and the Worker Service with [PingOne Verify](../pingone-verify/README.md); do not substitute DaVinci for the AIC journey layer.
- **Other platform signals:** For PingOne Advanced Services, self-managed Advanced Identity Software, or Government Identity Cloud, route to the relevant platform reference first. The Verified Trust solution pages do not establish an equivalent product composition for those platforms; ask for the platform before recommending products.

## Third-party Identity-Provider Integrations

Universal-service or journey integrations are not limited to Ping products, but support is host-specific. PingOne documents external IdPs that conform to SAML or OIDC, including attribute mapping, and the PingOne Verified Trust help-desk flow provides an optional **Sign On with External Identity Provider** path. In that flow, the external IdP supplies authentication and user attributes; the help-desk agent still authenticates through PingOne and PingOne Verify remains the proofing service. See [PingOne external IdPs](https://docs.pingidentity.com/pingone/integrations/p1_external_idps.html) and the [PingOne help-desk flow](https://docs.pingidentity.com/solution-guides/verified-trust/verified-trust-helpdesk-pingone.html).

Do not generalize this option to every service, provider, or platform. The AIC Verified Trust help-desk guide does not establish external-IdP support for that flow, and an external IdP does not replace identity proofing.

## Scope and composition
Verified Trust packages capabilities from a host platform and its products; it is not another peer service. This README maps the documented compositions and routes to owning references.

For an implementation blueprint, see [Verified Trust Workforce Help-Desk Fulfillment Blueprint](blueprint.md).

## Related implementation contexts
- [PingOne platform](../pingone/README.md) — platform composition and service boundaries.
- [Advanced Identity Cloud](../pingone-advanced-identity-cloud/README.md) — AIC journey-hosting context.
- [PingOne Verify](../pingone-verify/README.md) — identity-proofing capability.
- [PingOne DaVinci](../pingone-davinci/README.md) — PingOne orchestration capability.
- [PingOne SSO](../pingone-sso/README.md) — sign-on and federation context.
- [PingOne Protect](../pingone-protect/README.md) — adjacent risk capability.
- [PingOne Credentials](../pingone-credentials/README.md) — adjacent credential capability.

## Source
- [Verified Trust overview](https://docs.pingidentity.com/solution-guides/verified-trust/verified-trust-overview.html)
- [Verified Trust help desk with PingOne](https://docs.pingidentity.com/solution-guides/verified-trust/verified-trust-helpdesk-pingone.html)
- [Verified Trust help desk with Advanced Identity Cloud](https://docs.pingidentity.com/solution-guides/verified-trust/verified-trust-helpdesk-aic.html)
- [Product Index](https://docs.pingidentity.com/product-index.html)
