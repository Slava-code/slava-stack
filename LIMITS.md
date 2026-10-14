# Limits — What this KB deliberately does not capture

The scope of this KB is strategic and cross-cutting artifacts for the project — research, decisions, brainstorms, etc. This file lists what it deliberately does NOT try to capture, so neither a human nor an agent tries to stuff the wrong thing in here.

---

## Out of scope

- **Line-by-line code or implementation detail.** Those live in your product source trees (e.g. `../your-product-repo/`). This KB references, it doesn't duplicate.
- **Real-time metrics dashboards.** Traction snapshots are *dated point-in-time records*; live metrics belong in Grafana / Linear / whatever runtime tool you use.
- **Recordings, screenshots and multi-MB binaries.** Don't commit them. (Text transcripts and raw artifacts are a bounded carve-out; see § "Raw artifacts" below.)
- **Legally-sensitive documents** (cap tables, shareholder agreements, NDAs, signed contracts). Wrong surface; keep those in a secure drive with proper access controls.
- **HR / hiring / comp details** about specific individuals. If team processes require such notes, use a separate private system. `team/<person>/README` is for role/focus/public-facing context, not confidential details.
- **Scratch notes that aren't worth version history.** Use ephemeral chat / notes apps. If a note turns out to matter, add it with `/add-entry`.
- **Running commentary / journal entries.** This isn't a diary. If an observation is worth keeping, it's a brainstorm, question, or decision.
- **Duplicated content from sub-project docs.** The "cite, don't copy" principle is absolute. If it's authoritative in `../your-product-repo/docs/` or a sibling repo, link out.

---

## Finances — a bounded carve-out

`finances/` is the one place transaction data and small binary receipts live, because cash-flow tracking needs structured records (see `finances/README.md`). It is a *deliberate, bounded* exception to two rules above, not a loophole:

- **Allowed:** the append-only `finances/ledger.csv`, **small** receipt images in `finances/receipts/`, and **redacted** statement snapshots (`finances/statements/`, last-4 only).
- **Still out:** raw bank statements (full account numbers — redacted in memory, never committed), full account/routing/card numbers anywhere, multi-MB binaries, and **cap tables / contracts / payroll-comp detail** (those remain out per "Out of scope" above — `finances/` is operational cash-flow, not legal/HR records).
- This is *tracking*, not bookkeeping — no double-entry, accrual, P&L, or tax prep. If real books are needed, that's QuickBooks; `finances/` becomes the feeder.

---

## Raw artifacts — a bounded carve-out

`raw/` holds primary artifacts the rest of the KB cites: verbatim meeting and session transcripts (`raw/transcripts/`, cited line by line from `meetings/` notes and never edited after filing), sent and received email threads (`raw/emails/`), deck PDFs with slide-by-slide sidecars (`raw/pitchdecks/`), event material, and renders of KB docs (`raw/renders/`). Each binary gets a same-name `.md` sidecar so it is searchable; transcripts and large machine dumps are excluded from default search via the repo's `.ignore`. Recordings and multi-MB binaries stay out.

---

## Anti-patterns we won't enable

- **Append-only mega-files.** We use dated folders with one-file-per-entry instead (`decisions/`, `questions/`, `traction/`).
- **Line-range citations** (`[[foo#L42-58]]`). They rot silently. Use section anchors or quoted phrases. (Sole exception: `[T:NN]` links into never-edited transcripts — CONVENTIONS §"Citation discipline".)
- **Rule duplication between skills and CONVENTIONS.** Skills reference the rulebook; the rulebook is the single source of truth.
- **Flat INDEX.md that contains both rules and listing.** Rules live in `CONVENTIONS.md`, folder purpose in `<folder>/README.md`, entry listing in auto-generated `<folder>/INDEX.md`, routing in `AGENT-GUIDE.md`.
- **Auto-summaries at end of every session.** Skills produce output by doing work; they don't narrate.
- **Running two browser-tool tasks in parallel, or letting a subagent drive a browser.** Single session, single-writer rule; subagents report "could not fetch".

---

## Known limits of this KB as a system

- **Single-writer lock is local to the session filesystem.** Two users on two machines aren't synchronized by the lock; you'd need a remote mutex. Current assumption: one user at a time writing.
- **Wikilinks are checked for existence, not meaning.** `kb-lint` rejects a `[[...]]` that does not resolve, but it cannot tell whether the link points at the right file.
- **Frontmatter schema validates types and required fields, not semantic content.** "All synthesis docs have `## Counter-arguments` section" is a schema rule; "the counter-arguments are actually considered" is a human rule.
- **Search is lexical.** git + grep + `scripts/kb-prompt-lookup.py` (term and alias matching over frontmatter and text). No embedding / semantic retrieval layer here. If you need that, layer it on top — the KB is a plain markdown tree.
- **The KB doesn't auto-age content.** `/kb-audit` and the session-start staleness report surface stale drafts and an out-of-date `STATE.md`; updating, promotion and archival are still a human call.

---

## When a limit starts to hurt

If you're thinking "this doesn't fit anywhere" and you've consulted `AGENT-GUIDE.md` §"Where does this content go?" — either:
1. It's out of scope (see above); use a different system.
2. It warrants a new folder or a new file type; invoke `/kb-add-folder` (enforces CONVENTIONS growth rules and requires justification).

Never silently stuff it into the nearest-looking folder.
