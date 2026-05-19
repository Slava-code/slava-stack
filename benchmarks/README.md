---
type: folder
description: "Benchmark specifications — what we measure, how, against what; feeds experiment runs"
---

# benchmarks/

**Benchmark specs** — what we measure, how, with what corpus, against what threshold, with what models, *why* each choice.

**File naming:** `YYYY-MM-DD-<spec-slug>.md`. Most recent per product = current setup.

**Frontmatter required:** `type: benchmark-spec`, `product:`, `supersedes:` (if superseding a prior spec), `status:`.

**Written on:** explicit ask.

**Note:** Per-project benchmarks live in their respective product repos (e.g. `../your-product-repo/eval/`). This folder holds *aggregate-level* benchmark work (KB-itself benchmarks, cross-project comparative benchmarks).

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
