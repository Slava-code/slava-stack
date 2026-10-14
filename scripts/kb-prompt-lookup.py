#!/usr/bin/env python3
"""kb-prompt-lookup.py - point at the KB files most likely relevant to a prompt.

Usage:
    scripts/kb-prompt-lookup.py "<terms or raw prompt>"   manual search
    scripts/kb-prompt-lookup.py --hook                    UserPromptSubmit hook: reads the
                                                          hook JSON on stdin, prints context

Searches this KB. Gitignored private notes (any `private/` folder, e.g.
team/*/private/) are skipped by default so their paths never land in context; set
KB_LOOKUP_INCLUDE_PRIVATE=1 to search them too. Shorthand is expanded through
ALIASES.md when that file exists (format: `| alias / alias | canonical | `hub`<br>`hub` |`).
Superseded files and older -vN / draft-N siblings are ranked down and labelled;
brainstorms older than KB_BRAINSTORM_CUTOFF (YYYY-MM-DD, optional) are ranked
down too. Prints at most 12 lines, or nothing when nothing scores. Read-only,
stdlib only, never fails loudly (a hook must not block the prompt).

Environment (all optional): KB_ROOT (default: this script's repo), KB_ALIASES
(default: $KB_ROOT/ALIASES.md), KB_LOOKUP_INCLUDE_PRIVATE, KB_BRAINSTORM_CUTOFF.
"""
import datetime
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KB_ROOT = os.environ.get("KB_ROOT") or os.path.dirname(HERE)
ROOTS = [("", KB_ROOT)]
INCLUDE_PRIVATE = os.environ.get("KB_LOOKUP_INCLUDE_PRIVATE") == "1"
ALIASES_MD = os.environ.get("KB_ALIASES", os.path.join(KB_ROOT, "ALIASES.md"))
MAX_LINES = 12
DESC_MAX = 110
COMMON_DF = 60    # above this, a title/description match alone is not strong evidence
RARE_DF = 25      # a term found in at most this many files is "rare"
REL_CUT = 0.40    # drop non-hub lines scoring below this fraction of the top line
TODAY = datetime.date.today()


def _cutoff():
    try:
        return datetime.date.fromisoformat(os.environ.get("KB_BRAINSTORM_CUTOFF", ""))
    except ValueError:
        return None


BRAINSTORM_CUTOFF = _cutoff()   # None = no brainstorm down-ranking by age
EXCLUDE_DIRS = {".git", "runs", "archive", "node_modules", "__pycache__", ".venv",
                ".claude", "worktrees"} | (set() if INCLUDE_PRIVATE else {"private"})
EXCLUDE_PREFIXES = ("raw/transcripts/", "runs/fetches/")
MAX_FILE_BYTES = 400_000  # bigger files are raw dumps, not digests
SKIP_NAMES = {"INDEX.md", "ALIASES.md", "STATE.md", "CLAUDE.md", "AGENTS.md", "MEMORY.md"}  # auto-generated listings: they match everything and say nothing

STOP = set("""a about above after again all also am an and any are aren as at be because been before being below
between both but by can could did do does doing don down during each few for from further get give got had has have
having he her here hers him his how i if in into is it its just kb know let like me more most my no nor not now of off
on once only or other our ours out over own please s same she should so some such t tell than that the their them
then there these they this those through to too under until up us very was we were what when where which while who
whom why will with would you your yours vs versus compare compared say says said find show look need want make made
thing things stuff use using used new one two think file files doc docs document page write draft update status
whats what's who's hows going go happened happen did tell about much many still yet ever any again
check read open see give summarize summary explain help thanks thank ok okay yes yeah good great looks sure cool
nice fine right fix please lets let's can't cant don't dont it's im i'm""".split())
RECENCY_WORDS = {"latest", "newest", "current", "recent", "last", "now", "today", "currently", "final"}

FM_KEYS = ("title", "description", "tags", "aliases", "status", "superseded_by", "supersedes", "updated", "date_found", "deadline")
DATE_RE = re.compile(r"(20\d\d)-(\d\d)-(\d\d)")
VER_RE = re.compile(r"-(?:draft-|v)(\d+)(?=-|$)")


def walk(root):
    """Yield (rel, text) for every searchable .md under root (gitignored paths included)."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if not fn.endswith(".md") or fn in SKIP_NAMES:
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            if rel.startswith(EXCLUDE_PREFIXES):
                continue
            try:
                if os.path.getsize(full) > MAX_FILE_BYTES:
                    continue
                with open(full, encoding="utf-8", errors="replace") as fh:
                    yield rel, fh.read()
            except OSError:
                continue


def term_regex(term):
    """Word-boundary regex for a term; words of a phrase may be joined by space, hyphen or underscore."""
    return r"\b" + term_core(term) + r"\b"


def term_core(term):
    words = [w for w in re.split(r"[\s\-_]+", term) if w]
    out = []
    for i, w in enumerate(words):
        last = i == len(words) - 1
        if last and len(w) > 4 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        out.append(re.escape(w) + (r"(?:s|es)?" if last and len(w) > 3 else ""))
    return r"[\s\-_]?".join(out)


def load_aliases():
    """Parse the ALIASES.md table: | alias / alias | canonical | `hub`<br>`hub` |."""
    rows = []
    try:
        with open(ALIASES_MD, encoding="utf-8") as fh:
            lines = fh.readlines()
    except OSError:
        return rows
    for line in lines:
        if not line.startswith("|") or line.startswith("|---") or line.lower().startswith("| alias"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        aliases = [a.strip().lower() for a in cells[0].split(" / ") if a.strip()]
        canon = re.split(r"[,(;:]", cells[1])[0].strip().lower()
        extra = [canon] if canon and len(canon.split()) <= 4 and not canon.isupper() else []
        hubs = re.findall(r"`([^`]+)`", cells[2])
        if aliases:
            rows.append((aliases, extra, hubs))
    return rows


def parse_prompt(prompt, alias_rows):
    """Return (terms, hub_rank dict, want_recent). terms: list of (term, weight_class)."""
    low = prompt.lower()
    hubs = {}
    terms = []
    consumed = set()
    for aliases, extra, hub_paths in alias_rows:
        hit = None
        for a in sorted(aliases, key=len, reverse=True):
            if re.search(r"(?<![a-z0-9])" + re.escape(a) + r"(?:'s|s)?(?![a-z0-9])", low):
                hit = a
                break
        if not hit:
            continue
        consumed.update(re.findall(r"[a-z0-9]+", hit))
        for i, h in enumerate(hub_paths):
            hubs[h] = min(hubs.get(h, 99), i)
        for t in (extra or [hit]):
            if t not in [x for x, _ in terms]:
                terms.append((t, "alias"))
    tokens = re.findall(r"[a-z0-9][a-z0-9&+\-]*[a-z0-9]|[a-z0-9]", low)
    want_recent = any(t in RECENCY_WORDS for t in tokens)
    for t in tokens:
        base = t[:-2] if t.endswith("'s") else t
        if base in STOP or base in RECENCY_WORDS or base in consumed or len(base) < 2:
            continue
        if base.isdigit() and len(base) < 4:
            continue
        if base not in [x for x, _ in terms]:
            terms.append((base, "token"))
    return terms[:10], hubs, want_recent


def read_head(path):
    """Frontmatter fields + first heading from the first lines of a file."""
    fm, heading = {}, ""
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = [next(fh, "") for _ in range(45)]
    except OSError:
        return fm, heading
    in_fm = lines and lines[0].strip() == "---"
    for ln in lines[1:] if in_fm else lines:
        s = ln.strip()
        if in_fm:
            if s == "---":
                in_fm = False
                continue
            m = re.match(r"([A-Za-z_]+):\s*(.*)$", ln)
            if m and m.group(1) in FM_KEYS:
                fm[m.group(1)] = m.group(2).strip().strip("\"'")
        elif s.startswith("#") and not heading:
            heading = s.lstrip("#").strip()
            break
    return fm, heading


def file_date(rel, fm, full):
    m = DATE_RE.search(os.path.basename(rel))
    cands = [m.group(0)] if m else []
    for k in ("updated", "date_found"):
        mm = DATE_RE.search(fm.get(k, ""))
        if mm:
            cands.append(mm.group(0))
    best = None
    for c in cands:
        try:
            d = datetime.date.fromisoformat(c)
        except ValueError:
            continue
        if d <= TODAY + datetime.timedelta(days=1) and (best is None or d > best):
            best = d
    if best is None and m:  # future-dated filename (todo deadline): keep it for display
        try:
            best = datetime.date.fromisoformat(m.group(0))
        except ValueError:
            best = None
    if best is None:
        try:
            best = datetime.date.fromtimestamp(os.path.getmtime(full))
        except OSError:
            best = None
    return best


def family(rel):
    """(family key, version) for -vN / draft-N siblings; version 0 when unversioned."""
    d, base = os.path.split(rel)
    stem = re.sub(r"^20\d\d-\d\d-\d\d-", "", base[:-3] if base.endswith(".md") else base)
    m = VER_RE.search(stem)
    if m:
        return (d, stem[:m.start()]), int(m.group(1))
    return (d, stem), 0


def run(prompt, hook=False):
    terms, hubs, want_recent = parse_prompt(prompt, load_aliases())
    if not terms and not hubs:
        return []
    if hook and not hubs and len(re.findall(r"\w+", prompt)) > 45:
        return []
    text_res = {t: re.compile(term_regex(t), re.I) for t, _ in terms}
    sup_re = re.compile(r"^supersedes:\s*(\S.*)$", re.M)

    rootmap = dict(ROOTS)
    all_files = []   # (key, prefix, rel)
    body = {}        # key -> {term: count}
    df = {t: 0 for t, _ in terms}
    superseded = set()
    for prefix, root in ROOTS:
        if not root or not os.path.isdir(root):
            continue
        for rel, text in walk(root):
            key = prefix + rel
            all_files.append((key, prefix, rel))
            for t, _ in terms:
                c = len(text_res[t].findall(text))
                if c:
                    body.setdefault(key, {})[t] = c
                    df[t] += 1
            m = sup_re.search(text[:3000])
            if m:
                for tgt in m.group(1).strip().strip("[]").split(","):
                    tgt = tgt.strip().strip("[]\"' ")
                    # a value with prose in it is a partial supersede: ignore
                    if not tgt or re.search(r"\s", tgt):
                        continue
                    if "/" not in tgt:
                        tgt = os.path.join(os.path.dirname(rel), tgt)
                    tgt = os.path.normpath(tgt)
                    if not tgt.endswith(".md"):
                        tgt += ".md"
                    superseded.add(prefix + tgt)
    nfiles = max(len(all_files), 1)

    # newest version per sibling family
    fam_max = {}
    for key, prefix, rel in all_files:
        fk, v = family(rel)
        fk = (prefix,) + fk
        fam_max[fk] = max(fam_max.get(fk, 0), v)

    # rare terms count for more than common ones
    idf = {t: 0.35 + 0.65 * (math.log((nfiles + 1) / (df[t] + 1)) / math.log(nfiles + 1)) for t, _ in terms}

    name_res = {t: re.compile(r"(?<![a-z0-9])" + term_core(t) + r"(?![a-z0-9])") for t, _ in terms}
    cands = {}
    for key, prefix, rel in all_files:
        base = os.path.basename(rel).lower()
        # README-style files are named by their folder
        namestr = (os.path.basename(os.path.dirname(rel)).lower() + "/" + base) if base in ("readme.md",) else base
        name_hits = [t for t, _ in terms if name_res[t].search(namestr)]
        if key in hubs or name_hits or key in body:
            cands[key] = (prefix, rel, name_hits)

    # cheap pre-rank so only a bounded number of file heads are read
    def pre(key):
        _, _, nh = cands[key]
        b = body.get(key, {})
        return (200 if key in hubs else 0) + 30 * len(nh) + sum(idf[t] * min(c, 20) for t, c in b.items())
    shortlist = sorted(cands, key=pre, reverse=True)[:160]

    scored = []
    nterms = max(len(terms), 1)
    has_alias = any(c == "alias" for _, c in terms)
    for key in shortlist:
        prefix, rel, name_hits = cands[key]
        full = os.path.join(rootmap[prefix], rel)
        fm, heading = read_head(full)
        meta = (fm.get("title", "") + " " + fm.get("description", "")).lower()
        tags = (fm.get("tags", "") + " " + fm.get("aliases", "")).lower()
        b = body.get(key, {})
        score, matched, strong, meta_hits, alias_hit = 0.0, set(), False, 0, False
        if key in hubs:
            score += 120 - 8 * hubs[key]
            strong = True
        for t, cls in terms:
            w = idf[t] * (1.25 if cls == "alias" else 1.0)
            if t in name_hits:
                score += 34 * w
                matched.add(t)
                strong = True
                alias_hit = alias_hit or cls == "alias"
            if meta and text_res[t].search(meta):
                score += 18 * w
                matched.add(t)
                meta_hits += 1
                # a common word in a description is weak evidence on its own
                if cls == "alias" or df[t] <= COMMON_DF:
                    strong = True
            elif tags and text_res[t].search(tags):
                score += 11 * w
                matched.add(t)
                strong = True
            c = b.get(t, 0)
            if c:
                score += min(14.0, 3.5 * math.log2(1 + c)) * w
                matched.add(t)
        if not matched and key not in hubs:
            continue
        if meta_hits >= 2:
            strong = True
        cover = len(matched) / nterms
        # one generic word matching while the rest of the prompt is absent from the file: skip
        if nterms >= 2 and cover < 0.5 and key not in hubs and not alias_hit and not has_alias:
            continue
        score += 26 * cover * cover if nterms > 1 else 0
        # body-only hits count only for a rare term mentioned repeatedly, or dense full coverage
        rare = any(df[t] <= RARE_DF and b.get(t, 0) >= 2 for t, _ in terms)
        if not strong:
            dense = cover == 1.0 and sum(b.values()) >= 6
            if not (rare or dense):
                continue
        d = file_date(rel, fm, full)
        if d:
            age = max((TODAY - d).days, 0)
            rec = max(0.0, 1.0 - age / 150.0)
            score += rec * (30 if want_recent else 14)
        status = fm.get("status", "").lower()
        fk, v = family(rel)
        is_sup = status == "superseded" or bool(fm.get("superseded_by")) or key in superseded
        older_sibling = v < fam_max.get((prefix,) + fk, 0)
        if is_sup or older_sibling:
            score -= 45
        if BRAINSTORM_CUTOFF and rel.startswith("brainstorming/") and d and d < BRAINSTORM_CUTOFF:
            score -= 25
        if "/completed/" in rel:
            score -= 6
        if "/templates/" in rel or rel.startswith("schema/"):
            score -= 40
        if score <= 12 and key not in hubs:
            continue
        desc = fm.get("description") or fm.get("title") or heading or ""
        scored.append((score, key, d, status, is_sup or older_sibling, desc, strong, rare, cover))

    scored.sort(key=lambda x: (-x[0], x[1]))
    # with no hub / filename / frontmatter match anywhere, only rare-term body hits are worth a line
    if not any(x[6] for x in scored):
        scored = [x for x in scored if x[7]]
    if not scored:
        return []
    top, top_cover = scored[0][0], scored[0][8]
    out, body_only = [], 0
    for score, key, d, status, sup, desc, strong, rare, cover in scored:
        if len(out) >= MAX_LINES:
            break
        if key not in hubs:
            if score < max(16.0, top * REL_CUT):
                break
            # a line matching far fewer of the prompt's terms than the best line is usually noise
            if cover < 0.6 * top_cover:
                continue
            if not strong:
                if body_only >= 3 or score < top * 0.5:
                    continue
                body_only += 1
        desc = re.sub(r"\s+", " ", desc).strip()
        if len(desc) > DESC_MAX:
            desc = desc[:DESC_MAX - 1].rstrip() + "…"
        tag = "[%s, %s]" % (d.isoformat() if d else "undated", status or "no-status")
        if sup:
            tag += " [SUPERSEDED]"
        out.append("%s %s - %s" % (key, tag, desc))
    return out


HOOK_HEADER = ("KB lookup (automatic, scripts/kb-prompt-lookup.py): files that may hold the answer, best first. "
               "Open what is relevant before answering; [SUPERSEDED] = history.")


def main():
    args = sys.argv[1:]
    if args and args[0] == "--hook":
        try:
            prompt = (json.load(sys.stdin).get("prompt") or "").strip()
        except Exception:
            return
        # slash commands, one-word replies and "continue" need no lookup
        if not prompt or prompt.startswith("/") or len(prompt) < 12:
            return
        # Long pasted text (transcripts, tool output, agent reports) matches half the KB on
        # generic words. For those, only answer when a known alias is named.
        out = run(prompt[:800], hook=True)
        if out:
            sys.stdout.write(HOOK_HEADER + "\n" + "\n".join(out) + "\n")
        return
    if not args or not " ".join(args).strip():
        return
    out = run(" ".join(args))
    if out:
        sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # a hook must never block the prompt
        pass
