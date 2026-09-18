# PingOne — App Integration Overview

Orientation for developers integrating an application with a PingOne environment: which SDK surface to choose and how the integration lifecycle fits together. The implementation files cover each surface in detail.

## Scope

**Covers:** integration lifecycle (platform prerequisites → flow availability → app-side wiring), the Ping SDK landscape for PingOne targets (Android, iOS, JavaScript/React), and the prerequisites for each phase.
**Does NOT cover:** PingOne environment, application record, or policy creation — platform administration. DaVinci flow authoring — see flow-design documentation. SDK implementation steps — see `mobile-integration.md`, `web-integration.md`, `server-side-integration.md`.

---

## App-side positioning

This material covers the developer side of a PingOne integration: writing code that authenticates users against a PingOne environment. Platform setup, application records, custom domains, policies, and DaVinci flow configuration must be available before app-side wiring can succeed.

A correct integration includes these layers:

| Layer | Prerequisite or implementation | Typical tasks |
|---|---|---|
| 1. Platform setup | Environment prerequisite | PingOne environment, application record (client ID, redirect URIs), sign-on policy or flow policy, populations |
| 2. Flow design | Flow prerequisite | DaVinci flow authoring, MFA policies, risk signal routing |
| 3. App-side wiring | This material | Install SDK, initialize client, wire auth code flow, render collectors, store tokens |

## SDK landscape — PingOne targets

### Android — PingOne Native SDK (Kotlin)

Gradle artifact: `com.pingidentity.sdks:android` (hosted on Maven Central and `maven.pingidentity.com`)

| Module | Purpose |
|---|---|
| `oidc` | Authorization code + PKCE, token management |
| `davinci` | Drives DaVinci collectors in Jetpack Compose |
| `journey` | Renders Journey callbacks (kept for AIC/PingAM targets) |
| `fido` | FIDO2 / passkey registration and assertion |
| `protect` | PingOne Protect signals collection |
| `push` | Push notification–based MFA (FCM) |
| `externalidp` | Social login (Google, Apple, Facebook) via IdP-initiated flow |
| `binding` | Device binding and integrity attestation |
| `oath` | TOTP / HOTP soft-token generation |

### iOS — PingOne Native SDK (Swift)

Swift Package: `Ping/ping-ios-sdk`

| Module | Purpose |
|---|---|
| `PingOidc` | OIDC authorization code + PKCE, token management |
| `PingDavinci` | DaVinci collectors in SwiftUI |
| `PingJourney` | Journey callbacks (kept for AIC/PingAM targets) |
| `PingStorage` | Keychain-backed secure token storage |
| `PingExternalIdP` | Social login via IdP-initiated flow |
| `PingProtect` | PingOne Protect signals |
| `PingOath` | TOTP / HOTP soft-token generation |
| `PingLogger` | Structured debug logging |
| `PingFido` | FIDO2 / passkey registration and assertion (iOS 16+) |

### Web / JavaScript — Ping Orchestration JavaScript SDK

| Package | Purpose |
|---|---|
| `@forgerock/davinci-client` | DaVinci collector rendering for SPAs |
| `@forgerock/oidc-client` | OIDC token exchange, session management, silent renewal |

Supports React (stable), Angular, Vue, and vanilla JS.

### DaVinci Orchestration SDK (cross-platform)

DaVinci flows are orchestrated server-side; the client SDK renders collectors. The same DaVinci flow definition works with Android, iOS, and JavaScript clients — only the rendering layer differs.

## Integration lifecycle

A production-ready PingOne integration passes through three phases. This material owns Phase 3.

### Phase 1 — Platform setup (platform administration)

- PingOne environment and population provisioning
- Application record creation (OIDC client ID, client secret, redirect URIs)
- Sign-on policy or DaVinci flow policy attachment
- Custom domain and certificate configuration

**Prerequisite condition:** Phase 1 is done when the application has a stable client ID, at least one redirect URI registered, and a policy attached.

### Phase 2 — Flow design (flow design tooling)

- DaVinci flow logic defined and tested end-to-end
- MFA policies and risk signal routing configured
- Collectors identified for the app to render

**Prerequisite condition:** Phase 2 is done when the flow runs end-to-end in the admin preview and produces the expected token.

### Phase 3 — App-side wiring (this material)

- SDK installed (Gradle / SPM / npm)
- SDK initialized with client ID, redirect URI, and scopes
- Auth code + PKCE flow wired to the login entry point
- Collectors rendered in the app UI
- Tokens received and stored in platform-secure storage
- Session refresh and logout implemented

## Prerequisites

- An application record exists in the PingOne environment (client ID and redirect URI registered)
- The DaVinci flow is functional (tested in the admin preview)
- Target platform SDK requirements: Android API 23+, iOS 14+, Node.js 16+ for JS
- Network access from the app to the PingOne token endpoint (no corporate proxy blocking)

## Source

- [PingOne Native SDK Documentation](https://docs.pingidentity.com/pingone/native-sdks/p1_native_sdks_landing.html)
- [Ping Identity Developer Documentation](https://developer.pingidentity.com/pingone-api/platform/)
