---
name: ping-foundation
description: Platform setup, administration, and core configuration for PingOne MT, PingOne ST (AIC), and on-premises Ping software. Use for ANY question about setting up environments, registering OIDC/SAML apps, managing directories and user populations, configuring authentication policies, branding, or administering PingFederate/PingAccess/PingDirectory/PingID — including advisory, planning, and "how should I..." questions, not just execution tasks. Also invoke with /ping-foundation.
compatibility: Designed for Ping Identity platform tasks. MCP tools for PingOne MT or PingOne ST are used when available; console instructions provided as fallback.
metadata:
  publisher: Ping Identity
  version: "1.0"
---

# ping-foundation

Platform setup, administration, and core configuration for all Ping Identity deployments. Covers tenant and environment setup, apps, directories, policies, branding, and on-premises software administration.

> **Role of this skill:** MCP tools handle execution — they can create, update, and delete platform resources directly. This skill supplies the context those tools lack: architecture patterns, correct sequencing, configuration constraints, platform concepts, and guardrails. Use it to reason correctly about *what* to do and *why* before (or alongside) using MCP tools to do it.

## Invocation

Invoke this skill explicitly with `/ping-foundation` or by saying "use ping-foundation to...".

## When to use this skill

Trigger on ANY of the following — including questions, planning, and advisory requests, not just implementation tasks:

- "Set up a PingOne environment"
- "Configure an application in PingOne MT or PingOne ST"
- "Manage directories, identity stores, or user populations"
- "Configure authentication policies or sign-on policies"
- "Set up branding, custom domains, or notification templates"
- "Administer PingFederate, PingAccess, PingDirectory, or PingID"
- "Deploy or upgrade on-premises Ping software"
- "Register an OIDC or SAML app in AIC / PingOne ST"
- "What do I need to configure to get [app type] working?"
- "How should I set up my tenant / realm / environment?"
- "What's the right way to structure my directory / populations?"
- "Should I use a confidential or public client for my app?"
- "Advise me on how to configure [platform feature]"
- "What are the pros and cons of [platform configuration option]?"
- "Help me plan my PingOne ST / PingOne MT setup before I build"
- "I'm not sure how to approach [admin or configuration task] in Ping"

**Catch-all:** Trigger this skill whenever the user asks ANY question about setting up, configuring, administering, or planning a Ping Identity platform — even if phrased as a question, a planning discussion, or an advisory request rather than a direct "do this" instruction.

## When NOT to use this skill

- If the primary task is **designing a DaVinci flow or PingOne ST journey**: use `ping-orchestration`
- If the task is **invoking a Universal Service** (Protect, Verify, IGA, Credentials): use `ping-universal-services`
- If the task is **integrating Ping into an app or SDK**: use `ping-app-integration`
- If unsure which platform: use `ping-quickstart` first

## Multi-skill use cases

Foundation is almost always the starting point, but rarely the only skill needed. Ping Identity platforms require significant configuration across multiple layers to reach a complete, production-ready solution — expect to compose several skills together.

`ping-foundation` is responsible for the platform layer. Other skills pick up where it leaves off:

| What comes next | Skill |
|---|---|
| Authentication flow or journey logic on top of the configured platform | `ping-orchestration` |
| Adding risk, MFA step-up, identity verification, or governance | `ping-universal-services` |
| Wiring the configured platform into an app, SDK, or mobile client | `ping-app-integration` |
| Securing AI agents or building trusted identity for AI workloads | `ping-identity-for-ai` |

**Example — Workforce SSO with MFA and PingFederate:**
1. `ping-foundation` — install PingFederate, configure the SP connection, connect PingDirectory
2. `ping-foundation` — configure the authentication policy / adapter chain
3. `ping-universal-services` — add PingID MFA step-up via the PingOne MFA adapter
4. `ping-app-integration` — configure the application to use the PingFederate OIDC or SAML endpoint

**Example — CIAM registration on PingOne ST:**
1. `ping-foundation` — provision the PingOne ST tenant, configure the realm and identity store
2. `ping-orchestration` — design the registration journey with email verification
3. `ping-universal-services` — add PingOne Verify for identity proofing within the journey
4. `ping-app-integration` — integrate the PingOne ST-hosted login page into the web or mobile app

Do not attempt to drive all of this from `ping-foundation` alone. Complete the platform setup here, then hand off to the appropriate skill for each subsequent layer.

---

## Routing — Step 1: Which platform?

| Platform signal | Branch |
|---|---|
| PingOne admin console, PingOne APIs, PingOne environment | [PingOne MT](#pingone-mt) |
| PingOne ST tenant admin, identity cloud, PingAM, PingIDM, PingDS | [PingOne ST](#pingone-st) |
| PingFederate, PingAccess, PingDirectory, PingID, PingAM standalone | [Ping Software Suite](#ping-software-suite) |

---

## PingOne MT

**Sub-routing by task:**

| Task | Reference |
|---|---|
| Create or manage environments/tenants | `references/generated/pingone-mt/tenants.md` |
| Add or configure applications (OIDC, SAML) | `references/generated/pingone-mt/apps.md` |
| Configure sign-on policies, MFA policies | `references/generated/pingone-mt/policies.md` |
| Manage directories, populations, user attributes | `references/generated/pingone-mt/directories.md` |

**Curated anchors** (load first — 1 to 3 max):
- `references/curated/cross-platform/foundation-overview.md`
- `references/curated/cross-platform/tenant-and-environment-setup.md`
- `references/curated/cross-platform/policy-and-branding-basics.md`

**Generated shortlist** (fallback):
- `references/generated/pingone-mt/top-25.json`

---

## PingOne ST

**Sub-routing by task:**

| Task | Reference |
|---|---|
| Platform orientation, tenant/realm architecture | `references/curated/pingone-st/foundation-overview.md` |
| Register OIDC, OAuth 2.0, or SAML applications | `references/curated/pingone-st/app-setup.md` |
| Understand journeys, nodes, realm auth settings | `references/curated/pingone-st/authentication-fundamentals.md` |
| Themes, branding, custom CSS, hosted pages | `references/curated/pingone-st/themes-and-customization.md` |
| Identity store, user schema, LDAP/AD, provisioning | `references/curated/pingone-st/directory-setup.md` |
| Reporting, auditing, logs | `references/generated/pingone-st/reports.md` |
| Self-service portal, end-user flows | `references/generated/pingone-st/self-service.md` |

**Curated anchors** (load first — 1 to 3 max, pick the ones matching the task):
- `references/curated/pingone-st/foundation-overview.md`
- `references/curated/pingone-st/app-setup.md`
- `references/curated/pingone-st/authentication-fundamentals.md`
- `references/curated/pingone-st/themes-and-customization.md`
- `references/curated/pingone-st/directory-setup.md`

**Generated shortlist** (fallback for topics not yet covered by curated files):
- `references/generated/pingone-st/top-25.json`

---

## Ping Software Suite

**Sub-routing by product:**

| Product | Reference |
|---|---|
| PingFederate | `references/generated/ping-software/pingfederate.md` |
| PingAccess | `references/generated/ping-software/pingaccess.md` |
| PingDirectory | `references/generated/ping-software/pingdirectory.md` |
| PingID (on-prem) | `references/generated/ping-software/pingid.md` |
| PingAM (standalone) | `references/generated/ping-software/pingam.md` |

**Curated anchors** (load first):
- `references/curated/cross-platform/foundation-overview.md`
- `references/curated/cross-platform/core-admin-patterns.md`

**Generated shortlist** (fallback):
- `references/generated/ping-software/top-25.json`

---

## MCP tool-first execution

Before writing any instructions, scan your available tool list for MCP tools that can perform the required operation against the target platform (PingOne ST, PingOne MT, etc.).

**If matching tools are available:** use them to perform the configuration directly. Do not write step-by-step console instructions for operations an MCP tool can execute. Only provide instructions for steps no tool covers (portal-only actions, unsupported operations).

**If no matching tools are available:** proceed with curated references and console instructions as described below.

## Retrieval escalation

1. Load 1–3 curated anchors matching the detected platform and task. Stop if sufficient.
2. If not sufficient, scan the matching generated shortlist. Pull summaries for relevant titles only.

## Cross-skill escalation

| If the task also involves... | Reference skill |
|---|---|
| DaVinci flows or PingOne ST journey design | `ping-orchestration` |
| Shared services (Protect, Verify, IGA, Credentials) | `ping-universal-services` |
| App/SDK code integration | `ping-app-integration` |
| Platform selection or orientation | `ping-quickstart` |
