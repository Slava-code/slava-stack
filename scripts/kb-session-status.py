#!/usr/bin/env python3
"""kb-session-status.py - one short staleness report, printed into context at session start.

Run by the SessionStart hook in .claude/settings.json. Makes drift visible in every
session instead of only when someone remembers to run /kb-audit or /deadlines:
  - how old STATE.md is and how many dated files are newer than it (only when the
    KB keeps a STATE.md current-truth card; silent otherwise)
  - how far the newest synthesis of each product track is behind
  - pending todos past their deadline (a pending todo past its date means UNKNOWN,
    not "not done": ask before relying on it)
  - days since the last /kb-audit run
Read-only, stdlib only, silent on any error (a hook must not block the session).
"""
import datetime
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today()
DATE_RE = re.compile(r"^(20\d\d-\d\d-\d\d)")
# folders whose dated files change "what is true now"
STATE_FOLDERS = ("meetings", "decisions", "competitions", "strategy", "traction", "discovery")
SYNTH_FOLDERS = STATE_FOLDERS + ("brainstorming", "comparisons", "research-dispatches")
SKIP_DIRS = ("completed",)  # moved-out todos and similar history
STATE_STALE_DAYS = 14      # STATE.md older than this with newer files behind it -> flag
SYNTH_STALE_FILES = 25     # dated files newer than a track's newest synthesis -> flag
AUDIT_STALE_DAYS = 30


def fdate(name):
    m = DATE_RE.match(name)
    if not m:
        return None
    try:
        return datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return None


def dated_files(folders):
    for folder in folders:
        base = os.path.join(ROOT, folder)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if fn.endswith(".md"):
                    d = fdate(fn)
                    if d and d <= TODAY:
                        yield d, os.path.relpath(os.path.join(dirpath, fn), ROOT)


def head(path, n=40):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return "".join(next(fh, "") for _ in range(n))
    except OSError:
        return ""


def synth_track(path):
    """synthesis/YYYY-MM-DD-<track>-architecture.md -> <track>."""
    stem = os.path.basename(path)[11:]
    stem = stem[:-3] if stem.endswith(".md") else stem
    return stem[:-len("-architecture")] if stem.endswith("-architecture") else stem


def main():
    out = []

    # STATE.md age (only if the KB keeps one)
    state = os.path.join(ROOT, "STATE.md")
    if os.path.exists(state):
        m = re.search(r"^as-of:\s*(20\d\d-\d\d-\d\d)", head(state, 8), re.M)
        if m:
            asof = datetime.date.fromisoformat(m.group(1))
            newer = sorted((d, p) for d, p in dated_files(STATE_FOLDERS) if d > asof)
            age = (TODAY - asof).days
            if newer and age > STATE_STALE_DAYS:
                out.append("STATE.md is %d days old (as-of %s) and %d dated files are newer, e.g. %s. "
                           "Check them against STATE.md before trusting it; update it if anything changed."
                           % (age, asof, len(newer), ", ".join(p for _, p in newer[-3:])))
        else:
            out.append("STATE.md has no `as-of:` line.")

    # synthesis lag, per product track
    newest = {}
    for d, p in dated_files(("synthesis",)):
        t = synth_track(p)
        if t and (t not in newest or d > newest[t]):
            newest[t] = d
    if newest:
        others = list(dated_files(SYNTH_FOLDERS))
        for t, last in sorted(newest.items()):
            behind = sum(1 for d, _ in others if d > last)
            if behind > SYNTH_STALE_FILES:
                out.append("Newest %s synthesis is %s: %d days and %d dated files behind. "
                           "Treat it as history where newer files disagree; suggest /kb-synthesize %s."
                           % (t, last, (TODAY - last).days, behind, t))

    # overdue pending todos
    overdue = []
    tdir = os.path.join(ROOT, "todos")
    if os.path.isdir(tdir):
        for fn in sorted(os.listdir(tdir)):
            d = fdate(fn)
            if d and d < TODAY and fn.endswith(".md") and re.search(r"^status:\s*pending", head(os.path.join(tdir, fn)), re.M):
                overdue.append(fn[:-3])
    if overdue:
        out.append("%d pending todos are past their deadline (status UNKNOWN, not 'not done'; ask before relying on them): %s%s"
                   % (len(overdue), ", ".join(overdue[-5:]), " ..." if len(overdue) > 5 else ""))

    # audit age
    rdir = os.path.join(ROOT, "runs")
    audits = sorted(d for d in (fdate(f) for f in os.listdir(rdir) if "audit" in f) if d) if os.path.isdir(rdir) else []
    if audits and (TODAY - audits[-1]).days > AUDIT_STALE_DAYS:
        out.append("Last /kb-audit was %s (%d days ago)." % (audits[-1], (TODAY - audits[-1]).days))

    if out:
        sys.stdout.write("KB status (scripts/kb-session-status.py):\n" + "\n".join("- " + o for o in out) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
