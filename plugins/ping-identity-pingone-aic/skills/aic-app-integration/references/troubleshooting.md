# AIC — Integration Troubleshooting

Diagnostic guide for the most common app-integration failure patterns against PingOne Advanced Identity Cloud (AIC) — redirect URI mismatch, CORS errors, token failures, and ForgeRock → Ping SDK migration breaking changes.

## Scope

**Covers:** Redirect URI mismatch, CORS errors on the token endpoint, token introspection failures, refresh token not honored, ForgeRock → Ping SDK migration (Android, iOS, JavaScript), quick-reference diagnostic table.
**Does NOT cover:** SDK installation or initialization — `references/mobile-integration.md` / `references/web-integration.md`. Journey or tree authoring errors — journey-design documentation. Platform-side application-agent configuration — tenant administration. Push MFA delivery checks — app-side checklists here; server-side push service configuration in current AIC documentation.

---

## Failure mode 1: Redirect URI mismatch

**Error messages:** `redirect_uri_mismatch`, `invalid_request: redirect_uri does not match`, `error=invalid_request`

**Cause:** The authorization server performs an exact-match comparison between the `redirect_uri` value in the request and the set of URIs registered on the application agent. Any character difference results in rejection.

**Common mismatch patterns:**

| Mismatch type | Example registered | Example sent by app | Outcome |
|---|---|---|---|
| Trailing slash | `https://app.example.com/callback` | `https://app.example.com/callback/` | Rejected |
| Protocol case | `https://app.example.com/callback` | `HTTPS://app.example.com/callback` | Rejected |
| http vs https | `https://app.example.com/callback` | `http://app.example.com/callback` | Rejected |
| Extra query param | `https://app.example.com/callback` | `https://app.example.com/callback?env=prod` | Rejected |
| Scheme mismatch | `myapp://callback` | `myapp://callback/` | Rejected |
| Localhost port | `http://localhost:3000/callback` | `http://localhost:3001/callback` | Rejected |

**Diagnosis:** Capture the full authorization request URL (browser network tab or SDK debug log). Extract the `redirect_uri` parameter value. Compare byte-for-byte against the URIs registered on the application agent in the target realm.

**Fix:** Update either the registered URIs on the application agent (add the exact value the app sends) or update the app to send the registered value exactly. Register all environment variants (dev, staging, prod) as separate entries — wildcard URIs are not supported.

## Failure mode 2: CORS errors on the token endpoint

**Symptom:** Authorization request succeeds (redirect to login, user authenticates, redirect back occurs), but the token exchange fails with a network error in the browser console. No HTTP response body is visible. The error reads: `Access to XMLHttpRequest at 'https://<tenant-host>/am/oauth2/...' from origin 'https://app.example.com' has been blocked by CORS policy`.

**Cause:** The browser is performing a cross-origin POST to the token endpoint. The response must include `Access-Control-Allow-Origin: https://app.example.com`.

**Diagnosis:** Inspect the network traffic to the token endpoint. Check whether an OPTIONS preflight is present; if it receives a 4xx response or is missing `Access-Control-Allow-Origin`, tenant CORS configuration is incomplete. If no OPTIONS preflight is present, verify the token request uses `Content-Type: application/x-www-form-urlencoded` (correct) rather than `application/json` (triggers a preflight and is often misconfigured).

**Fix:** Global tenant CORS configuration (Tenant settings → Global Settings → CORS). Add the app origin to Accepted Origins, with Accepted Methods including `POST` and Accepted Headers including `Content-Type`, `Authorization`.

**Architectural alternative:** Move the token exchange to a server-side BFF (Backend For Frontend). The browser makes a same-origin request to the BFF, which performs the token exchange server-to-server. Eliminates CORS entirely for the token endpoint.

**Prevent it up front:** this failure is avoidable by configuring the app origin before the first token exchange rather than reacting to the error. For proactive setup, see `references/web-integration.md` → "CORS pre-flight".

## Failure mode 3: Token introspection failures

**Error conditions:** `invalid_token`, `token_inactive`, `401 Unauthorized` at a resource server

**Sub-case A — Invalid or malformed token:**

Introspect the token using the realm's introspection endpoint:

```
POST /introspect
Authorization: Basic <client_credentials>
Content-Type: application/x-www-form-urlencoded

token=<access_token>
```

Response `{"active": false}` confirms the token is invalid. Decode the JWT to inspect `exp` and `aud`.

**Sub-case B — Clock skew (> 5 seconds):**

The authorization server sets `iat` and `exp` using its system clock. The resource server validates `exp` against its own clock. A skew greater than 5 seconds causes premature expiry rejections.

Diagnostic: compare `exp` in the token to the resource server's current time (`date +%s`). A difference of 5+ seconds indicates clock skew. Clock skew issues are most common when the tenant is recently provisioned.

Fix: synchronize both systems to an NTP server. Configure a clock skew tolerance on the resource server (`allowed_clock_skew` in Spring Security, `clockSkew` in passport-jwt, etc.) as a temporary mitigation — the root cause is always the unsynchronized clock.

**Sub-case C — Expired token:**

`exp` is in the past. The app should have used the refresh token to obtain a new access token before expiry. If the refresh token itself has expired, a full re-authentication is required.

Check: does the app perform proactive token refresh (e.g., 60 seconds before `exp`) or only reactive refresh (after receiving a 401)? Reactive refresh is riskier under high latency — prefer proactive.

**Sub-case D — Audience mismatch:**

The access token's `aud` claim does not include the resource server's identifier. The resource server rejects the token.

Fix: ensure the `audience` parameter is set correctly in the authorization request or the resource server identifier matches the configured audience in the OAuth 2.0 client or policy.

## Failure mode 4: Refresh token not honored

**Symptom:** The app presents a refresh token with `grant_type=refresh_token` and receives `invalid_grant`, or no `refresh_token` appears in the token response.

**Cause A — `offline_access` scope not requested:**

Refresh tokens are only issued when the `offline_access` scope is included in the authorization request. This scope is commonly omitted.

Verification: decode the access token or ID token and check the `scope` claim. If `offline_access` is absent, the server will not issue a refresh token.

Fix: add `offline_access` to the `scope` parameter in the initial authorization request.

**Cause B — Refresh token reuse policy:**

If refresh token rotation is enabled for the client, after one use the original refresh token is invalidated. If the app stores and reuses the original token after a successful rotation, subsequent refreshes fail with `invalid_grant`.

Fix: always store the new refresh token returned in the token response and discard the old one.

**Cause C — Refresh token lifetime exceeded:**

The refresh token has an absolute lifetime (configurable per client). After expiry, a full re-authentication is required.

## Failure mode 5: ForgeRock → Ping SDK migration breaking changes

Migrating from `forgerock-android-sdk`, `forgerock-ios-sdk`, or `@forgerock/javascript-sdk` to the Ping SDKs requires addressing the following breaking changes:

### Android breaking changes

| Area | ForgeRock SDK | Ping SDK | Action |
|---|---|---|---|
| Gradle group ID | `org.forgerock:forgerock-android-sdk` | `com.pingidentity.sdks:android` | Update all `implementation()` declarations |
| Initialization method | `FRAuth.start(context)` | `PingOne.init(context) { ... }` DSL | Replace init call; move config to builder DSL |
| Journey entry point | `FRUser.login(context, callbacks)` | Journey client start (DSL) | Replace call site |
| Node type | `FRNode` | `Node` (sealed class) | Update type references and `when` branches |
| Callback sealed types | `FRCallback` subclasses | `Callback` sealed subclasses (renamed) | Audit `instanceof` / `is` checks — names changed |
| Token retrieval | `FRUser.getCurrentUser()?.getAccessToken()` | tokens from the auth result | Update access pattern |
| Session token | `FRSession.getCurrentSession()` | session API on the client | Update session checks |

### iOS breaking changes

| Area | ForgeRock SDK | Ping SDK | Action |
|---|---|---|---|
| Package URL | `github.com/ForgeRock/forgerock-ios-sdk` | `github.com/ForgeRock/ping-ios-sdk` | Update SPM dependency URL |
| Module naming | `FRAuth`, `FRCore`, `FRProximity` | `PingOidc`, `PingJourney`, `PingStorage` | Update imports |
| Initialization | `FRAuth.start()` (static) | `OidcClient(config:)` instance | Replace with instance-based init |
| Node / callback model | `FRNode`, `FRCallback` | `Node`, typed `Callback` protocol | Update protocol conformances |
| Token storage | `FRUser.currentUser` tokens | `PingStorage` / Keychain-backed token manager | Update token access patterns |
| Journey entry | `FRUser.login(completion:)` | `journeyClient.start()` async | Convert to async/await |

### JavaScript breaking changes

| Area | ForgeRock SDK | Ping SDK | Action |
|---|---|---|---|
| Package name | `@forgerock/javascript-sdk` | `@forgerock/journey-client` | Update `package.json` dependencies |
| Config entry | `Config.set({...})` | Same API (no change) | No action needed |
| Node iteration | `FRAuth.next(previousStep, {realmPath})` | `journeyClient.next(step)` | Update iteration calls |
| Token retrieval | `TokenManager.getTokens()` | `@forgerock/oidc-client` `getTokens()` | Update import + call |
| Session management | `FRSession.logout()` | `oidcClient.logout()` | Update logout call |

**Migration strategy — manual approach:** address breaking changes in order — (1) dependency declarations, (2) imports, (3) initialization, (4) journey entry points, (5) callback/node handling, (6) token retrieval and storage. Test each phase with the existing journey before proceeding to the next.

## Quick-reference diagnostic table

| Symptom | Likely cause | Fix |
|---|---|---|
| `redirect_uri_mismatch` at authorization | App sends URI that does not exactly match registered URI | Compare byte-for-byte; register the exact URI the app sends |
| Network error on token exchange (CORS) | Token endpoint does not allow the app's origin | Configure tenant CORS accepted origins; or use BFF pattern |
| Token introspection returns `{"active": false}` | Token expired, invalid, or wrong audience | Check `exp`, `aud` in JWT; verify clock sync; request correct audience |
| `invalid_grant` on refresh | `offline_access` scope missing; rotated token reused | Add `offline_access`; store the new refresh token after rotation |
| `FRAuth not found` after migration (Android) | Old `org.forgerock` package still imported | Replace all `org.forgerock` imports with `com.pingidentity.sdks` |
| `Module 'FRAuth' not found` (iOS) | Old SPM URL still in Package.swift | Update package URL to `github.com/ForgeRock/ping-ios-sdk` |
| `@forgerock/javascript-sdk` import error (JS) | Package removed; new package not installed | `npm install @forgerock/journey-client @forgerock/oidc-client` |
| No `refresh_token` in token response | `offline_access` not in requested scopes | Add `offline_access` to `scope` parameter |
| 401 on API call with valid-looking token | Clock skew > 5s; audience mismatch | Sync clocks; verify `aud` claim matches resource server identifier |
| Silent renewal fails (Safari/Chrome) | Third-party cookie restrictions block iframe session | Use full-page redirect for renewal; or BFF session pattern |

## Prerequisites

- SDK version: verify the installed SDK version meets minimum requirements
- Application agent with registered redirect URI and correct scopes
- Access to the AIC admin console to verify registered URIs, tenant CORS origins, and application-agent settings

## Common variants

| Variant | Note |
|---|---|
| AIC | Journey-based flows; clock skew issues are most common when the tenant is recently provisioned |
| Self-managed PingAM | Same journey model; validate failure behavior against PingAM documentation for the target release |
| React Native | Uses the same JS SDK packages as React web; deep link handling differs (see Expo/React Native linking docs) |

## Source

- [PingOne Advanced Identity Cloud documentation](https://docs.pingidentity.com/pingoneaic/home.md)
- [Ping SDKs](https://developer.pingidentity.com/orchsdks/index.md)
