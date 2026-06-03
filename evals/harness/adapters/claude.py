"""LLM adapter for Layer 1 routing eval.

How it works:
  1. Build a system prompt that presents all 6 skills described by their
     SKILL.md description fields.
  2. Send the user prompt and ask the model to either route to skill(s) or ask
     a clarifying question, returning structured JSON.
  3. Parse the JSON response to populate RunResult.

Supports Bedrock (set CLAUDE_CODE_USE_BEDROCK=1 + AWS_BEARER_TOKEN_BEDROCK)
or direct API (set ANTHROPIC_API_KEY).
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

import anthropic

from evals.harness.adapters.base import RunResult

# Model IDs — set via MODEL_BEDROCK / MODEL_DIRECT env vars.
# Bedrock model IDs are region-prefixed (e.g. us.anthropic.claude-sonnet-4-6).
# Direct API model IDs follow the standard Anthropic naming scheme.
_BEDROCK_MODEL = os.environ.get("MODEL_BEDROCK", "us.anthropic.claude-sonnet-4-5-20250514-v1:0")
_DIRECT_MODEL = os.environ.get("MODEL_DIRECT", "claude-3-5-sonnet-20241022")

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


class ClaudeAdapter:
    def __init__(self) -> None:
        if os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1" or os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
            # Bedrock path — requires AWS_BEARER_TOKEN_BEDROCK and AWS_REGION env vars.
            # AWS_REGION must be set explicitly; there is no safe default.
            region = os.environ.get("AWS_REGION")
            if not region:
                raise SystemExit("AWS_REGION must be set when using the Bedrock adapter.")
            self._client = anthropic.AnthropicBedrock(aws_region=region)
            self._model = _BEDROCK_MODEL
        else:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise SystemExit("Neither ANTHROPIC_API_KEY nor AWS_BEARER_TOKEN_BEDROCK is set.")
            self._client = anthropic.Anthropic(api_key=api_key)
            self._model = _DIRECT_MODEL
        self._system = _build_system_prompt()

    def run(self, prompt: str) -> RunResult:
        message = self._client.messages.create(
            model=self._model,
            max_tokens=256,
            system=self._system,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()

        # Strip accidental markdown code fences
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
