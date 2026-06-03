"""Layer 4 — Cross-LLM consistency.

Phase 0 stub: lists what would be run. Phase 1 wires in real adapters
(codex.py, gemini.py) and drives them in parallel.

Usage:
  python3 -m evals.harness.cross_llm --layer 1
"""
from __future__ import annotations

import argparse
import sys

LLMS = ["claude", "codex", "gemini"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--layer", type=int, choices=[1, 3], default=1)
    args = parser.parse_args()

    print(f"[stub] cross-LLM Layer {args.layer} run plan:")
    for llm in LLMS:
        print(f"  - {llm}: would call run_eval.py / judge_plans.py with --adapter {llm}")
    print("\n[stub] Phase 1 wires real adapters. See PLAN.md § Evaluation Layer 4.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
