---
title: "PingOne Advanced Identity Cloud (AIC) — Progressive Profiling"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: []
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/auth-node-ref/latest/overview.html"
---

# AIC — Progressive Profiling

Design patterns for progressively collecting user profile data after login, without blocking authentication. Derived from the OOTB progressive profiling journey template.

## Scope

**Covers:** `LoginCountDecisionNode` trigger configuration, `QueryFilterDecisionNode` SCIM filter syntax, dual-gate pattern, `IncrementLoginCountNode` placement, `PatchObjectNode` for preference updates.
**Does NOT cover:** Registration-time attribute collection — see `nodes/identity-management-nodes.md`. Full profile management — see `journey-use-cases/social-and-local-registration-authentication.md`.

---

## Pattern: Dual-Gate Progressive Profiling

Progressive profiling should only prompt when two conditions are both true:
1. The user is at the right point in their lifecycle (e.g., 2nd login)
2. The data is actually missing

```
LoginCountDecisionNode (interval: AT, amount: 2)
  → true → QueryFilterDecisionNode (filter: attribute missing or incomplete)
                → true → PageNode (collect missing attributes)
                        → PatchObjectNode → SuccessNode
                → false → SuccessNode (data already present — skip)
  → false → SuccessNode (wrong login count — skip)
```

This pattern ensures users are never re-prompted once they have provided the data, and are not interrupted on every login.

---

## LoginCountDecisionNode Configuration

| Field | Value | Notes |
|---|---|---|
| `interval` | `AT` or `EVERY` | `AT`: trigger exactly at count N (one-time). `EVERY`: trigger at count N and every login after. |
| `amount` | `2` (OOTB) | Any positive integer |
| `identityAttribute` | `userName` | IDM attribute used to retrieve the user object |

- Outcomes: **True** (count matches) / **False** (count does not match)
- `AT` is preferred for one-time prompts — prevents the prompt from firing on every login after count N

---

## QueryFilterDecisionNode — SCIM Filter Syntax

Evaluates a SCIM/LDAP-style filter against the user's profile attributes to determine if data is missing.

**OOTB filter for preferences:**
```
!(/preferences pr) or /preferences/marketing eq false or /preferences/updates eq false
```

This matches users who:
- Have no `preferences` attribute at all (`!(/preferences pr)`)
- OR have `preferences/marketing` set to `false` (i.e., not yet opted in)
- OR have `preferences/updates` set to `false`

**Outcomes:** **True** (filter matches — data missing or incomplete) / **False** (filter does not match — data present)

**Dot-path notation for nested attributes:** Use `/` as the path separator for nested attributes: `/preferences/marketing`, `/preferences/updates`.

---

## AttributeCollectorNode for Nested Attributes

When collecting nested attributes, use dot-path notation in `attributesToCollect`:

```json
"attributesToCollect": ["preferences/updates", "preferences/marketing"]
```

The attribute must be defined in the identity schema before it can be collected. `required: false` allows users to skip optional fields.

---

## PatchObjectNode for Preference Updates

```
PatchObjectNode
  identityResource: managed/alpha_user
  patchAsObject: false
  ignoredFields: []
```

- Outcomes: **PATCHED** / **FAILURE**
- `patchAsObject: false` merges only the specified attributes — does not overwrite the entire user object
- `FAILURE`: route to FailureNode (or silently log and continue, depending on data criticality)

---

## IncrementLoginCountNode Placement

**Critical:** Place `IncrementLoginCountNode` immediately after `CreateObjectNode(CREATED)` in the registration journey so the login count starts at 1 after registration.

```
CreateObjectNode → CREATED → IncrementLoginCountNode → SuccessNode
```

Without this, the count is 0 after registration. `LoginCountDecisionNode(AT=2)` will then fire on the 3rd visit (2nd login), not the 2nd.

---

## Inner Journey Pattern

Progressive profiling should be an **inner journey** called from the main sign-in journey:

```
Main Sign-In journey (after authentication success)
  → InnerTreeEvaluatorNode (tree: Progressive Profiling)
      → true → SuccessNode
      → false → FailureNode (rare — only if PatchObjectNode fails)
```

Keeping it separate allows profiling to be updated independently and disabled without modifying the login journey.

---

## Common variants

| Variant | Notes |
|---|---|
| Trigger once, any login after N | Use `interval: EVERY` instead of `AT` |
| Trigger at multiple lifecycle points | Use multiple `LoginCountDecisionNode` instances with different amounts and different `QueryFilterDecisionNode` filters |
| Require mandatory data before access | Route `QueryFilterDecisionNode(true)` to collection before SuccessNode; remove the skip path |
| Collect a single attribute | Use a single-attribute `AttributeCollectorNode` in the PageNode |

## Prerequisites

- `IncrementLoginCountNode` placed in the registration journey so login count is initialized
- Custom attributes (`preferences/marketing`, etc.) defined in the IDM managed object schema before collection
- `managed/alpha_user` with write access for `PatchObjectNode`

## Related references

- `nodes/identity-management-nodes.md`
- `nodes/utility-nodes.md`
- `journey-use-cases/social-and-local-registration-authentication.md`

## Source

[Authentication nodes — PingOne AIC](https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html)
