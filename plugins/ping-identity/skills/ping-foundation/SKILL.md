---
name: ping-foundation
description: "Use when setting up, configuring, or administering any Ping Identity platform — PingOne, PingOne Advanced Identity Cloud (AIC), or Ping Advanced Identity Software (PingAM, PingFederate, PingAccess, PingDirectory, PingID). Covers tenant/environment creation, app registration (including Worker apps and service accounts for M2M API access), SSO, directories, policies, branding, and CLI-driven configuration automation (pingcli, Terraform/CaC export, multi-env promotion). Requires a named or clearly implied platform."
compatibility: Designed for Ping Identity platform tasks. MCP tools for PingOne and PingOne Advanced Identity Cloud (AIC) are used when available; console instructions provided as fallback.
metadata:
  publisher: Ping Identity
  version: "1.0.0"
---

# ping-foundation

Platform setup, administration, and core configuration for all Ping Identity deployments. Covers tenant and environment setup, apps, directories, policies, branding, and on-premises software administration. MCP tools handle execution; this skill supplies architecture patterns, sequencing, configuration constraints, and guardrails.

**What this skill does for you:** Generates configuration and drives setup directly through MCP tools where they exist (PingOne, AIC); where a tool does not exist, it guides you through the docs with the correct sequencing, field constraints, and guardrails. Both modes are available — it uses whichever the platform supports for the task.

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
- Automate configuration with Ping CLI (`pingcli`), export Terraform/CaC packages, or manage multi-environment promotion pipelines
- Advisory: "How should I structure my tenant?", "What client type should I use?"

## When NOT to use this skill

- If the primary task is **designing a DaVinci flow or PingOne Advanced Identity Cloud journey**: use `ping-orchestration`
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

## Ping Software Suite

**Curated anchors — pick 1–3 matching the task:**

| Task | Anchor |
|---|---|
| PingFederate federation, SP/IdP connections, adapters | `references/curated/ping-software/pingfederate-basics.md` |
| PingDirectory installation, replication, schema | `references/curated/ping-software/pingdirectory-basics.md` |
| PingAccess web app and API protection | `references/curated/ping-software/pingaccess-basics.md` |
| Cross-platform admin patterns (LDAP, OIDC, APIs) | `references/curated/cross-platform/core-admin-patterns.md` |

## Cross-platform tooling

| Task | Anchor |
|---|---|
| CLI-driven config, multi-env profiles, Terraform/CaC export across PingOne, DaVinci, PingFederate | `references/curated/cross-platform/ping-cli-basics.md` |
| Promote configuration between environments (PingOne native promotion, AIC self-service promotions, Ping CLI + Terraform config-as-code) | `references/curated/cross-platform/config-promotion.md` |

## MCP execution

See `references/runtime/mcp-preflight.md` for MCP config and Cursor preflight steps.

## Retrieval and execution

**Rule:** (1) scan for MCP tools first — run the MCP config preflight above before executing; (2) load 1–3 curated anchors for the platform/task.

## Cross-skill escalation

| If the task also involves... | Reference skill |
|---|---|
| DaVinci flows or PingOne Advanced Identity Cloud journey design | `ping-orchestration` |
| Shared services (Protect, Verify, IGA, Credentials) | `ping-universal-services` |
| App/SDK code integration | `ping-app-integration` |
