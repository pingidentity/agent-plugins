"""Layer 3 — Plan quality eval (LLM-as-judge).

Phase 0: parses prompt sets and golden plans, prints what it WOULD send
to the judge. Phase 1: wires in actual judge calls.

Usage:
  python3 -m evals.harness.judge_plans --skill ping-orchestration
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPTS_DIR = REPO_ROOT / "evals" / "prompts"
GOLDEN_DIR = REPO_ROOT / "evals" / "golden"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--judge", default="claude", choices=["claude", "codex", "gemini"])
    args = parser.parse_args()

    pf = PROMPTS_DIR / f"{args.skill}.yaml"
    if not pf.exists():
        print(f"no prompt set for {args.skill}", file=sys.stderr)
        return 1

    pset = yaml.safe_load(pf.read_text())
    gdir = GOLDEN_DIR / args.skill
    if not gdir.exists():
        print(f"[stub] no goldens at {gdir} — Phase 1 authors them. Skipping.")
        return 0

    for prompt in pset["trigger_prompts"]:
        gp = gdir / f"{prompt['id']}.md"
        if not gp.exists():
            print(f"[skip] {prompt['id']} — no golden")
            continue
        print(
            f"[would-judge] skill={args.skill} prompt={prompt['id']} "
            f"judge={args.judge} golden_chars={len(gp.read_text())}"
        )

    print("\n[stub] Phase 1 wires the judge LLM call. See evals/scorecards/plan-quality-eval.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
