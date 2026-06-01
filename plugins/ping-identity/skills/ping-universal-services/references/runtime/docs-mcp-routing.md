---
title: Docs MCP routing — ping-universal-services
product_family: cross-platform
capabilities:
  - universal-services
doc_type: reference
status: current
canonical: false
last_updated: "2026-05-29"
---

# Runtime tier — Docs MCP routing for ping-universal-services

This file describes when and how this skill falls back to live Docs MCP retrieval. It is the third (last-resort) tier in the retrieval hierarchy.

## When to escalate to Docs MCP

Use Docs MCP only when:
1. The 1–3 curated anchors loaded from `references/curated/` did not answer the question.
2. The generated shortlists in `references/generated/<service>/` did not fill the gap (or are not yet populated).
3. The user's task requires version-specific, current, or long-tail information.

If any of these is false, do NOT call Docs MCP. The retrieval rule is: use the smallest trusted context first.

## Surgical query rules

When Docs MCP is required, query it with:
- The exact platform family (PingOne MT, PingOne ST, Ping Software Suite)
- The exact product or service name
- The exact capability
- A version constraint when applicable

Retrieve specific sections, not full page dumps.

## Helix as a runtime path

Production-bound execution runs through Helix conversation APIs. The runtime selection decision (sandbox vs production) is: prefer sandbox for development and testing; use production Helix endpoints only when the execution context is confirmed as a production agent run. Helix is not a skill; it is a runtime tier that wraps skill execution.

## Related

- `references/curated/` — tier 1
- `references/generated/` — tier 2 (not yet populated)
