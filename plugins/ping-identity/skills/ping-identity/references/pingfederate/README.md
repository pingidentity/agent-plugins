# PingFederate

## Overview
PingFederate is an enterprise federation and authentication platform for identity-based application access. It provides a shared authentication authority that can streamline access for customers, employees, and business partners across application environments.

## Core Concepts
- **Identity federation** connects identity and access across application environments, supporting consistent authenticated access.
- **Authentication** verifies users before they access protected applications.
- **Single sign-on (SSO)** streamlines authenticated access across applications and reduces repeated sign-ins.
- **Centralized authentication authority** gives organizations a shared point for authenticating internal and external populations.
- **Population-aware access** supports customer, workforce, and partner application-access scenarios.

## When to use
- Use it when customers, employees, or partners need federated authentication or SSO across applications.
- Use it when an organization wants a centralized authority for application authentication.

## When not to use
- Do not treat this overview as installation, administration, or development guidance; use the corresponding PingFederate documentation for those needs.
- Do not infer specific protocols, deployment models, integrations, licensing, or service commitments from this summary; confirm them in the applicable product documentation.

## Integrations

- [Integrating PingOne Authorize](blueprint-integrating-pingone-authorize.md) - Research boundary for PingFederate-adjacent PingOne Authorize decisions, host enforcement, and the unresolved native-adapter boundary.
- [Integrating PingOne Credentials](blueprint-integrating-pingone-credentials.md) - Research boundary for PingFederate-adjacent credential issuance or presentation, wallet/verifier roles, and the absence of an assumed native adapter.
- [Integrating PingOne DaVinci](blueprint-integrating-pingone-davinci.md) - Research boundary for the PingOne DaVinci Adapter, flow/application launch surfaces, and PingFederate authentication-policy handoff.
- [Integrating PingOne MFA](blueprint-integrating-pingone-mfa.md) - Research boundary for the Customer-environment PingOne MFA Integration Kit, PingFederate authentication-policy handoff, and the separate Workforce PingID boundary.
- [Integrating PingOne Protect](blueprint-integrating-pingone-protect.md) - Research boundary for the PingFederate Protect Integration Kit, adapters, provider, and authentication-policy path.
- [Integrating PingOne Verify](blueprint-integrating-pingone-verify.md) - Research boundary for PingFederate-hosted PingOne Verify proofing transactions, capture channels, result handling, and policy handoff.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/pingfederate/latest/index.md)
