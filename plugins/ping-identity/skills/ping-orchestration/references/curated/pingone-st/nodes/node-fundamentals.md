---
title: "PingOne ST — Node Fundamentals"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: []
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: reference
status: current
canonical: true
last_updated: "2026-05-19"
slug: "https://docs.pingidentity.com/auth-node-ref/latest/overview.html"
---

# PingOne ST — Node Fundamentals

Tribal knowledge and non-obvious invariants about how nodes behave in PingOne ST journeys. Rules here are validated from live AIC sessions — they are not documented clearly in official docs and are common sources of bugs.

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

## Related references

- `nodes/utility-nodes.md` — PageNode configuration details
- `nodes/mfa-nodes.md` — OTP Email Sender, OTP Collector Decision
- `nodes/basic-auth-nodes.md` — ValidatedUsernameNode, ValidatedPasswordNode
- `nodes/identity-management-nodes.md` — AttributeCollectorNode
