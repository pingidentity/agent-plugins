# PingOne Platform

## Overview
PingOne is a cloud-based, multi-tenant identity-as-a-service framework for secure identity access management. Its organization-based model structures tenant accounts and related entities while bringing identity, security, authorization, and administration capabilities together.

## Core Concepts
- **Organization model:** Defines tenant accounts and related entities, giving customers a structured foundation for managing PingOne resources.
- **Access and authentication:** Supports single sign-on, authentication, and strong authentication/MFA to secure access to applications and services.
- **Threat protection and verification:** PingOne Protect provides threat protection, while PingOne Verify supports identity verification for higher-confidence interactions.
- **Credentials and authorization:** PingOne Credentials provides digital credentials, and PingOne Authorize supports authorization decisions.
- **Platform administration:** Administration, user profiles, monitoring, directories, applications, integrations, user experience, and environment settings support ongoing platform operations.

## When to use
- Use PingOne for cloud identity access management spanning authentication, application access, security, and authorization.
- Use it when tenant organization and centralized administration are important to the identity program.

## When not to use
- Do not treat this landing-page overview as detailed implementation or API guidance; use the linked product documentation for those needs.
- For support, training, community, or partner resources, use the separate destinations provided by the official documentation.

## Platform Components

PingOne is the platform; the following PingOne Services are reusable identity building blocks within it. Solutions and use cases describe how those building blocks are packaged or applied for a particular audience, outcome, or scenario; they are not additional peer services.

### Composable Services

- [**PingOne SSO**](../pingone-sso/README.md) - Single sign-on, identity-provider, OpenID Provider, and token-issuer capabilities.
- [**PingOne MFA (Strong Authentication)**](../pingone-mfa/README.md) - Multi-factor authentication for Customer and Workforce environments. PingID is a related, separately administered Workforce MFA product that can integrate with PingOne.
- [**PingOne Protect**](../pingone-protect/README.md) - Threat protection and risk detection for identity interactions.
- [**PingOne Verify**](../pingone-verify/README.md) - Identity verification and proofing capabilities.
- [**PingOne Credentials**](../pingone-credentials/README.md) - Verifiable digital credentials and wallet capabilities.
- [**PingOne Authorize**](../pingone-authorize/README.md) - Authorization decisions for applications and APIs.

### Related orchestration offering

- [**PingOne DaVinci**](../pingone-davinci/README.md) - An orchestration platform for composing IAM flows. It is adjacent to the core PingOne Services above and is commonly used by solution and flow packs; it is not an additional environment-level service in this list.

## Solutions and use cases

Solutions package PingOne Services for an audience or outcome. Solution and flow packs provide more focused, often prebuilt journeys; use-case guides describe scenarios that can combine PingOne with other Ping products or integrations. None of these layers is an additional PingOne Service.

### PingOne solution packages

- **PingOne for Customers** - Customer identity capabilities, with Essential and Plus package levels.
- **PingOne for B2B** - Business-to-business and partner identity capabilities, with Essential and Plus package levels.
- **PingOne for Workforce** - Workforce identity, application access, and workforce integration capabilities, with Essential and Plus package levels.
- **Agent IAM Core** - Identity and access foundations for AI agents, with optional capabilities.

### Solution and flow packs

- [**PingOne for Customers Passwordless**](../pingone-for-customers-passwordless/README.md) - Preconfigured passwordless customer registration, sign-on, profile, and recovery journeys.
- [**PingOne for Customers Plus**](../pingone-for-customers-plus/README.md) - Prebuilt customer registration, authentication, profile-management, and recovery journeys using PingOne and DaVinci. This separately documented flow pack should not be confused with the Plus package level above.
- [**PingOne for Financial Services**](../pingone-for-financial-services/README.md) - Industry-oriented journeys for financial-services interactions.
- [**PingOne for Gift Card Redemption**](../pingone-for-gift-card-redemption/README.md) - Gift-card redemption, step-up authentication, and user-information journeys.
- [**PingOne for Healthcare**](../pingone-for-healthcare/README.md) - A healthcare flow pack for account access and management journeys.

### Cross-product use cases

Use-case indexes describe implementation scenarios rather than a product hierarchy:

- [**Customer identity**](../customer-use-cases/README.md) - Customer sign-on, application access, self-service, recovery, and synchronization scenarios.
- [**Workforce identity**](../workforce-use-cases/README.md) - Workforce application access, federation, authentication, and lifecycle scenarios.
- [**MFA**](../mfa-use-cases/README.md) - Multi-factor authentication method and policy scenarios.
- [**Single sign-on or federation**](../single-sign-on-use-cases/README.md) - Standards-based sign-on and federation scenarios.
- [**Data or application security**](../data-and-application-security-use-cases/README.md) - Application access control, gateway protection, and identity integration scenarios.
- [**Standards or protocols**](../standards-and-protocols-use-cases/README.md) - Protocol and standards-oriented integration scenarios.

Use the [Solutions routing](../../SKILL.md#solutions-routing) and [Use cases routing](../../SKILL.md#use-cases-routing) tables in this skill's `SKILL.md` to select the focused reference. The routing tables remain the source of truth for exact destinations; consult the routed reference and current Ping Identity documentation for scope and implementation details.

## Configuration Management and Runtime Interfaces

Configuration can be managed in the console or programmatically using API, CLI or Terraform.

| Request signal | Use when | Reference |
|---|---|---|
| CLI | Making live changes to service configuration, generating shell scripts for CI/CD or developer workflows | `cli.md` |
| REST API | Generating application code with API calls to the service, creating API-focused scripts | `api.md` |
| Terraform | Declaritive configuration-as-code, generating/validating Terraform code | `terraform.md` |

## Gotchas

- Platform limits are in place for paid and trial tenants: [PingOne platform limits](https://docs.pingidentity.com/pingone/getting_started_with_pingone/p1_platform_limits.html)
- **Admin MFA enrollment is mandatory** — the first admin console sign-on always triggers MFA enrollment (email passcode or authenticator app); it cannot be skipped and completes before the Environments page is accessible.
- **Admin console session thresholds are not configurable** — the console re-prompts for authentication after inactivity, and re-prompts MFA if the last sign-on was long ago.
- **Keep all admin identities in the dedicated Administrators environment**, not in end-user environments.
- **Licensing model:** license types include ADMIN, TRIAL, SOLUTION, and JIT_TRIAL (and combinations); a PingOne environment has exactly **one license**; MAU/AAU limits may be soft or hard depending on contract; DaVinci metering is identity- vs transaction-based per contract. Trial environments carry strict quotas and expire — plan a separate production tenant rather than promoting a trial. Fetch current numbers from the platform-limits page above.
- **PingOne for Enterprise (P14E) identification:** `admin.pingone.com` with four sub-variants identifiable from the top navigation (Standard: Dashboard/Apps/Users/Setup/Account; MSP adds Customers; SSO-for-SaaS adds Customer Connections; Managed Accounts adds Customer Connections + Managed Accounts). P14E is a different product to PingOne.  P14E is now legacy with limited new feature investment.  Customers can migrate to PingOne.

## Integrations

- [Integrating applications](blueprint-integrating-applications.md) - Research boundary for application launch surfaces (sign-on policy, DaVinci flow policy), application CORS settings, and Worker applications.
- [Integrating PingOne Authorize](blueprint-integrating-pingone-authorize.md) - Research boundary for PingOne Authorize decision evaluation across APIs, gateways, DaVinci, CloudFront, and external OAuth integrations.
- [Integrating PingOne Credentials](blueprint-integrating-pingone-credentials.md)
- [Integrating PingOne DaVinci](blueprint-integrating-pingone-davinci.md) - Research boundary for DaVinci flows, connectors, applications, launch surfaces, and connected-product handoffs.
- [Integrating PingOne MFA](blueprint-integrating-pingone-mfa.md) - Research boundary for PingOne MFA environment readiness, policy and device flows, native SDK/API surfaces, and DaVinci or related host integrations.
- [Integrating PingOne Privilege](blueprint-integrating-pingone-privilege.md) - Research boundary for Privilege deployment models, privileged-access targets, network surfaces, and documented workflow integrations.
- [Integrating PingOne Protect](blueprint-integrating-pingone-protect.md) - Research boundary for PingOne platform, DaVinci, and direct Protect API/Signals integrations.
- [Integrating PingOne Recognize](blueprint-integrating-pingone-recognize.md) - Research boundary for Recognize enrollment, authentication, SDK/API, IDV Bridge, and host-application surfaces.
- [Integrating PingOne SSO](blueprint-integrating-pingone-sso.md) - Compact research boundary for SSO attached to a PingOne environment and used through an application sign-on policy or PingOne DaVinci flow.
- [Integrating PingOne Verify](blueprint-integrating-pingone-verify.md) - Research boundary for Verify policy, capture, transaction, and host-platform integrations.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Introduction to PingOne](https://docs.pingidentity.com/pingone/introduction_to_pingone/p1_introduction.html)
- [PingOne Platform documentation](https://docs.pingidentity.com/pingone/p1_cloud__platform_main_landing_page.md)
- [PingOne Solutions](https://docs.pingidentity.com/pingone-solutions/index.md)
- [Use Cases Overview](https://docs.pingidentity.com/solution-guides/htg_overview.html)
