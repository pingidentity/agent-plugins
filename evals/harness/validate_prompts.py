"""Validate evals/prompts/*.yaml files against the prompt-set JSON schema."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

import yaml
from jsonschema import Draft7Validator

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "evals" / "schemas" / "prompt-set.schema.json"
PROMPTS_DIR = REPO_ROOT / "evals" / "prompts"
TASK_SCHEMA_PATH = REPO_ROOT / "evals" / "schemas" / "task.schema.json"
TASKS_DIR = REPO_ROOT / "evals" / "tasks"


class ValidationError(Exception):
    pass


def _load_schema(schema_path: Path) -> dict:
    with schema_path.open() as f:
        return json.load(f)


def _validate_against_schema(path: Path, schema_path: Path) -> dict:
    with path.open() as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValidationError(f"{path}: top-level must be a mapping")

    schema = _load_schema(schema_path)
    errors = sorted(Draft7Validator(schema).iter_errors(data), key=lambda e: e.path)
    if errors:
        msgs = "; ".join(
            f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors
        )
        raise ValidationError(f"{path}: {msgs}")

    return data


def validate_prompt_file(path: Path) -> None:
    data = _validate_against_schema(path, SCHEMA_PATH)
    expected_skill = path.stem
    if data["skill"] != expected_skill:
        raise ValidationError(
            f"{path}: skill '{data['skill']}' must match filename '{expected_skill}'"
        )


def validate_task_file(path: Path) -> None:
    data = _validate_against_schema(path, TASK_SCHEMA_PATH)
    expected_skill = path.parent.name
    if data["skill"] != expected_skill:
        raise ValidationError(
            f"{path}: skill '{data['skill']}' must match parent directory '{expected_skill}'"
        )


SKIP_VALIDATION = {"composition"}  # composition.yaml uses a different schema (multi-skill)


def validate_all(paths: Iterable[Path] | None = None) -> list[Path]:
    paths = list(paths) if paths is not None else sorted(PROMPTS_DIR.glob("*.yaml"))
    failed: list[Path] = []
    for p in paths:
        if p.stem in SKIP_VALIDATION:
            print(f"SKIP {p.relative_to(REPO_ROOT)} (composition schema)")
            continue
        try:
            validate_prompt_file(p)
            print(f"OK  {p.relative_to(REPO_ROOT)}")
        except ValidationError as exc:
            failed.append(p)
            print(f"FAIL {exc}", file=sys.stderr)
    return failed


def validate_all_tasks() -> list[Path]:
    failed: list[Path] = []
    if not TASKS_DIR.exists():
        return failed
    for p in sorted(TASKS_DIR.rglob("*.yaml")):
        try:
            validate_task_file(p)
            print(f"OK  {p.relative_to(REPO_ROOT)}")
        except ValidationError as exc:
            failed.append(p)
            print(f"FAIL {exc}", file=sys.stderr)
    return failed


def main() -> int:
    failed = validate_all() + validate_all_tasks()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
