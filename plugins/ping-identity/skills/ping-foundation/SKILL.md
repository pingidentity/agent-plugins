---
name: ping-foundation
description: Platform setup, administration, and core configuration for PingOne MT, PingOne ST (AIC), and on-premises Ping software. Use this skill whenever a user asks ANY question about setting up environments, registering OIDC/SAML apps, managing directories and user populations, configuring authentication policies, branding, or administering PingFederate/PingAccess/PingDirectory/PingID — including advisory, planning, and "how should I..." questions, not just execution tasks. Also invoke with /ping-foundation.
compatibility: Designed for Ping Identity platform tasks. MCP tools for PingOne MT or PingOne ST are used when available; console instructions provided as fallback.
metadata:
  publisher: Ping Identity
  version: "1.0"
---

# ping-foundation

Platform setup, administration, and core configuration for all Ping Identity deployments. Covers tenant and environment setup, apps, directories, policies, branding, and on-premises software administration.

> **Role of this skill:** MCP tools handle execution. This skill supplies the context they lack: architecture patterns, correct sequencing, configuration constraints, platform concepts, and guardrails.

## When to use this skill

Trigger on ANY question about setting up, configuring, administering, or planning a Ping Identity platform — including advisory and planning requests:

- Set up or provision environments, tenants, or realms
- Register OIDC, SAML, or OAuth 2.0 applications
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

**Workforce SSO + MFA (PingFederate):** ping-foundation → ping-universal-services (PingID MFA) → ping-app-integration. **CIAM registration (PingOne ST):** ping-foundation → ping-orchestration (registration journey) → ping-universal-services (Verify) → ping-app-integration

---

## Routing — Step 1: Which platform?

| Platform signal | Branch |
|---|---|
| PingOne admin console, PingOne APIs, PingOne environment | [PingOne MT](#pingone-mt) |
| PingOne ST tenant admin, identity cloud, PingAM, PingIDM, PingDS | [PingOne ST](#pingone-st) |
| PingFederate, PingAccess, PingDirectory, PingID, PingAM standalone | [Ping Software Suite](#ping-software-suite) |

---

## PingOne MT

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

---

## PingOne ST

**Curated anchors — pick 1–3 matching the task:**

| Task | Anchor |
|---|---|
| Platform orientation, tenant/realm architecture | `references/curated/pingone-st/foundation-overview.md` |
| Register OIDC, OAuth 2.0, or SAML applications | `references/curated/pingone-st/app-setup.md` |
| Journeys, nodes, realm auth settings | `references/curated/pingone-st/authentication-fundamentals.md` |
| Themes, branding, custom CSS | `references/curated/pingone-st/themes-and-customization.md` |
| Identity store, user schema, LDAP/AD | `references/curated/pingone-st/directory-setup.md` |

**Generated shortlist** (fallback): `references/generated/pingone-st/top-25.json`

---

## Ping Software Suite

**Curated anchors — pick 1–3 matching the task:**

| Task | Anchor |
|---|---|
| PingFederate federation, SP/IdP connections, adapters | `references/curated/ping-software/pingfederate-basics.md` |
| PingDirectory installation, replication, schema | `references/curated/ping-software/pingdirectory-basics.md` |
| PingAccess web app and API protection | `references/curated/ping-software/pingaccess-basics.md` |
| Cross-platform admin patterns (LDAP, OIDC, APIs) | `references/curated/cross-platform/core-admin-patterns.md` |

**Generated shortlist by product** (fallback): `references/generated/ping-software/top-25.json`

---

## Retrieval and execution

**Rule:** (1) scan for MCP tools first; (2) load 1–3 curated anchors for the platform/task; (3) fall back to generated shortlist. Full rules: `references/runtime/docs-mcp-routing.md`.

## Cross-skill escalation

| If the task also involves... | Reference skill |
|---|---|
| DaVinci flows or PingOne ST journey design | `ping-orchestration` |
| Shared services (Protect, Verify, IGA, Credentials) | `ping-universal-services` |
| App/SDK code integration | `ping-app-integration` |
