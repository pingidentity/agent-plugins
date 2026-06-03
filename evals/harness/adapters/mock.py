"""Deterministic mock adapter for harness self-tests."""
from __future__ import annotations

from dataclasses import dataclass, field

from evals.harness.adapters.base import RunResult


@dataclass
class MockRule:
    prompt_contains: str
    loaded_skills: list[str] = field(default_factory=list)
    read_paths: list[str] = field(default_factory=list)
    clarifying_question: str | None = None
    final_message: str = "[mock plan]"


class MockAdapter:
    def __init__(self, rules: list[MockRule], default_skills: list[str] | None = None):
        self.rules = rules
        self.default_skills = default_skills or []

    def run(self, prompt: str) -> RunResult:
        for rule in self.rules:
            if rule.prompt_contains.lower() in prompt.lower():
                return RunResult(
                    loaded_skills=list(rule.loaded_skills),
                    read_paths=list(rule.read_paths),
                    final_message=rule.final_message,
                    clarifying_question=rule.clarifying_question,
                )
        return RunResult(loaded_skills=list(self.default_skills))
