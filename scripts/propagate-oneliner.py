#!/usr/bin/env python3
"""
propagate-oneliner.py — Propagate the canonical product one-liner from its
single source of truth (the newest synthesis/*.md carrying a `one_liner:`
field) into the AUTOGEN-marked block of each target file (e.g. GLOSSARY.md).

This is the T1 analog of rebuild-indexes.py: a derived, always-loaded fact
is GENERATED from one authored source, never hand-maintained — so it cannot
drift. kb-lint rejects a commit whose target block no longer matches source.

Usage:
    scripts/propagate-oneliner.py            # write the block into every target
    scripts/propagate-oneliner.py --check    # exit 1 if any target is stale (no write)

Source selection: among synthesis/*.md with a non-empty `one_liner:`, pick the
one with the newest `date_found` (ties broken by filename desc). Its one_liner
is the canonical string.

The bolded label in the rendered block (`PRODUCT_LABEL` below) is the product /
project name shown in GLOSSARY.md. Set it once for your project — it must match
exactly what the GLOSSARY AUTOGEN block expects (kb-lint compares verbatim).
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("propagate-oneliner: PyYAML missing. Install: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "kb-schema.yaml"

# The bolded glossary term the one-liner hangs off. Rename to your product name
# (must match the term already present in GLOSSARY.md's AUTOGEN block).
PRODUCT_LABEL = "Your Product"


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None
    lines = text.splitlines(keepends=True)
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].startswith("---"):
            end_idx = i
            break
    if end_idx is None:
        return None
    try:
        fm = yaml.safe_load("".join(lines[1:end_idx]))
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


def load_config():
    with open(SCHEMA_PATH) as f:
        schema = yaml.safe_load(f)
    cfg = schema.get("oneliner_propagation") or {}
    return cfg


def find_source_one_liner():
    """Return (one_liner_str, source_path) from the newest synthesis carrying one."""
    candidates = []
    syn_dir = REPO_ROOT / "synthesis"
    if not syn_dir.is_dir():
        return None, None
    for p in syn_dir.glob("*.md"):
        if p.name == "INDEX.md":
            continue
        fm = parse_frontmatter(p.read_text(encoding="utf-8"))
        if not fm:
            continue
        ol = fm.get("one_liner")
        if ol and isinstance(ol, str) and ol.strip():
            candidates.append((str(fm.get("date_found", "")), p.name, ol.strip(), p))
    if not candidates:
        return None, None
    # newest date_found, then filename desc
    candidates.sort(key=lambda c: (c[0], c[1]), reverse=True)
    _, _, one_liner, path = candidates[0]
    return one_liner, path


def render_block(one_liner, marker_begin, marker_end):
    """The exact text (markers included) that a target's block must equal.

    Shared canonical render — kb-lint recomputes this identically to detect drift.
    """
    return f"{marker_begin}\n- **{PRODUCT_LABEL}** — {one_liner}\n{marker_end}"


def replace_block(text, marker_begin, marker_end, rendered):
    """Return (new_text, status). status: 'written'|'unchanged'|'no-markers'."""
    bi = text.find(marker_begin)
    ei = text.find(marker_end)
    if bi == -1 or ei == -1 or ei < bi:
        return text, "no-markers"
    block_start = bi
    block_end = ei + len(marker_end)
    current = text[block_start:block_end]
    if current == rendered:
        return text, "unchanged"
    return text[:block_start] + rendered + text[block_end:], "written"


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--check", action="store_true",
                        help="Exit 1 if any target block is stale; do not write.")
    args = parser.parse_args(argv)

    cfg = load_config()
    marker_begin = cfg.get("marker_begin")
    marker_end = cfg.get("marker_end")
    targets = cfg.get("targets") or []
    if not marker_begin or not marker_end:
        print("propagate-oneliner: oneliner_propagation markers missing in schema", file=sys.stderr)
        return 2

    one_liner, source = find_source_one_liner()
    if one_liner is None:
        print("propagate-oneliner: no synthesis/*.md carries a `one_liner:` field; nothing to do")
        return 0

    rendered = render_block(one_liner, marker_begin, marker_end)
    stale = []
    for tname in targets:
        tpath = REPO_ROOT / tname
        if not tpath.exists():
            print(f"propagate-oneliner: target {tname} not found", file=sys.stderr)
            return 2
        text = tpath.read_text(encoding="utf-8")
        new_text, status = replace_block(text, marker_begin, marker_end, rendered)
        if status == "no-markers":
            print(f"propagate-oneliner: {tname}: AUTOGEN markers not found", file=sys.stderr)
            return 2
        if status == "unchanged":
            continue
        # status == written
        if args.check:
            stale.append(tname)
        else:
            tpath.write_text(new_text, encoding="utf-8")
            print(f"propagate-oneliner: updated {tname} (source: synthesis/{source.name})")

    if args.check and stale:
        print(f"propagate-oneliner --check: stale block(s): {', '.join(stale)}. "
              f"Run `python3 scripts/propagate-oneliner.py` and re-stage.", file=sys.stderr)
        return 1

    if not args.check:
        print(f"propagate-oneliner: OK (source: synthesis/{source.name})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
