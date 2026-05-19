---
type: folder
description: "Architecture snapshots — one per product track, concurrent; most recent per product = current view"
---

# synthesis/

Architecture snapshots. **One per product track, concurrent.** Most recent dated file per `product:` = current view.

**File naming:** `YYYY-MM-DD-<product>-architecture.md`

**Required sections:** `## Counter-arguments`, `## Data gaps` (anti-sycophancy).

**Frontmatter required:** `type: synthesis`, `product:`, `supersedes:` (points at prior synthesis for this product), `confidence:`.

**Rollforward rule:** when writing a new synthesis for a product, read the prior one + every brainstorm / dispatch / experiment / decision written for that product since. Consolidate. Set `supersedes:`. Mark the prior entry `**(superseded)**` in the root [CATALOG](../CATALOG.md).

**Written on:** explicit ask — "synthesize" / "snapshot the architecture." Never unprompted.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Routing: [../AGENT-GUIDE.md](../AGENT-GUIDE.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
