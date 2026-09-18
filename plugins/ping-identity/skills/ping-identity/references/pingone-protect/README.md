# Threat Protection using PingOne Protect

## Overview
PingOne Protect is a PingOne capability for reducing identity fraud through advanced functionality and real-time detection. It helps organizations counter malicious actors, including password attacks and MFA fatigue.

## Core Concepts
- **Risk predictors:** Risk signals used to support fraud and threat assessment, helping organizations evaluate potentially harmful activity.
- **Third-party risk scores:** External risk information that can be applied alongside PingOne Protect, broadening the signals available for assessment.
- **Staging-policy risk data:** Risk information from staging policies that supports evaluation before applying decisions more broadly.

## Service integrations

- **PingOne Platform and PingOne DaVinci:** Use the [PingOne Platform](../pingone/README.md) and [PingOne DaVinci](../pingone-davinci/README.md) contexts for the native Protect connector integration.
- **Advanced Identity Cloud:** Use the [Advanced Identity Cloud](../pingone-advanced-identity-cloud/README.md) context for Protect journey-node integration.
- **PingFederate:** Use the [PingFederate](../pingfederate/README.md) context for the Protect Integration Kit and IdP Adapter integration.
- **PingAM:** Use the [PingAM](../pingam/README.md) context for documented Protect authentication-node integration with self-managed AM.
- **Third-party identity providers or systems:** Integrate with Protect via API; use the [developer tools](../developer-tools/README.md) context for the API-oriented path rather than treating this as a generic federation adapter.
- **PingGateway:** Use the [PingGateway](../pinggateway/README.md) context for gateway-edge Protect evaluation and threat-level routing.
- **Protect API and Signals SDK:** Use the [developer tools](../developer-tools/README.md) context for direct API and SDK integration.

## When to use
- Assess identity risk while addressing malicious activity, password attacks, or MFA fatigue.
- Test predictors or evaluate staging-policy risk data before wider adoption.
- Apply third-party risk scores or integrate Protect with PingOne and related products.

## When not to use
- Do not treat this overview as a configuration or implementation procedure.
- Do not infer predictor behavior, scoring logic, performance, or coverage limits from this page.
- For detailed integration or risk-data behavior, use the dedicated product documentation rather than this high-level overview.

## Client Side Integration

PingOne Protect is expected to be integrated client side so risk signals are sent to the Protect service for live evaluation against configured risk policies.

Integration to iOS, Android and Web clients is achieved by including the [PingOne Protect Native SDKs](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-risk-sdks/risk_evaluation_sdk.html) into client side apps.

- [**iOS**](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-risk-sdks/risk_evaluation_sdk_ios.html)
- [**Android**](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-risk-sdks/risk_evaluation_sdk_android.html)
- [**Web**](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-risk-sdks/risk_evaluation_sdk_web.html)

## Source
- [Protect overview](https://docs.pingidentity.com/pingone/threat_protection_using_pingone_protect/p1_protect_overview.html)
- [Protect API](https://developer.pingidentity.com/pingone-api/protect/introduction.html)
