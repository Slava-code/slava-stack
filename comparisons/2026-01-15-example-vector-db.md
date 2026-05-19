---
title: "Example: Vector DB comparison — managed vs self-hosted for our embedding store"
description: "EXAMPLE — four-way vector DB comparison with decision_status; shows the Decision section pattern"
type: comparison
product: track-a
decision_status: adopted
confidence: medium
date_found: 2026-01-15
tags: [example, vector-db, comparison]
status: reviewed
---

> **This is example content shipped with project-kb.** Replace it with your own comparisons, or delete it once you have your own.

## What we're comparing

Four options for our embedding store. Two managed, two self-hosted. Evaluated on: recall@10 (table-stakes), p99 latency at our query mix, ops burden, cost at projected 5M vectors.

## Option A — Managed Provider 1

- **Strengths:** Zero ops; sub-100ms p99 in published numbers; per-vector pricing is predictable.
- **Weaknesses:** Pricing model gets steep past ~50M vectors. Limited control over index parameters.
- **Fit for us:** Strong fit at current scale; revisit at 50M.

## Option B — Managed Provider 2

- **Strengths:** Slightly cheaper than A; competitive recall.
- **Weaknesses:** Newer offering; smaller community; we'd be a relatively early customer.
- **Fit for us:** Plausible but we'd accept maturity risk.

## Option C — Self-hosted Library 1

- **Strengths:** Best-in-class recall in published numbers; widely deployed; large community.
- **Weaknesses:** Adds on-call surface; index rebuilds need scheduled jobs; backup/restore is on us.
- **Fit for us:** Strong technically; weak for a 3-person team without dedicated ops.

## Option D — Self-hosted Library 2

- **Strengths:** Lean operationally; embedded mode keeps it simple.
- **Weaknesses:** Recall lags A/B/C at higher k. Limited update-heavy benchmarks.
- **Fit for us:** Plausible for a smaller deployment; less proven at our projected scale.

## Decision

**decision_status: adopted** — Option A (Managed Provider 1).

Rationale lives in [[decisions/2026-01-15-example-vector-db-choice]]. Re-evaluation trigger documented there.

## Confidence

Medium. The published benchmarks support the choice on quality and latency; the labor-cost argument is the load-bearing claim and is harder to verify in advance. If managed proves expensive faster than projected, we revisit per the decision's re-evaluation trigger.
