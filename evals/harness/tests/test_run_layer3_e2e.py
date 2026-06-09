import json
from pathlib import Path
import yaml

from evals.harness import run_layer3
from evals.harness.runners.claude_code_cli import RunOutcome


def _write_task(root: Path, skill: str, task_id: str) -> None:
    (root / skill).mkdir(parents=True, exist_ok=True)
    (root / skill / f"{task_id}.yaml").write_text(yaml.safe_dump({
        "id": task_id, "skill": skill, "title": "smoke",
        "prompt": "write a kotlin file that prints davinci",
        "expected_artifacts": ["**/*.kt"],
        "deterministic_checks": [
            {"id": "c1", "description": "prints davinci", "type": "grep",
             "glob": "**/*.kt", "pattern": "davinci", "must_match": True}
        ],
        "judge_rubric": {"enabled": False},
    }))


def test_e2e_with_fake_runner(tmp_path, monkeypatch):
    tasks_dir = tmp_path / "tasks"
    results_dir = tmp_path / "results"
    _write_task(tasks_dir, "ping-app-integration", "01-x")

    def fake_run(*, prompt, model, config, plugin_dir, workdir, max_turns, timeout_seconds):
        # Pretend the agent wrote a file
        (Path(workdir) / "Out.kt").write_text("fun main() = println(\"davinci\")\n")
        return RunOutcome(
            tokens_input=1000,
            tokens_output=500,
            duration_ms=5000,
            turn_count=2,
            final_message="done",
        )
    monkeypatch.setattr(run_layer3.claude_code_cli, "run_in_workdir", fake_run)

    rc = run_layer3.main([
        "--models", "claude-sonnet-4-6",
        "--workers", "1",
        "--tasks-dir", str(tasks_dir),
        "--results-dir", str(results_dir),
        "--write-summary",
    ])
    assert rc == 0

    written = list(results_dir.rglob("*.json"))
    assert any("with_skill" in p.name for p in written)
    assert any("without_skill" in p.name for p in written)
    summary = next(p for p in written if p.name == "summary.json")
    data = json.loads(summary.read_text())
    cell = data["by_skill_model_config"]["ping-app-integration"]["claude-sonnet-4-6"]
    assert cell["with_skill"]["pass_rate"] == 1.0
    assert cell["without_skill"]["pass_rate"] == 1.0
