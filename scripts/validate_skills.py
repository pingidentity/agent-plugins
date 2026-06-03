#!/usr/bin/env python3
"""Validate all skill content against authoring rules.

Checks:
  1. SKILL.md frontmatter is valid (skill-frontmatter-schema.json)
  2. SKILL.md name: matches directory name
  3. SKILL.md ≤120 lines
  4. Curated anchor frontmatter is valid (reference-frontmatter-schema.json)
  5. Curated anchor product_family matches directory path
  6. Routing table cross-references in SKILL.md resolve to real files
  7. index.json paths all resolve
  8. No /r/en-us/ or apps.pingone.com in curated anchors
  9. No /latest/ in AIC URLs (docs.pingidentity.com/pingoneaic)

Usage:
    python3 scripts/validate_skills.py [--root REPO_ROOT]
    Exit code 0 = all clean; non-zero = failures printed to stderr.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

try:
    import yaml as _yaml_mod
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# ---------------------------------------------------------------------------
# Frontmatter parser (same logic as build_reference_manifests.py)
# ---------------------------------------------------------------------------

def _parse_frontmatter(path: Path) -> dict:
    fm: dict = {}
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
    current_key: Optional[str] = None
    for line in block.splitlines():
        if line.startswith("  ") and current_key:
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
        elif val.lower() == "true":
            fm[key] = True
        elif val.lower() == "false":
            fm[key] = False
        elif val.startswith("["):
            items = re.findall(r'"([^"]+)"|\'([^\']+)\'|(\w[\w\-]*)', val)
            fm[key] = [a or b or c for a, b, c in items if a or b or c]
        else:
            fm[key] = val.strip('"').strip("'")
    return fm


# ---------------------------------------------------------------------------
# Schema validator (minimal JSON Schema draft-07 subset)
# ---------------------------------------------------------------------------

def _validate_schema(data: dict, schema: dict, path_hint: str) -> list[str]:
    """Return list of error strings. Only validates required + type + enum."""
    errors: list[str] = []
    required = schema.get("required", [])
    for field in required:
        if field not in data:
            errors.append(f"{path_hint}: missing required field '{field}'")
    props = schema.get("properties", {})
    for field, fschema in props.items():
        if field not in data:
            continue
        val = data[field]
        ftype = fschema.get("type")
        if ftype == "string" and not isinstance(val, str):
            errors.append(f"{path_hint}: '{field}' must be a string, got {type(val).__name__}")
        elif ftype == "array" and not isinstance(val, list):
            errors.append(f"{path_hint}: '{field}' must be an array, got {type(val).__name__}")
        elif ftype == "boolean" and not isinstance(val, bool):
            errors.append(f"{path_hint}: '{field}' must be a boolean, got {type(val).__name__}")
        enum = fschema.get("enum")
        if enum and isinstance(val, str) and val not in enum:
            errors.append(f"{path_hint}: '{field}' value '{val}' not in allowed values {enum}")
        min_len = fschema.get("minLength")
        if min_len and isinstance(val, str) and len(val) < min_len:
            errors.append(f"{path_hint}: '{field}' is too short (min {min_len} chars)")
        pattern = fschema.get("pattern")
        if pattern and isinstance(val, str) and not re.match(pattern, val):
            errors.append(f"{path_hint}: '{field}' value '{val}' does not match pattern '{pattern}'")
        min_items = fschema.get("minItems")
        if min_items and isinstance(val, list) and len(val) < min_items:
            errors.append(f"{path_hint}: '{field}' must have at least {min_items} item(s)")
        # Nested object
        if ftype == "object" and isinstance(val, dict):
            errors.extend(_validate_schema(val, fschema, f"{path_hint}.{field}"))
        # Array item enums
        if ftype == "array" and isinstance(val, list):
            items_schema = fschema.get("items", {})
            item_enum = items_schema.get("enum")
            if item_enum:
                for item in val:
                    if isinstance(item, str) and item not in item_enum:
                        errors.append(f"{path_hint}: '{field}' contains invalid item '{item}' (allowed: {item_enum})")
    return errors


# ---------------------------------------------------------------------------
# Check: SKILL.md
# ---------------------------------------------------------------------------

SKILL_SCHEMA = None
REF_SCHEMA = None

def _load_schemas(repo_root: Path) -> tuple[dict, dict]:
    global SKILL_SCHEMA, REF_SCHEMA
    if SKILL_SCHEMA is None:
        SKILL_SCHEMA = json.loads((repo_root / "shared/schemas/skill-frontmatter-schema.json").read_text())
    if REF_SCHEMA is None:
        REF_SCHEMA = json.loads((repo_root / "shared/schemas/reference-frontmatter-schema.json").read_text())
    return SKILL_SCHEMA, REF_SCHEMA


def _check_skill_md(skill_dir: Path, repo_root: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    skill_schema, _ = _load_schemas(repo_root)

    if not skill_md.exists():
        return [f"{skill_dir.name}: SKILL.md missing"]

    lines = skill_md.read_text(encoding="utf-8").splitlines()
    hint = f"{skill_dir.name}/SKILL.md"

    # Line count
    if len(lines) > 120:
        errors.append(f"{hint}: {len(lines)} lines (max 120)")

    # Frontmatter
    fm = _parse_frontmatter(skill_md)
    if not fm:
        errors.append(f"{hint}: no frontmatter found")
        return errors

    errors.extend(_validate_schema(fm, skill_schema, hint))

    # name: matches directory
    if fm.get("name") and fm["name"] != skill_dir.name:
        errors.append(f"{hint}: name '{fm['name']}' does not match directory '{skill_dir.name}'")

    # Routing table references — find `references/curated/...md` paths in the body
    body = skill_md.read_text(encoding="utf-8")
    for m in re.finditer(r'`(references/curated/[^`]+\.md)`', body):
        ref_path = skill_dir / m.group(1)
        if not ref_path.exists():
            errors.append(f"{hint}: routing reference '{m.group(1)}' does not exist")

    return errors


# ---------------------------------------------------------------------------
# Check: curated anchors
# ---------------------------------------------------------------------------

# Map directory name → expected product_family
_DIR_TO_FAMILY = {
    "pingone-mt": "pingone-mt",
    "pingone-st": "pingone-st",
    "ping-software": "ping-software",
    "cross-platform": "cross-platform",
    "ai-identity": "ai-identity",
    "nodes": "pingone-st",
    "journey-use-cases": "pingone-st",
}

# Forbidden URL patterns in curated anchors
_FORBIDDEN_URLS = [
    (r'/r/en-us/', "contains /r/en-us/ (localisation path — use direct URL)"),
    (r'apps\.pingone\.com', "contains apps.pingone.com (deprecated admin URL)"),
    (r'docs\.pingidentity\.com/pingoneaic/latest/', "contains /latest/ in AIC URL (use versioned path)"),
]


def _detect_expected_family(md_path: Path, curated_root: Path) -> Optional[str]:
    """Infer expected product_family from directory path."""
    try:
        rel = md_path.relative_to(curated_root)
    except ValueError:
        return None
    parts = rel.parts
    if len(parts) == 1:
        return None  # top-level — skip family path check
    for part in parts[:-1]:
        if part in _DIR_TO_FAMILY:
            return _DIR_TO_FAMILY[part]
    return None


def _check_curated_anchor(md_path: Path, curated_root: Path, repo_root: Path) -> list[str]:
    errors: list[str] = []
    _, ref_schema = _load_schemas(repo_root)
    hint = str(md_path.relative_to(repo_root))

    fm = _parse_frontmatter(md_path)
    if not fm:
        errors.append(f"{hint}: no frontmatter")
        return errors

    errors.extend(_validate_schema(fm, ref_schema, hint))

    # product_family vs directory
    expected_family = _detect_expected_family(md_path, curated_root)
    if expected_family:
        actual = fm.get("product_family", "")
        if actual != expected_family:
            errors.append(
                f"{hint}: product_family '{actual}' does not match directory path '{expected_family}'"
            )

    # Forbidden URL patterns
    body = md_path.read_text(encoding="utf-8")
    for pattern, reason in _FORBIDDEN_URLS:
        if re.search(pattern, body):
            errors.append(f"{hint}: {reason}")

    return errors


# ---------------------------------------------------------------------------
# Check: index.json
# ---------------------------------------------------------------------------

def _check_index_json(repo_root: Path) -> list[str]:
    errors: list[str] = []
    index_path = repo_root / "plugins/ping-identity/references/index.json"
    if not index_path.exists():
        return [f"plugins/ping-identity/references/index.json: missing"]

    try:
        data = json.loads(index_path.read_text())
    except json.JSONDecodeError as e:
        return [f"index.json: invalid JSON — {e}"]

    hint = "index.json"
    plugin_root = repo_root / "plugins/ping-identity"
    for skill, content in data.get("skills", {}).items():
        for rel in content.get("curated", []):
            p = plugin_root / rel
            if not p.exists():
                errors.append(f"{hint}: curated path '{rel}' (skill '{skill}') does not exist")
        for branch, rel in content.get("generated", {}).items():
            if rel.endswith(".json"):
                p = plugin_root / rel
                if not p.exists():
                    errors.append(f"{hint}: generated path '{rel}' (skill '{skill}', branch '{branch}') does not exist")

    return errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def validate(repo_root: Path) -> int:
    skills_root = repo_root / "plugins/ping-identity/skills"
    all_errors: list[str] = []

    for skill_dir in sorted(skills_root.iterdir()):
        if not skill_dir.is_dir():
            continue
        all_errors.extend(_check_skill_md(skill_dir, repo_root))
        curated_root = skill_dir / "references/curated"
        if curated_root.exists():
            for md in sorted(curated_root.rglob("*.md")):
                all_errors.extend(_check_curated_anchor(md, curated_root, repo_root))

    all_errors.extend(_check_index_json(repo_root))

    if all_errors:
        for e in all_errors:
            print(f"FAIL: {e}", file=sys.stderr)
        print(f"\n{len(all_errors)} error(s) found.", file=sys.stderr)
        return 1

    skill_count = sum(1 for d in skills_root.iterdir() if d.is_dir())
    curated_count = sum(1 for d in skills_root.iterdir() if d.is_dir()
                        for _ in (d / "references/curated").rglob("*.md")
                        if (d / "references/curated").exists())
    print(f"OK: {skill_count} skills, {curated_count} curated anchors, index.json — all valid.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate skill content against authoring rules.")
    parser.add_argument("--root", default=".", help="Repo root (default: current directory)")
    args = parser.parse_args()
    repo_root = Path(args.root).resolve()
    if not (repo_root / "plugins").exists():
        print(f"ERROR: plugins/ not found under {repo_root}", file=sys.stderr)
        return 1
    return validate(repo_root)


if __name__ == "__main__":
    sys.exit(main())
