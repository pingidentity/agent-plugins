<!--
USAGE — delete this comment after filling in the template:
1. Copy this file to `plugins/<plugin>/skills/<skill-dir>/SKILL.md`; the directory name must equal `name:`.
2. Replace every {{PLACEHOLDER}}, then remove this block.
3. `product_family` must be one of: pingone-mt | aic | ping-software | cross-platform | ai-identity | multi-product.
4. Run `python3 scripts/validate_skills.py --root .` before opening a PR. It enforces:
   - Frontmatter matches `shared/schemas/skill-frontmatter-schema.json` (description 50–500 chars).
   - `name` equals the skill directory name.
   - SKILL.md ≤ 160 lines.
   - Every inline `references/...` routing link resolves to a real file.
5. Full authoring rules: `.claude/skills/ping-skill-writing/SKILL.md` — write for a fully autonomous agent (no user-present steps), don't duplicate docs content (link out instead), one product per reference file, never cross-link skills as handoffs.
-->
---
name: {{SKILL_NAME}}
description: "{{Trigger description: the specific request signals that should activate this skill, phrased so an agent can route to it. 50–500 chars — pack the highest-value routing tokens (product names, protocols, error strings); cut anything an agent could infer.}}"
compatibility: "{{Assumes a harness with web retrieval — live docs via web_fetch; state live documentation overrides local reference files. Add: MCP access, CLI version, read-only vs mutating.}}"
metadata:
  publisher: Ping Identity
  version: "0.1.0"
  product_family: {{PRODUCT_FAMILY}}
---

# {{SKILL_TITLE}}

{{One-paragraph role statement: what this skill does, how it routes, and where it hands off.}}

## When to use this skill

- {{Request signal or trigger}}
- {{Request signal or trigger}}

## When NOT to use this skill

- {{Out-of-scope case}} → {{concrete next action: docs URL, admin console, MCP tool, or CLI — never a skill name}}
- {{Out-of-scope case}} → {{concrete next action: docs URL, admin console, MCP tool, or CLI — never a skill name}}

## Retrieval and output discipline

{{Optional — when live docs or MCP are required. Live documentation overrides local reference files. Each reference file ends with a `## Source` block linking the live docs behind it.}}

## Routing

{{How to choose a row. Load only the routed reference.}}

| Request signal | Start with |
|---|---|
| {{SIGNAL}} | `references/{{TOPIC}}.md` |
| {{SIGNAL}} | `references/{{TOPIC}}.md` |

Keep this file a router — triggers and routing tables only, ≤ 160 lines. Push versioned facts, API signatures, and step-level detail into `references/` so coverage grows without adding skills.

One product per reference file — split mixed-product topics into parallel per-product files (or per-product directories in a cross-portfolio skill).
