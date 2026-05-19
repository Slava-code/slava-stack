#!/usr/bin/env python3
"""
kb-convergence-scan — tally convergence tags across brainstorming/.

A brainstorm can declare `convergence: [tag1, tag2, ...]` in frontmatter when
its processor notes "this is the Nth time X has surfaced." This script walks
brainstorming/, tallies tag occurrences, and flags any tag with
>= CONVERGENCE_PROMOTION_THRESHOLD occurrences (default 3) as a promotion
candidate — i.e. the pattern is real and deserves its own questions/ or
research-dispatches/ file rather than staying buried inside individual
brainstorms.

Exit 0 regardless — this is a surfacer, not a validator. Intended to be
called from /kb-audit.

Usage:
    python3 scripts/kb-convergence-scan.py              # report to stdout
    python3 scripts/kb-convergence-scan.py --json       # machine-readable
    python3 scripts/kb-convergence-scan.py --threshold 2
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print("kb-convergence-scan: missing PyYAML; install with `pip install pyyaml`",
          file=sys.stderr)
    sys.exit(1)

DEFAULT_THRESHOLD = 3
REPO_ROOT = Path(__file__).resolve().parent.parent
BRAINSTORM_DIR = REPO_ROOT / "brainstorming"

FRONTMATTER_RE = re.compile(
    r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL
)


def parse_frontmatter(text: str) -> dict | None:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None


def scan(brainstorm_dir: Path) -> dict[str, list[Path]]:
    """Return {tag: [paths]} — one entry per tag, listing every brainstorm
    that declares it."""
    tag_to_files: dict[str, list[Path]] = defaultdict(list)

    if not brainstorm_dir.is_dir():
        return tag_to_files

    for md in sorted(brainstorm_dir.rglob("*.md")):
        if md.name == "INDEX.md":
            continue
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        fm = parse_frontmatter(text)
        if not fm:
            continue
        tags = fm.get("convergence") or []
        if not isinstance(tags, list):
            continue
        for tag in tags:
            if isinstance(tag, str) and tag.strip():
                tag_to_files[tag.strip()].append(md)

    return tag_to_files


def _display_path(path: Path) -> str:
    """Render a path relative to REPO_ROOT when possible; fall back to absolute."""
    try:
        return str(path.relative_to(REPO_ROOT).with_suffix(""))
    except ValueError:
        return str(path.with_suffix(""))


def format_report(
    tag_to_files: dict[str, list[Path]], threshold: int
) -> str:
    """Markdown report suitable for runs/YYYY-MM-DD-convergence.md or stdout."""
    lines: list[str] = []
    promoted = {t: f for t, f in tag_to_files.items() if len(f) >= threshold}
    watching = {t: f for t, f in tag_to_files.items() if 0 < len(f) < threshold}

    lines.append(f"# Convergence scan")
    lines.append("")
    lines.append(f"Threshold for promotion candidacy: **{threshold}** brainstorms "
                 f"sharing a `convergence:` tag.")
    lines.append("")

    if promoted:
        lines.append(f"## Promotion candidates ({len(promoted)})")
        lines.append("")
        lines.append("Each tag below has reached the threshold — consider promoting "
                     "to a `questions/` or `research-dispatches/` file so the "
                     "pattern escapes individual brainstorms.")
        lines.append("")
        for tag, files in sorted(promoted.items(), key=lambda kv: -len(kv[1])):
            lines.append(f"### `{tag}` ({len(files)} brainstorms)")
            lines.append("")
            for path in files:
                lines.append(f"- [[{_display_path(path)}]]")
            lines.append("")
    else:
        lines.append(f"## Promotion candidates (0)")
        lines.append("")
        lines.append("No tags have reached the threshold yet.")
        lines.append("")

    if watching:
        lines.append(f"## Watching (1 — {threshold - 1} occurrences)")
        lines.append("")
        for tag, files in sorted(watching.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            paths = ", ".join(f"[[{_display_path(p)}]]" for p in files)
            lines.append(f"- **`{tag}`** ({len(files)}): {paths}")
        lines.append("")

    if not tag_to_files:
        lines.append("_No `convergence:` tags found in any brainstorm._")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--threshold", type=int, default=DEFAULT_THRESHOLD,
        help=f"Minimum occurrences to surface a tag as a promotion candidate "
             f"(default: {DEFAULT_THRESHOLD}).",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Emit machine-readable JSON instead of markdown.",
    )
    parser.add_argument(
        "--brainstorm-dir", type=Path, default=BRAINSTORM_DIR,
        help=f"Override scan root (default: {BRAINSTORM_DIR}).",
    )
    args = parser.parse_args()

    tag_to_files = scan(args.brainstorm_dir)

    if args.json:
        def _rel(p: Path) -> str:
            try:
                return str(p.relative_to(REPO_ROOT))
            except ValueError:
                return str(p)

        payload = {
            "threshold": args.threshold,
            "tags": {
                tag: [_rel(p) for p in files]
                for tag, files in tag_to_files.items()
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(format_report(tag_to_files, args.threshold))

    return 0


if __name__ == "__main__":
    sys.exit(main())
