# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **public-facing skill package** that exposes Ping Identity's agent skills through a unified layer. It is consumed by AI agents (Claude Code, Copilot CLI, Gemini CLI, etc.) to guide reasoning about Ping Identity platforms — not executed as application code.

The repo ships one plugin: `plugins/ping-identity/`, which contains skills, reference files, and routing logic. The `/shared/` directory holds canonical taxonomies, schemas, templates, and evals that apply across all plugins.

## No build system

There are no build, compile, test, or lint commands. All content is Markdown and JSON. The only automated concern is frontmatter validation (CI rejects reference `.md` files with missing required fields).

## Skill authoring

Every skill lives in `plugins/<plugin>/skills/<skill-name>/`:
- `SKILL.md` — routing logic only (≤120 lines); structured as: when to use → when NOT to use → multi-skill use cases → routing tables → retrieval escalation
- `ping-marketplace.json` — skill metadata for the Claude Code marketplace
- `references/curated/` — hand-authored task-completing docs (150–400 lines, `canonical: true`)
- `references/generated/` — CI-populated shortlists and stubs (`canonical: false`)

Before writing any `SKILL.md` or reference file, read `shared/templates/AUTHORING-RULES.md` in full — it is the single source of truth for all authoring rules. Key constraints enforced in review:
- Every reference `.md` requires a complete frontmatter block (`title`, `product_family`, `capabilities`, `doc_type`, `status` are mandatory)
- `product_family` in frontmatter must match the file's directory path (e.g., a file in `pingone-st/` must have `product_family: pingone-st`)
- Curated anchors must include a `## Scope` section with explicit Covers/Does NOT cover statements
- No UI navigation steps ("click X", "navigate to Y") — write configuration facts, field tables, and decision rules instead
- Cross-references must use repo-relative paths, never absolute paths or bare filenames
- Plugin files (`plugins/<plugin>/`) must not reference anything in `/shared/`

## Reference file structure (curated anchors)

Follow this section order:
```
# Title
One-sentence description.
## Scope
## [Content sections — tables, decision rules, constraints]
## Prerequisites
## Common variants
## Related references
## Source
```

## Routing architecture

Skills route requests in three steps:
1. **Skill selection** — match user intent to the correct skill (`ping-quickstart`, `ping-foundation`, `ping-orchestration`, `ping-universal-services`, `ping-app-integration`, `ping-identity-for-ai`)
2. **Platform detection** — classify as `pingone-mt`, `pingone-st`, `ping-software`, or `cross-platform`
3. **Reference tier** — load curated anchors first (1–3 max); fall back to generated shortlist; only query external Docs MCP if both are insufficient

Canonical routing rules: `shared/taxonomies/routing-rules.md`. Platform family definitions: `shared/taxonomies/platform-families.md`. Plugin-local routing (for standalone installs without `/shared/`): `plugins/ping-identity/routing-hints.md`.

## Adding a new skill

1. Create `plugins/ping-identity/skills/<skill-name>/` with `SKILL.md` and `ping-marketplace.json`
2. The `name` field in `SKILL.md` frontmatter must exactly match the directory name
3. Add the skill to `plugins/ping-identity/plugin-map.md` and `plugins/ping-identity/references/index.json`
4. Write at least 3 benchmark prompts that should trigger the skill and 2 that should not — validate with `shared/evals/routing-eval.md`
5. Use `shared/templates/SKILL.template.md` as the starting structure

## Eval format

Run skill routing evals using the format in `shared/evals/routing-eval.md`. The scorecard has five dimensions: Routing Correctness (30), Context Correctness (25), Answer Correctness (20), Token Efficiency (15), Fallback Discipline (10). A run fails at <80/100 or any hard-gate violation (wrong umbrella skill, major factual error, unnecessary external docs call, token spend >150% of minimum).

## Plugin standalone vs. full-repo

The plugin at `plugins/ping-identity/` is designed to work standalone (without `/shared/`). In that mode it uses its own orientation files (`README.md`, `plugin-map.md`, `platform-scope.md`, `routing-hints.md`). When the full repo is present, `/shared/taxonomies/` is authoritative and overrides plugin-local equivalents.

## GitHub

Remote: `https://github.com/pingidentity/agent-plugins.git`  
Use a `pingidentity` org member account for all `gh` operations.
