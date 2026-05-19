---
name: kb-synthesize
description: "Roll up a new architecture / state snapshot for a product track (track-a | track-b | shared). Reads all content committed for that product since the last synthesis. Writes a new dated file to synthesis/ with supersedes: pointing at the prior synthesis. Regenerator rebuilds synthesis/INDEX.md. Required anti-sycophancy sections (Counter-arguments, Data gaps) are non-negotiable. Use when user says: synthesize, snapshot architecture, roll up current state, refresh architecture doc, update track-a/track-b snapshot."
---

# /kb-synthesize <product>

Usage: `/kb-synthesize track-a` (or `track-b`, or `shared`).

1. Acquire `runs/.lock`.
2. Identify prior synthesis: most recent `synthesis/*.md` with matching `product:`. Its `date_found` is the baseline.
3. Collect all files committed since the baseline, matching `product:`, across: synthesis/, brainstorming/, decisions/, strategy/, research-dispatches/, experiments/, comparisons/. Use `git log --since="<baseline>" --name-only`.
4. Read each; extract the key content for the new snapshot.
5. Create `synthesis/YYYY-MM-DD-<product>-architecture.md` using `schema/templates/synthesis.md`.
6. Fill frontmatter:
   - `supersedes: synthesis/<prior-file>.md`
   - `confidence:` (your honest assessment)
7. Fill body. Required sections (per CONVENTIONS §"Required body sections"):
   - `## Counter-arguments` — strongest case AGAINST the current architecture
   - `## Data gaps` — what we don't know yet
   Do not skip these. Anti-sycophancy is structural.
8. Cite the files you consolidated. Each major decision should cite the `decisions/*.md` or `brainstorming/*.md` that produced it.
9. Regenerate INDEXes: `python3 scripts/rebuild-indexes.py`. synthesis/INDEX.md now lists the new entry alongside the prior (both live in the folder until archived). Stage the regenerated INDEX.md.
10. Stage + commit: `synthesis: snapshot <product> @ YYYY-MM-DD`. Push.
11. Release the lock.
