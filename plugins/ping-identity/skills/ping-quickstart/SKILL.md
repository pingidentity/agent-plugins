---
name: ping-quickstart
description: Front door for all Ping Identity work. Detects the user's platform and routes to the correct skill. Use for ANY question about where to start, which Ping product to choose, evaluating PingOne vs PingOne ST vs on-premises, or when the platform is unknown — including advisory, evaluation, and "help me decide" requests. Also invoke with /ping-quickstart.
compatibility: Designed for Ping Identity platform tasks. Requires no tools — orientation and routing only.
metadata:
  publisher: Ping Identity
  version: "1.0"
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
- "What are the pros and cons of PingOne vs PingOne ST vs PingFederate?"
- "Should we use the cloud or on-prem version of Ping?"
- "Advise me on which Ping platform fits our use case"
- "Help me understand the Ping Identity product landscape before we commit"

**Catch-all:** Trigger this skill whenever the user's platform or starting point is unknown or unclear, or when they are in evaluation/planning mode and need orientation before selecting a product or skill.

## When NOT to use this skill

- If you already know the platform and task: use the appropriate skill directly (`ping-foundation`, `ping-orchestration`, etc.)

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
2. "Is this for employees (workforce) or customers (CIAM)?"
3. "Are you working in PingOne, PingOne ST, or on-premises software?"

---

## Orientation references

Load 1–2 of these matching the user's question. Stop when orientation is sufficient.

- `references/getting-started-overview.md`
- `references/choose-the-right-ping-platform.md`
- `references/common-starting-patterns.md`
