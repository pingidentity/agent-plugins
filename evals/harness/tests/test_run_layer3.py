from pathlib import Path
import yaml

from evals.harness.run_layer3 import (
    discover_tasks, build_run_matrix, RunSpec,
)


def _write_task(root: Path, skill: str, task_id: str) -> Path:
    sd = root / skill
    sd.mkdir(parents=True, exist_ok=True)
    p = sd / f"{task_id}.yaml"
    p.write_text(yaml.safe_dump({
        "id": task_id,
        "skill": skill,
        "title": "x",
        "prompt": "do the thing properly please",
        "expected_artifacts": ["**/*"],
        "deterministic_checks": [
            {"id": "c1", "description": "has a thing", "type": "grep",
             "glob": "**/*", "pattern": "thing", "must_match": True}
        ],
        "judge_rubric": {"enabled": False},
    }))
    return p


def test_discover_tasks(tmp_path):
    _write_task(tmp_path, "ping-app-integration", "01-a")
    _write_task(tmp_path, "ping-app-integration", "02-b")
    _write_task(tmp_path, "ping-orchestration", "01-c")
    discovered = discover_tasks(tmp_path)
    assert {(t["skill"], t["id"]) for t in discovered} == {
        ("ping-app-integration", "01-a"),
        ("ping-app-integration", "02-b"),
        ("ping-orchestration", "01-c"),
    }


def test_build_run_matrix_expands_models_and_configs(tmp_path):
    _write_task(tmp_path, "ping-app-integration", "01-a")
    tasks = discover_tasks(tmp_path)
    matrix = build_run_matrix(tasks, models=["claude-sonnet-4-6", "gpt-5.5"])
    # 1 task × 2 models × 2 configs = 4
    assert len(matrix) == 4
    configs = {(s.model, s.config) for s in matrix}
    assert configs == {
        ("claude-sonnet-4-6", "with_skill"),
        ("claude-sonnet-4-6", "without_skill"),
        ("gpt-5.5", "with_skill"),
        ("gpt-5.5", "without_skill"),
    }
    assert all(isinstance(s, RunSpec) for s in matrix)


def test_build_run_matrix_filters_by_skill(tmp_path):
    _write_task(tmp_path, "ping-app-integration", "01-a")
    _write_task(tmp_path, "ping-orchestration", "01-c")
    tasks = discover_tasks(tmp_path)
    matrix = build_run_matrix(tasks, models=["claude-sonnet-4-6"], skill="ping-app-integration")
    assert len(matrix) == 2
    assert {s.task["skill"] for s in matrix} == {"ping-app-integration"}
