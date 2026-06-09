from pathlib import Path
from evals.harness.runners.grading import build_judge_prompt


def test_judge_prompt_includes_rubric_and_output(tmp_path):
    rubric = {
        "enabled": True,
        "criteria": [
            {"name": "completeness", "description": "covers all steps", "weight": 0.5},
            {"name": "correctness",  "description": "no bad advice",     "weight": 0.5},
        ],
        "pass_threshold": 0.75,
        "judge_model": "gpt-5.5",
    }
    (tmp_path / "answer.md").write_text("# Setup\n1) Step one\n2) Step two\n")
    prompt = build_judge_prompt(
        task_prompt="Explain Ping setup",
        rubric=rubric,
        artifact_files=[tmp_path / "answer.md"],
    )
    assert "completeness" in prompt
    assert "correctness" in prompt
    assert "Step one" in prompt
    assert "JSON" in prompt or "json" in prompt
