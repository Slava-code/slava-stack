---
type: folder
description: "Head-to-head competitor/alternative analyses with decision_status; flat files + entity folders for deep dives"
---

# comparisons/

**Head-to-head competitor / alternative analyses** with a `decision_status`. The pile of competitor docs rolls up into strategic positioning via the status.

**File naming (flat):** `YYYY-MM-DD-<competitor-slug>.md` for positioning / quick-reference.

**File naming (entity folder):** `YYYY-MM-DD-<competitor-slug>/` with `README.md` + optional deep-dive chapters + dated event files. Used for reference implementations we want to study chapter-by-chapter. Promote from flat → folder when >300 lines OR a second dated event is added.

**Structure (flat / README):**
1. What it is
2. How it works / stack
3. Why it matters / overlap with the project
4. Structural limits / differentiators
5. `## Decision` section setting `decision_status`
6. `## Related` wikilinks

**Frontmatter required:** `type: comparison`, `product:`, `decision_status: considered | adopted | rejected | borrowed-partial`, `confidence:`, `status:`.

**Entity-folder convention:** README body is *current truth, rewritten as it evolves* (a competitor's architecture, funding, positioning). Dated sibling files (e.g., `2026-05-02-series-a-announced.md`) form the append-only evidence timeline. No separate `timeline.md`.

**Sub-taxonomy when folder reaches ~15 files:** use `comparisons/by-<facet>/` (e.g., `by-vertical/`, `by-horizontal-memory/`, `by-rag-infra/`) per CONVENTIONS growth rules.

**Written on:** explicit ask.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
