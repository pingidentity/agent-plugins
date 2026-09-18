---
title: "Audit Scenarios"
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
# PingOne audit scenarios

Map common audit intents to the discrete filters supported by `searchAuditActivities`. Apply environment, identifier, time-window, execution, output, and guardrail rules from the other owned references; this file does not repeat those procedures.

## Scenario map

| User intent | Required resolution | Audit filters | Result handling |
|---|---|---|---|
| Failed authentication for a username or email | Resolve email to username with `listUsers`; use a plain username directly | `filterByActorUserName`; `filterByEventType: ["AUTHENTICATION.CREATED", "AUTHENTICATION.UPDATED"]` | Descending timestamp; summarize failure indicators and burst vs. spread |
| PingOne correlation chain | Preserve the supplied PingOne correlation ID; do not treat a DaVinci transaction ID as equivalent | `filterByCorrelationId` | Ascending timestamp; retrieve full detail if the summary lacks correlation data |
| Administrative actions | No identity or resource resolution unless the user chooses a different query | `filterByTag: "adminIdentityEvent"` alone | Summarize top admin actors and action types |
| Events on a user resource | Resolve a supplied name if needed; distinguish the resource itself from its population | `filterByUserResource` | Summarize event-type distribution |
| Events on an application resource | Resolve an application name with `listApplications` when needed | `filterByClientResource` | Summarize event types and affected actors |
| Resources inside a population | Resolve the population with `listPopulations` | `filterByResourceBelongingToPopulation`; optionally exact password event types | Summarize matching resource and actor activity |
| Population lifecycle changes | Resolve the population with `listPopulations` | `filterByPopulationResource` | Report changes to the population itself |
| Client application activity | Resolve the application with `listApplications` | `filterByActorClientId` | Summarize event types and success/failure where discernible |
| Password events | No identifier resolution unless the user adds one | `filterByEventType: ["PASSWORD.RESET", "PASSWORD.SET", "PASSWORD.RECOVERY", "PASSWORD.CHECK_FAILED"]` | Summarize actor type and failure rate |
| MFA or device events | Map the request to exact enum values; never use prefix matching | `filterByEventType` with the requested device/MFA enum values | Summarize event types and success/failure where discernible |

## Query-specific notes

### Failed authentication

For `"Show me all failed login attempts for john.doe in the last 7 days"`, resolve the seven-day window and use `filterByActorUserName: "john.doe"` plus the authentication event types. For an email, resolve the username first; do not fabricate a user ID or use an untyped event prefix.

### Correlation IDs

`filterByCorrelationId` searches the PingOne request correlation ID. A DaVinci `transactionId` belongs to the DaVinci execution skill and must be investigated there rather than passed to this filter.

### Populations

Use `filterByPopulationResource` only when the population itself was targeted, such as renamed or deleted. Use `filterByResourceBelongingToPopulation` when the requested events concern users, applications, or other resources inside that population.

### Administrative tag

`filterByTag: "adminIdentityEvent"` is a standalone administrative query. If a request combines it with an actor or resource constraint, stop and apply the conflict rule in `../catalogs/audit-guardrails.md` rather than splitting the request into misleading queries.
