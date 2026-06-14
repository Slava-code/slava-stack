# Conventions — project-kb

The rulebook. How content is structured, how it grows, how skills enforce discipline. Read once; cite from skills and files rather than re-stating.

Sibling documents:
- [`CLAUDE.md`](CLAUDE.md) — T0 boot anchor for any agent landing in this repo
- [`AGENT-GUIDE.md`](AGENT-GUIDE.md) — T1 routing table: "where does X go?"
- [`INDEX.md`](INDEX.md) — T1 auto-generated one-line index per top-level folder; each folder has its own `INDEX.md` listing entries
- [`GLOSSARY.md`](GLOSSARY.md) — vocabulary used across this KB and the external patterns it borrows from
- [`LIMITS.md`](LIMITS.md) — what this KB deliberately does not try to capture
- [`READING-GUIDES.md`](READING-GUIDES.md) — per-persona entry paths
- [`schema/kb-schema.yaml`](schema/kb-schema.yaml) — machine-readable frontmatter contract

---

## What this KB is

A startup's running knowledge base — research, architecture decisions, brainstorms, experiments, competitor analyses, customer interviews, advisor outreach, strategy, GTM, fundraising. Everything the team needs to reason about together that isn't already authoritatively documented inside a sub-project's source tree.

**Overlay, not rewrite.** When authoritative content exists in another repo (a product codebase, a separate ops repo), cite with relative wikilinks instead of duplicating.

---

## Product tracks

Every file declares a `product:` in frontmatter. The default schema ships three placeholder tracks — rename them once for your project and never again.

| Track (default) | What it's for |
|---|---|
| `track-a` | Your primary product line |
| `track-b` | A second product line, intermediate play, or OSS variant |
| `shared` | Cross-cutting material that applies to multiple tracks |

To rename: edit `schema/kb-schema.yaml` §`enums.product`, then update any existing files via search-and-replace. Single-track projects can collapse all three to one value (e.g. always `track-a`) without breaking anything.

**Strategic threads** are orthogonal to tracks. Use optional `strategic-thread:` frontmatter (multi-value) to tag cross-cutting initiatives: `oss`, `gtm`, `fundraising`, `partnerships`, `hiring`, etc. Edit `schema/kb-schema.yaml` §`enums.strategic_thread` to match your initiatives. Cross-folder thread rollup is not auto-generated — use `grep -l 'strategic-thread:.*fundraising'` to find entries for a given thread.

---

## Folder layout

| Folder | Purpose | When written |
|---|---|---|
| [`synthesis/`](synthesis/) | Architecture snapshots — one per product. Most recent dated file per `product:` = current view. | On explicit ask to "synthesize" / "snapshot" |
| [`brainstorming/`](brainstorming/) | Exploratory thought processes — options weighed, half-formed ideas, train of thought. | On explicit ask to "save this brainstorm" |
| [`strategy/`](strategy/) | Crystallized decisions on GTM, positioning, pricing, fundraising, partnerships. Distinct from brainstorming: strategy is settled, brainstorming is open. | When a strategic choice has been made and should be recorded |
| [`competitions/`](competitions/) | External competitions / multi-round programs we enter. Entity-folder per program (`<slug>/`) holding logs, snapshots, forms, correspondence, round results. Distinct from `strategy/` (reusable positioning not bound to one program). | When entering/submitting to a program or logging a round |
| [`decisions/`](decisions/) | One file per architectural or strategic decision. Company-level record — scannable via `git log` + catalog. | After a decision is resolved and commits a direction |
| [`questions/`](questions/) | Lightweight open questions. Promoted to `research-dispatches/` when formalized. | On demand — "add this to questions" |
| [`research-dispatches/`](research-dispatches/) | Formal: hypothesis → prior → findings → recommendation. Re-opens appended as dated `## Update` sections. | When asked to research a specific question |
| [`experiments/`](experiments/) | What we tried, measured, learned. Distinct from benchmarks which hold the spec. | After running an experiment |
| [`benchmarks/`](benchmarks/) | Eval specs — what we measure, how, why. | On explicit ask |
| [`comparisons/`](comparisons/) | Head-to-head competitor / alternative analyses. Carry `decision_status`. | On explicit ask |
| [`sources/`](sources/) | Digested external references — papers, articles, repos, tools. Factual, not opinionated. | **Unprompted** — whenever user drops a new external source |
| [`study-sessions/`](study-sessions/) | Per-source study logs — append-only H2 checkpoints from `/study` sessions. Filename mirrors source exactly. | On explicit ask — `/study <source>` |
| [`concepts/`](concepts/) | Meta-topics spanning multiple sources. One folder per concept: `README.md` (research digest, `type: concept`) + `study-log.md` (`type: study-log`). | On explicit ask — `/study <concept>` |
| [`discovery/`](discovery/) | Customer / prospect calls, VC interviews, pilot feedback. Entity-folder pattern for firms that recur. | After a call or interview |
| [`advisors/`](advisors/) | Academic + advisor outreach: professor profiles, email drafts, collaboration angles, meeting notes. Entity-folder pattern default. | When researching or contacting an advisor |
| [`meetings/`](meetings/) | Verbatim meeting/call records (any counterparty) — digest on top, transcript collapsed below. Load-bearing extracts propagate to `todos/`/`strategy/`/`advisors/`. | Via `/meeting` — whenever a transcript/notes exist |
| [`traction/`](traction/) | Dated metric snapshots — corpus stats, customer pipeline, qualitative signals. | On explicit ask |
| [`finances/`](finances/) | Cash-flow tracking — append-only `ledger.csv` (one row per transaction), redacted statement snapshots, stored receipts, generated summaries. Structured data, not prose. | Via `/finance` (ingest) + `/financial-summary` |
| [`inbox/`](inbox/) | Queue of untriaged drops — URLs, notes, screenshots, topics-to-research. Processed one at a time by `/kb-process-inbox`. | **Unprompted** via `/drop` skill or `kbdrop` CLI |
| [`tools/`](tools/) | Bookmark-class entries — utility URLs, GPTs, reference docs to find/reuse later. Distinct from `sources/` (digest) and `inbox/` (temp). | **Unprompted** — whenever user shares a useful tool/URL |
| [`todos/`](todos/) | Tasks, events, deadlines. Completed items move to `todos/completed/`. | On explicit ask — `/add-todo` |
| [`archive/`](archive/) | Preserved-but-retired content. Never deleted; history is the point. | On explicit ask — `/kb-archive` |
| [`runs/`](runs/) | KB maintenance runs — audits, syntheses, migrations. Also holds `.lock` for single-writer coordination. | By skills themselves (audit, synthesize, etc.) |
| [`schema/`](schema/) | Machine-readable schema + per-type templates. Source of truth for what each file type must contain. | When the schema evolves |
| [`scripts/`](scripts/) | Validation + helper scripts (`kb-lint.py`, `kb-drop.sh`, `install-hooks.sh`). | When tooling evolves |

**`sources/`, `inbox/`, and `tools/` are the only folders written unprompted.** Everything else is write-on-demand.

---

## File naming

Dated files sort chronologically in a flat `ls`:

- Flat file: `<folder>/YYYY-MM-DD-<slug>.md` — lowercase, hyphenated
- Entity folder: `<folder>/<entity-slug>/README.md` + `<YYYY-MM-DD>-<event>.md` dated children — used when the subject is a living thing (competitor, advisor, customer firm) accumulating evidence over time. Promote from flat file → folder when content exceeds ~300 lines OR a second dated event is added.
- Todos use deadline date, not creation date: `todos/YYYY-MM-DD-<slug>.md` (deadline = sortable)
- Inbox drops: `inbox/YYYY-MM-DD-HHMMSS-<slug>.md` (second precision to avoid collisions)

---

## Frontmatter

Every file has YAML frontmatter. Fields, allowed values, and per-type requirements are defined in [`schema/kb-schema.yaml`](schema/kb-schema.yaml) and enforced by `scripts/kb-lint.py` (called by the pre-commit hook).

Common fields across types:

```yaml
---
title: "Short descriptive title"
type: brainstorm | synthesis | benchmark-spec | source | research-dispatch | comparison | experiment | decision | question | strategy | interview | lead | advisor | meeting | todo | event | inbox-drop | traction-snapshot | study-log | concept | tool
product: track-a | track-b | shared   # rename to your tracks in schema/kb-schema.yaml §enums.product
strategic-thread: [oss, gtm, fundraising, partnerships, hiring]   # optional multi-value; customize in schema
source: "URL, conversation date, or origin"
date_found: YYYY-MM-DD
tags: [relevant, topic, tags]
status: raw | reviewed | incorporated | superseded | archived
confidence: high | medium | low | uncertain   # required on synthesis, comparisons, decisions
supersedes: path/to/prior-doc.md              # optional — explicit pointer to the doc this replaces
decision_status: considered | adopted | rejected | borrowed-partial   # comparisons only
---
```

Keep frontmatter synchronized with content. If status or decision changes, update frontmatter in the same edit.

---

## Required body sections

Anti-sycophancy rules stolen from `shannholmberg-llm-wikid` and applied across decision-carrying files:

- **Synthesis** must include `## Counter-arguments` and `## Data gaps`
- **Decisions** must include `## Why` and `## What we're giving up`
- **Comparisons** must include a `## Decision` section that sets `decision_status`
- **Entity-folder README** (competitor, advisor, customer firm) body is **current truth, rewritten as it changes**. Dated sibling files in the same folder form the timeline. No `## Timeline` section in the README — use `ls <folder>/` for chronology.

---

## Study logs — checkpoint + cross-reference rules

`study-sessions/` and `concepts/*/study-log.md` use `type: study-log`. Append-only: each `/study` session adds **one H2 checkpoint at session end** (not mid-session). Newest at the bottom. Checkpoint shape:

- `## Checkpoint — YYYY-MM-DD (session N)`
- **What we covered** — topics touched this session
- **What I now understand** — incremental delta
- **Candidate questions / decisions** — inline `[?question]` / `[?decision]` tags
- **Related sources touched** — wikilinks triggering the cross-ref rule below
- **Open threads → next session** — resume hints

**Tag syntax — `[?question]` and `[?decision]`.** Used inline inside checkpoints to flag candidates. **Never auto-promoted.** Promotion to `questions/` or `decisions/` happens only when the user explicitly asks ("promote the `[?question]` from session 3 to questions/"). The `/study` skill picks up the tagged line and routes to `/add-entry` or `/kb-promote`. Tags are an affordance, not a commitment.

**Bidirectional cross-reference rule.** When a session on Source A meaningfully touches Source B (or concept C):
- A's study file gets the full checkpoint with `[[study-sessions/B]] §checkpoint-N` under "Related sources touched"
- B's study file gets a **short reciprocal checkpoint** — one sentence, pointer back (`from [[study-sessions/A]] §checkpoint-N`), no primary-study progress claimed

Both sides know about the link. `last_checkpoint:` in frontmatter updates on both files.

**Concept promotion is user-prompted.** If a source session keeps revealing cross-cutting themes, `/study` suggests "promote to a concept folder?" — never automatic.

---

## Citation discipline

Three-tier format. Escalate only as needed.

| Tier | Form | Use |
|---|---|---|
| Whole doc | `[[comparisons/YYYY-MM-DD-competitor-slug]]` | Pointing at a doc as one concept |
| Section-precise | `[[comparisons/YYYY-MM-DD-competitor-slug]] §"Decision"` | Default — points at one section |
| Quote-precise | `[[comparisons/YYYY-MM-DD-competitor-slug]] §"Decision" ("verbatim claim here")` | When the reader must read one verbatim claim |

**No line-range citations** (`[[foo#L42-58]]`). They rot silently.

**Self-firing artifacts — section headings only.** Hooks, skill files, scripts, and memory entries fire without a human re-reading the target. Line numbers (`file.md:42`, `file.md:129-141`) rot silently: the artifact keeps pointing at what *used to be* that line. Always cite by section heading (`file.md § "Header"`).

- ✗ `AGENT-GUIDE.md:129-141`
- ✓ `AGENT-GUIDE.md § "Login-walled content"`

Chat-layer narration to the user (Claude pinning a claim during conversation) may still use `file.md:42` — the user verifies immediately, and precision beats rot risk for live reading. The split: who reads the citation, and when.

**Keep H3 subsections ~10-50 lines.** A cited section is only useful if it fits in a reader's context cheaply.

**Cross-project wikilinks** use relative paths:
- `[[../your-product-repo/TECH-DECISIONS]]`
- `[[../your-other-repo/notes/2026-04-10-architecture]]`

Git-backed: when file history is needed, `git log --follow <file>` is authoritative — the semantic `supersedes:` chain and the syntactic git history complement each other.

---

## Growth rules

How the KB expands over time. Followed by skills; violate only with justification.

**Canonical thresholds.** Every numeric rule below references one of these names. Skills, scripts, and hooks cite the **NAME**, not the value — so changing a value here propagates to every enforcer in one edit. Prefer a name over a number anywhere you'd otherwise hardcode a threshold.

```
# Staleness (flagged by /kb-audit)
STALE_DRAFT_DAYS=90                      # status: raw/prospect unchanged beyond → stale
OVERSIZED_FILE_LINES=500                 # hard oversized; reactive (you missed PROMOTE_TO_MULTICHAPTER_LINES)
UNDECIDED_COMPARISON_DAYS=60             # decision_status: considered, no commit → flagged

# Growth / promotion (proactive signals)
PROMOTE_TO_MULTICHAPTER_LINES=300        # single file exceeds → split into multi-chapter
FOLDER_SPLIT_FILE_COUNT=15               # folder exceeds → split into by-<facet>/ subdirs
ANTI_CRAMMING_MAX_MAJOR_SECTIONS=2       # appending one more (3rd) → split to new file instead
ANTI_THINNING_MIN_LINES=30               # file below → fold into existing (description: field already gives it a one-line presence in parent INDEX.md)

# New-folder gate (/kb-add-folder)
NEW_FOLDER_MIN_FILES=3                   # minimum files that fit the new category
NEW_FOLDER_INDEX_MAX_LINES=25            # INDEX.md size ceiling (proves the category is tight)

# Archiving (/kb-archive)
ARCHIVE_UNCITED_MONTHS=3                 # superseded + uncited for this long → eligible
```

**Adding a new folder** — only if ALL:
1. At least `NEW_FOLDER_MIN_FILES` files fit the category
2. They don't fit existing folders
3. There is a clear *structural* difference (not just a topic; topics live in tags)
4. You can write its `INDEX.md` within `NEW_FOLDER_INDEX_MAX_LINES` lines without hand-waving

Use `/kb-add-folder` to force the justification + creation of `<newfolder>/README.md` with `type: folder` frontmatter. The generator picks up the new folder on the next run.

**Promoting a file to a multi-chapter subdirectory** — when a single file exceeds `PROMOTE_TO_MULTICHAPTER_LINES` AND has a natural progression. Start flat; promote when the signal appears. Use a `comparisons/YYYY-MM-DD-competitor-slug/` directory with `README.md` as the entry point and per-chapter sibling files.

**Splitting a folder into sub-taxonomy** — more than `FOLDER_SPLIT_FILE_COUNT` files with 2-3 natural clusters. Use `<folder>/by-<facet>/` subdirectories; don't refactor frontmatter.

**Archiving** — move to `archive/` when fully superseded AND uncited for `ARCHIVE_UNCITED_MONTHS` months AND no active decision references it. Moving the file automatically removes its listing from the source folder's INDEX.md (regenerator skips files in `archive/`). Never delete.

**Resolution stamps (partial supersede)** — when new content answers an *open thread inside* an otherwise-live doc, do NOT supersede, archive, or rewrite the whole doc. Supersede is whole-file replacement (`supersedes:` frontmatter, a successor file); a resolution stamp closes *one question* inside a file that's still current. This is the lightweight sibling of supersede, and the common case — a new entry often settles a thread recorded elsewhere without invalidating the host doc.
- **Format:** `**Resolved YYYY-MM-DD → [[resolver-file]]:** <one line on what was settled>`, placed at the *head* of the resolved bullet/section. Leave the original question text below it — don't delete it; the open thread is part of the history, the stamp just caps it.
- **Pairs with the open-thread vocabulary:** a stamp closes a `## Open threads` bullet, a `[?question]` / `[?decision]` tag (`/study`), or any line phrased as an unresolved question. Reuse those markers so threads stay greppable.
- **Bidirectional:** the resolving doc links back to the doc it resolved (a `## Related` wikilink is enough). Both sides know about the link, same as supersede.
- **Trigger:** any write that settles a question recorded elsewhere — most often mid-`/add-entry` or `/meeting`, when the new entry happens to answer an older thread. The skills prompt for it; the obligation holds for any write, skill or hand edit.
- **Mechanics:** it's a hand edit, no skill of its own. No `supersedes:`/`superseded_by:` frontmatter (that's whole-file), no archive (the host doc stays live). Do it inside the same lock + commit session as the content that triggered it.

**Anti-cramming** — if appending a new major section would push the doc past `ANTI_CRAMMING_MAX_MAJOR_SECTIONS`, consider splitting into a new file first.

**Anti-thinning** — file below `ANTI_THINNING_MIN_LINES` lines that isn't a glossary/source entry? Fold into an existing file. The file's `description:` frontmatter already gives it one-line presence in the parent folder's auto-generated INDEX.md; a whole file for one sentence is wasteful.

**Promotion path** — `questions/` (lightweight) → `research-dispatches/` (formalized) → `decisions/` (company-level resolution) → `synthesis/` (rolled up). `/kb-promote` handles the backlinks.

**Audit flags** (`/kb-audit` surfaces, doesn't fix):
- Raw drafts unchanged for more than `STALE_DRAFT_DAYS` days.
- Files exceeding `OVERSIZED_FILE_LINES` lines.
- Comparisons at `decision_status: considered` with no commit in the last `UNDECIDED_COMPARISON_DAYS` days.

---

## Single-writer rule

**Only one agent performs KB writes at a time.** Any write OR Chrome-extension operation (treated as a write because it consumes the single Chrome session) touches a lock file `runs/.lock` with session ID + timestamp. Other agents check the lock before starting; either wait or abort with "another agent is writing, retry later."

Manual override: `rm runs/.lock` if a previous session died.

All write-capable skills enforce this as their first/last step. You don't have to think about it.

**LinkedIn / X ingestion** is login-walled — WebFetch cannot see it. Use the Chrome extension via `mcp__claude-in-chrome__*`. Subject to the single-writer rule.

---

## Commit convention

One commit per atomic change, not one per session. Use conventional-commit-style prefixes that make `git log --oneline` scannable.

| Prefix | For | Example |
|---|---|---|
| `source:` | New external reference | `source: add 2026-04-17-paper-slug` |
| `comparison:` | Competitor analysis | `comparison: add 2026-04-17-competitor-slug` |
| `decision:` | Architectural / strategic decision | `decision: add 2026-04-17-gemini-2-5-flash-as-default` |
| `experiment:` | Experiment log | `experiment: log 2026-04-17-corpus-run` |
| `synthesis:` | Snapshot | `synthesis: snapshot enterprise @ 2026-04-17` |
| `brainstorm:` | Thought-process writeup | `brainstorm: add 2026-04-17-pricing-tiers` |
| `strategy:` | Crystallized strategy entry | `strategy: add 2026-04-17-oss-positioning` |
| `interview:` / `discovery:` | Customer/prospect call | `interview: add 2026-04-17-acme-capital-partner-call` |
| `lead:` | Pre-call prospect event (signup, outreach sent/received) | `lead: add 2026-04-21-prospect-signup` / `lead: contacted 2026-04-23-prospect-slug` |
| `advisor:` | Advisor profile / event | `advisor: contact 2026-04-17-doan-email-sent` |
| `meeting:` | Meeting/call record (+ its propagated extracts) | `meeting: add 2026-04-17-example-advisor-pricing` |
| `question:` | Open question | `question: add 2026-04-17-embedding-model` / `question: promote 2026-04-17-embedding-model → research-dispatches/` |
| `research:` | Research dispatch | `research: add 2026-04-17-entity-matching-enterprise` |
| `inbox:` | Drop or process | `inbox: drop 2026-04-17-090234-linkedin-post` / `inbox: process 2026-04-17-090234 → sources/2026-04-17-paper-slug` |
| `tool:` | New tool/bookmark | `tool: add 2026-04-27-svgl` |
| `todo:` | Todo/event | `todo: add 2026-04-20-email-advisor` / `todo: complete 2026-04-17-customer-intro` |
| `finance:` | Ledger ingest or summary | `finance: log 2026-05-30 Example SaaS $40 (saas)` / `finance: reconcile 2026-05` / `finance: summary 2026-05` |
| `archive:` | Archived file | `archive: 2026-04-10-old-brainstorm` |
| `study:` | Study log checkpoint append, new concept folder, or study-system seed | `study: checkpoint paper-slug session 1` / `study: add concepts/example-concept` |
| `index:` | Regeneration of auto-generated INDEX.md files | `index: regenerate after description edits` |
| `conventions:` | Rulebook edit | `conventions: add growth rules section` |
| `schema:` | Schema edit | `schema: add advisor type` |
| `skill:` | Skill edit | `skill: update add-entry to use schema templates` |
| `kb:` | Structural / meta change | `kb: rename ideas/ → project-kb/` |

**When to commit:**
- After each new entry (each source, comparison, decision, interview, advisor event, etc.)
- After each inbox drop (`inbox: drop`), and again when processed (`inbox: process`)
- After each synthesis snapshot
- After each description-only edit that regenerates INDEX.md files
- After each CONVENTIONS / AGENT-GUIDE / GLOSSARY edit
- After each skill edit
- After each schema change
- After each structural move (archive, promotion, rename)

**Always `git push` after every commit.** No local-only buffering. Skills handle stage → commit → push as a unit.

All commits end with:
```
Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

---

## What NOT to do

- Don't write opinionated takes inside `sources/` files (opinions go to brainstorming or comparisons).
- Don't write synthesis / benchmark / comparison / dispatch / experiment / decision / strategy / advisor / discovery files without being asked. These are explicit milestones, not running commentary.
- Don't create dated "session" subfolders. Flat-date naming is the structure, except the multi-chapter exception for entities.
- Don't delete or overwrite old files when superseding. Mark stale in catalog, write a new dated file, set `supersedes:`. History is the point.
- Don't supersede, archive, or rewrite a whole doc when only one thread *inside* it got resolved — use an inline **resolution stamp** (see §"Growth rules" → "Resolution stamps"). And don't leave the thread silently resolved either: stamp it so the next reader doesn't re-litigate a settled question.
- Don't duplicate content that lives authoritatively in a sibling repo (your product code, an ops repo, a separate research repo). Cite out.
- Don't bypass the single-writer lock.
- Don't skip the pre-commit lint.
- Don't batch commits. One logical change per commit; push after each.
