"""Layer 3 (skill execution value) eval runner.

Usage:
  python3 -m evals.harness.run_layer3 \
    --models claude-sonnet-4-6 \
    --skill ping-app-integration \
    --workers 4

Models you list must be runnable: Anthropic models route through
`claude -p` (requires the `claude` CLI on PATH); OpenAI models route
through the OpenAI SDK (requires OPENAI_API_KEY + OPENAI_BASE_URL).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from evals.harness.runners import claude_code_cli, openai_runner
from evals.harness.runners.grading import evaluate_task_checks
from evals.harness.runners.aggregate import RunRecord, write_run_result, aggregate_results

REPO_ROOT = Path(__file__).resolve().parents[2]
TASKS_DIR_DEFAULT = REPO_ROOT / "evals" / "tasks"
RESULTS_DIR_DEFAULT = REPO_ROOT / "evals" / "results"
PLUGIN_DIR = REPO_ROOT / "plugins" / "ping-identity"

ANTHROPIC_PREFIXES = ("claude-", "anthropic.", "eu.", "us.", "ap.")
# Single-word aliases the Claude CLI accepts (haiku, sonnet, opus, fast)
ANTHROPIC_ALIASES = frozenset({"haiku", "sonnet", "opus", "fast"})
OPENAI_PREFIXES = ("gpt-", "o1", "o3", "openai.")


def _is_anthropic(model: str) -> bool:
    return model in ANTHROPIC_ALIASES or model.startswith(ANTHROPIC_PREFIXES)


def _is_openai(model: str) -> bool:
    return model.startswith(OPENAI_PREFIXES)


@dataclass
class RunSpec:
    task: dict
    model: str
    config: str  # "with_skill" | "without_skill"


def discover_tasks(tasks_dir: Path) -> list[dict]:
    tasks: list[dict] = []
    for p in sorted(tasks_dir.rglob("*.yaml")):
        with p.open() as f:
            data = yaml.safe_load(f)
        tasks.append(data)
    return tasks


def build_run_matrix(
    tasks: list[dict], *, models: list[str], skill: str | None = None,
) -> list[RunSpec]:
    selected = [t for t in tasks if skill is None or t["skill"] == skill]
    out: list[RunSpec] = []
    for t in selected:
        for m in models:
            for cfg in ("with_skill", "without_skill"):
                out.append(RunSpec(task=t, model=m, config=cfg))
    return out


def _git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


def execute_one(spec: RunSpec, *, max_turns: int, timeout_s: int) -> RunRecord:
    task = spec.task
    with tempfile.TemporaryDirectory(prefix="layer3-") as td:
        workdir = Path(td)
        if _is_anthropic(spec.model):
            outcome = claude_code_cli.run_in_workdir(
                prompt=task["prompt"], model=spec.model, config=spec.config,
                plugin_dir=PLUGIN_DIR, workdir=workdir,
                max_turns=max_turns, timeout_seconds=timeout_s,
            )
        elif _is_openai(spec.model):
            outcome = openai_runner.run_in_workdir(
                prompt=task["prompt"], model=spec.model, config=spec.config,
                skill=task["skill"], workdir=workdir, timeout_seconds=timeout_s,
            )
        else:
            return RunRecord(
                skill=task["skill"], task_id=task["id"], pass_rate=0.0,
                checks_passed=0, checks_total=len(task["deterministic_checks"]),
                tokens_input=0, tokens_output=0, duration_seconds=0.0, turn_count=0,
                error=f"unsupported_model:{spec.model}",
            )

        summary = evaluate_task_checks(task["deterministic_checks"], workdir)
        all_pass = all(r.passed for r in summary.results)

        rubric = task.get("judge_rubric") or {}
        judge_scores = None
        rubric_pass = True
        if rubric.get("enabled"):
            from evals.harness.runners.grading import judge_task
            artifact_files = sorted(
                p for g in task["expected_artifacts"]
                for p in workdir.glob(g) if p.is_file()
            )
            try:
                scores, weighted = judge_task(
                    task_prompt=task["prompt"], rubric=rubric,
                    artifact_files=artifact_files,
                    judge_model=rubric.get("judge_model", "gpt-5.5"),
                )
                judge_scores = scores
                rubric_pass = weighted >= rubric.get("pass_threshold", 0.75)
            except Exception as exc:
                judge_scores = [{"name": "<judge_error>", "score": 0.0,
                                 "justification": f"{type(exc).__name__}: {exc}"}]
                rubric_pass = False

        passed = all_pass and rubric_pass

        return RunRecord(
            skill=task["skill"], task_id=task["id"],
            pass_rate=1.0 if passed else 0.0,
            checks_passed=summary.checks_passed, checks_total=summary.checks_total,
            tokens_input=outcome.tokens_input, tokens_output=outcome.tokens_output,
            duration_seconds=round(outcome.duration_ms / 1000.0, 1),
            turn_count=outcome.turn_count,
            deterministic_checks=[
                {"id": r.id, "passed": r.passed, "evidence": r.evidence}
                for r in summary.results
            ],
            judge_scores=judge_scores,
            error=outcome.error,
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", required=True,
                        help="Model IDs (e.g. claude-sonnet-4-6 gpt-5.5)")
    parser.add_argument("--skill", default=None,
                        help="Restrict to one skill (default: all)")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-turns", type=int, default=30)
    parser.add_argument("--timeout-s", type=int, default=600)
    parser.add_argument("--tasks-dir", type=Path, default=TASKS_DIR_DEFAULT)
    parser.add_argument("--results-dir", type=Path, default=RESULTS_DIR_DEFAULT)
    parser.add_argument("--write-summary", action="store_true",
                        help="Run aggregate over results dir and write summary.json")
    args = parser.parse_args(argv)

    workers = max(1, min(8, args.workers))
    tasks = discover_tasks(args.tasks_dir)
    matrix = build_run_matrix(tasks, models=args.models, skill=args.skill)
    if not matrix:
        print("No runs to execute", file=sys.stderr)
        return 1

    print(f"Executing {len(matrix)} runs with {workers} worker(s)")
    plugin_sha = _git_sha()
    by_model_cfg: dict[tuple[str, str], list[RunRecord]] = {}

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(execute_one, s, max_turns=args.max_turns, timeout_s=args.timeout_s): s
                   for s in matrix}
        for fut in as_completed(futures):
            spec = futures[fut]
            try:
                record = fut.result()
            except Exception as exc:
                t = spec.task
                record = RunRecord(
                    skill=t["skill"], task_id=t["id"], pass_rate=0.0,
                    checks_passed=0, checks_total=len(t["deterministic_checks"]),
                    tokens_input=0, tokens_output=0, duration_seconds=0.0, turn_count=0,
                    error=f"runner_exception:{type(exc).__name__}",
                )
            print(f"  [{spec.model} | {spec.config}] {record.skill}/{record.task_id} "
                  f"pass={record.pass_rate:.0%} tokens={record.tokens_input + record.tokens_output} "
                  f"err={record.error}")
            by_model_cfg.setdefault((spec.model, spec.config), []).append(record)

    day = date.today().isoformat()
    for (model, cfg), records in by_model_cfg.items():
        write_run_result(
            results_dir=args.results_dir, date_str=day,
            model=model, config=cfg, records=records, plugin_sha=plugin_sha,
        )

    if args.write_summary:
        layer3_dir = args.results_dir / day / "layer3"
        summary = aggregate_results(layer3_dir)
        (layer3_dir / "summary.json").write_text(json.dumps(summary, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
