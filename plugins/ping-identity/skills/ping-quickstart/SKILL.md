---
name: ping-quickstart
description: Use this skill whenever the Ping Identity platform is unknown, the user needs orientation, or no other skill clearly owns the request. Triggers: "where do I start with Ping", "which Ping product do I need", "should we use PingOne or PingFederate", "PingOne vs AIC vs PingFederate", "help me choose", "I'm new to Ping", "I inherited a Ping deployment", "evaluating Ping Identity", "migrating from ForgeRock or Okta", "where do we start with [any Ping feature]", "recommended starting point", "test this end to end and tell me what to change", "validate my Ping setup before going live". Catch-all when platform is unspecified and intent is unclear — route here first, then hand off. Also invoke with /ping-quickstart.
compatibility: Designed for Ping Identity platform tasks. Requires no tools — orientation and routing only.
metadata:
  publisher: Ping Identity
  version: "1.0.0"
---

# ping-quickstart

Front door for all Ping Identity work. Detects the user's platform, identifies what they are trying to accomplish, and routes them to the correct skill.

## Invocation

Invoke this skill explicitly with `/ping-quickstart` or by saying "use ping-quickstart to...".

## When to use this skill

Trigger on ANY of the following — including questions, evaluation discussions, and advisory requests:

- "Where do I start with Ping Identity?"
- "Which Ping product do I need?"
- "Help me choose between PingOne, PingOne ST, and PingFederate"
- "I'm new to Ping — what should I set up first?"
- "I inherited a Ping deployment and don't know where to begin"
- "We're evaluating Ping Identity — what should we be asking?"
- "Pros and cons of PingOne vs PingOne ST vs PingFederate; cloud or on-prem?"
- "Advise me on which Ping platform fits our use case"
- "We're migrating from ForgeRock to Ping — what does the migration path look like?"
- "Where do we start with adding [feature] to our app?" (any feature, when the platform is unspecified)
- "We want to add identity verification / KYC — where do we start?"
- "What's the recommended starting point for Ping employee identity?"
- "What license do I need for DaVinci / Protect / Verify?"
- "I inherited a Ping deployment — where do I start?"
- "Test this end to end / validate my Ping setup / how do I prove the path works before going live"

**Catch-all rule:** Trigger this skill whenever the user's platform or starting point is unknown or unclear, when they use "where do we start", "what should we set up first", "what's the recommended starting point", or "not sure whether to use [product A] or [product B]" framing. Trigger on migration intents (ForgeRock → Ping, Okta → Ping, Auth0 → Ping). Trigger when platform is not yet specified and the user is in evaluation or orientation mode.

## When NOT to use this skill

- User asks to configure a PingOne OIDC application → use `ping-foundation`
- User asks to build a registration journey or DaVinci flow in PingOne ST → use `ping-orchestration`
- User asks to integrate the Ping iOS or Android SDK → use `ping-app-integration`
- User asks about PingOne Protect risk scoring, PingOne Verify, or PingOne MFA policy → use `ping-universal-services`
- User asks about Verified Trust, AI agent identity, or securing AI agents with Ping → use `ping-identity-for-ai`
- User asks to configure PingFederate adapters or PingAccess policies on an existing deployment → use `ping-foundation`
- User already knows their platform (PingOne, PingOne ST, or Ping Software) and knows their task → skip this skill and use the relevant skill directly

## Multi-skill use cases

Ping Identity platforms are deeply layered — a complete, production-ready solution almost always requires more than one skill. This is by design, not a gap.

A single end-to-end use case typically spans:

| Layer | Skill |
|---|---|
| Platform setup and app registration | `ping-foundation` |
| Authentication flow or journey design | `ping-orchestration` |
| MFA, risk, verification, or governance | `ping-universal-services` |
| App or SDK integration | `ping-app-integration` |
| AI agent or trusted identity patterns | `ping-identity-for-ai` |

**Example — Customer registration with identity verification:**
1. `ping-foundation` — provision the environment, register the app, configure the directory
2. `ping-orchestration` — design the DaVinci flow or PingOne ST journey for registration
3. `ping-universal-services` — invoke PingOne Verify for document/liveness check within the flow
4. `ping-app-integration` — wire the SDK into the mobile or web app

Skills are designed to be composed. Load them in sequence as the task progresses — do not try to satisfy all layers from a single skill. Use `ping-quickstart` (this skill) to orient, then hand off to the appropriate skill for each layer.

---

## Routing — Step 1: What is the user trying to do?

| Intent | Route to |
|---|---|
| Set up or configure a platform, tenant, or app | [Platform Detection](#step-2--detect-the-platform) → `ping-foundation` |
| Build or design flows, journeys, or orchestration | [Platform Detection](#step-2--detect-the-platform) → `ping-orchestration` |
| Use a shared service (Protect, Verify, IGA, Credentials) | `ping-universal-services` |
| Integrate Ping into an app, mobile, or web SDK | `ping-app-integration` |
| AI agent identity, Verified Trust, or agent security | `ping-identity-for-ai` |
| Still unclear — ask one clarifying question | Stay in this skill; use clarifying questions below |

---

## Step 2 — Detect the platform

Ask or infer from context:

| Signal | Platform family | Next skill |
|---|---|---|
| "PingOne", "admin console at apps.pingone.com", "PingOne environment" | PingOne MT | `ping-foundation` → `pingone-mt` branch |
| "AIC", "PingOne ST", "identity cloud", "PingOne ST", "PingAM", "IDM", "ForgeRock" | PingOne ST | `ping-foundation` → `pingone-st` branch |
| "PingFederate", "PingAccess", "PingDirectory", "on-prem", "self-managed" | Ping Software Suite | `ping-foundation` → `ping-software` branch |
| Platform unknown | Ask: "Are you working in PingOne, PingOne ST, or on-premises software?" | — |

---

## Step 3 — Clarifying questions (use only if intent and platform are both unclear)

Ask at most one question at a time:

1. "Are you setting something up for the first time, or do you have an existing deployment?"
2. "Are you working in PingOne, PingOne ST, or on-premises software?"

---

## Orientation references

Load 1–2 of these matching the user's question. Stop when orientation is sufficient.

- `references/curated/getting-started-overview.md`
- `references/curated/choose-the-right-ping-platform.md`
- `references/curated/common-starting-patterns.md`
- `references/curated/pingone-licensing-and-packaging.md`
- `references/curated/forgerock-to-ping-migration-paths.md`
- `references/curated/inherited-deployment-orientation.md`
- `references/curated/end-to-end-validation.md` — load when the user is past the build phase and asking "test what I just built"
