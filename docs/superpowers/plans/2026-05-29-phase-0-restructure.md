# Phase 0 — Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring the repo into the Cloudflare-inspired layout described in [PLAN.md](../../../PLAN.md) Phase 0 and the [Ping Identity Agent Skill Strategy doc § 4 "In Practice"](https://docs.google.com/document/d/1ts57b476DNIEduopqq5fSwyJx5RZSWL72UVGj_EVRYk). The 6 umbrella skills land in `plugins/ping-identity/skills/` (3 already live, 3 newly scaffolded), each with the `references/{curated,generated,runtime}/` tier. Top-level `commands/`, `rules/`, `evals/` directories ship per the Cloudflare pattern. A runnable Layer 1 + Layer 2 eval harness ships ungated in Phase 0 and becomes a CI gate in Phase 3.

**Architecture:** The repo follows Cloudflare's outer shape — `.claude-plugin/`, `.cursor-plugin/`, `commands/`, `rules/`, `skills/` (under `plugins/ping-identity/`) — and extends it with three Ping-specific additions: a 3-tier reference model (`curated/` + `generated/` + `runtime/`) on each skill per strategy doc § 6, an `evals/` harness, and `shared/` taxonomies that are out of scope for Cloudflare's repo. The 6 v1 skills are exactly the strategy-doc umbrellas: `ping-quickstart`, `ping-foundation`, `ping-orchestration`, `ping-universal-services`, `ping-app-integration`, `ping-identity-for-ai`. Helix is **not** a v1 skill — it lives as a runtime tier inside each skill's `references/runtime/` per strategy doc.

**Tech Stack:** Markdown, YAML (PyYAML), JSON Schema, Python 3.11+, `pytest` for harness tests. No new runtime infra.

**Branch:** `skills-refactoring` (already created and checked out).

**Working directory:** `/Users/george.bafaloukas/Dev/tiger-agent-skills`

---

## Departure from the previous draft

This plan was rewritten from the prior 9-skill cloud-first version once we confirmed the strategy doc's § 4 set is the source of truth. Key changes:

- **Skill set:** 6 umbrella skills (matches strategy doc § 4), not 9 cloud-product skills.
- **No `_archive/`:** the three live skills stay in place — they already match strategy doc § 4. Only their `references/` directory is reorganized to add the `runtime/` tier.
- **No top-level `skills/` directory:** skills nest under `plugins/ping-identity/skills/` per strategy doc § 5. That preserves the multi-plugin model (`plugins/ping-identity-sdks/` is v1.1).
- **Helix is not a skill:** it's a runtime tier referenced from each skill's `references/runtime/docs-mcp-routing.md`. v1.1 may promote it.
- **Cursor `.mdc` rule added:** Cloudflare ships one (`rules/workers.mdc`); we ship `rules/ping-identity.mdc` for parity.
- **Eval harness retained as Ping addition:** strategy doc § 2.7 says eval is "a progressive evolution" — Phase 0 ships Layer 1 + Layer 2 ungated; Phase 3 makes it a CI gate.

---

## File Structure

After Phase 0, the repo looks like this. Items marked **NEW** are created by this plan. Items marked **REORGANIZED** keep their content but get extra tier directories. Items marked **MODIFIED** have small content edits.

```
.claude-plugin/
  marketplace.json                              MODIFIED (small content refresh)
  plugin.json                                   NEW (Cloudflare parity)
.cursor-plugin/
  marketplace.json                              NEW (Cloudflare parity)
  plugin.json                                   NEW (Cloudflare parity)
.well-known/
  agent-skills/
    index.json                                  NEW — empty stub for Phase 3 to fill

commands/                                       NEW
  .gitkeep                                      NEW — Phase S fills this

rules/                                          NEW
  authoring-rules.md                            PORTED from shared/templates/AUTHORING-RULES.md
  routing-rules.md                              PORTED from shared/taxonomies/routing-rules.md
  runtime-selection.md                          NEW — sandbox vs production decision rule
  ping-identity.mdc                             NEW — Cursor-style rule for Cloudflare parity

shared/                                         (existing) unchanged

plugins/
  ping-identity/
    .claude-plugin/
      plugin.json                               NEW (per strategy doc § 5)
    skills/
      ping-quickstart/                          REORGANIZED — add references/runtime/
        SKILL.md                                (existing) unchanged in Phase 0
        ping-marketplace.json                   (existing) unchanged
        references/
          curated/                              REORGANIZED — existing flat refs move into curated/
            getting-started-overview.md         (existing — moved one level deeper)
            choose-the-right-ping-platform.md   (existing — moved)
            common-starting-patterns.md         (existing — moved)
          generated/                            (existing) unchanged
          runtime/
            docs-mcp-routing.md                 NEW (stub)
      ping-foundation/                          REORGANIZED — add references/runtime/
        SKILL.md                                (existing)
        ping-marketplace.json                   (existing)
        references/
          curated/                              (existing) unchanged
          generated/                            (existing) unchanged
          runtime/
            docs-mcp-routing.md                 NEW (stub)
      ping-orchestration/                       REORGANIZED — add references/runtime/
        SKILL.md                                (existing)
        ping-marketplace.json                   (existing)
        references/
          curated/                              (existing) unchanged
          generated/                            (existing) unchanged
          runtime/
            docs-mcp-routing.md                 NEW (stub)
      ping-universal-services/                  NEW
        SKILL.md                                NEW (≤120 lines, scaffold)
        ping-marketplace.json                   NEW
        references/{curated,generated,runtime}/ NEW (with .gitkeep + runtime stub)
      ping-app-integration/                     NEW
        SKILL.md                                NEW
        ping-marketplace.json                   NEW
        references/{curated,generated,runtime}/ NEW
      ping-identity-for-ai/                     NEW
        SKILL.md                                NEW
        ping-marketplace.json                   NEW
        references/{curated,generated,runtime}/ NEW

evals/                                          NEW
  README.md                                     NEW
  prompts/
    ping-quickstart.yaml                        NEW
    ping-foundation.yaml                        NEW
    ping-orchestration.yaml                     NEW
    ping-universal-services.yaml                NEW
    ping-app-integration.yaml                   NEW
    ping-identity-for-ai.yaml                   NEW
  golden/.gitkeep                               NEW (Phase 1 populates per skill)
  schemas/
    prompt-set.schema.json                      NEW — JSON Schema for prompts/*.yaml
  scorecards/
    routing-eval.md                             PORTED+EXTENDED from shared/evals/routing-eval.md
    anchor-selection-eval.md                    NEW — Layer 2 scorecard
    plan-quality-eval.md                        NEW — Layer 3 scorecard (used Phase 1+)
  harness/
    pyproject.toml                              NEW
    requirements.txt                            NEW
    run_eval.py                                 NEW — Layer 1 + Layer 2 runner
    judge_plans.py                              NEW — Layer 3 LLM-as-judge stub
    cross_llm.py                                NEW — Layer 4 multi-LLM driver stub
    validate_prompts.py                         NEW — schema validator
    adapters/
      __init__.py                               NEW
      base.py                                   NEW — LLMAdapter abstract base
      claude.py                                 NEW — Anthropic SDK adapter (stub)
      mock.py                                   NEW — deterministic adapter for harness tests
    tests/
      __init__.py                               NEW
      test_validate_prompts.py                  NEW
      test_run_eval.py                          NEW
      test_adapters_mock.py                     NEW
  results/.gitkeep                              NEW (per-day folders generated at run time)
```

**Why this layout:**

- The 6 skill directories under `plugins/ping-identity/skills/` mirror strategy doc § 5 exactly.
- Each skill's `references/{curated,generated,runtime}/` tier matches strategy doc § 6.
- `_archive/` is intentionally absent — the three live skills already match the strategy and stay in place.
- `evals/harness/` is a self-contained Python project so it runs locally in Phase 0 and from GitHub Actions in Phase 3 with no migration.
- `evals/prompts/<skill>.yaml` is one file per skill — easy to diff alongside SKILL.md PRs.
- Adapters are pluggable so Layer 4 (cross-LLM) drops in by adding `codex.py` and `gemini.py` without changing the runner.

---

## Eval design — how skill accuracy is measured

This section defines the contract that every skill PR (Phase 1 onward) must satisfy. The harness scaffolded in Phase 0 is the implementation of this contract. Strategy doc § 2.7 explicitly notes that "Testing and eval frameworks are a progressive evolution, not a day-1 requirement. We keep the investment low" — the design below honors that by shipping Layers 1–2 runnable in Phase 0 and Layers 3–4 as runnable stubs.

### What "accuracy" means for a Ping skill

A Ping umbrella skill is a routing + retrieval + planning artifact. There is no single "correct output" — accuracy decomposes into four observable signals:

1. **Activation accuracy** — given a prompt, does the agent invoke this umbrella skill iff this skill should handle it?
2. **Anchor selection accuracy** — once the skill is active, does the agent open the smallest sufficient set of curated reference files?
3. **Plan accuracy** — does the answer name the right products, services, fields, and runtimes, with no factual errors?
4. **Tier discipline** — does the answer stop at curated when curated is enough, expand to generated only when needed, fall back to Docs MCP only as a last resort? Strategy doc § 0 ("Agent Path") makes this explicit.

Layer 1 and Layer 2 of the harness measure (1) and (2) deterministically by inspecting the agent's tool-call log. Layer 3 measures (3) and (4) via LLM-as-judge against a hand-authored golden plan. Layer 4 reruns Layers 1 and 3 across Claude / Codex / Gemini. Layer 5 (Phase S) verifies the plan actually produces a working tenant artifact.

### Prompt set contract — `evals/prompts/<skill>.yaml`

Every umbrella skill ships a YAML prompt set with this shape (validated by `evals/schemas/prompt-set.schema.json`):

```yaml
skill: ping-orchestration         # required, must match the skill directory name
version: 1
trigger_prompts:                  # ≥10 — should activate this skill
  - id: T-01
    prompt: "I want to build a registration journey in PingOne ST that collects email and sends an OTP."
    expected_anchors:             # Layer 2: curated paths the agent should load
      - plugins/ping-identity/skills/ping-orchestration/references/curated/journey-design-patterns.md
    expected_tier: curated        # curated | generated | docs-mcp — Layer 3 tier-discipline check
    notes: "Sandbox-tier orientation; one curated anchor is sufficient."
non_trigger_prompts:              # ≥5 — should NOT activate this skill
  - id: N-01
    prompt: "How do I install PingFederate on RHEL?"
    expected_skill: ping-foundation
ambiguous_prompts:                # ≥3 — should produce a clarifying question, not a route
  - id: A-01
    prompt: "I want to add MFA."
    expected_clarification_keywords: ["pingone", "aic", "platform", "mt", "st", "workforce", "ciam"]
```

### Layer 1 — Routing accuracy (mandatory, every PR from Phase 3)

**Question answered:** Did the agent activate the right umbrella skill for this prompt?

**Algorithm:**
1. For each prompt in `trigger_prompts`, `non_trigger_prompts`, `ambiguous_prompts`, send the prompt to the LLM adapter with the 6 SKILL.md files registered as available skills.
2. Record `loaded_skills`: every skill the agent invoked.
3. Score:
   - Trigger prompt → **correct** iff `<skill>` is in `loaded_skills`. Multi-skill activation is allowed (and expected per strategy doc); the named skill must be present.
   - Non-trigger prompt → **correct** iff the prompt's `<skill>` is NOT in `loaded_skills` AND the `expected_skill` IS in `loaded_skills` (when non-null).
   - Ambiguous prompt → **correct** iff the agent emitted a clarifying question containing ≥1 keyword from `expected_clarification_keywords` AND did not finalize a route.

**Pass bar (per skill):** ≥90% trigger correct, ≥90% non-trigger correct, ≥80% ambiguous handled.

### Layer 2 — Curated anchor selection (mandatory, every PR from Phase 3)

**Question answered:** Within an activated skill, did the agent open the right curated reference files?

**Algorithm:**
1. For each `trigger_prompt` whose `expected_anchors` is non-empty, run the same prompt through the adapter.
2. Capture every `Read(<path>)` call the agent issues during the run.
3. Score:
   - **Precision** = `|loaded ∩ expected| / |loaded|`
   - **Recall**    = `|loaded ∩ expected| / |expected|`
   - **Per-prompt pass** = recall ≥ 1.0 AND precision ≥ 0.5.

**Pass bar (per skill):** ≥85% of `expected_anchors`-bearing prompts pass.

**Why precision and recall:** Strategy doc § 0 mandates "use the smallest trusted context first." Loading the wrong anchor wastes tokens; missing the right one produces a vague answer. Both must be measured.

### Layer 3 — Plan quality (LLM-as-judge, weekly + before release)

**Question answered:** Is the produced plan correct, complete, concrete, and at the right tier?

**Algorithm:**
1. For each prompt in `evals/golden/<skill>/<prompt-id>.md`, run the prompt through the adapter and capture the full final assistant message.
2. Pass `(prompt, golden_plan, produced_plan)` to a judge LLM (DIFFERENT model than the one being evaluated).
3. Judge scores 1–5 on each of:
   - **Correctness** — no factual errors about Ping products, services, fields
   - **Completeness** — covers all required steps in the golden plan
   - **Concreteness** — names specific products, fields, env vars; no "configure as appropriate"
   - **Tier discipline** — used curated when sufficient; only escalated to generated/docs-mcp when curated didn't cover the task; matches `expected_tier` per `rules/runtime-selection.md`
4. Output: per-prompt scores + overall mean per skill.

**Pass bar (per skill):** mean ≥ 4.0 across all 4 dimensions; zero prompts scoring < 3 on any dimension.

### Layer 4 — Cross-LLM consistency (weekly)

**Question answered:** Do skills work acceptably on Codex and Gemini, not just Claude?

**Algorithm:**
1. Run Layer 1 + Layer 3 with adapters for Claude, Codex, Gemini in parallel.
2. Write per-LLM JSON to `evals/results/<YYYY-MM-DD>/<llm>.json`.
3. Acceptance:
   - Any LLM scoring < 70% on Layer 1 → adds an entry to `README.md § Known limitations`, does NOT block merge.
   - Any LLM scoring < 60% on Layer 1 → blocks v1 launch (Phase 4).

### Layer 5 — End-to-end (Phase S only, scaffolded but unused in Phase 0)

Out of scope for this plan beyond directory placeholders.

### Eval pass-bar summary

| Layer | What it measures | Per-skill bar | When |
|---|---|---|---|
| 1 — Routing | Correct skill activated | 90% trigger / 90% non-trigger / 80% ambiguous | Every PR from Phase 3 |
| 2 — Anchors | Right curated files loaded | 85% per-prompt pass | Every PR from Phase 3 |
| 3 — Plan quality | Correct, complete, concrete, right tier | mean ≥ 4.0; no dim < 3 | Weekly + pre-release |
| 4 — Cross-LLM | Acceptable on Codex/Gemini | ≥70% Layer 1 (warn); ≥60% (block at launch) | Weekly |
| 5 — E2E | Sandbox tenant actually works | 95% rolling 7-day | Nightly, Phase S only |

### Phase 0 specifically delivers

- All 6 prompt-set files. The three live skills (`ping-quickstart`, `ping-foundation`, `ping-orchestration`) ship at full v1 minimums (≥10 / ≥5 / ≥3) since their SKILL.md and curated content already exist. The three new skills ship Phase-0 minimums (3 / 2 / 1); Phase 1 expands them once their bodies land.
- `validate_prompts.py` enforcing the schema, with pytest coverage.
- `run_eval.py` capable of executing Layer 1 and Layer 2 against the `mock` adapter (so the harness itself is testable without API budget).
- `judge_plans.py` and `cross_llm.py` as runnable stubs.
- A documented invocation: `python -m evals.harness.run_eval --adapter mock --layer 1` produces a passing run on the placeholder prompt sets — proves the harness end-to-end before Phase 1 wires real LLM calls.

---

## Tasks

### Task 1: Create the v1 directory skeleton (commands, rules, evals, .well-known, multi-IDE manifests)

**Files:**
- Create: `commands/.gitkeep`
- Create: `rules/.gitkeep`
- Create: `evals/` subtree (placeholders only; content lands in Tasks 7–13)
- Create: `.well-known/agent-skills/index.json` (empty stub)
- Create: `.cursor-plugin/marketplace.json`
- Create: `.cursor-plugin/plugin.json`
- Create: `.claude-plugin/plugin.json`
- Create: `plugins/ping-identity/.claude-plugin/plugin.json`

- [ ] **Step 1: Create top-level directories with .gitkeep markers**

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills
mkdir -p commands rules
mkdir -p evals/prompts evals/golden evals/schemas evals/scorecards evals/harness/adapters evals/harness/tests evals/results
mkdir -p .well-known/agent-skills .cursor-plugin plugins/ping-identity/.claude-plugin
touch commands/.gitkeep rules/.gitkeep evals/golden/.gitkeep evals/results/.gitkeep
```

- [ ] **Step 2: Create the `.well-known/agent-skills/index.json` stub**

Write `/Users/george.bafaloukas/Dev/tiger-agent-skills/.well-known/agent-skills/index.json`:

```json
{
  "$schema": "https://agentskills.io/spec/v0.2.0/index.schema.json",
  "version": "0.2.0",
  "skills": []
}
```

(Phase 3 populates the `skills` array.)

- [ ] **Step 3: Create `.cursor-plugin/marketplace.json` and `.cursor-plugin/plugin.json`**

Write `/Users/george.bafaloukas/Dev/tiger-agent-skills/.cursor-plugin/marketplace.json`:

```json
{
  "name": "ping-identity-skills",
  "owner": { "name": "Ping Identity" },
  "description": "Agent skills for Ping Identity platforms — six umbrella skills covering platform setup, orchestration, universal services, app integration, AI identity patterns, and platform routing.",
  "plugins": [
    {
      "name": "ping-identity",
      "source": "./plugins/ping-identity"
    }
  ]
}
```

Write `/Users/george.bafaloukas/Dev/tiger-agent-skills/.cursor-plugin/plugin.json`:

```json
{
  "name": "ping-identity",
  "version": "1.0.0",
  "description": "Six-umbrella agent skill suite for Ping Identity: PingOne MT, PingOne ST (AIC), Ping Software Suite, DaVinci, universal services, app integration, identity for AI.",
  "author": { "name": "Ping Identity" },
  "keywords": ["ping", "pingone", "aic", "davinci", "pingfederate", "identity", "authentication", "ciam", "ai-identity"]
}
```

- [ ] **Step 4: Create `.claude-plugin/plugin.json` (Cloudflare parity)**

Write `/Users/george.bafaloukas/Dev/tiger-agent-skills/.claude-plugin/plugin.json`:

```json
{
  "name": "ping-identity",
  "version": "1.0.0",
  "description": "Six-umbrella agent skill suite for Ping Identity platforms.",
  "author": { "name": "Ping Identity" }
}
```

- [ ] **Step 5: Create the inner plugin manifest required by strategy doc § 5**

Write `/Users/george.bafaloukas/Dev/tiger-agent-skills/plugins/ping-identity/.claude-plugin/plugin.json`:

```json
{
  "name": "ping-identity",
  "version": "1.0.0",
  "description": "Core Ping Identity platform skills: ping-quickstart, ping-foundation, ping-orchestration, ping-universal-services, ping-app-integration, ping-identity-for-ai.",
  "author": { "name": "Ping Identity" }
}
```

- [ ] **Step 6: Validate every JSON file parses**

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills
for f in .claude-plugin/marketplace.json .claude-plugin/plugin.json .cursor-plugin/marketplace.json .cursor-plugin/plugin.json .well-known/agent-skills/index.json plugins/ping-identity/.claude-plugin/plugin.json; do
  python3 -c "import json; json.load(open('$f'))" && echo "OK $f" || echo "FAIL $f"
done
```

Expected: every line prints `OK`.

- [ ] **Step 7: Commit**

```bash
git add commands/ rules/ evals/ .well-known/ .cursor-plugin/ .claude-plugin/plugin.json plugins/ping-identity/.claude-plugin/
git commit -m "chore: scaffold v1 directory skeleton (Cloudflare-inspired)

Add commands/, rules/, evals/ top-level dirs and the multi-IDE
manifests required by strategy doc § 5: .claude-plugin/plugin.json,
.cursor-plugin/marketplace.json + plugin.json, plugins/ping-identity/
.claude-plugin/plugin.json, and a .well-known/agent-skills/index.json
stub for the discovery RFC.

Refs: PLAN.md Phase 0 step 1; strategy doc § 5"
```

---

### Task 2: Reorganize the three live skills into the `references/{curated,generated,runtime}/` shape

The three live skills (`ping-quickstart`, `ping-foundation`, `ping-orchestration`) keep their SKILL.md and existing content. Only their reference layout changes:

- `ping-quickstart` currently has flat `references/*.md` — those move into `references/curated/`.
- `ping-foundation` and `ping-orchestration` already have `references/curated/` and `references/generated/`.
- All three need a new `references/runtime/docs-mcp-routing.md` stub.

**Files:**
- Move: `plugins/ping-identity/skills/ping-quickstart/references/*.md` → `plugins/ping-identity/skills/ping-quickstart/references/curated/`
- Create: `plugins/ping-identity/skills/ping-quickstart/references/runtime/docs-mcp-routing.md`
- Create: `plugins/ping-identity/skills/ping-foundation/references/runtime/docs-mcp-routing.md`
- Create: `plugins/ping-identity/skills/ping-orchestration/references/runtime/docs-mcp-routing.md`
- Modify: `plugins/ping-identity/skills/ping-quickstart/SKILL.md` (update reference paths from `references/X.md` to `references/curated/X.md`)

- [ ] **Step 1: Reorganize ping-quickstart's flat references into `curated/`**

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills/plugins/ping-identity/skills/ping-quickstart
mkdir -p references/curated
git mv references/getting-started-overview.md references/curated/getting-started-overview.md
git mv references/choose-the-right-ping-platform.md references/curated/choose-the-right-ping-platform.md
git mv references/common-starting-patterns.md references/curated/common-starting-patterns.md
```

- [ ] **Step 2: Update SKILL.md reference paths in ping-quickstart**

Read `/Users/george.bafaloukas/Dev/tiger-agent-skills/plugins/ping-identity/skills/ping-quickstart/SKILL.md`, then replace all three flat reference paths to point under `curated/`:

- `references/getting-started-overview.md` → `references/curated/getting-started-overview.md`
- `references/choose-the-right-ping-platform.md` → `references/curated/choose-the-right-ping-platform.md`
- `references/common-starting-patterns.md` → `references/curated/common-starting-patterns.md`

- [ ] **Step 3: Create the runtime tier stub for all three live skills**

For each of `ping-quickstart`, `ping-foundation`, `ping-orchestration`, create `references/runtime/docs-mcp-routing.md`:

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills/plugins/ping-identity/skills
for s in ping-quickstart ping-foundation ping-orchestration; do
  mkdir -p $s/references/runtime
done
```

Write the same content (with the skill name substituted) to each `<skill>/references/runtime/docs-mcp-routing.md`:

```markdown
---
title: Docs MCP routing — <SKILL>
status: current
last_updated: 2026-05-29
---

# Runtime tier — Docs MCP routing for <SKILL>

This file describes when and how this skill falls back to live Docs MCP retrieval. It is the third tier in the strategy doc § 0 "Agent Path".

## When to escalate to Docs MCP

Use Docs MCP only when:
1. The 1–3 curated anchors loaded from `references/curated/` did not answer the question.
2. The bounded shortlist in `references/generated/<branch>/top-N.json` did not fill the gap.
3. The user's task requires version-specific, current, or long-tail information (e.g., a recently released feature, a deprecation note, a specific API field).

If any of these is false, do NOT call Docs MCP. Strategy doc § 0 mandates "use the smallest trusted context first."

## Surgical query rules

When Docs MCP is required, query it with:
- The exact platform family (PingOne MT, PingOne ST, Ping Software Suite)
- The exact product or service name
- The exact capability (e.g., "MFA policy", not "authentication")
- A version constraint when applicable

Retrieve specific sections, not full page dumps.

## Helix as a runtime path

Production-bound execution runs through Helix conversation APIs. The decision rule for sandbox-vs-production lives in `rules/runtime-selection.md`. Helix is **not** a v1 skill; it is a runtime tier referenced from this file.

## Related

- `rules/runtime-selection.md`
- `references/curated/` — tier 1
- `references/generated/` — tier 2
```

- [ ] **Step 4: Verify the reorganization**

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills/plugins/ping-identity/skills
for s in ping-quickstart ping-foundation ping-orchestration; do
  for tier in curated generated runtime; do
    [ -d $s/references/$tier ] && echo "OK $s/references/$tier" || echo "FAIL $s/references/$tier"
  done
done
ls ping-quickstart/references/curated/ | wc -l   # Expect: 3
```

Expected: all `OK`, ping-quickstart has 3 curated files.

- [ ] **Step 5: Commit**

```bash
git add plugins/ping-identity/skills/
git commit -m "refactor: align live skills with strategy-doc reference tier model

Move ping-quickstart's flat references into references/curated/, add
the runtime/ tier with a docs-mcp-routing.md stub to all three live
skills (ping-quickstart, ping-foundation, ping-orchestration), and
update ping-quickstart's SKILL.md paths to match.

Refs: PLAN.md Phase 0 step 3; strategy doc § 6"
```

---

### Task 3: Scaffold the three new umbrella skills

Each new skill ships with `SKILL.md` (≤120 lines, scaffold), `ping-marketplace.json`, and the full `references/{curated,generated,runtime}/` tier.

**Files (all NEW, three skills × four files each):**
- `plugins/ping-identity/skills/ping-universal-services/{SKILL.md, ping-marketplace.json, references/curated/.gitkeep, references/generated/.gitkeep, references/runtime/docs-mcp-routing.md}`
- `plugins/ping-identity/skills/ping-app-integration/{...same...}`
- `plugins/ping-identity/skills/ping-identity-for-ai/{...same...}`

- [ ] **Step 1: Create directory trees for the three new skills**

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills/plugins/ping-identity/skills
for s in ping-universal-services ping-app-integration ping-identity-for-ai; do
  mkdir -p $s/references/curated $s/references/generated $s/references/runtime
  touch $s/references/curated/.gitkeep $s/references/generated/.gitkeep
done
```

- [ ] **Step 2: Define the SKILL.md scaffold template**

Every new SKILL.md uses this shape (replace `<…>` placeholders per skill). Keep ≤120 lines.

```markdown
---
name: <skill-name>
description: <one-paragraph assertive description naming what the skill does AND when to invoke. Include keywords agents pattern-match on. Max 1024 chars.>
compatibility: Designed for Ping Identity <area> work. References product docs and the Ping Marketplace.
metadata:
  publisher: Ping Identity
  version: "0.1.0-scaffold"
---

# <skill-name>

> **Status:** Phase 0 scaffold per strategy doc § 4. Body authored in Phase 1. Routing logic stub only.

<one-sentence purpose statement from strategy doc § 4>

## Invocation

Invoke explicitly with `/<skill-name>` or by saying "use <skill-name> to...".

## When to use this skill

- <placeholder trigger 1>
- <placeholder trigger 2>
- <placeholder trigger 3>
- <placeholder trigger 4>
- <placeholder trigger 5>

## When NOT to use this skill

- If the task is platform setup or admin: use `ping-foundation`.
- If the task is flow / journey design: use `ping-orchestration`.
- If the user is just orienting: use `ping-quickstart`.

## Multi-skill use cases

A complete <area> use case typically spans:

| Layer | Skill |
|---|---|
| Platform setup | `ping-foundation` |
| Orchestration / flows | `ping-orchestration` |
| <area-specific layer> | `<skill-name>` (this skill) |
| App integration | `ping-app-integration` |

## Routing — Step 1: What are you trying to do?

| Task | Branch |
|---|---|
| <placeholder> | <branch> |

## Step 2: Platform branch

| Platform | Curated reference |
|---|---|
| PingOne MT | `references/curated/<placeholder>.md` |
| PingOne ST (AIC) | `references/curated/<placeholder>.md` |
| Ping Software Suite | `references/curated/<placeholder>.md` |

## Retrieval escalation

Per strategy doc § 0:

1. Curated anchors (`references/curated/`) — load 1–3 max. Stop if sufficient.
2. Generated shortlist (`references/generated/<branch>/top-N.json`) — Phase 2.
3. Docs MCP fallback — see `references/runtime/docs-mcp-routing.md`. Only if curated + shortlist insufficient.
```

- [ ] **Step 3: Author `ping-universal-services/SKILL.md`**

Use the template with:
- `name: ping-universal-services`
- `description`: "Shared services skill for the strategic value layers used across PingOne MT, PingOne ST (AIC), and Ping Software Suite — Protect, Verify, Credentials, IGA, SSO, Authorize. Use this skill whenever a task involves a Universal Service that is consumed from multiple platforms rather than administered from one. Includes service selection guidance, invocation patterns from PingOne or AIC, policy and verification patterns, and cross-product service usage. Also invoke with /ping-universal-services."
- Triggers: "Add PingOne Verify for KYC", "Score risk with PingOne Protect", "Issue a verifiable credential", "Add IGA governance", "Authorize with PingOne Authorize", etc.

- [ ] **Step 4: Author `ping-app-integration/SKILL.md`**

- `name: ping-app-integration`
- `description`: "Implementation skill for integrating Ping Identity into web, mobile, and SDK experiences. Use this whenever a task involves Android, iOS, or React SDK integration; embedding journeys; wiring auth flows into a web or mobile app; browser-based redirect flows; orchestration SDK references; or on-prem app-side integration patterns where the primary task is implementation rather than platform administration. Also invoke with /ping-app-integration."
- Triggers: "Integrate Ping into my React app", "Use the iOS SDK with AIC", "Wire OIDC into my mobile app", "Embed a journey in a webview", "Migrate from ForgeRock SDK to Ping SDK", etc.

- [ ] **Step 5: Author `ping-identity-for-ai/SKILL.md`**

- `name: ping-identity-for-ai`
- `description`: "AI-era identity patterns: Identity for AI, Verified Trust, agent identity, agent security, AI app authentication patterns, and workforce-helpdesk AI use cases. Use this whenever the task involves giving an AI agent a verified identity, securing agent-to-API access, applying Verified Trust signals, or designing identity for AI workloads. Also invoke with /ping-identity-for-ai."
- Triggers: "Give my AI agent an identity", "Verified Trust signals for an MCP server", "Secure agent access to APIs", "Workforce helpdesk AI auth pattern", "Identity for AI architecture", etc.

- [ ] **Step 6: Author `ping-marketplace.json` for each new skill**

Each file follows the existing `ping-marketplace.json` shape from a live skill. Use `/Users/george.bafaloukas/Dev/tiger-agent-skills/plugins/ping-identity/skills/ping-foundation/ping-marketplace.json` as the reference template; substitute name, description, tags per skill.

- [ ] **Step 7: Author the runtime stub for each new skill**

Use the same `docs-mcp-routing.md` template from Task 2 Step 3, substituting the skill name.

- [ ] **Step 8: Verify every SKILL.md is ≤120 lines and `name` matches its directory**

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills
for s in ping-quickstart ping-foundation ping-orchestration ping-universal-services ping-app-integration ping-identity-for-ai; do
  f=plugins/ping-identity/skills/$s/SKILL.md
  lines=$(wc -l < $f)
  name=$(grep -E '^name:' $f | head -1 | awk '{print $2}')
  if [ "$lines" -gt 120 ]; then echo "FAIL: $s SKILL.md is $lines lines (>120)"; fi
  if [ "$name" != "$s" ]; then echo "FAIL: $s has name: $name"; fi
done
```

Expected: no `FAIL` output. (The three live skills may already exceed 120 lines — if so, leave them for Phase 1 trim work; do not break working content. Print as `WARN` instead and continue.)

- [ ] **Step 9: Commit**

```bash
git add plugins/ping-identity/skills/ping-universal-services/ plugins/ping-identity/skills/ping-app-integration/ plugins/ping-identity/skills/ping-identity-for-ai/
git commit -m "feat: scaffold ping-universal-services, ping-app-integration, ping-identity-for-ai

Three Phase 0 scaffolds (≤120 lines each, agentskills.io compliant)
matching strategy doc § 4 'In Practice'. Each ships SKILL.md, a
ping-marketplace.json metadata file, and the canonical
references/{curated,generated,runtime}/ tier set per strategy § 6.
Bodies are stubs marked status=Phase 0 scaffold; Phase 1 fills in
routing tables and curated anchors per strategy § 7.

Refs: PLAN.md Phase 0 step 4; strategy doc § 4 and § 7"
```

---

### Task 4: Author `rules/runtime-selection.md`

This is the canonical decision rule for sandbox-vs-production runtime, referenced from every skill's `references/runtime/docs-mcp-routing.md` and used by Layer 3 of the eval (tier discipline scoring).

**Files:**
- Create: `rules/runtime-selection.md`
- Delete: `rules/.gitkeep`

- [ ] **Step 1: Author `rules/runtime-selection.md`**

```markdown
---
title: Runtime selection — sandbox vs production
status: current
last_updated: 2026-05-29
---

# Runtime selection

Decision rule: which runtime applies a plan produced by a Ping skill, and which reference tier to load.

## The two runtime modes

| Mode | What it does | When applied |
|---|---|---|
| **docs** | Output is a written plan: steps, product names, field tables, links to admin console pages. The user (or another agent) executes manually. | Sandbox/orientation, evaluation, learning, no live tenant available. |
| **helix** | Plan is executed by Helix conversation APIs against a live tenant via product-specific tools. Each write is gated. | Production-bound work, when the user has tenant credentials and explicit intent to apply changes. |

Helix is **not** a v1 skill — it is a runtime tier referenced from each skill's `references/runtime/docs-mcp-routing.md`. v1.1 may promote Helix to a first-class skill if it passes the four-criteria decision rule in PLAN.md.

## Decision rule for runtime mode (apply in order)

1. If the user explicitly asks for **a plan**, **explanation**, **walkthrough**, or **evaluation help** → `docs`.
2. If the user names a **sandbox**, **trial**, **POC**, or asks **"how would I…"** → `docs`.
3. If the user names a **production tenant**, asks to **apply / create / update / configure** in a specific tenant, or invokes a `/ping:` command with `--apply` → `helix`.
4. If the user is **unclear**, default to `docs` and ask one clarifying question.

## Tier discipline (the strategy doc § 0 "Agent Path" rule)

Within a `docs` plan, choose the smallest tier that resolves the prompt:

1. **Curated anchors** (`references/curated/`) — load 1–3. Stop if sufficient.
2. **Generated shortlist** (`references/generated/<branch>/top-N.json`) — only if curated didn't cover the task.
3. **Docs MCP** (per `references/runtime/docs-mcp-routing.md`) — only if curated + shortlist insufficient.

Layer 3 of the eval scores **Tier discipline (1–5)**: did the produced plan stop at the smallest sufficient tier per the prompt's `expected_tier`?

## Anti-patterns

- ❌ Producing a Helix-style plan when the user is in sandbox mode → over-promises execution.
- ❌ Producing a docs plan when the user explicitly asked to apply → under-delivers.
- ❌ Loading the generated shortlist when one curated anchor is sufficient → wastes tokens.
- ❌ Calling Docs MCP when curated + shortlist would have been enough → wastes tokens and slows the agent.

## Related

- `rules/routing-rules.md` — skill selection precedence
- `evals/scorecards/plan-quality-eval.md` — how tier discipline is scored
- Each skill's `references/runtime/docs-mcp-routing.md`
```

- [ ] **Step 2: Verify and commit**

```bash
rm -f /Users/george.bafaloukas/Dev/tiger-agent-skills/rules/.gitkeep
git add rules/runtime-selection.md
git commit -m "docs: add rules/runtime-selection.md

Canonical decision rule for sandbox (docs) vs production (helix) runtime
plus the strategy-doc § 0 tier-discipline rule (curated → generated →
docs MCP). Referenced from every skill's references/runtime/
docs-mcp-routing.md and scored by Layer 3 of the eval.

Refs: PLAN.md Phase 0 step 5; strategy doc § 0 and § 4"
```

---

### Task 5: Port `authoring-rules.md` and `routing-rules.md` into `rules/`; add Cursor `.mdc` rule

**Files:**
- Create: `rules/authoring-rules.md` (copied from `shared/templates/AUTHORING-RULES.md`)
- Create: `rules/routing-rules.md` (copied from `shared/taxonomies/routing-rules.md`)
- Create: `rules/ping-identity.mdc` (Cursor-style rule for Cloudflare parity)

- [ ] **Step 1: Copy authoring rules and routing rules**

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills
cp shared/templates/AUTHORING-RULES.md rules/authoring-rules.md
cp shared/taxonomies/routing-rules.md rules/routing-rules.md
```

- [ ] **Step 2: Author `rules/ping-identity.mdc`** (Cursor's `.mdc` rule format, per Cloudflare's `rules/workers.mdc`)

```mdc
---
description: Apply when working on Ping Identity platform tasks (PingOne MT, PingOne ST/AIC, PingFederate, PingAccess, PingDirectory, PingID, DaVinci).
alwaysApply: false
globs:
  - "**/*.tsx"
  - "**/*.ts"
  - "**/*.swift"
  - "**/*.kt"
  - "**/*.java"
  - "**/*.js"
  - "**/*.jsx"
---

# Ping Identity skill routing

When the user's task involves Ping Identity platforms, agents have access to six umbrella skills via the agent-skills repo:

- `ping-quickstart` — front door; product-family detection and routing
- `ping-foundation` — tenant, app, directory, policy, branding, admin
- `ping-orchestration` — DaVinci flows and journeys
- `ping-universal-services` — Protect, Verify, Credentials, IGA, SSO
- `ping-app-integration` — web, mobile, SDK integration
- `ping-identity-for-ai` — AI agent identity, Verified Trust

## Routing decision order inside every skill

1. What is the user trying to do? (intent)
2. Which platform family? (PingOne MT / PingOne ST / Ping Software Suite / cross-platform)
3. Which exact product or service?
4. Which reference tier? (curated → generated → docs-mcp)

## Tier discipline

Use the smallest trusted context first. Load 1–3 curated anchors before considering the generated shortlist. Use Docs MCP only when the first two tiers are insufficient.
```

- [ ] **Step 3: Commit**

```bash
git add rules/authoring-rules.md rules/routing-rules.md rules/ping-identity.mdc
git commit -m "docs: port authoring-rules and routing-rules into rules/; add Cursor .mdc

Copy shared/templates/AUTHORING-RULES.md and shared/taxonomies/
routing-rules.md into rules/ so authors have a single source of truth
at the new repo root. Add rules/ping-identity.mdc (Cursor-style rule)
for parity with Cloudflare's rules/workers.mdc.

Refs: PLAN.md Phase 0 step 5; Cloudflare repo structure"
```

---

### Task 6: Refresh `.claude-plugin/marketplace.json` for the v1 skill set

**Files:**
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Read the current marketplace.json**

Read `/Users/george.bafaloukas/Dev/tiger-agent-skills/.claude-plugin/marketplace.json`. The existing file already points at `plugins/ping-identity` — only minor metadata refreshes are needed.

- [ ] **Step 2: Replace the file with v1 content**

Write `/Users/george.bafaloukas/Dev/tiger-agent-skills/.claude-plugin/marketplace.json`:

```json
{
  "name": "ping-identity-skills",
  "owner": {
    "name": "Ping Identity",
    "email": "developer-experience@pingidentity.com"
  },
  "description": "Agent skills for Ping Identity platforms — six umbrella skills covering PingOne MT, PingOne Advanced Identity Cloud (ST), Ping Software Suite, DaVinci, universal services, app integration, and identity for AI.",
  "plugins": [
    {
      "name": "ping-identity",
      "source": "./plugins/ping-identity",
      "displayName": "Ping Identity",
      "description": "Six umbrella skills modelled on the Cloudflare few-broad-skills approach: ping-quickstart, ping-foundation, ping-orchestration, ping-universal-services, ping-app-integration, ping-identity-for-ai. Each routes by intent, platform family, exact product/service, and reference tier.",
      "version": "1.0.0",
      "author": { "name": "Ping Identity" },
      "category": "identity",
      "keywords": ["ping", "pingone", "aic", "davinci", "pingfederate", "pingaccess", "identity", "authentication", "ciam", "ai-identity"]
    }
  ]
}
```

- [ ] **Step 3: Validate JSON parses**

```bash
python3 -c "import json; json.load(open('/Users/george.bafaloukas/Dev/tiger-agent-skills/.claude-plugin/marketplace.json'))"
```

Expected: no output (success).

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "chore: refresh marketplace.json for the 6-umbrella v1 skill set

Update plugin description and keywords to reflect the strategy-doc § 4
umbrella set. Source path (./plugins/ping-identity) and version (1.0.0)
unchanged.

Refs: PLAN.md Phase 0 step 1"
```

---

### Task 7: Author the eval scorecards

**Files:**
- Create: `evals/scorecards/routing-eval.md` (ported + extended from `shared/evals/routing-eval.md`)
- Create: `evals/scorecards/anchor-selection-eval.md` (NEW for Layer 2)
- Create: `evals/scorecards/plan-quality-eval.md` (NEW for Layer 3)

- [ ] **Step 1: Port and update the routing scorecard**

```bash
cp /Users/george.bafaloukas/Dev/tiger-agent-skills/shared/evals/routing-eval.md /Users/george.bafaloukas/Dev/tiger-agent-skills/evals/scorecards/routing-eval.md
```

The existing scorecard already targets the 6 umbrella skills (it's the `shared/evals/` source). Add a new section near the top:

```markdown
## Layer 1 in the harness

This scorecard is the human-readable rubric for Layer 1 (routing accuracy). The automated harness implementation is `evals/harness/run_eval.py --layer 1`. It consumes `evals/prompts/<skill>.yaml` validated against `evals/schemas/prompt-set.schema.json`. CI runs Layer 1 from Phase 3 onward; PRs failing the pass bar (90% trigger / 90% non-trigger / 80% ambiguous) are blocked.
```

- [ ] **Step 2: Author `evals/scorecards/anchor-selection-eval.md`**

(Same content as in the previous draft — Layer 2 precision/recall against `expected_anchors`. The scorecard explains the algorithm in the same form as Layer 1.)

```markdown
---
title: Anchor selection eval — Layer 2
status: current
last_updated: 2026-05-29
---

# Anchor Selection Eval (Layer 2)

Used by `evals/harness/run_eval.py --layer 2` to score whether the agent loaded the right curated reference files within an active skill.

## Inputs

- `evals/prompts/<skill>.yaml` — every `trigger_prompts[*]` entry with non-empty `expected_anchors`.
- The agent's tool-call log for the run, captured by the LLM adapter.

## Score per prompt

```
loaded   = set of paths the agent passed to Read(...)
expected = set of paths in expected_anchors
precision = |loaded ∩ expected| / |loaded|
recall    = |loaded ∩ expected| / |expected|
pass      = recall >= 1.0 AND precision >= 0.5
```

## Aggregate per skill

- `pass_rate = passed_prompts / total_prompts_with_expected_anchors`
- **Pass bar:** `pass_rate >= 0.85`

## Failure output

```
[FAIL] T-04 (ping-orchestration)
  expected: plugins/ping-identity/skills/ping-orchestration/references/curated/journey-design-patterns.md
  loaded:   plugins/ping-identity/skills/ping-orchestration/references/curated/davinci-flow-patterns.md
  recall=0.0 precision=0.0
```

## Common failure modes

| Failure | Likely cause | Fix |
|---|---|---|
| recall=0 always | SKILL.md doesn't reference the expected anchor by path | Add anchor path to the SKILL.md retrieval list |
| recall=1 but precision<0.5 | SKILL.md loads too many anchors per prompt | Tighten routing table; split anchors |
| Inconsistent across runs | LLM non-determinism | Run with temperature=0; if still inconsistent, reword SKILL.md |
```

- [ ] **Step 3: Author `evals/scorecards/plan-quality-eval.md`** (Layer 3, LLM-as-judge — same content as previous draft, with the rubric updated to score `tier_discipline` rather than `runtime_correctness`)

```markdown
---
title: Plan quality eval — Layer 3
status: current
last_updated: 2026-05-29
---

# Plan Quality Eval (Layer 3)

Used by `evals/harness/judge_plans.py` to score the textual plan a skill produces against a hand-authored golden plan.

## Inputs

- `evals/prompts/<skill>.yaml` — `trigger_prompts[*]` with a corresponding `evals/golden/<skill>/<id>.md` file.
- The full final assistant message from the skill being evaluated.
- A judge LLM (Claude / Codex / Gemini), DIFFERENT from the LLM under test.

## Judge prompt template

```
You are scoring an agent's response against a reference plan.

USER PROMPT:
<prompt text>

REFERENCE PLAN (golden):
<golden plan markdown>

AGENT'S PRODUCED PLAN:
<produced plan markdown>

Score 1–5 on each dimension. Output ONLY valid JSON:
{
  "correctness":     {"score": <int>, "reason": "<≤200 chars>"},
  "completeness":    {"score": <int>, "reason": "<≤200 chars>"},
  "concreteness":    {"score": <int>, "reason": "<≤200 chars>"},
  "tier_discipline": {"score": <int>, "reason": "<≤200 chars>", "expected": "<curated|generated|docs-mcp>", "observed": "<curated|generated|docs-mcp|none>"}
}

Rubric:
- correctness: factual accuracy about Ping products, services, fields
- completeness: covers every required step in the reference
- concreteness: names specific products, fields, env vars; no generic prose
- tier_discipline: matches expected_tier per rules/runtime-selection.md;
  did not over-escalate; did not under-load
```

## Aggregate per skill

```
mean_correctness    = mean of all correctness scores
mean_completeness   = mean of all completeness scores
mean_concreteness   = mean of all concreteness scores
mean_tier           = mean of all tier_discipline scores

pass = all four means >= 4.0 AND no individual score < 3
```

## Why a different judge model

Self-judging collapses the eval. Defaults:
- Claude under test → Codex judges
- Codex under test → Claude judges
- Gemini under test → Claude judges

Override with `--judge <model>`.
```

- [ ] **Step 4: Commit**

```bash
git add evals/scorecards/
git commit -m "docs: add Layer 1, 2, 3 eval scorecards

Port shared/evals/routing-eval.md to evals/scorecards/ and add Layer 2
(anchor selection — precision/recall against expected_anchors) and
Layer 3 (plan quality — LLM-as-judge across correctness, completeness,
concreteness, tier discipline).

Refs: PLAN.md § Evaluation; strategy doc § 0"
```

---

### Task 8: Author the prompt-set JSON Schema and validator (TDD)

**Files:**
- Create: `evals/schemas/prompt-set.schema.json`
- Create: `evals/harness/validate_prompts.py`
- Create: `evals/harness/tests/test_validate_prompts.py`
- Create: `evals/harness/pyproject.toml`
- Create: `evals/harness/requirements.txt`
- Create: `evals/__init__.py`, `evals/harness/__init__.py`, `evals/harness/adapters/__init__.py`, `evals/harness/tests/__init__.py`

- [ ] **Step 1: Write the failing test**

`/Users/george.bafaloukas/Dev/tiger-agent-skills/evals/harness/tests/test_validate_prompts.py`:

```python
"""Schema validation tests for evals/prompts/*.yaml."""
import textwrap
from pathlib import Path

import pytest

from evals.harness.validate_prompts import ValidationError, validate_prompt_file


def write_yaml(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(content).strip() + "\n")
    return p


def test_minimal_valid_prompt_set_passes(tmp_path: Path):
    f = write_yaml(tmp_path, "ping-quickstart.yaml", """
        skill: ping-quickstart
        version: 1
        trigger_prompts:
          - id: T-01
            prompt: "Where do I start with Ping Identity?"
            expected_anchors: []
            expected_tier: curated
        non_trigger_prompts:
          - id: N-01
            prompt: "Build me a journey in PingOne ST."
            expected_skill: ping-orchestration
        ambiguous_prompts:
          - id: A-01
            prompt: "I want to add MFA."
            expected_clarification_keywords: ["pingone", "aic"]
    """)
    validate_prompt_file(f)  # no exception = pass


def test_skill_field_must_match_filename(tmp_path: Path):
    f = write_yaml(tmp_path, "ping-foundation.yaml", """
        skill: ping-orchestration
        version: 1
        trigger_prompts: []
        non_trigger_prompts: []
        ambiguous_prompts: []
    """)
    with pytest.raises(ValidationError, match="skill .* must match filename"):
        validate_prompt_file(f)


def test_missing_required_top_level_field_fails(tmp_path: Path):
    f = write_yaml(tmp_path, "ping-orchestration.yaml", """
        skill: ping-orchestration
        trigger_prompts: []
        non_trigger_prompts: []
        ambiguous_prompts: []
    """)
    with pytest.raises(ValidationError, match="version"):
        validate_prompt_file(f)


def test_trigger_prompt_requires_id_and_prompt(tmp_path: Path):
    f = write_yaml(tmp_path, "ping-foundation.yaml", """
        skill: ping-foundation
        version: 1
        trigger_prompts:
          - prompt: "missing id"
            expected_anchors: []
            expected_tier: curated
        non_trigger_prompts: []
        ambiguous_prompts: []
    """)
    with pytest.raises(ValidationError, match="id"):
        validate_prompt_file(f)


def test_expected_tier_enum_enforced(tmp_path: Path):
    f = write_yaml(tmp_path, "ping-foundation.yaml", """
        skill: ping-foundation
        version: 1
        trigger_prompts:
          - id: T-01
            prompt: "test prompt for tier"
            expected_anchors: []
            expected_tier: invalid-value
        non_trigger_prompts: []
        ambiguous_prompts: []
    """)
    with pytest.raises(ValidationError, match="expected_tier"):
        validate_prompt_file(f)
```

- [ ] **Step 2: Run the tests and verify they fail**

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills
python3 -m pytest evals/harness/tests/test_validate_prompts.py -v
```

Expected: 5 failures (module `evals.harness.validate_prompts` not found).

- [ ] **Step 3: Write `evals/schemas/prompt-set.schema.json`**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Skill prompt set",
  "type": "object",
  "required": ["skill", "version", "trigger_prompts", "non_trigger_prompts", "ambiguous_prompts"],
  "additionalProperties": false,
  "properties": {
    "skill": { "type": "string", "pattern": "^[a-z][a-z0-9-]*$" },
    "version": { "type": "integer", "minimum": 1 },
    "trigger_prompts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "prompt", "expected_anchors", "expected_tier"],
        "additionalProperties": false,
        "properties": {
          "id":     { "type": "string", "pattern": "^T-[0-9]{2,3}$" },
          "prompt": { "type": "string", "minLength": 10 },
          "expected_anchors":  { "type": "array", "items": { "type": "string" } },
          "expected_tier":     { "type": "string", "enum": ["curated", "generated", "docs-mcp"] },
          "notes":  { "type": "string" }
        }
      }
    },
    "non_trigger_prompts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "prompt", "expected_skill"],
        "additionalProperties": false,
        "properties": {
          "id":     { "type": "string", "pattern": "^N-[0-9]{2,3}$" },
          "prompt": { "type": "string", "minLength": 10 },
          "expected_skill": { "type": ["string", "null"] },
          "notes":  { "type": "string" }
        }
      }
    },
    "ambiguous_prompts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "prompt", "expected_clarification_keywords"],
        "additionalProperties": false,
        "properties": {
          "id":     { "type": "string", "pattern": "^A-[0-9]{2,3}$" },
          "prompt": { "type": "string", "minLength": 5 },
          "expected_clarification_keywords": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
          "notes":  { "type": "string" }
        }
      }
    }
  }
}
```

- [ ] **Step 4: Implement `evals/harness/validate_prompts.py`**

```python
"""Validate evals/prompts/*.yaml files against the prompt-set JSON schema."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

import yaml
from jsonschema import Draft7Validator

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "evals" / "schemas" / "prompt-set.schema.json"
PROMPTS_DIR = REPO_ROOT / "evals" / "prompts"


class ValidationError(Exception):
    pass


def _load_schema() -> dict:
    with SCHEMA_PATH.open() as f:
        return json.load(f)


def validate_prompt_file(path: Path) -> None:
    with path.open() as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValidationError(f"{path}: top-level must be a mapping")

    schema = _load_schema()
    errors = sorted(Draft7Validator(schema).iter_errors(data), key=lambda e: e.path)
    if errors:
        msgs = "; ".join(f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors)
        raise ValidationError(f"{path}: {msgs}")

    expected_skill = path.stem
    if data["skill"] != expected_skill:
        raise ValidationError(
            f"{path}: skill '{data['skill']}' must match filename '{expected_skill}'"
        )


def validate_all(paths: Iterable[Path] | None = None) -> list[Path]:
    paths = list(paths) if paths is not None else sorted(PROMPTS_DIR.glob("*.yaml"))
    failed: list[Path] = []
    for p in paths:
        try:
            validate_prompt_file(p)
            print(f"OK  {p.relative_to(REPO_ROOT)}")
        except ValidationError as exc:
            failed.append(p)
            print(f"FAIL {exc}", file=sys.stderr)
    return failed


def main() -> int:
    failed = validate_all()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Add `__init__.py` files and dependency manifests**

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills
touch evals/__init__.py evals/harness/__init__.py evals/harness/adapters/__init__.py evals/harness/tests/__init__.py
```

`evals/harness/requirements.txt`:
```
pyyaml>=6.0
jsonschema>=4.0
pytest>=8.0
anthropic>=0.40
```

`evals/harness/pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["evals/harness/tests"]
pythonpath = ["."]
```

- [ ] **Step 6: Install deps and run tests**

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills
python3 -m pip install -r evals/harness/requirements.txt
python3 -m pytest evals/harness/tests/test_validate_prompts.py -v
```

Expected: 5 passed.

- [ ] **Step 7: Commit**

```bash
git add evals/__init__.py evals/schemas/prompt-set.schema.json evals/harness/__init__.py evals/harness/adapters/__init__.py evals/harness/tests/__init__.py evals/harness/validate_prompts.py evals/harness/tests/test_validate_prompts.py evals/harness/requirements.txt evals/harness/pyproject.toml
git commit -m "feat(evals): prompt-set schema and validator

JSON Schema for evals/prompts/*.yaml + Python validator with 5 pytest
cases covering: minimal valid set, skill/filename match, required
top-level fields, required item fields, tier enum.

Run: python -m evals.harness.validate_prompts

Refs: PLAN.md § Evaluation Layer 1"
```

---

### Task 9: Author the 6 prompt-set YAML files

The three live skills (`ping-quickstart`, `ping-foundation`, `ping-orchestration`) ship at v1 minimums (≥10 / ≥5 / ≥3) since their bodies and curated content already exist. The three new skills ship Phase-0 minimums (3 / 2 / 1) and grow in Phase 1.

**Files (all NEW):**
- `evals/prompts/ping-quickstart.yaml`         (10 / 5 / 3)
- `evals/prompts/ping-foundation.yaml`         (10 / 5 / 3)
- `evals/prompts/ping-orchestration.yaml`      (10 / 5 / 3)
- `evals/prompts/ping-universal-services.yaml` (3 / 2 / 1)
- `evals/prompts/ping-app-integration.yaml`    (3 / 2 / 1)
- `evals/prompts/ping-identity-for-ai.yaml`    (3 / 2 / 1)

- [ ] **Step 1: Author `evals/prompts/ping-quickstart.yaml`**

10 trigger prompts mining the existing curated content (`getting-started-overview`, `choose-the-right-ping-platform`, `common-starting-patterns`). Examples: "Where do I start?", "PingOne vs PingFederate?", "We're evaluating Ping", "I inherited a Ping deployment", "Should we use cloud or on-prem?", "We want CIAM where do we begin?", "Add MFA without a platform context", "ForgeRock migration starting point", "Identity verification for new product", "Help us choose between AIC and PingOne MT".

Each `expected_anchors` references the seeded curated files at `plugins/ping-identity/skills/ping-quickstart/references/curated/<file>.md`.

5 non-trigger: prompts that name a platform directly and should route to the relevant umbrella, not quickstart. Examples: "Build me a DaVinci flow" (→ orchestration), "Add an OIDC app to my AIC tenant" (→ foundation), "Integrate Ping into my React app" (→ app-integration), "Score risk with PingOne Protect" (→ universal-services), "Give my AI agent a verified identity" (→ identity-for-ai).

3 ambiguous: "I want to add MFA", "How do I do passwordless?", "Risk-based authentication"; each lists keywords covering platform + workforce/CIAM + sandbox/production.

Skeleton (full file written by the executing agent):

```yaml
skill: ping-quickstart
version: 1
trigger_prompts:
  - id: T-01
    prompt: "Where do I start with Ping Identity? We're new and don't know which product to pick."
    expected_anchors:
      - plugins/ping-identity/skills/ping-quickstart/references/curated/getting-started-overview.md
      - plugins/ping-identity/skills/ping-quickstart/references/curated/choose-the-right-ping-platform.md
    expected_tier: curated
  # T-02 ... T-10
non_trigger_prompts:
  - id: N-01
    prompt: "Build me a registration journey in PingOne ST that collects email and sends an OTP."
    expected_skill: ping-orchestration
  # N-02 ... N-05
ambiguous_prompts:
  - id: A-01
    prompt: "I want to add MFA."
    expected_clarification_keywords: ["pingone", "aic", "platform", "workforce", "ciam"]
  # A-02, A-03
```

- [ ] **Step 2: Author `evals/prompts/ping-foundation.yaml`**

10 trigger covering: PingOne MT environment provisioning, AIC tenant + realm setup, OIDC app registration, SAML SP connection on PingFederate, directory setup (managed objects, LDAP/AD), authentication policy, branding/themes, PingDirectory admin, PingID administration, identity data model.

`expected_anchors` reference the existing curated files at `plugins/ping-identity/skills/ping-foundation/references/curated/<branch>/<file>.md`.

5 non-trigger: orchestration prompt, app integration prompt, AI identity prompt, universal services prompt, "where do I start" prompt.

3 ambiguous: "Configure MFA" (policy in foundation, or step-up in orchestration?), "Set up SSO" (which platform?), "Add a user" (admin or identity service?).

- [ ] **Step 3: Author `evals/prompts/ping-orchestration.yaml`**

10 trigger covering the existing curated content: DaVinci flow patterns, journey design patterns, the six node-category files (basic-auth, mfa, identity-management, federation-contextual, risk-management, utility), and the eight journey-use-case files (passwordless registration, social/local registration, password reset, progressive profiling, account recovery, MFA multi-method, financial step-up, Protect risk integration).

5 non-trigger / 3 ambiguous as appropriate.

- [ ] **Step 4: Author `evals/prompts/ping-universal-services.yaml`** (3 / 2 / 1)

Trigger: "Add PingOne Verify for KYC", "Score risk with PingOne Protect during login", "Issue a verifiable credential to a user". `expected_anchors: []` for now with `notes: "Phase 1 will populate expected_anchors once curated anchors exist."`. `expected_tier: curated`.

Non-trigger: a foundation prompt, an app-integration prompt.

Ambiguous: 1 prompt naming "verification" without specifying KYC vs. MFA verification.

- [ ] **Step 5: Author `evals/prompts/ping-app-integration.yaml`** (3 / 2 / 1)

Trigger: "Integrate Ping into my React app via the orchestration SDK", "Use the iOS SDK with AIC journeys", "Wire OIDC redirect into a mobile app".

Non-trigger: a foundation prompt, a quickstart prompt.

Ambiguous: 1 prompt naming "SDK" without specifying iOS / Android / React.

- [ ] **Step 6: Author `evals/prompts/ping-identity-for-ai.yaml`** (3 / 2 / 1)

Trigger: "Give my AI agent a verified identity for API access", "Use Verified Trust signals in my MCP server", "Workforce helpdesk AI auth pattern".

Non-trigger: a foundation prompt, an orchestration prompt.

Ambiguous: 1 prompt naming "agent" without specifying AI agent vs. user agent.

- [ ] **Step 7: Validate every prompt YAML**

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills
python3 -m evals.harness.validate_prompts
```

Expected:
```
OK  evals/prompts/ping-app-integration.yaml
OK  evals/prompts/ping-foundation.yaml
OK  evals/prompts/ping-identity-for-ai.yaml
OK  evals/prompts/ping-orchestration.yaml
OK  evals/prompts/ping-quickstart.yaml
OK  evals/prompts/ping-universal-services.yaml
```

- [ ] **Step 8: Commit**

```bash
git add evals/prompts/
git commit -m "feat(evals): seed prompt sets for the 6 v1 umbrella skills

Live skills (ping-quickstart, ping-foundation, ping-orchestration) ship
at v1 minimums (10/5/3) since their bodies and curated content already
exist. The three new skills ship Phase-0 minimums (3/2/1) and expand in
Phase 1 once curated anchors land per strategy doc § 7.

All prompt sets validate against evals/schemas/prompt-set.schema.json.

Refs: PLAN.md § Evaluation, Phase 0 step 4"
```

---

### Task 10: Build the LLM adapter base + mock adapter (TDD)

Same content as the previous draft. The mock adapter is what makes the harness testable without API budget.

**Files:**
- Create: `evals/harness/adapters/base.py`
- Create: `evals/harness/adapters/mock.py`
- Create: `evals/harness/tests/test_adapters_mock.py`

- [ ] **Step 1: Write the failing test**

`/Users/george.bafaloukas/Dev/tiger-agent-skills/evals/harness/tests/test_adapters_mock.py`:

```python
from evals.harness.adapters.mock import MockAdapter, MockRule


def test_mock_adapter_returns_loaded_skills_per_rule():
    rules = [
        MockRule(prompt_contains="MFA",       loaded_skills=["ping-quickstart"], read_paths=[]),
        MockRule(prompt_contains="journey",   loaded_skills=["ping-orchestration"],
                 read_paths=["plugins/ping-identity/skills/ping-orchestration/references/curated/journey-design-patterns.md"]),
    ]
    adapter = MockAdapter(rules=rules, default_skills=[])

    r1 = adapter.run("I want to add MFA to my mobile banking app.")
    assert r1.loaded_skills == ["ping-quickstart"]
    assert r1.read_paths == []
    assert r1.final_message != ""

    r2 = adapter.run("Build a registration journey with email OTP.")
    assert r2.loaded_skills == ["ping-orchestration"]
    assert r2.read_paths == [
        "plugins/ping-identity/skills/ping-orchestration/references/curated/journey-design-patterns.md"
    ]


def test_mock_adapter_default_when_no_rule_matches():
    adapter = MockAdapter(rules=[], default_skills=[])
    r = adapter.run("a prompt that matches nothing")
    assert r.loaded_skills == []
    assert r.read_paths == []


def test_mock_adapter_supports_clarification_for_ambiguous_prompts():
    rules = [
        MockRule(prompt_contains="add MFA",
                 clarifying_question="Are you in PingOne MT, AIC, or on-prem? Workforce or CIAM?"),
    ]
    adapter = MockAdapter(rules=rules, default_skills=[])
    r = adapter.run("I want to add MFA.")
    assert r.loaded_skills == []
    assert r.clarifying_question is not None
    assert "pingone" in r.clarifying_question.lower() or "ciam" in r.clarifying_question.lower() or "aic" in r.clarifying_question.lower()
```

- [ ] **Step 2: Run the tests and verify they fail**

```bash
python3 -m pytest evals/harness/tests/test_adapters_mock.py -v
```

Expected: 3 failures (module not found).

- [ ] **Step 3: Implement `evals/harness/adapters/base.py`**

```python
"""Adapter base — every LLM driver implements this."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class RunResult:
    loaded_skills: list[str] = field(default_factory=list)
    read_paths: list[str] = field(default_factory=list)
    final_message: str = ""
    clarifying_question: str | None = None
    raw_trace: list[dict] = field(default_factory=list)


class LLMAdapter(Protocol):
    def run(self, prompt: str) -> RunResult: ...
```

- [ ] **Step 4: Implement `evals/harness/adapters/mock.py`**

```python
"""Deterministic mock adapter for harness self-tests."""
from __future__ import annotations

from dataclasses import dataclass, field

from evals.harness.adapters.base import RunResult


@dataclass
class MockRule:
    prompt_contains: str
    loaded_skills: list[str] = field(default_factory=list)
    read_paths: list[str] = field(default_factory=list)
    clarifying_question: str | None = None
    final_message: str = "[mock plan]"


class MockAdapter:
    def __init__(self, rules: list[MockRule], default_skills: list[str] | None = None):
        self.rules = rules
        self.default_skills = default_skills or []

    def run(self, prompt: str) -> RunResult:
        for rule in self.rules:
            if rule.prompt_contains.lower() in prompt.lower():
                return RunResult(
                    loaded_skills=list(rule.loaded_skills),
                    read_paths=list(rule.read_paths),
                    final_message=rule.final_message,
                    clarifying_question=rule.clarifying_question,
                )
        return RunResult(loaded_skills=list(self.default_skills))
```

- [ ] **Step 5: Run the tests**

```bash
python3 -m pytest evals/harness/tests/test_adapters_mock.py -v
```

Expected: 3 passed.

- [ ] **Step 6: Commit**

```bash
git add evals/harness/adapters/ evals/harness/tests/test_adapters_mock.py
git commit -m "feat(evals): LLMAdapter protocol + deterministic mock adapter

base.py defines the RunResult dataclass and LLMAdapter Protocol every
driver must satisfy. mock.py provides a rule-based adapter so harness
unit tests can assert scoring without hitting a real LLM API.

Refs: PLAN.md § Evaluation Layer 4 (cross-LLM)"
```

---

### Task 11: Build `evals/harness/run_eval.py` Layer 1 + Layer 2 runner (TDD)

Same content as the previous draft, with paths updated to the strategy-doc layout (`plugins/ping-identity/skills/<skill>/references/curated/...`).

**Files:**
- Create: `evals/harness/run_eval.py`
- Create: `evals/harness/tests/test_run_eval.py`

- [ ] **Step 1: Write the failing test**

`/Users/george.bafaloukas/Dev/tiger-agent-skills/evals/harness/tests/test_run_eval.py`:

```python
from pathlib import Path
import textwrap

from evals.harness.adapters.mock import MockAdapter, MockRule
from evals.harness.run_eval import score_layer_1, score_layer_2, load_prompt_set


def write(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(content).strip() + "\n")
    return p


def test_layer1_trigger_correct_when_skill_loaded(tmp_path):
    f = write(tmp_path, "ping-quickstart.yaml", """
        skill: ping-quickstart
        version: 1
        trigger_prompts:
          - id: T-01
            prompt: "where do I start with Ping?"
            expected_anchors: []
            expected_tier: curated
        non_trigger_prompts:
          - id: N-01
            prompt: "build me a journey"
            expected_skill: ping-orchestration
        ambiguous_prompts:
          - id: A-01
            prompt: "I want MFA"
            expected_clarification_keywords: ["pingone", "aic"]
    """)
    pset = load_prompt_set(f)
    adapter = MockAdapter(rules=[
        MockRule(prompt_contains="where do I start", loaded_skills=["ping-quickstart"]),
        MockRule(prompt_contains="build me a journey", loaded_skills=["ping-orchestration"]),
        MockRule(prompt_contains="I want MFA", clarifying_question="pingone aic mt or st?"),
    ])
    report = score_layer_1(pset, adapter)
    assert report.trigger_pass_rate == 1.0
    assert report.non_trigger_pass_rate == 1.0
    assert report.ambiguous_pass_rate == 1.0
    assert report.passed_overall is True


def test_layer1_trigger_fails_when_wrong_skill_loaded(tmp_path):
    f = write(tmp_path, "ping-quickstart.yaml", """
        skill: ping-quickstart
        version: 1
        trigger_prompts:
          - id: T-01
            prompt: "where do I start"
            expected_anchors: []
            expected_tier: curated
        non_trigger_prompts: []
        ambiguous_prompts: []
    """)
    pset = load_prompt_set(f)
    adapter = MockAdapter(rules=[
        MockRule(prompt_contains="where do I start", loaded_skills=["ping-foundation"]),
    ])
    report = score_layer_1(pset, adapter)
    assert report.trigger_pass_rate == 0.0
    assert report.passed_overall is False
    assert "T-01" in report.failures[0]


def test_layer2_recall_and_precision(tmp_path):
    f = write(tmp_path, "ping-orchestration.yaml", """
        skill: ping-orchestration
        version: 1
        trigger_prompts:
          - id: T-01
            prompt: "build a journey"
            expected_anchors:
              - plugins/ping-identity/skills/ping-orchestration/references/curated/journey-design-patterns.md
            expected_tier: curated
        non_trigger_prompts: []
        ambiguous_prompts: []
    """)
    pset = load_prompt_set(f)

    adapter_pass = MockAdapter(rules=[MockRule(
        prompt_contains="build a journey",
        loaded_skills=["ping-orchestration"],
        read_paths=["plugins/ping-identity/skills/ping-orchestration/references/curated/journey-design-patterns.md"],
    )])
    rep = score_layer_2(pset, adapter_pass)
    assert rep.pass_rate == 1.0

    adapter_miss = MockAdapter(rules=[MockRule(
        prompt_contains="build a journey",
        loaded_skills=["ping-orchestration"],
        read_paths=["plugins/ping-identity/skills/ping-orchestration/references/curated/davinci-flow-patterns.md"],
    )])
    rep = score_layer_2(pset, adapter_miss)
    assert rep.pass_rate == 0.0
```

- [ ] **Step 2: Run and verify the tests fail**

```bash
python3 -m pytest evals/harness/tests/test_run_eval.py -v
```

Expected: 3 failures (module not found).

- [ ] **Step 3: Implement `evals/harness/run_eval.py`**

```python
"""Layer 1 (routing) + Layer 2 (anchor selection) eval runner.

Usage:
  python -m evals.harness.run_eval --adapter mock --layer 1
  python -m evals.harness.run_eval --adapter claude --layer 2 --skill ping-orchestration
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

from evals.harness.adapters.base import LLMAdapter
from evals.harness.adapters.mock import MockAdapter, MockRule

REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPTS_DIR = REPO_ROOT / "evals" / "prompts"
RESULTS_DIR = REPO_ROOT / "evals" / "results"

LAYER_1_TRIGGER_BAR = 0.90
LAYER_1_NON_TRIGGER_BAR = 0.90
LAYER_1_AMBIGUOUS_BAR = 0.80
LAYER_2_BAR = 0.85


@dataclass
class PromptSet:
    skill: str
    trigger: list[dict]
    non_trigger: list[dict]
    ambiguous: list[dict]


@dataclass
class Layer1Report:
    skill: str
    trigger_pass_rate: float
    non_trigger_pass_rate: float
    ambiguous_pass_rate: float
    failures: list[str] = field(default_factory=list)

    @property
    def passed_overall(self) -> bool:
        return (
            self.trigger_pass_rate >= LAYER_1_TRIGGER_BAR
            and self.non_trigger_pass_rate >= LAYER_1_NON_TRIGGER_BAR
            and self.ambiguous_pass_rate >= LAYER_1_AMBIGUOUS_BAR
        )


@dataclass
class Layer2Report:
    skill: str
    pass_rate: float
    failures: list[str] = field(default_factory=list)

    @property
    def passed_overall(self) -> bool:
        return self.pass_rate >= LAYER_2_BAR


def load_prompt_set(path: Path) -> PromptSet:
    with path.open() as f:
        data = yaml.safe_load(f)
    return PromptSet(
        skill=data["skill"],
        trigger=data["trigger_prompts"],
        non_trigger=data["non_trigger_prompts"],
        ambiguous=data["ambiguous_prompts"],
    )


def _safe_rate(passed: int, total: int) -> float:
    return 1.0 if total == 0 else passed / total


def score_layer_1(pset: PromptSet, adapter: LLMAdapter) -> Layer1Report:
    failures: list[str] = []

    t_pass = 0
    for p in pset.trigger:
        result = adapter.run(p["prompt"])
        if pset.skill in result.loaded_skills:
            t_pass += 1
        else:
            failures.append(f"[trigger] {p['id']} expected {pset.skill}, got {result.loaded_skills}")

    n_pass = 0
    for p in pset.non_trigger:
        result = adapter.run(p["prompt"])
        if pset.skill not in result.loaded_skills:
            n_pass += 1
        else:
            failures.append(f"[non-trigger] {p['id']} {pset.skill} should NOT load")

    a_pass = 0
    for p in pset.ambiguous:
        result = adapter.run(p["prompt"])
        cq = (result.clarifying_question or "").lower()
        keywords = p["expected_clarification_keywords"]
        if cq and any(k.lower() in cq for k in keywords):
            a_pass += 1
        else:
            failures.append(f"[ambiguous] {p['id']} expected clarification with one of {keywords}")

    return Layer1Report(
        skill=pset.skill,
        trigger_pass_rate=_safe_rate(t_pass, len(pset.trigger)),
        non_trigger_pass_rate=_safe_rate(n_pass, len(pset.non_trigger)),
        ambiguous_pass_rate=_safe_rate(a_pass, len(pset.ambiguous)),
        failures=failures,
    )


def score_layer_2(pset: PromptSet, adapter: LLMAdapter) -> Layer2Report:
    failures: list[str] = []
    counted = 0
    passed = 0

    for p in pset.trigger:
        expected = set(p.get("expected_anchors") or [])
        if not expected:
            continue
        counted += 1
        result = adapter.run(p["prompt"])
        loaded = set(result.read_paths or [])
        recall = len(loaded & expected) / len(expected)
        precision = (len(loaded & expected) / len(loaded)) if loaded else 0.0
        if recall >= 1.0 and precision >= 0.5:
            passed += 1
        else:
            failures.append(
                f"{p['id']} expected={sorted(expected)} loaded={sorted(loaded)} "
                f"recall={recall:.2f} precision={precision:.2f}"
            )

    return Layer2Report(skill=pset.skill, pass_rate=_safe_rate(passed, counted), failures=failures)


def _build_adapter(name: str) -> LLMAdapter:
    if name == "mock":
        rules = []
        for prompt_file in sorted(PROMPTS_DIR.glob("*.yaml")):
            pset = load_prompt_set(prompt_file)
            for p in pset.trigger:
                rules.append(MockRule(
                    prompt_contains=p["prompt"][:30],
                    loaded_skills=[pset.skill],
                    read_paths=p.get("expected_anchors") or [],
                ))
            for p in pset.ambiguous:
                rules.append(MockRule(
                    prompt_contains=p["prompt"][:30],
                    clarifying_question=" ".join(p["expected_clarification_keywords"]),
                ))
        return MockAdapter(rules=rules)
    if name == "claude":
        from evals.harness.adapters.claude import ClaudeAdapter
        return ClaudeAdapter()
    raise SystemExit(f"unknown adapter: {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", default="mock", choices=["mock", "claude"])
    parser.add_argument("--layer", type=int, choices=[1, 2], default=1)
    parser.add_argument("--skill", default=None)
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()

    adapter = _build_adapter(args.adapter)
    files = sorted(PROMPTS_DIR.glob("*.yaml"))
    if args.skill:
        files = [f for f in files if f.stem == args.skill]

    all_pass = True
    out: dict[str, dict] = {}

    for f in files:
        pset = load_prompt_set(f)
        if args.layer == 1:
            r = score_layer_1(pset, adapter)
            print(f"[L1] {pset.skill}  trigger={r.trigger_pass_rate:.0%}  "
                  f"non_trigger={r.non_trigger_pass_rate:.0%}  ambiguous={r.ambiguous_pass_rate:.0%}  "
                  f"{'PASS' if r.passed_overall else 'FAIL'}")
            for line in r.failures:
                print(f"     {line}")
            all_pass = all_pass and r.passed_overall
            out[pset.skill] = {
                "layer": 1,
                "trigger": r.trigger_pass_rate,
                "non_trigger": r.non_trigger_pass_rate,
                "ambiguous": r.ambiguous_pass_rate,
                "passed": r.passed_overall,
            }
        else:
            r = score_layer_2(pset, adapter)
            print(f"[L2] {pset.skill}  pass_rate={r.pass_rate:.0%}  "
                  f"{'PASS' if r.passed_overall else 'FAIL'}")
            for line in r.failures:
                print(f"     {line}")
            all_pass = all_pass and r.passed_overall
            out[pset.skill] = {"layer": 2, "pass_rate": r.pass_rate, "passed": r.passed_overall}

    if args.write_results:
        day = RESULTS_DIR / date.today().isoformat()
        day.mkdir(parents=True, exist_ok=True)
        (day / f"{args.adapter}.layer{args.layer}.json").write_text(json.dumps(out, indent=2))

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run all harness unit tests**

```bash
python3 -m pytest evals/harness/tests/ -v
```

Expected: all 11 tests pass.

- [ ] **Step 5: Run the harness end-to-end with the mock adapter**

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills
python3 -m evals.harness.run_eval --adapter mock --layer 1
python3 -m evals.harness.run_eval --adapter mock --layer 2
```

Expected: prints `[L1] <skill> ... PASS` and `[L2] <skill> ... PASS` for each of the 6 skills, exits 0.

- [ ] **Step 6: Commit**

```bash
git add evals/harness/run_eval.py evals/harness/tests/test_run_eval.py
git commit -m "feat(evals): Layer 1 + Layer 2 runner with mock-adapter end-to-end

run_eval.py loads evals/prompts/*.yaml, drives an LLMAdapter (mock or
claude), and scores routing accuracy (Layer 1) or anchor selection
(Layer 2) against the bars in evals/scorecards/. Three pytest cases
cover trigger pass, trigger fail, and Layer 2 recall/precision. Mock
adapter makes the harness self-testing without API budget.

Run:
  python -m evals.harness.run_eval --adapter mock --layer 1
  python -m evals.harness.run_eval --adapter mock --layer 2

Refs: PLAN.md § Evaluation Layers 1 and 2"
```

---

### Task 12: Stub the Layer 3 (judge) and Layer 4 (cross-LLM) drivers

**Files:**
- Create: `evals/harness/judge_plans.py`
- Create: `evals/harness/cross_llm.py`
- Create: `evals/harness/adapters/claude.py` (stub)

- [ ] **Step 1: Write `evals/harness/adapters/claude.py`** (stub)

```python
"""Claude (Anthropic) adapter — Phase 1 implementation.

Phase 0 ships this as a stub so `--adapter claude` exits with a clear,
actionable message rather than an ImportError.
"""
from __future__ import annotations

import os

from evals.harness.adapters.base import RunResult


class ClaudeAdapter:
    def __init__(self) -> None:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise SystemExit(
                "ANTHROPIC_API_KEY not set. Phase 1 wires real Claude calls — "
                "for now the mock adapter is the only fully implemented driver."
            )
        raise SystemExit(
            "ClaudeAdapter is a Phase 0 stub. Phase 1 implements: "
            "register skills/* as available skills, capture Skill() and Read() "
            "tool calls, return RunResult."
        )

    def run(self, prompt: str) -> RunResult:
        raise NotImplementedError
```

- [ ] **Step 2: Write `evals/harness/judge_plans.py`** (Layer 3 stub)

```python
"""Layer 3 — Plan quality eval (LLM-as-judge).

Phase 0: parses prompt sets and golden plans, prints what it WOULD send
to the judge. Phase 1: wires in actual judge calls.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPTS_DIR = REPO_ROOT / "evals" / "prompts"
GOLDEN_DIR = REPO_ROOT / "evals" / "golden"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--judge", default="claude", choices=["claude", "codex", "gemini"])
    args = parser.parse_args()

    pf = PROMPTS_DIR / f"{args.skill}.yaml"
    if not pf.exists():
        print(f"no prompt set for {args.skill}", file=sys.stderr)
        return 1

    pset = yaml.safe_load(pf.read_text())
    gdir = GOLDEN_DIR / args.skill
    if not gdir.exists():
        print(f"[stub] no goldens at {gdir} — Phase 1 authors them. Skipping.")
        return 0

    for prompt in pset["trigger_prompts"]:
        gp = gdir / f"{prompt['id']}.md"
        if not gp.exists():
            print(f"[skip] {prompt['id']} — no golden")
            continue
        print(f"[would-judge] skill={args.skill} prompt={prompt['id']} judge={args.judge} "
              f"golden_chars={len(gp.read_text())}")

    print("\n[stub] Phase 1 wires the judge LLM call. See evals/scorecards/plan-quality-eval.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Write `evals/harness/cross_llm.py`** (Layer 4 stub)

```python
"""Layer 4 — Cross-LLM consistency.

Phase 0 stub: lists what would be run. Phase 1 wires in real adapters.
"""
from __future__ import annotations

import argparse
import sys

LLMS = ["claude", "codex", "gemini"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--layer", type=int, choices=[1, 3], default=1)
    args = parser.parse_args()

    print(f"[stub] cross-LLM Layer {args.layer} run plan:")
    for llm in LLMS:
        print(f"  - {llm}: would call run_eval.py / judge_plans.py with --adapter {llm}")
    print("\n[stub] Phase 1 wires real adapters.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Smoke-run the stubs**

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills
python3 -m evals.harness.judge_plans --skill ping-orchestration
python3 -m evals.harness.cross_llm --layer 1
```

Expected: both print `[stub]` lines and exit 0.

- [ ] **Step 5: Commit**

```bash
git add evals/harness/judge_plans.py evals/harness/cross_llm.py evals/harness/adapters/claude.py
git commit -m "feat(evals): scaffold Layer 3 judge and Layer 4 cross-LLM stubs

Both runnable, both exit 0 with [stub] messages so Phase 1 can wire in
real LLM calls without churning file layout. ClaudeAdapter raises a
clear SystemExit until Phase 1 implements it.

Refs: PLAN.md § Evaluation Layers 3 and 4"
```

---

### Task 13: Author `evals/README.md` and run the Phase 0 exit-criteria smoke check

**Files:**
- Create: `evals/README.md`

- [ ] **Step 1: Author `evals/README.md`** (same content as previous draft, with paths updated to the strategy-doc layout)

```markdown
# Skill Evaluation Harness

Measures skill accuracy across 5 layers. Layer 1 + Layer 2 are runnable
in Phase 0; Layer 3, 4, 5 are scaffolded and wired up in Phase 1+.

Strategy doc § 2.7: "Testing and eval frameworks are a progressive
evolution, not a day-1 requirement. We keep the investment low."

## What gets measured

| Layer | Question | Bar | When |
|---|---|---|---|
| 1 — Routing | Right umbrella skill activated? | 90% trigger / 90% non-trigger / 80% ambiguous | Every PR (Phase 3+) |
| 2 — Anchors | Right curated files loaded? | 85% per-prompt pass | Every PR (Phase 3+) |
| 3 — Plan quality | Plan correct, complete, concrete, right tier? | mean ≥ 4.0; no dim < 3 | Weekly + pre-release |
| 4 — Cross-LLM | Acceptable on Codex, Gemini? | ≥70% Layer 1 (warn); ≥60% (block at launch) | Weekly |
| 5 — E2E | Sandbox tenant actually works? | 95% rolling 7-day | Nightly (Phase S) |

## Layout

```
evals/
  prompts/<skill>.yaml          # one prompt set per skill (validated by schema)
  schemas/prompt-set.schema.json
  golden/<skill>/<id>.md        # golden plans for Layer 3 (Phase 1+)
  scorecards/                   # rubric for each layer
  harness/
    validate_prompts.py         # YAML schema validator
    run_eval.py                 # Layer 1 + Layer 2 runner
    judge_plans.py              # Layer 3 — LLM-as-judge (stub in Phase 0)
    cross_llm.py                # Layer 4 — multi-LLM (stub in Phase 0)
    adapters/                   # mock + claude (+ codex, gemini in Phase 1)
    tests/                      # pytest covering the harness itself
  results/<YYYY-MM-DD>/<llm>.layer{1,2,3}.json
```

## Run

```bash
python3 -m pip install -r evals/harness/requirements.txt
python3 -m evals.harness.validate_prompts
python3 -m evals.harness.run_eval --adapter mock --layer 1
python3 -m evals.harness.run_eval --adapter mock --layer 2
python3 -m pytest evals/harness/tests/ -v
```

## Authoring checklist (every skill PR from Phase 1+)

A skill PR is rejected by CI (Phase 3+) unless it includes:

1. `evals/prompts/<skill>.yaml` — ≥10 trigger / ≥5 non-trigger / ≥3 ambiguous prompts; schema-valid.
2. `evals/golden/<skill>/<id>.md` — ≥3 golden plans for Layer 3.
3. A passing local Layer 1 + Layer 2 run against the Claude adapter.
```

- [ ] **Step 2: Run the full Phase 0 smoke check**

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills
python3 -m evals.harness.validate_prompts
python3 -m evals.harness.run_eval --adapter mock --layer 1
python3 -m evals.harness.run_eval --adapter mock --layer 2
python3 -m pytest evals/harness/tests/ -v
```

All four commands must exit 0.

- [ ] **Step 3: Verify Phase 0 exit criteria from PLAN.md**

```bash
cd /Users/george.bafaloukas/Dev/tiger-agent-skills

# 1. Top-level dirs exist
[ -d commands ] && [ -d rules ] && [ -d evals ] && echo "OK: top-level dirs"

# 2. Six umbrella skill directories exist with the canonical tier set
for s in ping-quickstart ping-foundation ping-orchestration ping-universal-services ping-app-integration ping-identity-for-ai; do
  base=plugins/ping-identity/skills/$s
  [ -f $base/SKILL.md ] || echo "MISSING: $base/SKILL.md"
  [ -f $base/ping-marketplace.json ] || echo "MISSING: $base/ping-marketplace.json"
  for tier in curated generated runtime; do
    [ -d $base/references/$tier ] || echo "MISSING: $base/references/$tier"
  done
  [ -f $base/references/runtime/docs-mcp-routing.md ] || echo "MISSING: $base/references/runtime/docs-mcp-routing.md"
done

# 3. Multi-IDE manifests
[ -f .claude-plugin/marketplace.json ] && [ -f .claude-plugin/plugin.json ] && echo "OK: claude-plugin"
[ -f .cursor-plugin/marketplace.json ] && [ -f .cursor-plugin/plugin.json ] && echo "OK: cursor-plugin"
[ -f plugins/ping-identity/.claude-plugin/plugin.json ] && echo "OK: inner plugin manifest"

# 4. .well-known and .mdc rule
[ -f .well-known/agent-skills/index.json ] && echo "OK: well-known"
[ -f rules/ping-identity.mdc ] && echo "OK: cursor mdc rule"

# 5. runtime-selection.md
[ -f rules/runtime-selection.md ] && echo "OK: runtime-selection rule"
```

Expected: every relevant line prints `OK: ...` and no `MISSING` line appears.

- [ ] **Step 4: Commit**

```bash
git add evals/README.md
git commit -m "docs: evals/README.md and Phase 0 smoke check passes

Documents the 5-layer eval framework, how to run each layer locally,
and the per-PR authoring checklist (≥10/≥5/≥3 prompts + ≥3 goldens)
that becomes a CI gate in Phase 3.

Phase 0 smoke check passes:
- validate_prompts: all 6 prompt YAMLs valid against schema
- run_eval --layer 1 --adapter mock: PASS for all 6 skills
- run_eval --layer 2 --adapter mock: PASS
- pytest evals/harness/tests/: 11 passed

Phase 0 exit criteria from PLAN.md all green.

Refs: PLAN.md Phase 0 exit criterion"
```

---

## Phase 0 done — what Phase 1 inherits

After all 13 tasks land:

- 6 umbrella skill directories with the canonical `references/{curated,generated,runtime}/` tier set per strategy doc § 6. Three live skills (`ping-quickstart`, `ping-foundation`, `ping-orchestration`) keep all their content; three new skills (`ping-universal-services`, `ping-app-integration`, `ping-identity-for-ai`) have empty SKILL.md scaffolds, marketplace metadata, and runtime stubs.
- `rules/runtime-selection.md` is the canonical decision rule for sandbox-vs-production runtime AND for the strategy-doc § 0 tier-discipline rule (curated → generated → docs-mcp).
- A runnable Layer 1 + Layer 2 eval harness with 6 prompt sets and 11 passing pytest cases. Phase 1 wires in the real Claude adapter and the harness becomes a CI gate in Phase 3.
- Multi-IDE manifests in `.claude-plugin/` AND `.cursor-plugin/` (Cloudflare parity), plus the inner `plugins/ping-identity/.claude-plugin/plugin.json` required by strategy doc § 5.
- `rules/ping-identity.mdc` for Cursor parity with Cloudflare's `rules/workers.mdc`.
- `.well-known/agent-skills/index.json` stub ready for Phase 3 to populate.

The next phase opens with: "Author `ping-universal-services/SKILL.md` body following the routing decision tree per strategy doc § 7, then run `python -m evals.harness.run_eval --adapter claude --layer 1 --skill ping-universal-services` and iterate until ≥90% trigger pass."
