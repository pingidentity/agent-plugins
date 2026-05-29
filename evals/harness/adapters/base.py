"""Adapter base — every LLM driver implements this."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class RunResult:
    loaded_skills: list[str] = field(default_factory=list)
    read_paths: list[str] = field(default_factory=list)
    final_message: str = ""
    clarifying_question: str | None = None
    raw_trace: list[dict] = field(default_factory=list)


class LLMAdapter(Protocol):
    def run(self, prompt: str) -> RunResult: ...
