---
title: "PingOne Advanced Identity Cloud (AIC) — AM Services Configuration"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["foundation"]
services: ["push", "oath", "webauthn", "device-binding", "social-auth", "policy", "session"]
audience: ["admin", "architect", "developer"]
use_cases: ["workforce", "customer"]
doc_type: reference
status: current
canonical: true
last_updated: "2026-06-05"
slug: "https://docs.pingidentity.com/pingoneaic/am-reference/services-configuration.html"
---

# PingOne Advanced Identity Cloud (AIC) — AM Services Configuration

PingAM-level services that must be configured at the global or realm scope **before** related journey nodes, applications, or features will function end-to-end.

## Scope

**Covers:** All AM services exposed in AIC (`Native Consoles → Access Management → Services`), what each does, and which journey nodes / features require the service to be configured first.
**Does NOT cover:**
- Journey node configuration and outcomes — see `ping-orchestration` (e.g. `nodes/mfa-nodes.md`, `nodes/federation-contextual-nodes.md`).
- OIDC/SAML application registration — see `references/curated/pingone-st/app-setup.md`.
- Identity store / managed object schema — see `references/curated/pingone-st/directory-setup.md`.
- IDM-side services (Notifications, Email Templates, Connectors) — those live in the IDM admin console, not under AM Services.

> **Why this reference exists.** Many journey nodes silently fail or never appear in the picker until the corresponding AM Service is configured at the realm level. The most common example: the `Push Notification Sender` and `Push Registration` nodes will not deliver notifications until **Push Notification Service** is configured. This reference is the prerequisite checklist before journey authoring.

---

## Where to configure

**Admin surfaces (in priority order):**

1. **AIC tenant admin console** (preferred for the services it surfaces): `https://<tenant>.forgeblocks.com/platform/` → relevant section (Email Provider, Social Providers, etc.).
2. **AM admin console / Native Console:** `https://<tenant>.forgeblocks.com/am/console` → Realms → `<realm>` → **Services** → **+ Add a Service** (or edit existing).
3. **REST / config API:** `PUT /am/json/global-config/services/<serviceId>` for global, `PUT /am/json/realms/root/realms/<realm>/realm-config/services/<serviceId>` for realm.

Most services are **realm-scoped**: configure them in each realm where they are used (`alpha`, `bravo`, custom realms). A handful are **global**.

---

## Service ↔ node / feature prerequisite map

Use this table first. If a journey requires one of these nodes, ensure the service in the right column is added and configured in the realm.

| If you plan to use… | First configure |
|---|---|
| `Push Sender`, `Push Registration`, `Push Wait`, `Push Result Verifier` nodes | **Push Notification Service** (credentials) **+** **ForgeRock Authenticator (Push) Service** (profile storage) |
| `OATH Registration`, `OATH Token Verifier`, `OATH Device Storage` nodes | **ForgeRock Authenticator (OATH) Service** |
| `WebAuthn Registration`, `WebAuthn Authentication`, `WebAuthn Device Storage` nodes | **WebAuthn Profile Encryption Service** **+** **WebAuthn Metadata Service** (for attestation/FIDO MDS validation) |
| `Device Binding`, `Device Binding Storage`, `Device Signing Verifier` nodes | **Device Binding Service** |
| `Device Profile Collector`, `Device Match`, `Device Tampering Detection` nodes | **Device Profiles Service** |
| `Social Provider Handler`, `Select Identity Provider` nodes | **Social Authentication Implementations** (per-provider configuration) |
| `Identity Assertion`, `PingGateway Identity Assertion` nodes | **Identity Assertion Service** |
| Any OIDC / OAuth 2.0 client or `OAuth 2.0` node | **OAuth 2.0 Provider** (typically pre-configured per realm) |
| Any policy-based authorization or `Policy` decision node | **Policy Configuration** |
| Any session-aware node or session quota enforcement | **Session Service** |
| Scripts that read session attributes via `session.getProperty(...)` | **Session Property Whitelist Service** |
| `Consent Collector` against an external consent UI | **Remote Consent Service** |
| Self-service flows (forgot username, password reset, registration) bound to specific journeys | **Self Service Trees** |
| OAuth 2.0 / OIDC clients for IoT devices | **IoT Service** |
| Scripted HTTP calls that need mTLS, proxies, or custom timeouts | **HTTP Client Service** |
| Cross-origin SDK / SPA calls to AM endpoints | **CORS Service** *(global)* |
| Android device verification (Play Integrity / Key Attestation) | **Android Key Attestation Service** |
| Branded admin console naming / locale formatting | **Globalization Settings** *(global)* |
| Connectivity from AM to PingOne (multi-tenant cloud) services (MFA, Verify, Risk via PingOne Worker) | **PingOne Worker Service** |
| OneSpan-based authentication | **OneSpan Configuration** |
| Transaction-specific re-authentication (e.g. high-value transfer) | **Transaction Authentication Service** |
| Per-input validation rules in journeys | **Validation Service** |
| Cached script results (e.g. expensive scripted decision lookups) | **Cache Manager Service** |
| End-user profile attribute exposure | **User Service** |
| Generated absolute URLs in emails / OIDC responses behind a load balancer or custom domain | **Base URL Source** |

---

## Global services

These are configured **once per tenant**, not per realm.

### CORS Service
Controls cross-origin headers for AM endpoints across all realms. Required for any browser-based SDK (Ping SDK for JavaScript, single-page app login, custom UIs hosted on a different origin) calling `/am/json/...` endpoints.

- **Configure:** accepted origins (exact match, no wildcards in production), allowed methods (`GET, POST, PUT, DELETE, OPTIONS`), allowed headers (`accept-api-version`, `x-requested-with`, `authorization`, `content-type`, `iplanet-directory-pro`), max age, allow credentials = `true`.
- **Common gotcha:** Custom domain origin not added → SPA login fails with `CORS error: missing Allow-Origin`. Add both the custom domain and the default `<tenant>.forgeblocks.com` origin if both are reachable.

### Dashboard Service
Application dashboard config exposed to all realms. Rarely customized in modern AIC tenants — primarily a legacy XUI surface.

### Globalization Settings
Locale-based formatting of usernames in console banners. Cosmetic; no journey impact.

---

## Realm services — authentication & MFA

### ForgeRock Authenticator (Push) Service
Profile storage for Push device enrollments. **Required before any Push node.**

- Stores the user's push profile (device name, public key, push endpoint).
- **Pair with:** Push Notification Service (the credential service that actually delivers notifications). Both are required — one stores the profile, the other delivers the message.

### Push Notification Service
Delivers push notifications via APNs (iOS) and FCM (Android). **Required before `PushSenderNode`, `PushRegistrationNode`, `PushWaitNode`, `PushResultVerifierNode` will deliver messages.**

- **Required fields:** SNS Access Key ID, SNS Secret Access Key, SNS Endpoint, APNs ARN, GCM (FCM) ARN, region.
- **Workflow:** SNS-based delivery is the AIC default; raw APNs/FCM credentials are not entered directly here.
- **Symptom if missing:** `PushSenderNode` returns `NOT_REGISTERED` even when the user has a registered device; or push reaches the device but no notification arrives.
- **Test path:** AIC console → MFA → enroll a test user → trigger a push journey → verify notification arrives on device.

### ForgeRock Authenticator (OATH) Service
Profile storage for TOTP/HOTP enrollments. **Required before any OATH node.**

- Stores OATH device records (issuer, secret, counter for HOTP).
- **No external credentials needed** — OATH is computed client-side, no network delivery.

### WebAuthn Profile Encryption Service
Encrypts stored WebAuthn credentials in the user profile. **Required before `WebAuthnRegistrationNode` and `WebAuthnAuthenticationNode` will persist or read credentials.**

- Auto-provisions a key pair on first use; key rotation requires careful coordination — rotating without a migration window invalidates all stored credentials.

### WebAuthn Metadata Service
FIDO2 / WebAuthn authenticator metadata for attestation validation. Configure if `attestationPreference` on the WebAuthn Registration node is anything other than `NONE`.

- Pulls from FIDO Alliance Metadata Service (MDS) by default.
- Required for `fidoCertificationLevel != OFF` deployments.

### Device Binding Service
Storage of device binding keys (private key reference, device identifier) on the user's profile. **Required before `DeviceBindingNode`, `DeviceBindingStorageNode`, `DeviceSigningVerifierNode`.**

### Device Profiles Service
Encrypts and stores collected device profiles (browser, OS, screen, IP, location). **Required before `DeviceProfileCollectorNode` and any device-match decision logic.**

- Used by risk-based MFA flows.
- **See:** `ping-orchestration/nodes/risk-management-nodes.md` for the consuming nodes.

### Android Key Attestation Service
Validates Android device key attestation and checks certificate revocation. Required for Android-specific device verification (high-assurance mobile MFA).

### Social Authentication Implementations
Per-provider configuration (Google, Apple, Microsoft, Facebook, GitHub, custom OIDC). **Required before `SocialProviderHandlerNode` will offer that provider as an option.**

- Each provider entry holds: client ID, client secret, well-known config URL or endpoint set, scopes, attribute mappings.
- **Common gotcha:** social button order is controlled by node placement and provider list order — not by theme CSS.

### Identity Assertion Service
Enables PingGateway-fronted identity assertion. **Required before `IdentityAssertionNode`.**

- Used for header-based SSO from on-prem applications fronted by PingGateway.

### IoT Service
Creates OAuth 2.0 clients and JWT issuers for device-flow / IoT authentication scenarios.

### OneSpan Configuration
OneSpan integration for legacy OneSpan-based MFA. Rarely used in modern deployments.

### Transaction Authentication Service
Per-transaction authentication requirements (e.g. require step-up for transfers > $X). Configure before `TransactionAuthorizationNode`-based flows.

---

## Realm services — OAuth/OIDC, sessions, policy

### OAuth 2.0 Provider
The realm's OAuth 2.0 / OIDC authorization server configuration. **Required before any OIDC client will work.** Pre-configured in every AIC realm; customize for:

- Custom claims and claim sources (link to managed object attributes)
- ACR-to-journey mapping (`acr_values=high` → `HighAssuranceJourney`)
- Token lifetimes (access, refresh, ID)
- Stateful vs. stateless tokens
- Refresh token rotation
- PKCE enforcement for public clients
- Consent screen behavior
- Supported scopes and response types

> **Warning:** Changing token format (stateless ↔ stateful) impacts existing sessions and refresh tokens. Coordinate rollout.

### Policy Configuration
Authorization policy configuration. Required before policy-based decision nodes or REST policy evaluation calls.

### Session Service
Realm session lifecycle (idle timeout, max time, max concurrent sessions). See `references/curated/pingone-st/authentication-fundamentals.md` → Session management.

### Session Property Whitelist Service
Controls which session properties scripts (Scripted Decision nodes, OIDC claim scripts) can read via `session.getProperty(...)`. **If a script reads a property that is not in the whitelist, it returns null silently.**

- Add custom session properties here when scripts need to consume them.
- **Common gotcha:** Scripted Decision node correctly sets a property via `nodeState.putShared`, but a downstream OIDC claim script reads `null` because the property name was never added to the whitelist.

### Remote Consent Service
External consent collection (e.g. an external consent UI for OIDC consent). Configure before binding remote consent to an OIDC flow.

### Self Service Trees
Maps self-service operations (forgot password, forgot username, registration) to specific journey names. Without this, the default self-service journeys are used.

---

## Realm services — infrastructure & utility

### HTTP Client Service
Custom HTTP client config for scripted HTTP calls (`ScriptedDecisionNode` invoking `httpClient.send(...)`). Configure when scripts need:
- mTLS to a backend service
- Custom timeouts
- HTTP proxy
- Custom truststore

### Cache Manager Service
Caches computed values from scripts to reduce per-request load. Configure cache regions and eviction policies before relying on script-side caching.

### Base URL Source
How AM constructs absolute URLs in emails, OIDC responses, and SAML metadata. **Critical when using custom domains or sitting behind a load balancer.**

- Sources: `Request`, `Host`, `Forwarded` header, `X-Forwarded-*` headers, fixed value.
- **Common gotcha:** OIDC `iss` claim or password reset email links contain `<tenant>.forgeblocks.com` instead of the customer's custom domain → set Base URL Source to `Fixed value` with the custom domain.

### Validation Service
Per-input validation rules invoked by `ValidatedUsernameNode`, `ValidatedPasswordNode`, and similar. Define password policy, username format rules.

### User Service
Default user profile attribute exposure. Foundational; rarely modified.

### Email Service
**Not used on AIC.** In AIC, email delivery is configured via **Email Provider** and **Email Templates** (under Tenant Settings), not this AM service. Do not configure this AM-level service on AIC — it has no effect. For standalone PingIDM, configure email in IDM; for standalone PingAM, journey nodes connect to an external email provider directly.

### Dashboard Service
*(See Global services above.)*

---

## PingOne integration

### PingOne Worker Service
Connection from AIC to PingOne (multi-tenant cloud) services (PingOne MFA, PingOne Verify, PingOne Protect/Risk, PingOne DaVinci). **Required before** any of:

- `PingOne MFA` nodes (Authenticate, Register, etc.)
- `PingOne Verify` nodes (identity proofing)
- `PingOne Protect` / `Protect Evaluation` nodes (risk)
- `PingOne DaVinci` flow invocation

**Required fields:** PingOne tenant ID, environment ID, worker app client ID, worker app client secret, region (`NA`, `EU`, `APAC`, `CA`).

**Test connection** before saving — the console exposes a "Test Connection" button. A failed connection will not block save, but every dependent node will fail at runtime.

**See:** `ping-universal-services` skill for the corresponding PingOne (multi-tenant cloud) service configuration on the other side of this connection.

---

## Setup sequence (greenfield realm)

When configuring a new realm from scratch, work through services in this order to avoid dependency errors:

1. **Base URL Source** — set first if using a custom domain; many later URLs depend on it
2. **CORS Service** *(global)* — needed for SDK / SPA testing
3. **OAuth 2.0 Provider** — verify defaults; add custom claim scripts later
4. **Session Service** — set timeouts and quotas to fit your use case
5. **Validation Service** — define password / username rules before building registration journeys
6. **Identity store** — see `directory-setup.md`
7. **MFA services as needed:**
   - OATH: ForgeRock Authenticator (OATH) Service
   - Push: ForgeRock Authenticator (Push) Service **+** Push Notification Service
   - WebAuthn: WebAuthn Profile Encryption Service (+ Metadata if doing attestation)
   - Device Binding: Device Binding Service
   - Device Profile/Risk: Device Profiles Service
8. **Social Authentication Implementations** — one entry per IdP
9. **PingOne Worker Service** — if integrating with PingOne (multi-tenant cloud)
10. **Session Property Whitelist Service** — once your journey scripts settle on which session properties they read
11. **Self Service Trees** — last; bind self-service operations to the journeys you've built

---

## Common gotchas across services

| Gotcha | Symptom | Fix |
|---|---|---|
| Push node returns `NOT_REGISTERED` for an enrolled user | Service credentials missing or wrong region | Re-check Push Notification Service SNS ARNs and region |
| Scripted Decision reads `null` for a session attribute | Property not whitelisted | Add to Session Property Whitelist Service |
| OIDC discovery returns `<tenant>.forgeblocks.com` instead of custom domain | Base URL Source not set to fixed custom domain | Configure Base URL Source → Fixed value |
| Social provider button missing on hosted page | Provider not added under Social Authentication Implementations, or journey is using a stale `Select Identity Provider` node config | Re-add provider; refresh the node's IdP list |
| WebAuthn registration succeeds but credential not retrievable on next login | WebAuthn Profile Encryption Service key rotated | Stored credentials encrypted with old key are unrecoverable; users must re-enroll |
| PingOne MFA node fails with `401` | PingOne Worker Service credentials expired or wrong env | Test connection in service config; update worker app secret |
| Self-service forgot-password uses default flow not the custom one | Self Service Trees mapping not set | Map the self-service operation to the custom journey name |

---

## Prerequisites

- AIC tenant with realm-admin or super-admin access
- For Push Notification Service: AWS SNS endpoint, ARNs for APNs and FCM platform applications, and credentials provisioned by the AIC tenant onboarding team (these are typically supplied to the customer by Ping)
- For PingOne Worker Service: a PingOne (multi-tenant cloud) environment with a Worker application created
- For Social Authentication: client ID/secret and well-known endpoint for each external IdP

## Common variants

| Variant | Note |
|---|---|
| Workforce realm (`bravo`) | Often uses fewer services — typically OATH + WebAuthn for MFA, no social, no self-service registration |
| CIAM realm (`alpha`) | Full set: OATH, Push, WebAuthn, Social, Self Service Trees, Validation Service for registration, Device Profiles for risk |
| Multi-realm tenants | Service config is per-realm — do not assume `alpha` config carries to `bravo` |
| ForgeRock Identity Cloud | Same services, same names — older docs may use `forgerock.io` URLs |

## Related references

- `references/curated/pingone-st/foundation-overview.md` — tenant and realm architecture
- `references/curated/pingone-st/authentication-fundamentals.md` — journey and session basics
- `references/curated/pingone-st/app-setup.md` — OAuth 2.0 Provider relationship to OIDC clients
- `references/curated/pingone-st/directory-setup.md` — managed object schema for attributes referenced in claims and validation rules
- `../../../ping-orchestration/references/curated/pingone-st/nodes/mfa-nodes.md` — Push, OATH, WebAuthn node configuration
- `../../../ping-orchestration/references/curated/pingone-st/nodes/risk-management-nodes.md` — Device Profile and risk-based nodes
- `../../../ping-orchestration/references/curated/pingone-st/nodes/federation-contextual-nodes.md` — Social Provider and federation nodes

## Source

[AM services configuration — AIC](https://docs.pingidentity.com/pingoneaic/am-reference/services-configuration.html)
[Push Notification Service](https://docs.pingidentity.com/pingoneaic/am-reference/push-notification-service.html)
[ForgeRock Authenticator (Push) Service](https://docs.pingidentity.com/pingoneaic/am-reference/forgerock-authenticator-push-service.html)
[ForgeRock Authenticator (OATH) Service](https://docs.pingidentity.com/pingoneaic/am-reference/forgerock-authenticator-oath-service.html)
[OAuth 2.0 Provider Service](https://docs.pingidentity.com/pingoneaic/am-oauth2-guide/oauth2-provider-service.html)
[PingOne Worker Service](https://docs.pingidentity.com/pingoneaic/am-reference/pingone-worker-service.html)
[Session Property Whitelist Service](https://docs.pingidentity.com/pingoneaic/am-reference/session-property-whitelist-service.html)
[Base URL Source](https://docs.pingidentity.com/pingoneaic/am-reference/base-url-source.html)
[CORS Service](https://docs.pingidentity.com/pingoneaic/am-reference/cors-service.html)
