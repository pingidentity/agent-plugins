# PingAccess

## Overview
PingAccess is a security product for protecting web applications and APIs. It applies security policies to requests from clients, giving customers a documented product area for policy-based application and API protection.

## Core Concepts
- **Client requests:** Requests from clients are the traffic to which PingAccess applies protection; this defines the product’s policy enforcement focus.
- **Security policies:** Policies are the mechanism applied to client requests, making them central to protecting the resources identified by the product.
- **Web applications:** Web applications are a primary protected resource type, making PingAccess relevant to application-protection needs.
- **APIs:** APIs are another explicitly supported protected resource type, extending the product’s scope beyond browser-facing applications.
- **Product operations:** Configuration, customization, integrations, monitoring, installation, backup, restoration, and upgrades are documented areas that support operating PingAccess across its lifecycle.

## When to use
- Protect web applications or APIs through policies applied to client requests.
- Consult PingAccess use-case, integration, configuration, or monitoring guidance for a PingAccess-specific requirement.

## When not to use
- Do not infer deployment models, protocols, policy types, or operational requirements from this landing-page summary; use the relevant PingAccess guides.
- For detailed installation, lifecycle, integration, or monitoring procedures, use the corresponding official documentation areas.

## Gotchas
- **PingAccess validates tokens but issues none** — its token provider must point at a real authorization server (PingFederate, PingAM, AIC or PingOne).
- **Web session cookies are domain-scoped** — wildcard domain configuration is needed for multi-subdomain applications.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/pingaccess/9.1/pa_landing_page.md)
