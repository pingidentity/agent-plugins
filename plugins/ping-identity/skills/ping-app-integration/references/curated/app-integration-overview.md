---
title: "Ping Identity App Integration — Overview"
product_family: cross-platform
products: ["pingone", "pingone-aic", "pingfederate", "pingaccess", "pingdirectory"]
capabilities: ["app-integration"]
services: []
audience: ["developer", "architect"]
use_cases: ["customer", "workforce", "cross-platform"]
doc_type: concept
status: current
canonical: true
last_updated: "2026-06-03"
slug: "https://developer.pingidentity.com/pingone-api/platform/"
---

# Ping Identity App Integration — Overview

Orientation for developers choosing the correct SDK surface and integration pattern for embedding Ping Identity authentication into a web, mobile, or on-prem application.

## Scope

**Covers:**
- When to use this skill vs. `ping-foundation` (implementation vs. admin)
- SDK landscape: Android, iOS, JavaScript/React, DaVinci orchestration SDK, on-prem agents
- Integration lifecycle: setup → flow design → app-side wiring
- Routing table: developer task → SDK/surface → reference anchor

**Does NOT cover:**
- Platform-level setup, application registration, or tenant configuration — use `ping-foundation`
- Designing or building journeys and DaVinci flows — use `ping-orchestration`
- Universal services (Protect, Verify, Credentials) invocation patterns — use `ping-universal-services`
- Generic onboarding orientation — use `ping-quickstart`

## Skill positioning: implementation vs. administration

`ping-app-integration` covers the **developer's side** of a Ping Identity integration. It answers: "How do I write code that authenticates users through Ping?"

`ping-foundation` covers the **admin's side**: tenant setup, application records, custom domains, policies. An agent must complete those steps first (or in parallel) before the developer-side wiring can succeed.

A correct integration always requires both layers:

| Layer | Primary skill | Typical tasks |
|---|---|---|
| 1. Platform setup | `ping-foundation` | Create tenant, register OIDC application, configure sign-on policy, set redirect URIs |
| 2. Flow / journey design | `ping-orchestration` | Author Journey nodes, build DaVinci flows, configure MFA policies |
| 3. App-side wiring | `ping-app-integration` | Install SDK, initialize client, wire auth code flow, handle callbacks/collectors, store tokens |

When a user says "add Ping login to my app," the correct sequence is: complete platform setup and flow design first, then hand off to this skill for the SDK wiring.

## SDK landscape

### Android — PingOne Native SDK (Kotlin)

Gradle artifact: `com.pingidentity.sdks:android`

| Module | Purpose |
|---|---|
| `journey` | Renders Journey callbacks (Username/Password, OTP, Push, Biometric) |
| `davinci` | Drives DaVinci collectors in Jetpack Compose |
| `oidc` | Authorization code + PKCE, token management |
| `fido` | FIDO2 / passkey registration and assertion |
| `protect` | PingOne Protect signals collection |
| `externalidp` | Social login (Google, Apple, Facebook) via IdP-initiated flow |
| `binding` | Device binding and integrity attestation |
| `oath` | TOTP / HOTP soft-token generation |
| `push` | Push notification–based MFA (FCM/APNs) |

Reference: `references/curated/mobile-integration-basics.md`

### iOS — PingOne Native SDK (Swift)

Swift Package: `Ping/ping-ios-sdk`

| Module | Purpose |
|---|---|
| `PingJourney` | Journey callbacks in SwiftUI / UIKit |
| `PingDavinci` | DaVinci collectors in SwiftUI |
| `PingOidc` | OIDC authorization code + PKCE, token management |
| `PingExternalIdP` | Social login via IdP-initiated flow |
| `PingProtect` | PingOne Protect signals |
| `PingOath` | TOTP / HOTP soft-token generation |
| `PingLogger` | Structured debug logging |
| `PingStorage` | Keychain-backed secure token storage |

Reference: `references/curated/mobile-integration-basics.md`

### Web / JavaScript — Ping Orchestration JavaScript SDK

npm packages:

| Package | Purpose |
|---|---|
| `@forgerock/journey-client` | Journey callback rendering for web apps |
| `@forgerock/davinci-client` | DaVinci collector rendering for SPAs |
| `@forgerock/oidc-client` | OIDC token exchange, session management, silent renewal |

Supports React (stable), Angular, Vue, and vanilla JS.

Reference: `references/curated/web-integration-basics.md`

### DaVinci Orchestration SDK (cross-platform)

DaVinci flows are orchestrated server-side; the client SDK renders collectors. The same DaVinci flow definition works with Android, iOS, and JavaScript clients — only the rendering layer differs.

Routing rule: if the user asks about designing the flow → `ping-orchestration`; if they ask about rendering collectors in their app → `ping-app-integration`.

### On-prem agents — PingFederate / PingAccess

| Agent type | Use case |
|---|---|
| PingFederate Java Integration Kit | Add SSO/federation to Java EE apps |
| PingAccess Agent SDK | Policy enforcement point for web apps behind PingAccess |
| PingFederate OAuth AS integration | Existing apps adopting OAuth2/OIDC via PF as the AS |
| PingFederate SAML SP connector | SAML SP-initiated SSO from third-party apps |

On-prem agents are configured at the PingFederate/PingAccess level; app-side changes are typically limited to redirect URI handling and token validation.

## Developer task → reference routing table

| Developer task | SDK / surface | Curated reference |
|---|---|---|
| Android Journey or DaVinci integration | Android SDK | `references/curated/mobile-integration-basics.md` |
| iOS Swift Journey or DaVinci integration | iOS SDK | `references/curated/mobile-integration-basics.md` |
| React / JavaScript OIDC web app | JS SDK / generic OIDC | `references/curated/web-integration-basics.md` |
| Browser-based hosted login (redirect) | Generic OIDC + browser flows | `references/curated/web-integration-basics.md` |
| SAML SP integration (web app) | SAML (PingFederate / PingOne) | `references/curated/web-integration-basics.md` |
| Redirect URI mismatch, CORS errors, token failures | All surfaces | `references/curated/integration-troubleshooting-basics.md` |
| ForgeRock → Ping SDK migration (Android/iOS/JS) | All SDK surfaces | `references/curated/integration-troubleshooting-basics.md` (migration section) |
| Platform setup / app registration | Admin surface | `ping-foundation` skill |
| Flow or journey design | DaVinci / Journey | `ping-orchestration` skill |

## Integration lifecycle

A production-ready integration passes through three phases. This skill owns Phase 3.

### Phase 1 — Platform setup (ping-foundation)

- Tenant provisioning (PingOne MT, AIC, or PF license install)
- Application record creation (OIDC client ID, client secret, redirect URIs)
- Sign-on policy / authentication policy attachment
- Custom domain and certificate configuration
- User population or directory integration

**Handoff point:** Phase 1 is done when the application has a stable client ID, at least one redirect URI registered, and a policy attached.

### Phase 2 — Flow design (ping-orchestration)

- Journey node graph authored (AIC / PingAM)
- DaVinci flow logic defined (PingOne MT)
- MFA policies and risk signal routing configured
- Callbacks / collectors identified for the app to render

**Handoff point:** Phase 2 is done when the flow runs end-to-end in the admin preview and produces the expected token.

### Phase 3 — App-side wiring (ping-app-integration — this skill)

- SDK installed (Gradle / SPM / npm)
- SDK initialized with client ID, redirect URI, and scopes
- Auth code + PKCE flow wired to the login entry point
- Callbacks / collectors rendered in the app UI
- Tokens received and stored in platform-secure storage
- Session refresh and logout implemented

## Prerequisites

- An application record exists in the Ping platform (client ID and redirect URI registered)
- The flow or journey is functional (tested in the admin preview)
- Target platform SDK version requirements: Android API 23+, iOS 14+, Node.js 16+ for JS
- Network access from the app to the Ping AS token endpoint (no corporate proxy blocking)

## Common variants

| Variant | Note |
|---|---|
| PingOne MT (multi-tenant cloud) | Use `@forgerock/davinci-client` or Android/iOS DaVinci modules; flows are DaVinci-based |
| PingOne AIC / ST (single-tenant) | Use `@forgerock/journey-client` or Android/iOS Journey modules; flows are Journey-based |
| PingFederate on-prem | OIDC or SAML from PF; no native Ping SDK needed unless also using MFA; agent-based enforcement via PingAccess |
| ForgeRock SDK (legacy) | Being replaced by Ping native SDKs; migration guide in `references/curated/integration-troubleshooting-basics.md` |

## Related references

- `references/curated/mobile-integration-basics.md` — Android and iOS SDK wiring
- `references/curated/web-integration-basics.md` — JavaScript / React / OIDC / SAML web integration
- `references/curated/integration-troubleshooting-basics.md` — Failure modes and migration path
- `references/runtime/docs-mcp-routing.md` — Escalation to Docs MCP when curated content is insufficient

## Source

[Ping Identity Developer Documentation](https://developer.pingidentity.com/pingone-api/platform/)
