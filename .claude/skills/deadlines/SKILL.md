---
name: deadlines
description: "Surface today-due and overdue-pending todos in the project-kb. Dispatches a subagent to grep frontmatter only — never reads full todo bodies — keeping main context cheap. Returns a compact list. User-invoked (NOT auto on session start). Agent may auto-invoke if a task relates to deadlines. Use when user asks: what's due today, what's overdue, check deadlines, any stale todos."
---

# /deadlines

Read-only skill. No lock needed.

1. Dispatch an Explore subagent with this task:
   > Read frontmatter ONLY from every file in `todos/*.md` (ignore `todos/completed/*` and `todos/INDEX.md`). Extract the `deadline:` and `status:` fields from each — use grep (`deadline:` and `status:`) rather than full file reads, to keep this cheap.
   > Return a compact list:
   > - "Due today": items where `status == pending` AND `deadline == today`
   > - "Overdue": items where `status == pending` AND `deadline < today`, sorted by how overdue (most overdue first)
   > - "No pending deadlines today or overdue": if the lists are empty.
   > Format each item: `- <deadline> — <title> (P:<priority>) — <slug>`.
2. Receive the list; surface to user.
3. For overdue items, gently prompt: "Want to mark complete (`/complete-todo <slug>`), update the deadline, or cancel?"

Do not auto-trigger on every session start — only when the user asks, or when a task explicitly relates to deadlines / scheduling.
