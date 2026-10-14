---
paths: ["advisors/**", "archive/**", "benchmarks/**", "brainstorming/**", "comparisons/**", "competitions/**", "concepts/**", "decisions/**", "discovery/**", "experiments/**", "finances/**", "meetings/**", "questions/**", "raw/**", "research-dispatches/**", "sources/**", "strategy/**", "study-sessions/**", "synthesis/**", "team/**", "todos/**", "tools/**", "traction/**"]
---
# Writing to the KB

Loads when you read a content file. Full rulebook: `CONVENTIONS.md`; routing: `AGENT-GUIDE.md`. Read both before the first write of a session.

- **Lock.** One writer at a time: create `runs/.lock` (session id + timestamp) before writing, remove it after, including on failure. If it exists and is not yours, stop.
- **Frontmatter.** Required fields per `schema/kb-schema.yaml`. `description:` is at most 120 characters, with no wikilinks; it is what the INDEX and the prompt hook show, so make it say what the file is.
- **Links.** Root-relative wikilinks (`[[folder/file]]`): the style that survives moves. Lint rejects links that do not resolve.
- **New version of a doc.** New file with `supersedes:`; in the same commit stamp the old file `status: superseded` + `superseded_by:` + a `> ⚠️ Superseded by [[...]]` banner (lint enforces the pair), and update the hub's current-docs row. Never write "current" or "canonical" into a description or README by hand; it rots.
- **Closing a thread.** When a decision, outcome or completed todo closes a thread, put a one-line outcome banner (or a resolution stamp, CONVENTIONS §"Growth rules") on the files that still read as open, and link the closing file.
- **State.** If the write changes what is true now, update the matching line in `STATE.md` and bump its `as-of:`. A new recurring name gets a row in `ALIASES.md`.
- **Transcripts: two files per call.** (1) The verbatim transcript, unedited, as its own file in `raw/transcripts/YYYY-MM-DD-<slug>.md` (`type: source`, a short header, then the text; never edited afterwards, so line numbers stay stable). (2) The meeting file in `meetings/` is the notes, and every claim links to the line it came from: `[T:NN](../raw/transcripts/<file>.md#LNN)`. "The full transcript lives in the recording app" is not a record; if the user has not pasted it, ask for it.
- **Raw artifacts.** Emails, deck PDFs, contracts, event material go in `raw/<kind>/` with a same-name `.md` sidecar so they are searchable (see `raw/README.md`).
- **Agent-written notes** (session dumps, brainstorm write-ups) stay `status: raw` and say so; verbatim statements by the team are marked as such with the date.
- **Commit.** One commit per atomic change with the prefix from `CONVENTIONS.md` § "Commit convention"; stage explicit paths, never `git add -A`. The post-commit hook pushes; if it fails, fix it before continuing. Run `git pull --rebase` first if another session may have pushed.
- **Renders.** HTML or PDF renders of KB docs go to `raw/renders/YYYY-MM-DD-<slug>.html`, never the repo root (this overrides any user-level "write HTML in the current directory" default for this repo).
- **Never** run deploy or publish commands (`vercel`, `npm publish`, `wrangler deploy`) from this directory; a hook in `.claude/settings.json` blocks them.
