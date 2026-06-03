# Contributing to Ping Identity Agent Skills

This repo ships the 6 umbrella skills for the Ping Identity agent skills package. Contributions are welcome — this guide covers the workflow for adding or updating a skill, a curated reference anchor, or an eval prompt set.

---

## Quick start

```bash
git clone https://github.com/pingidentity/agent-plugins.git
cd agent-plugins

# Install pre-commit hooks (run once after cloning)
bash scripts/install-hooks.sh

# Validate everything manually
python3 scripts/validate_skills.py --root .

# Run evals (mock, no API key needed)
python3 -m evals.harness.validate_prompts
python3 -m evals.harness.run_eval --adapter mock --layer 1
python3 -m evals.harness.run_eval --adapter mock --layer 2

# Run evals (live, requires Bedrock credentials)
python3 -m evals.harness.run_eval --adapter claude --layer 1
```

All three commands must exit 0 before you open a PR.

---

## PR checklist

The pre-commit hook (`bash scripts/install-hooks.sh`) runs the first four checks automatically on every `git commit`. Confirm all items before opening a PR:


- [ ] `python3 scripts/validate_skills.py --root .` exits 0
- [ ] `python3 -m evals.harness.validate_prompts` exits 0
- [ ] `python3 -m evals.harness.run_eval --adapter mock --layer 1` — all skills PASS
- [ ] `python3 -m evals.harness.run_eval --adapter mock --layer 2` — all skills PASS
- [ ] `SKILL.md` ≤ 120 lines (`wc -l plugins/ping-identity/skills/<name>/SKILL.md`)
- [ ] `SKILL.md` `name:` field matches directory name
- [ ] All new curated anchors have complete frontmatter (see Frontmatter contract below)
- [ ] `product_family` in each anchor matches its directory path
- [ ] No `/r/en-us/`, `apps.pingone.com`, or `/latest/` AIC URLs in anchors
- [ ] New skill: `evals/prompts/<skill>.yaml` added with ≥10 trigger / ≥5 non-trigger / ≥3 ambiguous prompts
- [ ] `plugins/ping-identity/references/index.json` updated if new curated anchors added
- [ ] No changes to `/shared/` referenced from `plugins/` (plugin files must be self-contained)

CI runs these checks automatically and blocks merge on failure.

---

## Authoring a new skill

1. Create `plugins/ping-identity/skills/<skill-name>/` — name must be lowercase, hyphenated, ≤64 chars.
2. Copy from the template:
   ```bash
   cp shared/templates/SKILL.template.md plugins/ping-identity/skills/<name>/SKILL.md
   cp shared/templates/ping-marketplace.template.json plugins/ping-identity/skills/<name>/ping-marketplace.json
   mkdir -p plugins/ping-identity/skills/<name>/references/{curated,generated,runtime}
   ```
3. Fill in `SKILL.md`:
   - Keep it ≤120 lines — routing decision tree only, no prose
   - `name:` must exactly match the directory name
   - `description:` must be specific enough that an agent can decide to activate this skill without reading the body
   - Add a `## When to use` section, a `## When NOT to use` section, and a routing table
4. Add ≥3 curated anchors in `references/curated/` — see Authoring a curated anchor below
5. Add `references/runtime/docs-mcp-routing.md` — use `shared/templates/runtime-routing-stub.md` as a starting point
6. Add the skill to `plugins/ping-identity/references/index.json`
7. Add `evals/prompts/<skill>.yaml` — see Eval prompt requirements below
8. Add the skill to `plugins/ping-identity/plugin-map.md` and `.well-known/agent-skills/index.json`
9. Run `python3 scripts/validate_skills.py --root .` — must exit 0
10. Run all mock evals — must exit 0

**Decision rule** (from strategy doc § 4): A new skill is created only if it has a distinct trigger, a distinct user outcome, enough reference depth that routing materially improves results, and low overlap with an existing umbrella. Otherwise add it as a reference pack inside an existing skill.

---

## Authoring a curated anchor

Curated anchors live in `references/curated/<branch>/` where `<branch>` is one of:
`pingone-mt` | `pingone-st` | `ping-software` | `cross-platform` | `ai-identity`

Use the template:

```bash
cp shared/templates/curated-reference.template.md \
   plugins/ping-identity/skills/<skill>/references/curated/<branch>/<name>.md
```

### Frontmatter contract

Every curated `.md` file must have ALL of these fields:

```yaml
---
title: "Human-readable title"
product_family: cross-platform          # must match directory path
products: ["pingone", "pingone-aic"]    # specific products
capabilities: ["foundation"]            # at least one
services: []
audience: ["admin", "developer"]
use_cases: ["workforce", "customer"]
doc_type: guide                         # guide | reference | concept | troubleshooting | architecture
status: current                         # current | draft | deprecated
canonical: true                         # true for all curated anchors
last_updated: "2026-06-03"             # ISO date
slug: "https://docs.pingidentity.com/..." # source URL
---
```

`product_family` must match the anchor's **directory path**:

| Directory | Required product_family |
|---|---|
| `curated/pingone-mt/` | `pingone-mt` |
| `curated/pingone-st/` | `pingone-st` |
| `curated/ping-software/` | `ping-software` |
| `curated/cross-platform/` | `cross-platform` |
| `curated/ai-identity/` | `ai-identity` |
| `curated/` (root, skill = ping-identity-for-ai) | `ai-identity` |
| `curated/` (root, any other skill) | `cross-platform` |

### Body structure

Follow this section order (from `shared/templates/AUTHORING-RULES.md`):

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

Rules:
- Include an explicit `## Scope` with **Covers:** and **Does NOT cover:** statements
- Write configuration facts and field tables — no UI navigation steps ("click X", "navigate to Y")
- Cross-references use repo-relative paths only — no absolute paths or bare filenames
- Anchor length: 150–400 lines for curated anchors
- No `/r/en-us/`, `apps.pingone.com`, or `/latest/` AIC URLs

---

## Eval prompt requirements

Every skill must have `evals/prompts/<skill>.yaml` validated against `evals/schemas/prompt-set.schema.json`.

**Minimum per skill:**
- ≥10 `trigger_prompts` — prompts that should activate this skill
- ≥5 `non_trigger_prompts` — prompts that belong to a different skill (include `expected_skill`)
- ≥3 `ambiguous_prompts` — prompts that need clarification before routing (include `expected_clarification_keywords`)

**For strategy use cases:** prompts matching the 9 Getting Started 0–30 use cases from the strategy doc use IDs `T-50` and above to avoid collision with existing T-01–T-12 series.

Validate locally:

```bash
python3 -m evals.harness.validate_prompts
```

---

## Updating a curated anchor

1. Make your changes
2. Update `last_updated:` in the frontmatter to today's date
3. Run `python3 scripts/validate_skills.py --root .`
4. If the anchor changed materially, regenerate manifests:
   ```bash
   python3 scripts/build_reference_manifests.py --root .
   ```
5. Commit anchor changes and updated manifests together

---

## Ownership

- **Skill routing logic and SKILL.md:** TAP / DevEx Catalyst PMs (Ping Identity)
- **Curated anchor accuracy:** Product teams own the content; skill authors own the structure
- **Eval prompt sets:** Skill authors
- **CI and tooling:** DevEx

**Support:** This is a community-supported, open-source package. See [README.md](README.md) for the support model. File bugs at `https://github.com/pingidentity/agent-plugins/issues`.
