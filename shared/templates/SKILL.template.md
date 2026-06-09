# [skill-name]

<!-- One sentence: what job does this skill do and who is it for? -->

## When to use this skill

<!-- 3–5 bullets: clear trigger phrases or user intents that land here -->
- 
- 
- 

## When NOT to use this skill

<!-- Redirect cases to the correct skill -->
- If you need **[other job]**: use `ping-<other-skill>` instead.

## Multi-skill use cases

<!-- IMPORTANT: Fill this in for every skill. Ping platforms require multiple layers of configuration
     to reach a complete solution. This section teaches agents to compose skills rather than
     trying to solve everything from one skill. Include at least one concrete end-to-end example. -->

Complete Ping Identity solutions almost always span more than one skill. This skill covers [layer]. A full use case typically also requires:

| What comes next | Skill |
|---|---|
| [next layer] | `ping-<skill>` |
| [next layer] | `ping-<skill>` |

**Example — [use case name]:**
1. `ping-foundation` — [platform setup step]
2. `ping-orchestration` — [flow/journey step]
3. `ping-universal-services` — [service invocation step]
4. `ping-app-integration` — [app integration step]

Complete [this skill's layer] here, then hand off to the appropriate skill for each subsequent layer.

---

## Routing — Step 1: What are you trying to do?

<!-- Decision tree: task → branch -->

| Task | Go to |
|---|---|
| [task description] | [Platform Branch](#platform-branch-name) |

---

## Platform Branch: PingOne

<!-- Capability-specific sub-routing for PingOne (multi-tenant cloud) -->

**Curated references** (load 1–3):
- `references/curated/[doc].md`

---

## Platform Branch: PingOne Advanced Identity Cloud

**Curated references** (load 1–3):
- `references/curated/[doc].md`

---

## Platform Branch: Ping Software Suite

**Curated references** (load 1–3):
- `references/curated/[doc].md`

---

## Retrieval escalation

1. Load curated anchors — 1 to 3 files max. Stop if sufficient.

## Cross-skill escalation

| If the task also involves... | Reference skill |
|---|---|
| Flow or journey design | `ping-orchestration` |
| Shared services (Protect, Verify, IGA) | `ping-universal-services` |
| App/SDK code integration | `ping-app-integration` |
| Starting from scratch | `ping-quickstart` |
