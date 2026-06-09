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
- A judge LLM (Claude / Codex / Gemini), **DIFFERENT** from the LLM under test.

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
  "tier_discipline": {"score": <int>, "reason": "<≤200 chars>",
                      "expected": "<curated|docs-fallback>",
                      "observed": "<curated|docs-fallback|none>"}
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

Self-judging collapses the eval — a model rates its own wording highly because it matches its priors. Defaults:
- Claude under test → Codex judges
- Codex under test → Claude judges
- Gemini under test → Claude judges

Override with `--judge <model>`.

## Schedule

Layer 3 runs weekly and before any release. It is NOT a per-PR gate in Phase 0 or Phase 1. It becomes a pre-release requirement from Phase 2 onward.
