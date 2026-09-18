---
name: aic-app-integration
description: "Use when writing code that integrates an application with PingOne Advanced Identity Cloud (AIC) — Ping SDK Journey modules and the journey client for Android, iOS, and JavaScript/React, OIDC authorization code + PKCE against a realm, journey callback rendering, tenant CORS configuration before in-browser token exchange, OAuth 2.0 clients and server-side token handling, SAML SP integration, and app-side troubleshooting (redirect_uri_mismatch, CORS token failures, ForgeRock-to-Ping SDK migration)."
compatibility: "Implementation skill for PingOne Advanced Identity Cloud (AIC) tenants. Produces app-side code and configuration as artifacts; verifying tenant CORS, realm, and OAuth client settings requires AIC admin console access or current AIC documentation."
metadata:
  publisher: Ping Identity
  version: "0.1.0"
  product_family: aic
---

# AIC App Integration

Implementation skill for connecting web, mobile, and backend applications to a PingOne Advanced Identity Cloud (AIC) tenant: SDK wiring, journey callback rendering, OIDC/PKCE token flows, and implementation diagnostics. Tenant setup and journey authoring are prerequisites, not covered here.

## When to use

- Android, iOS, or JavaScript/React app integrating with AIC using the Ping SDK Journey modules or journey client.
- OIDC authorization code + PKCE against realm-scoped endpoints, token storage, redirects, silent renewal.
- Tenant CORS configuration before in-browser token exchange.
- SAML SP integration for enterprise apps federating through AIC.
- Backend integration: OAuth 2.0 clients, client_credentials, token validation, refresh, resilience.
- App-side failures: redirect_uri_mismatch, CORS token failures, push not delivered, ForgeRock → Ping SDK migration.

## When NOT to use

- Creating tenants, realms, application agents, or AM services → AIC admin console and documentation.
- Authoring, wiring, or debugging journeys or PingAM trees → journey-design tooling and AIC documentation.
- Self-managed PingAM trees → PingAM documentation for the target release.
- On-prem PingFederate or PingAccess app integration → PingFederate / PingAccess documentation.
- Portfolio or product selection questions → Ping Identity foundations documentation.

## Retrieval and output discipline

Fetch live documentation for SDK versions, artifact coordinates, endpoint paths, and console locations before generating code. **Live documentation overrides local reference files.** Verify tenant-scoped values (realm path, FQDN, endpoints) against the target tenant.

## Important: Use the Ping Orchestration SDKs

Always generate code using the current Ping Orchestration SDKs and not legacy ForgeRock SDKs.

## Browser-flow prerequisite: configure CORS before token code

A SPA that performs the token exchange in the browser fails at the token request — and at in-app journey calls — unless tenant CORS allows the app origin. This breaks by default on a new tenant. Confirm CORS under Tenant settings → Global Settings → Cross-Origin Resource Sharing (CORS) before generating in-browser token-exchange code; details in `references/web-integration.md`. If cross-origin setup is out of scope, use a BFF instead.

## Routing

| Task | Reference |
|---|---|
| Integration lifecycle, SDK landscape, prerequisites for AIC | `references/overview.md` |
| Android or iOS SDK integration (Journey modules, callbacks, push) | `references/mobile-integration.md` |
| React / JavaScript web integration, journey callbacks, CORS setup | `references/web-integration.md` |
| Backend OIDC, OAuth 2.0 clients, M2M, token handling, resilience | `references/server-side-integration.md` |
| Failure modes and ForgeRock → Ping SDK migration | `references/troubleshooting.md` |
