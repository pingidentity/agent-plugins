---
name: ping-orchestration
description: Use this skill whenever you need to design, build, plan, or advise on authentication flows, journeys, or orchestration logic for Ping Identity platforms — including DaVinci flows, PingOne ST journeys, PingAM trees, scripted decision nodes, and branching authentication/registration logic. When the intent is a platform or product comparison ("AIC vs DaVinci?", "journey vs DaVinci flow?", "which platform for my login flow?") without specifying the use case, workforce vs CIAM context, or platform, ask a clarifying question about the use case or platform before answering. When the platform is unspecified and matters (e.g., MFA configuration differs by platform), ask which platform before advising. Also invoke with /ping-orchestration.
compatibility: Designed for Ping Identity orchestration tasks. MCP tools for PingOne ST are used when available to create and update journeys directly.
metadata:
  publisher: Ping Identity
  version: "1.0"
---

# ping-orchestration

Design and build authentication flows, orchestration logic, and journey-based experiences across Ping Identity platforms. MCP tools handle execution; this skill supplies design patterns, node sequencing, branching logic, and platform-specific constraints.

## Invocation

Invoke this skill explicitly with `/ping-orchestration` or by saying "use ping-orchestration to...".

## When to use this skill

Trigger on ANY question — including advisory, planning, and "what nodes do I need" requests, not just implementation — when the task involves:
- Building or designing a login, registration, recovery, MFA, or step-up journey in PingOne ST / AIC / PingAM
- Creating or designing a DaVinci flow for authentication, MFA, or orchestration
- Configuring a PingAM authentication tree or scripted decision node
- Planning or reviewing journey structure before implementation
- Deciding between inner journeys, scripted nodes, or DaVinci connectors
- Any question about designing, planning, or advising on authentication flows, journeys, or orchestration logic in PingOne ST, PingOne MT / DaVinci, or PingAM

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

**Example — CIAM registration with identity proofing:** `ping-foundation` → `ping-orchestration` (journey design) → `ping-universal-services` (PingOne Verify) → `ping-app-integration` (SDK wiring).

**Example — DaVinci workforce SSO:** `ping-foundation` → `ping-orchestration` (DaVinci flow) → `ping-universal-services` (PingOne Protect).

---

## MCP tool-first execution

Scan available tools for MCP tools that can perform the required operation. If matching tools are available, use them directly. Otherwise, proceed with curated references.

---

## Routing — Step 1: Which platform?

| Platform signal | Branch |
|---|---|
| PingOne ST tenant, PingAM, identity cloud, ForgeRock lineage | [PingOne ST](#pingone-st) |
| PingOne MT + DaVinci | [PingOne MT / DaVinci](#pingone-mt--davinci) |

---

## PingOne ST

Sub-routing by task and journey use case: see `references/curated/pingone-st/routing-index.md`.

**Quick reference — node families:**

| Task | Reference |
|---|---|
| Journey design principles, patterns, resilience, security | `references/curated/pingone-st/journey-design-patterns.md` |
| Node composition rules, PageNode usage, child node gotchas | `references/curated/pingone-st/nodes/node-fundamentals.md` |
| Username/password, passthrough auth, session entry, lifecycle outcomes | `references/curated/pingone-st/nodes/basic-auth-nodes.md` |
| MFA: WebAuthn, OATH, push, OTP, recovery codes | `references/curated/pingone-st/nodes/mfa-nodes.md` |
| Risk scoring, lockout, CAPTCHA, auth level, PingOne Authorize | `references/curated/pingone-st/nodes/risk-management-nodes.md` |
| Registration, attributes, consent, KBA, T&C, social login, SelectIdP | `references/curated/pingone-st/nodes/identity-management-nodes.md` |
| Scripting, page composition, session, state, async, polling, LoginCount | `references/curated/pingone-st/nodes/utility-nodes.md` |
| SAML/OIDC federation, Twilio Verify, device/cookie/cert | `references/curated/pingone-st/nodes/federation-contextual-nodes.md` |

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
