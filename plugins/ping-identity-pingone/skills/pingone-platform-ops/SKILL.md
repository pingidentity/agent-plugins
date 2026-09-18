---
name: pingone-platform-ops
description: "Use this skill whenever a user needs a PingOne audit-event investigation: failed logins, authentication history, admin actions, compliance or event-history queries, correlation IDs, resource events, password or MFA events, pagination, or a BOM-based hint about DaVinci execution troubleshooting."
compatibility: "Requires authorized PingOne MCP audit tools or Ping CLI access."
metadata:
  publisher: Ping Identity
  version: "2.0.0"
---

# PingOne Platform Operations

Route PingOne audit and operational investigations to the smallest sufficient reference. Preserve evidence, scope every query to one environment, and avoid persisting audit output or PII.

## When to use this skill

- Investigate failed logins, authentication history, admin actions, compliance events, or event history.
- Trace a PingOne correlation ID or inspect application, user, population, password, or MFA/device events.
- Explain who changed what, when an event occurred, or why an audit query returned no results.
- Retrieve paginated audit activity and render a complete event table and pattern summary.
- Check the environment Bill of Materials (BOM) for DaVinci availability.

## When NOT to use this skill

- DaVinci node-level execution tracing.
- User, application, directory, or tenant configuration.
- Flow design or universal-service policy changes.
- App or SDK integration.

## Multi-skill use cases

Audit findings often identify an operational symptom while the remediation belongs to another discipline:

1. Investigate audit events here and preserve correlation IDs as evidence.
2. If a finding points at a DaVinci flow execution, hand the node-level trace to the flow-execution troubleshooting workflow available in the session.
3. If a finding points at configuration or policy, hand the fix to the platform-configuration or universal-service workflow that owns it.

Complete the audit investigation here, then hand off to whichever workflow owns the remediation.

## Routing — Step 1: Investigation need

| Need | Load first |
|---|---|
| Reference selection and retrieval stopping | `references/troubleshooting.md` |
| Environment, actor, identifier, time-window, or typed-filter preparation | `references/playbooks/audit-investigation.md` |
| Audit calls, pagination, full event details, or DaVinci entitlement check | `references/playbooks/audit-execution.md` |
| Common failed-login, admin, resource, population, password, MFA, or client scenarios | `references/playbooks/audit-scenarios.md` |
| Result tables, summaries, structured status, and completeness checks | `references/catalogs/audit-output.md` |
| Errors, PII, execution-mode fallback, and cross-skill boundaries | `references/catalogs/audit-guardrails.md` |
| Ping CLI audit and BOM operations | `references/cli.md` |
| Synthetic routing and behavior examples | `references/examples/sample-prompts.md` |

## Retrieval escalation

1. Load `references/troubleshooting.md` to select the smallest sufficient reference.
2. Load one matching playbook, then add only the required catalog or execution-mode reference.
3. Load `references/examples/sample-prompts.md` only for evaluation or ambiguous routing.
4. Stop when the evidence-backed answer is complete.

## Execution boundary

Use connected MCP tools after inspecting their schemas. The mandatory audit capability is `listEnvironments`, `searchAuditActivities`, and `getAuditActivity`; use `listUsers`, `listApplications`, or `listPopulations` only for required identifier resolution. Use Ping CLI guidance when MCP is unavailable. Never construct raw SCIM filters when the typed audit tool exposes discrete fields.
