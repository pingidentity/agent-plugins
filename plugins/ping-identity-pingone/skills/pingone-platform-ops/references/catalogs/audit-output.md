---
title: "Audit Output"
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
# PingOne audit output

Covers the event table, pattern summary, structured result contract, and pre-emit checks.

## Scope

**Covers:** Rendering complete, chronological, evidence-backed audit results.

**Does NOT cover:** Changing tenant configuration or replacing the required tool workflow.

## Prerequisites

Retain the query, result pages, detail records, and any evidence gaps before rendering.

## Phase 4 — Output synthesis

### 4a — Primary results table

Render results as a markdown table. Default sort: `timestamp` descending (most recent first), except for correlation ID traces which sort ascending (chronological).

**Required columns — never omit** (the fields the platform exposes on a result):

| Column | Source field | Constraint |
|---|---|---|
| # | Row number | Sequential from 1, do not reset across pages |
| Timestamp (UTC) | `timestamp` | ISO 8601 format — never truncate |
| Description | `description` | As returned |
| Client | `client` | As returned; may be `-` or null |
| User Identity | `userIdentity` | As returned; may be `-` or null |
| Population | `population` | As returned; may be `-` or null when not exposed |
| Resource Type | `resourceType` | As returned; may be `-` or null when not exposed |

The `searchAuditActivities` response shapes each activity as `{ id, timestamp, eventType, description, client, userIdentity }`; Population and Resource Type are possible result fields that may not appear in every shaped summary — when absent, populate them per event with `getAuditActivity` from `actors`/`resources` (e.g. `resources[].type`, `resources[].population.id`). Do not invent or derive display columns the platform does not provide (e.g. a separate "Result" column) — success/failure is surfaced in the pattern summary from event types and descriptions. Call `getAuditActivity` on specific events for the raw full record; it carries the activity `id` used for follow-up lookups, always rendered as a full UUID.

### 4b — Pattern summary

After the table, always include a brief pattern summary:

- Total events returned (and running total if paginated)
- Failure/success breakdown where discernible from event types and descriptions
- Most frequent event type(s) in the result set
- Most frequent actor(s) if multiple actors are present
- For auth failure investigations: note the time distribution (burst vs. spread)

### 4c — Output contract

```yaml
status: success | partial | not_found | error
query:
  environmentId: string
  startDate: ISO-8601
  endDate: ISO-8601
  filtersApplied:         # list the discrete fields that were passed
    - field: string
      value: string
  limit: number
  cursor: string | null

results:
  totalReturned: number
  hasMore: boolean
  nextCursor: string | null
  events:
    - id: string                  # Full UUID — use with getAuditActivity
      timestamp: ISO-8601
      eventType: string
      description: string
      client: string | null
      userIdentity: string | null
      population: string | null
      resourceType: string | null

summary:
  totalEvents: number
  topEventTypes: [string]
  topActors: [string]
  patternNote: string | null

diagnostics:
  paginationHandled: boolean
  fullDetailFetched: boolean      # true if getAuditActivity was called
  warnings: [string]
  davinciEscalation:
    available: boolean | null     # true/false if probe ran (signals detected); null if no signals found (probe skipped)
    signalsDetected: boolean      # retained for compatibility; no longer gates the hint
    offered: boolean              # true when the BOM confirms DaVinci and the hint is shown
    accepted: boolean | null      # null because the hint does not require confirmation
    bomChecked: boolean           # true when the environment BOM query completed
    transactionIds: [string]      # populated only when supplied by the user or audit detail
    interactionIds: [string]      # populated only when supplied by the user or audit detail
```

### 4d — Pre-emit checklist

| Check | Required |
|---|---|
| `startDate` and `endDate` present in every `searchAuditActivities` call | MUST pass |
| No conflicting filter fields passed together (see `../playbooks/audit-investigation.md`) | MUST pass |
| All Activity IDs shown (table, contract, or detail) are full UUIDs — not truncated | MUST pass |
| Table includes all required columns | MUST pass |
| Pattern summary is present | MUST pass |
| Pagination state communicated if `hasMore: true` | MUST pass |
| Full JSON shown for `getAuditActivity` calls — every field present, pretty-printing allowed | MUST pass |
| The environment BOM was checked before a DaVinci hint was emitted | MUST pass |
| If the BOM contains DaVinci, `davinciEscalation.available: true` and `offered: true` are set | MUST pass |
| `davinciEscalation.accepted` remains null because the BOM-based hint needs no confirmation | MUST pass |

---
