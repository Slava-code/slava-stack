# Reading Guides

Per-persona entry paths into this KB. Saves a cold reader from having to understand the whole folder layout before they can find what they care about.

---

## New engineer joining the project

You want to understand the architecture and what's been tried. Read in this order:

1. [`CLAUDE.md`](CLAUDE.md) — 2 min. What the KB is.
2. Most recent file in [`synthesis/`](synthesis/) for the product track you're joining — current architectural state.
3. The product source tree itself (cite-outs from synthesis) — source of truth for implementation.
4. [`experiments/`](experiments/) — concrete results: what was tried, what worked, what didn't.
5. [`research-dispatches/`](research-dispatches/) — open technical questions currently being chewed on.

Before contributing: [`CONVENTIONS.md`](CONVENTIONS.md).

---

## Investor evaluating the company

You want to understand positioning, competitive landscape, and traction. Read in this order:

1. [`CLAUDE.md`](CLAUDE.md) — 2 min.
2. [`comparisons/INDEX.md`](comparisons/) — competitive landscape entries (open the positioning file + any analyses of the best-funded competitors).
3. Most recent file in [`synthesis/`](synthesis/) — what the product actually is, where it stands.
4. [`strategy/`](strategy/) — GTM, pricing, fundraising narrative as it crystallizes.
5. [`traction/`](traction/) — dated snapshots of pipeline, corpus, qualitative signals.

---

## Advisor evaluating alignment

You want to understand whether the project is technically serious and how your expertise connects. Read in this order:

1. [`advisors/<your-slug>/README.md`](advisors/) — if it exists, alignment thinking is already drafted.
2. Most recent file in [`synthesis/`](synthesis/) — current system capabilities and gaps.
3. [`research-dispatches/`](research-dispatches/) — open technical questions where external expertise could help.
4. [`experiments/`](experiments/) — what was tried, what broke, what was learned. Unvarnished.

---

## Teammate joining the project

Different focus from "new engineer" — you may own product, go-to-market, or ops rather than core code.

1. [`USER-MANUAL.md`](USER-MANUAL.md) — 5 min. How to USE this KB.
2. [`team/INDEX.md`](team/INDEX.md) — who's here.
3. Most recent file in [`synthesis/`](synthesis/) — product state.
4. [`comparisons/INDEX.md`](comparisons/) — positioning + competitor reads.
5. [`strategy/`](strategy/) — GTM / pricing / fundraising as it fills.
6. [`discovery/`](discovery/) — customer conversations as they accumulate.
7. [`advisors/`](advisors/) — who's being cultivated externally.

Before contributing: [`CONVENTIONS.md`](CONVENTIONS.md) and [`AGENT-GUIDE.md`](AGENT-GUIDE.md).

---

## LLM agent booting up

See [`CLAUDE.md`](CLAUDE.md) §"Progressive boot." Then [`AGENT-GUIDE.md`](AGENT-GUIDE.md). Don't guess rules — the rulebook is [`CONVENTIONS.md`](CONVENTIONS.md).
