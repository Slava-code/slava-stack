---
title: "Example: Implications of the vector DB survey for our embedding store"
description: "EXAMPLE — brainstorm paired with the vector DB survey source; demonstrates the source+brainstorm pair pattern"
type: brainstorm
product: track-a
date_found: 2026-01-15
tags: [example, vector-db, architecture, brainstorm]
status: reviewed
---

> **This is example content shipped with project-kb.** Replace it with your own brainstorms, or delete it once you have your own.

## The setup

The survey ([[sources/2026-01-15-example-vector-db-survey]]) reframes our vector-DB choice as a labor-cost question, not an infra-cost question. Below: what that actually means for us at our current stage.

## What changes if labor-cost is the bottleneck

- We're a 3-person team with no dedicated ops. An on-call surface for index rebuilds is real cost.
- We have ~500K vectors today, ~5M projected end of year. Both are well under the "managed gets expensive" threshold the survey calls out.
- Managed lets us delete one whole class of incident from our future.

## What the survey doesn't tell us

- Update-heavy recall is unbenchmarked. Our use case is high-churn (re-embedding nightly). If managed offerings degrade silently under that load, we'd find out at scale.
- The survey is written by a self-hosting-leaning author (read between the lines: "your real cost is engineer-hours"). May undersell the lock-in cost of managed.

## Open questions

- Is there a public benchmark that simulates daily re-embedding? (Probably worth an `/add-entry questions/` if not.)
- At what vector count would we revisit? Concrete trigger > vague "if it gets expensive."

## Provisional read

Lean managed for now, with a documented re-evaluation trigger (vector count or monthly cost). The decision lives in [[decisions/2026-01-15-example-vector-db-choice]].
