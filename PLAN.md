# Delivery Plan — Agent Skills v1 (6 Umbrella Skills, Cloudflare-Inspired)

> Companion to [SUMMARY.md](SUMMARY.md). v1 ships the 6 umbrella skills defined in the [Ping Identity Agent Skill Strategy doc](https://docs.google.com/document/d/1ts57b476DNIEduopqq5fSwyJx5RZSWL72UVGj_EVRYk) § 4 "In Practice". Layout is **Cloudflare-inspired** — `commands/`, `rules/`, `skills/`, `.claude-plugin/`, `.cursor-plugin/` — extended for Ping with a 3-tier reference model (`curated/` + `generated/` + `runtime/`) and a lightweight eval harness. Helix is the production runtime; MCPs are out of scope for v1.

---

## North star

A user types something like _"I want to add MFA to my mobile banking app"_ and the skill set:

1. **Orients** — `ping-quickstart` detects the platform and routes to the right umbrella skill.
2. **Plans** — the umbrella skill (typically `ping-foundation` + `ping-orchestration` + `ping-app-integration`) loads the relevant curated anchor and produces a concrete configure-and-build plan.
3. **(Stretch) Executes** — Helix conversation APIs consume the plan and apply it to a tenant via product-specific Helix tools, behind policy/approval gates.

---

## Skill set for v1 — 6 umbrella skills

This is the **canonical set from the strategy doc § 4**. Three are already live in the repo (`ping-quickstart`, `ping-foundation`, `ping-orchestration`); three are planned (`ping-universal-services`, `ping-app-integration`, `ping-identity-for-ai`).

| Skill | Status | Scope (per strategy doc § 4) |
|---|---|---|
| `ping-quickstart` | Live | Front door. Product-family selection, cloud vs. on-prem routing, workforce vs. customer identity orientation, common starting paths, key prerequisites, and links into the other five umbrella skills. |
| `ping-foundation` | Live | Tenant and environment setup, app setup, directories, policy, branding, admin basics across PingOne MT, PingOne ST (AIC), PingFederate, PingAccess, PingDirectory, PingID. |
| `ping-orchestration` | Live | DaVinci flows, AIC and PingAM journey patterns, flow composition, decisioning patterns, handoff to app integration, troubleshooting for orchestration paths. |
| `ping-universal-services` | **Live (v1)** | Protect, Verify, Credentials, and other shared service references; cross-product service usage; service selection guidance. |
| `ping-app-integration` | **Live (v1)** | Android, iOS, React SDK references; web app integration; mobile and browser auth flows; orchestration SDK references; on-prem app-side integration when the primary task is implementation. |
| `ping-identity-for-ai` | **Live (v1)** | Identity for AI solution references, Verified Trust references, workforce helpdesk AI use cases, agent security patterns, AI app auth patterns. |

### Decision rule for adding a 7th skill (from strategy doc)

A new skill is created only if it has **all four** of:
- A distinct trigger
- A distinct user outcome
- Enough depth that routing through references materially improves results
- Low overlap with an existing umbrella

Otherwise, add it as a reference pack inside an existing umbrella, not a new skill.

### Out of scope for v1

- On-prem-specialist umbrella (PingFederate, PingAccess, PingDirectory get tagged sub-routes inside `ping-foundation`, not their own skill).
- IGA-specific umbrella (lives as a service inside `ping-universal-services`).
- Full SDK plugin (`plugins/ping-identity-sdks/` from strategy doc § 2.3) — defer to v1.1.
- Operational use-case plugin (`plugins/ping-identity-ops/`) — defer to v1.1.
- MCP-based execution path — re-evaluate post-v1 when AIC/DaVinci MCP servers stabilize.

---

## Routing taxonomy (consistent across every skill)

Every `SKILL.md` routes in this order, per strategy doc § 4:

1. **What are they trying to do?** — setup, configure, orchestrate, integrate, secure, troubleshoot.
2. **Which platform family applies?**
   - PingOne MT (multi-tenant)
   - PingOne ST / AIC (single-tenant)
   - Ping Software Suite (PingFederate, PingAccess, PingDirectory, PingID, PingAM)
   - Cross-platform / Universal Services
3. **Which exact product or service applies?**
4. **Which reference tier should be used?** — curated anchor → generated shortlist → live Docs MCP.

---

## Helix runtime

Helix is the production execution backbone but is **NOT a skill** in v1. Per the strategy doc, "MCP-based execution" is deferred and Helix is documented inside each skill's `references/runtime/` tier as the production-bound path. The decision rule for sandbox-vs-production runtime lives in `rules/runtime-selection.md` and is referenced from each skill's `references/runtime/docs-mcp-routing.md`.

When/if Helix execution becomes a first-class umbrella skill (v1.1+), it will pass the four-criteria decision rule above. For v1 it stays as a **runtime tier**, not a skill.

---

## Repo layout (Cloudflare-inspired, Ping-extended)

This layout follows Cloudflare's structure for the public-facing surface (`.claude-plugin/`, `.cursor-plugin/`, `commands/`, `rules/`, `skills/`) and extends it with the Ping-specific reference tier model and eval harness. See [strategy doc § 5 "Recommended repo structure"](https://docs.google.com/document/d/1ts57b476DNIEduopqq5fSwyJx5RZSWL72UVGj_EVRYk).

```
.claude-plugin/
  plugin.json                          # Claude Code plugin manifest
  marketplace.json                     # Claude Code marketplace listing
.cursor-plugin/
  marketplace.json                     # Cursor marketplace listing
.well-known/
  agent-skills/
    index.json                         # Cloudflare Agent Skills Discovery RFC v0.2.0 (Ping addition)
.github/
  workflows/                           # CI: validate-skills, build-reference-manifests, sync-doc-metadata, run-evals
commands/                              # Cloudflare-style slash commands (stretch)
  configure-mfa.md
  scaffold-app-integration.md
  build-davinci-flow.md
rules/                                 # Top-level rules referenced by all skills
  authoring-rules.md                   # Frontmatter contract, body length, naming
  routing-rules.md                     # Skill selection precedence
  runtime-selection.md                 # Sandbox-vs-production decision rule
  workers.mdc                          # Cursor-style .mdc rule (Cloudflare parity)
shared/                                # Ping-specific cross-skill assets (NOT in Cloudflare repo)
  taxonomies/
    platform-families.md
    capability-map.md
    service-map.md
    routing-rules.md
  schemas/
    doc-frontmatter-schema.json
    reference-manifest-schema.json
  templates/
    SKILL.template.md
    curated-reference.template.md
  generated/
    global-doc-catalog.json
    docs-by-platform.json
plugins/
  ping-identity/
    .claude-plugin/plugin.json
    skills/                            # The 6 umbrella skills
      ping-quickstart/
      ping-foundation/
      ping-orchestration/
      ping-universal-services/
      ping-app-integration/
      ping-identity-for-ai/
evals/                                 # Ping addition — eval harness (see § Evaluation)
  prompts/
  golden/
  schemas/
  scorecards/
  harness/
  results/
ping-marketplace.json                  # Ping Marketplace metadata for the entire repo
CONTRIBUTING.md
README.md
LICENSE
```

### Per-skill internal structure

Every skill follows this exact shape (per strategy doc § 6 "Internal structure for each skill"):

```
plugins/ping-identity/skills/<skill-name>/
  SKILL.md                             # ≤120 lines; routing decision tree only
  ping-marketplace.json                # Marketplace metadata (icons, tags, filters)
  references/
    curated/                           # Hand-authored canonical docs (5–10 files)
    generated/                         # Capped, ranked shortlists per branch (20–50 max)
    runtime/                           # Pointers/rules for Docs MCP retrieval (no copied content)
```

### Reference tier semantics (per strategy doc § 6)

| Tier | Purpose | Size cap | Source of truth | Update mode |
|---|---|---|---|---|
| `curated/` | Hand-picked canonical playbooks; the agent loads 1–3 per task | 5–10 docs | This repo | Manual |
| `generated/` | Capped top-N shortlist per platform/product branch | 20–50 per branch | Generated from docs frontmatter | CI on docs publish |
| `runtime/` | Routing rules and pointers for live Docs MCP retrieval | No copied content | Docs MCP server | Live |

---

## Phase 0 — Restructure (May 30) ✅ COMPLETE

**Goal:** Repo skeleton matches the Cloudflare-inspired layout, the 6 umbrella skills exist as scaffolds, the three live skills are reorganized into the canonical reference tier shape, and the eval harness is runnable.

### Steps

1. Create `commands/`, `rules/`, `evals/` top-level directories. Add `.well-known/agent-skills/index.json` stub. Add Cursor `.mdc` rule under `rules/` for Cloudflare parity.
2. Verify `.claude-plugin/marketplace.json` and `.cursor-plugin/marketplace.json` both exist and point at `plugins/ping-identity/`. Author `.claude-plugin/plugin.json` and `.cursor-plugin/marketplace.json` if missing.
3. Reorganize the three live skills (`ping-quickstart`, `ping-foundation`, `ping-orchestration`) so each has the full `references/{curated,generated,runtime}/` tier set per strategy § 6. Existing curated content is already in `references/curated/`; add `references/runtime/docs-mcp-routing.md` stubs for each.
4. Scaffold the three planned skills (`ping-universal-services`, `ping-app-integration`, `ping-identity-for-ai`) with empty SKILL.md (≤120 lines, agentskills.io frontmatter), `ping-marketplace.json`, and the `references/{curated,generated,runtime}/` directory tree.
5. Author `rules/authoring-rules.md` (port from `shared/templates/AUTHORING-RULES.md`), `rules/routing-rules.md` (port from `shared/taxonomies/routing-rules.md`), and `rules/runtime-selection.md` (NEW — sandbox-vs-production decision rule).
6. Stand up the eval harness: prompt-set JSON Schema, validator, Layer 1 + Layer 2 runner, mock adapter, pytest coverage, all six skills with prompt sets at the agreed minimums.

**Exit criterion:** Six umbrella skill directories exist with the full per-skill tree; `python -m evals.harness.validate_prompts` and `python -m evals.harness.run_eval --adapter mock --layer 1` both exit 0; both `.claude-plugin/` and `.cursor-plugin/` manifests resolve.

> **Status (2026-06-01):** Exit criterion met. All 6 skill scaffolds exist; mock eval exits 0; both plugin manifests present.

---

## Phase 1 — Author the three planned umbrella skills (May 31 – June 1) ✅ COMPLETE

**Goal:** `ping-universal-services`, `ping-app-integration`, and `ping-identity-for-ai` ship at orientation depth — each with a working SKILL.md decision tree and ≥3 curated anchors.

### Steps

1. **`ping-universal-services`** — curated anchors per strategy doc § 7:
   - `universal-services-overview.md`
   - `choosing-the-right-service.md`
   - `service-invocation-patterns.md`
   - `cross-platform-service-usage.md`
   - Generated branches: `protect/`, `verify/`, `credentials/`, `sso/`, `iga/` (top-15 stubs each).
2. **`ping-app-integration`** — curated anchors per strategy doc § 7:
   - `app-integration-overview.md`
   - `mobile-integration-basics.md`
   - `web-integration-basics.md`
   - `integration-troubleshooting-basics.md`
   - Generated branches: `mobile/`, `web/`, `orchestration-sdks/`, `on-prem-integration/` (top-20 stubs each).
3. **`ping-identity-for-ai`** — curated anchors per strategy doc § 7:
   - `identity-for-ai-overview.md`
   - `verified-trust-overview.md`
   - `agent-security-patterns.md`
   - `workforce-helpdesk-ai.md`
4. Each skill ships ≥10 trigger / ≥5 non-trigger / ≥3 ambiguous prompts in `evals/prompts/<skill>.yaml`.
5. Cross-link each new skill from `ping-quickstart/SKILL.md` and from `rules/routing-rules.md`.
6. Run Layer 1 eval against the Claude adapter; iterate until all 6 skills pass (90% trigger / 90% non-trigger / 80% ambiguous).

**Exit criterion:** End-to-end test passes — free-text intent ("KYC during registration on my React app") routes correctly through `ping-quickstart` → `ping-orchestration` + `ping-universal-services` + `ping-app-integration`, returns a curated plan citing the right anchors.

> **Status (2026-06-01):** Exit criterion met. All 12 curated anchors authored (4 per new skill). All 6 skills pass Layer 1 eval at ≥90/100/80% on the Claude Bedrock adapter (`evals/results/2026-06-01/claude.layer1.json`). Also completed: full repo audit (119 issues found and fixed), `ClaudeAdapter` implemented via Bedrock, `validate_prompts` and `run_eval` composition-file handling fixed. The `ping-foundation` T-07 and `ping-quickstart` T-09 prompts sit exactly at the 90% floor — intentional known-good edge cases documented in eval results.

**Additional work completed beyond Phase 1 plan:**
- Full verify/review/optimize pass across all 6 skills (119 issues fixed in 43 files): frontmatter gaps, routing placeholders, line-count violations, UI navigation language, missing Scope sections, broken index.json paths
- `ClaudeAdapter` implemented using Bedrock (`eu.anthropic.claude-sonnet-4-6`); auto-detects `CLAUDE_CODE_USE_BEDROCK` env flag
- `evals/prompts/composition.yaml` created (5 cross-skill routing test cases)
- `evals/harness/validate_prompts.py` and `run_eval.py` updated to skip composition file correctly

---

## Phase 2 — Curated content depth + reference manifests (June 2 – June 3) ✅ COMPLETE

**Goal:** Generated shortlists land in every skill branch; curated anchors are upgraded from orientation depth to task-completing depth where Phase 1 left gaps.

### Steps

1. Author `shared/schemas/reference-manifest-schema.json` (already present — verify it covers the v1 generated tier).
2. Build `.github/workflows/build-reference-manifests.yml` — scans frontmatter, generates `top-N.json` per branch.
3. Run the manifest builder against the existing docs catalog; commit the generated `top-N.json` files to each skill's `references/generated/<branch>/` subdir.
4. Upgrade weak curated anchors flagged by Phase 1 evals (any anchor scoring <4.0 on Layer 3 plan-quality).
5. Each skill: ≥3 trigger prompts and ≥2 non-trigger prompts in `evals/prompts/`. Layer 1 + Layer 2 must pass for all 6 skills.

**Exit criterion:** All 6 skills pass Layer 1 (≥90/90/80%) and Layer 2 (≥85% per-prompt anchor selection); generated shortlists exist for every documented branch; routing eval against a 25-prompt benchmark scores ≥80/100.

> **Status (2026-06-03):** Exit criterion met. All 6 skills pass Layer 1 (100/100/100 except ping-quickstart at 90%). Generated shortlists built for all skill branches (14 manifests across 6 skills). Builder script at `scripts/build_reference_manifests.py`; CI workflow at `.github/workflows/build-reference-manifests.yml`. All curated anchors upgraded to task-completing depth during Phase 1 continuation work.

---

## Phase 3 — Repo + CI hardening (June 4) ⏳ NEXT

### Steps

1. `CONTRIBUTING.md`: authoring workflow, frontmatter contract, eval requirement, PR checklist.
2. CI workflows:
   - `.github/workflows/validate-skills.yml` — frontmatter schema, broken-link check, SKILL.md ≤120 lines, name-matches-directory
   - `.github/workflows/run-evals.yml` — Layer 1 + Layer 2 on every PR (blocks merge below pass bar)
   - `.github/workflows/build-reference-manifests.yml` — already in Phase 2
3. Multi-IDE manifests verified: `.claude-plugin/`, `.cursor-plugin/`, `.well-known/agent-skills/index.json`. README install table for OpenCode / Codex / Gemini CLI.
4. `npx skills-ref validate` scaffold (stub script) referenced from CONTRIBUTING.md.

**Exit criterion:** A clean PR fails CI when frontmatter is malformed, a routing table points to a missing file, a SKILL.md exceeds 120 lines, or eval scores drop below pass bar.

---

## Phase 4 — Public launch

### Steps

1. Strip all internal-only references: Glean MCP, Polaris, internal Slack pointers, internal tenant URLs.
2. ~~Repo rename~~ — repo is already at `pingidentity/agent-plugins`. ✅
3. Flip visibility public; verify `gh repo view` is clean.
4. Smoke test from a fresh machine: `/plugin marketplace add pingidentity/agent-plugins`, ask 5 sample router questions, confirm correct routing.

**Exit criterion:** Public repo installable in <2 minutes from any supported IDE.

---

## Phase 5 — Distribution

### Steps

1. Submit `ping-marketplace.json` for each skill to Ping Marketplace.
2. Publish to AI Marketplaces: Claude Code, Cursor, OpenCode (`npx skills add`), Codex, Gemini CLI.
3. Update Build with AI Docs: add "Agent Skills" section linking to the public repo.
4. Publish blog post: strategy + technical walkthrough + install instructions + 1 demo (free-text → quickstart → product skill → curated plan).

**Exit criterion:** A developer reading the blog can install + ask a question + get to a curated anchor in <2 minutes.

---

## Phase S (Stretch) — Executable build commands

Only attempt if Phases 0–3 land on time.

### Steps

1. Author `commands/configure-mfa.md`, `commands/scaffold-app-integration.md`, `commands/build-davinci-flow.md` per Cloudflare's command file structure (frontmatter `description`, `argument-hint`, `allowed-tools`).
2. Each command supports `--dry-run` (default) and `--apply`. Dry run prints the plan; apply opens a Helix conversation, posts the plan, polls, and presents the diff for approval before committing.
3. End-to-end test against a sandbox tenant.

**Exit criterion:** Each command produces a working artifact in a sandbox tenant from a single user prompt.

---

## Orchestration model

### Skill activation order at runtime

1. `ping-quickstart` activates on any unstructured user intent where platform is unknown.
2. Quickstart asks ≤3 clarifying questions; resolves to {umbrella skill, platform family, exact product/service}.
3. The umbrella skill loads.
4. Inside the skill, routing logic selects the platform branch and loads 1–3 curated anchors. If insufficient, falls back to generated shortlist; if still insufficient, surgical Docs MCP query.
5. (Stretch) User invokes the matching `/ping:` command which executes the plan via Helix.

### Cross-skill composition

Strategy doc § 4 explicitly notes that "complete Ping Identity solutions almost always span more than one skill." Each `SKILL.md` MUST include a "Multi-skill use cases" section showing the typical composition (already present in the live `ping-quickstart` and `ping-foundation` skills — extend pattern to all 6).

### Routing rule precedence (`rules/routing-rules.md`)

1. If the user asks "what should I use?" or "where do I start?", route to `ping-quickstart`.
2. If the user names a platform directly ("I'm using AIC"), skip quickstart, route to the most specific umbrella skill for the named task.
3. If the user describes a workflow without naming a product, route to `ping-quickstart`.
4. Cross-skill composition is the norm, not an exception — `SKILL.md` "Multi-skill use cases" sections teach this.

---

## Evaluation

Per strategy doc § 2.7: "Testing and eval frameworks are a progressive evolution, not a day-1 requirement. We keep the investment low." Phase 0 ships a runnable Layer 1 + Layer 2 harness; Phase 3 makes it a CI gate; Layers 3–5 land progressively.

Eval is the gate that turns "we shipped skills" into "we shipped skills that work." Every skill must pass Layer 1 + Layer 2 before merge from Phase 3 onward.

### Five evaluation layers

#### Layer 1 — Routing accuracy (mandatory, every PR from Phase 3)

**What:** Does the agent send the right user prompt to the right umbrella skill?

**How:**
- Each skill ships `evals/prompts/<skill>.yaml` with:
  - ≥10 trigger prompts (should activate this skill)
  - ≥5 non-trigger prompts (should NOT activate this skill — they belong elsewhere)
  - ≥3 ambiguous prompts (require clarification before routing)
- Harness: a thin Python script that runs each prompt through Claude / Codex / Gemini in turn and records which skill(s) the agent loaded.
- Score: % of trigger prompts correctly activated, % of non-trigger correctly rejected, % of ambiguous prompts that produced a clarifying question.
- Pass bar: 90% trigger, 90% non-trigger, 80% ambiguous-handled.

**Why:** Routing failures are the most expensive — a wrong skill produces a wrong plan.

#### Layer 2 — Curated anchor selection (mandatory, every PR from Phase 3)

**What:** Within an activated skill, does the agent load the right curated anchor for the specific intent?

**How:**
- For each curated anchor, define ≥3 prompts that should cause that anchor to be read.
- Harness inspects the agent's tool-call log: did `Read(<anchor-path>)` happen?
- Pass bar: 85% per-prompt pass (recall ≥ 1.0 AND precision ≥ 0.5 against the prompt's `expected_anchors`).

**Why:** Loading the wrong anchor wastes tokens and produces irrelevant content.

#### Layer 3 — Plan quality (LLM-as-judge, weekly)

**What:** When a skill produces a plan, is it correct, complete, and concrete?

**How:**
- Define 20 representative prompts per skill, each with a hand-authored "golden plan" (reference answer).
- Run the prompt through the skill set; capture the produced plan.
- LLM-as-judge: ask a DIFFERENT model than the one being evaluated to score on:
  - **Correctness** — no factual errors (1–5)
  - **Completeness** — covers all required steps (1–5)
  - **Concreteness** — names specific products, tools, fields (1–5)
  - **Runtime correctness** — picks the right tier (curated / generated / docs MCP) for the prompt's context (1–5)
- Pass bar: average ≥4.0 across all dimensions; no individual prompt scoring <3 on any dimension.

**Why:** Routing + anchor selection can be right while the actual answer is still vague or wrong.

#### Layer 4 — Cross-LLM consistency (weekly)

**What:** Do skills behave acceptably across Claude, Codex, and Gemini? The strategy doc explicitly accepts behavioral drift but we still need a floor.

**How:**
- Run Layer 1 + Layer 3 evals against ≥3 LLMs.
- Track per-LLM scores in `evals/results/<date>/<llm>.json`.
- Acceptance: any LLM scoring <70% on Layer 1 triggers a documented "known limitation" entry in README; any LLM scoring <60% blocks v1.

**Why:** Strategy targets multiple IDEs; we need data, not vibes, on which combinations work.

#### Layer 5 — End-to-end task completion (Phase S only)

**What:** When a user invokes `/ping:configure-mfa`, does the resulting tenant actually have a working MFA configuration?

**How:** Sandbox tenant + scripted assertion; nightly run; pass bar 95% rolling 7-day.

### Eval directory layout

```
evals/
  prompts/
    ping-quickstart.yaml           # trigger / non-trigger / ambiguous
    ping-foundation.yaml
    ping-orchestration.yaml
    ping-universal-services.yaml
    ping-app-integration.yaml
    ping-identity-for-ai.yaml
  golden/
    ping-foundation/
      add-mfa-pingone-mt.md        # golden plan
      ...
  schemas/
    prompt-set.schema.json
  scorecards/
    routing-eval.md                # Layer 1
    anchor-selection-eval.md       # Layer 2
    plan-quality-eval.md           # Layer 3
  harness/
    run_eval.py                    # Layer 1 + Layer 2
    judge_plans.py                 # Layer 3 (Phase 1+)
    cross_llm.py                   # Layer 4 (Phase 1+)
    validate_prompts.py            # schema validator
    adapters/                      # mock + claude (+ codex, gemini in Phase 1)
    tests/                         # pytest covering the harness itself
  results/
    2026-06-01/
      claude.json
      gemini.json
      codex.json
```

### Eval execution schedule

| Layer | When |
|---|---|
| 1 — Routing | Every PR via CI from Phase 3; blocks merge if <pass bar |
| 2 — Anchor selection | Every PR via CI from Phase 3 |
| 3 — Plan quality | Weekly + before any release |
| 4 — Cross-LLM | Weekly |
| 5 — End-to-end | Nightly (Phase S only) |

### Authoring requirement (from Phase 1 onward)

Every new skill PR MUST include:
- `evals/prompts/<skill>.yaml` populated to spec
- ≥3 golden plans in `evals/golden/<skill>/`
- A passing local Layer 1 + Layer 2 run

CI rejects skill PRs that lack these artifacts (Phase 3+).

---

## v1.1 backlog (post-June 10)

Ordered by leverage:

1. **MCP execution path** — once AIC MCP supports unattended/headless auth and DaVinci's MCP path is decided, add MCP as a sandbox-side runtime alongside Helix.
2. **`plugins/ping-identity-sdks/`** — SDK skills as their own plugin per strategy doc § 2.3.
3. **`plugins/ping-identity-ops/`** — Operational / use-case skills per strategy doc § 2.3.
4. **More build commands** — `/ping:set-up-ciam`, `/ping:add-passwordless`, `/ping:migrate-from-forgerock`.
5. **Docs frontmatter pipeline + CI metadata sync** — automated generated shortlists from docs catalog (built in Phase 2; this is the productionization).
6. **Marketplace sync CI** — auto-publish `ping-marketplace.json` on merge.
7. **Helix-as-a-skill** — re-evaluate when Helix tooling matures and the four-criteria decision rule is met.

---

## External dependencies

### Runtime

| Dependency | Used for | Phase | Criticality |
|---|---|---|---|
| **Ping Docs site** (`docs.pingidentity.com`) | Tier-3 retrieval; primary backing for skills | All phases | Hard |
| **Docs MCP server** | Live tier-3 retrieval | Phase 2 onward | Soft (docs site is fallback) |
| **Helix conversation APIs** | Production execution (Phase S only) | Phase S | Soft for v1 |

### Specifications

| Spec | Used for | Criticality |
|---|---|---|
| agentskills.io spec | SKILL.md frontmatter | Hard |
| Cloudflare Agent Skills RFC v0.2.0 | `.well-known/agent-skills/index.json` | Hard for Phase 3 |
| Claude Code plugin marketplace format | Distribution | Hard |
| Cursor remote rules format (incl. `.mdc`) | Distribution | Hard |
| OpenCode `npx skills add` | Distribution | Soft |

### Tooling and CI

| Tool | Used for | Criticality |
|---|---|---|
| GitHub Actions | CI pipelines + eval harness execution | Hard |
| Python 3.11+ | Eval harness runtime | Hard |
| Anthropic / OpenAI / Google API access | Cross-LLM eval (Layer 4) | Hard from Phase 3 |
| JSON Schema validator (`ajv-cli`) | Frontmatter validation | Hard |
| Markdown link checker (`lychee`) | Broken-link CI gate | Hard |

### v1 hard list

Must work before going public on June 8:

1. agentskills.io frontmatter spec stable
2. Claude Code marketplace accepting submissions
3. Cursor remote rules format confirmed
4. GitHub Actions runner availability
5. `pingidentity` GitHub org admin access

---

## Critical-path risks

| Risk | Mitigation |
|---|---|
| Three planned skills authored in parallel under tight timeline | Each ships at orientation depth (3 curated anchors); use-case depth lands in v1.1. |
| Generated shortlists require docs frontmatter | Phase 2 scans existing `.md` for partial frontmatter; manual fill for canonical anchors; full automation in v1.1. |
| Eval harness blocks development | Layer 1 + 2 runnable in Phase 0 against mock adapter (no API budget); becomes CI gate only at Phase 3. |
| Cross-LLM scores diverge significantly | Layer 4 produces data, not blockers. README lists known good combinations. |
| Repo rename breaks links | Single `grep` sweep before flipping public. |

---

## Decisions needed from product

### Pre-Phase 0

1. **Scope confirmation** — confirm v1 ships exactly the 6 strategy-doc umbrella skills; defer SDK plugin and ops plugin to v1.1.
2. **Cursor `.mdc` rule** — ship one rule for parity with Cloudflare, or skip until Phase 3?
3. **Quickstart clarification depth** — confirm ≤3 questions max.

### Pre-Phase 1

4. **Docs MCP server availability** — by June 8, will the Docs MCP server be reachable from external developer environments, or do `references/runtime/docs-mcp-routing.md` files document the pattern with the public docs site as fallback?
5. **Reference manifest builder** — Phase 2 ships the CI workflow; pre-Phase 1 confirm where the docs catalog lives and whether docs frontmatter is sufficient for shortlist generation.
6. **Repo rename timing** — June 8 (planned) or earlier.

### Eval-related

7. **LLM API budget** — Layer 4 cross-LLM evals require Claude + Codex + Gemini API access. Confirm budget owner.
8. **Sandbox tenant for Layer 5** — confirm dedicated PingOne ST + DaVinci sandbox available for nightly e2e runs (Phase S only).
9. **Eval failure response policy** — when CI eval drops below pass bar, does the PR block, or does the system page an owner?

### Stretch goal scoping

10. **Stretch ship/no-ship** — confirm `/ping:configure-mfa`, `/ping:scaffold-app-integration`, `/ping:build-davinci-flow` are stretch, not committed.
11. **Helix coordination** — does June 10 launch align with a Helix milestone, or stand alone?
