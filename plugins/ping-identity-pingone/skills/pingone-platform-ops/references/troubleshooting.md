---
title: "Audit Troubleshooting Router"
product_family: pingone-mt
products: ["pingone"]
capabilities: ["validation"]
services: []
audience: ["admin", "operator", "developer"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: false
last_updated: "2026-08-28"
slug: ""
---
# PingOne audit troubleshooting

Select the smallest set of references needed for a bounded PingOne audit investigation. This router owns reference selection; the linked playbooks and catalogs own the detailed procedure and contracts.

## Route by investigation need

| Need | Load first |
|---|---|
| Environment, actor, identifier, time-window, or typed-filter preparation | `playbooks/audit-investigation.md` |
| Audit calls, pagination, full event details, or BOM-based DaVinci entitlement check | `playbooks/audit-execution.md` |
| Failed-login, admin, resource, population, password, MFA/device, or client scenario | `playbooks/audit-scenarios.md` |
| Result tables, summaries, status, and completeness checks | `catalogs/audit-output.md` |
| Errors, PII, unsupported filters, execution fallback, and cross-skill boundaries | `catalogs/audit-guardrails.md` |
| Ping CLI execution mode | `cli.md` |
| Synthetic routing or behavior examples | `examples/sample-prompts.md` |

## Retrieval sequence

1. Load the matching playbook for the user's investigation need.
2. Add `catalogs/audit-output.md` when rendering results, or `catalogs/audit-guardrails.md` when validating errors, safety, or handoff behavior.
3. Add `playbooks/audit-execution.md` for live retrieval, pagination, detail lookup, or the BOM check.
4. Use `cli.md` only when MCP is unavailable; use `examples/sample-prompts.md` only for evaluation or ambiguous routing.
5. Stop when the answer is evidence-backed. Do not load every reference or copy a procedure into another reference.

## Shared operating principles

- Scope every operation to one resolved environment and preserve evidence gaps when a tool is unavailable.
- Use bounded, explicit time windows and typed audit fields; never infer facts from an identifier or construct raw SCIM for the typed MCP tool.
- Treat pagination as part of completeness, and keep audit output and PII in the current session only.
- Keep PingOne audit investigation separate from DaVinci node-level tracing.
