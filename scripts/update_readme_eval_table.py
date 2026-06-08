"""Regenerate the Layer 3 'Eval status' subsection in README.md.

Reads evals/results/<date>/layer3/summary.json and rewrites the block
between <!-- BEGIN: layer3-eval-table --> and <!-- END: ... --> markers.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"
RESULTS_DIR = REPO_ROOT / "evals" / "results"


def render_layer3_section(summary: dict, *, models: list[str]) -> str:
    skills = sorted(summary["by_skill_model_config"].keys())
    header_cells = ["Skill"]
    for m in models:
        header_cells += [f"{m} Δ pass", f"{m} Δ tokens"]
    header = "| " + " | ".join(header_cells) + " |"
    sep = "|" + "|".join("---" for _ in header_cells) + "|"

    rows = []
    for skill in skills:
        row = [skill]
        for m in models:
            cell = summary["by_skill_model_config"][skill].get(m, {})
            d = cell.get("delta") or {}
            pr = d.get("pass_rate", "—")
            tk = d.get("tokens", "—")
            row += [pr, tk]
        rows.append("| " + " | ".join(row) + " |")

    agg_lines = []
    for m in models:
        a = summary["aggregate_by_model"].get(m, {})
        if "with_skill_pass" in a and "without_skill_pass" in a:
            delta = a["with_skill_pass"] - a["without_skill_pass"]
            agg_lines.append(
                f"- **{m}** — with skill: {a['with_skill_pass']:.0%}, "
                f"without: {a['without_skill_pass']:.0%}, Δ {delta:+.0%}"
            )

    return (
        "### Layer 3 — Skill execution value\n\n"
        "Per-skill delta with the ping-identity plugin loaded vs a clean baseline. "
        "Each cell is one run (n=1); footnote: gpt-5.5 measures SKILL.md content only "
        "(the discovery layer is Anthropic-only).\n\n"
        + header + "\n" + sep + "\n" + "\n".join(rows) + "\n\n"
        + "Headlines:\n" + "\n".join(agg_lines) + "\n"
    )


def replace_between_markers(path: Path, *, begin: str, end: str, new_content: str) -> None:
    text = path.read_text()
    if begin not in text or end not in text:
        raise ValueError(f"missing markers in {path}")
    pre, _, rest = text.partition(begin)
    _, _, post = rest.partition(end)
    path.write_text(f"{pre}{begin}\n{new_content}\n{end}{post}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--models", nargs="+", required=True)
    parser.add_argument("--readme", type=Path, default=README)
    parser.add_argument("--results-dir", type=Path, default=RESULTS_DIR)
    args = parser.parse_args(argv)

    summary_path = args.results_dir / args.date / "layer3" / "summary.json"
    summary = json.loads(summary_path.read_text())
    body = render_layer3_section(summary, models=args.models)
    replace_between_markers(
        args.readme,
        begin="<!-- BEGIN: layer3-eval-table -->",
        end="<!-- END: layer3-eval-table -->",
        new_content=body,
    )
    print(f"Updated {args.readme} with Layer 3 results from {summary_path}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
