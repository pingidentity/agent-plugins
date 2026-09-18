# PingOne MFA Native SDK

PingOne MFA provides native mobile SDK documentation for Android and iOS applications. Use the SDK flow and platform guides for mobile enrollment and authentication; do not confuse this path with PingOne Protect risk-evaluation SDKs.

## Intent routing

| Request signal | Use when | Continue with |
|---|---|---|
| Flow selection | Choose automatic enrollment, automatic device authorization, or authentication-code flow | [MFA SDK flows](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-mfa-mobile-sdks/pingone-mfa-mobile-sdk-flows.html) |
| Android implementation | Embed PingOne MFA in a native Android application | [PingOne MFA Android SDK](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-mfa-mobile-sdks/pingone-mfa-mobile-sdk-for-android.html) |
| iOS implementation | Embed PingOne MFA in a native iOS application | [PingOne MFA iOS SDK](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-mfa-mobile-sdks/pingone-mobile-sdk-for-ios.html) |
| SDK errors | Interpret documented native SDK error codes | [MFA SDK error codes](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-mfa-mobile-sdks/pingone_mfa_sdk_errror_codes.html) |
| Orchestrated app flow | Render a DaVinci or journey flow rather than calling MFA directly | [Orchestration SDKs](../orchestration-sdks/README.md) |
| Threat signals | Evaluate risk around authentication rather than enroll or authenticate an MFA device | [PingOne Protect](../pingone-protect/README.md) and its [native SDKs](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-risk-sdks/risk_evaluation_sdk.html) |

## Boundary

The native SDK landing page documents Android and iOS guides but does not classify every SDK flow by Customer or Workforce audience or specify all supported versions. The environment documentation identifies Workforce native-mobile support as Singapore-limited; verify current applicability before implementation. Deep client implementation belongs in the official SDK documentation or the companion SDK skill, not in this portfolio index.

## Source

- [PingOne MFA Native SDK overview](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-mfa-mobile-sdks.html)
- [PingOne Strong Authentication integrations](https://docs.pingidentity.com/pingone/strong_authentication_mfa/p1_strong_authentication_integrations.html)
