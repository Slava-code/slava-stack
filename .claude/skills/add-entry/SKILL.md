---
name: add-entry
description: "File content into the KB: source, comparison, decision, brainstorm, strategy, interview, experiment, advisor or team profile. Use when the user says: save this to the KB, add this, log this, record this, file this for later (with an unread URL: fetch it now). Picks folder and template, fills frontmatter, commits, pushes. Not for todos (add-todo skill) or transcripts (meeting skill)."
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
6. **Stamp any thread this entry resolves.** Ask: does this new entry answer an *open thread* recorded in an existing doc — a `## Open threads` bullet, a `[?question]` / `[?decision]` tag, an unresolved question you remember from this session? If yes, apply an inline **resolution stamp** to that doc (CONVENTIONS §"Growth rules" → "Resolution stamps"): `**Resolved YYYY-MM-DD → [[this-entry]]:** <one line>` at the head of the resolved bullet, original text left below. Add a back-link from this entry's `## Related`. Do NOT supersede/rewrite the host doc — it stays live. Stage the stamped doc to commit alongside the new entry. Skip if nothing is resolved (most entries resolve nothing — don't manufacture one).
6a. **Check for an existing entry and back-stamp versions.** Run `python3 scripts/kb-prompt-lookup.py "<entity or slug>"` first: if the entity already has a file or hub, update or link it instead of creating a parallel one. If this file replaces an older version (`-vN`, `draft-N`, a newer deck), set `supersedes:` here AND stamp the old file `status: superseded` + `superseded_by:` + a `> ⚠️ Superseded by [[...]]` banner, and update the hub's current-docs row. Lint rejects the commit otherwise. Collateral made for one specific program, customer or project goes in that entity's folder, not `strategy/`.
6b. **Keep current truth current.** Ask: does this change what is true now — an outcome, a status, a number, a price, a decision, who someone is? If yes: (a) edit the matching line in `STATE.md` and bump its `as-of:` date; (b) update the hub README if the entity has one (see `ALIASES.md`); (c) add a new row to `ALIASES.md` for any new recurring name, nickname or transcript mis-spelling; (d) put a one-line outcome banner on older files that still read as open. Stage these in the same commit set. Skip silently if nothing changed.
7. **Regenerate INDEXes.** Run `python3 scripts/rebuild-indexes.py`. It rewrites the destination folder's `INDEX.md` (and root `INDEX.md` if a new folder was created). Stage any modified INDEX.md files alongside the new content file.
8. **Stage + commit + push.** Use the right commit prefix per CONVENTIONS §"Commit convention". Message format: `<prefix>: <verb> <slug>`. Always push after.
9. **Release the lock.** `rm runs/.lock`.

If the pre-commit lint fails: fix the content (or amend the schema, with a separate `schema:` commit) — never `--no-verify`.

Required reading first time: CONVENTIONS.md, AGENT-GUIDE.md, schema/kb-schema.yaml.
