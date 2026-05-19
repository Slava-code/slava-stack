---
name: study-unstudied
description: "List project-kb sources and concepts that haven't been studied yet (no matching study-sessions/ file, or empty concept study-log). Live grep — no persisted queue file. Ranked by convergence-tag priority: sources in high-convergence clusters surface first. Use when: user asks 'what haven't we studied?', 'what's the queue?', 'what should I study next?', 'what sources/concepts are outstanding?'. Do NOT use to start a session (use /study). Do NOT use to check progress on a specific source (use /study-status)."
---

# /study-unstudied — What hasn't been studied yet

Live query over `sources/` + `concepts/` + `study-sessions/`. No persisted queue — regenerated on every invocation so state is always accurate.

## Flow

1. **Enumerate sources.** List every `sources/YYYY-MM-DD-*.md` file (exclude README.md, INDEX.md).
2. **Enumerate concepts.** List every `concepts/<slug>/` subfolder with a `README.md`.
3. **For each source** — check if `study-sessions/<source-filename>.md` exists. If not → **unstudied source**.
4. **For each concept** — check if `concepts/<slug>/study-log.md` exists AND has at least one `## Checkpoint — ` header. If not → **unstudied concept**.
5. **Score + rank unstudied items:**
   - Read each unstudied source's matching brainstorm from `brainstorming/` (filename pattern `*<source-slug>*`)
   - Count convergence-tag membership (from brainstorm frontmatter `convergence:` list) — higher count = more leverage
   - Sources in clusters of 3+ brainstorms (per `scripts/kb-convergence-scan.py` threshold) rank first
   - Concepts rank by number of referenced KB signals in their `README.md`
6. **Render:**

```
## Unstudied

### Sources (<N>)

**High-leverage cluster: <cluster-tag>** (<N> brainstorms converge here)
- [[sources/YYYY-MM-DD-<slug>]] — <short description>
- ...

**Other unstudied:**
- [[sources/...]] — ...

### Concepts (<N>)
- [[concepts/<slug>]] — <description>
- ...
```

Keep the list scannable. Full `/study-status` output belongs in that skill — here, one line per item.

## Voice mode stub

`--mode voice`: same query, renderer narrates "you have 23 unstudied sources, most clustered around <top-cluster> — top three are <X>, <Y>, <Z>. Want to start with one of those?"

## What `/study-unstudied` is NOT

- **Not a writeable queue.** If you want to pin specific sources for later, add them to `todos/` via `/add-todo`.
- **Not a ranking of importance.** Convergence-tag count is a proxy for *leverage*, not intrinsic value — a standalone source can still be worth studying.
- **Not a replacement for `/kb-audit`.** That skill flags stale/broken things; this one flags unstudied ones.
