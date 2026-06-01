"""Layer 1 (routing) + Layer 2 (anchor selection) eval runner.

Usage:
  python3 -m evals.harness.run_eval --adapter mock --layer 1
  python3 -m evals.harness.run_eval --adapter claude --layer 2 --skill ping-orchestration
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

from evals.harness.adapters.base import LLMAdapter
from evals.harness.adapters.mock import MockAdapter, MockRule

REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPTS_DIR = REPO_ROOT / "evals" / "prompts"
RESULTS_DIR = REPO_ROOT / "evals" / "results"

LAYER_1_TRIGGER_BAR = 0.90
LAYER_1_NON_TRIGGER_BAR = 0.90
LAYER_1_AMBIGUOUS_BAR = 0.80
LAYER_2_BAR = 0.85


@dataclass
class PromptSet:
    skill: str
    trigger: list[dict]
    non_trigger: list[dict]
    ambiguous: list[dict]


@dataclass
class Layer1Report:
    skill: str
    trigger_pass_rate: float
    non_trigger_pass_rate: float
    ambiguous_pass_rate: float
    failures: list[str] = field(default_factory=list)

    @property
    def passed_overall(self) -> bool:
        return (
            self.trigger_pass_rate >= LAYER_1_TRIGGER_BAR
            and self.non_trigger_pass_rate >= LAYER_1_NON_TRIGGER_BAR
            and self.ambiguous_pass_rate >= LAYER_1_AMBIGUOUS_BAR
        )


@dataclass
class Layer2Report:
    skill: str
    pass_rate: float
    failures: list[str] = field(default_factory=list)

    @property
    def passed_overall(self) -> bool:
        return self.pass_rate >= LAYER_2_BAR


def load_prompt_set(path: Path) -> PromptSet:
    with path.open() as f:
        data = yaml.safe_load(f)
    return PromptSet(
        skill=data["skill"],
        trigger=data["trigger_prompts"],
        non_trigger=data["non_trigger_prompts"],
        ambiguous=data["ambiguous_prompts"],
    )


def _safe_rate(passed: int, total: int) -> float:
    return 1.0 if total == 0 else passed / total


def score_layer_1(pset: PromptSet, adapter: LLMAdapter) -> Layer1Report:
    failures: list[str] = []

    t_pass = 0
    for p in pset.trigger:
        result = adapter.run(p["prompt"])
        if pset.skill in result.loaded_skills:
            t_pass += 1
        else:
            failures.append(
                f"[trigger] {p['id']} expected {pset.skill}, got {result.loaded_skills}"
            )

    n_pass = 0
    for p in pset.non_trigger:
        result = adapter.run(p["prompt"])
        if pset.skill not in result.loaded_skills:
            n_pass += 1
        else:
            failures.append(f"[non-trigger] {p['id']} {pset.skill} should NOT load")

    a_pass = 0
    for p in pset.ambiguous:
        result = adapter.run(p["prompt"])
        cq = (result.clarifying_question or "").lower()
        keywords = p["expected_clarification_keywords"]
        if cq and any(k.lower() in cq for k in keywords):
            a_pass += 1
        else:
            failures.append(
                f"[ambiguous] {p['id']} expected clarification with one of {keywords}"
            )

    return Layer1Report(
        skill=pset.skill,
        trigger_pass_rate=_safe_rate(t_pass, len(pset.trigger)),
        non_trigger_pass_rate=_safe_rate(n_pass, len(pset.non_trigger)),
        ambiguous_pass_rate=_safe_rate(a_pass, len(pset.ambiguous)),
        failures=failures,
    )


def score_layer_2(pset: PromptSet, adapter: LLMAdapter) -> Layer2Report:
    failures: list[str] = []
    counted = 0
    passed = 0

    for p in pset.trigger:
        expected = set(p.get("expected_anchors") or [])
        if not expected:
            continue
        counted += 1
        result = adapter.run(p["prompt"])
        loaded = set(result.read_paths or [])
        recall = len(loaded & expected) / len(expected)
        precision = (len(loaded & expected) / len(loaded)) if loaded else 0.0
        if recall >= 1.0 and precision >= 0.5:
            passed += 1
        else:
            failures.append(
                f"{p['id']} expected={sorted(expected)} loaded={sorted(loaded)} "
                f"recall={recall:.2f} precision={precision:.2f}"
            )

    return Layer2Report(
        skill=pset.skill,
        pass_rate=_safe_rate(passed, counted),
        failures=failures,
    )


def _build_adapter(name: str) -> LLMAdapter:
    if name == "mock":
        rules: list[MockRule] = []
        for prompt_file in sorted(PROMPTS_DIR.glob("*.yaml")):
            pset = load_prompt_set(prompt_file)
            for p in pset.trigger:
                rules.append(MockRule(
                    prompt_contains=p["prompt"][:30],
                    loaded_skills=[pset.skill],
                    read_paths=p.get("expected_anchors") or [],
                ))
            for p in pset.ambiguous:
                rules.append(MockRule(
                    prompt_contains=p["prompt"][:30],
                    clarifying_question=" ".join(p["expected_clarification_keywords"]),
                ))
        return MockAdapter(rules=rules)
    if name == "claude":
        from evals.harness.adapters.claude import ClaudeAdapter
        return ClaudeAdapter()
    raise SystemExit(f"unknown adapter: {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", default="mock", choices=["mock", "claude"])
    parser.add_argument("--layer", type=int, choices=[1, 2], default=1)
    parser.add_argument("--skill", default=None, help="Run a single skill (default: all)")
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()

    adapter = _build_adapter(args.adapter)
    files = sorted(PROMPTS_DIR.glob("*.yaml"))
    if args.skill:
        files = [f for f in files if f.stem == args.skill]

    all_pass = True
    out: dict[str, dict] = {}

    SKIP_FILES = {"composition"}  # multi-skill format, not a per-skill prompt set

    for f in files:
        if f.stem in SKIP_FILES:
            continue
        pset = load_prompt_set(f)
        if args.layer == 1:
            r = score_layer_1(pset, adapter)
            status = "PASS" if r.passed_overall else "FAIL"
            print(
                f"[L1] {pset.skill}  trigger={r.trigger_pass_rate:.0%}  "
                f"non_trigger={r.non_trigger_pass_rate:.0%}  "
                f"ambiguous={r.ambiguous_pass_rate:.0%}  {status}"
            )
            for line in r.failures:
                print(f"     {line}")
            all_pass = all_pass and r.passed_overall
            out[pset.skill] = {
                "layer": 1,
                "trigger": r.trigger_pass_rate,
                "non_trigger": r.non_trigger_pass_rate,
                "ambiguous": r.ambiguous_pass_rate,
                "passed": r.passed_overall,
            }
        else:
            r = score_layer_2(pset, adapter)
            status = "PASS" if r.passed_overall else "FAIL"
            print(f"[L2] {pset.skill}  pass_rate={r.pass_rate:.0%}  {status}")
            for line in r.failures:
                print(f"     {line}")
            all_pass = all_pass and r.passed_overall
            out[pset.skill] = {
                "layer": 2,
                "pass_rate": r.pass_rate,
                "passed": r.passed_overall,
            }

    if args.write_results:
        day = RESULTS_DIR / date.today().isoformat()
        day.mkdir(parents=True, exist_ok=True)
        result_file = day / f"{args.adapter}.layer{args.layer}.json"
        result_file.write_text(json.dumps(out, indent=2))

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
