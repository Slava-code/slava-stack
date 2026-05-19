---
title: "Example: Adopt Managed Provider 1 as the vector database"
description: "EXAMPLE — decision record demonstrating ## Why and ## What we're giving up; cites the comparison and brainstorm"
type: decision
product: track-a
confidence: medium
date_found: 2026-01-15
tags: [example, vector-db, infrastructure, decision]
status: reviewed
---

> **This is example content shipped with project-kb.** Replace it with your own decisions, or delete it once you have your own.

## What we decided

Adopt Managed Provider 1 ([[comparisons/2026-01-15-example-vector-db]] §"Option A") as the vector database for the embedding store.

## Why

Three concurrent reasons:

1. **Labor cost dominates infra cost at our size.** Self-hosted adds an on-call surface (index rebuilds, backups, replication) that we don't have the ops headcount to support today. A managed offering deletes that class of incident.
2. **Current scale is well inside the managed price band.** At ~500K vectors today and ~5M projected end of year, we're far from the "managed gets expensive" threshold (~50M, per [[sources/2026-01-15-example-vector-db-survey]]).
3. **Quality differences are not load-bearing.** All four options hit > 0.95 recall@10 on standard benchmarks. The decision is not "which is best technically" — it's "which is best for a 3-person team."

## What we're giving up

- **Cost ceiling at scale.** If we grow past 50M vectors faster than projected, managed pricing becomes uncomfortable. Migration off a vector DB mid-flight is non-trivial.
- **Control over index parameters.** Some HNSW tuning knobs are not exposed. If we hit a corner-case recall problem on our specific data, the diagnostic path is "open a support ticket," not "tune the index ourselves."
- **Lock-in.** Switching costs grow with vector count. The longer we run on Provider 1, the more expensive a future migration becomes.

## Re-evaluation trigger

Revisit when either is true:
- Monthly cost crosses **$2,000** (current projection: ~$300 at year-end).
- Vector count crosses **25M** (current projection: ~5M at year-end).

When either trigger fires, re-run the comparison ([[comparisons/2026-01-15-example-vector-db]]) with current numbers.
