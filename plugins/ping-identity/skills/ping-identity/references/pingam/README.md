# PingAM

## Overview
PingAM is an access management platform for protecting resources and controlling user access. It supports authentication, single sign-on, authorization, federation, and OAuth 2.0, OpenID Connect, and SAML 2.0.

## Core Concepts
- **Authentication journeys:** Configurable mechanisms, node-and-tree journeys, and multi-factor checks support identity verification.
- **Single sign-on:** One sign-in provides access to multiple services, reducing repeated authentication.
- **Authorization policies:** Policies define protected resources and access conditions for consistent access decisions.
- **Federation and protocols:** External identity providers and standard protocols connect applications and identity domains.
- **Realms and identity stores:** Realms organize user groups, while configurable identity-store connections support local identity data.
- **Security and operations:** Documentation covers infrastructure, cryptography, configuration, maintenance, monitoring, logs, and troubleshooting.

## When to use
- Centralize authentication, single sign-on, and policy-based access for applications and services.
- Integrate external identity providers or standard federation and authorization protocols.

## When not to use
- Do not treat this overview as a substitute for environment-specific security design.
- For detailed protocol behavior or feature protections, use PingAM’s dedicated protocol and security documentation.

## Journey design notes
- **Realm separation:** Reserve the root realm for administrative operations; run journey work in a dedicated realm (for example, `alpha`).
- **Redirect trust is deny-by-default:** Only `goto`/redirect targets explicitly configured in the redirect validation are honored after journey completion — configure the trusted set before journeys hand control back to applications.
- **Session posture is part of the security outcome:** Session lifetime, idle timeout, and client-side session settings should be chosen deliberately, because session behavior is a core part of what the tree enforces.

## Configuration Management and Runtime Interfaces

Use the interface-specific handoff only after confirming that the target is self-managed PingAM. Do not substitute PingOne cloud or Advanced Identity Cloud surfaces.

| Request signal | Use when | Reference |
|---|---|---|
| REST API | Route a release-specific PingAM REST or protocol task to the API-area inventory | [PingAM API handoff](api.md) |
| Administration CLI | Automate self-managed PingAM configuration or operations | [PingAM administration CLI](cli.md) |
| Terraform | Assess infrastructure-as-code coverage | No PingAM Terraform provider or resource coverage is asserted here; verify the target release and provider documentation before using Terraform. |

## Integrations

- [Integrating PingOne Protect](blueprint-integrating-pingone-protect.md) - Research boundary for self-managed PingAM Protect authentication nodes and the PingAM-to-PingOne connection.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/pingam/latest/index.md)
