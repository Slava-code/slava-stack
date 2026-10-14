---
name: study-status
description: "Read-only: where we left off studying a source or concept (latest checkpoint, open threads). Use when the user asks: where were we on X, what have we studied about Y."
---

# /study-status — Read-only study-log resume query

Compact summary of where a source or concept study log currently stands. Read-only — no lock, no writes, no session created.

## Arguments

- **`/study-status <source-slug>`** — source study log (looks up `study-sessions/*-<arg>-*.md`)
- **`/study-status <concept-slug>`** — concept study log (looks up `concepts/<arg>/study-log.md`)

Fuzzy-match on slug-contains / tag-match / title-keyword if the exact match fails.

## Flow

1. **Resolve target.** Same resolution order as `/study` (source filename → concept folder → fuzzy). If ambiguous, list candidates and stop (don't pick).
2. **If no study log exists** → report: "never studied. Last touch via [[brainstorming/<matching-brainstorm>]] if one exists, else none." For concepts, report the folder doesn't exist.
3. **If study log exists** → parse frontmatter + body. Extract:
   - `last_checkpoint:` date
   - Count of `## Checkpoint — ` headers (the session count)
   - Latest checkpoint's `**Open threads → next session**` bullets
   - Latest checkpoint's `**Open threads**` content as-is (those ARE the resume hints)
   - Last 3 bullets from the latest checkpoint's `**What we covered**` section (for recent-context recall)
   - Any `[?question]` / `[?decision]` tags still open in the latest checkpoint
4. **Render compact output:**

```
## Study log — <source or concept name>

Studied <N> session(s); last checkpoint <date>.

**Where we left off:**
- <open threads bullets>

**Recent context (last 3 from "What we covered"):**
- <bullet>
- <bullet>
- <bullet>

**Open candidate flags:**
- [?question] <text>
- [?decision] <text>

To continue: `/study <slug>`
```

If caller is `/study` in resume mode, return this block as-is for use as session preamble.

## Voice mode stub

`--mode voice`: same retrieval, renderer drops markdown, phrases wikilinks naturally, prefers "last session we covered..." narration over bullet dumps.

## What `/study-status` is NOT

- **Not `/study`.** Does not start a session.
- **Not `/study-unstudied`.** Answers "where are we on X?" not "what haven't we touched?"
- **Not a diff of checkpoints.** Shows latest only. For history, read the study-log file directly or `git log`.
