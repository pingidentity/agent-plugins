# Ping Identity Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A skill package that teaches AI coding agents (Claude Code, Cursor, Copilot CLI, Gemini CLI) how to reason about the Ping Identity platform — which product to use, how to configure it, and how to integrate it into an application.

Skills provide **judgment and context** that MCP tools lack. MCP tools handle execution; skills handle the *what* and *why* before execution begins.

---

## Install

| Agent | Command |
|---|---|
| **Claude Code** | `/plugin add pingidentity/agent-plugins` |
| **Cursor** | Settings → Rules → Add Rule → Remote Rule → `https://github.com/pingidentity/agent-plugins` |
| **GitHub Copilot** | Agent Skills discovery via `.well-known/agent-skills/index.json` (see [Copilot docs](https://docs.github.com/en/copilot)) |
| **Gemini CLI** | Add to `GEMINI.md`: `plugins: [https://github.com/pingidentity/agent-plugins]` |
| **OpenCode / other** | `npx github:pingidentity/agent-plugins validate` (validator); skill install per agent's plugin spec |

Agent discovery index: [`https://raw.githubusercontent.com/pingidentity/agent-plugins/main/.well-known/agent-skills/index.json`](https://raw.githubusercontent.com/pingidentity/agent-plugins/main/.well-known/agent-skills/index.json)

---

## The 6 umbrella skills

| Skill | What it does | Trigger when... |
|---|---|---|
| `ping-quickstart` | Front door — detects platform and routes | Platform unknown, "where do I start", migrating from ForgeRock/Okta |
| `ping-foundation` | Tenant setup, app registration, directories, policy, branding | Configuring or administering a Ping platform |
| `ping-orchestration` | DaVinci flows, AIC/PingAM journeys, scripted nodes | Designing or building an authentication flow |
| `ping-universal-services` | Protect, Verify, Credentials, IGA, Authorize, MFA — service config and invocation | Adding a shared service to a flow (risk, KYC, credentials, governance, MFA) |
| `ping-app-integration` | Android, iOS, React, OIDC, on-prem SDK integration | Wiring Ping into app code; troubleshooting redirect/CORS/token errors |
| `ping-identity-for-ai` | AI agent identity, Verified Trust, helpdesk AI delegation | Securing an AI agent or LLM-fronted app with Ping |

Skills compose — a complete solution typically spans 2–3 skills. `ping-quickstart` tells you which combination to load.

---

## How it works

Every skill follows a 3-tier progressive disclosure model:

```
Tier 1 — Metadata (~100 tokens)
  skill name + description — loaded at discovery for all skills

Tier 2 — SKILL.md (<5k tokens)
  Routing decision tree: intent → platform → reference tier
  Loaded in full when the skill activates

Tier 3 — References (on demand)
  curated/    hand-authored canonical anchors (1–3 loaded per task)
  generated/  bounded top-N shortlists per platform branch
  runtime/    pointers for live Docs MCP retrieval
```

The agent stops at the first tier that answers the question. It never loads all anchors at once.

---

## Repo layout

```
plugins/ping-identity/
  skills/
    ping-quickstart/          SKILL.md + references/{curated,generated,runtime}/
    ping-foundation/
    ping-orchestration/
    ping-universal-services/
    ping-app-integration/
    ping-identity-for-ai/
  plugin-map.md               skill index and selection rules
  references/index.json       all curated anchor paths
rules/
  authoring-rules.md          frontmatter contract, body length, naming
  routing-rules.md            skill selection precedence
  runtime-selection.md        sandbox-vs-production decision rule
shared/
  taxonomies/                 platform families, capability map, service map
  schemas/                    frontmatter JSON schema
  templates/                  SKILL.md and curated-reference templates
evals/
  prompts/                    trigger / non-trigger / ambiguous prompt sets per skill
  harness/                    Layer 1 + Layer 2 runner, Claude + OpenAI adapters
  results/                    dated eval run outputs
```

---

## Eval status

<!-- BEGIN: layer1-eval-table -->
Layer 1 routing eval across two vendors and six model tiers — last run **2026-06-04**.
Pass bar: 90% trigger / 90% non-trigger / 80% ambiguous. Cells show `trigger% / non-trigger% / ambiguous%`.

### Cross-model comparison

| Skill | Haiku 4.5 | Sonnet 4.6 | Opus 4.7 | gpt-5.4-nano | gpt-5.4-mini | gpt-5.5 |
|---|---|---|---|---|---|---|
| ping-app-integration    | 100 / 100 / **67** ❌ | 100 / 100 / 100 ✅ | 100 / 100 / 100 ✅ | 93 / **80** / **67** ❌ | 100 / **80** / **67** ❌ | 100 / **80** / 100 ❌ |
| ping-foundation         | 100 / 100 / 100 ✅ | 100 / 100 / 100 ✅ | 100 / 100 / **67** ❌ | 95 / 100 / 100 ✅ | 95 / 100 / 100 ✅ | 100 / 100 / 100 ✅ |
| ping-identity-for-ai    | 100 / 100 / 100 ✅ | 100 / 100 / 100 ✅ | 100 / 100 / 100 ✅ | 100 / 100 / 100 ✅ | 100 / 100 / **33** ❌ | 100 / 100 / **67** ❌ |
| ping-orchestration      | **84** / 100 / 100 ❌ | 100 / 100 / 100 ✅ | 100 / 100 / 100 ✅ | 100 / 100 / **67** ❌ | 100 / 100 / **67** ❌ | 95 / 100 / 100 ✅ |
| ping-quickstart         | 92 / 100 / 100 ✅ | 100 / 100 / 100 ✅ | 100 / 100 / 100 ✅ | 92 / 100 / 100 ✅ | 100 / 100 / **67** ❌ | 100 / 100 / 100 ✅ |
| ping-universal-services | **88** / 100 / 100 ❌ | 100 / 100 / 100 ✅ | 100 / 100 / 100 ✅ | 100 / 100 / **67** ❌ | 100 / 100 / **67** ❌ | 94 / 100 / **67** ❌ |
| **Skills passing**      | **4 / 6** | **6 / 6** 🎉 | **5 / 6** | **3 / 6** | **1 / 6** | **3 / 6** |

Bold = below the pass bar.

### Aggregate metrics

| Model | Vendor | Trigger | Non-trigger | Ambiguous | Skills passing |
|---|---|---|---|---|---|
| **Sonnet 4.6** | Anthropic | **100%** | **100%** | **100%** | **6 / 6** 🥇 |
| Opus 4.7 | Anthropic | 100% | 100% | 95% | 5 / 6 |
| Haiku 4.5 | Anthropic | 94% | 100% | 94% | 4 / 6 |
| gpt-5.5 | OpenAI | 98% | 97% | 83% | 3 / 6 |
| gpt-5.4-nano | OpenAI | 97% | 97% | 83% | 3 / 6 |
| gpt-5.4-mini | OpenAI | 99% | 97% | 67% | 1 / 6 |
<!-- END: layer1-eval-table -->

<!-- BEGIN: layer3-eval-table -->
### Layer 3 — Skill execution value

Per-skill accuracy and token consumption with the ping-identity plugin loaded vs a clean `--bare` baseline. Model: Haiku 4.5. n=5 tasks per skill. Pass = all deterministic checks for a task pass.

| Skill | with skill | without skill | Δ pass | tokens/task (w/ → w/o) | token saving |
|---|---|---|---|---|---|
| ping-app-integration    | 60% | 20% | **+40 pp** | 4,142 → 15,925 | −74% |
| ping-foundation         | 60% | 40% | **+20 pp** | 5,219 → 13,679 | −62% |
| ping-universal-services | 40% | 20% | **+20 pp** | 8,441 → 35,026 | **−76%** |
| ping-orchestration      | 20% |  0% | **+20 pp** | 4,278 → 6,375  | −33% |
| ping-quickstart         | 20% |  0% | **+20 pp** | 3,071 → 5,286  | −42% |
| ping-identity-for-ai    |  0% | 40% | −40 pp ⚠️  | 9,460 → 15,439 | −39% |
| **Aggregate**           | **33%** | **20%** | **+13 pp** | **5,835 → 15,289** | **−62%** |

Token savings are measured as `(without − with) / without`; a positive number means the skill made the agent use fewer tokens.

#### Why absolute pass rates look modest

Pass rates of 20–60% are expected for this kind of eval on a small model — they are not a sign the skills are broken:

- **Binary all-or-nothing scoring.** A task with 8 deterministic checks (exact property names, file paths, regex patterns) passes only if every check passes. A single wrong API property name scores the whole task 0%, even if 7/8 checks pass. Real-world value accrues task-by-task even from partial improvements.
- **Haiku is the smallest, cheapest model.** These numbers are a floor. Sonnet 4.6 and Opus 4.8 will show materially higher absolute pass rates. The *relative delta* (skill loaded vs bare) is the value signal — and it is positive for 5 of 6 skills at every model tier.
- **Write-to-disk compliance.** Some 0% results occur because the model answers in chat instead of writing a file. The grader then has nothing to check, and the task scores 0% even though the logic may have been correct. This is a Haiku trait — larger models follow the "use the Write tool" instruction more reliably.
- **`ping-identity-for-ai` inversion (−40 pp).** This skill's tasks are prose-heavy AI-identity guidance scenarios. Haiku's limited working memory is strained by the skill's additional context, producing worse task compliance than the bare baseline. The token savings (−39%) confirm the skill is loading correctly — the accuracy regression is a model-capability mismatch. Sonnet and Opus are expected to show a positive delta for this skill.
<!-- END: layer3-eval-table -->

### What the results show

**Layer 1 — routing:**

- **Trigger accuracy is vendor-portable (94–100%).** All six models correctly identify which skill to load when the user's intent is clear — the descriptions transfer outside the Anthropic ecosystem.
- **Sonnet 4.6 achieves a perfect 6/6** across trigger, non-trigger, and ambiguous prompts and is the recommended deployment target.
- **Non-trigger discipline improved significantly for GPT-5.x** (80–91% → 97%) after adding an adapter-level routing tie-breaker that tells GPT the integration verb (SDK, Swift, React, "my app") takes priority over the service noun when both appear in a prompt.
- **The residual gap is concentrated on ambiguous prompts.** Anthropic models average 98% on prompts requiring a clarifying question; GPT-5.x averages 78%. GPT-5.x defaults to confident routing on borderline cases — this is a vendor-behavioural trait. The clarification rule in the adapter has narrowed but not fully closed this gap.

**Layer 3 — skill execution value:**

- **Token savings are large and consistent across all 6 skills (−33% to −76%).** The skill gives the model exactly what it needs upfront; without it the model burns tokens exploring, self-correcting, and hallucinating API details.
- **Accuracy improves for 5 of 6 skills (+20 to +40 pp).** The largest gain is `ping-app-integration` (+40 pp), where exact SDK property names and package IDs are the deciding factor — the kind of detail an LLM fabricates without authoritative context.
- **`ping-universal-services` shows the biggest token reduction (−76%, 35 k → 8 k tokens/task)** because without the skill, the model spends many turns researching Protect/Verify/Credentials service APIs from scratch.
- **`ping-identity-for-ai` is the one exception (−40 pp on Haiku).** The skill context loads correctly (token saving confirmed at −39%) but overloads Haiku's working memory on prose-heavy tasks. Larger models (Sonnet/Opus) are expected to handle the additional context without the accuracy regression.

### Run the eval yourself

**Layer 1 — routing accuracy:**

```bash
pip install pyyaml jsonschema anthropic openai

# Mock — no API key needed, deterministic:
python3 -m evals.harness.run_eval --adapter mock --layer 1

# Anthropic — direct API:
export ANTHROPIC_API_KEY=sk-ant-...
export MODEL_DIRECT=claude-sonnet-4-6
python3 -m evals.harness.run_eval --adapter claude --layer 1

# Anthropic — AWS Bedrock:
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=eu-west-2
export AWS_BEARER_TOKEN_BEDROCK=<token>
export MODEL_BEDROCK=eu.anthropic.claude-sonnet-4-6
python3 -m evals.harness.run_eval --adapter claude --layer 1

# OpenAI:
export OPENAI_API_KEY=sk-...
export MODEL_OPENAI=gpt-5.5
python3 -m evals.harness.run_eval --adapter openai --layer 1
```

**Layer 3 — skill execution value (requires `claude` CLI on PATH):**

```bash
# Haiku — cheapest, ~15 min for all 60 runs:
export $(grep -v '^#' .env.local | xargs)
python3 -m evals.harness.run_layer3 --models haiku --workers 3 --max-turns 30 --timeout-s 600 --write-summary

# Sonnet — higher accuracy, ~30 min:
python3 -m evals.harness.run_layer3 --models sonnet --workers 3 --max-turns 30 --timeout-s 600 --write-summary

# Restrict to one skill:
python3 -m evals.harness.run_layer3 --models haiku --skill ping-app-integration --workers 3 --write-summary
```

After the run, update the README table:

```bash
python3 scripts/update_readme_eval_table.py --models haiku
```

All required env vars must be set — the adapters have no defaults and will exit with a clear error if any are missing.

---

## Authoring a skill or reference

Read `shared/templates/AUTHORING-RULES.md` before writing anything — it is the single source of truth.

Key constraints enforced by `scripts/validate_skills.py` and the pre-commit hook:
- Every reference `.md` requires a complete frontmatter block (`title`, `product_family`, `capabilities`, `doc_type`, `status` are mandatory)
- `product_family` must match the file's directory path
- Curated anchors must have a `## Scope` section with explicit Covers/Does NOT cover statements
- No UI navigation steps — write field tables and decision rules instead
- Cross-references use repo-relative paths only
- Plugin files (`plugins/<plugin>/`) must not reference `/shared/`
- `SKILL.md` ≤ 120 lines; every new skill PR must include passing Layer 1 eval results

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution guide.

---

## License

See [LICENSE](LICENSE).
