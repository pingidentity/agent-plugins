# AGENTS.md

This file provides guidance to coding agents when working with code in this repository.

## What this repo is

Ping Identity Agent Plugins — a set of agent-skills plugins (Claude Code, Cursor, Copilot, Gemini CLI, etc.) that give AI coding agents deep knowledge of the Ping Identity platform (PingOne, PingOne Advanced Identity Cloud / AIC, PingFederate, PingAccess, PingDirectory, DaVinci). The repo is content (Markdown skills + reference anchors + JSON manifests), not application code. The Python/JS here exists to validate that content.

## Commands

```bash
# Install pre-commit hooks (once after cloning)
bash scripts/install-hooks.sh

# Validate all skill/reference content against authoring rules — run after any skill or reference change
python3 scripts/validate_skills.py --root .

# Validate without cloning (npx)
npx github:pingidentity/agent-plugins validate
```

The skill-content validator must exit 0 before opening a PR. The pre-commit hook (installed via `install-hooks.sh`, hooksPath `.githooks`) runs it automatically when staged files touch skill content or validation inputs — its trigger pattern matches any plugin's `skills/` directory plus `shared/schemas/` and `scripts/validate_skills.py`.

## Architecture

### Plugin layout

Everything lives under `plugins/<plugin-name>/`, one plugin per audience surface:

- `ping-identity-quickstart` — human-facing front door. One skill, `ping-identity-quickstart`: a one-page resource site map (platform detection + pointers to docs, portal, marketplace, GitHub, tooling). It has no `references/` directory — its durable orientation facts were distilled into `ping-identity` reference topics.
- `ping-identity` — cross-portfolio, agent-facing. One skill under `skills/`:
  - `ping-identity` — cross-portfolio advisory dispatcher (routes by platform/product/solution/use-case before handing off); its reference topics include general app-integration orientation.
- `ping-identity-pingone` — agent-facing, PingOne multi-tenant. Three skills under `skills/`:
  - `pingone-app-integration` — app-side integration code against a PingOne environment (Ping SDK wiring for Android/iOS/JS, OIDC/PKCE, CORS, Worker applications, troubleshooting, ForgeRock→Ping SDK migration).
  - `davinci-flow-design` — DaVinci flow design/build (flow model, flow patterns, registration/MFA, passkey flows, flow promotion); produces flow designs and connector wiring as artifacts.
  - `davinci-flow-engineering` — traces and debugs live PingOne DaVinci flow executions (actor/interaction/transaction/time-window correlation, subflow reconstruction, failure-signal detection) using evidence pulled through the remote PingOne MCP server. This plugin doesn't install or configure the MCP server itself — it assumes authorized access is already connected.
- `ping-identity-pingone-aic` — agent-facing, PingOne Advanced Identity Cloud (single-tenant). Two skills under `skills/`:
  - `aic-journey-design` — AIC journey design/build (node families, journey use cases, wiring invariants, promotion, MCP journey authoring) that also covers PingAM trees; uses AIC MCP tools to create/update journeys when connected.
  - `aic-app-integration` — app-side integration code against AIC (Journey modules, journey client, OIDC/PKCE, tenant CORS, OAuth clients, troubleshooting, ForgeRock→Ping SDK migration).

A companion plugin, `ping-orchestration-sdks`, is sourced externally (`pingidentity/ping-sdk-agent-skills`) via the marketplace and is not stored under this repo's `plugins/` directory — don't look for its content here.

Plugins contain `.claude-plugin/` and `.cursor-plugin/` (agent manifests), `assets/`, and `skills/`.

### Skill authoring

How to write, structure, and package skill content — SKILL.md routers and routing tables, reference files, frontmatter/metadata, cross-skill independence, validator rules — is defined in the `ping-skill-writing` skill at `.claude/skills/ping-skill-writing/SKILL.md`. Invoke it for any change to skill or reference content under `plugins/**/skills/` rather than working from this file.

Agent-facing facts that stay here:

- `scripts/validate_skills.py` validates `SKILL.md` files only — frontmatter against `shared/schemas/skill-frontmatter-schema.json`, `name:` matching the directory, length, and resolution of inline `` `references/...` `` routing links. Reference-file content is not validated; its authoring rules live in the skill.
- Portfolio reference topics under `plugins/ping-identity/skills/ping-identity/references/<topic>/README.md` are plain-markdown orientation pages (no frontmatter), selected via the routing tables embedded in that skill's `SKILL.md`.
- Plugin-level identity lives in `.claude-plugin/plugin.json` plus the repo-level `.claude-plugin/marketplace.json` / `.cursor-plugin/marketplace.json`; skill-level identity lives in each `SKILL.md` frontmatter (see the skill).
