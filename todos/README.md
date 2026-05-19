---
type: folder
description: "Tasks, events, meetings, deadlines — lightweight layer linked to entities; file date = deadline"
---

# todos/

**Tasks, events, meetings, deadlines.** Lightweight todo layer on top of the KB — linked to entities (advisors, firms, decisions) so completion flows naturally into their timelines.

**File naming:** `YYYY-MM-DD-<slug>.md` where date = **deadline date** (not creation date). This way `ls todos/` sorts by upcoming.

**Minimal frontmatter:**
```yaml
---
type: todo | event | meeting
title: "Email <advisor> re <topic>"
deadline: YYYY-MM-DD
status: pending | completed | cancelled
priority: high | medium | low
related:
  - "[[advisors/<advisor-slug>/README]]"
created_at: YYYY-MM-DD
completed_at: null
---
```

**Body:** brief — what needs to happen, prep needed. Usually a few lines. Meeting notes go in `discovery/` or advisor event files; `todos/` is the reminder, not the record.

**Lifecycle:**
- `/add-todo` — creates the file
- `/deadlines` — lists today-due + overdue-pending (subagent reads frontmatter only; cheap)
- `/complete-todo <slug>` — updates frontmatter to `status: completed`, moves file to `todos/completed/`, and **automatically** appends a one-line `## Interactions` entry to each `related:` entity file

**Stale handling:** `/deadlines` surfaces overdue pending items; user decides per-item: mark completed, update deadline, or cancel.

**Never auto-deletes.** Completed todos preserve detail in `todos/completed/`; the one-line merge into related entity files gives you the entity-view timeline.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
