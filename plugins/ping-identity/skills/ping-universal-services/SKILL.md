---
name: ping-universal-services
description: Shared services skill for strategic value layers used across PingOne MT, PingOne ST (AIC), and Ping Software Suite — Protect, Verify, Credentials, IGA, SSO, and Authorize. Use this skill whenever a task involves a Universal Service consumed from multiple platforms rather than administered from one platform alone. Covers service selection guidance, invocation patterns from PingOne or AIC, policy and verification patterns, cross-product service usage, and positioning. Also invoke with /ping-universal-services.
compatibility: Designed for Ping Identity shared services work. References product docs and the Ping Marketplace.
metadata:
  publisher: Ping Identity
  version: "0.1.0-scaffold"
---

# ping-universal-services

> **Status:** Phase 0 scaffold per strategy doc § 4. Body authored in Phase 1. Routing logic stub only.

Shared strategic services used across PingOne and AIC rather than a single-product admin surface.

## Invocation

Invoke explicitly with `/ping-universal-services` or by saying "use ping-universal-services to...".

## When to use this skill

- "Add PingOne Protect risk evaluation to my login flow"
- "Use PingOne Verify for KYC / identity proofing during registration"
- "Issue or present a verifiable credential"
- "Add IGA governance to my PingOne environment"
- "Use PingOne Authorize for fine-grained authorization"
- "Score risk with PingOne Protect and adapt the journey based on the signal"
- "Cross-platform service selection — which shared service do I need?"

## When NOT to use this skill

- If the task is platform setup or admin: use `ping-foundation`.
- If the task is flow / journey design (without a specific service invocation): use `ping-orchestration`.
- If the user is just orienting or choosing a platform: use `ping-quickstart`.
- If the task is app / SDK integration: use `ping-app-integration`.

## Multi-skill use cases

A complete identity verification or risk-based flow typically spans:

| Layer | Skill |
|---|---|
| Platform setup | `ping-foundation` |
| Flow / journey design | `ping-orchestration` |
| Service invocation (Protect, Verify, etc.) | `ping-universal-services` (this skill) |
| App integration | `ping-app-integration` |

## Routing — Step 1: What are you trying to do?

| Task | Branch |
|---|---|
| Evaluate risk or adapt flows based on risk signals | Protect branch |
| Identity proofing / document + liveness check | Verify branch |
| Issue or present verifiable credentials | Credentials branch |
| Governance, access reviews, provisioning | IGA branch |
| Fine-grained authorization policies | Authorize / SSO branch |
| "Which service do I need?" | Cross-service selection (curated overview) |

## Step 2: Platform branch

| Platform | Curated reference |
|---|---|
| PingOne MT | `references/curated/<service>.md` (Phase 1) |
| PingOne ST (AIC) | `references/curated/<service>.md` (Phase 1) |
| Cross-platform | `references/curated/universal-services-overview.md` (Phase 1) |

## Retrieval escalation

Per strategy doc § 0:

1. Curated anchors (`references/curated/`) — load 1–3 max. Stop if sufficient.
2. Generated shortlist (`references/generated/<service>/top-N.json`) — Phase 2.
3. Docs MCP fallback — see `references/runtime/docs-mcp-routing.md`. Only if curated + shortlist insufficient.
