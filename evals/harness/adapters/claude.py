"""Claude (Anthropic) adapter — Phase 1 implementation.

Phase 0 ships this as a stub so `--adapter claude` exits with a clear,
actionable message rather than an ImportError.
"""
from __future__ import annotations

import os

from evals.harness.adapters.base import RunResult


class ClaudeAdapter:
    def __init__(self) -> None:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise SystemExit(
                "ANTHROPIC_API_KEY not set. Phase 1 wires real Claude calls — "
                "for now the mock adapter is the only fully implemented driver. "
                "See evals/harness/run_eval.py."
            )
        raise SystemExit(
            "ClaudeAdapter is a Phase 0 stub. Phase 1 implements: "
            "register skills/* as available skills, capture Skill() and Read() "
            "tool calls, return RunResult. See PLAN.md Phase 1."
        )

    def run(self, prompt: str) -> RunResult:  # pragma: no cover
        raise NotImplementedError
