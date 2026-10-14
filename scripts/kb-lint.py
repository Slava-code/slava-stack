#!/usr/bin/env python3
"""
kb-lint.py — Validate frontmatter of project-kb content files
against schema/kb-schema.yaml.

Usage:
    scripts/kb-lint.py [<file>...]   validate specific files
    scripts/kb-lint.py               validate all *.md in repo

Exit code: 0 = pass, 1 = errors found.
Called by scripts/hooks/pre-commit (via core.hooksPath) and by the /kb-audit skill.
"""

import importlib.util
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


def _load_propagate_module():
    """Import scripts/propagate-oneliner.py (hyphenated → importlib) so we reuse
    its source-selection + render logic instead of duplicating it (duplication is
    the drift we're guarding against)."""
    path = REPO_ROOT / "scripts" / "propagate-oneliner.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location("propagate_oneliner", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_oneliner_propagation(schema, errors):
    """Global invariant: each target's AUTOGEN block must equal the canonical
    render of the newest synthesis `one_liner:`. Drift → error with a fix hint.
    Runs once per lint invocation (the invariant is repo-global)."""
    cfg = schema.get("oneliner_propagation") or {}
    mb, me = cfg.get("marker_begin"), cfg.get("marker_end")
    targets = cfg.get("targets") or []
    if not (mb and me and targets):
        return
    prop = _load_propagate_module()
    if prop is None:
        return
    one_liner, source = prop.find_source_one_liner()
    if one_liner is None:
        return  # no source one_liner yet → nothing to enforce
    rendered = prop.render_block(one_liner, mb, me)
    for tname in targets:
        tpath = REPO_ROOT / tname
        if not tpath.exists():
            errors.append(f"{tname}: one-liner propagation target missing")
            continue
        _, status = prop.replace_block(tpath.read_text(encoding="utf-8"), mb, me, rendered)
        if status == "no-markers":
            errors.append(
                f"{tname}: AUTOGEN:product-oneliner markers missing "
                f"(run `python3 scripts/propagate-oneliner.py`)"
            )
        elif status == "written":
            errors.append(
                f"{tname}: product one-liner is STALE vs synthesis/{source.name} — "
                f"run `python3 scripts/propagate-oneliner.py` and re-stage"
            )


# ───────────────────────────────────────────────────────────────
# Currency + reference checks. Anti-drift checks that only run when someone
# remembers to invoke a skill (/kb-audit) do not run often enough; these run on
# every commit instead (via the pre-commit hook).
# ───────────────────────────────────────────────────────────────

WIKILINK_RE = re.compile(r"\[\[([^\]\[]+?)\]\]")
_BASENAME_INDEX = None


def _basename_index():
    """basename-without-.md -> [repo-relative paths]. Built once per run."""
    global _BASENAME_INDEX
    if _BASENAME_INDEX is None:
        idx = {}
        for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
            dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "__pycache__", ".venv")]
            for fn in filenames:
                if fn.endswith(".md"):
                    idx.setdefault(fn[:-3], []).append(Path(dirpath) / fn)
        _BASENAME_INDEX = idx
    return _BASENAME_INDEX


def resolve_link(target, src):
    """Resolve a wikilink / supersedes target written in any of the three styles in
    use (relative `../x/y`, root-relative `x/y`, bare slug). Returns a Path, the
    string "external" for links that leave the repo (e.g. sibling repos),
    or None when nothing matches. Falls back to todos/completed/ so /complete-todo
    moves do not break citations."""
    t = target.split("|")[0].split("#")[0].strip()
    if not t or any(c in t for c in "<>{}*") or "YYYY" in t or t.startswith(("http", "feedback", "project-")):
        return "external"
    t = t[:-3] if t.endswith(".md") else t
    cands = [src.parent / t, REPO_ROOT / t]
    for c in cands:
        try:
            c = c.resolve()
        except OSError:
            continue
        if REPO_ROOT not in c.parents and c != REPO_ROOT:
            return "external"
        for v in (c.with_name(c.name + ".md"), c, c / "README.md"):
            if v.is_file():
                return v
        if c.is_dir():
            return c
    base = Path(t).name
    hits = _basename_index().get(base, [])
    if "/" not in t and hits:
        return hits[0]
    # moved by /complete-todo or /kb-archive: same basename under todos/completed/ or archive/
    for h in hits:
        rel = str(h.relative_to(REPO_ROOT))
        if rel.startswith(("todos/completed/", "archive/")):
            return h
    # wrong `../` depth is the commonest slip: accept when the path tail is unique
    tail = t.lstrip("./")
    for h in hits:
        if str(h.relative_to(REPO_ROOT))[:-3].endswith(tail):
            return h
    return None


def strip_code(body):
    """Drop fenced code blocks, inline code and <details> transcript blocks before link checks."""
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    body = re.sub(r"<details>.*?</details>", "", body, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", body)


def check_wikilinks(filepath, body, errors):
    seen = set()
    for m in WIKILINK_RE.finditer(strip_code(body)):
        tgt = m.group(1)
        if tgt in seen:
            continue
        seen.add(tgt)
        if resolve_link(tgt, filepath) is None:
            errors.append(f"{filepath}: broken wikilink [[{tgt}]] — fix the path (root-relative "
                          f"`folder/file` is the style that survives moves)")


def check_supersedes(fm, filepath, errors):
    """If A says `supersedes: B`, B must say so too — otherwise B still reads as current
    to anyone who lands on it (a dead draft keeps reading as the 'current draft')."""
    val = fm.get("supersedes")
    if not val:
        return
    for tgt in (val if isinstance(val, list) else [val]):
        tgt = str(tgt).strip()
        if not tgt or re.search(r"\s", tgt):   # prose value = partial supersede, not a file pointer
            continue
        b = resolve_link(tgt, filepath)
        if b in (None, "external") or not isinstance(b, Path) or not b.is_file():
            continue
        try:
            bfm, _ = parse_frontmatter(b.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if not bfm:
            continue
        if bfm.get("status") != "superseded" or not bfm.get("superseded_by"):
            errors.append(
                f"{filepath}: supersedes `{tgt}`, but that file is not back-stamped — set "
                f"`status: superseded` + `superseded_by:` + a `> ⚠️ Superseded by [[...]]` banner on "
                f"{b.relative_to(REPO_ROOT)} in the same commit"
            )


CONFIG_FILES = ["CLAUDE.md", "STATE.md", "ALIASES.md", "AGENT-GUIDE.md"]
PATH_TOKEN_RE = re.compile(r"^[A-Za-z0-9_.\-]+(/[A-Za-z0-9_.\-]+)*/?$")
PATH_EXTS = (".md", ".py", ".sh", ".yaml", ".csv", ".json", ".tsv")
# Paths that are legitimately absent: gitignored local files, and example paths
# inside *another* repo (AGENT-GUIDE's github-deep-fetch "files worth reading" list).
PATH_ALLOW = {"runs/.lock", "SOUL.md", ".claude/settings.local.json", "scripts/eval.py"}
BUILTIN_COMMANDS = {"hooks", "doctor", "context", "memory", "workflows", "clear", "model", "config",
                    "plugin", "loop", "skills", "agents", "compact", "help", "init", "fast"}
ALWAYS_LOADED_BUDGET_BYTES = 36000
WARN_SHOW = int(os.environ.get("KB_LINT_WARN_SHOW", "40"))


def check_config(errors, warnings):
    """Global invariant: the always-loaded / routing files may not point at paths or
    skills that no longer exist, or at superseded files. Catches routing rows that
    outlive their target (a routing question pointed at a superseded file, or a
    removed /command still referenced)."""
    files = [REPO_ROOT / f for f in CONFIG_FILES]
    rules_dir = REPO_ROOT / ".claude" / "rules"
    if rules_dir.is_dir():
        files += sorted(rules_dir.rglob("*.md"))
    skills_dir = REPO_ROOT / ".claude" / "skills"
    skills = {p.name for p in skills_dir.iterdir() if p.is_dir()} if skills_dir.is_dir() else set()
    # optional plugins (plugins/<name>/.claude/skills/<skill>/) ship skills too
    skills |= {p.parent.name for p in REPO_ROOT.glob("plugins/*/.claude/skills/*/SKILL.md")}
    skill_files = sorted(skills_dir.glob("*/SKILL.md")) if skills_dir.is_dir() else []
    top = {p.name for p in REPO_ROOT.iterdir()}
    loaded = 0
    for f in files + skill_files:
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        rel = f.relative_to(REPO_ROOT)
        is_skill = f in skill_files
        if not is_skill and (f.parent == REPO_ROOT and f.name != "AGENT-GUIDE.md" or rules_dir in f.parents):
            # rules with `paths:` frontmatter load on demand and do not count
            if not (rules_dir in f.parents and re.match(r"---\n(?:.*\n)*?paths:", text)):
                loaded += len(text.encode("utf-8"))
        scan = text
        if is_skill:  # only the always-listed description, not the body
            m = re.match(r"---\n(.*?)\n---", text, re.S)
            scan = m.group(1) if m else ""
        tokens = set(re.findall(r"`([^`\n]+)`", scan))
        if is_skill:
            tokens |= set(re.findall(r"(?:(?<=\s)|(?<=\()|^)(/[a-z][a-z0-9\-]+)(?![\w/])", scan, re.M))
        for tok in tokens:
            tok = tok.strip()
            m = re.match(r"^/([a-z][a-z0-9\-]+)(\s.*)?$", tok)
            if m:
                if m.group(1) not in skills and m.group(1) not in BUILTIN_COMMANDS:
                    errors.append(f"{rel}: references `/{m.group(1)}`, which is not a skill in .claude/skills/")
                continue
            if is_skill or tok in PATH_ALLOW or tok.startswith(("~", "..", "http", "mcp__", "-")):
                continue
            if not PATH_TOKEN_RE.match(tok):
                continue
            first = tok.split("/")[0]
            if "/" in tok.rstrip("/"):
                if first not in top:
                    continue          # not a repo path (e.g. `x.com/y`, `and/or`)
            elif not tok.endswith(PATH_EXTS) or not tok.endswith("/") and tok not in top and not tok.endswith(".md"):
                continue
            target = REPO_ROOT / tok
            if not target.exists():
                if "/" not in tok.rstrip("/"):
                    continue          # bare filename mentioned generically (e.g. `README.md`)
                errors.append(f"{rel}: points at `{tok}`, which does not exist")
                continue
            if target.is_file() and target.suffix == ".md" and not is_skill:
                try:
                    tfm, _ = parse_frontmatter(target.read_text(encoding="utf-8"))
                except (ValueError, OSError):
                    tfm = None
                if tfm and (tfm.get("status") == "superseded" or tfm.get("superseded_by")):
                    errors.append(f"{rel}: points at `{tok}`, which is superseded — route to its successor")
    if loaded > ALWAYS_LOADED_BUDGET_BYTES:
        warnings.append(f"always-loaded config is {loaded} bytes (budget {ALWAYS_LOADED_BUDGET_BYTES}): "
                        f"CLAUDE.md + STATE.md + ALIASES.md + unscoped .claude/rules/. Trim or path-scope a rule.")
    state = REPO_ROOT / "STATE.md"
    if state.exists() and not re.search(r"^as-of:\s*20\d\d-\d\d-\d\d", state.read_text(encoding="utf-8"), re.M):
        errors.append("STATE.md: missing `as-of: YYYY-MM-DD` line")


# Canonical-name rules: (regex, message). Warnings, not errors — verbatim transcripts
# legitimately contain the short forms. Add one row per entity whose short form
# is ambiguous, e.g.:
#   (re.compile(r"\bExample\b(?!\s+Co\b)"), 'bare "Example" — write "Example Co"'),
NAME_RULES = []


def check_names(filepath, body, warnings):
    text = strip_code(body)
    for rx, msg in NAME_RULES:
        n = len(rx.findall(text))
        if n:
            warnings.append(f"{filepath}: {n}x {msg}")


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


def validate_file(filepath, schema, errors, warnings=None, strict=True):
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

    # Reference checks run on every file handed to the linter, frontmatter or not.
    # `strict` is True for explicitly named files (the pre-commit case: what you
    # touch must be clean) and False for the whole-repo sweep (reported as warnings).
    link_sink = errors if strict else (warnings if warnings is not None else [])
    check_wikilinks(filepath, body if fm else text, link_sink)
    if warnings is not None:
        check_names(filepath, body if fm else text, warnings)

    if fm is None or not fm:
        return  # no frontmatter → skip (navigational / plain README)

    check_supersedes(fm, filepath, link_sink)

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

    # superseded_by: if set, the file must carry a visible banner so a reader
    # landing on it directly sees it's dead (deterministic; safe to enforce).
    if fm.get("superseded_by"):
        if not re.search(r"^>\s*.*[Ss]uperseded by", body, re.MULTILINE):
            errors.append(
                f"{filepath}: has `superseded_by:` but no visible banner — add a top "
                f"blockquote, e.g. `> ⚠️ Superseded by [[...]] — YYYY-MM-DD`"
            )

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
    warnings = []
    strict = bool(args)
    for f in files:
        if not f.exists():
            continue
        if f.suffix != ".md":
            continue
        if is_exempt(f, exempt):
            skipped += 1
            continue
        validate_file(f, schema, errors, warnings, strict)
        checked += 1

    # Global invariant (not per-file): always enforce one-liner propagation.
    check_oneliner_propagation(schema, errors)
    check_config(errors, warnings)

    if warnings:
        print(f"kb-lint: {len(warnings)} warning(s) (non-blocking):", file=sys.stderr)
        for w in warnings[:WARN_SHOW]:
            print(f"  {w}", file=sys.stderr)
        if len(warnings) > WARN_SHOW:
            print(f"  ... and {len(warnings) - WARN_SHOW} more", file=sys.stderr)

    if errors:
        print(f"kb-lint: {len(errors)} error(s) in {checked} file(s):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    print(f"kb-lint: OK ({checked} checked, {skipped} exempt)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
