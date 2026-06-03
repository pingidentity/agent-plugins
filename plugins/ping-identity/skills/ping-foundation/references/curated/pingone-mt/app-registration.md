---
title: "PingOne MT — Application Registration"
product_family: pingone-mt
products: ["pingone"]
capabilities: ["foundation"]
services: ["oidc", "saml"]
audience: ["admin", "developer"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/pingone/applications/p1_applications_add_applications.html"
---

# PingOne MT — Application Registration

Registering OIDC, SAML, and Worker applications in PingOne MT: required fields, grant type selection, public-vs-confidential client rules, and common failure modes.

## Scope

**Covers:** OIDC Web, Native, Single-Page App, Worker, and SAML application creation and post-creation configuration in PingOne MT (console.pingone.com).
**Does NOT cover:** PingOne ST application setup (separate platform); Journey/DaVinci flow design — see `skills/ping-orchestration/SKILL.md`; SDK wiring and token consumption — see `skills/ping-app-integration/SKILL.md`.

---

## Application types

| Type | Client model | Typical grant types | Notes |
|---|---|---|---|
| OIDC Web App | Confidential (server-side) | Authorization Code | Holds a client secret; server renders HTML |
| Native / Mobile App | Public | Authorization Code + PKCE | Mobile (iOS, Android); no secret stored on device |
| Single-Page App (SPA) | Public | Authorization Code + PKCE | Front-end only; cannot hold a client secret |
| Worker | Confidential | Client Credentials | M2M / admin automation; no user sign-on by default |
| Device Authorization | Public | Device Authorization + PKCE | Constrained devices (smart TV, CLI); user approves on second device |
| SAML Application | N/A (SAML) | SP-initiated or IdP-initiated | Browser SSO only; no token endpoint |

**Decision rule — public vs. confidential:**
- If the app runs in a browser or on a user's device, treat it as **public**: set Token Endpoint Auth Method to `none` and enforce PKCE.
- If the app runs on a server you control and the secret never leaves that server, treat it as **confidential**: use `client_secret_basic` or `client_secret_post`.

---

## Required fields at creation time

The only fields collected when first creating an app are Name, Type, and (for SAML) ACS URL + Entity ID. All OIDC-specific fields are configured post-creation.

| Field | Applies to | Requirement | Notes |
|---|---|---|---|
| Application Name | All | Required | Unique within the environment; max 256 characters |
| Application Type | All | Required | Cannot be changed after creation |
| ACS URLs | SAML | Required | At least one; first entry is the default |
| Entity ID | SAML | Required | Unique within the environment |
| SP Metadata | SAML | Optional | Import XML or metadata URL to auto-fill ACS URL and Entity ID |

**After creation, the app is disabled by default.** Enable it explicitly before testing.

---

## OIDC configuration fields (post-creation)

### Identifiers

| Field | Notes |
|---|---|
| Client ID | Auto-generated; note immediately — used in all token requests |
| Client Secret | Confidential clients only; cannot be retrieved after the creation screen; rotate immediately if lost |

### Grant types and response types

| Grant type | Use case | PKCE required |
|---|---|---|
| Authorization Code | User-facing web and mobile apps | Required for public clients; recommended for confidential |
| Client Credentials | M2M / Worker | No (no user context) |
| Refresh Token | Offline access | No |
| Device Authorization | Constrained devices | Optional |
| Implicit | Legacy only | No — do not use for new apps |

Enable only the grant types the application will actually use. Unused grant types increase attack surface.

### Token endpoint authentication method

| Method | Client type | Notes |
|---|---|---|
| None | Public (SPA, Native) | No secret; PKCE enforced instead |
| Client Secret Basic | Confidential | Secret sent in HTTP Authorization header (Base64-encoded) |
| Client Secret Post | Confidential | Secret sent in request body |
| Client Secret JWT | Confidential | Secret used to sign a JWT assertion |
| Private Key JWT | Confidential | Asymmetric key pair; strongest confidential option |

### Redirect URIs

- Exact-match enforced: the URI in the authorization request must match a registered URI character-for-character.
- Fragment components (`#`) are not allowed in registered URIs.
- Trailing slashes matter: `https://app.example.com/callback` and `https://app.example.com/callback/` are different entries.
- In production, wildcard patterns are disabled by default. Register every environment's URI explicitly.

### Scopes

| Scope | Included by default | Notes |
|---|---|---|
| `openid` | Required minimum | Must be present; triggers ID token issuance |
| `profile` | Optional | Claims: name, given_name, family_name, etc. |
| `email` | Optional | Claim: email |
| `address` | Optional | Claim: address |
| `phone` | Optional | Claim: phone_number |
| Custom scope | Optional | Must be defined as a Resource first, then assigned to the app |

### Refresh token settings

| Field | Default | Range | Notes |
|---|---|---|---|
| Duration | 30 days | 60s – 1826 days | Absolute expiry from issuance |
| Rolling Duration | 180 days | 60s – 1826 days | Must be >= Duration |
| Rolling Grace Period | 0 | 0 – 86,400 seconds | Window during which the previous refresh token remains valid after rotation |
| Token format | Opaque | Opaque or JWT | JWT refresh token format is deprecated; retires 2027-03-01 |

---

## SAML-specific fields (post-creation)

| Field | Notes |
|---|---|
| ACS URLs | If the SP sends `AssertionConsumerServiceURL` in the auth request, it must exactly match a registered ACS URL |
| Entity ID | Used as the SAML Issuer; must match what the SP sends |
| Subject NameID Format | Default: `urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified` |
| Signing Key | Certificate PingOne uses to sign assertions and SLO messages |
| Sign options | Sign Assertion (default), Sign Response, or Sign Assertion & Response |
| Signing Algorithm | RSA-SHA256 / RSA-SHA384 / RSA-SHA512 or EC equivalents |
| Encryption | Optional; AES-128 or AES-256 (AES-256 recommended); SAML 2.0 only |
| SLO Endpoint | URL on the SP that receives SLO requests from PingOne |
| SLO Binding | HTTP POST (default) or HTTP Redirect |
| SLO Window | Min 1 hour, max 24 hours |

---

## Sign-on policy attachment

An application with no explicit sign-on policy uses the **environment default policy**. In production, always attach a named policy to each application.

- Sign-on policies are configured under Authentication in the left navigation.
- Attach a policy to an app via the app's Sign-on Policies tab.
- Multiple policies can be assigned; PingOne evaluates them in priority order.

**Risk:** Relying on the environment default means a policy change affects all unattached apps simultaneously — silent behavior change.

---

## Population assignment

Users must belong to a population that is permitted to access the application.

- Population assignment is configured on the app's Allowed Populations tab.
- If a user's population is not in the allowed list, authentication will be denied.
- A mismatch produces a generic access-denied response that does not name the population as the cause — hard to diagnose without checking the app's allowed population list.

## Group-based access

In addition to population-level access, applications support group-based access control.

- Configure on the app's Access tab.
- Select one or more groups; only members of those groups can access the application.
- Combine with dynamic groups (see directory-and-populations.md) for attribute-driven access — for example, only users with `countryCode = US` in the target group can access the app.
- Group access and population access are both enforced — a user must satisfy both conditions.

## Application SSO URLs

After enabling the application, the Overview tab provides:
- **Initiate Single Sign-On URL** — the entry point to start the SSO flow; share with users or embed in application launchers.
- **OIDC applications:** Discovery document at `https://auth.pingone.com/{envId}/as/.well-known/openid-configuration`.
- **SAML applications:** IdP-initiated SSO URL and SP metadata download link are on the Configuration tab.

---

## Common gotchas

| Gotcha | Symptom | Fix |
|---|---|---|
| App left disabled after creation | Token requests fail immediately; no error details | Enable the app toggle after creation |
| Redirect URI mismatch | `redirect_uri_mismatch` or `invalid_request` | Register the exact URI including scheme, port, path, and trailing slash |
| Missing PKCE on public client | `invalid_grant` from modern OIDC libraries | Set Token Endpoint Auth Method to None and enable PKCE |
| Client secret lost | Cannot retrieve after creation screen | Rotate the secret via the console or API; update all consumers |
| Population not allowed | Silent access-denied; user cannot authenticate | Add the user's population to the app's Allowed Populations list |
| Custom scope not granted | Scope absent from access token | Define the scope as a Resource, then assign the Resource to the app |
| Implicit grant on new app | Insecure; tokens in URL fragment | Remove Implicit grant; use Authorization Code + PKCE |
| JWT refresh token in use | Will break 2027-03-01 | Switch to Opaque token format before the retirement date |

---

## Prerequisites

- PingOne MT environment with Environment Admin or Application Admin role
- For SAML: SP metadata (ACS URL and Entity ID) from the service provider
- For custom scopes: Resource definition created before app registration
- For sign-on policies: Policy defined in the environment before attachment

---

## Common variants

| Variant | Note |
|---|---|
| Multi-environment redirect URIs | Register all environment-specific redirect URIs (dev, staging, prod) in a single app, or use one app registration per environment |
| Custom domain impact on redirect URIs | If using a custom domain, redirect URIs must match the custom domain hostname — not `auth.pingone.com` |
| Worker app for API automation | Create a Worker app; assign admin roles to it; use client credentials grant to obtain tokens for API calls |
| PKCE for confidential clients | PKCE is valid on Authorization Code for confidential clients too; adds defense-in-depth against authorization code interception |
| Secret rotation with zero downtime | Configure a retention window for the previous secret so existing tokens remain valid during the rotation window |

---

## Related references

- `references/curated/pingone-mt/tenant-and-environment-setup.md` — environment prerequisites before app registration
- `skills/ping-orchestration/SKILL.md` — Journey and DaVinci flow wiring
- `skills/ping-app-integration/SKILL.md` — SDK-level token consumption and OIDC client setup

---

## Source

[Adding applications in PingOne](https://docs.pingidentity.com/pingone/applications/p1_applications_add_applications.html)
[PingOne application types](https://docs.pingidentity.com/pingone/applications/p1_application_types.html)
[Editing OIDC applications](https://docs.pingidentity.com/pingone/applications/p1_edit_application_oidc.html)
[Editing SAML applications](https://docs.pingidentity.com/pingone/applications/p1_edit_application_saml.html)
[Editing native applications](https://docs.pingidentity.com/pingone/applications/p1_edit_application_native.html)
[Editing worker applications](https://docs.pingidentity.com/pingone/applications/p1_edit_application_worker.html)
