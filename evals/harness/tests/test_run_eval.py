from pathlib import Path
import textwrap

from evals.harness.adapters.mock import MockAdapter, MockRule
from evals.harness.run_eval import score_layer_1, score_layer_2, load_prompt_set


def write(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(content).strip() + "\n")
    return p


def test_layer1_trigger_correct_when_skill_loaded(tmp_path):
    f = write(tmp_path, "ping-quickstart.yaml", """
        skill: ping-quickstart
        version: 1
        trigger_prompts:
          - id: T-01
            prompt: "where do I start with Ping?"
            expected_anchors: []
            expected_tier: curated
        non_trigger_prompts:
          - id: N-01
            prompt: "build me a journey in AIC"
            expected_skill: ping-orchestration
        ambiguous_prompts:
          - id: A-01
            prompt: "I want MFA please"
            expected_clarification_keywords: ["pingone", "aic"]
    """)
    pset = load_prompt_set(f)
    adapter = MockAdapter(rules=[
        MockRule(prompt_contains="where do I start", loaded_skills=["ping-quickstart"]),
        MockRule(prompt_contains="build me a journey", loaded_skills=["ping-orchestration"]),
        MockRule(prompt_contains="I want MFA", clarifying_question="pingone aic mt or st?"),
    ])
    report = score_layer_1(pset, adapter)
    assert report.trigger_pass_rate == 1.0
    assert report.non_trigger_pass_rate == 1.0
    assert report.ambiguous_pass_rate == 1.0
    assert report.passed_overall is True


def test_layer1_trigger_fails_when_wrong_skill_loaded(tmp_path):
    f = write(tmp_path, "ping-quickstart.yaml", """
        skill: ping-quickstart
        version: 1
        trigger_prompts:
          - id: T-01
            prompt: "where do I start with Ping"
            expected_anchors: []
            expected_tier: curated
        non_trigger_prompts: []
        ambiguous_prompts: []
    """)
    pset = load_prompt_set(f)
    adapter = MockAdapter(rules=[
        MockRule(prompt_contains="where do I start", loaded_skills=["ping-foundation"]),
    ])
    report = score_layer_1(pset, adapter)
    assert report.trigger_pass_rate == 0.0
    assert report.passed_overall is False
    assert "T-01" in report.failures[0]


def test_layer2_recall_and_precision(tmp_path):
    anchor = "plugins/ping-identity/skills/ping-orchestration/references/curated/pingone-st/journey-design-patterns.md"
    f = write(tmp_path, "ping-orchestration.yaml", """
        skill: ping-orchestration
        version: 1
        trigger_prompts:
          - id: T-01
            prompt: "build a registration journey in AIC"
            expected_anchors:
              - plugins/ping-identity/skills/ping-orchestration/references/curated/pingone-st/journey-design-patterns.md
            expected_tier: curated
        non_trigger_prompts: []
        ambiguous_prompts: []
    """)
    pset = load_prompt_set(f)

    # recall=1.0, precision=1.0 -> pass
    adapter_pass = MockAdapter(rules=[MockRule(
        prompt_contains="build a registration journey",
        loaded_skills=["ping-orchestration"],
        read_paths=[anchor],
    )])
    rep = score_layer_2(pset, adapter_pass)
    assert rep.pass_rate == 1.0

    # recall=0.0 -> fail
    adapter_miss = MockAdapter(rules=[MockRule(
        prompt_contains="build a registration journey",
        loaded_skills=["ping-orchestration"],
        read_paths=["plugins/ping-identity/skills/ping-orchestration/references/curated/pingone-st/nodes/mfa-nodes.md"],
    )])
    rep = score_layer_2(pset, adapter_miss)
    assert rep.pass_rate == 0.0
