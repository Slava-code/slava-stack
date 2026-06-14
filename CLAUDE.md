# project-kb — Agent Entry (T0)

A closed-loop, AI-native knowledge base for running a startup. Holds research, decisions, brainstorms, experiments, competitor analyses, customer interviews, advisor outreach, strategy, GTM, fundraising, cash-flow tracking — anything the team needs to reason about together.

Git-backed. Version history is authoritative for "when did we X" — see `git log --follow <file>`.

## Progressive boot — read on demand

| Tier | Read when |
|---|---|
| **T0** (this file) | Always loaded when Claude sees the dir |
| **T1** [`INDEX.md`](INDEX.md), [`GLOSSARY.md`](GLOSSARY.md) | First KB-touching query in the session |
| **T2** [`CONVENTIONS.md`](CONVENTIONS.md), [`AGENT-GUIDE.md`](AGENT-GUIDE.md), relevant `<folder>/README.md` + `<folder>/INDEX.md` | Before adding/editing content in that folder |
| **T3** Specific content files | When cited, queried, or processed |

Root `INDEX.md` is auto-generated — a one-liner per top-level folder. Each folder has its own `README.md` (hand-authored rules + purpose) and `INDEX.md` (auto-generated listing of direct children, built from each file's `description:` frontmatter).

Humans: read [`USER-MANUAL.md`](USER-MANUAL.md) for a practical quickstart. Persona-specific reading paths in [`READING-GUIDES.md`](READING-GUIDES.md). Scope boundaries in [`LIMITS.md`](LIMITS.md).

**Optional conversational tone — only if `SOUL.md` exists at the repo root:** read it immediately, before responding to the user. Gitignored, personal. Only affects how you TALK to the user — not how you write documents. Subagents don't load it. If the file is absent, skip — this is an opt-in personality layer, not a required boot step.

**Optional active-user preferences — only if `SOUL.md` declares an active user:** `SOUL.md` may declare an active user slug (e.g. `Active user: founder-template`). If present, read `team/<slug>/preferences.md` for working preferences. They apply to any write the main agent performs. Skip if SOUL.md is absent or has no active-user line. Subagents don't load this.

## If user asks anything KB-related

- **Unsure which skill to run** — invoke `/kb` (skill chooser / index)
- **Add content to the KB** — `/add-entry` (picks folder, copies template, fills frontmatter, commits, pushes)
- **Drop something to process later** — `/drop <content-or-url>` (queues to `inbox/`). Shell alias from terminal: `kbdrop <url-or-text>` if installed — same effect, no Claude Code session needed.
- **Process the inbox queue** — `/kb-process-inbox` (each drop handled by a fresh subagent)
- **Save a meeting/call transcript (+ propagate its contents)** — `/meeting` (writes `meetings/` digest + collapsed transcript, then fans action items → `todos/`, insights → `strategy/`, contacts → `advisors/`, artifacts → `raw/`; confirms each before writing)
- **Add a todo/event with deadline** — `/add-todo`
- **Complete a todo** — `/complete-todo <slug>` (auto-merges related-entity timeline entry)
- **Check deadlines** — `/deadlines` (user-invoked; agent may invoke if relevant to task)
- **Log a transaction / spend / payment / receipt / bank statement** — `/finance` (appends to `finances/ledger.csv`; parses verbal note, receipt image, or statement; dedup + reconcile; confirms before writing)
- **Summarize cash flow for a period** — `/financial-summary <period>` (persisted breakdown → `finances/summaries/`; one-off lookups just ask, no skill)
- **Audit the KB** (freshness, broken citations, stale drafts) — `/kb-audit`
- **Roll up a synthesis** — `/kb-synthesize <track>`
- **Archive a file** — `/kb-archive <path>`
- **Add a new folder** — `/kb-add-folder` (enforces CONVENTIONS growth rules)
- **Promote content along the path** (question → dispatch → decision → synthesis) — `/kb-promote`
- **Start or resume a study session on a source or concept** — `/study <source|concept|next>` (appends one H2 checkpoint at session end; bidirectional cross-refs when touching other sources; `--mode text|voice`)
- **Check where we left off on a source or concept** — `/study-status <source|concept>` (read-only; no session started)
- **List what hasn't been studied yet** — `/study-unstudied` (live grep, ranked by convergence-tag priority)

If the optional voice plugin is installed (`plugins/voice/`):

- **Draft text in the active user's voice** (email, X post, LinkedIn, strategy note) — `/write-as` (loads `team/<active-user-slug>/voice/style-card.md` and stitches register-matched reverse-prompt pairs)

## KB-first for named-entity queries

If a user names a person, company, tool, or concept ("what does X do?", "tell me about Y", "what's Z working on?"), treat it as a KB-touching query: read relevant `<folder>/INDEX.md` files (one-liner descriptions) and grep BEFORE going to the web. The KB is small and may already have a reviewed entry.

Web-in-parallel is fine. But if the KB has the thing, the KB wins — it's the opinionated, reviewed version, and the web answer should be used to *extend* it (new angles, updates), not replace it.

**Unknown term — grep first, then ask.** If the user names something you don't recognize at all (tool, codename, person, internal shorthand), grep the KB *before* falling back to "what did you mean?" — the KB very often has the digest already. If grep turns up nothing either, *then* ask the user. Do not substitute a similarly-named tool (e.g. "OpenClaw" → "OpenHands") — guesses anchor wrong and waste a turn.

## Commit + push together (no local-only buffering)

**Every `git commit` on this repo is followed immediately by `git push` to origin.** Not at session end, not after a batch — right after each commit. The post-commit hook enforces this automatically; if it reports a push failure, fix it before continuing, don't let unpushed commits accumulate.

Full rule: `CONVENTIONS.md` §"Commit convention". This also applies when you chain commits from a single tool call — each must push.

## Single-writer rule

Only one agent performs KB writes at a time. Any write OR Chrome-extension operation respects `runs/.lock`. Skills handle this — don't bypass.

## Inference discipline (applies to every agent, not just writes)

When narrating KB content to the user, report what sources SAY, not what they IMPLY. The KB is small, the temptation to "round up" a sparse fact into a vivid narrative is real, and inflated claims about third parties (customers, advisors, competitors) are the most dangerous kind because they leak into pitches and outreach.

- **Preserve hedges.** `e.g.`, `possible`, `target`, `exploring`, `customer discovery` are load-bearing. Don't drop them in retellings.
- **Who is the actor of a claim?** A timeline-row dependency describes *us*, not the counterparty. "We need demo fixes before pilot Y" ≠ "Y is waiting for demo fixes."
- **Cite when it matters.** `file.md:42` beats a confident paraphrase. If the user might act on what you say, pin it to a line.
- **When unsure, quote.** A short quote + pointer beats a summary that inflates the original.
- **Absence ≠ denial.** If the KB is silent on something, say "the KB doesn't say," not a confident inference.

This is the chat-layer analog of CONVENTIONS §counter-arguments / data-gaps: don't narrate past the evidence.

## Rules you must not invent

All conventions (frontmatter, citations, file naming, folder purpose, commit format, growth rules, single-writer rule) live in [`CONVENTIONS.md`](CONVENTIONS.md). Do not guess — read the rulebook when touching content.

Routing ("where does this specific thing go?") lives in [`AGENT-GUIDE.md`](AGENT-GUIDE.md).
