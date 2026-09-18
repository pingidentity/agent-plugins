---
name: ping-skill-writing
description: "Use this skill when authoring Ping Identity specific plugin skills for this repository. Plugin skills are those in `./plugins/**/skills/`. Covers structure, formatting and content guidance."
---

# Ping Skill Writing

Structure, formatting, and content guidance for distributable plugin skills. Use alongside any general-purpose skill-authoring skill.

## Structure

Start from `assets/templates/SKILL.template.md`. Default to one skill per domain, not one per product or activity — keep the number of skills low. SKILL.md is a router: routing tables progressively disclose product- and activity-specific detail from `references/` files, so each skill's coverage grows through its references rather than by adding skills.

`references/` is a plain tree of maintained content — every file in it is shipped and kept current. There is no "curated" or staging tier.

After any change, run `python3 scripts/validate_skills.py --root .` — it enforces the skill frontmatter schema (description 50–500 chars), `name:` matching the directory, SKILL.md ≤ 160 lines, and resolution of inline `references/...` routing links.

## Rules

### Keep the `description:` between 50 and 500 characters

The description is the trigger surface every agent routes on, at a standing context cost in every session. Keep 50–500 chars, packing the highest-value routing tokens (product names, protocols, error strings) and cutting anything an agent could infer from the task itself.

### Never cross-link skills as handoffs

Take an "agent knows best" approach: the agent sources its own context and tools from the original prompt. No skill may reference or signpost another inside its content — SKILL.md or references. Inter-skill links create dependencies that break easily and can pull the agent into context the prompt never asked for. The frontmatter `description:` is the routing surface, not in-content links: phrase it so a prompt like "create an application for PingOne" routes here without the skill ever being named.

- Bad: "Step 1: integrate the XYZ application. To integrate applications, hand off to the `ping-application-integration` skill."
- Good: "Step 1: integrate the XYZ application."

Name the concrete task only — the agent knows it needs application integration and will find the best available skill, docs, or tool for it (possibly better than any skill we could point to).

### Never bake tool calls (API, CLI, MCP, SDK) into SKILL.md or references

Reference content gives the "what" and "why", optionally as a pseudo-workflow — never channel-specific invocations. The "how" lives in per-channel files, each repeating the workflow with that channel's instructions, hints, and gotchas:

```
SKILL.md                                # router (short skills may hold reference material directly)
references/application-integration.md   # what / why / pseudo-workflow — no tool calls
references/application-integration/     # per-channel "how"
    api.md                              #   API calls
    cli.md                              #   CLI commands
    mcp.md                              #   MCP tool calls
    sdk.md                              #   SDK functions
```

### Don't duplicate documentation content

Plugin skills assume the customer's harness has web retrieval (`web_fetch`). SKILL.md and references give a high-level steer — awareness, concept linkage, where the work goes — and link to live docs for detail. Duplicated docs content drifts as the docs change, duplicates the work of docs writers, bloats context the agent may not need, and can wrongly signal that no further material is needed. End each reference file with a short `## Source` block linking the live docs behind it, and state in the skill that live documentation overrides local files. If a docs MCP ships, a skill's base instruction can switch from `web_fetch` to a docs search keyed on those links.

### One product per reference file

Never mix considerations for different products in a single reference file. Split into parallel per-product files (flat layout, in a single-product skill) or per-product directories with a README entry point (in a cross-portfolio skill), so an agent working one product loads only that product's content. Mixed-product files blur integration boundaries and invite hallucination.

### Write for a fully autonomous agent

Skills assume no user is present. No "ask the user", "present options", or "wait for confirmation" steps — an autonomous agent loops waiting for an answer that never comes. Name the concrete next action instead: a docs URL, the admin console, an MCP tool, or a CLI. Human-facing clarification workflows belong only in the `ping-identity-quickstart` skill, the one deliberately user-present front door.

## Packaging

- Skill identity lives entirely in SKILL.md frontmatter: `name`, `description`, `compatibility`, and the full `metadata` block (`publisher`, `version`, `product_family`). There are no per-skill marketplace JSON files. When renaming or rescoping a skill, update its frontmatter and the plugin descriptions (`.claude-plugin/plugin.json`, marketplace manifests) together.
- Plugins ship content only. No eval routines, enforcement scripts, or taxonomy files are bundled alongside skills.
