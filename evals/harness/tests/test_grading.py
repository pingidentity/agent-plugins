import json
from pathlib import Path
from evals.harness.runners.grading import (
    evaluate_check, evaluate_task_checks, CheckResult,
)


def _write(tmp_path: Path, rel: str, content: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return p


def test_grep_match_passes(tmp_path):
    _write(tmp_path, "AuthViewModel.kt", "import com.pingidentity.davinci.module.Oidc\n")
    check = {"id": "c1", "description": "uses davinci",
             "type": "grep", "glob": "**/*.kt",
             "pattern": "com.pingidentity.davinci.module.Oidc", "must_match": True}
    r = evaluate_check(check, tmp_path)
    assert r.passed is True
    assert "AuthViewModel.kt" in r.evidence


def test_grep_miss_fails(tmp_path):
    _write(tmp_path, "AuthViewModel.kt", "// nothing relevant here\n")
    check = {"id": "c1", "description": "uses davinci",
             "type": "grep", "glob": "**/*.kt",
             "pattern": "davinci", "must_match": True}
    r = evaluate_check(check, tmp_path)
    assert r.passed is False
    assert "no match" in r.evidence.lower()


def test_not_contains_passes_when_absent(tmp_path):
    _write(tmp_path, "x.kt", "import com.pingidentity.davinci.module.Oidc\n")
    check = {"id": "c1", "description": "no journey",
             "type": "not_contains", "glob": "**/*.kt",
             "pattern": "com.pingidentity.journey.module.Oidc"}
    r = evaluate_check(check, tmp_path)
    assert r.passed is True


def test_not_contains_fails_when_present(tmp_path):
    _write(tmp_path, "x.kt", "import com.pingidentity.journey.module.Oidc\n")
    check = {"id": "c1", "description": "no journey",
             "type": "not_contains", "glob": "**/*.kt",
             "pattern": "com.pingidentity.journey.module.Oidc"}
    r = evaluate_check(check, tmp_path)
    assert r.passed is False


def test_regex_with_flags(tmp_path):
    _write(tmp_path, "Auth.kt", "ContinueNode\nSuccessNode\nErrorNode\nFailureNode\n")
    check = {"id": "c1", "description": "all branches",
             "type": "regex", "glob": "**/*.kt",
             "pattern": "ContinueNode.*SuccessNode.*ErrorNode.*FailureNode",
             "flags": "ms", "must_match": True}
    r = evaluate_check(check, tmp_path)
    assert r.passed is True


def test_file_exists(tmp_path):
    _write(tmp_path, "subdir/AuthScreen.kt", "")
    check = {"id": "c1", "description": "screen file present",
             "type": "file_exists", "glob": "**/AuthScreen.kt"}
    r = evaluate_check(check, tmp_path)
    assert r.passed is True


def test_evaluate_task_checks_all_pass_returns_pass_rate_1(tmp_path):
    _write(tmp_path, "x.kt", "import com.pingidentity.davinci.module.Oidc\n")
    checks = [
        {"id": "c1", "description": "d1", "type": "grep",
         "glob": "**/*.kt", "pattern": "davinci", "must_match": True},
        {"id": "c2", "description": "d2", "type": "not_contains",
         "glob": "**/*.kt", "pattern": "journey"},
    ]
    summary = evaluate_task_checks(checks, tmp_path)
    assert summary.checks_passed == 2
    assert summary.checks_total == 2
    assert summary.pass_rate == 1.0


def test_json_path_dotted_key_match(tmp_path):
    (tmp_path / "config.json").write_text(json.dumps({"app": {"name": "demo"}}))
    check = {"id": "c1", "description": "app name is demo",
             "type": "json_path", "path": "config.json",
             "json_path": "$.app.name", "expected": "demo"}
    r = evaluate_check(check, tmp_path)
    assert r.passed is True


def test_json_path_index_traversal(tmp_path):
    (tmp_path / "data.json").write_text(json.dumps({"users": [{"id": 1}, {"id": 2}]}))
    check = {"id": "c1", "description": "second user id is 2",
             "type": "json_path", "path": "data.json",
             "json_path": "$.users[1].id", "expected": 2}
    r = evaluate_check(check, tmp_path)
    assert r.passed is True


def test_json_path_distinguishes_null_value_from_missing_key(tmp_path):
    """Regression test: a literal null must not be reported as missing."""
    (tmp_path / "data.json").write_text(json.dumps({"disabled": None}))
    check = {"id": "c1", "description": "disabled is null",
             "type": "json_path", "path": "data.json",
             "json_path": "$.disabled", "expected": None}
    r = evaluate_check(check, tmp_path)
    assert r.passed is True
    assert "got None" not in r.evidence  # should not have flowed into the mismatch branch


def test_json_path_missing_key_fails(tmp_path):
    (tmp_path / "data.json").write_text(json.dumps({"present": 1}))
    check = {"id": "c1", "description": "absent key",
             "type": "json_path", "path": "data.json",
             "json_path": "$.absent", "expected": "anything"}
    r = evaluate_check(check, tmp_path)
    assert r.passed is False
    assert "path not found" in r.evidence


def test_json_path_value_mismatch(tmp_path):
    (tmp_path / "data.json").write_text(json.dumps({"app": {"version": "1.0"}}))
    check = {"id": "c1", "description": "version is 2",
             "type": "json_path", "path": "data.json",
             "json_path": "$.app.version", "expected": "2.0"}
    r = evaluate_check(check, tmp_path)
    assert r.passed is False
    assert "1.0" in r.evidence and "2.0" in r.evidence
