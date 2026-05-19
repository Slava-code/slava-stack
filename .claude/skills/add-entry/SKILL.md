---
name: add-entry
description: "Add typed content to the project-kb. Classifies the destination folder, copies the matching template from schema/templates/, fills frontmatter (including required `description:` field) and body, runs the INDEX generator, commits with a proper prefix, pushes. Respects the single-writer lock. Use when the user says: save this to the KB, add this source/comparison/decision/interview/experiment, log this brainstorm, record this advisor profile, add a team member, etc. Do NOT use for quick URL drops (use /drop) or todos (use /add-todo)."
---

# /add-entry — Add content to the KB

Steps:

1. **Acquire the single-writer lock.** Check `runs/.lock`. If it exists, abort with "another agent is writing, retry later." Otherwise write `<session-id> <ISO-timestamp>` to it.
2. **Classify.** Use AGENT-GUIDE.md §"Where does this content go?" to pick the destination folder. If ambiguous, ask the user.
3. **Copy template.** From `schema/templates/<type>.md` to the target path. File naming per CONVENTIONS §"File naming" (dated flat file OR entity folder — see comparisons/advisors/discovery/team conventions).
4. **Fill frontmatter.** All required fields for the type (see `schema/kb-schema.yaml`). Do not invent values — ask the user where needed. Always write a `description:` field (≤120 chars, rule-not-summary, no wikilinks/links, include category keyword — see the template's placeholder hint for examples).
5. **Fill body.** Keep required sections per CONVENTIONS §"Required body sections":
   - synthesis: `## Counter-arguments`, `## Data gaps`
   - decision: `## Why`, `## What we're giving up`
   - comparison: `## Decision`
6. **Regenerate INDEXes.** Run `python3 scripts/rebuild-indexes.py`. It rewrites the destination folder's `INDEX.md` (and root `INDEX.md` if a new folder was created). Stage any modified INDEX.md files alongside the new content file.
7. **Stage + commit + push.** Use the right commit prefix per CONVENTIONS §"Commit convention". Message format: `<prefix>: <verb> <slug>`. Always push after.
8. **Release the lock.** `rm runs/.lock`.

If the pre-commit lint fails: fix the content (or amend the schema, with a separate `schema:` commit) — never `--no-verify`.

Required reading first time: CONVENTIONS.md, AGENT-GUIDE.md, schema/kb-schema.yaml.
