---
type: folder
description: "Project team members — per-person README + voice preferences"
---

# team/

**Project team members.** Profiles + context for anyone building the project. Distinct from `advisors/` (external academics / advisors) and `discovery/` (customers / prospects).

**Default pattern: entity folder per person.** Each member gets a subdirectory with `README.md` (current profile, rewritten as role/focus evolves) + optional dated files (1:1 notes, focus-area deep-dives, decisions attributable to that person).

**Shared team info** (team inbox, domain, anything not tied to one person) lives in [`general/README.md`](general/README.md). Not a personal profile — the active-user preferences loader keys off `SOUL.md`, not anything here.

```
team/<person-slug>/
├── README.md                       current profile — role, focus, contact
├── 2026-05-01-1-1-notes.md         optional: 1:1 notes
└── 2026-05-15-focus-shift.md       optional: significant role/focus change
```

**File naming:** `<person-slug>/README.md` for the profile; dated siblings use `YYYY-MM-DD-<event>.md`.

**Frontmatter (README):** `type: team-member`, `role:`, `status: active | inactive`, `product: shared`, `tags:`.

**What NOT to put here:**
- Comp, equity, HR-sensitive details — wrong surface; use a secure drive.
- Private 1:1 feedback — if it's sensitive, keep it out of git.
- Other people's stuff without their say-so.

**Completion hook:** when a todo has `related: team/<person>/README`, `/complete-todo` auto-appends a one-line entry to that person's README `## Interactions` section — same mechanism as advisors.

**Written on:** when someone joins, when role/focus shifts, when shareable context accumulates.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
