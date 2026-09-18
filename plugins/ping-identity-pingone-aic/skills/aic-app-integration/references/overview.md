# AIC — App Integration Overview

Orientation for connecting applications to a PingOne Advanced Identity Cloud (AIC) tenant: which SDK surfaces apply and how the integration lifecycle fits together. Implementation detail lives in the sibling references.

## Scope

**Covers:** integration lifecycle (tenant prerequisites → journey availability → app-side wiring), the Ping SDK landscape for AIC targets, and prerequisites for each phase.
**Does NOT cover:** tenant, realm, or application-agent administration — AIC admin console and documentation. Journey or tree authoring — journey-design documentation. SDK implementation steps — `mobile-integration.md`, `web-integration.md`, `server-side-integration.md`.

---

## App-side positioning

This material covers the developer side of an AIC integration: writing code that authenticates users through AIC journeys and realm-scoped OAuth 2.0 endpoints. Tenant setup, application agents, AM services, and journey configuration must be available before app-side wiring can succeed.

A correct integration includes these layers:

| Layer | Prerequisite or implementation | Typical tasks |
|---|---|---|
| 1. Tenant setup | Environment prerequisite | Tenant, realm (Alpha/Bravo), application agent (client ID, redirect URIs, scopes), AM services |
| 2. Journey design | Flow prerequisite | Journey node graph authored, tested end-to-end in the realm |
| 3. App-side wiring | This material | Install SDK, initialize journey client, render callbacks, store tokens |

## SDK landscape — AIC targets

### Android — PingOne Native SDK (Kotlin)

Gradle artifact: `com.pingidentity.sdks:android` (hosted on Maven Central and `maven.pingidentity.com`)

| Module | Purpose |
|---|---|
| `oidc` | Authorization code + PKCE, token management |
| `journey` | Renders Journey callbacks |
| `fido` | FIDO2 / passkey registration and assertion |
| `protect` | Risk signals collection |
| `push` | Push notification–based MFA |
| `externalidp` | Social login (Google, Apple, Facebook) via IdP-initiated flow |
| `binding` | Device binding and integrity attestation |
| `oath` | TOTP / HOTP soft-token generation |

### iOS — PingOne Native SDK (Swift)

Swift Package: `Ping/ping-ios-sdk`

| Module | Purpose |
|---|---|
| `PingOidc` | OIDC authorization code + PKCE, token management |
| `PingJourney` | Journey callbacks in SwiftUI / UIKit |
| `PingStorage` | Keychain-backed secure token storage |
| `PingExternalIdP` | Social login via IdP-initiated flow |
| `PingProtect` | Risk signals |
| `PingOath` | TOTP / HOTP soft-token generation |
| `PingLogger` | Structured debug logging |
| `PingFido` | FIDO2 / passkey registration and assertion (iOS 16+) |

### Web / JavaScript — journey client

| Package | Purpose |
|---|---|
| `@forgerock/journey-client` | Journey callback rendering for web apps |
| `@forgerock/oidc-client` | OIDC token exchange, session management, silent renewal |

Supports React (stable), Angular, Vue, and vanilla JS.

## Integration lifecycle

A production-ready AIC integration passes through three phases. This material owns Phase 3.

### Phase 1 — Tenant setup (tenant administration)

- Tenant and realm provisioning (Alpha for consumer/CIAM, Bravo for workforce)
- Application agent creation (client ID, redirect URIs, scopes)
- AM services configuration for the features the journeys depend on (push, OATH, WebAuthn, social identity providers, device profiles)
- Tenant CORS for the application origins

**Prerequisite condition:** Phase 1 is done when the application agent has a stable client ID, redirect URIs registered, and the required AM services are configured.

### Phase 2 — Journey design (journey design tooling)

- Journey node graph authored in the target realm
- MFA policies and risk signal routing configured
- Callbacks identified for the app to render

**Prerequisite condition:** Phase 2 is done when the journey runs end-to-end in the realm and produces the expected token.

### Phase 3 — App-side wiring (this material)

- SDK installed (Gradle / SPM / npm)
- Journey client initialized with client ID, realm path, and journey name
- Journey callbacks rendered in the app UI
- Tokens received and stored in platform-secure storage
- Session refresh and logout implemented

## Prerequisites

- An application agent exists in the tenant's realm (client ID and redirect URI registered)
- The journey is functional in the target realm (tested end-to-end)
- Target platform SDK requirements: Android API 23+, iOS 14+, Node.js 16+ for JS
- Network access from the app to the realm's OAuth 2.0 endpoints (no corporate proxy blocking)

## Common variants

| Variant | Note |
|---|---|
| AIC realms | Realm path scopes discovery, authentication, and OAuth endpoints; Alpha/Bravo are fixed |
| Self-managed PingAM | Journey model is shared; validate node availability against PingAM documentation for the target release |
| React Native | Uses the same JS SDK packages as React web; deep link handling differs (see Expo/React Native linking docs) |

## Source

- [PingOne Advanced Identity Cloud documentation](https://docs.pingidentity.com/pingoneaic/home.md)
- [Ping SDKs](https://developer.pingidentity.com/orchsdks/index.md)
