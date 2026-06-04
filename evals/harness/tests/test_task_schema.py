import json
from pathlib import Path
import yaml
from jsonschema import Draft7Validator

REPO = Path(__file__).resolve().parents[3]
SCHEMA = REPO / "evals" / "schemas" / "task.schema.json"


def _validator():
    with SCHEMA.open() as f:
        return Draft7Validator(json.load(f))


def test_minimal_task_validates():
    data = {
        "id": "01-example",
        "skill": "ping-app-integration",
        "title": "Example",
        "prompt": "Do the thing.",
        "expected_artifacts": ["**/*.kt"],
        "deterministic_checks": [
            {
                "id": "uses-foo",
                "description": "Uses foo",
                "type": "grep",
                "glob": "**/*.kt",
                "pattern": "foo",
                "must_match": True,
            }
        ],
        "judge_rubric": {"enabled": False},
    }
    errors = list(_validator().iter_errors(data))
    assert errors == []


def test_missing_required_field_fails():
    data = {"id": "01", "skill": "x", "title": "t", "prompt": "p"}
    errors = list(_validator().iter_errors(data))
    assert errors  # missing expected_artifacts, deterministic_checks


def test_unknown_check_type_fails():
    data = {
        "id": "01-x",
        "skill": "ping-app-integration",
        "title": "t",
        "prompt": "p",
        "expected_artifacts": ["**/*"],
        "deterministic_checks": [
            {"id": "c1", "description": "d", "type": "wibble", "glob": "**/*", "pattern": "x"}
        ],
        "judge_rubric": {"enabled": False},
    }
    errors = list(_validator().iter_errors(data))
    assert errors


def test_real_task_file_validates():
    """The first authored task must validate."""
    f = REPO / "evals" / "tasks" / "ping-app-integration" / "01-davinci-android-full-flow.yaml"
    with f.open() as fh:
        data = yaml.safe_load(fh)
    errors = list(_validator().iter_errors(data))
    assert errors == [], errors
