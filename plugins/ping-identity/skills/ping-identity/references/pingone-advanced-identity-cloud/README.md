# PingOne Advanced Identity Cloud

## Overview
PingOne Advanced Identity Cloud is a SaaS-based identity and access management platform for workforce, consumer, and B2B identities. It supports lifecycle management while Ping Identity operates deployment, administration, upgrades, and monitoring.

## Core Concepts
- **Identity and application management:** Manage identities and connect SaaS products, directories, or custom applications, supporting connected account administration.
- **Authentication journeys:** Node-based workflows support login, registration, recovery, and other tailored self-service experiences.
- **Node-and-tree journey model:** Journeys are graphs of nodes (credential collectors, decision nodes, page compositions, inner-journey calls) that end at terminal outcomes; pages group interactive nodes into a single user-facing step. This model is shared with self-managed PingAM, so journey designs port between them with product-specific adjustments.
- **Single sign-on and federation:** Applications can use OIDC, SAML, or WS-Federation so users authenticate through Advanced Identity Cloud.
- **Provisioning and synchronization:** Provisioning creates and maintains accounts in connected services, while cloud-to-on-premises synchronization connects identity environments.
- **Operations and policy:** Application policies, PingGateway enforcement, tenant monitoring, audit records, and debug logs support controlled access and operational visibility.

## When to use
- For workforce, consumer, or B2B identity programs needing a managed cloud IAM platform.
- When journeys, connected-application SSO, or account provisioning are central requirements.

## When not to use
- For implementation procedures, use the documentation for the relevant journey, application, identity, or tenant area.
- For another Ping product, consult that product’s authoritative documentation.
- This summary does not establish pricing, service limits, compliance claims, or protocol-specific requirements.

## Gotchas
- **Realm model is fixed:** a tenant has exactly two configurable end-user realms — Alpha (consumer/CIAM) and Bravo (workforce). The names are not renameable, and the top-level realm is tenant-admin-only. Alpha supports delegated administration and IGA; Bravo does not.
- **Administrator roles are tiered** (tenant administrator, super administrator, tenant auditor, brand administrator); only the super administrator manages other admins.
- **Stage separation is per tenant:** AIC uses separate tenant instances per stage, with configuration promoted via the AIC REST API or Ping Platform Config Manager.
- **Tenant security posture shapes journey design:** HTTPS-only usage, trusted cookie-domain configuration, CORS controls, and CSRF protections are part of secure tenant design, not add-ons; recovery journeys should rely on step-up authentication, risk signals, and verified, unique recovery identifiers.
- **AM services must precede dependent nodes:** Journey nodes that depend on platform services (push, OATH, WebAuthn, social identity providers, device profiles) fail at runtime, not design time, when the corresponding AM service is not configured in the tenant.

## Integrations
- [Integrating applications](blueprint-integrating-applications.md) - Research boundary for applications authenticating through AIC (OIDC/SAML agents, realm-scoped endpoints, tenant CORS).
- [Integrating PingOne Protect](blueprint-integrating-pingone-protect.md) - AIC journey integration for risk evaluation and adaptive outcomes.
- [Integrating PingOne Verify](blueprint-integrating-pingone-verify.md) - AIC journey integration for identity verification and proofing.
- [Integrating PingOne Credentials](blueprint-integrating-pingone-credentials.md) - AIC journey integration for wallet and verifiable-credential operations.

These are documented AIC-to-PingOne service integrations. AIC's native journeys and AM services provide MFA, authentication, SSO, and orchestration capabilities; do not infer separate AIC integrations for PingOne MFA, PingOne SSO, or PingOne DaVinci. PingOne Recognize, PingOne Authorize, and PingOne Privilege are also separate product boundaries and are not listed here without a current AIC-specific integration contract.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/pingoneaic/home.md)
