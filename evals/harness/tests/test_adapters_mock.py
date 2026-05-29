from evals.harness.adapters.mock import MockAdapter, MockRule


def test_mock_adapter_returns_loaded_skills_per_rule():
    rules = [
        MockRule(prompt_contains="MFA", loaded_skills=["ping-quickstart"], read_paths=[]),
        MockRule(
            prompt_contains="journey",
            loaded_skills=["ping-orchestration"],
            read_paths=[
                "plugins/ping-identity/skills/ping-orchestration/references/curated/pingone-st/journey-design-patterns.md"
            ],
        ),
    ]
    adapter = MockAdapter(rules=rules, default_skills=[])

    r1 = adapter.run("I want to add MFA to my mobile banking app.")
    assert r1.loaded_skills == ["ping-quickstart"]
    assert r1.read_paths == []
    assert r1.final_message != ""

    r2 = adapter.run("Build a registration journey with email OTP.")
    assert r2.loaded_skills == ["ping-orchestration"]
    assert r2.read_paths == [
        "plugins/ping-identity/skills/ping-orchestration/references/curated/pingone-st/journey-design-patterns.md"
    ]


def test_mock_adapter_default_when_no_rule_matches():
    adapter = MockAdapter(rules=[], default_skills=[])
    r = adapter.run("a prompt that matches nothing at all")
    assert r.loaded_skills == []
    assert r.read_paths == []


def test_mock_adapter_supports_clarification_for_ambiguous_prompts():
    rules = [
        MockRule(
            prompt_contains="add MFA",
            clarifying_question="Are you in PingOne MT, AIC, or on-prem? Workforce or CIAM?",
        ),
    ]
    adapter = MockAdapter(rules=rules, default_skills=[])
    r = adapter.run("I want to add MFA.")
    assert r.loaded_skills == []
    assert r.clarifying_question is not None
    assert any(k in r.clarifying_question.lower() for k in ["pingone", "aic", "ciam", "workforce"])
