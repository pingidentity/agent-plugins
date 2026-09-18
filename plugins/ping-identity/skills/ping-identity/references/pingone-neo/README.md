# PingOne Neo

## Overview
PingOne Neo is a decentralized identity solution that gives control of identity data back to users. PingOne Neo empowers businesses to give their users full control over how they securely store and share verified credentials without unnecessary friction.

The PingOne Neo product is a combination of both [PingOne Credentials](../pingone-credentials/README.md) and [PingOne Verify](../pingone-verify/README.md) functionality.

## Core Concepts
- **Wallet setup:** A Neo-labelled starter flow sets up a user digital wallet, using PingID or a customer mobile app with the wallet native SDK.
- **Credential issuance:** After wallet pairing, the starter flow supports testing credential issuance into the wallet.
- **Credential presentation:** A Neo-labelled presentation-request flow supports testing credential sharing and verification.
- **Native wallet SDK:** A customer mobile app can run the wallet SDK so users can accept and share credentials.

## When to use
- Test wallet pairing and credential issuance.
- Validate credential presentation and verification.
- Build a native mobile wallet experience.

## When not to use
- For general credential creation or lifecycle administration, use the broader PingOne Credentials documentation.
- For implementation-specific SDK details, use the native wallet SDK documentation.
- For other PingOne capabilities, use the relevant product documentation.

## Client side integration

PingOne Neo provides client side native SDKs for both PingOne Wallet and PingOne Verify for both iOS and Android: [Native SDKs](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-neo-native-sdks.html)

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
