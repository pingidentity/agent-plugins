"""Subprocess driver for `claude -p`, with stream-json parsing.

Used by Layer 3 to invoke Claude Code in two configurations:
  with_skill    : claude -p --plugin-dir <repo>/plugins/ping-identity
  without_skill : claude -p --bare

Both use --output-format stream-json so we can extract token totals,
duration, and turn count without scraping prose.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RunOutcome:
    tokens_input: int = 0
    tokens_output: int = 0
    duration_ms: int = 0
    turn_count: int = 0
    final_message: str = ""
    error: str | None = None
    raw_lines: list[str] = field(default_factory=list)

    @property
    def tokens_total(self) -> int:
        return self.tokens_input + self.tokens_output


def parse_stream_json(lines: list[str]) -> RunOutcome:
    out = RunOutcome(raw_lines=list(lines))
    last_assistant_text = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = obj.get("type")
        if kind == "assistant":
            msg = obj.get("message", {})
            for block in msg.get("content", []) or []:
                if block.get("type") == "text" and block.get("text"):
                    last_assistant_text = block["text"]
        elif kind == "result":
            usage = obj.get("usage") or {}
            out.tokens_input = int(usage.get("input_tokens") or 0)
            out.tokens_output = int(usage.get("output_tokens") or 0)
            out.duration_ms = int(obj.get("duration_ms") or 0)
            out.turn_count = int(obj.get("num_turns") or 0)
            if obj.get("is_error"):
                out.error = obj.get("subtype") or "unknown_error"
    out.final_message = last_assistant_text
    return out


def build_argv(
    *,
    prompt: str,
    model: str,
    config: str,
    plugin_dir: Path,
    max_turns: int,
    claude_bin: str = "claude",
) -> list[str]:
    if config not in ("with_skill", "without_skill"):
        raise ValueError(f"unknown config: {config}")
    argv = [
        claude_bin, "-p", prompt,
        "--model", model,
        "--output-format", "stream-json",
        "--verbose",  # required for stream-json with --print
        "--max-turns", str(max_turns),
        "--dangerously-skip-permissions",
    ]
    if config == "with_skill":
        argv += ["--plugin-dir", str(plugin_dir)]
    else:
        argv += ["--bare"]
    return argv


def run_in_workdir(
    *,
    prompt: str,
    model: str,
    config: str,
    plugin_dir: Path,
    workdir: Path,
    max_turns: int = 30,
    timeout_seconds: int = 600,
) -> RunOutcome:
    """Spawn claude -p in workdir; return parsed RunOutcome."""
    if shutil.which("claude") is None:
        raise RuntimeError("`claude` CLI not on PATH")
    argv = build_argv(
        prompt=prompt, model=model, config=config,
        plugin_dir=plugin_dir, max_turns=max_turns,
    )
    try:
        result = subprocess.run(
            argv, cwd=workdir, capture_output=True, text=True,
            timeout=timeout_seconds, check=False,
        )
    except subprocess.TimeoutExpired:
        return RunOutcome(error="timeout", duration_ms=timeout_seconds * 1000)
    lines = (result.stdout or "").splitlines()
    outcome = parse_stream_json(lines)
    if result.returncode != 0 and outcome.error is None:
        outcome.error = f"exit_{result.returncode}"
    return outcome
