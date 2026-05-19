---
type: folder
description: "Metrics snapshots — corpus/pipeline/revenue/team/qualitative; what moved since last snapshot"
---

# traction/

**Dated metric snapshots.** Business traction, corpus stats, customer pipeline, qualitative signals — anything that shows "where are we now, compared to before."

Distinct from `experiments/` which is system-quality metrics. Traction is *business* state.

**File naming:** `YYYY-MM-DD-<scope-slug>.md`. Examples: `2026-04-17-corpus-stats.md`, `2026-04-17-pipeline-snapshot.md`, `2026-04-17-team-metrics.md`.

**Structure:** one table or a few paragraphs; diffable against prior snapshots. Keep it tight — if it's bloating, split into scope-specific files.

**Frontmatter required:** `type: traction-snapshot`, `scope: corpus | pipeline | revenue | team | qualitative`, `date_found:`, `status:`.

**Cadence suggestion:** weekly → monthly → quarterly as the business matures. Not enforced — written on explicit ask.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
