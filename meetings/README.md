---
type: folder
description: "Meeting/call notes citing raw/transcripts/ by line; extracts propagate to todos/, strategy/, advisors/"
---

# meetings/

**Notes for every meeting and call, each tied line by line to its verbatim transcript.** Any meeting — advisor, customer, investor, partner, internal — is two files: a notes file here (a short digest agents actually read) and the verbatim transcript in [`../raw/transcripts/`](../raw/transcripts/) under the same slug. Every claim in the notes links to the transcript line it came from, so a reader can check the exact words in one click. Written by the `/meeting` skill.

**Two-file rule.** (1) The transcript is saved unedited as `raw/transcripts/YYYY-MM-DD-<slug>.md` (`type: source`, a short header, then the text) and is never edited after filing, so line numbers stay stable. (2) The notes file cites it as `[T:NN](../raw/transcripts/<file>.md#LNN)`. "The full transcript lives in the recording app" is not a record: if the transcript hasn't been pasted yet, ask for it.

**Why a format-keyed folder** (vs. routing each meeting by counterparty): a meeting is a distinct *artifact* — the transcript is long, machine-generated, low signal-per-token — and the capture habit is high-frequency. One consistent home + flow beats classifying every meeting by who attended. Counterparty context isn't lost; it's a `related:` wikilink (`[[advisors/<slug>/README]]`), same as everything else in the KB.

**Distinct from:**
- `discovery/` (`type: interview`) — customer/prospect-call *digest* keyed to a firm/persona. A customer meeting can keep its interview digest in `discovery/` AND link to the notes here.
- `advisors/<slug>/` (`type: advisor-event`) — advisor *relationship timeline*. An advisor meeting's notes live here (transcript in `raw/transcripts/`); the relationship state stays in `advisors/`.

Those are relationship-keyed digests; `meetings/` is the format-keyed record they cite into.

## The propagation rule (the point of this folder)

A meeting file is a *source*, not a destination. The valuable bits fan out:

| Inside a meeting | Propagates to |
|---|---|
| Action items / "we should do X" | `todos/` |
| Positioning / GTM / competition insight | `strategy/` (or `brainstorming/` if still open) |
| Who we met (advisor/contact worth tracking) | `[[wikilink]]` now; `advisors/<slug>/` stub if recurring |
| Files / links exchanged | `raw/` (binaries) or `tools/` (utilities) |

`/meeting` extracts these and **confirms each with the user before writing** — transcripts are full of hedges ("we *should ask about* X", "*maybe* reposition") and must not be rounded up into commitments (CONVENTIONS §inference discipline).

## File naming

`meetings/YYYY-MM-DD-<counterparty-slug>-<topic>.md` — date sorts chronologically in a flat `ls`.
- `2026-01-15-example-advisor-pricing-model.md`

Promote to an entity folder only if one counterparty accumulates many meetings (rare — recurring advisors/customers already have homes in `advisors/`/`discovery/`).

## Frontmatter

**Required:** `type: meeting`, `title`, `product`, `date_found` (meeting date), `participants:` (list), `counterparty_kind: advisor | customer | investor | partner | internal | networking | other`, `status`.
**Optional:** `related` (wikilinks), `source` (how captured), `confidence`, `redacted`, `tags`, `description`.

**Privacy:** sensitive/NDA meeting? Set `redacted: true` and scrub identifying detail before committing. Git history is the repo's memory.

## Body

Mandatory `## TL;DR` (the digest — enforced by lint so a meeting is never a raw dump). Then `## Key points`, `## Action items`, optional `## Strategy notes` / `## Notable quotes` / `## Artifacts shared`, `## Related`, and a one-line `## Transcript` pointing at `raw/transcripts/<same-slug>.md`. Every claim links to its transcript line as `[T:NN](../raw/transcripts/<file>.md#LNN)`.

**Written on:** `/meeting` — whenever you have a transcript or notes to save.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
