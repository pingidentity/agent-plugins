#!/usr/bin/env python3
"""Build generated reference manifests for all skill branches.

Scans curated anchors under plugins/ping-identity/skills/*/references/curated/,
reads their frontmatter, and produces top-N.json shortlists in the matching
references/generated/<branch>/ directories.

Usage:
    python3 scripts/build_reference_manifests.py [--root REPO_ROOT] [--dry-run]

Scoring (0.0–1.0):
    - canonical: true  → +0.40
    - doc_type=guide   → +0.15  (reference → +0.10, concept → +0.05, troubleshooting → +0.12)
    - last_updated within 90 days  → +0.25
    - last_updated within 180 days → +0.15
    - last_updated within 365 days → +0.05
    - slug non-empty               → +0.10
    - status=current               → +0.10
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, date, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Branch routing: maps (skill, path_segment) → branch name
# A curated file at  .../curated/<segment>/...  belongs to the branch.
# Files directly under curated/ (no sub-directory) are "cross-platform".
# ---------------------------------------------------------------------------
BRANCH_ALIASES = {
    "pingone-mt":      "pingone-mt",
    "pingone-st":      "pingone-st",
    "ping-software":   "ping-software",
    "cross-platform":  "cross-platform",
    "ai-identity":     "ai-identity",
    # orchestration sub-dirs map to the same branch as the parent
    "nodes":           "pingone-st",
    "journey-use-cases": "pingone-st",
}

# Per-skill branch → generated subdir and max_docs cap
SKILL_BRANCHES = {
    "ping-quickstart": {
        "cross-platform": ("cross-platform", 15),
    },
    "ping-foundation": {
        "pingone-mt":    ("pingone-mt",    25),
        "pingone-st":    ("pingone-st",    25),
        "ping-software": ("ping-software", 25),
        "cross-platform": ("cross-platform", 10),
    },
    "ping-orchestration": {
        "pingone-mt":    ("pingone-mt",    25),
        "pingone-st":    ("pingone-st",    25),
        "ping-software": ("ping-software", 25),
        "cross-platform": ("cross-platform", 10),
    },
    "ping-universal-services": {
        "cross-platform": ("cross-platform", 20),
    },
    "ping-app-integration": {
        "cross-platform": ("cross-platform", 20),
    },
    "ping-identity-for-ai": {
        "ai-identity":   ("ai-identity",   20),
    },
}


def parse_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file (simple key: value parser)."""
    fm = {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return fm

    if not text.startswith("---"):
        return fm

    end = text.find("\n---", 3)
    if end == -1:
        return fm

    block = text[3:end].strip()
    # Simple line-by-line parse; handles string, bool, and list values
    current_key = None
    for line in block.splitlines():
        if line.startswith("  ") and current_key:
            # List item under current_key
            item = line.strip().lstrip("- ").strip().strip('"').strip("'")
            if item:
                if not isinstance(fm.get(current_key), list):
                    fm[current_key] = []
                fm[current_key].append(item)
            continue

        m = re.match(r'^(\w[\w\-]*)\s*:\s*(.*)$', line)
        if not m:
            current_key = None
            continue

        key, val = m.group(1), m.group(2).strip()
        current_key = key

        if val == "":
            fm[key] = []
            continue
        if val.lower() == "true":
            fm[key] = True
        elif val.lower() == "false":
            fm[key] = False
        elif val.startswith("["):
            # Inline list: ["a", "b"]
            items = re.findall(r'"([^"]+)"|\'([^\']+)\'|(\w[\w\-]*)', val)
            fm[key] = [a or b or c for a, b, c in items if a or b or c]
        else:
            fm[key] = val.strip('"').strip("'")

    return fm


def score_doc(fm: dict, today: date) -> float:
    """Compute a relevance score (0.0–1.0) from frontmatter."""
    s = 0.0

    if fm.get("canonical") is True:
        s += 0.40

    doc_type = fm.get("doc_type", "")
    if doc_type == "guide":
        s += 0.15
    elif doc_type == "troubleshooting":
        s += 0.12
    elif doc_type == "reference":
        s += 0.10
    elif doc_type == "concept":
        s += 0.05

    if fm.get("status", "") == "current":
        s += 0.10

    if fm.get("slug", ""):
        s += 0.10

    raw_date = fm.get("last_updated", "")
    if raw_date:
        try:
            lu = date.fromisoformat(str(raw_date).strip('"'))
            age = (today - lu).days
            if age <= 90:
                s += 0.25
            elif age <= 180:
                s += 0.15
            elif age <= 365:
                s += 0.05
        except ValueError:
            pass

    return round(min(s, 1.0), 4)


def detect_branch(skill: str, path: Path, curated_root: Path) -> str:
    """Determine which branch a curated file belongs to."""
    rel = path.relative_to(curated_root)
    parts = rel.parts

    if len(parts) == 1:
        # Directly under curated/ — cross-platform or ai-identity
        return "ai-identity" if skill == "ping-identity-for-ai" else "cross-platform"

    top_dir = parts[0]
    return BRANCH_ALIASES.get(top_dir, "cross-platform")


def build_doc_entry(path: Path, fm: dict, today: date, repo_root: Path) -> dict:
    """Build a single doc entry for the manifest."""
    rel_path = str(path.relative_to(repo_root)).replace("\\", "/")
    return {
        "title": fm.get("title", path.stem.replace("-", " ").title()),
        "slug": rel_path,
        "url": fm.get("slug", ""),
        "doc_type": fm.get("doc_type", ""),
        "capabilities": fm.get("capabilities", []) if isinstance(fm.get("capabilities"), list) else [],
        "score": score_doc(fm, today),
        "canonical": fm.get("canonical", False),
        "last_updated": str(fm.get("last_updated", "")).strip('"'),
        "stale_warning": _is_stale(fm.get("last_updated", "")),
    }


def _is_stale(raw_date) -> bool:
    if not raw_date:
        return False
    try:
        lu = date.fromisoformat(str(raw_date).strip('"'))
        return (date.today() - lu).days > 180
    except ValueError:
        return False


def write_manifest(out_path: Path, skill: str, branch: str, max_docs: int,
                   docs: list, generated_at: str, dry_run: bool):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "_comment": "Machine-generated. Do not hand-edit. Regenerated by CI workflow build-reference-manifests.yml on docs publish.",
        "skill": skill,
        "branch": branch,
        "generated_at": generated_at,
        "max_docs": max_docs,
        "docs": docs[:max_docs],
    }
    if dry_run:
        print(f"  [dry-run] would write {out_path} ({len(docs[:max_docs])} docs)")
    else:
        out_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"  wrote {out_path} ({len(docs[:max_docs])} docs)")


def build_manifests(repo_root: Path, dry_run: bool = False) -> int:
    skills_root = repo_root / "plugins" / "ping-identity" / "skills"
    today = date.today()
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    errors = 0

    for skill, branches in SKILL_BRANCHES.items():
        skill_dir = skills_root / skill
        curated_root = skill_dir / "references" / "curated"
        generated_root = skill_dir / "references" / "generated"

        if not curated_root.exists():
            print(f"[WARN] {skill}: curated dir missing, skipping")
            continue

        print(f"\n{skill}:")

        # Collect all curated .md files
        all_md = list(curated_root.rglob("*.md"))
        if not all_md:
            print(f"  no curated anchors found")
            continue

        # Group by branch
        branch_docs: dict[str, list] = {b: [] for b in branches}

        for md_path in all_md:
            fm = parse_frontmatter(md_path)
            if not fm:
                continue
            branch = detect_branch(skill, md_path, curated_root)
            if branch not in branch_docs:
                # Assign orphaned branch to cross-platform if available, else skip
                fallback = "cross-platform" if "cross-platform" in branch_docs else next(iter(branch_docs), None)
                if fallback:
                    branch_docs[fallback].append(build_doc_entry(md_path, fm, today, repo_root))
                continue
            branch_docs[branch].append(build_doc_entry(md_path, fm, today, repo_root))

        for branch, (subdir, max_docs) in branches.items():
            docs = sorted(branch_docs.get(branch, []), key=lambda d: d["score"], reverse=True)
            out_path = generated_root / subdir / "top-25.json"
            # Use the correct filename based on max_docs
            cap_name = f"top-{max_docs}.json" if max_docs != 25 else "top-25.json"
            out_path = generated_root / subdir / cap_name
            write_manifest(out_path, skill, branch, max_docs, docs, generated_at, dry_run)

    return errors


def main():
    parser = argparse.ArgumentParser(description="Build reference manifests for all skill branches.")
    parser.add_argument("--root", default=".", help="Repo root directory (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be written without writing")
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    if not (repo_root / "plugins").exists():
        print(f"ERROR: plugins/ not found under {repo_root}. Run from repo root.", file=sys.stderr)
        sys.exit(1)

    errors = build_manifests(repo_root, dry_run=args.dry_run)
    sys.exit(errors)


if __name__ == "__main__":
    main()
