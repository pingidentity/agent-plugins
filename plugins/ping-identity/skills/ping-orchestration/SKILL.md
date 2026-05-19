---
name: ping-orchestration
description: Design and build authentication flows, journeys, and orchestration logic for Ping Identity platforms. Use for ANY question about DaVinci flows, PingOne ST journeys, PingAM trees, scripted decision nodes, or branching authentication/registration logic — including advisory, planning, "what nodes do I need", "how should I design my flow", and "advise me before I build" requests, not just implementation tasks. Also invoke with /ping-orchestration.
compatibility: Designed for Ping Identity orchestration tasks. MCP tools for PingOne ST are used when available to create and update journeys directly.
metadata:
  publisher: Ping Identity
  version: "1.0"
---

# ping-orchestration

Design and build authentication flows, orchestration logic, and journey-based experiences across Ping Identity platforms.

> **Role of this skill:** MCP tools handle execution — creating, updating, and managing journeys and flow nodes directly. This skill supplies what the tools lack: flow design patterns, node sequencing, branching logic, scripting guidance, and platform-specific constraints. Use it to reason correctly about *what* to build and *why* before (or alongside) using MCP tools to do it.

## Invocation

Invoke this skill explicitly with `/ping-orchestration` or by saying "use ping-orchestration to...".

## When to use this skill

Trigger on ANY of the following — including questions, planning, and advisory requests, not just implementation tasks:

- "Build a login journey in PingOne ST"
- "Design a registration flow with email verification"
- "Create a DaVinci flow for customer login"
- "Add a scripted decision node to my authentication tree"
- "Configure a PingAM authentication tree"
- "Build MFA step-up logic in a journey"
- "Design a self-service password reset flow"
- "Orchestrate identity proofing in a registration journey"
- "What nodes do I need for [flow scenario]?"
- "How should I structure my journey for [use case]?"
- "What's the right way to handle [authentication or registration pattern]?"
- "Advise me on how to design my [journey / DaVinci flow] before I build it"
- "What are the pros and cons of using [node type / flow pattern]?"
- "Help me plan my registration / login / MFA flow"
- "I'm not sure how to approach [journey design challenge]"
- "Should I use inner journeys / scripted nodes / DaVinci connectors for this?"

**Catch-all:** Trigger this skill whenever the user asks ANY question about designing, planning, or advising on authentication flows, journeys, or orchestration logic in PingOne ST, PingOne MT / DaVinci, or PingAM — even before implementation starts, even if phrased as a question or planning discussion.

## When NOT to use this skill

- If the platform is not yet set up (no tenant, no realm, no app registered): use `ping-foundation` first
- If the task is **configuring the platform layer** (apps, directories, policies, branding): use `ping-foundation`
- If the task is **invoking a Universal Service** (Protect, Verify, IGA, Credentials) without needing flow design: use `ping-universal-services`
- If the task is **integrating the flow into an app or SDK**: use `ping-app-integration`
- If unsure which platform: use `ping-quickstart` first

## Multi-skill use cases

Orchestration sits in the middle of the stack — platform foundation must exist before flows can be built, and other skills extend what those flows can do.

| What comes before | Skill |
|---|---|
| Tenant, realm, identity store, and app must be configured first | `ping-foundation` |

| What comes after | Skill |
|---|---|
| Add risk scoring, MFA step-up, identity verification within the flow | `ping-universal-services` |
| Wire the finished flow into a web, mobile, or SDK-based app | `ping-app-integration` |

**Example — CIAM registration with identity proofing on PingOne ST:**
1. `ping-foundation` — provision tenant, configure realm and identity store, register OIDC app
2. `ping-orchestration` — design the registration journey: username collection, email OTP, profile completion
3. `ping-universal-services` — add PingOne Verify node for document and liveness check
4. `ping-app-integration` — integrate the hosted login page into the web or mobile app

**Example — DaVinci workforce SSO with adaptive MFA:**
1. `ping-foundation` — configure PingOne MT environment, add SSO application
2. `ping-orchestration` — build the DaVinci flow: username/password, MFA step-up branch
3. `ping-universal-services` — invoke PingOne Protect for risk-based MFA decision

Complete the platform setup in `ping-foundation` first. Then use this skill for the flow layer. Do not design flows before the underlying platform is configured.

---

## MCP tool-first execution

Before writing any instructions, scan your available tool list for MCP tools that can perform the required operation against the target platform (journey create/update, node update, script create, etc.).

**If matching tools are available:** use them to build or modify the flow directly. Do not write step-by-step console instructions for operations an MCP tool can execute.

**If no matching tools are available:** proceed with curated references and console instructions as described below.

---

## Routing — Step 1: Which platform?

| Platform signal | Branch |
|---|---|
| PingOne ST tenant, PingAM, identity cloud, ForgeRock lineage | [PingOne ST](#pingone-st) |
| PingOne MT + DaVinci | [PingOne MT / DaVinci](#pingone-mt--davinci) |

---

## PingOne ST

**Sub-routing by task:**

| Task | Reference |
|---|---|
| Journey design principles, patterns, resilience, security | `references/curated/pingone-st/journey-design-patterns.md` |
| Node composition rules, PageNode usage, child node gotchas | `references/curated/pingone-st/nodes/node-fundamentals.md` |
| Username/password collection, ValidatedUsernameNodeV2, passthrough auth, session entry, lifecycle outcomes | `references/curated/pingone-st/nodes/basic-auth-nodes.md` |
| MFA: WebAuthn, OATH, push, OTP, recovery codes | `references/curated/pingone-st/nodes/mfa-nodes.md` |
| Risk scoring, lockout, CAPTCHA, auth level, PingOne Authorize | `references/curated/pingone-st/nodes/risk-management-nodes.md` |
| User registration, attributes (PRESENT/EQUALS), consent, KBA, T&C, social login, SelectIdP, TimeSince | `references/curated/pingone-st/nodes/identity-management-nodes.md` |
| Scripting, page composition, session, state, async, polling, LoginCount (AT/EVERY), EmailSuspend/EmailTemplate config | `references/curated/pingone-st/nodes/utility-nodes.md` |
| SAML/OIDC federation, Twilio Verify, device/cookie/cert | `references/curated/pingone-st/nodes/federation-contextual-nodes.md` |
| Scripted Decision node deep-dive | `references/curated/pingone-st/scripted-decision-nodes.md` |
| Inner journeys and reusable flow components | `references/curated/pingone-st/inner-journeys.md` |

**Journey use case patterns** (load when the task matches a named use case):

| Use case | Reference |
|---|---|
| Account recovery, username reminder, anti-enumeration | `references/curated/pingone-st/journey-use-cases/account-recovery-and-username-reminder.md` |
| Password reset (unauthenticated) or password update (authenticated) | `references/curated/pingone-st/journey-use-cases/password-reset-and-update.md` |
| MFA device registration (WebAuthn, OATH, Push, SMS, VOICE) | `references/curated/pingone-st/journey-use-cases/passwordless-mfa-registration.md` |
| Multi-method MFA authentication with retry loops and recovery codes | `references/curated/pingone-st/journey-use-cases/mfa-authentication-multi-method.md` |
| PingOne Protect risk integration (init/eval pattern, step-up chain) | `references/curated/pingone-st/journey-use-cases/pingone-protect-risk-integration.md` |
| Financial services step-up, transaction authorization, PingOne Authorize | `references/curated/pingone-st/journey-use-cases/financial-services-step-up.md` |
| Progressive profiling (login-count trigger, attribute gate) | `references/curated/pingone-st/journey-use-cases/progressive-profiling.md` |
| Social + local registration and authentication, email verification gate | `references/curated/pingone-st/journey-use-cases/social-and-local-registration-authentication.md` |

**Generated shortlist** (fallback):
- `references/generated/pingone-st/top-25.json`

---

## PingOne MT / DaVinci

**Sub-routing by task:**

| Task | Reference |
|---|---|
| DaVinci flow concepts, connectors, variables | `references/curated/pingone-mt/davinci-overview.md` |
| DaVinci flow design patterns | `references/curated/pingone-mt/davinci-flow-patterns.md` |

**Generated shortlist** (fallback):
- `references/generated/pingone-mt/top-25.json`

---

## Retrieval escalation

1. Load 1–3 curated anchors matching the detected platform and task. Stop if sufficient.
2. If not sufficient, scan the matching generated shortlist. Pull summaries for relevant titles only.

## Cross-skill escalation

| If the task also involves... | Reference skill |
|---|---|
| Platform setup not yet complete | `ping-foundation` |
| Shared services (Protect, Verify, IGA, Credentials) within the flow | `ping-universal-services` |
| App/SDK code integration | `ping-app-integration` |
| Platform selection or orientation | `ping-quickstart` |
