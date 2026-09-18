---
title: "Audit Guardrails"
product_family: pingone-mt
products: ["pingone"]
capabilities: ["validation"]
services: []
audience: ["admin", "operator", "developer"]
use_cases: ["workforce", "customer"]
doc_type: reference
status: current
canonical: false
last_updated: "2026-08-26"
slug: ""
---
# PingOne audit guardrails

Covers error handling, safety constraints, execution-mode fallback, and cross-skill escalation.

## Scope

**Covers:** Handling tool failures, protecting data, and deciding when to hand off to another skill.

**Does NOT cover:** Persisting audit data or making unreviewed production changes.

## Error handling

| Situation | Response |
|---|---|
| API 400 — bad filter or conflict | "The query failed. This is likely a filter combination the API does not support. Check: filterByTag cannot be combined with actor or resource-type filters. Filter fields used: [list]." |
| API 401 / 403 — permission denied | "You don't have permission to access audit events for this environment. Check that your PingOne OAuth client has the `audit_reporting:read:activity` permission." |
| No events returned | "No events found matching your criteria. Verify the filter fields and time range, or widen the search window." |
| Rate limit hit | "The audit API rate limit has been reached. Please wait a moment before retrying." |
| `startDate` >= `endDate` | Stop before calling: "The start date must be earlier than the end date. Please provide a valid time range." |

---

## Constraints and guardrails

| Rule | Detail |
|---|---|
| Time range always enforced | Every `searchAuditActivities` call MUST include `startDate` and `endDate`. Never omit. |
| Default window when unspecified | Last 24 hours. Always inform the user of the default applied. |
| `filterByTag` is exclusive | Cannot be combined with actor, resource-type, or resource-population filters. If requested, ask the user to choose one or the other — never split into multiple queries silently. |
| Resource-type fields are exclusive | Only one of `filterByResourceType`, `filterByPopulationResource`, `filterByUserResource`, `filterByClientResource` may be used per call. |
| `filterByEventType` and `filterByResourceType` are exclusive | Cannot be used together in the same call. |
| Activity ID display | Always render full UUIDs — never truncate. Truncated IDs cannot be used with `getAuditActivity`. |
| No auto cross-environment queries | Operate on one environment at a time. If the user asks for a cross-environment query, respond: "Cross-environment queries are not supported — please specify one environment at a time." |
| Full JSON for getAuditActivity | Show the full response — never summarise, omit, rename, or restructure fields. Pretty-printing (whitespace only) is fine. |
| Pagination — user-driven | Do not auto-paginate beyond the first page. Prompt the user to continue. |
| Results order default | `timestamp` descending unless the use case requires chronological order (correlation ID trace). |
| PII handling | Audit output contains PII (usernames, email addresses). Do not persist beyond the current session. |
| No raw SCIM construction | Never build or pass a raw SCIM filter string to `searchAuditActivities`. The tool takes discrete fields only. |

---

## MCP execution

Tool-use order: MCP (check tool list) → Ping CLI (`which pingcli`) → general guidance. If MCP tools are unavailable or unconfigured, refer to [https://developer.pingidentity.com/build-with-ai/llms.txt](https://developer.pingidentity.com/build-with-ai/llms.txt) for setup options.

## Cross-skill escalation

| If the investigation reveals... | How to escalate |
|---|---|
| Environment BOM contains a DaVinci suite entry | After the audit result, hint the user that DaVinci flow-execution tracing is available for this environment; audit-event correlation and confirmation are not required. |
| User explicitly reports a DaVinci flow execution failure (node-level trace needed) | Hand off to the workflow that traces, debugs, and explains DaVinci flow execution failures — it reconstructs the execution timeline, correlates subflows, and returns root cause and remediation. The BOM check is not needed for an explicit request. |
| Environment or role configuration gap | Hand off to the workflow that owns platform setup, administration, and core configuration — environments, applications, directories, and policies. |
| Risk or MFA policy needing adjustment | Hand off to the workflow that configures and invokes the shared identity services — Protect, Verify, Credentials, IGA, Authorize, and MFA policies. |
