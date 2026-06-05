"""Layer 3 result writer and summary aggregator."""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path

HARNESS_VERSION = "layer3-v1"


@dataclass
class RunRecord:
    skill: str
    task_id: str
    pass_rate: float
    checks_passed: int
    checks_total: int
    tokens_input: int
    tokens_output: int
    duration_seconds: float
    turn_count: int
    deterministic_checks: list = field(default_factory=list)
    judge_scores: object = None
    error: object = None

    @property
    def tokens_total(self) -> int:
        return self.tokens_input + self.tokens_output

    def to_json(self) -> dict:
        d = asdict(self)
        d["tokens_total"] = self.tokens_total
        return d


def write_run_result(
    *, results_dir: Path, date_str: str, model: str, config: str,
    records: list, plugin_sha: str,
) -> Path:
    out_dir = results_dir / date_str / "layer3"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{model}.{config}.json"
    body = {
        "metadata": {
            "model": model,
            "config": config,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "harness_version": HARNESS_VERSION,
            "ping_identity_plugin_sha": plugin_sha,
        },
        "runs": [r.to_json() for r in records],
    }
    out_path.write_text(json.dumps(body, indent=2))
    return out_path


def _mean(values: list) -> float:
    return sum(values) / len(values) if values else 0.0


def aggregate_results(layer3_dir: Path) -> dict:
    """Combine all <model>.<config>.json into summary.json shape."""
    files = sorted(layer3_dir.glob("*.json"))
    files = [f for f in files if f.stem != "summary"]

    # cells[skill][model][config] = list of run dicts
    cells: dict = {}
    by_model_config: dict = {}

    for f in files:
        data = json.loads(f.read_text())
        meta = data["metadata"]
        model = meta["model"]
        config = meta["config"]
        for run in data["runs"]:
            cells.setdefault(run["skill"], {}).setdefault(model, {}).setdefault(config, []).append(run)
            by_model_config.setdefault(model, {}).setdefault(config, []).append(run["pass_rate"])

    by_skill_model_config: dict = {}
    for skill, by_model in cells.items():
        by_skill_model_config[skill] = {}
        for model, by_cfg in by_model.items():
            entry = {}
            for cfg in ("with_skill", "without_skill"):
                runs = by_cfg.get(cfg, [])
                if not runs:
                    continue
                entry[cfg] = {
                    "pass_rate": round(_mean([r["pass_rate"] for r in runs]), 4),
                    "tokens_mean": int(round(_mean([r.get("tokens_total", 0) for r in runs]))),
                    "duration_mean_s": round(_mean([r.get("duration_seconds", 0.0) for r in runs]), 1),
                    "n": len(runs),
                }
            if "with_skill" in entry and "without_skill" in entry:
                w, b = entry["with_skill"], entry["without_skill"]
                entry["delta"] = {
                    "pass_rate": f"{w['pass_rate'] - b['pass_rate']:+.2f}",
                    "tokens": f"{w['tokens_mean'] - b['tokens_mean']:+d}",
                    "duration_s": f"{w['duration_mean_s'] - b['duration_mean_s']:+.1f}",
                }
            by_skill_model_config[skill][model] = entry

    aggregate_by_model: dict = {}
    for model, by_cfg in by_model_config.items():
        agg = {}
        if "with_skill" in by_cfg:
            agg["with_skill_pass"] = round(_mean(by_cfg["with_skill"]), 4)
        if "without_skill" in by_cfg:
            agg["without_skill_pass"] = round(_mean(by_cfg["without_skill"]), 4)
        aggregate_by_model[model] = agg

    return {
        "by_skill_model_config": by_skill_model_config,
        "aggregate_by_model": aggregate_by_model,
    }
