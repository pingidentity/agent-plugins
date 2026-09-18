# AIC — Web Integration (React, JavaScript, OIDC, and SAML)

Integration guide for web applications authenticating through PingOne Advanced Identity Cloud (AIC) — the journey client, journey callback rendering, generic OIDC/OAuth2 flows, SAML SP integration, and browser-specific auth patterns.

## Scope

**Covers:** `@forgerock/journey-client` and `@forgerock/oidc-client` for React apps, journey callback rendering, generic OIDC authorization code + PKCE for SPAs, client credentials for server-to-server, tenant CORS pre-flight, SAML SP-initiated and IdP-initiated flows, hosted login / popup / silent renewal, flow type comparison.
**Does NOT cover:** Android or iOS SDK integration — `references/mobile-integration.md`. Journey or tree authoring — journey-design documentation. Application-agent registration — tenant administration. Failure diagnosis — `references/troubleshooting.md`. This file covers CORS as proactive setup; `references/troubleshooting.md` covers diagnosing the runtime error.

---

## React SDK — journey client

### Package selection

| Package | Target flow | Supported framework |
|---|---|---|
| `@forgerock/journey-client` | AIC / PingAM Journey-based auth | React (stable); Angular, Vue (roadmap) |
| `@forgerock/oidc-client` | OIDC token lifecycle | Framework-agnostic |

Install:

```bash
npm install @forgerock/journey-client @forgerock/oidc-client
```

### Initialization

Initialize once at app startup (e.g., `main.tsx`), before rendering any authenticated route:

```typescript
import { Config } from '@forgerock/journey-client';

Config.set({
  clientId: '<client-id>',
  redirectUri: window.location.origin + '/callback',
  scope: 'openid profile email offline_access',
  serverConfig: {
    baseUrl: 'https://<tenant-host>/am/',
    timeout: 5000,
  },
  realmPath: 'alpha',         // AIC realm; adjust per target realm
  journeyName: 'Login',       // Entry journey name
});
```

### TokenStorage

`@forgerock/oidc-client` stores tokens in either `sessionStorage` (default) or `localStorage`. Prefer `sessionStorage` for SPAs to limit the token lifetime to the browser tab.

```typescript
import { TokenStorage } from '@forgerock/oidc-client';

TokenStorage.set({ store: 'sessionStorage' }); // 'sessionStorage' | 'localStorage'
```

Do not persist refresh tokens in `localStorage` for public clients — a compromised token in `localStorage` is exploitable via XSS. Use a BFF (Backend For Frontend) with `HttpOnly` cookie token storage for high-security applications.

### Embedded login vs. hosted login page redirect

| Mode | Description | When to use |
|---|---|---|
| Embedded login | SDK renders journey callbacks inline in the SPA | Full control over UI; acceptable security model for same-origin apps |
| Hosted login redirect | App redirects to AIC-hosted login page; receives tokens via callback | Recommended for cross-origin apps, social login, MFA; simpler CORS requirements |

For hosted login: call `client.authorize()` without overriding the login page; the SDK redirects to the configured `redirectUri` with `code` + `state` query params on completion.

## Handling journey callbacks

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

**Pattern:** iterate `node.callbacks`, render each by `callback.getType()`, collect user input, call `node.next(updatedCallbacks)`.

## Generic OIDC integration

### Authorization code + PKCE for SPAs

Required parameters for the authorization request:

| Parameter | Value |
|---|---|
| `response_type` | `code` |
| `client_id` | Registered application agent client ID |
| `redirect_uri` | Exact match of a registered redirect URI |
| `scope` | `openid` (required) + additional scopes |
| `code_challenge` | Base64URL(SHA256(code_verifier)) |
| `code_challenge_method` | `S256` |
| `state` | Random nonce (CSRF protection) |
| `nonce` | Random nonce (ID token replay protection) |

Token exchange: POST to the realm's token endpoint with `grant_type=authorization_code`, `code`, `code_verifier`, `redirect_uri`, `client_id`.

> **Before writing this in-browser POST, complete the CORS pre-flight below.** A cross-origin token POST from a SPA fails unless the app origin is already allowed on the server; configure it first rather than shipping code that breaks at runtime.

Constraint: `redirect_uri` in the token exchange must be byte-for-byte identical to the one used in the authorization request and the one registered on the application agent. A trailing slash difference or protocol mismatch (`http` vs `https`) causes `invalid_grant`.

### Client credentials (server-to-server)

Use `grant_type=client_credentials` for M2M flows where no user is present. The access token represents the client application, not a user. Requires a confidential client (client secret or private key JWT).

Client credentials tokens do not include `sub` (user subject) — resource servers must not assume user identity from these tokens.

### OIDC libraries — framework-agnostic requirements

No specific library is mandated. Any library implementing RFC 6749 + RFC 7636 works. Requirements for the library:

- PKCE support (`S256` method)
- State parameter generation and validation
- Nonce validation against the ID token claim
- Token expiry tracking and automatic refresh
- Logout (RP-initiated logout, `end_session_endpoint`)

## CORS pre-flight — configure before the first token exchange

Any SPA that performs the token exchange in the browser (not via a BFF) requires the token endpoint to allow the app's origin. On a new tenant this is **not configured by default for arbitrary origins**, so a browser flow breaks at the token step unless the origin is allowed. Treat CORS as a setup pre-flight, not a failure to diagnose later.

Symptom if skipped: the authorization request succeeds (redirect to login, authenticate, redirect back), but the token exchange fails with a network error in the browser console and no response body — `Access to XMLHttpRequest at 'https://<tenant-host>/am/oauth2/...' … blocked by CORS policy`.

Constraint: the `OPTIONS` preflight for the token endpoint must receive `Access-Control-Allow-Origin` matching the app origin, `Access-Control-Allow-Methods` including `POST`, and `Access-Control-Allow-Headers: Content-Type, Authorization`. Keep the token request `Content-Type: application/x-www-form-urlencoded` (an `application/json` body forces a preflight that is commonly misconfigured).

**Do:** confirm CORS is configured for the app's origin before generating in-browser token-exchange code. **Don't:** ship code that performs the token exchange cross-origin and let it fail at runtime.

### AIC tenant CORS configuration

CORS in AIC is a **tenant-level global configuration**, not per-application. Add the app origin (`scheme://host:port` — not the redirect URI path) to Accepted Origins, with Accepted Methods including `POST` and Accepted Headers including `Content-Type`, `Authorization`.

Admin surface: Tenant settings → Global Settings → Cross-Origin Resource Sharing (CORS).

### CORS-free alternative

If cross-origin configuration is out of scope for the environment, move the token exchange to a server-side BFF (Backend For Frontend): the browser calls the same-origin BFF, which performs the token exchange server-to-server. This eliminates browser CORS on the token endpoint entirely (see the BFF row in the flow-type table below).

## SAML integration

### OIDC vs. SAML decision rule

| Condition | Recommendation |
|---|---|
| New SPA or mobile app | OIDC (authorization code + PKCE) |
| Existing enterprise app with SAML SP already configured | Keep SAML — no migration value |
| App needs to federate with multiple IdPs | OIDC (simpler multi-IdP federation) |
| App only needs an API access token | OIDC (client credentials or auth code) |

SAML does not produce OAuth2 access tokens natively — if the app needs both SSO and API access, prefer OIDC or a token translation at the identity provider.

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
3. User authenticates on the AIC-hosted login page (journey)
4. AIC redirects back to `redirect_uri` with `?code=...&state=...`
5. App exchanges `code` for tokens at the realm's token endpoint
6. App validates `state` against the stored value (CSRF check)

### Popup / post-message flow

Some apps open the login page in a popup window and receive tokens via `window.postMessage`. This pattern requires:
- The hosted login page to support post-message
- A listener on the parent window: `window.addEventListener('message', handler)`
- Origin validation in the handler against the tenant host

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

- Application agent created in the tenant realm with `redirect_uri` registered (tenant administration)
- Journey operational in the target realm (journey design tooling)
- Tenant CORS origins configured for the app's domain
- AM services configured for journey features the app renders (push, WebAuthn, social, device profiles)

## Common variants

| Variant | Note |
|---|---|
| AIC realms | Realm path scopes the endpoints; Alpha (consumer) and Bravo (workforce) are fixed |
| Self-managed PingAM | Same journey model; endpoints point at the PingAM deployment; validate against PingAM documentation |
| React with Vite | Vite dev server proxy can avoid CORS during development; do not proxy the token endpoint in production |
| Next.js (SSR) | Use server-side OAuth2 (NextAuth / Auth.js) with AIC as the provider; do not use client-side PKCE for SSR routes |

## Source

- [PingOne Advanced Identity Cloud documentation](https://docs.pingidentity.com/pingoneaic/home.md)
- [Ping SDKs](https://developer.pingidentity.com/orchsdks/index.md)

