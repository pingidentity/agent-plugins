---
title: "PingOne Advanced Identity Cloud (AIC) — Node Fundamentals"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: []
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: reference
status: current
canonical: true
last_updated: "2026-06-05"
slug: "https://docs.pingidentity.com/auth-node-ref/latest/overview.html"
---

# AIC — Node Fundamentals

Tribal knowledge and non-obvious invariants about how nodes behave in AIC journeys. Rules here are validated from live AIC sessions — they are not documented clearly in official docs and are common sources of bugs.

## Scope

**Covers:** Node composition rules, PageNode usage, child node requirements, outcome wiring, and known gotchas.
**Does NOT cover:** Individual node reference — see the specific node files (e.g., `basic-auth-nodes.md`, `mfa-nodes.md`, `utility-nodes.md`).

---

## PageNode rules

### PageNode is never used alone

A PageNode without child nodes renders as an empty page ("Drag nodes here") — no inputs, no outcomes, no way for the user to proceed. PageNodes only work when child nodes are declared inside `config.nodes`.

This is the most common PageNode bug in `createJourney` calls: the PageNode is created but its children are omitted or passed as an empty array.

### Child nodes must be declared in `config.nodes`

When building a journey via the API or `createJourney`, child nodes of a PageNode must be listed in the `config.nodes` array. Each entry requires at minimum:

```json
{"nodeType": "<NodeType>", "displayName": "<label>"}
```

If `config.nodes` is absent or empty, the page has no content.

### Outcomes come from the child decision node, not the PageNode

The PageNode itself has no outcome logic. Its branch outcomes (e.g. `true`/`false`, `outcome`) are determined by whichever child node produces them — typically the last decision-type node in the children list.

### Nodes that must always live inside a PageNode

These nodes render no UI and provide no outcomes when placed as standalone nodes in the journey graph:

| Node | Why it must be a PageNode child |
|---|---|
| `ValidatedUsernameNode` | Renders the username input field only inside a Page |
| `ValidatedPasswordNode` | Renders the password input field only inside a Page |
| `OneTimePasswordCollectorDecisionNode` | Renders the OTP input and drives `true`/`false` only inside a Page |
| `AttributeCollectorNode` | Renders profile attribute fields only inside a Page |

---

## Login page pattern — username + password

Never split username and password across two separate PageNodes unless multi-step login is explicitly requested. The correct default:

```
PageNode
  ├── ValidatedUsernameNode  (child)
  └── ValidatedPasswordNode  (child)
      → outcome → DataStoreDecisionNode
```

Splitting them into two PageNodes creates two separate screens and two round-trips, which is not the default login UX.

---

## OTP collection pattern

The `OneTimePasswordCollectorDecisionNode` must always be a child of a PageNode:

```json
"config": {
  "nodes": [
    {
      "nodeType": "OneTimePasswordCollectorDecisionNode",
      "displayName": "OTP Collector Decision"
    }
  ],
  "pageHeader": {"en": "One Time Passcode Required"},
  "pageDescription": {"en": "Please check your email and enter your passcode"}
}
```

The `true`/`false` outcomes on the PageNode come from the embedded `OneTimePasswordCollectorDecisionNode`.

---

## Prerequisites

- PingOne AIC or PingAM tenant with at least one journey configured.
- Journey creation via the admin console or API with a valid realm.

## Common variants

- **AIC:** same node model; add ESV-backed scripts and hosted-page theme configuration.
- **PingAM:** same node model; realm config and redirect trust configuration required separately.

---

## MCP createJourney — PageNode child node constraint

The `createJourney` MCP tool transforms top-level node keys (e.g. `"reg-page"`) into UUIDs via `nodeIdMapping`. It does **not** transform `config.nodes[].\_id` values inside a PageNode's config. Passing human-readable strings there causes a **500 Internal Server Error with no response body**.

**Correct two-step pattern:**

1. Define all child nodes as top-level nodes with `connections: {}` in the `createJourney` call. They are assigned UUIDs via `nodeIdMapping` but are "orphan" nodes — not reachable via the graph. This is expected; the PageNode owns their routing.
2. After journey creation, call `updateJourneyNode` on the PageNode UUID, setting `config.nodes` with the real UUIDs from step 1.

```json
// Step 1 — createJourney: child nodes as top-level with empty connections
"reg-username": { "nodeType": "ValidatedUsernameNode", "connections": {}, "config": { ... } }
"reg-page":     { "nodeType": "PageNode", "connections": { "outcome": "next-node" }, "config": { "nodes": [] } }

// Step 2 — updateJourneyNode on the PageNode UUID
{
  "nodes": [
    { "_id": "<uuid-from-mapping>", "nodeType": "ValidatedUsernameNode", "displayName": "..." }
  ]
}
```

A PageNode with `nodes: []` creates successfully and can be populated immediately after with `updateJourneyNode`. Do not attempt to pass child node UUIDs in the initial `createJourney` call.

**Note:** A "failure" PageNode (a node whose sole purpose is to show an error) must **not** have any connections — route directly to the `failure` terminal node instead. Self-connections produce a "Node outcome cannot connect to itself" error.

---

## Related references

- `nodes/utility-nodes.md` — PageNode configuration details
- `nodes/mfa-nodes.md` — OTP Email Sender, OTP Collector Decision
- `nodes/basic-auth-nodes.md` — ValidatedUsernameNode, ValidatedPasswordNode
- `nodes/identity-management-nodes.md` — AttributeCollectorNode

## Source

[Authentication node reference](https://docs.pingidentity.com/auth-node-ref/latest/overview.html)
[Page node](https://docs.pingidentity.com/auth-node-ref/latest/page.html)
