---
name: kb-process-inbox
description: "Drain the project-kb inbox queue. Groups near-duplicate drops (same URL) and dispatches ONE subagent per group — so duplicate drops produce one merged entry, not N redundant ones. Each group is processed sequentially by a fresh subagent that fetches external content (Chrome for LinkedIn/X), classifies, creates the entry, commits, and removes all grouped inbox files. Respects single-writer lock. Use when user says: process inbox, drain queue, triage drops, clean up captures, deal with the backlog."
---

# /kb-process-inbox — Drain the queue

Usage: `/kb-process-inbox` (process all, with grouping), or `/kb-process-inbox <slug>` (one specific drop, skips grouping).

## Step 1 — Group near-duplicates before dispatching

1. **List inbox drops.** Paths of `inbox/*.md` (ignore `INDEX.md`). If given a slug arg, skip grouping.
2. **Read frontmatter + first ~20 body lines of each drop** — not full body, keeps main context cheap. Extract:
   - `source_url` frontmatter field if present
   - Any URL pattern (`https?://...`) found in body
   - A 1-line topic summary if no URL
3. **Group** drops by shared URL (exact match after stripping common trackers: `?trackingId=...`, `&utm_*`, `?fbclid=...`, `?ref=...`, trailing `/`). Drops sharing a URL → one group. Drops with no URL → their own singleton groups. **Do not auto-group by topic string similarity** — false merges destroy information; solo processing is the safe default.
4. **Report groupings to user up front**: e.g., "2 drops about <URL> grouped → 1 task; 3 solo drops → 3 tasks. Proceed?" — wait for OK unless user said "process all without asking."

## Step 2 — Sequential dispatch (one subagent per group)

Respect the single-writer lock + single Chrome session. For each group:

Dispatch a **fresh Agent subagent** with this task:

> Process this group of `N` near-duplicate inbox drops that share a URL. Paths:
>   `<path1>`
>   `<path2>`
>   ...
>
> Steps:
> 1. Acquire `runs/.lock` at repo root. If held, wait briefly then abort with clear message.
> 2. Read all `N` drops fully. Extract: the shared URL, each drop's distinct commentary / prompt angle, any user-supplied context.
> 3. **Fetch the URL content ONCE** — not per drop.
>    - WebFetch for regular URLs
>    - `mcp__claude-in-chrome__*` for LinkedIn / X / login-walled
>    - Never parallel Chrome tasks
> 4. **Classify** destination per AGENT-GUIDE.md §"Where does this content go?". For a single URL with multiple analysis prompts, typical outcome is ONE `sources/` digest (factual) — and possibly ONE follow-on `brainstorming/` or `comparisons/` entry that incorporates ALL commentary angles. Not N duplicate files.
> 5. Create entries using `schema/templates/<type>.md`. Merge the distinct angles from all N drops into the single target entry (cite each drop's specific prompt if it adds value).
> 6. Regenerate INDEXes: `python3 scripts/rebuild-indexes.py`. Stage all modified INDEX.md files. The destination folder's INDEX.md now lists the new entry (pulled from its `description:` frontmatter).
> 7. Stage everything in ONE commit: new entry/entries + regenerated INDEX.md files + removal of all N inbox drops. Message: `inbox: process <group-slug> (n=<N>) → <destination>` (body can enumerate each input drop slug).
> 8. Push. Release the lock.
> 9. Return one line: `<N> drops merged → <destination>` (or `<N> drops → (discarded — <reason>)`).

For singleton groups (N=1), same flow — straight process, no merging.

## Step 3 — Summarize

Collect per-group results. Report to user:
- Total drops in, total groups, total new entries written, drops discarded
- Destinations list
- Any failures (lock held, Chrome unavailable, classification ambiguous)

## Rules

- **Never parallelize** subagents — lock serialization + single Chrome session.
- **Never merge drops that don't share a URL** — topic-string similarity is unreliable; false merges destroy information.
- **Login-walled content** (LinkedIn, X) — if the Chrome extension isn't available, abort the group cleanly and leave drops in inbox for a later retry.
- **Discarding low-signal drops** — explicit commit `inbox: discard <slug> — <reason>` per drop (or one commit for a group).
