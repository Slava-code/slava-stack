---
name: pitchdecks — pitch deck PDFs + sidecars
description: Pitch deck PDFs + paired sidecars (slide-by-slide); current = newest sidecar without superseded_by.
type: folder
---

# raw/pitchdecks/

Your project's pitch deck PDFs and their paired `.md` sidecars. Ships empty — add your first deck here.

## Pairing convention

Each PDF has a same-basename `.md` sidecar with `type: source`. The sidecar contains:

- Slide-by-slide breakdown (every numeric metric, every claim, every diagram element, every named entity)
- Headline metrics list (every numeric stat in the deck, one per line, with slide N)
- Vocabulary map (every distinctive term/phrase with slide N + meaning)
- Verticals named, competitors named, team-slide details, ask-slide details
- Diff vs the prior deck (when applicable)

Pairing rule (DEMO slugs — replace with your own):

| PDF | Sidecar |
|---|---|
| `2026-01-15-example-pitchdeck.pdf` | `2026-01-15-example-pitchdeck.md` |

When a new deck is added, set `supersedes:` in the new sidecar and back-stamp the prior sidecar in the same commit: `status: superseded` + `superseded_by:` pointing at the new one.

## Current deck

Do not hand-label a deck "current canonical" here or anywhere else: the label rots the day a newer deck lands. The current deck is the newest sidecar in this folder that has no `superseded_by:` in its frontmatter. Pricing and competitor slides tend to differ between decks, so always say which deck a figure comes from.

## Why a sidecar instead of just opening the PDF

PDF reads are token-expensive and the binary doesn't grep. A `.md` sidecar lets every agent — main or sub — answer "what does the deck claim about traction?" or "which competitors are named?" with a cheap text read, and lets the deck be cited section-by-section from other files (investor blurb, applications, comparisons).
