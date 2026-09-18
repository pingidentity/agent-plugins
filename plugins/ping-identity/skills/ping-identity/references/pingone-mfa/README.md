# PingOne MFA (Strong Authentication)

## Overview
PingOne MFA is PingOne's multi-tenant Strong Authentication service for Customer and Workforce users. Method availability depends on environment type, license, geography, and policy.

## Core Concepts
- **Policy:** MFA policies enable methods; Workforce deployments may also require registration and authentication policies.
- **Methods:** Common methods include passkeys/FIDO2, authenticator apps, email, SMS/voice, OATH, and native mobile. Customer environments can use WhatsApp; Workforce environments can use PingID mobile, YubiKey, and PingID desktop where supported.
- **Environment boundary:** Do not transfer methods or integrations between Customer and Workforce environments without checking current support. Workforce native-mobile support is geography-dependent, including the documented Singapore limitation.

## When to use
- Secure PingOne Customer or Workforce authentication with additional identity proof.
- Configure MFA methods, native mobile enrollment/authentication, or MFA administration through an execution surface.

## When not to use
- Start with [MFA use cases](../mfa-use-cases/README.md) for cross-product scenarios such as VPN, federation, or offline authentication.
- Do not treat [PingID](../pingid/README.md) as a synonym for PingOne MFA; it is a separately administered Workforce service.
- [PingOne Protect](../pingone-protect/README.md) evaluates risk, [PingOne Verify](../pingone-verify/README.md) performs identity verification, and [PingOne DaVinci](../pingone-davinci/README.md) orchestrates flows; none is the MFA service.

## Gotchas
- **An MFA policy has no effect unless it is attached to the sign-on policy assigned to the application** — creating the policy alone changes nothing.
- The TOTP method requires the user to have a `totpSecretKey` attribute in the identity store; extend the schema before enabling it.

## Integration and deployment contexts
| Context | Role | Continue with |
|---|---|---|
| Customer application or native mobile app | MFA enrollment and authentication | [Native SDK](sdk.md) and [API](api.md) |
| Workforce application or policy | Methods, registration, and authentication policies | [Strong Authentication configuration](https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_configuring_strong_authentication_start.md) |
| Workforce desktop, RADIUS, SSH, or federation | Service-dependent Workforce integration | [PingID](../pingid/README.md) and [Workforce use cases](../workforce-use-cases/README.md) |

## Service integrations

Integration availability depends on the environment type, geography, license, and whether the flow uses PingOne MFA or a separately administered PingID service.

| Host or integration context | Supported role | Continue with |
|---|---|---|
| PingOne APIs and worker application | Administrative and runtime MFA API access for Customer and Workforce environments | [API](api.md) |
| PingOne DaVinci | Customer flows use the PingOne MFA connector; Workforce flows generally use the PingID connector, while Workforce flows in Singapore use the PingOne MFA connector | [PingOne DaVinci](../pingone-davinci/README.md) and [PingID](../pingid/README.md) |
| PingFederate | Customer environments use PingOne with the PingOne MFA Integration Kit; Workforce federation or identity-bridge deployments use legacy PingID, with PingID adapter 2.17 or later required for PingID accounts integrated with PingOne | [PingFederate](../pingfederate/README.md) and [PingID](../pingid/README.md) |
| Workforce RADIUS Gateway | Connects Workforce strong authentication to RADIUS-compatible systems, including VPN scenarios; Singapore availability differs from legacy PingID integrations | [Workforce use cases](../workforce-use-cases/README.md) and [PingID](../pingid/README.md) |
| Microsoft Entra ID | Workforce integration uses PingID as the external MFA provider and requires PingOne SSO | [PingID](../pingid/README.md) and [PingOne SSO](../pingone-sso/README.md) |
| Workforce desktop and operating-system access | Platform SSO for macOS uses the PingID desktop app; legacy PingID integrations cover Windows login, passwordless Windows login, Mac login, and SSH outside Singapore | [PingID](../pingid/README.md) |
| PingOne Protect | Predictor-based registration and authentication rules can inform MFA decisions; Protect evaluates risk and does not enroll or authenticate an MFA factor | [PingOne Protect](../pingone-protect/README.md) |

## Configuration Management and Runtime Interfaces
| Surface | Use for | Reference |
|---|---|---|
| REST API | Settings, policies, devices, pairing keys, and device-authentication flows | [API](api.md) |
| CLI | MFA settings, device policies, FIDO2 policies, and user devices | [CLI](cli.md) |
| Terraform | Supported MFA settings, policies, FIDO2 policies, and push credentials | [Terraform](terraform.md) |
| Native SDK | Mobile MFA enrollment and authentication | [SDK](sdk.md) |

## Related products
- [PingOne](../pingone/README.md) hosts the MFA service.
- [PingID](../pingid/README.md) is a separate Workforce MFA service with its own integrations and policy model.
- [PingOne Protect](../pingone-protect/README.md) provides risk evaluation, not factor enrollment.
- [PingOne Verify](../pingone-verify/README.md) provides identity verification/proofing, not sign-on MFA.
- [PingOne DaVinci](../pingone-davinci/README.md) and [orchestration SDKs](../orchestration-sdks/README.md) compose application flows around authentication services.

## Source
- [PingOne Strong Authentication overview](https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_strong_authentication_start.html)
- [Customer and Workforce environment differences](https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_pid_what_is_the_difference.html)
- [PingOne MFA integrations](https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_strong_authentication_integrations.html)
