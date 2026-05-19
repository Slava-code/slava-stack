---
name: complete-todo
description: "Mark a project-kb todo complete. Updates frontmatter (status: completed, completed_at: today), moves the file to todos/completed/, and AUTOMATICALLY appends a one-line entry to each related entity's `## Interactions` section — no permission prompt. Use when user says: completed X, done with Y, sent the email, had the call, meeting happened, task finished."
---

# /complete-todo <slug>

Usage: `/complete-todo 2026-04-20-example-slug`.

1. Acquire `runs/.lock`.
2. Read `todos/<slug>.md`.
3. Update frontmatter:
   - `status: completed`
   - `completed_at: <today>`
4. Move file: `git mv todos/<slug>.md todos/completed/<slug>.md`.
5. **Auto-merge to related entities (NO permission prompt):**
   For each wikilink in the todo's `related:` frontmatter field:
   - Resolve the target file path
   - **If the target is a team-member README** (path like `team/<slug>/README.md` or `team/<slug>` resolving to it): append `- YYYY-MM-DD — <todo title>` to the bottom of `team/<slug>/interactions.md` instead. Create that sidecar if it doesn't exist (use `team/founder-template/interactions.md` as template — frontmatter `type: interactions-log` + body with `## Log` heading). Do NOT touch the README's `## Interactions` section — it just points at the sidecar.
   - **Otherwise** (advisor, decision, comparison, project, etc.): if the target file has an existing `## Interactions` section, append `- YYYY-MM-DD — <todo title>` under it. If no `## Interactions` section exists, create one just before `## Related` (or at the end if no `## Related`).
6. Stage all modified files (the moved todo + every related entity touched) + commit: `todo: complete <slug>`. Push.
7. Release the lock.

If the user wants to add a note/outcome beyond the todo title (e.g., "advisor replied yes, meeting on Tuesday"), use `/add-entry` with type advisor-event (or whatever fits) — separate from completion.
