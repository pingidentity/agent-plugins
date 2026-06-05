"""OpenAI driver for Layer 3 task runs (gpt-5.x family).

We can't use `claude -p` for non-Anthropic models, so we drive the API
directly. The 'with_skill' system prompt = the target skill's SKILL.md
body. The 'without_skill' system prompt = empty.

The model writes code in fenced blocks; we extract them to workdir so
the same deterministic_checks code can score the output.
"""
from __future__ import annotations

import os
import re
import time
from pathlib import Path

from evals.harness.runners.claude_code_cli import RunOutcome


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_ROOT_DEFAULT = REPO_ROOT / "plugins" / "ping-identity" / "skills"

_FINAL_MESSAGE_MAX_CHARS = 2000


def _read_skill_body(skills_root: Path, skill: str) -> str:
    f = skills_root / skill / "SKILL.md"
    if not f.exists():
        return ""
    text = f.read_text()
    # Strip frontmatter
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            text = text[end + 3 :].lstrip("\n")
    return text


def build_system_prompt(config: str, skill: str, skills_root: Path = SKILLS_ROOT_DEFAULT) -> str:
    if config == "with_skill":
        return _read_skill_body(skills_root, skill)
    return ""


_FENCE_RE = re.compile(
    r"```(?P<lang>[a-zA-Z0-9_+-]*)(?:\s+(?:file=)?(?P<name>[^\s`]+))?\s*\n(?P<body>.*?)```",
    re.DOTALL,
)

_LANG_TO_EXT = {
    "kotlin": "kt", "kt": "kt", "swift": "swift", "java": "java",
    "javascript": "js", "js": "js", "typescript": "ts", "ts": "ts",
    "tsx": "tsx", "jsx": "jsx", "python": "py", "py": "py",
    "json": "json", "yaml": "yaml", "yml": "yml", "md": "md", "markdown": "md",
    "bash": "sh", "shell": "sh", "sh": "sh",
}


def extract_code_blocks_to_workdir(text: str, workdir: Path) -> list[Path]:
    written: list[Path] = []
    for i, m in enumerate(_FENCE_RE.finditer(text)):
        lang = (m.group("lang") or "").lower()
        name = (m.group("name") or "").strip()
        body = m.group("body")
        if not body.endswith("\n"):
            body += "\n"
        if name:
            target = workdir / name
        else:
            ext = _LANG_TO_EXT.get(lang, "txt")
            target = workdir / f"snippet_{i:02d}.{ext}"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body)
        written.append(target)
    return written


def run_in_workdir(
    *,
    prompt: str,
    model: str,
    config: str,
    skill: str,
    workdir: Path,
    timeout_seconds: int = 600,
) -> RunOutcome:
    """Single-turn OpenAI completion; extract code blocks into workdir."""
    if config not in ("with_skill", "without_skill"):
        raise ValueError(f"unknown config: {config!r}")

    from openai import OpenAI, OpenAIError

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY — set OPENAI_API_KEY env var")

    client_kwargs = {"api_key": api_key}
    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        client_kwargs["base_url"] = base_url
    client = OpenAI(**client_kwargs)

    system = build_system_prompt(config, skill)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    t0 = time.monotonic()
    try:
        completion = client.chat.completions.create(
            model=model, messages=messages, max_completion_tokens=8192,
            timeout=timeout_seconds,
        )
    except (OpenAIError, TimeoutError) as exc:
        return RunOutcome(error=type(exc).__name__, duration_ms=int((time.monotonic() - t0) * 1000))

    elapsed_ms = int((time.monotonic() - t0) * 1000)
    body = completion.choices[0].message.content or ""
    extract_code_blocks_to_workdir(body, workdir)

    usage = completion.usage
    return RunOutcome(
        tokens_input=getattr(usage, "prompt_tokens", 0) or 0,
        tokens_output=getattr(usage, "completion_tokens", 0) or 0,
        duration_ms=elapsed_ms,
        turn_count=1,
        final_message=body[:_FINAL_MESSAGE_MAX_CHARS],
        raw_lines=[body],
    )
