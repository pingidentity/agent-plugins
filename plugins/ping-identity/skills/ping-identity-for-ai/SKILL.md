---
name: ping-identity-for-ai
description: AI-era identity patterns for the Ping Identity platform. Use this skill whenever a task involves giving an AI agent a verified identity, securing agent-to-API access, applying Verified Trust signals, designing identity for AI workloads, workforce helpdesk AI authentication patterns, or Ping Identity's Identity for AI solution references. Also invoke with /ping-identity-for-ai.
compatibility: Designed for AI identity and agent security work on Ping Identity platforms. References product docs and Ping Labs content.
metadata:
  publisher: Ping Identity
  version: "0.1.0-scaffold"
---

# ping-identity-for-ai

> **Status:** Phase 0 scaffold per strategy doc § 4. Body authored in Phase 1. Routing logic stub only.

AI-era identity patterns: Identity for AI, Verified Trust, agent identity, agent security, and AI application authentication.

## Invocation

Invoke explicitly with `/ping-identity-for-ai` or by saying "use ping-identity-for-ai to...".

## When to use this skill

- "Give my AI agent a verified identity for API access"
- "Use Verified Trust signals in my MCP server"
- "Secure agent-to-agent authentication using Ping"
- "Workforce helpdesk AI — how do I authenticate users for my AI assistant?"
- "Identity for AI architecture with Ping"
- "AI app authentication patterns on PingOne"
- "Agent security and authorization for agentic workflows"

## When NOT to use this skill

- If the task is general platform setup: use `ping-foundation`.
- If the task is building a flow or journey (not AI-specific): use `ping-orchestration`.
- If the task is app integration (not AI-specific): use `ping-app-integration`.
- If the user is just orienting: use `ping-quickstart`.

## Multi-skill use cases

A complete AI identity solution typically spans:

| Layer | Skill |
|---|---|
| Platform setup | `ping-foundation` |
| Auth flow / journey design | `ping-orchestration` |
| AI identity patterns and Verified Trust | `ping-identity-for-ai` (this skill) |
| App / SDK integration | `ping-app-integration` |

## Routing — Step 1: What are you trying to do?

| Task | Branch |
|---|---|
| Give an AI agent an identity / machine-to-machine auth | Agent identity patterns |
| Apply Verified Trust signals | Verified Trust branch |
| Workforce helpdesk AI authentication | Workforce AI branch |
| AI application (LLM app) authentication | AI app auth branch |
| Strategy / positioning for Identity for AI | Overview / strategy branch |

## Step 2: Platform branch

| Platform | Curated reference |
|---|---|
| PingOne MT / ST | `references/curated/identity-for-ai-overview.md` (Phase 1) |
| Cross-platform | `references/curated/verified-trust-overview.md` (Phase 1) |

## Retrieval escalation

Per strategy doc § 0:

1. Curated anchors (`references/curated/`) — load 1–3 max. Stop if sufficient.
2. Generated shortlist (`references/generated/top-20.json`) — Phase 2.
3. Docs MCP fallback — see `references/runtime/docs-mcp-routing.md`. Only if curated + shortlist insufficient.
