# PingOne Recognize

## Overview
PingOne Recognize supports biometric enrollment, authentication, account recovery, and workforce scenarios. Enrolled users verify face, device, and presence with liveness checks for multi-factor security.

## Core Concepts
- **Enrollment** registers a face and device and creates a biometric template; Live Enrollment captures facial biometrics with passive liveness.
- **Authentication** covers sign-on, sensitive-action step-up, and payment authentication with strong customer authentication and dynamic linking.
- **Mobile and Web SDKs** add enrollment and authentication to applications and browser services.
- **IDV Bridge** reuses existing KYC or IDV biometric imagery for enrollment, with SaaS and on-premise options.
- **Client state** supports web/mobile interoperability and replacement-device binding after another factor and selfie verification.

## When to use
- Add biometric login or step-up verification to a mobile or web application.
- Reuse existing KYC or IDV imagery.
- Support payment authentication, account recovery, or workforce employee authentication.

## When not to use
- Enrollment is required before authentication.
- IDV Bridge requires an existing biometric template or image from an external identity process.
- Workforce is employee-focused; choose another path for consumer enrollment.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/recognize/introduction/introduction_to_p1recognize.html)
