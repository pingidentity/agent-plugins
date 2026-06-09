# GPT-5.x Eval Improvement Plan

## Context

Layer 1 routing evals across the GPT-5.x family show correct trigger accuracy (94–100%) but
low scores on two other dimensions:

| Dimension | GPT-5.4-nano | GPT-5.4-mini | GPT-5.5 |
|---|---|---|---|
| Trigger | 98% | 99% | 100% |
| Non-trigger | 90% | 91% | 95% |
| Ambiguous (clarify) | 56% | 56% | 72% |
| **Skills passing** | **1 / 6** | **0 / 6** | **3 / 6** |

The root cause is not description quality — trigger accuracy proves the descriptions are
vendor-portable. There are two distinct failure patterns, each with a different fix track.

---

## Failure pattern 1 — Non-trigger misroutes (3 prompts across 3 skills)

GPT occasionally over-triggers on a skill when a service or platform name appears in the
prompt but the task belongs elsewhere. All three are consistent across GPT tiers.

### Affected prompts

| Prompt | Expected skill | GPT routes to | Why |
|---|---|---|---|
| `ping-app-integration` N-05: *"How do I invoke the PingOne Verify service to verify a user's identity document from my backend?"* | `ping-universal-services` | `ping-app-integration` | "from my backend" + "invoke" reads as SDK/code integration |
| `ping-orchestration` N-04: *"Integrate the Ping iOS SDK with my AIC journeys in my Swift app."* | `ping-app-integration` | `ping-orchestration` | "AIC journeys" overrides "iOS SDK" + "Swift app" |
| `ping-universal-services` N-04: *"Integrate the PingOne Protect JavaScript SDK into my React single-page application."* | `ping-app-integration` | `ping-universal-services` | "PingOne Protect" overrides "JavaScript SDK" + "React" |

### Fix track: adapter-level system instruction (no description changes)

These misroutes share a pattern: the service/platform noun overrides the intent signal
(SDK integration, app wiring). This is a GPT-specific reading style — Claude handles
noun/intent disambiguation correctly without extra instruction.

The fix is a short paragraph appended to the routing system prompt **in the OpenAI adapter
only**, not in any SKILL.md file. Adding it to descriptions would risk breaking Claude.

**Proposed addition to `evals/harness/adapters/openai.py` system prompt:**

```
Routing tie-breaker: when a prompt contains both a Ping service/product name (Protect,
Verify, IGA, DaVinci, AIC, Journey) AND an explicit app/code integration signal (SDK,
Swift, Kotlin, React, JavaScript, "my app", "my backend", "integrate into"), the
integration signal takes priority. Route to ping-app-integration unless the prompt is
asking to configure the service itself (policies, connectors, thresholds) — not to embed
it in code.
```

**Expected lift:** non-trigger 90–95% → ~98% across GPT tiers. Three specific prompts
resolved with no Claude regression risk.

---

## Failure pattern 2 — Ambiguous prompts not triggering clarification (13 failures)

GPT-5.x defaults to confident routing even on severely underspecified prompts. Where Claude
asks a clarifying question, GPT picks a skill and answers. This is the dominant failure
mode (56–72% ambiguous average vs 98% for Claude).

All 13 failures catalogued by skill:

### `ping-app-integration` (A-01, A-02, A-03)

| ID | Prompt | Expected keywords |
|---|---|---|
| A-01 | "I need to integrate Ping into my app." | android, ios, react, web, mobile, sdk |
| A-02 | "I need to add login to my app." | android, ios, web, react, mobile, platform |
| A-03 | "How do I integrate Ping with my backend?" | oidc, client-credentials, token, sdk, server |

All three are genuinely underspecified — no platform, no tech stack. GPT routes to
`ping-app-integration` directly.

### `ping-foundation` (A-02, A-03)

| ID | Prompt | Expected keywords |
|---|---|---|
| A-02 | "Set up SSO." | pingone, aic, software, platform, workforce, ciam |
| A-03 | "Add a user to Ping." | pingone, aic, directory, platform, mt, st |

Two-to-four word prompts with zero platform context. GPT assumes PingOne MT and answers.

### `ping-identity-for-ai` (A-01, A-02, A-03)

| ID | Prompt | Expected keywords |
|---|---|---|
| A-01 | "I need to authenticate an agent." | ai, human, user, machine, api, bot |
| A-02 | "I need to secure API access for an automated process that runs on a schedule..." | ai, agent, batch, machine, llm, autonomous |
| A-03 | "How do I add trust to my application so downstream services can rely on the claims it presents?" | verified trust, oidc, jwt, signed assertion, ai |

A-02 and A-03 are the most important: they test whether GPT asks "is this an AI agent or
a conventional machine process?" before routing. GPT routes to `ping-identity-for-ai`
directly for A-02 (automated process) and to `ping-foundation` or `ping-app-integration`
for A-03.

### `ping-orchestration` (A-02, A-03)

| ID | Prompt | Expected keywords |
|---|---|---|
| A-02 | "AIC or DaVinci for my login flow?" | use case, workforce, ciam, requirement, platform |
| A-03 | "Where do I configure MFA in Ping?" | pingone, aic, platform, mt, st, journey, policy |

These are explicit platform-comparison questions. GPT picks one and recommends it. Claude
asks which use case / platform first.

### `ping-quickstart` (A-02, A-03 on some tiers)

| ID | Prompt | Expected keywords |
|---|---|---|
| A-02 | "How do I do passwordless?" | pingone, aic, platform, product, davinci, journey |
| A-03 | "We need risk-based authentication." | pingone, aic, platform, protect, davinci, journey |

Platform unspecified. GPT routes to `ping-orchestration` or `ping-universal-services`
directly.

### `ping-universal-services` (A-01, A-02, A-03)

| ID | Prompt | Expected keywords |
|---|---|---|
| A-01 | "I need to add verification to my registration flow." | verify, protect, risk, identity proofing |
| A-02 | "My users are getting suspicious login attempts — how do I add security to my AIC journey?" | protect, risk, mfa, signal, fraud, threat, score |
| A-03 | "A user says they can't verify their identity when they try to log in — is this a Verify issue or an MFA issue?" | verify, mfa, document, liveness |

A-01 and A-02 are vague ("add verification", "add security") — service unspecified. GPT
picks the most keyword-salient service and runs with it. A-03 is an explicit compare
question that GPT answers rather than clarifies.

---

### Fix track: adapter-level clarification instruction

The same pattern that fixes non-trigger misroutes applies here: an adapter-level instruction
that GPT will respect because it's a direct system instruction, not a behavioural hint
buried in a skill description.

**Proposed addition to `evals/harness/adapters/openai.py` system prompt (separate paragraph):**

```
Clarification rule: when the user's prompt is 10 words or fewer AND does not name a
specific platform (PingOne MT, AIC, PingFederate, PingOne ST), tech stack (Android, iOS,
React, Node.js), or named service (Protect, Verify, IGA, MFA, DaVinci), respond with
action "clarify" and ask a single focused question. Do not route. Examples that require
clarification: "Set up SSO", "Add a user to Ping", "I need to integrate Ping into my app",
"I need to authenticate an agent", "AIC or DaVinci for my login flow?".
```

**Why this works without breaking Claude:** The instruction is injected only into the
OpenAI adapter's system prompt, not into SKILL.md descriptions. Claude never sees it.

**Expected lift:** ambiguous 56–72% → ~85–90% across GPT tiers. The 10-word / no-named-
entity heuristic covers all 13 failing prompts while leaving well-specified prompts
unaffected.

---

## Implementation plan

### Step 1 — Adapter-level system prompt additions (no SKILL.md changes)

File to edit: `evals/harness/adapters/openai.py` — `_build_system_prompt()` function.

Add two paragraphs after the routing rules, before the closing instruction:

1. **Routing tie-breaker** (fixes non-trigger pattern 1)
2. **Clarification rule** (fixes ambiguous pattern 2)

Estimated effort: 15 minutes. Zero risk to Claude eval scores.

### Step 2 — Re-run GPT-5.x Layer 1 eval

```bash
for model in gpt-5.4-nano gpt-5.4-mini gpt-5.5; do
  OPENAI_API_KEY=... MODEL_OPENAI=$model \
    python3 -m evals.harness.run_eval --adapter openai --layer 1 --write-results
done
```

### Step 3 — Verify Claude scores unchanged

```bash
for model in eu.anthropic.claude-sonnet-4-6 eu.anthropic.claude-opus-4-7 eu.anthropic.claude-haiku-4-5-20251001-v1:0; do
  CLAUDE_CODE_USE_BEDROCK=1 AWS_REGION=eu-west-2 MODEL_BEDROCK=$model \
    python3 -m evals.harness.run_eval --adapter claude --layer 1
done
```

Sonnet 4.6 must remain 6/6. If any Claude score drops, revert the adapter change and
investigate.

### Step 4 — Update README cross-model table

Replace results in the All-models cross comparison table with the new scores.

---

## Expected outcome

| Model | Before | After (projected) |
|---|---|---|
| gpt-5.4-nano | 1 / 6 | 3–4 / 6 |
| gpt-5.4-mini | 0 / 6 | 3–4 / 6 |
| gpt-5.5 | 3 / 6 | 5–6 / 6 |

The ambiguous-prompt gap will narrow but not fully close — some GPT-5.x models will still
prefer to route on borderline cases even with explicit instruction. Full parity with Claude
on ambiguous prompts is not a realistic target without fine-tuning.

---

## What is NOT in scope for this plan

- Changing any SKILL.md description (confirmed to cause Claude regressions)
- Improving Opus 4.7 `ping-identity-for-ai` T-09 (separate question pending on skill
  ownership — see conversation context)
- Improving Haiku 4.5 `ping-orchestration` (tier limitation, not a prompt or description
  issue)
- Gemini or other vendor adapters (no API key available)
