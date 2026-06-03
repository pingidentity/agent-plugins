---
title: Docs MCP routing — ping-quickstart
status: current
last_updated: 2026-05-29
---

# Runtime tier — Docs MCP routing for ping-quickstart

This file describes when and how this skill falls back to live Docs MCP retrieval. It is the third tier in the strategy doc § 0 "Agent Path".

## When to escalate to Docs MCP

Use Docs MCP only when:
1. The 1–3 curated anchors loaded from `references/curated/` did not answer the question.
2. The bounded shortlist in `references/generated/<branch>/top-N.json` did not fill the gap.
3. The user's task requires version-specific, current, or long-tail information (e.g., a recently released feature, a deprecation note, a specific API field).

If any of these is false, do NOT call Docs MCP. Strategy doc § 0 mandates "use the smallest trusted context first."

## Surgical query rules

When Docs MCP is required, query it with:
- The exact platform family (PingOne MT, PingOne ST, Ping Software Suite)
- The exact product or service name
- The exact capability (e.g., "MFA policy", not "authentication")
- A version constraint when applicable

Retrieve specific sections, not full page dumps.

## Related

- `references/curated/` — tier 1
- `references/generated/` — tier 2
