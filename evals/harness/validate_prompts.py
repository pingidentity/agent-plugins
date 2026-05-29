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


class ValidationError(Exception):
    pass


def _load_schema() -> dict:
    with SCHEMA_PATH.open() as f:
        return json.load(f)


def validate_prompt_file(path: Path) -> None:
    with path.open() as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValidationError(f"{path}: top-level must be a mapping")

    schema = _load_schema()
    errors = sorted(Draft7Validator(schema).iter_errors(data), key=lambda e: e.path)
    if errors:
        msgs = "; ".join(
            f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors
        )
        raise ValidationError(f"{path}: {msgs}")

    expected_skill = path.stem
    if data["skill"] != expected_skill:
        raise ValidationError(
            f"{path}: skill '{data['skill']}' must match filename '{expected_skill}'"
        )


def validate_all(paths: Iterable[Path] | None = None) -> list[Path]:
    paths = list(paths) if paths is not None else sorted(PROMPTS_DIR.glob("*.yaml"))
    failed: list[Path] = []
    for p in paths:
        try:
            validate_prompt_file(p)
            print(f"OK  {p.relative_to(REPO_ROOT)}")
        except ValidationError as exc:
            failed.append(p)
            print(f"FAIL {exc}", file=sys.stderr)
    return failed


def main() -> int:
    failed = validate_all()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
