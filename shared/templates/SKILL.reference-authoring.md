---
name: reference-authoring
description: Use this skill whenever you are asked to create, update, or review a reference file in this repo — including curated anchors and node reference files. Invoke with /reference-authoring or when the task is "add a reference", "write a reference file", "create a curated anchor", "document [feature] in a reference", or any request to author content under a skill's references/ directory.
compatibility: Designed for this repo's skill system. No external tools required.
metadata:
  publisher: internal
  version: "1.0"
---

# reference-authoring

Author well-formed reference files for any skill in this repo — curated anchors and node reference files — following the conventions in AUTHORING-RULES.md.

## When to use this skill

- "Create a reference file for [topic]"
- "Add a curated anchor for [platform feature]"
- "Document [node / service / pattern] in a reference"
- "Write the reference for [X] under ping-orchestration"
- "Update the reference for [topic] to add [detail]"
- "Review this reference file"
- Any task that produces a `.md` file under a `references/` directory

## When NOT to use this skill

- If the task is editing a `SKILL.md` routing file: follow AUTHORING-RULES.md §0 and §11 directly
- If the task is building a new skill from scratch: use `SKILL.template.md` first, then return here for the reference files

---

## Step 1 — Confirm the reference type

| Type | When to create it | Directory |
|---|---|---|
| Curated anchor | Hand-authored, task-completing, canonical | `references/curated/<platform>/` |

All reference files are hand-authored curated anchors.

**Canonical rule:** set `canonical: true` on curated anchors.

---

## Step 2 — Choose the right directory

Match the file's platform scope to its directory path:

| Content scope | Directory |
|---|---|
| PingOne MT only | `references/curated/pingone-mt/` |
| PingOne ST only | `references/curated/pingone-st/` |
| Ping Software Suite only | `references/curated/ping-software/` |
| Two or more platforms | `references/curated/cross-platform/` |
| Node reference (PingOne ST) | `references/curated/pingone-st/nodes/` |

The `product_family` frontmatter field must match the directory.

---

## Step 3 — Write the frontmatter

Every reference file requires a complete frontmatter block. Use `curated-reference.template.md` as the base.

**Required fields** (CI rejects files missing these):

| Field | Notes |
|---|---|
| `title` | Sentence-case; completes "How to ___" |
| `product_family` | `pingone-mt` / `pingone-st` / `ping-software` / `cross-platform` |
| `capabilities` | One or more of: `foundation` / `orchestration` / `universal-services` / `app-integration` / `identity-for-ai` / `quickstart` |
| `doc_type` | `guide` / `reference` / `concept` / `tutorial` / `troubleshooting` / `architecture` |
| `status` | `current` for new files; `draft` if not yet reviewed |

**Optional but always include for curated anchors:**

| Field | Notes |
|---|---|
| `canonical` | `true` for curated anchors |
| `last_updated` | YYYY-MM-DD |
| `slug` | Canonical docs URL for this topic |

---

## Step 4 — Structure the body

Every curated anchor must follow this section order:

```
# Title

One-sentence description of the task this file helps complete.

## Scope
  Covers: ...
  Does NOT cover: ... (with redirect to correct file/skill)

## [Content sections]
  Configuration fields, decision rules, constraints, patterns.
  Use tables for fields. Use one-liners for admin surface pointers.

## Prerequisites
  Bullet list. Omit if none.

## Common variants
  Table of variant / note pairs. Include platform differences here.

## Related references
  Repo-relative paths only.

## Source
  Canonical docs URL(s).
```

The `## Scope` section is mandatory. A file without it will be rejected in review.

---

## Step 5 — Write the content

### Write configuration facts, not console procedures

Reference files are read by agents. They are not walkthroughs for humans.

**Do this:**
```markdown
**Admin surface:** Realm → Applications → OAuth 2.0 Clients → + Create Client

| Field | Notes |
|---|---|
| Client ID | Auto-generated or custom; must be unique within the realm |
| Redirect URIs | Exact match enforced; add all environments upfront |
| Client Type | Confidential (can hold a secret) or Public (SPA/native; requires PKCE) |
```

**Not this:**
```markdown
1. Navigate to Applications
2. Click OAuth 2.0 Clients
3. Click + Create Client
4. Enter a Client ID
5. Click Save
```

### Rules for content

- **Admin surface:** one line per surface, format: `**Admin surface:** Path → To → Location`
- **Configuration fields:** always a table with field name + constraint or note
- **Decision rules:** state the criterion, not the navigation ("Use confidential client type when the app can hold a secret")
- **Constraints:** state them directly ("Redirect URIs require exact match")
- **No UI verbs:** ban "navigate to", "click", "scroll", "open", "find the button", "hit Save"
- **No marketing language:** no "powerful", "seamless", "best-in-class"
- **Length:** 150–400 lines for curated anchors; split if longer

### One file = one primary task

The title must complete "How to ___." If it covers two unrelated tasks, split it.

---

## Step 6 — Cross-references

Use repo-relative paths from the skill root:

```markdown
- `references/curated/cross-platform/foundation-overview.md`
- `references/curated/pingone-st/nodes/mfa-nodes.md`
```

Never use absolute paths, bare filenames, or full URLs to internal files.

---

## Step 7 — Validate before finishing

Run through this checklist before marking the file done:

- [ ] Frontmatter present and complete; all required fields set
- [ ] `product_family` matches directory path
- [ ] `## Scope` section present with Covers / Does NOT cover
- [ ] No numbered UI navigation steps
- [ ] No UI verbs (navigate, click, scroll, open, save)
- [ ] Configuration fields in tables, not prose lists
- [ ] Admin surface pointers are single lines, not paragraphs
- [ ] `canonical: true` only if this is the single authoritative file for the task
- [ ] Cross-references use repo-relative paths
- [ ] `## Source` present with canonical docs URL

---

## Reference

- `shared/templates/curated-reference.template.md` — base template
- `shared/templates/AUTHORING-RULES.md` — full rule set (§6, §6a, §7 most relevant)
