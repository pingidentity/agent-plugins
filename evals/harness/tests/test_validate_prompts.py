"""Schema validation tests for evals/prompts/*.yaml."""
import textwrap
from pathlib import Path

import pytest

from evals.harness.validate_prompts import ValidationError, validate_prompt_file


def write_yaml(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(content).strip() + "\n")
    return p


def test_minimal_valid_prompt_set_passes(tmp_path: Path):
    f = write_yaml(tmp_path, "ping-quickstart.yaml", """
        skill: ping-quickstart
        version: 1
        trigger_prompts:
          - id: T-01
            prompt: "Where do I start with Ping Identity?"
            expected_anchors: []
            expected_tier: curated
        non_trigger_prompts:
          - id: N-01
            prompt: "Build me a journey in PingOne ST."
            expected_skill: ping-orchestration
        ambiguous_prompts:
          - id: A-01
            prompt: "I want to add MFA."
            expected_clarification_keywords: ["pingone", "aic"]
    """)
    validate_prompt_file(f)  # no exception = pass


def test_skill_field_must_match_filename(tmp_path: Path):
    f = write_yaml(tmp_path, "ping-foundation.yaml", """
        skill: ping-orchestration
        version: 1
        trigger_prompts: []
        non_trigger_prompts: []
        ambiguous_prompts: []
    """)
    with pytest.raises(ValidationError, match="skill .* must match filename"):
        validate_prompt_file(f)


def test_missing_required_top_level_field_fails(tmp_path: Path):
    f = write_yaml(tmp_path, "ping-orchestration.yaml", """
        skill: ping-orchestration
        trigger_prompts: []
        non_trigger_prompts: []
        ambiguous_prompts: []
    """)
    with pytest.raises(ValidationError, match="version"):
        validate_prompt_file(f)


def test_trigger_prompt_requires_id_and_prompt(tmp_path: Path):
    f = write_yaml(tmp_path, "ping-foundation.yaml", """
        skill: ping-foundation
        version: 1
        trigger_prompts:
          - prompt: "missing id"
            expected_anchors: []
            expected_tier: curated
        non_trigger_prompts: []
        ambiguous_prompts: []
    """)
    with pytest.raises(ValidationError, match="id"):
        validate_prompt_file(f)


def test_expected_tier_enum_enforced(tmp_path: Path):
    f = write_yaml(tmp_path, "ping-foundation.yaml", """
        skill: ping-foundation
        version: 1
        trigger_prompts:
          - id: T-01
            prompt: "test prompt for tier validation"
            expected_anchors: []
            expected_tier: invalid-value
        non_trigger_prompts: []
        ambiguous_prompts: []
    """)
    with pytest.raises(ValidationError, match="expected_tier"):
        validate_prompt_file(f)
