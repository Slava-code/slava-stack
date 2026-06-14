---
name: kb-synthesize
description: "Roll up a new architecture / state snapshot for a product track (track-a | track-b | shared). Reads all content committed for that product since the last synthesis. Writes a new dated file to synthesis/ with supersedes: pointing at the prior synthesis. Regenerator rebuilds synthesis/INDEX.md. Required anti-sycophancy sections (Counter-arguments, Data gaps) are non-negotiable. Use when user says: synthesize, snapshot architecture, roll up current state, refresh architecture doc, update track-a/track-b snapshot."
---

# /kb-synthesize <product>

Usage: `/kb-synthesize track-a` (or `track-b`, or `shared`).

This skill is a **drift detector**, not just a roll-up. It recency-weights recent commits to propose the CURRENT framing, and propagates a corrected one-liner to the always-loaded T1 layer (`GLOSSARY.md`) — but only when confident.

1. **Acquire `runs/.lock`.**

2. **Baseline.** Most recent `synthesis/*.md` with matching `product:`. Its `date_found` is the baseline; note its `one_liner:` (the prior framing).

3. **Collect the delta.** `git log --since="<baseline>" --name-only`, then keep every changed `*.md` whose frontmatter `product:` matches — **across ALL content folders, EXCLUDING only the operational ones**: `todos/ finances/ inbox/ runs/ raw/ archive/ schema/ scripts/ study-sessions/ team/ .claude/`. (Do NOT use a hardcoded include-list — that silently misses folders. In particular `discovery/` and `advisors/` carry customer-call + advisor-thread signal where positioning shifts surface; an include-list that omits them blinds the drift detector.) `team/` is excluded because it is operational by nature (person profiles, prefs, voice cards); strategic substance belongs in `brainstorming/`/`strategy/`/`decisions/` (which ARE scanned) — if it's sitting in `team/`, it's misfiled, promote it rather than tag it. Untagged files (no `product:`) are skipped — tag them if they should feed synthesis.

4. **No-delta short-circuit (the periodic-run path).** If the delta is empty or trivial (only typo/index commits), DO NOT create a new snapshot. Instead: bump `last_verified: <today>` on the existing synthesis, run `python3 scripts/propagate-oneliner.py` (re-assert the one-liner), stage `GLOSSARY.md` + the synthesis, commit `synthesis: verify <product> still-current @ <date>`, push, release lock, STOP. Report "still current as of <date>."

5. **Read the delta, recency-weighted.** Newer commits outweigh older when deciding "what are we NOW." A late brainstorm/decision/strategy beats an early one on the same question.

6. **Propose `one_liner` + `confidence` + tension check.** Write one current-framing sentence. **PRESERVE source hedges** — `likely`, `target`, `exploring` stay; never harden an exploration into "we ARE X." Then assess: `confidence:` high|medium|low, and **tension** — do recent committed sources contradict each other on the framing (e.g. one leads with one customer segment, the freshest with another)?

7. **Create** `synthesis/YYYY-MM-DD-<product>-architecture.md` from `schema/templates/synthesis.md`. Frontmatter: `supersedes:` the prior file, `one_liner:` your proposed sentence, `last_verified: <today>`, `confidence:`.

8. **Stamp the superseded file.** On the prior synthesis add `superseded_by: synthesis/<new>.md` AND a top-of-body banner `> ⚠️ Superseded by [[synthesis/<new>]] — <date>`. (kb-lint requires the banner when `superseded_by` is set.)

9. **Fill body.** Required: `## Counter-arguments`, `## Data gaps`. Cite the decisions/brainstorms you consolidated. Anti-sycophancy is structural — do not skip.

10. **Confidence-tiered T1 propagation:**
    - **High confidence AND no tension** → run `python3 scripts/propagate-oneliner.py` (writes the new one-liner into `GLOSSARY.md`). Stage `GLOSSARY.md`.
    - **Medium/low confidence OR unresolved tension** → DO NOT propagate. Write `runs/YYYY-MM-DD-<product>-drift.md`: `NEEDS HUMAN: framing in transition — <the tension>; proposed one-liner: <...>; not propagated to GLOSSARY pending confirmation.` Leave `GLOSSARY.md` untouched.

11. **Regenerate INDEXes:** `python3 scripts/rebuild-indexes.py`. Stage changed `INDEX.md`.

12. **Commit + push.** `synthesis: snapshot <product> @ YYYY-MM-DD`. Pre-commit lint enforces: GLOSSARY one-liner matches source (if you propagated) + superseded file has its banner. Fix any failure — never `--no-verify`.

13. **Release the lock.** Report: new snapshot, confidence, and whether T1 was updated or a `NEEDS HUMAN` flag was written.
