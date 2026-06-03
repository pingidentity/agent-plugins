---
title: "Web Integration Basics — React, JavaScript, OIDC, and SAML"
product_family: cross-platform
products: ["pingone", "pingone-aic", "pingfederate"]
capabilities: ["app-integration"]
services: []
audience: ["developer"]
use_cases: ["customer", "workforce", "cross-platform"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-03"
slug: "https://docs.pingidentity.com/pingone/javascript-sdk/p1_javascript_sdk_landing.html"
---

# Web Integration Basics — React, JavaScript, OIDC, and SAML

Integration guide for web applications authenticating through Ping Identity — covers the Ping JavaScript/React SDK, generic OIDC / OAuth2 flows, SAML SP integration, and browser-specific auth patterns.

## Scope

**Covers:**
- Ping JavaScript SDK (`@forgerock/journey-client`, `@forgerock/davinci-client`, `@forgerock/oidc-client`) for React apps
- Generic OIDC authorization code + PKCE for SPAs; client credentials for server-to-server
- OIDC redirect URI exact-match constraint, CORS requirements, token endpoint access
- SAML SP-initiated and IdP-initiated flows — when to use SAML vs. OIDC
- Browser-specific flows: hosted login page redirect, popup/post-message, silent renewal
- Flow type comparison table

**Does NOT cover:**
- Android or iOS native SDK integration — see `references/curated/mobile-integration-basics.md`
- Journey node or DaVinci flow authoring — use `ping-orchestration`
- Application record creation or redirect URI registration in the admin console — use `ping-foundation`
- Failure-mode diagnosis — see `references/curated/integration-troubleshooting-basics.md`

## React SDK — Ping JavaScript SDK

### Package selection

| Package | Target flow | Supported framework |
|---|---|---|
| `@forgerock/journey-client` | AIC / PingAM Journey-based auth | React (stable); Angular, Vue (roadmap) |
| `@forgerock/davinci-client` | PingOne MT DaVinci-based auth | React (stable); Angular, Vue (roadmap) |
| `@forgerock/oidc-client` | OIDC token lifecycle (any IdP) | Framework-agnostic |

Install:

```bash
npm install @forgerock/journey-client @forgerock/oidc-client
# or for DaVinci:
npm install @forgerock/davinci-client @forgerock/oidc-client
```

### Initialization

Initialize once at app startup (e.g., `main.tsx` or `index.ts`), before rendering any authenticated route:

```typescript
import { Config } from '@forgerock/journey-client';

Config.set({
  clientId: '<client-id>',
  redirectUri: window.location.origin + '/callback',
  scope: 'openid profile email offline_access',
  serverConfig: {
    baseUrl: 'https://<tenant>/am/',
    timeout: 5000,
  },
  realmPath: 'alpha',         // AIC realm; omit for PingAM default realm
  journeyName: 'Login',       // Entry journey name
});
```

DaVinci variant (replace `@forgerock/journey-client` import):

```typescript
import { davinci } from '@forgerock/davinci-client';

const client = davinci({
  config: {
    clientId: '<client-id>',
    redirectUri: window.location.origin + '/callback',
    scope: 'openid profile email offline_access',
    serverConfig: { baseUrl: 'https://auth.pingone.com/<envId>/as' },
  },
});
```

### TokenStorage

`@forgerock/oidc-client` stores tokens in either `sessionStorage` (default) or `localStorage`. Prefer `sessionStorage` for SPAs to limit the token lifetime to the browser tab.

Configuration:

```typescript
import { TokenStorage } from '@forgerock/oidc-client';

TokenStorage.set({ store: 'sessionStorage' }); // 'sessionStorage' | 'localStorage'
```

Do not persist refresh tokens in `localStorage` for public clients — a compromised token in `localStorage` is exploitable via XSS. Use BFF (Backend For Frontend) pattern with `HttpOnly` cookie token storage for high-security applications.

### Embedded login vs. hosted login page redirect

| Mode | Description | When to use |
|---|---|---|
| Embedded login | SDK renders callbacks/collectors inline in the SPA | Full control over UI; acceptable security model for same-origin apps |
| Hosted login redirect | App redirects to Ping-hosted login page; receives tokens via callback | Recommended for cross-origin apps, social login, MFA; simpler CORS requirements |

For hosted login: call `FRUser.login()` or `client.authorize()` without overriding the login page; the SDK redirects to the configured `redirectUri` with `code` + `state` query params on completion.

### Handling session callbacks (Journey)

Journey callbacks arrive as typed objects from the SDK iterator:

| Callback type | Rendering requirement |
|---|---|
| `NameCallback` | Text input (username field) |
| `PasswordCallback` | Password input |
| `ChoiceCallback` | Radio group or select |
| `TextOutputCallback` | Display-only message (INFO / WARNING / ERROR level) |
| `ConfirmationCallback` | Button group (OK / Cancel) |
| `DeviceProfileCallback` | Silent — SDK collects device fingerprint automatically |
| `HiddenValueCallback` | Silent — SDK handles; no UI required |
| `ValidatedCreateUsernameCallback` | Text input with server-returned validation rules |
| `ValidatedCreatePasswordCallback` | Password input with strength rules |
| `StringAttributeInputCallback` | Text input for a named user attribute (email, phone, etc.) |
| `BooleanAttributeInputCallback` | Checkbox for a boolean attribute |
| `PollingWaitCallback` | Display wait spinner; SDK polls until journey advances |
| `MetadataCallback` | Silent — read `.getValue()` for flow context |
| `SuspendedTextOutputCallback` | Email-suspend message; user told to check email; flow resumes via link |
| `SelectIdPCallback` | IdP selection list; render IdP names/logos |
| `IdPCallback` | Social login button (Google, Apple, Facebook, OIDC) |
| `KbaCreateCallback` | KBA question setup — display question list; collect answer |
| `ReCaptchaCallback` | Google reCAPTCHA widget; submit token on completion |
| `WebAuthnRegistrationCallback` | Trigger FIDO2/passkey registration via browser WebAuthn API |
| `WebAuthnAuthenticationCallback` | Trigger FIDO2/passkey assertion via browser WebAuthn API |

Pattern: iterate `node.callbacks`, render each by `callback.getType()`, collect user input, call `node.next(updatedCallbacks)`.

### DaVinci collector types (web)

For `@forgerock/davinci-client` (PingOne MT), collectors per step:

| Collector type | Notes |
|---|---|
| `TextCollector` | Text input — username, email |
| `PasswordCollector` | Masked password input |
| `SubmitCollector` | Submit button — call `node.next()` on click |
| `FlowCollector` | Secondary action — "Forgot password", "Register" |
| `SelectCollector` | Dropdown or radio group |
| `SsoCollector` / `IdpCollector` | Social login button (Google, Apple, Facebook) |
| `QrCodeCollector` | QR code display; flow polls for scan completion |
| `PhoneCollector` | Phone number with country picker |

Auto-advancing (no render): `ProtectCollector` (signals, silent).

## Generic OIDC integration

### Authorization code + PKCE for SPAs

Required parameters for the authorization request:

| Parameter | Value |
|---|---|
| `response_type` | `code` |
| `client_id` | Registered application client ID |
| `redirect_uri` | Exact match of a registered redirect URI |
| `scope` | `openid` (required) + additional scopes |
| `code_challenge` | Base64URL(SHA256(code_verifier)) |
| `code_challenge_method` | `S256` |
| `state` | Random nonce (CSRF protection) |
| `nonce` | Random nonce (ID token replay protection) |

Token exchange: POST to the token endpoint with `grant_type=authorization_code`, `code`, `code_verifier`, `redirect_uri`, `client_id`.

Constraint: `redirect_uri` in the token exchange must be byte-for-byte identical to the one used in the authorization request and the one registered in the admin console. A trailing slash difference or protocol mismatch (`http` vs `https`) causes `invalid_grant`.

### Client credentials (server-to-server)

Use `grant_type=client_credentials` for M2M flows where no user is present. The access token represents the client application, not a user. Requires a confidential client (client secret or private key JWT).

Client credentials tokens do not include `sub` (user subject) in the access token — resource servers must not assume user identity from these tokens.

### OIDC libraries — framework-agnostic requirements

No specific library is mandated. Any library implementing RFC 6749 + RFC 7636 works. Requirements for the library:

- PKCE support (`S256` method)
- State parameter generation and validation
- Nonce validation against the ID token claim
- Token expiry tracking and automatic refresh
- Logout (RP-initiated logout, `end_session_endpoint`)

Commonly used: `oidc-client-ts`, `@auth0/auth0-spa-js` (when using PingOne as IdP behind a proxy), `AppAuth-JS`.

### CORS requirements for the token endpoint

PingOne MT and AIC return `Access-Control-Allow-Origin` headers for cross-origin requests to the token endpoint. PingFederate requires explicit CORS configuration in `pf.properties` or via the PF admin console.

For SPAs performing the token exchange in-browser (not via a BFF), the token endpoint must allow the app origin. Symptoms of CORS misconfiguration: the authorization request succeeds but the token exchange fails with a network error in the browser console (no response body).

Constraint: the `OPTIONS` preflight for `/token` must receive `Access-Control-Allow-Origin` and `Access-Control-Allow-Headers: Content-Type, Authorization`.

## SAML integration

### OIDC vs. SAML decision rule

| Condition | Recommendation |
|---|---|
| New SPA or mobile app | OIDC (authorization code + PKCE) |
| Existing enterprise app with SAML SP already configured | Keep SAML — no migration value |
| App needs to federate with multiple IdPs | OIDC (simpler multi-IdP via PingOne as a broker) |
| Legacy .NET / Java EE app using WS-Federation | SAML SP + PingFederate WS-Fed adapter |
| App only needs an API access token | OIDC (client credentials or auth code) |

SAML does not produce OAuth2 access tokens natively — if the app needs both SSO and API access, consider OIDC or a SAML → OIDC token translation via PingFederate.

### SP-initiated SSO

Flow: app generates SAML `AuthnRequest` → POST or redirect to IdP SSO endpoint → IdP authenticates user → IdP POSTs SAML `Response` to ACS URL → app validates assertion → app establishes session.

Required configuration on the SP side:
- `AssertionConsumerServiceURL` (ACS URL) — must exactly match what is registered at the IdP
- IdP SSO endpoint URL — obtained from IdP metadata
- IdP signing certificate — for validating the assertion signature
- Entity ID — globally unique identifier for the SP

### IdP-initiated SSO

Flow: IdP sends unsolicited `Response` to ACS URL — no `AuthnRequest` from SP. Security consideration: IdP-initiated flows are vulnerable to CSRF attacks if the SP does not validate `InResponseTo` (which will be absent). Mitigate with a signed `RelayState` or by restricting IdP-initiated access to known IdPs.

## Browser-specific auth flows

### Hosted login page redirect

Standard flow for SPAs and web apps:

1. App builds the authorization URL with all required parameters
2. App redirects the browser (full-page or `window.location.href`)
3. User authenticates on the Ping-hosted login page
4. Ping redirects back to `redirect_uri` with `?code=...&state=...`
5. App exchanges `code` for tokens at the token endpoint
6. App validates `state` against the stored value (CSRF check)

### Popup / post-message flow

Some apps open the login page in a popup window and receive tokens via `window.postMessage`. This pattern requires:
- The hosted login page to support post-message (PingOne supports this for embedded flows)
- A listener on the parent window: `window.addEventListener('message', handler)`
- Origin validation in the handler: `event.origin === 'https://<tenant>'`

Popup flow is blocked by browsers when not triggered from a user gesture (click, keypress).

### Silent renewal (check session iframe)

OIDC silent renewal uses a hidden iframe to re-authenticate the user without interaction:

1. App embeds an iframe pointing to the authorization endpoint with `prompt=none`
2. If the user has an active session, the IdP redirects the iframe to the `redirect_uri` with a new `code`
3. The iframe posts the code to the parent via `postMessage`
4. The parent exchanges the code for a fresh token set

Constraints:
- Requires the IdP to have a session cookie accessible in the iframe context
- Third-party cookies blocked in Safari (ITP) and Chrome (Privacy Sandbox) break this flow — fallback to full-page redirect or BFF cookie-based session management

## Flow type comparison table

| Flow type | Use case | Library type | Token storage | Notes |
|---|---|---|---|---|
| Auth code + PKCE (redirect) | SPA, mobile web | Any OIDC library | `sessionStorage` / `localStorage` | Standard for public clients |
| Auth code + PKCE (popup) | SPA, embedded widget | OIDC library with popup support | In-memory | Blocked without user gesture |
| Client credentials | Server-to-server M2M | HTTP client with OAuth2 support | Server-side only | No user context |
| Hosted login redirect | Any web app | Redirect only; no SDK required | Tokens after callback | Simplest; recommended for cross-origin |
| SAML SP-initiated | Enterprise SSO | SAML library (e.g., passport-saml, Spring SAML) | Server-side session | No access token |
| Silent renewal (iframe) | Token refresh without interaction | OIDC library with iframe support | In-memory | Breaks with third-party cookie restrictions |
| BFF pattern (server-side) | High-security SPA | Server framework + OIDC library | `HttpOnly` cookie | Strongest XSS protection |

## Prerequisites

- Application record created in PingOne MT, AIC, or PingFederate with `redirect_uri` registered (use `ping-foundation`)
- Hosted login page or Journey/DaVinci flow operational (use `ping-orchestration`)
- CORS origins configured on the Ping tenant or PingFederate instance for the app's domain
- For SAML: SP entity ID and ACS URL registered at the IdP; IdP metadata downloaded for SP-side validation

## Common variants

| Variant | Note |
|---|---|
| PingOne MT | `@forgerock/davinci-client`; discovery endpoint `https://auth.pingone.com/<envId>/as/.well-known/openid-configuration` |
| AIC / PingOne ST | `@forgerock/journey-client`; realm-specific discovery endpoint |
| PingFederate on-prem | Standard OIDC (no Ping JS SDK required); CORS must be explicitly enabled in PF config |
| React with Vite | Vite dev server proxy can be used to avoid CORS during development; do not proxy token endpoint in production |
| Next.js (SSR) | Use server-side OAuth2 (NextAuth / Auth.js) with PingOne or PingFederate as the provider; do not use client-side PKCE for SSR routes |

## Related references

- `references/curated/app-integration-overview.md` — SDK landscape and lifecycle
- `references/curated/mobile-integration-basics.md` — Android and iOS SDK wiring
- `references/curated/integration-troubleshooting-basics.md` — Redirect URI mismatch, CORS errors, token failures

## Source

[Ping Identity JavaScript SDK Documentation](https://docs.pingidentity.com/pingone/javascript-sdk/p1_javascript_sdk_landing.html)
