# Authoring Rules for Skill Reference Files

Rules for every `.md` file created in this repo. Apply these before writing any new reference or curated anchor.

---

## 0. Every `SKILL.md` must comply with the agentskills.io specification

Reference: https://agentskills.io/specification

### Required frontmatter fields

| Field | Constraint |
|---|---|
| `name` | 1–64 chars. Lowercase letters, numbers, hyphens only. No leading/trailing/consecutive hyphens. Must match the parent directory name. |
| `description` | 1–1024 chars. Describe what the skill does AND when to use it. Include keywords agents use to detect relevance. |

### Optional frontmatter fields

| Field | Use |
|---|---|
| `license` | License name or reference to a bundled LICENSE file |
| `compatibility` | Environment requirements (tools needed, platform scope, network access). Include only when relevant. |
| `metadata` | Arbitrary key-value map. Use for `publisher`, `version`, etc. |
| `allowed-tools` | Space-separated pre-approved tools. Experimental. |

### Minimal valid SKILL.md

```yaml
---
name: skill-name
description: What this skill does and when to use it.
---
```

### `name` must match directory name

The `name` field must exactly match the skill's parent directory name. A skill in `skills/ping-foundation/` must have `name: ping-foundation`.

### Description quality bar

A good description:
- States what the skill does (actions/capabilities)
- States when to use it (trigger phrases, user intents, task types)
- Includes keywords that help the agent pattern-match to the right skill
- Uses assertive language: "Use this skill whenever..." not "This skill can be used for..."

A poor description says only what the skill is, not when to invoke it. Agents tend to **undertrigger** skills — write descriptions that push them toward triggering, not away.

**From Anthropic's skill-creator guidance:** "The description should be deliberately assertive — use language like 'Make sure to use this skill whenever...' rather than passive phrasing, since models tend to undertrigger skills."

Reference: https://agentskills.io/spec/v0.2.0/

---

## 0b. SKILL.md authoring best practices (from Anthropic skill-creator)

### Writing style

- Use **imperative form** for instructions ("Load the curated anchor", not "The agent should load")
- Explain **why** things matter rather than imposing rigid rules — LLMs benefit from understanding reasoning
- Favor **theory of mind**: make skills general, not narrow to specific examples
- Reference files clearly with guidance on **when** to read them, not just what they are
- For large reference files (>300 lines), include a **table of contents** at the top

### Body length

Keep the main `SKILL.md` body under ~500 lines. Move detailed reference material to separate files in `references/`. The agent loads `SKILL.md` fully on activation — every line costs tokens.

### Progressive disclosure

Structure the skill so that:
1. **Metadata** (~100 tokens): `name` and `description` loaded at startup for all skills
2. **Instructions** (<5000 tokens): Full `SKILL.md` body loaded on activation
3. **Resources** (as needed): Files in `references/` loaded only when required

The goal is to serve the minimum sufficient context at each stage.

### Iteration discipline

Skills are products, not one-time files. Before publishing a skill:
1. Write at least 3 benchmark prompts that should trigger it
2. Write at least 2 prompts that should NOT trigger it
3. Verify routing decisions are correct using the eval format in `evals/routing-eval.md`
4. Update the description if undertriggering is observed

---

## 1. Every reference `.md` file must start with a frontmatter block

No exceptions. This drives automation (shortlist generation, branch placement, stale detection) and plugin-local routing.

```yaml
---
title: ""
product_family: ""        # pingone-mt | pingone-st | ping-software | cross-platform
products: []              # exact product names, e.g. ["pingfederate", "pingaccess"]
capabilities: []          # foundation | orchestration | universal-services | app-integration | identity-for-ai | quickstart
services: []              # universal services if applicable, e.g. ["protect", "verify"]
audience: []              # admin | developer | architect | operator
use_cases: []             # workforce | customer | cross-platform | ai-identity
doc_type: ""              # guide | reference | concept | tutorial | troubleshooting | architecture
status: current           # current | draft | deprecated
canonical: false          # true only if this is the single authoritative page for this task
last_updated: ""          # YYYY-MM-DD
slug: ""                  # canonical docs URL for this topic
---
```

### Required fields

`title`, `product_family`, `capabilities`, `doc_type`, `status` — CI will reject files missing these.

### `product_family` enum (pick one primary family)

| Value | Platform |
|---|---|
| `pingone-mt` | PingOne (multi-tenant cloud) |
| `pingone-st` | PingOne Advanced Identity Cloud (AIC) |
| `ping-software` | Ping Software Suite (on-premises) |
| `cross-platform` | Spans multiple platform families |

> **Naming note:** The `pingone-st` value is a stable internal routing tag and directory name — it denotes **PingOne Advanced Identity Cloud (AIC)**. Always call the platform "PingOne Advanced Identity Cloud (AIC)" or "AIC" in prose. Never surface "PingOne ST" or "single-tenant" as the product name in author-facing or agent-facing text.

Use `cross-platform` only when the content genuinely applies without modification to two or more platform families. If a doc has platform-specific sections, pick the primary family and note variants in the body.

---

## 1a. Editorial principles — accuracy, tone, and durability

Skills and MCP tool descriptions ride alongside the product and the official docs. They must not get ahead of shipped behaviour, and they must not editorialise about Ping's own products or documentation.

**Follow the product — do not jump ahead of it.** Only document behaviour that is shipped and documented. If a capability is not yet supported by the product or has no stable querying logic, do not invent it in a skill or MCP description. When in doubt, defer to the official docs.

**No statements that go stale.** Do not bake release timing, channel state, or version-promotion plans into reference prose. These rot between updates and mislead agents.

- ❌ "Available on the Rapid channel as of 2026-06-03; Regular channel promotion planned."
- ❌ "Not yet GA; this skill will cover it when available."
- ❌ "These will be introduced progressively from Q3 2026."
- ✅ State the capability, then link to the live release notes / docs for current availability: "Check the [AIC release notes](…) for current channel availability."

If availability genuinely gates usage, express it as a durable constraint plus a pointer to the authoritative source — not a dated promise.

**No negative framing about Ping docs or products.** Reference files describe capability and behaviour neutrally. Do not characterise the official docs or product as deficient, and do not position skill content as compensating for them.

- ❌ "Not documented clearly in official docs and a common source of bugs."
- ❌ "Tribal knowledge the docs don't cover."
- ✅ "Behavioural invariants validated against live sessions; complements the per-node reference docs."

The test: state what the content **is** and what it **enables**, not what the docs or product **lack**.

---

## 2. Curated anchors — how to write them

### Curated anchors (`references/curated/`)

- Written by a human; reviewed before merge
- Must be task-completing: a reader can finish a real task using this file alone
- `canonical: true`
- Body structure: **Scope** → **Key steps / content** → **Prerequisites** → **Common variants** → **Related references** → **Source**
- 150–400 lines max. If longer, split into two anchors.
- No duplicate content with other curated files in the same skill

---

## 3. Platform branch belongs in the directory path AND the frontmatter

For platform-scoped curated anchors, the directory path and `product_family` must agree:

| Directory | `product_family` |
|---|---|
| `references/curated/pingone-mt/` | `pingone-mt` |
| `references/curated/pingone-st/` | `pingone-st` |
| `references/curated/ping-software/` | `ping-software` |
| `references/curated/cross-platform/` | `cross-platform` (or any) |

A file in `pingone-mt/` with `product_family: pingone-st` is a validation error.

---

## 4. One file = one primary task

Do not combine unrelated tasks in one file. If a curated anchor covers both "add an application" and "configure a sign-on policy," split it into two files.

The `title` should complete the sentence: "How to ___." If it cannot, the scope is too broad.

---

## 5. Scope section is mandatory in curated anchors

Every curated anchor must open with a `## Scope` section that states:
- **Covers:** what task this file helps complete
- **Does NOT cover:** what to use instead (with a reference to the correct file or skill)

This prevents agents from loading the wrong context and prevents authors from scope-creeping a file.

---

## 6. Do not copy full documentation into reference files

Curated anchors should capture:
- Decision points and prerequisites
- Configuration fields and their constraints (use tables)
- Platform-specific variants
- Cross-references

They should NOT contain:
- Full verbatim doc pages
- Screenshots or image embeds
- Content already covered in another curated file in the same skill
- Marketing language

If the full detail belongs in the docs, link to it in `## Source`.

---

## 6a. No UI navigation language

Reference files are read by agents, not humans following a walkthrough. Never write step-by-step UI procedures.

**Banned patterns:**
- Numbered click sequences: "1. Navigate to X → 2. Click Y → 3. Enter Z"
- "Go to", "open", "scroll to", "find the button", "click Save"
- Prose that describes how to use an admin console UI

**Allowed patterns:**
- Admin surface pointer (single line): **Admin surface:** Settings → Custom Domains
- Configuration field tables with field name, type, and constraint
- Decision rules: "Use confidential client type when the app can hold a secret"
- Constraint statements: "Redirect URIs require exact match — add all environments upfront"

The test: if a sentence is about where to click, delete it. If it is about what a field means or what decision to make, keep it.

---

## 7. Cross-references use relative repo paths

Always reference other files using repo-relative paths from the skill root:

```markdown
- `references/curated/cross-platform/foundation-overview.md`
- `references/curated/pingone-mt/app-registration.md`
```

Never use absolute paths, full URLs to internal files, or bare filenames without a path.

---

## 8. `status` must be accurate

| Value | Meaning |
|---|---|
| `current` | Accurate and maintained |
| `draft` | Not yet reviewed; do not load in production |
| `deprecated` | Outdated; do not load; kept for history |

Set `status: deprecated` instead of deleting a file when the content has been replaced, so CI can detect dangling references.

---

## 9. Plugin-local files must not import from `/shared`

Files inside `plugins/<plugin>/` must be self-contained. They may reference:
- Other files within the same plugin (`skills/<skill>/...`, `references/...`)
- The plugin's own orientation files (`README.md`, `routing-hints.md`, etc.)

They must NOT reference:
- `/shared/taxonomies/...`
- `/shared/schemas/...`
- Any path outside the plugin directory

The `/shared` layer is available only in full-repo installs. Plugin files are the fallback for standalone installs.

---

## 10. Every `SKILL.md` must have a Multi-skill use cases section

Ping Identity solutions require multiple layers of configuration — a single skill is rarely sufficient for a production-ready outcome. Every `SKILL.md` must include a `## Multi-skill use cases` section that:

- States which other skills are needed to complete a real end-to-end use case
- Provides at least one concrete numbered example showing the full skill sequence
- Ends with an explicit handoff instruction ("complete X here, then hand off to Y")

This section must appear after `## When NOT to use this skill` and before the first routing table.

The goal is to prevent agents from treating a single skill as complete when the platform actually requires composing several skills to reach a working solution.

---

## 11. `SKILL.md` files are routing logic, not content

A `SKILL.md` must:
- State when to use the skill (trigger phrases / user intents)
- State when NOT to use the skill (redirect to the correct skill)
- Route by task → platform → curated anchor (in that order)
- Reference curated files by path

A `SKILL.md` must NOT:
- Contain step-by-step configuration instructions
- Duplicate content from reference files
- Exceed ~120 lines

If a routing table is growing beyond 10–12 rows, that is a sign the skill scope is too broad — split the routing branch into a sub-skill or a dedicated reference file.
