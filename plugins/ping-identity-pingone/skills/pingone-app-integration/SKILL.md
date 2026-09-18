---
name: pingone-app-integration
description: "Use when writing code that integrates an application with PingOne (multi-tenant) — Ping SDK setup for Android, iOS, and JavaScript/React, OIDC authorization code + PKCE against auth.pingone.com, DaVinci client and collector rendering, CORS configuration before in-browser token exchange, Worker applications and client_credentials or token exchange for backends, push MFA device registration, and app-side troubleshooting (redirect_uri_mismatch, CORS token failures, ForgeRock-to-Ping SDK migration)."
compatibility: "Implementation skill for PingOne multi-tenant environments. Produces app-side code and configuration as artifacts; verifying CORS, redirect URIs, and application settings in a live tenant requires PingOne admin console access, PingOne MCP tools, or Ping CLI."
metadata:
  publisher: Ping Identity
  version: "0.1.0"
  product_family: pingone-mt
---

# PingOne App Integration

Implementation skill for connecting web, mobile, and backend applications to a PingOne environment: SDK wiring, OIDC/PKCE token flows, and implementation diagnostics. Platform setup and DaVinci flow authoring are prerequisites, not covered here.

## When to use

- Android, iOS, or JavaScript/React app integrating with PingOne (`auth.pingone.com`) using the Ping SDKs.
- OIDC authorization code + PKCE, token storage, redirects, and silent renewal against a PingOne environment.
- CORS configuration on the PingOne application before in-browser token exchange.
- Backend integration: Worker applications, client_credentials, token exchange, CIBA, refresh, resilience.
- App-side failures: redirect_uri_mismatch, CORS on `/as/token`, push not delivered, ForgeRock → Ping SDK migration.

## When NOT to use

- Creating the PingOne environment or application record, sign-on policies, or populations → PingOne admin console and documentation.
- Authoring, wiring, or debugging a DaVinci flow → DaVinci studio and flow documentation.
- On-prem PingFederate or PingAccess app integration → PingFederate / PingAccess documentation.
- Portfolio or product selection questions → Ping Identity foundations documentation.

## Retrieval and output discipline

Fetch live documentation for SDK versions, artifact coordinates, endpoint paths, and console locations before generating code. **Live documentation overrides local reference files.**

## Important: Use the Ping Orchestration SDKs

Always generate code using the current Ping Orchestration SDKs and not legacy ForgeRock SDKs.

## Browser-flow prerequisite: configure CORS before token code

A SPA that performs the token exchange in the browser fails at the token request — and at in-app `/as/authorize` calls — unless the application's CORS settings allow the app origin. This breaks by default on a new tenant. Confirm CORS under Applications → [app] → Configuration → CORS Settings before generating in-browser token-exchange code; details in `references/web-integration.md`. If cross-origin setup is out of scope, use a BFF instead.

## Routing

| Task | Reference |
|---|---|
| Integration lifecycle, SDK landscape, prerequisites for PingOne | `references/overview.md` |
| Android or iOS SDK integration (DaVinci collectors, push, storage) | `references/mobile-integration.md` |
| React / JavaScript web integration, CORS setup, browser flows | `references/web-integration.md` |
| Backend OIDC, Worker applications, M2M, token exchange, CIBA, retry/429 | `references/server-side-integration.md` |
| Failure modes and ForgeRock → Ping SDK migration | `references/troubleshooting.md` |
