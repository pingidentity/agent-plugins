# Data and Application Security Use Cases

## Overview
Data and Application Security Use Cases brings together scenarios for authentication, application access control, identity integration, and protection of Ping applications and gateways. It spans PingOne, PingFederate, PingAccess, external identity providers, and cloud platforms.

## Core Concepts
- **AWS EKS authentication:** Uses OpenID Connect (OIDC) with PingOne as the identity provider to support strong user authentication for EKS clusters.
- **Application access control:** Combines Azure AD, PingFederate, and PingAccess for medium-grained application access control.
- **OIDC integration:** Connects PingFederate and PingAccess through OIDC, supporting standards-based authentication between the products.
- **External identity providers:** Uses PingFederate as a service provider through FedHub to protect PingAccess resources with external identity providers.
- **Gateway protection:** Places PingAccess in a gateway deployment to proxy and protect PingFederate.

## When to use
- When securing AWS EKS cluster access with PingOne-backed OIDC authentication.
- When integrating Azure AD, PingFederate, and PingAccess for application access control.
- When selecting an OIDC, external-identity-provider, or gateway protection scenario for Ping products.

## When not to use
- Not as a detailed implementation procedure; use the relevant product documentation for configuration steps and prerequisites.
- Not for scenarios outside these listed integrations; identify the product-specific or platform-specific documentation instead.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/solution-guides/data_and_application_security_use_cases/htg_data_and_app_security_use_cases.md)
