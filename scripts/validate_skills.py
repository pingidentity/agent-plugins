#!/usr/bin/env python3
"""Validate all skill content against authoring rules.

Checks:
  1. SKILL.md frontmatter is valid (skill-frontmatter-schema.json)
  2. SKILL.md name: matches directory name
  3. SKILL.md ≤160 lines
  4. Routing table cross-references in SKILL.md resolve to real files

Reference-anchor content (layout, scope sections, link style, etc.) is
authoring guidance for skill writers, not machine-validated by this script.

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

# ---------------------------------------------------------------------------
# Frontmatter parser — supports top-level scalars, lists, and nested
# metadata values. Tracks a stack of (indent, container) frames rather than
# a single current_key, so indentation depth determines nesting.
# ---------------------------------------------------------------------------

def _coerce_scalar(val: str):
    """Convert a raw YAML-ish scalar into a Python value."""
    val = val.strip()
    if val == "":
        return ""
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    if val.startswith("["):
        items = re.findall(r'"([^"]+)"|\'([^\']+)\'|([\w\-]+)', val)
        return [a or b or c for a, b, c in items if a or b or c]
    return val.strip('"').strip("'")


def _indent_of(raw_line: str) -> int:
    return len(raw_line) - len(raw_line.lstrip(" "))


def _parse_block(lines: list[tuple[int, str]], i: int, indent: int):
    """Parse sibling lines at `indent`, starting at lines[i]. Returns (value, next_i)."""
    if lines[i][1].startswith("- "):
        items: list = []
        while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
            item_text = lines[i][1][2:].strip()
            if item_text:
                items.append(_coerce_scalar(item_text))
            i += 1
        return items, i

    obj: dict = {}
    while i < len(lines) and lines[i][0] == indent:
        m = re.match(r'^(\w[\w\-]*)\s*:\s*(.*)$', lines[i][1])
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        i += 1
        if val == "":
            if i < len(lines) and lines[i][0] > indent:
                child_indent = lines[i][0]
                obj[key], i = _parse_block(lines, i, child_indent)
            else:
                obj[key] = None
        else:
            obj[key] = _coerce_scalar(val)
    return obj, i


def _parse_frontmatter(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip()

    lines = [(_indent_of(raw), raw.strip()) for raw in block.splitlines() if raw.strip()]
    if not lines:
        return {}

    fm, _ = _parse_block(lines, 0, lines[0][0])
    return fm


# ---------------------------------------------------------------------------
# Schema validator (minimal JSON Schema draft-07 subset)
# ---------------------------------------------------------------------------

def _validate_schema(data: dict, schema: dict, path_hint: str) -> list[str]:
    """Return list of error strings. Validates required, type, enum, pattern, minLength, minItems, nested objects."""
    errors: list[str] = []
    required = schema.get("required", [])
    for field in required:
        if field not in data or data.get(field) in (None, ""):
            errors.append(f"{path_hint}: missing required field '{field}'")
    props = schema.get("properties", {})
    for field, fschema in props.items():
        if field not in data or data[field] is None:
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
        max_len = fschema.get("maxLength")
        if max_len and isinstance(val, str) and len(val) > max_len:
            errors.append(f"{path_hint}: '{field}' is too long (max {max_len} chars)")
        pattern = fschema.get("pattern")
        if pattern and isinstance(val, str) and not re.match(pattern, val):
            errors.append(f"{path_hint}: '{field}' value '{val}' does not match pattern '{pattern}'")
        min_items = fschema.get("minItems")
        if min_items and isinstance(val, list) and len(val) < min_items:
            errors.append(f"{path_hint}: '{field}' must have at least {min_items} item(s)")
        if ftype == "object" and isinstance(val, dict):
            errors.extend(_validate_schema(val, fschema, f"{path_hint}.{field}"))
        if ftype == "array" and isinstance(val, list):
            items_schema = fschema.get("items", {})
            item_enum = items_schema.get("enum")
            if item_enum:
                for item in val:
                    if isinstance(item, str) and item not in item_enum:
                        errors.append(f"{path_hint}: '{field}' contains invalid item '{item}' (allowed: {item_enum})")
    return errors


# ---------------------------------------------------------------------------
# Schema loading
# ---------------------------------------------------------------------------

SKILL_SCHEMA = None

def _load_skill_schema(repo_root: Path) -> dict:
    global SKILL_SCHEMA
    if SKILL_SCHEMA is None:
        SKILL_SCHEMA = json.loads((repo_root / "shared/schemas/skill-frontmatter-schema.json").read_text())
    return SKILL_SCHEMA


# ---------------------------------------------------------------------------
# Check: SKILL.md
# ---------------------------------------------------------------------------

SKILL_LINE_CAP = 160
ROUTING_REF_RE = re.compile(
    r'`(references/(?:playbooks|blueprints|catalogs|examples)/[^`]+\.md)`'
)
def _check_skill_md(skill_dir: Path, plugin_name: str, repo_root: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    skill_schema = _load_skill_schema(repo_root)

    if not skill_md.exists():
        return [f"{skill_dir.name}: SKILL.md missing"]

    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    hint = f"{skill_dir.name}/SKILL.md"

    if len(lines) > SKILL_LINE_CAP:
        errors.append(f"{hint}: {len(lines)} lines (max {SKILL_LINE_CAP})")

    fm = _parse_frontmatter(skill_md)
    if not fm:
        errors.append(f"{hint}: no frontmatter found")
        return errors

    errors.extend(_validate_schema(fm, skill_schema, hint))

    if fm.get("name") and fm["name"] != skill_dir.name:
        errors.append(f"{hint}: name '{fm['name']}' does not match directory '{skill_dir.name}'")

    for m in ROUTING_REF_RE.finditer(text):
        ref_path = skill_dir / m.group(1)
        if not ref_path.exists():
            errors.append(f"{hint}: routing reference '{m.group(1)}' does not exist")

    return errors


# ---------------------------------------------------------------------------
# Main walk
# ---------------------------------------------------------------------------

def validate(repo_root: Path) -> int:
    plugins_root = repo_root / "plugins"
    all_errors: list[str] = []
    skill_count = 0

    for plugin_dir in sorted(plugins_root.iterdir()):
        if not plugin_dir.is_dir():
            continue
        skills_root = plugin_dir / "skills"
        if not skills_root.exists():
            continue
        for skill_dir in sorted(skills_root.iterdir()):
            if not skill_dir.is_dir():
                continue
            # Cross-portfolio orientation summaries live directly under this
            # directory and are not a standalone skill or canonical anchors.
            if plugin_dir.name == "ping-identity" and skill_dir.name == "references":
                continue
            all_errors.extend(_check_skill_md(skill_dir, plugin_dir.name, repo_root))
            skill_count += 1

    if all_errors:
        for e in all_errors:
            print(f"FAIL: {e}", file=sys.stderr)
        print(f"\n{len(all_errors)} error(s) found.", file=sys.stderr)
        return 1

    print(f"OK: {skill_count} skills — all valid.")
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
