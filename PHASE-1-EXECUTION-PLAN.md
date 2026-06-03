# Phase 1 — Detailed Execution Plan

> Companion to [PLAN.md](PLAN.md) § "Phase 1 — Author the three planned umbrella skills". Decomposes the four-day window (May 31 – June 3) into sequenced sub-phases with concrete deliverables, file lists, dependencies, and exit gates.

## Phase 1 goal (verbatim from PLAN.md)

`ping-universal-services`, `ping-app-integration`, and `ping-identity-for-ai` ship at **orientation depth** — each with a working `SKILL.md` decision tree and **≥3 curated anchors**, complete eval prompt sets, and a passing Layer 1 routing run.

## Entry preconditions (must be true before Phase 1 starts)

| # | Precondition | How to verify | Status |
|---|---|---|---|
| 1 | Phase 0 exit criteria met | `python -m evals.harness.validate_prompts` exits 0; `python -m evals.harness.run_eval --adapter mock --layer 1` exits 0 | ✅ per `evals/README.md` ("Phase 0 smoke check passes") |
| 2 | All six skill directories exist with the per-skill tree | `ls plugins/ping-identity/skills/<skill>/references/{curated,generated,runtime}/` returns 0 in all 6 | ✅ confirmed |
| 3 | Three planned skills have SKILL.md + ping-marketplace.json scaffolds | File exists check | ✅ confirmed |
| 4 | Existing prompt sets exist for the three planned skills | `evals/prompts/ping-{universal-services,app-integration,identity-for-ai}.yaml` exist | ✅ stubs present (~1.3–1.4 KB each — need expansion to spec) |
| 5 | `rules/routing-rules.md` is committed and authoritative | File exists, references all 6 skills | ⚠️ verify in 1.0 |
| 6 | Decision needed: Docs MCP availability for `references/runtime/` (PLAN.md decision #4) | Product confirms public docs site fallback is the v1 path | ⚠️ assume public docs fallback unless told otherwise |

If any precondition fails, address before starting 1.1.

---

## Sub-phase 1.0 — Prep & alignment (Day 0, ~2 h)

**Goal:** clear ambiguities, lock the curated-anchor outline for each skill, and confirm the eval pass bar so authoring doesn't loop on rework.

### Steps

1. **Read current state.** Open the three planned skills' `SKILL.md` files; capture the existing routing tables and which curated anchor filenames they already promise (the universal-services SKILL.md, for example, already references `references/curated/<service>.md` placeholders). Treat any name in the existing routing table as a hard contract — anchors must be authored at those exact paths or the SKILL.md must be edited in the same PR.
2. **Verify `rules/routing-rules.md`** lists all 6 skills with disambiguation rules. If gaps exist, fix in this sub-phase before Phase 1.1 — multi-skill composition cases for the 3 planned skills must be documented before authoring.
3. **Lock anchor outlines.** For each skill, draft a one-paragraph outline per curated anchor (filename → 3-bullet "Covers / Does NOT cover / Decision rules" outline). Save the three outlines as a single working note (`PHASE-1-OUTLINES.md`, untracked or PR-local) — this is the spec the authoring sub-phases write against.
4. **Confirm `shared/templates/curated-reference.template.md` and `shared/templates/AUTHORING-RULES.md`** are the source of truth (per CLAUDE.md). If either template is missing required sections (Scope, Prerequisites, Common variants, Related references, Source), patch first.
5. **Pick the Layer 1 adapter.** Phase 0 uses `mock`; Phase 1 needs the `claude` adapter wired up against the real API. Confirm API keys are present in the environment used for `python -m evals.harness.run_eval --adapter claude --layer 1`. If not, file a blocker before 1.4.

### Deliverables

- `PHASE-1-OUTLINES.md` (working doc) — anchor-by-anchor outlines for all three skills.
- Patched `rules/routing-rules.md` if gaps were found.
- Confirmed `claude` adapter readiness (API key + smoke test on a single prompt).

### Exit gate

- All three planned-skill SKILL.md files cross-checked against PLAN.md § Phase 1 step 1–3 anchor lists. Any naming mismatches resolved (either fix the SKILL.md routing table or rename the planned anchor file).
- One smoke prompt round-trips through `run_eval --adapter claude --layer 1`.

---

## Sub-phase 1.1 — `ping-universal-services` content (Day 1, ~1 day)

**Goal:** ship orientation-depth curated content + complete eval prompt set.

### Curated anchors (PLAN.md § Phase 1 step 1)

Author all four under `plugins/ping-identity/skills/ping-universal-services/references/curated/`:

1. `universal-services-overview.md` — what the universal services umbrella covers (Protect, Verify, Credentials, IGA, SSO, Authorize), the "consumed-from-multiple-platforms" criterion, when to reach for this skill vs. `ping-foundation` or `ping-orchestration`.
2. `choosing-the-right-service.md` — decision table: user intent → which service. Must cover the six services named in PLAN.md and the SKILL.md routing table.
3. `service-invocation-patterns.md` — how a service is invoked from PingOne MT vs. PingOne ST vs. Ping Software, including DaVinci-flow integration and the policy/verification handoff pattern.
4. `cross-platform-service-usage.md` — the cross-platform usage rules (which combinations are supported, which are anti-patterns).

Each anchor MUST follow the curated-reference structure from CLAUDE.md (frontmatter with `title`, `product_family`, `capabilities`, `doc_type`, `status`; sections in order: Title, Description, Scope, Content, Prerequisites, Common variants, Related references, Source).

`product_family` for these anchors is `cross-platform` (path mismatch will fail CI in Phase 3 — get it right now).

### Generated branch stubs (PLAN.md § Phase 1 step 1)

Create empty `top-15.json` placeholders or `.gitkeep` directories under `references/generated/{protect,verify,credentials,sso,iga}/`. **Do not populate with real content** — Phase 2 builds shortlists from the docs catalog. Goal in Phase 1 is just directory shape.

### SKILL.md edits

- Replace placeholder anchor paths in the routing table with the four real filenames above.
- Confirm the "Multi-skill use cases" table matches `rules/routing-rules.md`.
- Confirm body still fits within 120 lines.

### Eval prompt set (PLAN.md § Phase 1 step 4)

Expand `evals/prompts/ping-universal-services.yaml` to:
- ≥10 trigger prompts (cover all 6 services × MT/ST/cross-platform variants)
- ≥5 non-trigger prompts (cleanly belong to `ping-foundation` / `ping-orchestration` / `ping-app-integration` / `ping-quickstart`)
- ≥3 ambiguous prompts (require clarification — e.g., "I want better security on logins" could be Protect or just MFA)

Run `python -m evals.harness.validate_prompts` after editing.

### Cross-link

- Add or update a row in `ping-quickstart/SKILL.md` routing table pointing at universal-services for Protect/Verify/Credentials/IGA intents.
- Add an entry under `plugins/ping-identity/plugin-map.md`.
- Add an entry under `plugins/ping-identity/references/index.json`.

### Exit gate

- 4 curated anchors committed, all passing frontmatter validation.
- SKILL.md routing table self-consistent; ≤120 lines.
- Prompt YAML validates against the schema; counts ≥10/≥5/≥3.
- `run_eval --adapter mock --layer 1` still exits 0.

---

## Sub-phase 1.2 — `ping-app-integration` content (Day 2, ~1 day)

**Goal:** same shape as 1.1, with mobile + web + on-prem variants.

### Curated anchors (PLAN.md § Phase 1 step 2)

Author all four under `plugins/ping-identity/skills/ping-app-integration/references/curated/`:

1. `app-integration-overview.md` — when to reach for this skill (implementation-side work) vs. `ping-foundation` (admin-side); the SDK landscape (Android, iOS, React, web, on-prem agents).
2. `mobile-integration-basics.md` — Android + iOS SDK orientation; common auth flows (OIDC, MFA, biometric); known pitfalls (token storage, deep linking, refresh).
3. `web-integration-basics.md` — React SDK + browser auth flows; PKCE; session handling; OIDC vs. SAML decision rule.
4. `integration-troubleshooting-basics.md` — top failure modes (CORS, redirect URI mismatch, token introspection, clock skew) and their fixes.

`product_family` should be `cross-platform` for the overview and troubleshooting anchors; mobile/web anchors can stay `cross-platform` since they cover SDKs that target multiple Ping platforms.

### Generated branch stubs

Create directories under `references/generated/{mobile,web,orchestration-sdks,on-prem-integration}/` (empty placeholders only).

### SKILL.md edits

Verify routing table matches the 4 anchors; verify ≤120 lines.

### Eval prompt set

Expand `evals/prompts/ping-app-integration.yaml` to ≥10 / ≥5 / ≥3.

Trigger prompts must cover:
- Mobile (Android, iOS) — at least 3
- Web / React — at least 3
- On-prem app integration — at least 2
- Orchestration SDK (DaVinci-from-app) — at least 2

Non-trigger prompts must include at least one each of: a `ping-foundation` admin task, a `ping-orchestration` flow-design task, a `ping-quickstart` "where do I start?" prompt.

### Cross-link

- `ping-quickstart/SKILL.md` routing table.
- `plugins/ping-identity/plugin-map.md`.
- `plugins/ping-identity/references/index.json`.

### Exit gate

Same shape as 1.1.

---

## Sub-phase 1.3 — `ping-identity-for-ai` content (Day 3 morning, ~½ day)

**Goal:** the smallest of the three skills (4 anchors, but the domain is newer and content depth will be lighter).

### Curated anchors (PLAN.md § Phase 1 step 3)

Author all four under `plugins/ping-identity/skills/ping-identity-for-ai/references/curated/`:

1. `identity-for-ai-overview.md` — what "identity for AI" means at Ping; the three buckets (verified trust, agent security, AI app auth); how this skill differs from the other five.
2. `verified-trust-overview.md` — the Verified Trust product: capabilities, where it plugs in (DaVinci flow, app-side, policy).
3. `agent-security-patterns.md` — patterns for securing autonomous / semi-autonomous agents calling Ping APIs; auth model; token scoping; revocation.
4. `workforce-helpdesk-ai.md` — workforce helpdesk AI use case (employee asks AI agent → agent calls Ping APIs on their behalf); identity verification pattern; audit pattern.

Note: PLAN.md does NOT list a `references/generated/` branch list for this skill. Skip generated branches in Phase 1; revisit in Phase 2 when the docs catalog is scanned.

### SKILL.md edits

Verify routing table; ≤120 lines.

### Eval prompt set

Expand `evals/prompts/ping-identity-for-ai.yaml` to ≥10 / ≥5 / ≥3. Trigger prompts must include: agent calling Ping APIs, verifiable trust for AI output, helpdesk-AI auth, AI app auth (LLM-fronted apps), and the negative case (a regular customer-identity flow that happens to use ML — should NOT activate this skill).

### Cross-link

- `ping-quickstart/SKILL.md` (very important — this is the newest concept and quickstart needs to know how to point at it).
- `plugin-map.md` and `references/index.json`.

### Exit gate

Same shape as 1.1.

---

## Sub-phase 1.4 — Layer 1 eval iteration (Day 3 afternoon – Day 4 morning, ~1 day)

**Goal:** pass bar — 90% trigger / 90% non-trigger / 80% ambiguous-handled — across all 6 skills, on the `claude` adapter.

This is the loop where most rework happens. Budget for 2–3 iterations.

### Steps

1. Run `python -m evals.harness.run_eval --adapter claude --layer 1 --skill all`. Save output to `evals/results/2026-06-01/claude.json` (use the appropriate dated dir).
2. **Diagnose failures by category:**
   - **Wrong umbrella selected** — usually a SKILL.md "When to use" wording problem. Tighten the disambiguation language; add the failing prompt's intent class to "When NOT to use".
   - **Ambiguous prompt routed without clarification** — strengthen the "what are you trying to do?" decision tree.
   - **Two skills both activated unnecessarily** — `rules/routing-rules.md` precedence is unclear; tighten.
3. Edit only the `SKILL.md` files and `rules/routing-rules.md` — do NOT edit the prompt YAMLs to make the test pass (that defeats the eval).
4. Re-run; iterate until pass bar is hit for all 6 skills.
5. Save final results in `evals/results/<date>/claude.json` (gitignored is fine; this is not a CI gate yet — Phase 3 turns it into one).

### What "passing" means here

Per PLAN.md § Layer 1: ≥90% of trigger prompts activated the right skill, ≥90% of non-trigger prompts correctly NOT activated, ≥80% of ambiguous prompts got a clarifying question (not a guess).

### Risk handling

If a single skill is stuck below the bar after 3 iterations, **don't lower the bar**. Two options:
- (a) Move the failing prompts to the ambiguous bucket if they genuinely belong there.
- (b) Escalate as a documented "known limitation" to be fixed in Phase 2 with a curated-anchor rewrite.

Option (b) requires an entry in `risks` section of the PR description.

### Exit gate

- All 6 skills meet the Layer 1 pass bar on the `claude` adapter.
- `evals/results/<date>/claude.json` is committed (or referenced in PR description).

---

## Sub-phase 1.5 — End-to-end composition test + PR prep (Day 4 afternoon, ~½ day)

**Goal:** verify PLAN.md's Phase 1 Exit Criterion — the cross-skill routing case actually works.

### The canonical test

> "I want to add KYC during registration on my React app"

This prompt must:
1. Activate `ping-quickstart` first (free-text intent, platform unknown).
2. After clarification, route to `ping-orchestration` (registration flow) + `ping-universal-services` (KYC = Verify) + `ping-app-integration` (React).
3. Load curated anchors from each: at least one anchor per skill. Concretely:
   - `ping-orchestration/references/curated/.../` — a registration flow anchor
   - `ping-universal-services/references/curated/choosing-the-right-service.md` (Verify branch) and likely `service-invocation-patterns.md`
   - `ping-app-integration/references/curated/web-integration-basics.md`
4. Produce a plan that names: which Ping product (PingOne MT or ST), which Verify policy, which React SDK calls, and the sequence.

### Steps

1. Run the canonical prompt manually (or scripted) against the `claude` adapter.
2. Capture the full transcript (skill activations + Read tool calls + final plan).
3. Verify each of the 4 conditions above.
4. If any condition fails, return to 1.1–1.4 to fix the underlying skill or rule. Do **not** ship Phase 1 with a broken composition case.
5. Author 2 additional composition prompts to spot-check the pattern works generally:
   - "Add MFA + risk-based step-up on iOS" → orchestration + universal-services + app-integration
   - "Build an AI agent that can reset employee passwords" → identity-for-ai + foundation
6. Add the three composition prompts to `evals/prompts/composition.yaml` (a NEW file — orienting a future Phase 2/3 to test composition explicitly). Validate against the schema.

### PR

Open a single PR titled `feat: Phase 1 — author 3 planned umbrella skills`.

PR description checklist:
- [ ] All 12 curated anchors authored and frontmatter-valid (4 + 4 + 4)
- [ ] All 3 SKILL.md files ≤120 lines
- [ ] All 3 prompt YAMLs at ≥10/≥5/≥3
- [ ] Layer 1 eval `evals/results/<date>/claude.json` shows pass bar for all 6 skills
- [ ] Canonical KYC composition test transcript attached
- [ ] `ping-quickstart/SKILL.md` cross-links updated
- [ ] `plugin-map.md` + `references/index.json` updated
- [ ] `rules/routing-rules.md` updated if precedence changed during 1.4 iteration
- [ ] No internal-only references introduced (Glean, Polaris, internal Slack)
- [ ] Each new curated anchor has `Related references` filled in (cross-skill linkage)

### Exit gate (Phase 1 complete)

PLAN.md exit criterion verbatim:

> End-to-end test passes — free-text intent ("KYC during registration on my React app") routes correctly through `ping-quickstart` → `ping-orchestration` + `ping-universal-services` + `ping-app-integration`, returns a curated plan citing the right anchors.

Plus the PR-checklist items above.

---

## Deliverables summary (final inventory at Phase 1 close)

### New files (12 curated anchors + 1 composition prompt set)

```
plugins/ping-identity/skills/ping-universal-services/references/curated/
  universal-services-overview.md
  choosing-the-right-service.md
  service-invocation-patterns.md
  cross-platform-service-usage.md

plugins/ping-identity/skills/ping-app-integration/references/curated/
  app-integration-overview.md
  mobile-integration-basics.md
  web-integration-basics.md
  integration-troubleshooting-basics.md

plugins/ping-identity/skills/ping-identity-for-ai/references/curated/
  identity-for-ai-overview.md
  verified-trust-overview.md
  agent-security-patterns.md
  workforce-helpdesk-ai.md

evals/prompts/composition.yaml
```

### Edited files

- All 3 planned-skill `SKILL.md` files (routing tables finalized)
- `ping-quickstart/SKILL.md` (cross-links)
- `rules/routing-rules.md` (any disambiguation tightening from 1.4)
- `plugins/ping-identity/plugin-map.md`
- `plugins/ping-identity/references/index.json`
- `evals/prompts/ping-universal-services.yaml` (expand to spec)
- `evals/prompts/ping-app-integration.yaml` (expand to spec)
- `evals/prompts/ping-identity-for-ai.yaml` (expand to spec)

### Generated branch directories (empty placeholders only — populated in Phase 2)

```
ping-universal-services/references/generated/{protect,verify,credentials,sso,iga}/
ping-app-integration/references/generated/{mobile,web,orchestration-sdks,on-prem-integration}/
```

---

## Day-by-day timeline (4-day window, May 31 – June 3 per PLAN.md)

| Day | Sub-phase | Focus | Hours |
|---|---|---|---|
| Day 1 AM | 1.0 | Outlines, route-rule check, adapter smoke | 2–3 h |
| Day 1 PM | 1.1 | `ping-universal-services` anchors + prompts + cross-links | 5–6 h |
| Day 2 | 1.2 | `ping-app-integration` anchors + prompts + cross-links | 6–8 h |
| Day 3 AM | 1.3 | `ping-identity-for-ai` anchors + prompts + cross-links | 4–5 h |
| Day 3 PM | 1.4 | Layer 1 eval — first run + first iteration | 3–4 h |
| Day 4 AM | 1.4 cont. | Layer 1 eval — second iteration if needed | 3–4 h |
| Day 4 PM | 1.5 | Composition test + PR prep | 3–4 h |

Total: ~28–34 hours of focused authoring + eval work.

---

## Risks specific to Phase 1

| Risk | Likelihood | Mitigation |
|---|---|---|
| Curated content drifts beyond orientation depth and burns time | High | Hard cap each anchor at 200–400 lines per CLAUDE.md; if a topic needs more, split into a Phase 2 follow-up anchor. |
| Layer 1 eval doesn't converge — two skills keep tying | Medium | `rules/routing-rules.md` precedence ladder is the disambiguation tool; add a tie-breaker clause rather than rewriting SKILL.md repeatedly. |
| `ping-identity-for-ai` content is hardest to source (newest product area) | Medium | If Verified Trust / agent-security docs are thin, anchor body cites the public Ping AI announcements + names the product, defers detail to a `references/runtime/docs-mcp-routing.md` pointer. Document gap in PR description. |
| Claude API rate limits during 1.4 eval iteration | Low | Budget at most 3 full Layer 1 sweeps × 6 skills × ~18 prompts ≈ 324 API calls; well within standard limits. |
| Composition test reveals a structural gap that requires SKILL.md surgery on a live skill (e.g., `ping-orchestration`) | Medium | Allowed — fix in this PR. Re-run Layer 1 for the changed skill. |
| Frontmatter `product_family` mismatch caught only at Phase 3 CI | Low | Validate locally via `python -m evals.harness.validate_prompts` and a manual frontmatter grep before PR open. |

---

## Out of scope for Phase 1 (deferred to Phase 2)

- Populating `references/generated/<branch>/top-N.json` files. Phase 1 only creates the directories.
- Layer 2 anchor-selection eval. Phase 1 only requires Layer 1 to pass; Layer 2 becomes a gate in Phase 2.
- Layer 3 plan-quality eval. Weekly cadence starts in Phase 2.
- Upgrading curated anchors beyond orientation depth — that's explicitly Phase 2 work for "weak anchors flagged by Phase 1 evals (Layer 3 score <4.0)."
- The `ping-identity-for-ai` generated-branch list (PLAN.md § Phase 1 does not require it).
- CI gating. Eval is local-only in Phase 1; CI integration is Phase 3.

---

## Open questions to resolve before starting

These map to PLAN.md § "Decisions needed from product":

1. **Decision #4 (Docs MCP availability)** — Phase 1 assumes `references/runtime/docs-mcp-routing.md` documents the pattern with public docs as fallback. Confirm before authoring the runtime stubs in 1.1–1.3.
2. **Decision #7 (LLM API budget)** — Layer 1 in Phase 1 only needs Claude. Codex + Gemini are Phase 3+. No blocker for Phase 1 if Claude API access is available.
3. **`ping-identity-for-ai` content depth** — confirm with product whether Verified Trust and agent-security material is shareable at orientation depth on a public repo (Phase 4 strips internal references; better to author public-safe from the start).
