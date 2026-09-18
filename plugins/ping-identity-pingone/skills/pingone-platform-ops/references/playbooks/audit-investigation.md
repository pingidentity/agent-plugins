---
title: "Audit Investigation"
product_family: pingone-mt
products: ["pingone"]
capabilities: ["validation"]
services: []
audience: ["admin", "operator", "developer"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: false
last_updated: "2026-08-26"
slug: ""
---
# PingOne audit investigation

Prepare a bounded PingOne audit query using the available environment, identity, time, resource, and event data.

## Scope

**Covers:** Environment resolution, identifier handling, time windows, and typed audit query construction.

**Does NOT cover:** DaVinci node-level execution tracing.

## Tool pre-flight

Confirm these mandatory tools before retrieval:

| Tool | Requirement |
|---|---|
| `listEnvironments` | Resolve or verify the environment |
| `searchAuditActivities` | Search typed audit filters |
| `getAuditActivity` | Retrieve full event detail when needed |

Use `listUsers`, `listApplications`, and `listPopulations` only when the supplied actor, client, or population requires resolution. Treat unavailable tools as evidence gaps and stop before an incomplete query.

## Input validation

Require one environment context and at least one filter criterion or query intent. If the environment is absent, ask for an environment ID or resolvable name. If filters are absent, ask for an actor, resource, event type, correlation ID, or explicit query intent. Operate on one environment at a time.

Resolve a named environment with `listEnvironments`; present multiple matches for confirmation. Carry the resolved `environmentId` into every subsequent call.

## Identifier resolution

| Input | Resolution | Audit field |
|---|---|---|
| Plain username | Use directly when no lookup is needed | `filterByActorUserName` |
| Email address | Resolve with `listUsers`; prefer the returned username | `filterByActorUserName` |
| Application name | Resolve with `listApplications`; select the client or resource ID based on intent | `filterByActorClientId` or `filterByClientResource` |
| Population name | Resolve with `listPopulations`; distinguish population target from members | `filterByPopulationResource` or `filterByResourceBelongingToPopulation` |
| PingOne correlation ID | Preserve exactly | `filterByCorrelationId` |

Present multiple identifier matches for confirmation. Do not derive an environment from an opaque transaction or correlation value.

## Time-window rules

Every `searchAuditActivities` call includes explicit `startDate` and `endDate`:

| User expression | Resolve to |
|---|---|
| Explicit date/time | ISO 8601 UTC, without widening the requested range |
| `last N days` | `now - N days` through `now` |
| `yesterday` | Previous calendar day, 00:00:00 through 23:59:59 UTC |
| `this week` | Most recent Monday through `now` |
| `last week` | Previous Monday through Sunday 23:59:59 UTC |
| `this month` | First day of the current month through `now` |
| No range | Last 24 hours, stated before querying |
| Approximate time | Expand by ±15 minutes and state the expansion |

Reject an inverted or unsupported range before calling the API.

## Typed filter selection

Use discrete filter fields exposed by `searchAuditActivities`; never construct a raw SCIM string. Apply only fields relevant to the intent:

| Intent | Field |
|---|---|
| Actor user UUID or username | `filterByActorUserId` or `filterByActorUserName` (one only) |
| Actor OAuth client | `filterByActorClientId` |
| Exact event types | `filterByEventType` with enum values; no prefix matching |
| Resource type | `filterByResourceType` |
| Event targets a population, user, or application | `filterByPopulationResource`, `filterByUserResource`, or `filterByClientResource` |
| Any specific resource | `filterByResourceId` |
| Resources inside a population | `filterByResourceBelongingToPopulation` |
| PingOne request chain | `filterByCorrelationId` |
| Administrative identity events | `filterByTag: "adminIdentityEvent"` |

`filterByTag` is exclusive with actor, resource, and population filters. Resource-type fields are mutually exclusive. `filterByEventType` and `filterByResourceType` are mutually exclusive. Do not silently split an unsupported combination into separate queries.
