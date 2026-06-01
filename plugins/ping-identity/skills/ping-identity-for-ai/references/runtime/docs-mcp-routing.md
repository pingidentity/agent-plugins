---
title: Docs MCP routing — ping-identity-for-ai
product_family: cross-platform
capabilities: ["identity-for-ai"]
doc_type: reference
canonical: false
audience: ["developer", "architect"]
status: current
last_updated: 2026-05-29
---

# Runtime tier — Docs MCP routing for ping-identity-for-ai

This file describes when and how this skill falls back to live Docs MCP retrieval. It is the third tier in the strategy doc § 0 "Agent Path".

## When to escalate to Docs MCP

Use Docs MCP only when:
1. The 1–3 curated anchors loaded from `references/curated/` did not answer the question.
2. The bounded shortlist in `references/generated/<branch>/top-N.json` did not fill the gap.
3. The user's task requires version-specific, current, or long-tail information.

If any of these is false, do NOT call Docs MCP. Strategy doc § 0 mandates "use the smallest trusted context first."

## Surgical query rules

When Docs MCP is required, query it with:
- The exact platform family (PingOne MT, PingOne ST, Ping Software Suite)
- The exact product or service name
- The exact capability
- A version constraint when applicable

Retrieve specific sections, not full page dumps.

## Helix as a runtime path

Production-bound execution runs through Helix conversation APIs. Helix is **not** a v1 skill; it is a runtime tier referenced from this file.

### Sandbox vs production decision rule (apply in order)

1. If the user asks for a plan, explanation, walkthrough, or evaluation help → `docs` mode.
2. If the user names a sandbox, trial, POC, or asks "how would I…" → `docs` mode.
3. If the user names a production tenant, asks to apply/create/update/configure in a specific tenant, or invokes a `/ping:` command with `--apply` → `helix` mode.
4. If the user is unclear, default to `docs` and ask one clarifying question: "Do you want a plan to apply manually, or should I execute this against a live tenant via Helix?"

## Related

- `references/curated/` — tier 1
- `references/generated/` — tier 2
