---
name: raw — founder-authored binary assets
description: Founder-authored binaries (decks, recordings, screenshots) outside classified folders; cite via raw/<sub>/<file>.
type: folder
---

# raw/

Holds founder-authored binary assets that don't fit a classified KB folder type. Currently scoped to:

- [`pitchdecks/`](pitchdecks/) — pitch deck PDFs + paired markdown sidecars
- [`contracts/`](contracts/) — signed/draft legal agreements (contractor, NDA, IP-assignment) + paired markdown sidecars
- [`events/`](events/) — event-planning binaries for events we host (budgets, sponsor decks, run-of-show)
- [`papers/`](papers/) — original external paper PDFs preserved beside their `sources/` digests
- [`transcripts/`](transcripts/) — verbatim founder-brainstorm transcripts (primary artifacts)

Cite the canonical file from elsewhere using the relative path appropriate to the citing file (e.g. `[[../raw/pitchdecks/YYYY-MM-DD-pitchdeck.pdf]]`).

## Convention — each binary that gets cited often gets a markdown sidecar

For PDFs, videos, and image assets that get cited often, pair the binary with a same-basename `.md` sidecar that an agent can read without opening the binary. The sidecar uses `type: source` and carries:

- A `description:` in frontmatter (so it appears in the parent INDEX)
- A breakdown of the binary's contents (slide-by-slide for decks, scene-by-scene for video, element-by-element for images)
- Headline metrics list, vocabulary map, named entities — anything an agent would want to cite

This way an agent answering "what does the deck say about TAM?" reads the sidecar `.md` and never opens the PDF.

## What this folder is NOT

- Not the inbox queue — see [`../inbox/`](../inbox/)
- Not for digested external sources — those go in [`../sources/`](../sources/)
- Not for opinionated takes on our own decks — those go in [`../brainstorming/`](../brainstorming/) or [`../strategy/`](../strategy/)
