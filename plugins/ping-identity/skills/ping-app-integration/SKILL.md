---
name: ping-app-integration
description: "Use this skill whenever the task involves writing code or wiring an SDK to integrate Ping Identity into an application. Triggers: Android, iOS, or React/JavaScript SDK integration; embedding DaVinci flows or AIC journeys in a web or mobile app; OIDC authorization code + PKCE flow wiring; server-side backend OIDC (Node.js, Java, Python, .NET); token validation, refresh, and session management; client credentials (M2M) and token exchange patterns; redirect_uri_mismatch, CORS, token refresh failures, push MFA not delivering; migrating from ForgeRock SDK to Ping SDK; embedding a Ping service SDK (Protect JavaScript signals SDK, Verify mobile SDK) in app code; on-prem PingFederate or PingAccess agent integration. NOT for: configuring or invoking PingOne Verify, Protect, IGA, or Authorize at the service/policy level (use ping-universal-services); platform admin (use ping-foundation); flow design (use ping-orchestration). Also invoke with /ping-app-integration."
compatibility: Designed for Ping Identity app and SDK integration work. References product docs and SDK documentation.
metadata:
  publisher: Ping Identity
  version: "1.0.0"
---

# ping-app-integration

Implementation skill for integrating Ping Identity into web, mobile, and application SDK experiences.

## Invocation

Invoke explicitly with `/ping-app-integration` or by saying "use ping-app-integration to...".

## When to use this skill

- "Integrate Ping into my React app using the orchestration SDK"
- "Use the iOS SDK with AIC journeys"
- "Wire OIDC redirect into a mobile app"
- "Embed a journey in a webview"
- "Migrate from the ForgeRock SDK to the Ping SDK"
- "Add browser-based login to my web application"
- "Connect my Android app to a DaVinci flow"
- "App-side OIDC / OAuth configuration for PingFederate"
- "Redirect URI mismatch error in my app"
- "CORS error on the token endpoint"

## When NOT to use this skill

- Platform setup or app registration (no code): use `ping-foundation`.
- Designing the flow or journey itself: use `ping-orchestration`.
- General onboarding orientation: use `ping-quickstart`.

## Multi-skill use cases

A complete app integration spans three layers — all are required for a production outcome:

| Layer | Skill | Typical tasks |
|---|---|---|
| 1. Platform setup + app registration | `ping-foundation` | Tenant setup, redirect URI registration, sign-on policy |
| 2. Journey or flow design | `ping-orchestration` | Journey nodes, DaVinci flows, MFA policy |
| 3. SDK / app-side implementation | `ping-app-integration` (this skill) | SDK install, init, auth flow, token storage |

Complete platform setup first, then flow design, then hand off to this skill for SDK wiring.

**End-to-end example (Android + DaVinci on PingOne):**

1. Use `ping-foundation` to register an OIDC application in PingOne, configure the redirect URI (`myapp://callback`), and note the client ID and environment ID.
2. Use `ping-orchestration` to build and test a DaVinci login flow with username/password and push MFA nodes.
3. Use this skill (`ping-app-integration`) to add the `com.pingidentity.sdks:davinci` and `com.pingidentity.sdks:oidc` dependencies, initialize `PingOne.init(context)` with the client ID and discovery endpoint, call `PingOne.startAuthentication(activity)`, and handle the `AuthResult`.

## Step 1: What are you trying to do?

| Task | Curated reference |
|---|---|
| Overview: skill positioning, SDK landscape, integration lifecycle | `references/curated/app-integration-overview.md` |
| Android SDK integration (Journey or DaVinci) | `references/curated/mobile-integration-basics.md` |
| iOS Swift SDK integration (Journey or DaVinci) | `references/curated/mobile-integration-basics.md` |
| React / JavaScript web integration | `references/curated/web-integration-basics.md` |
| Generic OIDC web app or SAML integration | `references/curated/web-integration-basics.md` |
| Browser-based redirect / hosted login | `references/curated/web-integration-basics.md` |
| On-prem app integration (PingFederate, PingAccess) | `references/curated/web-integration-basics.md` |
| Server-side / backend OIDC, M2M client_credentials, token exchange, CIBA, retry/429 | `references/curated/server-side-integration-basics.md` |
| Troubleshooting, migration (ForgeRock → Ping SDK) | `references/curated/integration-troubleshooting-basics.md` |

## MCP execution

See `references/runtime/mcp-preflight.md` for MCP config and Cursor preflight steps.

## Step 2: Retrieval escalation

1. Curated anchors (`references/curated/`) — load 1–3 max. Stop if sufficient.
2. Generated shortlists (`references/generated/web/`, `references/generated/mobile/`, `references/generated/on-prem-integration/`, `references/generated/orchestration-sdks/`) — load the relevant directory for the surface; skip if empty.
3. Docs MCP fallback — query the Ping docs MCP server with a targeted product + task query. Only if curated + shortlist insufficient.

## Companion SDK skills — `ping-sdk-agent-skills`

For deep implementation work (full code scaffolding, collector rendering, migration automation), delegate to the specialist skills in the `pingidentity/ping-sdk-agent-skills` plugin:

| Specialist skill | Platform |
|---|---|
| `ping-orchestration-sdk-router` | Detects platform (Android/iOS/JS) and routes — use first when platform is ambiguous |
| `ping-orchestration-android-sdk` | Android Kotlin / Jetpack Compose — Journey + DaVinci |
| `ping-orchestration-ios-sdk` | iOS Swift / SwiftUI — Journey + DaVinci |
| `ping-orchestration-reactjs-journey-sdk` | React + AIC Journey flows |
| `ping-orchestration-reactjs-davinci-sdk` | React + PingOne DaVinci flows |
| `ping-orchestration-javascript-sdk` | Angular / Vue / Vanilla JS |
| `forgerock-to-ping-journey-migration` | ForgeRock SDK → Ping SDK automated migration |

Install: `https://github.com/pingidentity/ping-sdk-agent-skills`
