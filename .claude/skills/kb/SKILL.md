---
name: kb
description: "project-kb skill index and chooser. Use when unsure which KB skill applies. Returns a routing table of every project skill (/add-entry, /drop, /kb-process-inbox, /kb-audit, /kb-synthesize, /kb-archive, /kb-add-folder, /kb-promote, /add-todo, /complete-todo, /deadlines, /study, /study-status, /study-unstudied) with one-line purpose. Safe to invoke anytime. Invoke for queries like 'how do I add to the KB?', 'what KB skills are there?', 'I have something to save but not sure where', 'which skill should I use?'."
---

# /kb — Skill Chooser

Output the routing table below verbatim. Do not do anything else unless the user asks.

## Available KB skills

- **/add-entry** — add any typed content (source, comparison, decision, interview, advisor, team member, strategy, brainstorm, synthesis, research-dispatch, experiment, benchmark, traction snapshot)
- **/drop** `<content|url>` — quick-capture to inbox without classifying
- **/kb-process-inbox** — drain inbox; each drop processed by a fresh subagent (keeps main context clean)
- **/kb-audit** — freshness / consistency check: broken citations, stale drafts, oversized files, orphans, lint errors
- **/kb-synthesize** `<product>` — roll up a new architecture snapshot for `track-a` | `track-b` | `shared`
- **/kb-archive** `<path>` — move a superseded file to `archive/`
- **/kb-add-folder** — add a new top-level folder (forces justification against CONVENTIONS growth rules)
- **/kb-promote** `<path>` — move content along the promotion path (question → dispatch → decision → synthesis)
- **/add-todo** — add a todo / event / meeting with deadline
- **/complete-todo** `<slug>` — mark a todo complete; auto-appends Interactions entry to each related entity
- **/deadlines** — list today-due + overdue-pending (subagent reads frontmatter only)
- **/study** `<source|concept|next>` — start or resume a deep-study session on a source or concept. Appends one H2 checkpoint at session end to `study-sessions/<source-filename>.md` or `concepts/<slug>/study-log.md`. `--mode text|voice`.
- **/study-status** `<source|concept>` — read-only resume query: where we left off, open threads, recent context. No session started.
- **/study-unstudied** — list sources + concepts without study logs, ranked by convergence-tag priority.

Optional plugins (install separately):
- **/write-as** — voice-imitation drafting. See `plugins/voice/` for installation.

## Broader routing

For "where does this specific content go?" see **AGENT-GUIDE.md**.
For rules (frontmatter, citations, commits, growth rules): **CONVENTIONS.md**.
For human-facing quickstart: **USER-MANUAL.md**.
