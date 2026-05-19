---
type: folder
description: "Research questions we don't yet have answers to — promotion path: questions -> dispatches -> decisions"
---

# questions/

**Lightweight open questions.** Things we want to think about later but aren't formalized enough to be a research dispatch.

Promotion path: `questions/` → `research-dispatches/` (when the question is worth formally researching) → `decisions/` (when the research commits a direction). `/kb-promote` handles the backlinks.

**File naming:** `YYYY-MM-DD-<question-slug>.md`. Examples: `YYYY-MM-DD-embedding-model-choice.md`, `YYYY-MM-DD-who-owns-retrieval-quality.md`.

**Structure:** the question (1-2 sentences) → why we're asking / context → current leaning if any → when we plan to address it (or "no plan yet") → related wikilinks.

**Frontmatter required:** `type: question`, `product:`, `status:`, `priority: high | medium | low`.

**Anti-thinning:** if a question is really a 1-liner, keep it as a one-liner — *don't* pad. Short files are fine here.

**Staleness:** `/kb-audit` surfaces questions that have been `raw` for 90+ days. User decides: promote, delete, or leave.

**Written on:** explicit ask. Usually user says "add a question about X."

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
