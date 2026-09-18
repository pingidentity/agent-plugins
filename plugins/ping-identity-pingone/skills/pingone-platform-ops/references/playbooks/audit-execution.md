---
title: "Audit Execution"
product_family: pingone-mt
products: ["pingone"]
capabilities: ["validation"]
services: []
audience: ["admin", "operator", "developer"]
use_cases: ["workforce", "customer"]
doc_type: reference
status: current
canonical: false
last_updated: "2026-09-03"
slug: ""
---
# PingOne audit execution

Covers typed audit calls, pagination, full-event retrieval, and evidence-first DaVinci signal handling.

## Scope

**Covers:** Executing a prepared audit query and handling result pages or full event details.

**Does NOT cover:** Designing flows or diagnosing DaVinci nodes without an explicit handoff.

## Prerequisites

Complete environment, identifier, time-window, and filter validation in `audit-investigation.md`.

## Phase 3 — Execution and pagination

### 3a — Call searchAuditActivities

```
searchAuditActivities(
  environmentId,
  startDate,       // ISO 8601 or date-only
  endDate,         // ISO 8601 or date-only
  [filterByActorUserId | filterByActorUserName],
  [filterByActorClientId],
  [filterByEventType],
  [filterByResourceType | filterByPopulationResource | filterByUserResource | filterByClientResource],
  [filterByResourceId],
  [filterByResourceBelongingToPopulation],
  [filterByCorrelationId],
  [filterByTag],
  limit,
  cursor
)
```

- Always pass resolved `startDate` and `endDate`.
- Only pass filter fields relevant to the query — omit all others.
- Never pass conflicting field combinations; apply the typed-filter conflict rules in `audit-investigation.md`.

### 3b — Pagination handling

The response includes `activities[]`, and optionally `nextCursor` and `prevCursor`.

If `nextCursor` is present:
1. Inform the user: "There are more results available. Showing page [N] of results ([count] events so far). Say 'show more' or 'next page' to continue."
2. Store the cursor — do not auto-paginate beyond the first page without user confirmation.
3. On "show more" / "next page": call `searchAuditActivities` again with the same filters and the stored `nextCursor`. Append results to the existing table.
4. Always display the running total: "Showing [N] events total."
5. When no `nextCursor` is returned: "All results retrieved — [N] total events."

### 3c — Fetch full event detail

Call `getAuditActivity(environmentId, activityId)` when:
- The user asks for full detail on a specific event.
- A summary result is missing fields needed for the investigation (e.g. `correlationId`, `internalCorrelation.transactionId`, `sessionId`, or `actors` detail — the `searchAuditActivities` response is a shaped summary; `getAuditActivity` returns the raw full record).
- The user asks to "show raw event data" or "show the payload".

**Display rule for `getAuditActivity`:** Always show the full JSON response with every field as returned — do not summarise, omit, rename, or restructure any fields. Whitespace-only reformatting (pretty-printing) is expected for readability.

### 3d — DaVinci BOM availability hint

Do not infer DaVinci availability from audit event types, actor names, transaction IDs, or interaction IDs. After the audit result is available, check the environment Bill of Materials (BOM) instead.

1. Query the environment BOM using the connected BOM capability after inspecting its schema. In Ping CLI/API mode, use `GET /pingone/platform/v1/environments/{envId}/billOfMaterials`.
2. Match the returned product or suite entries case-insensitively for `DaVinci`; preserve the exact returned entry as evidence. Do not invent a product identifier when the BOM uses a different name.
3. If the BOM contains a DaVinci suite entry, set `davinciAvailable: true` and hint:
   > "This environment's Bill of Materials includes DaVinci. For flow-execution tracing, use the flow-execution troubleshooting skill available in your session."
4. If the BOM does not contain a DaVinci entry, set `davinciAvailable: false` and do not suggest DaVinci troubleshooting.
5. If the BOM cannot be retrieved, set `davinciAvailable: null` and record the failed BOM operation as an evidence gap. Do not treat the failure as evidence that DaVinci is unavailable.

This BOM check is an entitlement check only. It does not require audit-event correlation or a confirmation prompt before offering the flow-execution troubleshooting skill. Keep PingOne `correlationId`, DaVinci `transactionId`, and `sessionId` distinct when a later DaVinci investigation is requested.

---
