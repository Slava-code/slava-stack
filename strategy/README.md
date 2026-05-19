---
type: folder
description: "Crystallized strategic decisions — GTM, positioning, pricing, fundraising, partnerships, distribution"
---

# strategy/

**Crystallized strategic decisions.** GTM, positioning, pricing, fundraising, partnerships, distribution.

Distinct from:
- `brainstorming/` — which is the open exploration that may *lead* to a strategy entry
- `decisions/` — which is the single-decision ledger (one file per decision); strategy entries can be rolled-up positioning documents spanning multiple decisions
- `synthesis/` — which is architecture, not strategy

**File naming:** `YYYY-MM-DD-<topic-slug>.md`. Examples: `YYYY-MM-DD-positioning-v1.md`, `YYYY-MM-DD-pricing-tiers-v1.md`, `YYYY-MM-DD-fundraising-narrative.md`.

**Structure:** current position (one sentence) → reasoning → tradeoffs (what we're *not* doing) → dependencies / what could change this → `## Related` wikilinks.

**Frontmatter required:** `type: strategy`, `product:`, `strategic-thread:` (if applicable), `confidence:`, `status:`.

**Supersession:** when strategy changes, write a new dated file with `supersedes:` pointing at the prior; mark prior via `supersedes:` frontmatter.

**Written on:** explicit ask. Never unprompted.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
