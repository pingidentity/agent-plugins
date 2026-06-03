# Ping Identity Agent Skills

A public skill package that teaches AI coding agents (Claude Code, Cursor, Copilot CLI, Gemini CLI) how to reason about the Ping Identity platform — which product to use, how to configure it, and how to integrate it into an application.

Skills provide **judgment and context** that MCP tools lack. MCP tools handle execution; skills handle the *what* and *why* before execution begins.

---

## Install

**Claude Code**
```bash
/plugin add pingidentity/agent-skills
```

**Cursor** — add to `.cursor/settings.json`:
```json
"remoteRules": ["https://raw.githubusercontent.com/pingidentity/agent-skills/main/rules/routing-rules.md"]
```

**Copilot CLI / OpenCode**
```bash
npx skills add pingidentity/agent-skills
```

**Gemini CLI** — add the plugin path to your `GEMINI.md` or agent configuration.

> The repo will move to `pingidentity/agent-skills` at public launch (Phase 4). Current location: `brando-dill_pingcorp/agent-skills`.

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

Layer 1 routing eval — last run **2026-06-01** against `eu.anthropic.claude-sonnet-4-6` via Bedrock:

| Skill | Trigger | Non-trigger | Ambiguous | Result |
|---|---|---|---|---|
| ping-quickstart | 90% | 100% | 100% | ✅ PASS |
| ping-foundation | 90% | 100% | 100% | ✅ PASS |
| ping-orchestration | 100% | 100% | 100% | ✅ PASS |
| ping-universal-services | 100% | 100% | 100% | ✅ PASS |
| ping-app-integration | 100% | 100% | 100% | ✅ PASS |
| ping-identity-for-ai | 100% | 100% | 100% | ✅ PASS |

Pass bar: 90% trigger / 90% non-trigger / 80% ambiguous. Full results: `evals/results/2026-06-01/claude.layer1.json`.

Run the eval yourself:
```bash
pip install "anthropic[bedrock]" pyyaml jsonschema
python3 -m evals.harness.validate_prompts
python3 -m evals.harness.run_eval --adapter claude --layer 1
# Without an API key:
python3 -m evals.harness.run_eval --adapter mock --layer 1
```

---

## Authoring a skill or reference

Read `shared/templates/AUTHORING-RULES.md` before writing anything — it is the single source of truth.

Key constraints enforced in review (and Phase 3 CI):
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
| 2 | Generated shortlists + reference manifests | ⏳ In progress (June 2–3) |
| 3 | CI hardening + CONTRIBUTING.md | Planned (June 4) |
| 4 | Public launch + repo rename | Planned (TBD) |
| 5 | Marketplace distribution + blog post | Planned (TBD) |

See [PLAN.md](PLAN.md) for full phase details and exit criteria.

---

## License

See [LICENSE](LICENSE).
