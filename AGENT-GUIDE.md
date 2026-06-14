# Agent Guide — T1 Routing

How an LLM agent finds its way through this KB. Read after [`CLAUDE.md`](CLAUDE.md), before taking any KB-related action. Does not restate rules — those live in [`CONVENTIONS.md`](CONVENTIONS.md). This is the routing table.

---

## Boot order

| Tier | File(s) | When to load |
|---|---|---|
| T0 | `CLAUDE.md` | Always (auto-loaded when Claude sees the dir) |
| T1 | root `INDEX.md`, `GLOSSARY.md` | First KB-touching query in a session |
| T2 | this file, `CONVENTIONS.md`, relevant `<folder>/README.md` + `INDEX.md` | Before editing content in that folder |
| T2 | `CONVENTIONS.md`, relevant `<folder>/INDEX.md` | Before any write / edit |
| T3 | specific content files | When cited, queried, or referenced |

If you find yourself guessing a rule, you're skipping T2 — stop and read `CONVENTIONS.md`.

---

## Where does this piece of content go?

| User brings... | Destination |
|---|---|
| A URL, paper, repo, tool | `sources/YYYY-MM-DD-<slug>.md` — factual digest |
| A URL you haven't analyzed yet | `inbox/YYYY-MM-DD-HHMMSS-<slug>.md` via `/drop` |
| A useful tool/URL/GPT/reference doc to find again later (not a source to digest) | `tools/YYYY-MM-DD-<slug>.md` |
| A competitor analysis | `comparisons/YYYY-MM-DD-<slug>.md` (flat) or `comparisons/YYYY-MM-DD-<slug>/` (multi-chapter if >300 lines) |
| A design/strategy discussion to save | `brainstorming/YYYY-MM-DD-<slug>.md` |
| A crystallized GTM/positioning/pricing/fundraising choice | `strategy/YYYY-MM-DD-<slug>.md` |
| Investor blurb, pitch-application copy, elevator pitch, positioning messaging | `strategy/YYYY-MM-DD-<slug>.md` |
| A submission/log/snapshot/form/organizer email for a multi-round competition or program | `competitions/<program-slug>/YYYY-MM-DD-<slug>.md` (entity folder; hub `README.md`). One-shot applications with no rounds can stay in `strategy/`. |
| A single architectural or strategic decision | `decisions/YYYY-MM-DD-<slug>.md` |
| An open question (lightweight, pre-formal) | `questions/YYYY-MM-DD-<slug>.md` |
| A formalized research question (hypothesis → findings) | `research-dispatches/YYYY-MM-DD-<slug>.md` |
| A measured experiment result | `experiments/YYYY-MM-DD-<slug>.md` |
| A benchmark spec | `benchmarks/YYYY-MM-DD-<slug>.md` |
| An architecture snapshot for a product | `synthesis/YYYY-MM-DD-<product>-architecture.md` |
| A customer / prospect / stakeholder call | `discovery/<firm-slug>/<YYYY-MM-DD>-<call>.md` (folder default) |
| A meeting/call transcript to save (any counterparty) | `meetings/YYYY-MM-DD-<counterparty>-<topic>.md` via `/meeting` — digest + collapsed transcript; extracts propagate to `todos/`/`strategy/`/`advisors/`. A customer call can ALSO get a `discovery/` interview digest that links here. |
| Advisor outreach, professor profile, email drafts | `advisors/<person-slug>/<README or dated event>.md` |
| Team member profile or notes | `team/<person-slug>/<README or dated note>.md` |
| A task/event with a deadline | `todos/YYYY-MM-DD-<slug>.md` (date = deadline) |
| A metric snapshot / traction update | `traction/YYYY-MM-DD-<scope>.md` |
| A spend/payment/income, a receipt, or a bank statement | `finances/ledger.csv` (one row) via `/finance` — receipts → `finances/receipts/`, redacted statements → `finances/statements/`. NOT one md file per transaction. |
| Deep-study session on an existing source | `study-sessions/<source-filename>.md` (filename mirrors source exactly; append-only H2 checkpoints) — written by `/study` |
| Deep-study session on a cross-cutting concept | `concepts/<concept-slug>/` folder with `README.md` (type: concept, research digest) + `study-log.md` (type: study-log, checkpoints) — written by `/study` |
| New content resolves an open thread in an *existing* doc | NOT a new file and NOT a supersede — an inline **resolution stamp** on that doc. See CONVENTIONS §"Growth rules" → "Resolution stamps". Do it in the same lock/commit session as the content that triggered it. |

If the content type is unclear, drop it to `inbox/` via `/drop` and classify later.

**Source vs tool:** if the URL has facts you'd cite (architecture, customer count, benchmark numbers), it's a `source/`. If it's a utility you'd just use again (an icon library, a GPT, a PDF signer), it's a `tools/`.

---

## Drop vs add-entry — which door?

The routing table tells you *what folder*. This tells you *which skill*.

| Situation | Use |
|---|---|
| You've already read / analyzed the content in this conversation | `/add-entry` — classification is not deferred, you know what it is |
| User gave you a URL you haven't opened; they're queuing it for later | `/drop` |
| User said "save this for later" / "I want to come back to this" | `/drop` |
| Content type is genuinely unclear after reading | `/drop`, let `/kb-process-inbox` classify |

**Default bias:** if you just did the work of analyzing something in the chat, skip inbox. Inbox is for *unread* material. Reaching for `/drop` after analysis is the low-friction trap — it looks cheap, but it hides finished work behind a deferred-processing queue.

---

## Source + brainstorm pair

When an external source (article, tweet, repo, op-ed) triggers immediate implications work for your project, produce **two files in the same session**:

- `sources/YYYY-MM-DD-<slug>.md` — factual digest. What the source says, what the tool does, what data it presents. Neutral, quotable, citable.
- `brainstorming/YYYY-MM-DD-<slug>-implications.md` (or `-vs-ours`) — our take. Where it fits, where it conflicts, what questions it opens. Cites the source file.

They reference each other. The source is the fact; the brainstorm is the analysis. Keeping them separate means future readers can cite the fact without dragging in our opinion, and update the opinion without rewriting the fact.

Canonical example: `[[sources/YYYY-MM-DD-paper-slug]] + [[brainstorming/YYYY-MM-DD-paper-slug-implications]]` — same date, sibling slugs, cross-linked.

If the brainstorm surfaces a sharp, researchable question, that question can graduate to `questions/` or `research-dispatches/` via `/kb-promote`.

---

## Common queries ("where do I look to answer X?")

| User asks... | Primary file / folder |
|---|---|
| "What's our current architecture?" | Most recent `synthesis/` file for the `product:` asked about |
| "What's our positioning?" | `comparisons/2026-03-17-competitive-landscape.md` + most recent `strategy/*positioning*` |
| "Why did we choose X?" | Search `decisions/` by slug; fall back to `git log --all --full-history --grep='<keyword>'` |
| "What's open right now?" | `questions/` + `research-dispatches/` with `status: raw` or `reviewed`; also `todos/` with `status: pending` |
| "Who are the competitors?" | `comparisons/INDEX.md` — one-liner per competitor; open the files whose description_status matters |
| "Who are the advisors?" | `advisors/INDEX.md` then folders per advisor |
| "What did we discuss in the meeting with X?" | `meetings/INDEX.md` — one-liner per meeting; open the file for digest + transcript |
| "What's in the inbox?" | `inbox/` directory listing; run `/kb-process-inbox` to drain |
| "What's due today?" | `/deadlines` (reads only frontmatter via subagent) |
| "What are we giving up by choosing X?" | Each `decisions/*.md` has a required `## What we're giving up` section |
| "What have we tried and measured?" | `experiments/` |
| "Where did we leave off on X?" | `/study-status <source-or-concept>` — read-only summary of latest checkpoint + open threads |
| "What sources/concepts haven't we studied?" | `/study-unstudied` — live grep, ranked by convergence-tag priority |
| "Walk me through paper X" / "Study concept Y" | `/study <source-or-concept>` — starts or resumes a session |

---

## Skills — when to invoke which

All skills live at `.claude/skills/` inside this repo. Activated when Claude is run from the KB directory. If unsure which skill to run, invoke `/kb` (index / chooser).

| Skill | Use when |
|---|---|
| `/kb` | Unsure which skill fits. Lists every KB skill with one-line purpose. |
| `/add-entry` | Adding any content type (source, comparison, decision, etc.). Classifies, copies template, fills frontmatter, commits, pushes. |
| `/drop` | Quick-capture to inbox. Content or URL; no classification. |
| `/kb-process-inbox` | Drain the inbox queue. Each drop handled by a fresh subagent. |
| `/kb-audit` | Freshness + consistency check. Broken citations, stale `raw` statuses, oversized files, etc. Writes report to `runs/`. |
| `/kb-synthesize <product>` | Roll up a new architecture snapshot for one of the configured product tracks (e.g. `track-a`, `track-b`, `shared`). |
| `/kb-archive <path>` | Move a fully-superseded file to `archive/`. |
| `/kb-add-folder` | Add a new top-level folder. Forces justification against CONVENTIONS growth rules. |
| `/kb-promote <path>` | Move content along the promotion path (question → dispatch → decision → synthesis). Handles backlinks. |
| `/add-todo` | Add a todo / event / meeting with deadline. |
| `/meeting` | Save a meeting/call transcript → `meetings/` (digest + collapsed transcript), then extract action items / strategy insights / contacts / shared artifacts and propagate them to `todos/`/`strategy/`/`advisors/`/`raw/` — confirming each before writing. |
| `/finance` | Ingest a transaction into `finances/ledger.csv`. Verbal / receipt / statement. Parses, categorizes, dedup + reconciles, confirms everything, appends/enriches, redacts statements, commits + pushes. |
| `/financial-summary <period>` | Generate a persisted, formatted cash-flow summary for a month/quarter/range → `finances/summaries/`. One-off lookups need no skill — read the ledger and answer in chat. |
| `/complete-todo <slug>` | Mark a todo complete. Moves to `todos/completed/`, auto-appends one-line entry to each `related:` entity's timeline. |
| `/deadlines` | List today-due + overdue pending. Subagent reads frontmatter only. User-invoked. Agent may auto-invoke if relevant to the task. |
| `/write-as <instruction>` | Draft text in the active user's voice (email, X post, LinkedIn, strategy note). Resolves active user via SOUL.md, loads `team/<slug>/voice/style-card.md`, stitches register-matched reverse-prompt pairs, produces a single draft. Read-only. Agent auto-invokes when user says "draft this as me" / "write [X] in my voice" / "reply to this email for me". |
| `/study <source|concept|next>` | Start or resume a deep-study session. Appends one H2 checkpoint at session end to `study-sessions/<source-filename>.md` or `concepts/<slug>/study-log.md`. Bidirectional cross-refs. `--mode text|voice`. Promotion of `[?question]` / `[?decision]` tags is user-prompted only. |
| `/study-status <source|concept>` | Read-only resume query — latest checkpoint date, next-session intent, open threads, recent context. No lock, no session. |
| `/study-unstudied` | Live grep: sources without study-logs + empty concept logs. Ranked by brainstorm convergence-tag priority. No persisted queue. |

---

## Single-writer rule

**Only one agent writes to the KB at a time.** Any write OR Chrome-extension operation respects `runs/.lock`.

Before a write:
1. Check `runs/.lock` existence
2. If absent, touch it with `<session-id> <ISO-timestamp>`
3. Perform the write operation
4. Remove the lock on completion (success or failure)

If the lock is present, abort with "another agent is writing, retry later." Manual override: `rm runs/.lock` when you're confident no agent is active.

Skills enforce this automatically. Don't bypass.

---

## Special fetchers

WebFetch is the default URL fetcher, but several hostnames need a dedicated tool to get past abstract-page-only or login-walled views. The digesting subagent (in `/kb-process-inbox` or `/add-entry`) is **required** to call the matching fetcher before writing the source entry, and to cite `runs/fetches/<slug>.txt` in the entry's `## Fetched from` section so future readers can verify provenance.

| Hostname pattern | Fetcher | Subject to lock? | What you get |
|---|---|---|---|
| `linkedin.com`, `x.com`, `twitter.com` | Chrome extension via `mcp__claude-in-chrome__*` | **yes** (single Chrome session) | rendered post text + author handle + thread context |
| `youtube.com`, `youtu.be` | `scripts/yt-fetch.sh <url> --out runs/fetches/<slug>.txt` | no | metadata + auto/manual transcript |
| `arxiv.org` | `scripts/arxiv-fetch.sh <url-or-id> --out runs/fetches/<slug>.txt` | no | abstract-page metadata + full PDF text (`pdftotext -layout`) |
| `github.com` | `scripts/github-deep-fetch.sh <url-or-owner/repo> --out runs/fetches/<slug>.txt` (pass 1) + targeted `gh api` reads (pass 2) | no | repo metadata + README + tree + manifests; pass 2 reads code |
| (other) | WebFetch | no | rendered HTML |

**Provenance rule:** every source entry created from one of these fetchers must include in its body:

```markdown
## Fetched from

- `runs/fetches/2026-04-27-<slug>.txt` — raw output of `scripts/<fetcher>.sh` against `<url>` on `<date>`
```

This kills the historical "HTML capture" ambiguity — readers can open the raw fetch and verify what was available to the digester.

### Chrome extension (login-walled content)

Treat any Chrome operation as a write. **Never run two Chrome tasks in parallel** — the extension is a single-session resource. Flow:

1. User drops the URL via `/drop`
2. `/kb-process-inbox` picks it up
3. Subagent acquires `runs/.lock`
4. Subagent uses Chrome extension to open the post, capture content
5. Subagent writes `sources/YYYY-MM-DD-<slug>.md`, commits, pushes
6. Subagent releases lock, deletes inbox drop

### `scripts/yt-fetch.sh` — YouTube

Wraps `yt-dlp`. Auto-captions are ASR — punctuation rough, occasional misheard words. Fine for "what's the gist + key claims"; not suitable for verbatim quoting. Source entry should mark `transcript: auto-generated` (or `manual`) in the body. When no captions exist, the script emits `TRANSCRIPT_SOURCE: none` and the digester writes a stub source with a TODO to watch manually.

### `scripts/arxiv-fetch.sh` — arxiv

Downloads the PDF + parses the abstract page for citation metadata. `pdftotext -layout` preserves tables roughly but mangles math equations and drops figures. For papers where equations or visuals carry the argument, supplement with the abstract page or HTML version. Output header includes both the abstract and the full paper text — the digester should cite specific equations/sections by name (`Eq. 14`, `§ 3.2`, `Table 1 row 4`) when claims hinge on them.

### `scripts/github-deep-fetch.sh` — GitHub (two-pass)

A README is not a repo. Two-pass design:

**Pass 1 (mechanical, this script):** repo metadata, README, file tree (top 200), common manifest files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.). Always run.

**Pass 2 (judgment-driven, the digesting subagent):** read pass-1 output, identify 2–5 high-signal files based on README hints + tree structure, fetch each via:

```bash
gh api repos/<OWNER>/<REPO>/contents/<path> --jq '.content' | tr -d '\n' | base64 -d
```

**Hard caps:** 5 files OR 2000 total lines, whichever first. Heuristics encoded at the bottom of every pass-1 output:
- README-named paths first ("core logic in `src/X.py`")
- For libraries: entry point named in the manifest
- For agents/RAG/eval projects: `src/agents`, `src/eval`, `benchmarks/`, `evals/`
- For ML papers' code: `src/model.py`, `train.py`, `configs/`, `scripts/eval.py`
- Skip: `tests/`, `examples/`, `docs/`, `.github/`, vendored deps

---

## Commit convention (the short version)

Every commit uses a folder-or-type prefix: `<prefix>: <verb> <slug>`.

See `CONVENTIONS.md` §"Commit convention" for the full table. Skills handle stage → commit → push automatically with the right prefix. Always push after every commit — no local-only buffering.

---

## What this file is NOT

- Not the rulebook — see [`CONVENTIONS.md`](CONVENTIONS.md).
- Not the index — see root [`INDEX.md`](INDEX.md) and per-folder `INDEX.md` files.
- Not the glossary — see [`GLOSSARY.md`](GLOSSARY.md).
- Not a user manual for humans — see [`USER-MANUAL.md`](USER-MANUAL.md).

This file is a routing table. If adding content here would duplicate a rule from CONVENTIONS, cite out instead.
