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
