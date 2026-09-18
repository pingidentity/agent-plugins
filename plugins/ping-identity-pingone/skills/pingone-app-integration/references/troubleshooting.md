# PingOne — Integration Troubleshooting

Diagnostic guide for the most common app-integration failure patterns against a PingOne environment — redirect URI mismatch, CORS errors, token failures, push MFA, and ForgeRock → Ping SDK migration breaking changes.

## Scope

**Covers:** Redirect URI mismatch, CORS errors on `/as/token`, token introspection failures, refresh token not honored, push MFA not delivered, ForgeRock → Ping SDK migration, quick-reference diagnostic table.
**Does NOT cover:** SDK installation or initialization — `references/mobile-integration.md` / `references/web-integration.md`. DaVinci flow authoring errors — flow-design documentation. Platform-side application configuration — platform administration.

---

## Failure mode 1: Redirect URI mismatch

**Error messages:** `redirect_uri_mismatch`, `invalid_request: redirect_uri does not match`, `error=invalid_request`

**Cause:** The authorization server performs an exact-match comparison between the `redirect_uri` value in the request and the set of URIs registered on the application. Any character difference results in rejection.

**Common mismatch patterns:**

| Mismatch type | Example registered | Example sent by app | Outcome |
|---|---|---|---|
| Trailing slash | `https://app.example.com/callback` | `https://app.example.com/callback/` | Rejected |
| Protocol case | `https://app.example.com/callback` | `HTTPS://app.example.com/callback` | Rejected |
| http vs https | `https://app.example.com/callback` | `http://app.example.com/callback` | Rejected |
| Extra query param | `https://app.example.com/callback` | `https://app.example.com/callback?env=prod` | Rejected |
| Scheme mismatch | `myapp://callback` | `myapp://callback/` | Rejected |
| Localhost port | `http://localhost:3000/callback` | `http://localhost:3001/callback` | Rejected |

**Diagnosis:** Capture the full authorization request URL (browser network tab or SDK debug log). Extract the `redirect_uri` parameter value. Compare byte-for-byte against the registered URIs. Admin surface: Applications → [app] → Redirect URIs.

**Fix:** Update either the registered URI in the PingOne admin console (add the exact value the app sends) or update the app to send the registered value exactly. Register all environment variants (dev, staging, prod) as separate entries — wildcard URIs are not supported.

## Failure mode 2: CORS errors on `/as/token`

**Symptom:** Authorization request succeeds (redirect to login, user authenticates, redirect back occurs), but the token exchange fails with a network error in the browser console. No HTTP response body is visible. The error reads: `Access to XMLHttpRequest at 'https://auth.pingone.com/<envId>/as/token' from origin 'https://app.example.com' has been blocked by CORS policy`.

**Cause:** The browser is performing a cross-origin POST to `/as/token`. The response must include `Access-Control-Allow-Origin: https://app.example.com`.

**Diagnosis:** Inspect the network traffic to `/as/token`. Check whether an OPTIONS preflight is present; if it receives a 4xx response or is missing `Access-Control-Allow-Origin`, server-side CORS configuration is incomplete. If no OPTIONS preflight is present, verify the token request uses `Content-Type: application/x-www-form-urlencoded` (correct) rather than `application/json` (triggers a preflight and is often misconfigured).

**Fix:** Set on the application's `corsSettings` (Applications → [app] → Configuration → CORS Settings). The default `Allow any CORS-safe origin` permits `/as/token` from any origin but blocks `/as/authorize` and sensitive endpoints — an in-app DaVinci flow needs "Allow specific origins" with the app origin listed. Not derived from redirect URIs.

**Architectural alternative:** Move the token exchange to a server-side BFF (Backend For Frontend). The browser makes a same-origin request to the BFF, which performs the token exchange server-to-server. Eliminates CORS entirely for the token endpoint.

**Prevent it up front:** this failure is avoidable by configuring the app origin before the first token exchange rather than reacting to the error. For proactive setup, see `references/web-integration.md` → "CORS pre-flight".

## Failure mode 3: Token introspection failures

**Error conditions:** `invalid_token`, `token_inactive`, `401 Unauthorized` at a resource server

**Sub-case A — Invalid or malformed token:**

Introspect the token using the introspection endpoint:

```
POST /as/introspect
Authorization: Basic <client_credentials>
Content-Type: application/x-www-form-urlencoded

token=<access_token>
```

Response `{"active": false}` confirms the token is invalid. Decode the JWT to inspect `exp` and `aud`.

**Sub-case B — Clock skew (> 5 seconds):**

The authorization server sets `iat` and `exp` using its system clock. The resource server validates `exp` against its own clock. A skew greater than 5 seconds causes premature expiry rejections.

Diagnostic: compare `exp` in the token to the resource server's current time (`date +%s`). A difference of 5+ seconds indicates clock skew.

Fix: synchronize both systems to an NTP server. Configure a clock skew tolerance on the resource server (`allowed_clock_skew` in Spring Security, `clockSkew` in passport-jwt, etc.) as a temporary mitigation — the root cause is always the unsynchronized clock.

**Sub-case C — Expired token:**

`exp` is in the past. The app should have used the refresh token to obtain a new access token before expiry. If the refresh token itself has expired, a full re-authentication is required.

Check: does the app perform proactive token refresh (e.g., 60 seconds before `exp`) or only reactive refresh (after receiving a 401)? Reactive refresh is riskier under high latency — prefer proactive.

**Sub-case D — Audience mismatch:**

The access token's `aud` claim does not include the resource server's identifier. The resource server rejects the token.

Fix: ensure the `audience` parameter is set correctly in the authorization request or the resource server identifier matches the configured audience in the PingOne application or flow policy.

## Failure mode 4: Refresh token not honored

**Symptom:** The app presents a refresh token with `grant_type=refresh_token` and receives `invalid_grant`, or no `refresh_token` appears in the token response.

**Cause A — `offline_access` scope not requested:**

Refresh tokens are only issued when the `offline_access` scope is included in the authorization request. This scope is commonly omitted.

Verification: decode the access token or ID token and check the `scope` claim. If `offline_access` is absent, PingOne will not issue a refresh token.

Fix: add `offline_access` to the `scope` parameter in the initial authorization request.

**Cause B — Refresh token reuse policy:**

PingOne supports refresh token rotation. After one use, the original refresh token is invalidated. If the app stores and reuses the original token after a successful rotation, subsequent refreshes fail with `invalid_grant`.

Fix: always store the new refresh token returned in the token response and discard the old one.

**Cause C — Refresh token lifetime exceeded:**

The refresh token has an absolute lifetime (configurable per application in the admin console). After expiry, a full re-authentication is required.

## Failure mode 5: Push MFA not delivered

**Symptom:** User completes password authentication, push notification should arrive on the registered device, but the notification never appears. The DaVinci flow times out waiting for push approval.

**Android (FCM) diagnostic checklist:**

1. `google-services.json` is present in the app module and references the correct Firebase project
2. `PingOne.registerDevice(fcmToken)` was called with a valid FCM token after the user authenticated
3. The FCM token is current — FCM tokens rotate; call `FirebaseMessaging.getInstance().token` at app startup and re-register if the token changes
4. The Firebase project is configured in the PingOne admin console: Applications → [app] → Push Notifications → FCM Server Key
5. Verify device registration: Users → [user] → Devices; a registered device appears with status "registered".

**iOS (APNs) diagnostic checklist:**

1. APNs certificate or APNs auth key is configured in the PingOne admin console
2. App requests push notification permission (`UNUserNotificationCenter.requestAuthorization()`) and calls `UIApplication.registerForRemoteNotifications()`
3. The APNs device token is passed to the Ping SDK: `PingOne.setAPNSDeviceToken(deviceToken)` in `application(_:didRegisterForRemoteNotificationsWithDeviceToken:)`
4. Push notification entitlement is present: `aps-environment = development` (dev) or `production` (release)
5. APNs sandbox vs. production: use sandbox for debug builds, production for TestFlight and App Store

**Common root cause:** Device registration step is skipped. The device must be registered before push notifications can be sent. Registration associates the device's push token with the user account in the PingOne environment.

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
| Module naming | `FRAuth`, `FRCore`, `FRProximity` | `PingOidc`, `PingDavinci`, `PingStorage` | Update imports |
| Initialization | `FRAuth.start()` (static) | `OidcClient(config:)` instance | Replace with instance-based init |
| Node / callback model | `FRNode`, `FRCallback` | `Node`, typed `Callback` protocol | Update protocol conformances |
| Token storage | `FRUser.currentUser` tokens | `PingStorage` / Keychain-backed token manager | Update token access patterns |
| DaVinci entry | `FRUser.login(completion:)` | DaVinci client `start()` async | Convert to async/await |

### JavaScript breaking changes

| Area | ForgeRock SDK | Ping SDK | Action |
|---|---|---|---|
| Package name | `@forgerock/javascript-sdk` | `@forgerock/davinci-client` | Update `package.json` dependencies |
| Config entry | `Config.set({...})` | Same API (no change) | No action needed |
| Flow iteration | `FRAuth.next(previousStep, {realmPath})` | DaVinci client `next(step)` | Update iteration calls |
| Token retrieval | `TokenManager.getTokens()` | `@forgerock/oidc-client` `getTokens()` | Update import + call |
| Session management | `FRSession.logout()` | `oidcClient.logout()` | Update logout call |

**Migration strategy — manual approach:** address breaking changes in order — (1) dependency declarations, (2) imports, (3) initialization, (4) flow entry points, (5) callback/collector handling, (6) token retrieval and storage. Test each phase with the existing DaVinci flow before proceeding to the next.

## Quick-reference diagnostic table

| Symptom | Likely cause | Fix |
|---|---|---|
| `redirect_uri_mismatch` at authorization | App sends URI that does not exactly match registered URI | Compare byte-for-byte; register the exact URI the app sends |
| Network error on token exchange (CORS) | `/as/token` does not allow the app's origin | Configure application CORS settings; or use BFF pattern |
| Token introspection returns `{"active": false}` | Token expired, invalid, or wrong audience | Check `exp`, `aud` in JWT; verify clock sync; request correct audience |
| `invalid_grant` on refresh | `offline_access` scope missing; rotated token reused | Add `offline_access`; store the new refresh token after rotation |
| Push MFA not received (Android) | FCM token not registered; FCM key not in admin console | Re-register device; verify FCM server key configuration |
| Push MFA not received (iOS) | APNs token not passed to SDK; sandbox vs. production mismatch | Call `setAPNSDeviceToken` in delegate; check entitlement environment |
| `FRAuth not found` after migration (Android) | Old `org.forgerock` package still imported | Replace all `org.forgerock` imports with `com.pingidentity.sdks` |
| `Module 'FRAuth' not found` (iOS) | Old SPM URL still in Package.swift | Update package URL to `github.com/ForgeRock/ping-ios-sdk` |
| `@forgerock/javascript-sdk` import error (JS) | Package removed; new package not installed | `npm install @forgerock/davinci-client @forgerock/oidc-client` |
| No `refresh_token` in token response | `offline_access` not in requested scopes | Add `offline_access` to `scope` parameter |
| 401 on API call with valid-looking token | Clock skew > 5s; audience mismatch | Sync clocks; verify `aud` claim matches resource server identifier |
| Silent renewal fails (Safari/Chrome) | Third-party cookie restrictions block iframe session | Use full-page redirect for renewal; or BFF session pattern |

## Prerequisites

- SDK version: verify the installed SDK version meets minimum requirements (Android SDK ≥ 3.0, iOS SDK ≥ 3.0, JS SDK ≥ 4.0)
- Application record with registered redirect URI and correct scopes
- For push MFA: FCM/APNs credentials configured in the PingOne admin console
- Access to the PingOne admin console to verify registered URIs, CORS origins, and device registrations

## Common variants

| Variant | Note |
|---|---|
| DaVinci flows | Audience claim in the access token is the resource server entity configured in the flow policy |
| React Native | Uses the same JS SDK packages as React web; deep link handling differs (see Expo/React Native linking docs) |

## Source

[PingOne Troubleshooting Documentation](https://docs.pingidentity.com/pingone/troubleshooting/p1_troubleshoot_apps.html)
