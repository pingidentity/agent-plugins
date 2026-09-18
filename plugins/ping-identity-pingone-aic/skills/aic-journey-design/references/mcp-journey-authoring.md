# MCP Journey Authoring

Gotchas for creating and updating AIC journeys through the AIC MCP tools (`createJourney`, `updateJourneyNode`). Read this before authoring journeys through MCP; the composition invariants are the same regardless of whether the journey is created through MCP, the admin console, or the API.

## Scope

**Covers:** The createJourney PageNode child-node constraint and related MCP authoring gotchas.
**Does NOT cover:** General node configuration — see `nodes/`.

---

## createJourney — PageNode child node constraint

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

## Source

[Authentication node reference](https://docs.pingidentity.com/auth-node-ref/latest/overview.html)
