---
name: kb
description: "Chooser for the KB skills. Use when unsure which skill applies or the user asks: how do I add to the KB, what KB skills are there, where should this go."
---

# /kb — Skill Chooser

Output the routing table below verbatim. Do not do anything else unless the user asks.

## Available KB skills

- **/add-entry** — add any typed content (source, comparison, decision, interview, advisor, team member, strategy, brainstorm, synthesis, research-dispatch, experiment, benchmark, traction snapshot). Also handles "save this for later": an unread URL is fetched and filed now
- **/kb-audit** — freshness / consistency check: broken citations, stale drafts, oversized files, orphans, lint errors
- **/kb-synthesize** `<product>` — roll up a new architecture snapshot for `track-a` | `track-b` | `shared`
- **/kb-archive** `<path>` — move a superseded file to `archive/`
- **/kb-add-folder** — add a new top-level folder (forces justification against CONVENTIONS growth rules)
- **/kb-promote** `<path>` — move content along the promotion path (question → dispatch → decision → synthesis)
- **/add-todo** — add a todo / event / meeting with deadline
- **/complete-todo** `<slug>` — mark a todo complete; auto-appends Interactions entry to each related entity
- **/deadlines** — list today-due + overdue-pending (subagent reads frontmatter only)
- **/meeting** — save a meeting or call: verbatim transcript → `raw/transcripts/`, line-linked notes → `meetings/`; propagates action items, outcomes and contacts after confirming each
- **/finance** — ingest a transaction into `finances/ledger.csv` (verbal note, receipt image, or bank statement); parses, categorizes, dedup + reconciles, confirms before writing, redacts statements
- **/financial-summary** `<period>` — generate a persisted, formatted cash-flow summary for a month/quarter/range → `finances/summaries/`. One-off lookups need no skill — just ask
- **/study** `<source|concept|next>` — start or resume a deep-study session on a source or concept. Appends one H2 checkpoint at session end to `study-sessions/<source-filename>.md` or `concepts/<slug>/study-log.md`. `--mode text|voice`.
- **/study-status** `<source|concept>` — read-only resume query: where we left off, open threads, recent context. No session started.
- **/study-unstudied** — list sources + concepts without study logs, ranked by convergence-tag priority.

Optional plugins (install separately):
- **/write-as** — voice-imitation drafting. See `plugins/voice/` for installation.

## Broader routing

For "where does this specific content go?" see **AGENT-GUIDE.md**.
For rules (frontmatter, citations, commits, growth rules): **CONVENTIONS.md**.
For human-facing quickstart: **USER-MANUAL.md**.
