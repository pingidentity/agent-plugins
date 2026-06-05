"""Deterministic check evaluator for Layer 3 tasks.

Pure module: no network, no subprocesses. Reads files under workdir
matching each check's glob, applies the rule, returns CheckResult.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CheckResult:
    id: str
    passed: bool
    evidence: str


@dataclass
class CheckSummary:
    results: list[CheckResult]

    @property
    def checks_passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def checks_total(self) -> int:
        return len(self.results)

    @property
    def pass_rate(self) -> float:
        return 1.0 if not self.results else self.checks_passed / self.checks_total


def _files_matching(workdir: Path, glob: str) -> list[Path]:
    return sorted(p for p in workdir.glob(glob) if p.is_file())


def _re_flags(spec: str | None) -> int:
    if not spec:
        return 0
    flags = 0
    for ch in spec:
        if ch == "m": flags |= re.MULTILINE
        elif ch == "s": flags |= re.DOTALL
        elif ch == "i": flags |= re.IGNORECASE
    return flags


def evaluate_check(check: dict, workdir: Path) -> CheckResult:
    cid = check["id"]
    ctype = check["type"]

    if ctype in ("grep", "regex"):
        glob = check["glob"]
        pattern = check["pattern"]
        must_match = check.get("must_match", True)
        files = _files_matching(workdir, glob)
        if ctype == "regex":
            rx = re.compile(pattern, _re_flags(check.get("flags")))
            hit = next(((f, m) for f in files for m in [rx.search(f.read_text(errors="replace"))] if m), None)
        else:
            hit = next(((f, pattern) for f in files if pattern in f.read_text(errors="replace")), None)
        if hit and must_match:
            return CheckResult(cid, True, f"matched in {hit[0].relative_to(workdir)}")
        if not hit and not must_match:
            return CheckResult(cid, True, f"no match across {len(files)} files (as required)")
        return CheckResult(
            cid,
            False,
            f"no match across {len(files)} file(s) matching {glob!r}"
            if must_match
            else f"unexpected match in {hit[0].relative_to(workdir)}",
        )

    if ctype == "not_contains":
        glob = check["glob"]
        pattern = check["pattern"]
        files = _files_matching(workdir, glob)
        offender = next((f for f in files if pattern in f.read_text(errors="replace")), None)
        if offender is None:
            return CheckResult(cid, True, f"absent across {len(files)} file(s)")
        return CheckResult(cid, False, f"forbidden pattern present in {offender.relative_to(workdir)}")

    if ctype == "file_exists":
        glob = check["glob"]
        files = _files_matching(workdir, glob)
        if files:
            return CheckResult(cid, True, f"found {files[0].relative_to(workdir)}")
        return CheckResult(cid, False, f"no file matching {glob!r}")

    if ctype == "json_path":
        import json
        path = workdir / check["path"]
        if not path.exists():
            return CheckResult(cid, False, f"missing {check['path']}")
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            return CheckResult(cid, False, f"invalid JSON: {exc}")
        # Minimal jsonpath: dotted keys + [n] indices
        cursor = data
        for part in re.split(r"\.|(?=\[)", check["json_path"].lstrip("$.")):
            if not part:
                continue
            if part.startswith("[") and part.endswith("]"):
                try:
                    cursor = cursor[int(part[1:-1])]
                except (KeyError, IndexError, TypeError):
                    return CheckResult(cid, False, f"path not found: {check['json_path']}")
            else:
                if isinstance(cursor, dict) and part in cursor:
                    cursor = cursor[part]
                else:
                    return CheckResult(cid, False, f"path not found: {check['json_path']}")
        if "expected" in check and cursor != check["expected"]:
            return CheckResult(cid, False, f"got {cursor!r}, expected {check['expected']!r}")
        return CheckResult(cid, True, f"value at {check['json_path']} = {cursor!r}")

    return CheckResult(cid, False, f"unknown check type: {ctype}")


def evaluate_task_checks(checks: list[dict], workdir: Path) -> CheckSummary:
    return CheckSummary(results=[evaluate_check(c, workdir) for c in checks])
