# PingGateway

## Overview
PingGateway is a reverse-proxy gateway between clients and protected web applications. It centralizes authentication and access controls.

## Core Concepts
- **Reverse proxy gateway:** Fronts HTTPS applications and can serve or proxy static resources, providing a boundary for web-application access.
- **PingAM integration:** Connects gateway-protected applications with PingAM for agent authentication, single sign-on (SSO), and cross-domain single sign-on (CDSSO).
- **Protocol integrations:** AM integrations support OAuth 2.0 and SAML 2.0 use cases, aligning access with identity protocols.
- **JSON configuration and extensibility:** Gateway behavior is configured with JSON and can be extended with Groovy scripts or Java plugins for deployment-specific needs.
- **Lifecycle operations:** Documentation covers installation, upgrades, maintenance, logging, and troubleshooting for gateway operators.

## When to use
- Protect web applications behind a gateway with centralized authentication and access control.
- Integrate applications with PingAM or use supported OAuth 2.0 and SAML 2.0 identity flows.
- Evaluate, install, and maintain a self-managed gateway deployment.

## When not to use
- This is not a complete API-management or service-mesh reference; the cited guide focuses on web-application reverse-proxy patterns.
- This is not a substitute for product-specific PingOne or Advanced Identity Cloud guidance; use integration documentation when those services are the primary focus.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/pinggateway/latest/index.md)
