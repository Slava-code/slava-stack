---
type: folder
description: "What we tried, measured, learned — distinct from benchmarks (spec); results with metrics + next steps"
---

# experiments/

**What we tried, measured, learned.** Distinct from `benchmarks/` which holds the *spec*; `experiments/` holds the *result*.

**File naming:** `YYYY-MM-DD-<experiment-slug>.md`. Examples: `YYYY-MM-DD-corpus-run-entity-merging.md`, `YYYY-MM-DD-ingestion-model-selection.md`.

**Structure:**
1. What was tried + why
2. Setup (cite `benchmarks/` spec if applicable)
3. Result (metrics, comparisons)
4. What we learned
5. Next step / fixes shipped

**Frontmatter required:** `type: experiment`, `product:`, `status:`.

**Written on:** after running an experiment, when asked to log it.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
