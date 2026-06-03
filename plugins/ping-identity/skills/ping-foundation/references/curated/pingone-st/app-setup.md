---
title: "PingOne ST — App Setup"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["foundation"]
services: []
audience: ["admin", "developer"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/pingoneaic/getting_started/getting_started-create_oauth2_client.html"
---

# PingOne ST — App Setup

Register OIDC, OAuth 2.0, and SAML applications in PingOne ST so they can authenticate users through journeys.

## Scope

**Covers:** OIDC client registration, OAuth 2.0 client setup, SAML SP/IdP registration, key configuration fields.
**Does NOT cover:** Journey design — see `references/curated/pingone-st/authentication-fundamentals.md`. Provisioning to external systems — see `references/curated/pingone-st/directory-setup.md`.

---

## Application types

| Type | When to use |
|---|---|
| OIDC / OAuth 2.0 client | Web apps, SPAs, mobile apps, M2M service accounts needing tokens |
| SAML SP | Enterprise apps using SAML 2.0 federation |
| SAML IdP | PingOne ST acting as IdP to a third-party SP |

---

## OIDC / OAuth 2.0 application

**Admin surface:** AIC tenant admin console → Applications → OAuth 2.0 Clients → + Create Client

**Required configuration:**

| Field | Notes |
|---|---|
| Client ID | Auto-generated or custom; must be unique within the realm |
| Client Secret | Required for confidential clients; omit for public (SPA, native) |
| Redirect URIs | Exact match enforced; add all environments upfront to avoid `redirect_uri mismatch` in lower envs |
| Grant Types | Authorization Code (web apps), Client Credentials (M2M), Refresh Token as needed; avoid Implicit |
| Scopes | Minimum: `openid`; add `profile`, `email`, `address`, `phone` as needed |
| Client Type | Confidential (can hold a secret) or Public (SPA/native; requires PKCE) |

**Client authentication methods:**
- `client_secret_basic` — HTTP Basic header; most common for confidential clients
- `client_secret_post` — client ID/secret in POST body
- `private_key_jwt` — JWT signed with client's private key; recommended for high-security M2M

**OIDC discovery endpoint:**
`https://<tenant>/am/oauth2/realms/root/realms/<realm>/.well-known/openid-configuration`

**Token options:**
- Access token format: server-side (stateful) or JWT (stateless)
- ID token encryption: optional; configure if the client cannot inspect the JWT
- Refresh token expiry: per-client override or realm default

---

## SAML application

**Admin surface:** AIC admin console → Applications → SAML Applications → + Register Application

**Required configuration:**

| Field | Notes |
|---|---|
| Entity ID | Unique SP identifier; typically the app's base URL or a URN |
| ACS URL | Assertion Consumer Service URL — where PingOne ST POST-binds the SAML response |
| Single Logout URL | Optional; required for SLO support |
| Name ID Format | `email`, `persistent`, or `transient` — dictated by SP requirements |
| Signing | Enable response and/or assertion signing; export IdP metadata to share with SP admin |

**Metadata exchange:** Import SP metadata XML if available to auto-populate ACS URL, entity ID, and certificates. Export PingOne ST IdP metadata from Applications → SAML Applications → (app) → Export Metadata.

---

## Assigning a journey to an application

An OIDC or SAML app uses the realm's default authentication journey unless overridden.

**Override location:** Application settings → Authentication → Journey

Use per-app journey assignment to serve distinct login experiences (e.g., workforce vs. customer, standard vs. high-assurance) without modifying the realm default.

---

## Provisioning from apps

Applications can provision user accounts to 40+ external systems (Salesforce, Workday, Active Directory, Microsoft Entra ID) using PingIDM connectors.

**Admin surface:** Applications → Provisioning

Configure provisioning after basic app setup is complete and the identity store is verified.

---

---

## Token and session configuration

| Setting | Applies to | Constraint |
|---|---|---|
| Access token lifetime | OIDC clients | Configured per client; default varies by realm; shorter is better for API security |
| Refresh token rotation | OIDC clients with offline_access | Rotating refresh tokens reduce replay risk; configure grace period to avoid revocation on concurrent use |
| ID token claims | OIDC clients | Claims populated from mapped identity store attributes; map attributes under Application → Claims |
| PKCE enforcement | Public clients | Required for SPA and native apps; enforced by setting Client Type = Public |
| Token blacklisting | All OIDC clients | PingAM supports stateful access tokens with per-token revocation; enable via OAuth 2.0 provider settings |

---

## Common gotchas

| Gotcha | Symptom | Fix |
|---|---|---|
| Client registered in wrong realm | `invalid_client` error at token endpoint; client not found | Confirm the realm in the OIDC discovery endpoint matches the realm where the client was created |
| Redirect URI mismatch | `redirect_uri mismatch` error from PingAM | Register the exact URI; trailing slash and path case are significant |
| Journey not activated | Login flow returns error or no response | Activate the journey from the Journey editor before testing |
| Application using realm default journey | Different login experience than expected | Override the journey at Application settings → Authentication → Journey |
| SAML SP metadata imported but entity ID mismatch | SAML assertion delivery fails | Verify entity ID in the imported metadata matches what the SP will send in `AuthnRequest` |
| Token endpoint authentication method mismatch | `invalid_client` on token exchange | Align client's configured auth method with what the SDK or HTTP client sends |

## Prerequisites

- PingOne ST tenant with admin access
- Realm configured with at least one identity store (see `references/curated/pingone-st/directory-setup.md`)
- At least one authentication journey ready or in progress (see `references/curated/pingone-st/authentication-fundamentals.md`)

## Common variants

| Variant | Note |
|---|---|
| SPA | Public client type, PKCE required, no client secret |
| M2M / service account | Client Credentials grant, no redirect URI needed |
| Realm-scoped clients | Clients registered in `alpha` are not available in `bravo` and vice versa |

## Related references

- `references/curated/pingone-st/authentication-fundamentals.md`
- `references/curated/pingone-st/foundation-overview.md`
- `references/curated/pingone-st/directory-setup.md`

## Source

[Register OAuth 2.0 clients — PingOne ST](https://docs.pingidentity.com/pingoneaic/getting_started/getting_started-create_oauth2_client.html)
[OIDC client registration](https://docs.pingidentity.com/pingoneaic/am-oidc-guide/oidc-client-registration.html)
[SAML application registration](https://docs.pingidentity.com/pingoneaic/am-saml2-guide/saml2-sp-registration.html)
