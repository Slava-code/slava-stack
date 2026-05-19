#!/usr/bin/env python3
"""
kb-lint.py — Validate frontmatter of project-kb content files
against schema/kb-schema.yaml.

Usage:
    scripts/kb-lint.py [<file>...]   validate specific files
    scripts/kb-lint.py               validate all *.md in repo

Exit code: 0 = pass, 1 = errors found.
Called by .git/hooks/pre-commit and by /kb-audit skill.
"""

import os
import re
import sys
from pathlib import Path
from fnmatch import fnmatch

try:
    import yaml
except ImportError:
    print("kb-lint: PyYAML missing. Install: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "kb-schema.yaml"


def load_schema():
    with open(SCHEMA_PATH) as f:
        return yaml.safe_load(f)


def parse_frontmatter(text):
    """Return (frontmatter_dict, body_str). Returns (None, text) if no frontmatter."""
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return None, text
    # find second ---
    lines = text.splitlines(keepends=True)
    if not lines or not lines[0].startswith("---"):
        return None, text
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].startswith("---"):
            end_idx = i
            break
    if end_idx is None:
        return None, text
    fm_text = "".join(lines[1:end_idx])
    body = "".join(lines[end_idx + 1:])
    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError as e:
        raise ValueError(f"invalid YAML frontmatter: {e}")
    if fm is None:
        return {}, body
    if not isinstance(fm, dict):
        raise ValueError("frontmatter is not a mapping")
    return fm, body


def is_exempt(filepath, patterns):
    try:
        rel = str(filepath.relative_to(REPO_ROOT))
    except ValueError:
        return True  # outside repo root
    for pat in patterns:
        if fnmatch(rel, pat):
            return True
    return False


def resolve_enum(ref, enums):
    """ref is either a list literal or a string key into enums."""
    if isinstance(ref, list):
        return ref
    return enums.get(ref, [])


def check_enum_field(fm, field, allowed, filepath, errors):
    """Check that fm[field], if present, is in allowed (supports list or scalar)."""
    if field not in fm:
        return
    val = fm[field]
    if isinstance(val, list):
        for v in val:
            if v not in allowed:
                errors.append(
                    f"{filepath}: {field} value `{v}` not in allowed {allowed}"
                )
    else:
        if val not in allowed:
            errors.append(
                f"{filepath}: {field} value `{val}` not in allowed {allowed}"
            )


def check_description(fm, rules, filepath, errors):
    """Enforce description_rules on fm['description'] if present.

    Description is optional on every type; when present we verify length
    + style (no wikilinks, no markdown links). Empty-string or missing
    skips. Non-string is rejected.
    """
    if rules is None:
        return
    if "description" not in fm:
        return
    val = fm["description"]
    if val is None or val == "":
        return
    if not isinstance(val, str):
        errors.append(f"{filepath}: description must be a string")
        return
    max_len = rules.get("max_length")
    if max_len is not None and len(val) > max_len:
        errors.append(
            f"{filepath}: description exceeds {max_len} chars (is {len(val)}): `{val[:50]}...`"
        )
    forbids = rules.get("style_forbid_substrings") or []
    for sub in forbids:
        if sub in val:
            errors.append(
                f"{filepath}: description contains forbidden substring `{sub}` "
                f"(descriptions are rules, not wikilink-carrying): `{val}`"
            )


def validate_file(filepath, schema, errors):
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception as e:
        errors.append(f"{filepath}: could not read file ({e})")
        return

    try:
        fm, body = parse_frontmatter(text)
    except ValueError as e:
        errors.append(f"{filepath}: {e}")
        return

    if fm is None or not fm:
        return  # no frontmatter → skip (navigational / plain README)

    type_name = fm.get("type")
    if type_name is None:
        errors.append(f"{filepath}: missing required field `type:` in frontmatter")
        return

    type_def = schema["types"].get(type_name)
    if type_def is None:
        errors.append(
            f"{filepath}: unknown type `{type_name}` "
            f"(not in schema/kb-schema.yaml)"
        )
        return

    enums = schema["enums"]

    # required fields
    for field in type_def.get("required", []):
        if field not in fm:
            errors.append(
                f"{filepath}: missing required field `{field}` for type `{type_name}`"
            )

    # enum: status
    status_values_ref = type_def.get("status_values")
    if status_values_ref:
        allowed = resolve_enum(status_values_ref, enums)
        check_enum_field(fm, "status", allowed, filepath, errors)

    # enum: product
    if "product" in fm:
        check_enum_field(fm, "product", enums.get("product", []), filepath, errors)

    # enum: confidence
    if "confidence" in fm:
        check_enum_field(
            fm, "confidence", enums.get("confidence", []), filepath, errors
        )

    # enum: strategic-thread (multi)
    if "strategic-thread" in fm:
        check_enum_field(
            fm, "strategic-thread", enums.get("strategic_thread", []), filepath, errors
        )

    # extra_fields with enums
    extra = type_def.get("extra_fields", {}) or {}
    for field_name, field_def in extra.items():
        if "enum" in field_def:
            allowed = resolve_enum(field_def["enum"], enums)
            check_enum_field(fm, field_name, allowed, filepath, errors)

    # description: optional on every type; when present, enforce length + style
    check_description(fm, schema.get("description_rules"), filepath, errors)

    # required body sections (H2 headers); permissive — match if H2 starts with the
    # required word, optionally followed by punctuation/colon/etc. Enforces topic
    # presence, not exact heading string.
    for section in type_def.get("body_required_sections", []) or []:
        pattern = rf"^##\s+{re.escape(section)}(?=[^a-zA-Z0-9]|$)"
        if not re.search(pattern, body, re.MULTILINE):
            errors.append(
                f"{filepath}: missing required body section starting with "
                f"`## {section}` for type `{type_name}`"
            )


def main(args):
    schema = load_schema()
    exempt = schema.get("lint_exempt_patterns", []) or []

    if args:
        files = []
        for a in args:
            p = Path(a)
            if not p.is_absolute():
                p = (Path.cwd() / p).resolve()
            files.append(p)
    else:
        files = [
            p.resolve()
            for p in REPO_ROOT.rglob("*.md")
            if ".git" not in p.parts
        ]

    checked = 0
    skipped = 0
    errors = []
    for f in files:
        if not f.exists():
            continue
        if f.suffix != ".md":
            continue
        if is_exempt(f, exempt):
            skipped += 1
            continue
        validate_file(f, schema, errors)
        checked += 1

    if errors:
        print(f"kb-lint: {len(errors)} error(s) in {checked} file(s):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    print(f"kb-lint: OK ({checked} checked, {skipped} exempt)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
