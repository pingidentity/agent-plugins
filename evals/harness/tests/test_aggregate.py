import json
from pathlib import Path
from evals.harness.runners.aggregate import (
    write_run_result, RunRecord, aggregate_results,
)


def _make_record(skill, task_id, pass_rate=1.0, tokens_total=10_000, duration_seconds=100.0):
    return RunRecord(
        skill=skill, task_id=task_id, pass_rate=pass_rate,
        checks_passed=int(pass_rate * 5), checks_total=5,
        tokens_input=int(tokens_total * 0.8),
        tokens_output=int(tokens_total * 0.2),
        duration_seconds=duration_seconds,
        turn_count=4, deterministic_checks=[], judge_scores=None,
        error=None,
    )


def test_write_and_read_run_result(tmp_path):
    records = [
        _make_record("ping-app-integration", "01-x"),
        _make_record("ping-orchestration", "02-y", pass_rate=0.6, tokens_total=20000),
    ]
    out = write_run_result(
        results_dir=tmp_path, date_str="2026-06-04",
        model="claude-sonnet-4-6", config="with_skill",
        records=records, plugin_sha="abc1234",
    )
    assert out.exists()
    data = json.loads(out.read_text())
    assert data["metadata"]["model"] == "claude-sonnet-4-6"
    assert data["metadata"]["config"] == "with_skill"
    assert data["metadata"]["ping_identity_plugin_sha"] == "abc1234"
    assert data["metadata"]["harness_version"] == "layer3-v1"
    assert len(data["runs"]) == 2
    assert data["runs"][0]["tokens_total"] == 10_000


def test_aggregate_combines_with_and_without_skill(tmp_path):
    layer3_dir = tmp_path / "2026-06-04" / "layer3"
    layer3_dir.mkdir(parents=True)

    (layer3_dir / "claude-sonnet-4-6.with_skill.json").write_text(json.dumps({
        "metadata": {"model": "claude-sonnet-4-6", "config": "with_skill"},
        "runs": [
            {"skill": "ping-app-integration", "task_id": "01", "pass_rate": 1.0,
             "tokens_total": 20000, "duration_seconds": 100.0},
            {"skill": "ping-app-integration", "task_id": "02", "pass_rate": 1.0,
             "tokens_total": 22000, "duration_seconds": 110.0},
        ],
    }))
    (layer3_dir / "claude-sonnet-4-6.without_skill.json").write_text(json.dumps({
        "metadata": {"model": "claude-sonnet-4-6", "config": "without_skill"},
        "runs": [
            {"skill": "ping-app-integration", "task_id": "01", "pass_rate": 0.6,
             "tokens_total": 30000, "duration_seconds": 130.0},
            {"skill": "ping-app-integration", "task_id": "02", "pass_rate": 0.4,
             "tokens_total": 32000, "duration_seconds": 150.0},
        ],
    }))

    summary = aggregate_results(layer3_dir)
    cell = summary["by_skill_model_config"]["ping-app-integration"]["claude-sonnet-4-6"]
    assert cell["with_skill"]["pass_rate"] == 1.0
    assert cell["without_skill"]["pass_rate"] == 0.5
    assert cell["delta"]["pass_rate"] == "+0.50"
    # token mean delta: 21000 - 31000 = -10000
    assert cell["delta"]["tokens"] == "-10000"
    assert summary["aggregate_by_model"]["claude-sonnet-4-6"]["with_skill_pass"] == 1.0
    assert summary["aggregate_by_model"]["claude-sonnet-4-6"]["without_skill_pass"] == 0.5
