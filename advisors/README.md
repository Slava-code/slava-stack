---
type: folder
description: "Outreach-target intel on specific people — professors, potential advisors, angels"
---

# advisors/

**Academic + advisor outreach and profiles.** Professors, potential advisors, industry contacts whose engagement we're pursuing.

Distinct from:
- `sources/` — which is external *material* (papers, articles). A professor's *paper* goes in sources; the *professor* goes here.
- `discovery/` — which is customer-side. Advisors are supply-side of credibility/expertise.

**Default pattern: entity folder per person.** Advisors accumulate: a profile, email drafts, meeting notes, collaboration angles. Flat files don't scale here.

```
advisors/<advisor-slug>/
├── README.md                       current profile + relationship state
├── YYYY-MM-DD-initial-research.md  what we learned about them before outreach
├── YYYY-MM-DD-email-draft-v1.md    drafts (promote to sent + dated on send)
└── YYYY-MM-DD-intro-call-notes.md  dated events
```

**Structure (README.md per advisor):**
1. Who — title, institution, department
2. Research / expertise (brief — if in depth, link to sources/ digest of their work)
3. Relevance to the project (specific, not generic)
4. Relationship status — current state
5. Outreach strategy / collaboration angle
6. `## Related` wikilinks

**Frontmatter required (README):** `type: advisor`, `tier: 1 | 2 | 3`, `institution:`, `status: prospect | contacted | engaged | committed | declined`, `confidence:`, `tags:`.

**Timeline for free:** dated files in the folder = chronology. `ls advisors/<slug>/` sorts them. No separate timeline doc.

**Completion hook:** when a todo related to an advisor is completed via `/complete-todo`, a one-line entry is auto-appended to the advisor's README `## Interactions` section (e.g., `- YYYY-MM-DD — Emailed re <topic>`). Builds the timeline organically.

**Written on:** when researching or contacting an advisor; when outreach events happen.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
