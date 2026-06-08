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
<!-- Layer 3 — generated by scripts/update_readme_eval_table.py -->
<!-- END: layer3-eval-table -->

### What the results show

- **Trigger accuracy is vendor-portable (94–100%).** All six models correctly identify which skill to load when the user's intent is clear — the descriptions transfer outside the Anthropic ecosystem.
- **Sonnet 4.6 achieves a perfect 6/6** across trigger, non-trigger, and ambiguous prompts and is the recommended deployment target.
- **Non-trigger discipline improved significantly for GPT-5.x** (80–91% → 97%) after adding an adapter-level routing tie-breaker that tells GPT the integration verb (SDK, Swift, React, "my app") takes priority over the service noun when both appear in a prompt.
- **The residual gap is concentrated on ambiguous prompts.** Anthropic models average 98% on prompts requiring a clarifying question; GPT-5.x averages 78%. GPT-5.x defaults to confident routing on borderline cases — this is a vendor-behavioural trait. The clarification rule in the adapter has narrowed but not fully closed this gap.

### Run the eval yourself

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
