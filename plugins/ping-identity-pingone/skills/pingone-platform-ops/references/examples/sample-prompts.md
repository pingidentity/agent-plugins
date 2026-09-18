---
title: "Sample Prompts"
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
# Sample prompts — pingone-platform-ops

Covers synthetic acceptance prompts for audit routing and output behavior.

## Scope

**Covers:** Testing discrete filter selection, time windows, pagination, and escalation boundaries.

**Does NOT cover:** Live tenant data or DaVinci node-level diagnosis.

## How to read each entry

| Field | Description |
|---|---|
| **Prompt** | The exact text to submit to the agent |
| **Scenario** | Which use case playbook this exercises |
| **ACs exercised** | Acceptance criteria this prompt covers |
| **Minimum bar** | What the output MUST contain |
| **Edge cases** | What to watch for |
| **Captured baseline** | Result once run against a live environment |

---

### Prompt 1 — Failed logins by username + 7-day window

> "Show me all failed login attempts for john.doe in the last 7 days"

**Scenario:** Auth failure investigation
**ACs exercised:** Time range enforced, actor filter resolution, event type filter, structured table, pattern summary

**Minimum bar:**
- Time range resolved: `now - 7 days` → `now` (stated to user before querying)
- `listUsers` called to resolve `john.doe` → `userId`
- `searchAuditActivities` called with `filterByActorUserId: "<userId>"` and `filterByEventType: ["AUTHENTICATION.CREATED", "AUTHENTICATION.UPDATED"]`
- No raw SCIM filter string constructed or passed
- Results table with all required columns; Activity IDs are full UUIDs
- Pattern summary: event count, failure indicators from descriptions, time distribution

**Edge cases:**
- Username not found → "No PingOne user found for username john.doe. Verify the username or provide an email address."
- No auth events in window → "No authentication events found for john.doe in the last 7 days."
- More than 100 results → pagination prompt shown; first page rendered with running total

**Captured baseline:** ☐

---

### Prompt 2 — Correlation ID trace

> "What happened during correlation ID abc-123-xyz?"

**Scenario:** Correlation chain
**ACs exercised:** Correlation ID filter, time range default (24h), chronological sort, full request chain

**Minimum bar:**
- Default 24-hour window applied and stated to user
- `searchAuditActivities` called with `filterByCorrelationId: "abc-123-xyz"`
- Results sorted ascending by `timestamp` (chronological — not the default descending)
- Summary describes the full request chain from first to last event
- If correlationId not visible in summary fields, `getAuditActivity` called on relevant events

**Edge cases:**
- No events found → "No audit events found for correlation ID abc-123-xyz in the last 24 hours. Try widening the time range."
- Single event found → noted in summary: "Correlation chain contains only one event in this window."

**Captured baseline:** ☐

---

### Prompt 3 — Admin actions last week

> "What admin actions were taken in this environment last week?"

**Scenario:** Admin audit
**ACs exercised:** `filterByTag: "adminIdentityEvent"`, natural language date resolution ("last week"), tag exclusivity rule

**Minimum bar:**
- Time range resolved: previous Monday 00:00:00 UTC → previous Sunday 23:59:59 UTC (stated to user)
- `searchAuditActivities` called with `filterByTag: "adminIdentityEvent"` and NO other filters
- Results table with required columns
- Pattern summary: top admin actors, most frequent action types

**Edge cases:**
- User asks "admin events for user X last week" → skill must inform user that `filterByTag` cannot be combined with actor filters and ask them to choose one or the other — must NOT split into two queries silently
- No admin events in window → "No admin events found for last week."

**Captured baseline:** ☐

---

### Prompt 4 — Events on a specific application this month

> "Show me errors related to application ID app-456 this month"

**Scenario:** Application audit
**ACs exercised:** `filterByClientResource`, "this month" resolution

**Minimum bar:**
- Time range resolved: first day of current month 00:00:00 UTC → now (stated to user)
- `searchAuditActivities` called with `filterByClientResource: "app-456"`
- Results table rendered
- Pattern summary: breakdown by `eventType`, most affected actors

**Edge cases:**
- "app-456" is a name not an ID → skill resolves via `listApplications` before constructing call
- Application UUID not found → API error surfaced with the field used

**Captured baseline:** ☐

---

### Prompt 5 — Population-scoped password resets

> "Were there any password resets in the Employees population this week?"

**Scenario:** Population-scoped audit
**ACs exercised:** `filterByResourceBelongingToPopulation` (not `filterByPopulationResource`), population name resolution, event type array, "this week" resolution

**Minimum bar:**
- `listPopulations` called to resolve "Employees" → `populationId`
- Time range resolved: most recent Monday 00:00:00 UTC → now (stated to user)
- `searchAuditActivities` called with `filterByResourceBelongingToPopulation: "<populationId>"` and `filterByEventType: ["PASSWORD.RESET", "PASSWORD.SET", "PASSWORD.CHECK_FAILED"]`
- Skill does NOT use `filterByPopulationResource` (that is for events on the population itself)
- Results table rendered
- Pattern summary: count of resets, actor breakdown

**Edge cases:**
- Population name not found → "No population named 'Employees' found. Available populations: [list]. Which one did you mean?"
- No password resets in window → "No password reset events found for the Employees population this week."

**Captured baseline:** ☐

---

### Prompt 6 — Client application activity yesterday

> "What did the mobile app client do yesterday?"

**Scenario:** Client audit
**ACs exercised:** Client ID resolution via `listApplications`, "yesterday" resolution, `filterByActorClientId`

**Minimum bar:**
- `listApplications` called to resolve "mobile app" → `clientId`
- Time range resolved: previous calendar day 00:00:00 UTC → 23:59:59 UTC (stated to user)
- `searchAuditActivities` called with `filterByActorClientId: "<clientId>"`
- Results table rendered
- Pattern summary: event type breakdown, success/failure ratio

**Edge cases:**
- Multiple applications match "mobile app" → list presented; user asked to confirm
- No events yesterday → "No audit events found for the mobile app client yesterday."

**Captured baseline:** ☐

---

### Prompt 7 — Password event sweep, 3 days

> "Show me all password reset events in the last 3 days"

**Scenario:** Password event audit
**ACs exercised:** `filterByEventType` array, 3-day window

**Minimum bar:**
- Time range: now - 3 days → now (stated to user)
- `searchAuditActivities` called with `filterByEventType: ["PASSWORD.RESET", "PASSWORD.SET", "PASSWORD.RECOVERY", "PASSWORD.CHECK_FAILED"]`
- Results table rendered; Activity IDs are full UUIDs
- Pattern summary: success/failure breakdown, top actors

**Edge cases:**
- Skill must NOT use SCIM prefix matching (`sw "PASSWORD"`) — tool does not support it; use typed event type array
- No password events → "No password events found in the last 3 days."

**Captured baseline:** ☐

---

### Prompt 8 — filterByTag + actor conflict

> "Show me admin events for user john.doe last week"

**Scenario:** filterByTag mutual exclusion enforcement
**ACs exercised:** Conflict rule — `filterByTag` cannot be combined with actor filters

**Minimum bar:**
- Skill does NOT call `searchAuditActivities`
- Response: "The PingOne audit API does not support combining the `adminIdentityEvent` tag filter with actor filters. Please choose one: filter by admin tag only, or filter by the specific actor (john.doe) only."
- Skill does NOT split into two separate queries silently

**Edge cases:**
- User explicitly asks to split → still inform them the API does not support the combination and that splitting would give misleading results (one query shows all admin events, the other shows all events for that actor — neither is "admin events for that actor")

**Captured baseline:** ☐

---

### Prompt 9 — No time range specified (default 24h)

> "Show me all failed authentication events"

**Scenario:** Default window enforcement
**ACs exercised:** Default 24-hour window, informing the user of the default

**Minimum bar:**
- Skill informs user: "No time range was specified — defaulting to the last 24 hours. Specify a different range if needed."
- `searchAuditActivities` called with `filterByEventType: ["AUTHENTICATION.CREATED", "AUTHENTICATION.UPDATED"]`
- Default window stated before results

**Edge cases:**
- No events in last 24 hours → "No authentication events found in the last 24 hours. Specify a time range if you need to look further back."

**Captured baseline:** ☐

---

### Prompt 10 — Paginated result set + "show more"

> "Show me all admin events this week" (against an environment with 200+ admin events)

**Scenario:** Pagination handling
**ACs exercised:** Pagination prompt, user-driven continuation, running total display, `nextCursor` usage

**Minimum bar:**
- First page rendered (up to 100 events)
- Message: "There are more results available. Showing page 1 of results (100 events so far). Say 'show more' or 'next page' to continue."
- On "show more": `searchAuditActivities` called again with same filters + `cursor: "<nextCursor>"`
- Running total updated: "Showing 200 events total."
- When last page: "All results retrieved — [N] total events."

**Edge cases:**
- User says "show all" at once → skill explains pagination policy and prompts confirmation before retrieving multiple pages
- Cursor expires between pages → surface API error and offer to restart the query

**Captured baseline:** ☐

---

### Prompt 11 — filterByPopulationResource vs filterByResourceBelongingToPopulation distinction

> "Was the Employees population renamed or deleted recently?"

**Scenario:** Population lifecycle audit
**ACs exercised:** `filterByPopulationResource` (not `filterByResourceBelongingToPopulation`)

**Minimum bar:**
- `listPopulations` called to resolve "Employees" → `populationId`
- `searchAuditActivities` called with `filterByPopulationResource: "<populationId>"`
- Skill does NOT use `filterByResourceBelongingToPopulation` (that is for resources inside the population)
- Results table rendered

**Edge cases:**
- Skill correctly distinguishes the two fields when the user's intent is ambiguous — if unclear, ask: "Are you looking for events that affected the population itself (e.g. it was renamed or deleted), or events for users and resources that belong to that population?"

**Captured baseline:** ☐

---

## Baseline run tracking

| Prompt | Baseline run | Notes |
|---|---|---|
| 1 — Failed logins by username | ☐ | |
| 2 — Correlation ID trace | ☐ | |
| 3 — Admin actions last week | ☐ | |
| 4 — Application events this month | ☐ | |
| 5 — Population password resets | ☐ | |
| 6 — Client activity yesterday | ☐ | |
| 7 — Password event sweep | ☐ | |
| 8 — filterByTag + actor conflict | ☐ | |
| 9 — Default 24h window | ☐ | |
| 10 — Pagination + "show more" | ☐ | |
| 11 — Population resource vs belonging-to | ☐ | |
