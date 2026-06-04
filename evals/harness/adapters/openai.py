"""OpenAI adapter for Layer 1 routing eval.

Mirrors claude.py: builds the same routing system prompt from the 6 SKILL.md
description fields, sends the user prompt, parses the JSON response.

Required env vars (no defaults):
  OPENAI_API_KEY=<your key>
  MODEL_OPENAI=<model id, e.g. gpt-4o-2024-11-20 or gpt-5-mini>

Optional:
  OPENAI_BASE_URL=<override, e.g. for Azure OpenAI or a proxy>
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

from openai import OpenAI

from evals.harness.adapters.base import RunResult

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_DIR = REPO_ROOT / "plugins" / "ping-identity" / "skills"

SKILL_NAMES = [
    "ping-quickstart",
    "ping-foundation",
    "ping-orchestration",
    "ping-universal-services",
    "ping-app-integration",
    "ping-identity-for-ai",
]


def _extract_description(skill_name: str) -> str:
    skill_file = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_file.exists():
        return f"Skill: {skill_name}"
    text = skill_file.read_text()
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("description:"):
            desc = line[len("description:"):].strip().strip('"').strip("'")
            if desc:
                return desc
    return f"Skill: {skill_name}"


def _build_system_prompt() -> str:
    skill_list = "\n".join(
        f"- {name}: {_extract_description(name)}" for name in SKILL_NAMES
    )
    return f"""You are a routing assistant for the Ping Identity agent skills system.

Available skills:
{skill_list}

Given a user message, respond with a JSON object (no markdown, no prose) in one of two forms:

Form 1 — route to skill(s):
{{"action": "route", "skills": ["skill-name-1"], "reasoning": "one sentence"}}

Form 2 — ask a clarifying question:
{{"action": "clarify", "question": "your clarifying question here", "reasoning": "one sentence"}}

Rules:
- Use "route" when you can confidently identify the relevant skill(s).
- Use "clarify" ONLY when the intent is genuinely ambiguous between two or more skills and a question would resolve it. Do not clarify clear intents.
- You may route to multiple skills if the task genuinely spans them.
- Always output valid JSON and nothing else.
"""


class OpenAIAdapter:
    def __init__(self) -> None:
        api_key = os.environ.get("OPENAI_API_KEY")
        model = os.environ.get("MODEL_OPENAI")
        if not api_key:
            raise SystemExit(
                "Missing OPENAI_API_KEY.\n"
                "Set OPENAI_API_KEY and MODEL_OPENAI to use the OpenAI adapter."
            )
        if not model:
            raise SystemExit(
                "Missing MODEL_OPENAI.\n"
                "Set MODEL_OPENAI to the OpenAI model ID (e.g. gpt-4o-2024-11-20)."
            )
        base_url = os.environ.get("OPENAI_BASE_URL")
        if base_url:
            self._client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self._client = OpenAI(api_key=api_key)
        self._model = model
        self._system = _build_system_prompt()

    def run(self, prompt: str) -> RunResult:
        completion = self._client.chat.completions.create(
            model=self._model,
            max_completion_tokens=1024,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self._system},
                {"role": "user", "content": prompt},
            ],
        )
        raw = (completion.choices[0].message.content or "").strip()

        # Strip accidental markdown code fences (json_object mode usually prevents this)
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return RunResult(
                loaded_skills=[],
                final_message=raw,
                raw_trace=[{"role": "assistant", "content": raw}],
            )

        if data.get("action") == "clarify":
            return RunResult(
                loaded_skills=[],
                clarifying_question=data.get("question", ""),
                final_message=raw,
                raw_trace=[{"role": "assistant", "content": raw}],
            )

        return RunResult(
            loaded_skills=data.get("skills", []),
            final_message=raw,
            raw_trace=[{"role": "assistant", "content": raw}],
        )
