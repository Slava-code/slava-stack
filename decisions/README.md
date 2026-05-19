---
type: folder
description: "One file per architectural/strategic decision — company-level record, scannable via git log + index"
---

# decisions/

**One file per architectural or strategic decision.** Scannable ledger — `git log --oneline decisions/` gives the decision history across the company.

Distinct from:
- `comparisons/` — which carries `decision_status` on a competitor-analysis level. A decision here *may* cite a comparison as its source.
- `strategy/` — which is rolled-up positioning across multiple decisions. A strategy entry can cite several decisions.
- `experiments/` — which records *what we learned*. A decision here *may* cite an experiment as its basis.

**File naming:** `YYYY-MM-DD-<decision-slug>.md`. Examples: `YYYY-MM-DD-default-model-choice.md`, `YYYY-MM-DD-seed-round-target-size.md`.

**Required sections:** `## Why`, `## What we're giving up`, `## How this could be overturned` (anti-sycophancy).

**Frontmatter required:** `type: decision`, `product:`, `confidence:`, `status:`, `supersedes:` (if reversing a prior decision).

**Reversals:** write a new dated file with `supersedes:` pointing at the reversed decision. Mark prior as `status: superseded` in the same commit.

**Written on:** explicit ask. Decisions are milestones — not everything resolved is a decision worth recording.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
