---
name: ping-foundation
description: "Use this skill whenever the task involves setting up, configuring, or administering any Ping Identity platform — PingOne (multi-tenant cloud), PingOne Advanced Identity Cloud (AIC), PingFederate, PingAccess, PingDirectory, or PingID. Triggers: create or manage environments, tenants, realms; register OIDC, SAML, WS-Federation, or OAuth 2.0 apps; configure SSO, Platform SSO, or workforce single sign-on; manage directories, LDAP, user populations, or schema; configure sign-on policies, authentication policies, or step-up MFA policy settings at the platform level; configure MFA methods or PingID in PingFederate; branding, custom domains, or notification templates; administer on-premises Ping software; advisory questions like 'how should I structure my tenant' or 'what grant type should I use'. Prerequisite — a specific platform must be named or clearly implied; 'add a user to Ping' or 'create a user in Ping' without a named platform belongs in ping-quickstart first. Also invoke with /ping-foundation."
compatibility: Designed for Ping Identity platform tasks. MCP tools for PingOne and PingOne Advanced Identity Cloud (AIC) are used when available; console instructions provided as fallback.
metadata:
  publisher: Ping Identity
  version: "1.0.0"
---

# ping-foundation

Platform setup, administration, and core configuration for all Ping Identity deployments. Covers tenant and environment setup, apps, directories, policies, branding, and on-premises software administration. MCP tools handle execution; this skill supplies architecture patterns, sequencing, configuration constraints, and guardrails.

## Invocation

Invoke explicitly with `/ping-foundation` or by saying "use ping-foundation to...".

## When to use this skill

Trigger on ANY question about setting up, configuring, administering, or planning a Ping Identity platform — including advisory and planning requests:

- Set up or provision environments, tenants, or realms
- Register OIDC, SAML, WS-Federation, or OAuth 2.0 applications
- Configure SSO, Platform SSO, or workforce single sign-on
- Manage directories, identity stores, or user populations
- Configure authentication policies, sign-on policies, or branding
- Administer PingFederate, PingAccess, PingDirectory, or PingID
- Deploy or upgrade on-premises Ping software
- Advisory: "How should I structure my tenant?", "What client type should I use?"

## When NOT to use this skill

- If the primary task is **designing a DaVinci flow or PingOne ST journey**: use `ping-orchestration`
- If the task is **configuring a Universal Service** (Protect, Verify, IGA, Credentials) **as a standalone service**: use `ping-universal-services`. If the task is **wiring a Universal Service into a journey or DaVinci flow** (e.g., adding Verify to a registration journey): use `ping-orchestration`
- If the task is **integrating Ping into an app or SDK**: use `ping-app-integration`
- If unsure which platform: use `ping-quickstart` first

## Multi-skill use cases

`ping-foundation` covers the platform layer. Compose with:

| What comes next | Skill |
|---|---|
| Authentication flow or journey logic | `ping-orchestration` |
| Risk, MFA step-up, Verify, IGA, Credentials | `ping-universal-services` |
| App/SDK integration code | `ping-app-integration` |
| AI agent identity | `ping-identity-for-ai` |

## Routing — Step 1: Which platform?

| Platform signal | Branch |
|---|---|
| PingOne admin console, PingOne APIs, PingOne environment | [PingOne](#pingone) |
| PingOne Advanced Identity Cloud (AIC), identity cloud, PingAM, PingIDM, PingDS | [PingOne Advanced Identity Cloud](#pingone-advanced-identity-cloud) |
| PingFederate, PingAccess, PingDirectory, PingID, PingAM standalone | [Ping Software Suite](#ping-software-suite) |

## PingOne

**Curated anchors — pick 1–3 matching the task:**

| Task | Anchor |
|---|---|
| Platform orientation, org/environment structure | `references/curated/cross-platform/foundation-overview.md` |
| Create environment, enable services | `references/curated/pingone-mt/tenant-and-environment-setup.md` |
| Register OIDC, SAML, or Worker app | `references/curated/pingone-mt/app-registration.md` |
| Configure sign-on policy, MFA, step-up | `references/curated/pingone-mt/sign-on-policies.md` |
| Directory, LDAP gateway, populations, groups | `references/curated/pingone-mt/directory-and-populations.md` |
| Admin roles, onboarding administrators | `references/curated/pingone-mt/admin-roles-and-access.md` |
| Themes, branding, custom domain, email/SMS templates, DaVinci UI Studio | `references/curated/pingone-mt/themes-and-branding.md` |
| Cross-platform branding overview | `references/curated/cross-platform/policy-and-branding-basics.md` |

**Generated shortlist** (fallback): `references/generated/pingone-mt/top-25.json` — sub-files: `tenants.md`, `apps.md`, `policies.md`, `directories.md`

## PingOne Advanced Identity Cloud

**Curated anchors — pick 1–3 matching the task:**

| Task | Anchor |
|---|---|
| Platform orientation, tenant/realm architecture | `references/curated/pingone-st/foundation-overview.md` |
| Register OIDC, OAuth 2.0, or SAML applications | `references/curated/pingone-st/app-setup.md` |
| Journeys, nodes, realm auth settings | `references/curated/pingone-st/authentication-fundamentals.md` |
| AM Services configuration (Push, OATH, WebAuthn, Social, OAuth2 Provider, Session, CORS, Base URL, PingOne Worker, etc.) — prerequisite to most journey nodes | `references/curated/pingone-st/am-services.md` |
| Themes, branding, custom CSS | `references/curated/pingone-st/themes-and-customization.md` |
| Identity store, user schema, LDAP/AD | `references/curated/pingone-st/directory-setup.md` |

**Generated shortlist** (fallback): `references/generated/pingone-st/top-25.json`

## Ping Software Suite

**Curated anchors — pick 1–3 matching the task:**

| Task | Anchor |
|---|---|
| PingFederate federation, SP/IdP connections, adapters | `references/curated/ping-software/pingfederate-basics.md` |
| PingDirectory installation, replication, schema | `references/curated/ping-software/pingdirectory-basics.md` |
| PingAccess web app and API protection | `references/curated/ping-software/pingaccess-basics.md` |
| Cross-platform admin patterns (LDAP, OIDC, APIs) | `references/curated/cross-platform/core-admin-patterns.md` |

**Generated shortlist by product** (fallback): `references/generated/ping-software/top-25.json`

## MCP execution

See `references/runtime/mcp-preflight.md` for MCP config and Cursor preflight steps.

## Retrieval and execution

**Rule:** (1) scan for MCP tools first — run the MCP config preflight above before executing; (2) load 1–3 curated anchors for the platform/task; (3) fall back to generated shortlist. Full rules: `references/runtime/docs-mcp-routing.md`.

## Cross-skill escalation

| If the task also involves... | Reference skill |
|---|---|
| DaVinci flows or PingOne ST journey design | `ping-orchestration` |
| Shared services (Protect, Verify, IGA, Credentials) | `ping-universal-services` |
| App/SDK code integration | `ping-app-integration` |
