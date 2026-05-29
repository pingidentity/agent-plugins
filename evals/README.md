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

See detailed rubrics in `scorecards/`.

## Layout

```
evals/
  prompts/<skill>.yaml          # one prompt set per skill (validated by schema)
  schemas/prompt-set.schema.json
  golden/<skill>/<id>.md        # golden plans for Layer 3 (Phase 1+)
  scorecards/
    routing-eval.md             # Layer 1 rubric
    anchor-selection-eval.md    # Layer 2 rubric
    plan-quality-eval.md        # Layer 3 rubric
  harness/
    validate_prompts.py         # YAML schema validator
    run_eval.py                 # Layer 1 + Layer 2 runner
    judge_plans.py              # Layer 3 — LLM-as-judge (stub in Phase 0)
    cross_llm.py                # Layer 4 — multi-LLM driver (stub in Phase 0)
    adapters/
      base.py                   # RunResult dataclass + LLMAdapter Protocol
      mock.py                   # deterministic mock for harness tests
      claude.py                 # Anthropic SDK adapter (stub in Phase 0)
    tests/                      # pytest covering the harness itself
  results/<YYYY-MM-DD>/<llm>.layer{1,2}.json
```

## Quick start

Install dependencies once:

```bash
/usr/bin/python3 -m pip install -r evals/harness/requirements.txt
```

Validate the prompt sets parse:

```bash
/usr/bin/python3 -m evals.harness.validate_prompts
```

Run Layer 1 against the mock adapter (proves the harness; not a skill quality signal):

```bash
/usr/bin/python3 -m evals.harness.run_eval --adapter mock --layer 1
/usr/bin/python3 -m evals.harness.run_eval --adapter mock --layer 2
```

Run harness unit tests:

```bash
/usr/bin/python3 -m pytest evals/harness/tests/ -v
```

## Authoring checklist (every skill PR from Phase 1+)

A skill PR is rejected by CI (Phase 3+) unless it includes:

1. `evals/prompts/<skill>.yaml` — ≥10 trigger / ≥5 non-trigger / ≥3 ambiguous prompts; schema-valid.
2. `evals/golden/<skill>/<id>.md` — ≥3 golden plans for Layer 3.
3. A passing local Layer 1 + Layer 2 run against the Claude adapter.

## Adding a new LLM adapter

1. Add `evals/harness/adapters/<llm>.py` implementing `LLMAdapter`.
2. Wire `_build_adapter()` in `run_eval.py`.
3. Add `<llm>` to `LLMS` in `cross_llm.py`.

## CI wiring (Phase 3+)

`.github/workflows/run-evals.yml` will run:

```bash
/usr/bin/python3 -m evals.harness.validate_prompts
/usr/bin/python3 -m evals.harness.run_eval --adapter claude --layer 1 --write-results
/usr/bin/python3 -m evals.harness.run_eval --adapter claude --layer 2 --write-results
```

A non-zero exit blocks merge.

## Why a different judge model for Layer 3

Self-judging collapses the eval. The default is cross-model: Claude judges Codex/Gemini output; Codex/Gemini judge Claude output. Override with `--judge <model>`.
