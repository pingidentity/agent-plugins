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
precision = |loaded ∩ expected| / |loaded|       (1.0 if both sets are empty)
recall    = |loaded ∩ expected| / |expected|
pass      = recall >= 1.0 AND precision >= 0.5
```

## Aggregate per skill

- `pass_rate = passed_prompts / total_prompts_with_expected_anchors`
- **Pass bar:** `pass_rate >= 0.85`

## Failure output

For each failing prompt the harness prints:

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

## Why precision and recall

Strategy doc § 0 mandates "use the smallest trusted context first." Loading the wrong anchor wastes tokens; missing the right one produces a vague answer. Both must be measured — reporting only recall hides over-retrieval.
