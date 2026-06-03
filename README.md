# Ping Identity Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A public skill package that teaches AI coding agents (Claude Code, Cursor, Copilot CLI, Gemini CLI) how to reason about the Ping Identity platform — which product to use, how to configure it, and how to integrate it into an application.

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
| `ping-universal-services` | Protect, Verify, Credentials, IGA, Authorize — service config and invocation | Adding a shared service to a flow (risk, KYC, credentials, governance) |
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
  generated/  bounded top-N shortlists per platform branch (Phase 2)
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
  harness/                    Layer 1 + Layer 2 runner, Claude + mock adapters
  results/                    dated eval run outputs
```

---

## Eval status

Layer 1 routing eval — last run **2026-06-03**:

| Skill | Trigger | Non-trigger | Ambiguous | Result |
|---|---|---|---|---|
| ping-quickstart | 92% | 100% | 100% | ✅ PASS |
| ping-foundation | 100% | 100% | 100% | ✅ PASS |
| ping-orchestration | 93% | 100% | 100% | ✅ PASS |
| ping-universal-services | 100% | 100% | 100% | ✅ PASS |
| ping-app-integration | 100% | 100% | 100% | ✅ PASS |
| ping-identity-for-ai | 100% | 100% | 100% | ✅ PASS |

Pass bar: 90% trigger / 90% non-trigger / 80% ambiguous. Full results: `evals/results/`.

Run the eval yourself:
```bash
pip install pyyaml jsonschema anthropic

# Mock — no API key needed, deterministic:
python3 -m evals.harness.run_eval --adapter mock --layer 1

# Live — direct Anthropic API:
export ANTHROPIC_API_KEY=sk-ant-...
export MODEL_DIRECT=claude-3-5-sonnet-20241022
python3 -m evals.harness.run_eval --adapter claude --layer 1

# Live — AWS Bedrock:
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
export AWS_BEARER_TOKEN_BEDROCK=<token>
export MODEL_BEDROCK=<cross-region-inference-profile-id>
python3 -m evals.harness.run_eval --adapter claude --layer 1
```

All four env vars for the chosen path are required — the adapter has no defaults and will exit with a clear error message if any are missing.

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

---

## Delivery status

| Phase | Description | Status |
|---|---|---|
| 0 | Repo restructure + eval harness scaffold | ✅ Complete |
| 1 | Author 3 new skills + Layer 1 eval passing | ✅ Complete (2026-06-01) |
| 2 | Generated shortlists + reference manifests | ✅ Complete (2026-06-03) |
| 3 | CI hardening + CONTRIBUTING.md | ✅ Complete (2026-06-03) |
| 4 | Public launch + repo rename | Planned (TBD) |
| 5 | Marketplace distribution + blog post | Planned (TBD) |

Full delivery history is tracked in the project's internal planning docs.

---

## License

See [LICENSE](LICENSE).
