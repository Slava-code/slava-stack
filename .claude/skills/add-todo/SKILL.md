---
name: add-todo
description: "Add a todo / event / meeting with a deadline to the project-kb. Creates todos/YYYY-MM-DD-<slug>.md (filename date = deadline, so `ls todos/` sorts by upcoming). Frontmatter: type: todo, deadline, status: pending, priority, related entities (wikilinks to advisors/firms/decisions). Use when user says: add todo, remind me to X by Y, schedule event, log upcoming meeting, I need to do Z."
---

# /add-todo

1. Acquire `runs/.lock`.
2. Elicit (or infer) from user:
   - **Title** (required) — one-line description
   - **Deadline** (required) — YYYY-MM-DD
   - **Priority** (required) — high | medium | low
   - **Kind** (optional) — task | event | meeting (default: task)
   - **Related entities** (optional) — wikilinks to advisors/firms/decisions/team members
3. Generate slug from title (lowercase, hyphenated, max 40 chars).
4. Create `todos/<deadline>-<slug>.md` using `schema/templates/todo.md`. Fill frontmatter:
   - `type: todo`
   - `kind:` if provided
   - `title:`
   - `deadline:`
   - `status: pending`
   - `priority:`
   - `created_at:` (today)
   - `completed_at: null`
   - `related:` list of wikilinks
5. Fill body: title + deadline line + brief prep notes if user provided them.
6. Stage + commit: `todo: add <deadline>-<slug>`. Push.
7. Release the lock.
