---
title: "Integration Troubleshooting — Top Failure Modes"
product_family: cross-platform
products: ["pingone", "pingone-aic", "pingfederate"]
capabilities: ["app-integration"]
services: []
audience: ["developer"]
use_cases: ["customer", "workforce", "cross-platform"]
doc_type: troubleshooting
status: current
canonical: true
last_updated: "2026-06-03"
slug: "https://docs.pingidentity.com/pingone/troubleshooting/p1_troubleshoot_apps.html"
---

# Integration Troubleshooting — Top Failure Modes

Diagnostic guide for the most common failure patterns in Ping Identity app integrations — covering redirect URI mismatch, CORS errors, token failures, push MFA, and ForgeRock → Ping SDK migration breaking changes.

## Scope

**Covers:**
- Redirect URI mismatch — diagnosis and fix
- CORS errors on the token endpoint — cause, diagnosis, fix
- Token introspection failures — invalid token, clock skew, expiry
- Refresh token not honored — scope omission
- Push MFA not delivered — FCM/APNs configuration and device registration
- ForgeRock SDK → Ping SDK migration breaking changes (renamed packages, callback model, init API)
- Quick-reference diagnostic table: symptom → likely cause → fix

**Does NOT cover:**
- SDK installation or initialization steps — see `references/curated/mobile-integration-basics.md` or `references/curated/web-integration-basics.md`
- Journey node or DaVinci flow authoring errors — use `ping-orchestration`
- Platform-side application configuration — use `ping-foundation`

## Failure mode 1: Redirect URI mismatch

**Error messages:** `redirect_uri_mismatch`, `invalid_request: redirect_uri does not match`, `error=invalid_request`

**Cause:** The authorization server performs an exact-match comparison between the `redirect_uri` value in the request and the set of URIs registered for the application. Any character difference results in rejection.

**Common mismatch patterns:**

| Mismatch type | Example registered | Example sent by app | Outcome |
|---|---|---|---|
| Trailing slash | `https://app.example.com/callback` | `https://app.example.com/callback/` | Rejected |
| Protocol case | `https://app.example.com/callback` | `HTTPS://app.example.com/callback` | Rejected |
| http vs https | `https://app.example.com/callback` | `http://app.example.com/callback` | Rejected |
| Extra query param | `https://app.example.com/callback` | `https://app.example.com/callback?env=prod` | Rejected |
| Scheme mismatch | `myapp://callback` | `myapp://callback/` | Rejected |
| Localhost port | `http://localhost:3000/callback` | `http://localhost:3001/callback` | Rejected |

**Diagnosis:** Capture the full authorization request URL (browser network tab or SDK debug log). Extract the `redirect_uri` parameter value. Compare byte-for-byte against the list of registered URIs in the application record. Admin surface: Applications → [app] → Redirect URIs.

**Fix:** Update either the registered URI in the admin console (add the exact value the app sends) or update the app to send the registered value exactly. Register all environment variants (dev, staging, prod) as separate entries — wildcard URIs are not supported by most Ping platform configurations.

## Failure mode 2: CORS errors on the token endpoint

**Symptom:** Authorization request succeeds (browser redirects to login page, user authenticates, redirect back occurs), but the token exchange fails with a network error in the browser console. No HTTP response body is visible. The error in the console typically reads: `Access to XMLHttpRequest at 'https://<tenant>/token' from origin 'https://app.example.com' has been blocked by CORS policy`.

**Cause:** The browser is performing a cross-origin POST to the token endpoint. The Ping authorization server must include `Access-Control-Allow-Origin: https://app.example.com` (or `*` for public endpoints) in the response headers.

**Diagnosis:** Inspect the network traffic to the token endpoint (`POST /token`). Check whether an OPTIONS preflight request is present; if it receives a 4xx response or is missing `Access-Control-Allow-Origin` in the response headers, the problem is server-side CORS configuration. If no OPTIONS preflight is present, the browser is not issuing one — verify that the token request uses `Content-Type: application/x-www-form-urlencoded` (correct) rather than `application/json` (triggers a preflight and is often misconfigured). If both preflight and actual request are present but `Access-Control-Allow-Origin` is absent from the response headers, server-side CORS configuration is incomplete.

**Fix by platform:**

| Platform | Fix |
|---|---|
| PingOne | Set on the application's `corsSettings` (Applications → [app] → Configuration → CORS Settings). The default `Allow any CORS-safe origin` permits `/as/token` from any origin but blocks `/as/authorize` and sensitive endpoints — an in-app DaVinci/Journey flow needs "Allow specific origins" with the app origin listed. Not derived from redirect URIs. |
| PingOne Advanced Identity Cloud (AIC) | Global AM `CorsService` policy (Tenant settings → Global Settings → CORS). Add the app origin to `acceptedOrigins`; can be configured via the AIC MCP `CorsService` tools |
| PingFederate | Admin console: System → OAuth Settings → Authorization Server Settings → Cross-Origin Resource Sharing Settings → Allowed Origin. Replicate to all cluster nodes after saving |

**Architectural alternative:** Move the token exchange to a server-side BFF (Backend For Frontend). The browser makes a same-origin request to the BFF, which performs the token exchange server-to-server. Eliminates CORS entirely for the token endpoint.

**Prevent it up front:** this failure is avoidable by configuring the app origin before the first token exchange rather than reacting to the error. For proactive per-platform setup — including configuring AIC CORS via the AIC MCP `CorsService` tools — see `references/curated/web-integration-basics.md` → "CORS pre-flight".

## Failure mode 3: Token introspection failures

**Error conditions:** `invalid_token`, `token_inactive`, `401 Unauthorized` at a resource server

**Sub-case A — Invalid or malformed token:**

Introspect the token using the `/introspect` endpoint:

```
POST /introspect
Authorization: Basic <client_credentials>
Content-Type: application/x-www-form-urlencoded

token=<access_token>
```

Response `{"active": false}` confirms the token is invalid. Use `jwt.io` or `token.dev` to decode the JWT and inspect the payload for expiry (`exp`) and audience (`aud`).

**Sub-case B — Clock skew (> 5 seconds):**

The authorization server sets `iat` and `exp` using its system clock. The resource server validates `exp` against its own clock. A skew greater than 5 seconds causes premature expiry rejections.

Diagnostic: compare `exp` in the token to the resource server's current time (`date +%s`). A difference of 5+ seconds indicates clock skew.

Fix: synchronize both systems to an NTP server. Configure a clock skew tolerance on the resource server (`allowed_clock_skew` in Spring Security, `clockSkew` in passport-jwt, etc.) as a temporary mitigation — the root cause is always the unsynchronized clock.

**Sub-case C — Expired token:**

`exp` is in the past. The app should have used the refresh token to obtain a new access token before expiry. If the refresh token itself has expired, a full re-authentication is required.

Check: does the app perform proactive token refresh (e.g., 60 seconds before `exp`) or only reactive refresh (after receiving a 401)? Reactive refresh is riskier under high latency — prefer proactive.

**Sub-case D — Audience mismatch:**

The access token's `aud` claim does not include the resource server's identifier. The resource server rejects the token.

Fix: ensure the `audience` parameter is set correctly in the authorization request or the resource server identifier matches the configured audience in the Ping application or OAuth2 policy.

## Failure mode 4: Refresh token not honored

**Symptom:** The app presents a refresh token to the token endpoint with `grant_type=refresh_token` and receives `invalid_grant` or the refresh token is ignored (no `refresh_token` in the token response).

**Cause A — `offline_access` scope not requested:**

Refresh tokens are only issued when the `offline_access` scope is included in the authorization request. This scope is commonly omitted.

Verification: decode the access token or ID token and check the `scope` claim. If `offline_access` is absent, the authorization server will not issue a refresh token.

Fix: add `offline_access` to the `scope` parameter in the initial authorization request.

**Cause B — Refresh token reuse policy:**

PingOne and PingFederate support refresh token rotation. After one use, the original refresh token is invalidated. If the app stores and reuses the original token after a successful rotation, subsequent refreshes fail with `invalid_grant`.

Fix: always store the new refresh token returned in the token response and discard the old one.

**Cause C — Refresh token lifetime exceeded:**

The refresh token has an absolute lifetime (typically 30–90 days, configurable per application in the admin console). After expiry, a full re-authentication is required.

## Failure mode 5: Push MFA not delivered

**Symptom:** User completes password authentication, push notification should arrive on the registered device, but the notification never appears. The journey or DaVinci flow times out waiting for push approval.

**Android (FCM) diagnostic checklist:**

1. `google-services.json` is present in the app module and references the correct Firebase project
2. `PingOne.registerDevice(fcmToken)` was called with a valid FCM token after the user authenticated
3. The FCM token is current — FCM tokens rotate; call `FirebaseMessaging.getInstance().token` at app startup and re-register if the token changes
4. The Firebase project is configured in the PingOne admin console: Applications → [app] → Push Notifications → FCM Server Key
5. Verify device registration: admin surface — Users → [user] → Devices; a registered device appears with status "registered".

**iOS (APNs) diagnostic checklist:**

1. APNs certificate or APNs auth key is configured in the Ping admin console
2. App requests push notification permission (`UNUserNotificationCenter.requestAuthorization()`) and calls `UIApplication.registerForRemoteNotifications()`
3. The APNs device token is passed to the Ping SDK: `PingOne.setAPNSDeviceToken(deviceToken)` in `application(_:didRegisterForRemoteNotificationsWithDeviceToken:)`
4. Push notification entitlement is present in the app's entitlements file: `aps-environment = development` (dev) or `aps-environment = production` (release)
5. APNs sandbox vs. production: use sandbox for debug builds, production for TestFlight and App Store

**Common root cause:** Device registration step is skipped. The device must be registered before push notifications can be sent. Registration associates the device's push token with the user account in the Ping platform.

## Failure mode 6: ForgeRock → Ping SDK migration breaking changes

Migrating from `forgerock-android-sdk` or `forgerock-ios-sdk` to the Ping Native SDKs requires addressing the following breaking changes:

### Android breaking changes

| Area | ForgeRock SDK | Ping SDK | Action |
|---|---|---|---|
| Gradle group ID | `org.forgerock:forgerock-android-sdk` | `com.pingidentity.sdks:android` | Update all `implementation()` declarations |
| Initialization method | `FRAuth.start(context)` | `PingOne.init(context) { ... }` DSL | Replace init call; move config to builder DSL |
| Login flow entry point | `FRUser.login(context, callbacks)` | `PingOne.startAuthentication(activity)` | Replace call site |
| Node type | `FRNode` | `Node` (sealed class) | Update type references and `when` branches |
| Callback sealed types | `FRCallback` subclasses | `Callback` sealed subclasses (renamed) | Audit `instanceof` / `is` checks — names changed |
| Token retrieval | `FRUser.getCurrentUser()?.getAccessToken()` | `tokens.accessToken` from `AuthResult.Success` | Update access pattern |
| Session token | `FRSession.getCurrentSession()` | `PingOne.getSession()` | Update session checks |

### iOS breaking changes

| Area | ForgeRock SDK | Ping SDK | Action |
|---|---|---|---|
| Package URL | `github.com/ForgeRock/forgerock-ios-sdk` | `github.com/ForgeRock/ping-ios-sdk` | Update SPM dependency URL |
| Module naming | `FRAuth`, `FRCore`, `FRProximity` | `PingOidc`, `PingJourney`, `PingStorage` | Update imports |
| Initialization | `FRAuth.start()` (static) | `OidcClient(config:)` instance | Replace with instance-based init |
| Node / callback model | `FRNode`, `FRCallback` | `Node`, typed `Callback` protocol | Update protocol conformances |
| Token storage | `FRUser.currentUser` tokens | `PingStorage` / `Keychain`-backed `TokenManager` | Update token access patterns |
| Journey entry | `FRUser.login(completion:)` | `journeyClient.start()` async | Convert to async/await |

### JavaScript breaking changes

| Area | ForgeRock SDK | Ping SDK | Action |
|---|---|---|---|
| Package name | `@forgerock/javascript-sdk` | `@forgerock/journey-client` or `@forgerock/davinci-client` | Update `package.json` dependencies |
| Config entry | `Config.set({...})` | Same API (no change) | No action needed |
| FRAuth node iteration | `FRAuth.next(previousStep, {realmPath})` | `journeyClient.next(step)` | Update iteration calls |
| Token retrieval | `TokenManager.getTokens()` | `@forgerock/oidc-client` `getTokens()` | Update import + call |
| Session management | `FRSession.logout()` | `oidcClient.logout()` | Update logout call |

**Migration strategy — manual approach:** address breaking changes in order — (1) dependency declarations, (2) imports, (3) initialization, (4) flow entry points, (5) callback/node handling, (6) token retrieval and storage. Test each phase with the existing journey or DaVinci flow before proceeding to the next.

**Automated migration:** For full automated code migration, use the `forgerock-to-ping-journey-migration` skill from the `pingidentity/ping-sdk-agent-skills` plugin. That skill runs a structured 9-phase workflow: (1) Detect platform, (2) Gather context (read manifest, package.json, Podfile), (3) Pre-flight build check, (4) Scope migration, (5) Scan for legacy usage, (6) Preview plan, (7) Apply changes with `[ping-migration] BEGIN/END legacy` comment markers, (8) Post-flight build verification, (9) Write migration report. It never silently deletes code and keeps the build working at every step.

## Quick-reference diagnostic table

| Symptom | Likely cause | Fix |
|---|---|---|
| `redirect_uri_mismatch` at authorization | App sends URI that does not exactly match registered URI | Compare byte-for-byte; register the exact URI the app sends |
| Network error on token exchange (CORS) | Token endpoint does not allow the app's origin | Configure CORS allow-origins on PingOne/PF; or use BFF pattern |
| Token introspection returns `{"active": false}` | Token expired, invalid, or wrong audience | Check `exp`, `aud` in JWT; verify clock sync; request correct audience |
| `invalid_grant` on refresh | `offline_access` scope missing; refresh token rotated but old token reused | Add `offline_access`; store and use the new refresh token after rotation |
| Push MFA not received (Android) | FCM token not registered; FCM key not in admin console | Re-register device; verify FCM server key configuration |
| Push MFA not received (iOS) | APNs token not passed to SDK; sandbox vs. production mismatch | Call `setAPNSDeviceToken` in delegate; check entitlement environment |
| `FRAuth not found` after migration (Android) | Old `org.forgerock` package still imported | Replace all `org.forgerock` imports with `com.pingidentity.sdks` |
| `Module 'FRAuth' not found` (iOS) | Old SPM URL still in Package.swift | Update package URL to `github.com/ForgeRock/ping-ios-sdk` |
| `@forgerock/javascript-sdk` import error (JS) | Package removed; new package not installed | `npm install @forgerock/journey-client @forgerock/oidc-client` |
| No `refresh_token` in token response | `offline_access` not in requested scopes | Add `offline_access` to `scope` parameter |
| 401 on API call with valid-looking token | Clock skew > 5s; audience mismatch | Sync clocks; verify `aud` claim matches resource server identifier |
| Silent renewal fails (Safari/Chrome) | Third-party cookie restrictions block iframe session | Use full-page redirect for renewal; or BFF session pattern |

## Prerequisites

- SDK version: verify the installed SDK version meets minimum requirements (Android SDK ≥ 3.0, iOS SDK ≥ 3.0, JS SDK ≥ 4.0 for Ping Native SDKs)
- Application record with registered redirect URI and correct scopes (use `ping-foundation` to verify)
- For push MFA: FCM/APNs credentials configured in the Ping admin console
- Access to admin console to verify registered URIs, CORS origins, and device registrations

## Common variants

| Variant | Note |
|---|---|
| PingFederate on-prem | CORS configuration is in `pf.properties` + admin console; not auto-configured from redirect URI |
| AIC | Journey-based flows; clock skew issues are most common when the AIC instance is recently provisioned |
| PingOne | DaVinci flows; audience claim in access token is the resource server entity configured in the DaVinci policy |
| React Native | Uses the same JS SDK packages as React web; deep link handling differs (see Expo/React Native linking docs) |

## Related references

- `references/curated/mobile-integration-basics.md` — Android and iOS SDK setup including migration table
- `references/curated/web-integration-basics.md` — JavaScript OIDC and SAML integration
- `references/curated/app-integration-overview.md` — Integration lifecycle and skill positioning
- `pingidentity/ping-sdk-agent-skills` — `forgerock-to-ping-journey-migration` skill for automated SDK migration

## Source

[Ping Identity Troubleshooting Documentation](https://docs.pingidentity.com/pingone/troubleshooting/p1_troubleshoot_apps.html)
