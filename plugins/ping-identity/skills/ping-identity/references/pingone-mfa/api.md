# PingOne MFA API

The PingOne MFA API provides administrative resources and device-authentication flows for the PingOne Strong Authentication service. Use the current API reference for request schemas, authorization, status handling, and environment-specific availability.

## Intent routing

| Request signal | Use when | Continue with |
|---|---|---|
| MFA settings | Read, update, or reset environment-level MFA settings | [MFA settings](https://developer.pingidentity.com/pingone-api/mfa/mfa-settings.html) |
| MFA policies | Configure method-specific device-authentication policies | [Device-authentication policies](https://developer.pingidentity.com/pingone-api/mfa/device-authentication-policy.html) |
| User MFA devices | Enable MFA for a user or manage registered devices | [User MFA devices](https://developer.pingidentity.com/pingone-api/mfa/users/mfa-devices.html) and [enable user MFA](https://developer.pingidentity.com/pingone-api/mfa/users/enable-users-mfa.html) |
| Pairing | Associate a native device and application with a user for push MFA | [MFA pairing keys](https://developer.pingidentity.com/pingone-api/mfa/users/mfa-pairing-keys.html) |
| Runtime authentication | Start or complete device selection, OTP, assertion, or push-confirmation steps | [Device authentications](https://developer.pingidentity.com/pingone-api/mfa/mfa-authentication/mfa-device-authentications.html) |

## Boundary

The API reference documents MFA resources and flows; it is not a substitute for native mobile SDK implementation or Workforce desktop/PingID integration guidance. PingOne MFA API operations do not establish that a method is available in every environment, geography, or license.

## Source

- [PingOne MFA API introduction](https://developer.pingidentity.com/pingone-api/mfa/introduction.html)
- [Read one bill of materials](https://developer.pingidentity.com/pingone-api/platform/bill-of-materials-bom/read-one-bill-of-materials.html)
