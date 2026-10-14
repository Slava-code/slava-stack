---
name: complete-todo
description: "Close a todo: mark it completed (or cancelled), move it to todos/completed/, append a line to each related entity's Interactions, fix inbound links, and update STATE.md if an outcome changed. Use when the user says: done with X, sent the email, had the call, the meeting happened, that's cancelled, no longer needed."
---

# /complete-todo <slug>

Usage: `/complete-todo 2026-04-20-example-slug`.

1. Acquire `runs/.lock`.
2. Read `todos/<slug>.md`.
3. Update frontmatter:
   - `status: completed` and `completed_at: <today>`; or, when the task is moot or dropped, `status: cancelled` and `completed_at: <today>`.
   - Add one line under a `## Outcome` heading in the body: what happened, or why it was cancelled, with the date and who said so. A meeting-type todo always gets its outcome recorded, even "happened, nothing notable".
4. Move file: `git mv todos/<slug>.md todos/completed/<slug>.md` (cancelled todos move there too; the status tells them apart).
5. **Auto-merge to related entities (NO permission prompt):**
   For each wikilink in the todo's `related:` frontmatter field:
   - Resolve the target file path
   - **If the target is a team-member README** (path like `team/<slug>/README.md` or `team/<slug>` resolving to it): append `- YYYY-MM-DD — <todo title>` to the bottom of `team/<slug>/interactions.md` instead. Create that sidecar if it doesn't exist (copy `team/founder-template/interactions.md` — no frontmatter, a `## Log` heading). Do NOT touch the README's `## Interactions` section — it just points at the sidecar.
   - **Otherwise** (advisor, decision, comparison, project, etc.): if the target file has an existing `## Interactions` section, append `- YYYY-MM-DD — <todo title> (<outcome in a few words>)` under it. If no `## Interactions` section exists, create one just before `## Related` (or at the end if no `## Related`).
   - Skip the append for cancelled todos unless the cancellation itself is news for that entity.
6. **Inbound links.** `kb-lint` resolves links to a moved todo through `todos/completed/`, so nothing breaks; when you touch a file that links to it anyway, rewrite the link to the new path.
7. **Keep current truth current.** Ask: does this change what is true now — an outcome, a status, a number, a price, a decision, who someone is? If yes: (a) edit the matching line in `STATE.md` and bump its `as-of:` date; (b) update the hub README if the entity has one (see `ALIASES.md`); (c) add a new row to `ALIASES.md` for any new recurring name, nickname or transcript mis-spelling; (d) put a one-line outcome banner on older files that still read as open. Stage these in the same commit set. Skip silently if nothing changed.
8. Stage all modified files by explicit path (the moved todo + every related entity touched + `STATE.md`/hub if changed) + commit: `todo: complete <slug>` or `todo: cancel <slug>`. Push.
9. Release the lock.

If the user wants to add a note/outcome beyond the todo title (e.g., "advisor replied yes, meeting on Tuesday"), use `/add-entry` with type advisor-event (or whatever fits) — separate from completion.
