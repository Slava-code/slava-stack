---
title: "Example: Vector DB survey — managed vs self-hosted trade-offs"
description: "EXAMPLE — public survey comparing four open-source vector databases on recall, latency, and ops burden"
type: source
product: track-a
source: "https://example.com/vector-db-survey-2026"
date_found: 2026-01-15
tags: [example, vector-db, infrastructure, embeddings]
status: reviewed
---

> **This is example content shipped with project-kb.** Replace it with your own sources, or delete it once you have your own.

## What it is

A public survey article comparing four open-source vector databases on recall, p99 latency, and operational burden at ~10M-vector scale. Run by an independent benchmark team.

## Key claims

- All four hit > 0.95 recall@10 on the standard benchmark; the differences are in long-tail latency and ops burden, not core search quality.
- Managed offerings let teams ship faster but lock pricing at "per-vector" levels that get expensive past ~50M vectors.
- Self-hosted is cheaper at scale but adds an on-call surface (HNSW index rebuilds, replication, backup/restore).
- The author flags that benchmarks rarely include update-heavy workloads — recall under high-churn is mostly untested.

## Why we care

We're choosing between managed and self-hosted for the embedding store. The author's "your real cost is engineer-hours, not infra dollars" framing reframes our decision.

## Fetched from

- `runs/fetches/2026-01-15-example-vector-db-survey.txt` — fictional placeholder for the raw fetch output

## See also

- `[[brainstorming/2026-01-15-example-vector-db-implications]]` — our take on what this means for our architecture
- `[[comparisons/2026-01-15-example-vector-db]]` — head-to-head we ran ourselves
