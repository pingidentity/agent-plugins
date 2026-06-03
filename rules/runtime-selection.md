---
title: Runtime selection — sandbox vs production
status: current
last_updated: 2026-05-29
---

# Runtime selection

Decision rule: which runtime applies a plan produced by a Ping skill, and which reference tier to load.

## The two runtime modes

| Mode | What it does | When applied |
|---|---|---|
| **docs** | Output is a written plan: steps, product names, field tables, links to admin console pages. The user (or another agent) executes manually. | Sandbox/orientation, evaluation, learning, no live tenant available. |
| **helix** | Plan is executed by Helix conversation APIs against a live tenant via product-specific tools. Each write is gated. | Production-bound work, when the user has tenant credentials and explicit intent to apply changes. |

Helix is **not** a v1 skill — it is a runtime tier referenced from each skill's `references/runtime/docs-mcp-routing.md`. v1.1 may promote Helix to a first-class skill if it passes the four-criteria decision rule in PLAN.md.

## Decision rule for runtime mode (apply in order)

1. If the user explicitly asks for **a plan**, **explanation**, **walkthrough**, or **evaluation help** → `docs`.
2. If the user names a **sandbox**, **trial**, **POC**, or asks **"how would I…"** → `docs`.
3. If the user names a **production tenant**, asks to **apply / create / update / configure** in a specific tenant, or invokes a `/ping:` command with `--apply` → `helix`.
4. If the user is **unclear**, default to `docs` and ask one clarifying question:
   > "Do you want a plan to apply manually, or should I execute this against a live tenant via Helix?"

## Tier discipline (the strategy doc § 0 "Agent Path" rule)

Within a `docs` plan, choose the smallest tier that resolves the prompt:

1. **Curated anchors** (`references/curated/`) — load 1–3. Stop if sufficient.
2. **Generated shortlist** (`references/generated/<branch>/top-N.json`) — only if curated didn't cover the task.
3. **Docs MCP** (per `references/runtime/docs-mcp-routing.md`) — only if curated + shortlist insufficient.

Layer 3 of the eval scores **Tier discipline (1–5)**: did the produced plan stop at the smallest sufficient tier per the prompt's `expected_tier`?

## Anti-patterns

- ❌ Producing a Helix-style plan when the user is in sandbox mode → over-promises execution.
- ❌ Producing a docs plan when the user explicitly asked to apply → under-delivers.
- ❌ Loading the generated shortlist when one curated anchor is sufficient → wastes tokens.
- ❌ Calling Docs MCP when curated + shortlist would have been enough → wastes tokens and slows the agent.

## Related

- `rules/routing-rules.md` — skill selection precedence
- `evals/scorecards/plan-quality-eval.md` — how tier discipline is scored
- Each skill's `references/runtime/docs-mcp-routing.md`
