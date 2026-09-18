# App Integration

## Overview
Application integration is the discipline of embedding authentication into an application — web, mobile, or backend — so that users sign in through a Ping authorization server (PingOne, PingOne Advanced Identity Cloud, PingAM, or PingFederate) using OIDC/OAuth 2.0 or SAML. An integration spans prerequisites configured on the platform side and wiring inside the application itself. This topic is design orientation only: implementation detail lives in current product documentation and product-specific skills.

## Core Concepts
- **Three integration layers:** platform setup (tenant, application record, redirect URIs, sign-on policies) → flow or journey design (the authentication experience) → app-side wiring (SDK, token exchange, storage). App-side work presupposes the first two layers are complete.
- **Integration surfaces:** server-driven orchestration (the app renders flows or journey callbacks that the server directs), OIDC redirect and hosted login (the browser drives the flow), SAML federation for service-provider integration, and backend token patterns (BFF and service-to-service).
- **Orchestration SDK model:** DaVinci flows and AIC/PingAM journeys execute server-side while the client SDK renders the requested collectors or callbacks, so flow changes do not require app republishing where supported; a direct OIDC client, by contrast, owns the flow in the app.
- **Grant selection:** authorization code + PKCE for user sign-in, client credentials for machine-to-machine, token exchange for delegated access, CIBA for out-of-band approval. Choose by actor, platform, and trust model — not by habit.
- **Browser prerequisites:** CORS allow-listing and exact-match redirect URIs are environment prerequisites, not runtime concerns; a browser token exchange fails by default on a new tenant until origins are allowed.
- **Tokens and sessions:** ID, access, and refresh tokens have distinct roles; store them in platform-secure storage, refresh deliberately, and treat logout as both local session cleanup and server-side end.

## When to use
- An app integration is being planned and the question is what the integration involves, which surface fits, or which prerequisites must exist before code is written.
- Architecture or design discussions about where authentication logic should live (embedded flows, hosted login, BFF) or which grant type fits a use case.

## When not to use
- Do not treat this topic as API, SDK version, or configuration guidance; fetch current product documentation for exact parameters, artifact coordinates, and endpoints.
- For deep Android, iOS, JavaScript, or React implementation detail, use the SDK documentation for the target stack and product-specific skills.
- For protocol internals (OAuth 2.0, OIDC, SAML, WebAuthn), consult the standards and the product protocol documentation.

## Integrations
- [Authentication Orchestration](../orchestration/README.md) - Design principles for the authentication experience the app integrates with.
- [Ping Orchestration SDKs](../orchestration-sdks/README.md) - The SDK surfaces that embed orchestration in apps.
- [PingOne Platform](../pingone/README.md) - Multi-tenant platform whose environments host applications and DaVinci flows.
- [PingOne Advanced Identity Cloud](../pingone-advanced-identity-cloud/README.md) - Single-tenant platform whose journeys and application agents serve connected apps.
- [PingFederate](../pingfederate/README.md) - On-prem federation and OAuth authorization server for app integrations.

## Source
- [Ping Orchestration SDKs](https://developer.pingidentity.com/orchsdks/index.md)
- [OAuth 2.0 Framework (RFC 6749)](https://datatracker.ietf.org/doc/html/rfc6749)
- [Proof Key for Code Exchange (RFC 7636)](https://datatracker.ietf.org/doc/html/rfc7636)
