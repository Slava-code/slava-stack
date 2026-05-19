---
name: kb-promote
description: "Move project-kb content along the promotion path: questions/ → research-dispatches/ → decisions/ → synthesis/. Handles backlinks, supersedes frontmatter. Regenerator rebuilds folder INDEX.md files automatically. Use when: user says promote this question, elevate to dispatch, formalize as decision, roll this into synthesis. Source file's current folder determines the next step."
---

# /kb-promote <source-path>

Usage: `/kb-promote questions/2026-04-17-example-slug.md`.

1. Acquire `runs/.lock`.
2. Read source file; determine current stage by its folder.
3. Dispatch per the promotion path:

### question → research-dispatch

- Copy source content into `schema/templates/research-dispatch.md` structure.
- Carry the question text as the Hypothesis; bring context into "Prior constraints."
- Target file: `research-dispatches/YYYY-MM-DD-<slug>.md`. Date = today.
- Mark source question: `status: incorporated`, add `supersedes:` line pointing at the new dispatch (note: this is a reverse direction from the normal `supersedes:`; or alternatively, delete the question — user's preference; default to deletion since questions are lightweight).
- Commit: `question: promote <slug> → research-dispatches/<slug>`.

### research-dispatch → decision

- Extract the Recommendation section into a new `decisions/YYYY-MM-DD-<decision-slug>.md` using `schema/templates/decision.md`.
- Required sections: `## Why`, `## What we're giving up`.
- Dispatch file stays (history is the point). Update its frontmatter: `status: incorporated`. Add a pointer to the resulting decision at the end of the dispatch.
- Commit: `research: promote <slug> → decisions/<slug>`.

### decision → synthesis

- No move. A decision becomes a citation in the next `/kb-synthesize <product>` run. Suggest `/kb-synthesize` to user.

4. Regenerate INDEXes: `python3 scripts/rebuild-indexes.py`. Source + destination folder INDEX.md files update automatically. Stage all modified INDEX.md files.
5. Push. Release the lock.
