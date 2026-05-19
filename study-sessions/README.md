---
type: folder
description: "Per-source study logs — append-only /study session checkpoints tracking learning progression per source"
---

# study-sessions/

> The auto-generated list of entries lives in [`INDEX.md`](INDEX.md) — rebuilt by `scripts/rebuild-indexes.py` from each file's `description:` frontmatter. Do not hand-edit INDEX.md.

**Per-source learning logs.** One file per source, append-only. Tracks *your* progression through a source beyond what the `sources/` digest and `brainstorming/` take already capture. Factual digest and opinionated take are written *once*; the study log *grows* as you come back to the material.

**Written by `/study`** — never unprompted. Each session appends one H2 checkpoint at session end.

## Filename rule

**Study filename = source filename, exactly.** For a source at `sources/YYYY-MM-DD-example-source-slug.md`, the study log is at `study-sessions/YYYY-MM-DD-example-source-slug.md`. Date prefix mirrors the source (not the study start date). Makes `sources/X.md` ↔ `study-sessions/X.md` lookup trivial.

## Append-only checkpoint model

One checkpoint per `/study` session, written at session end (not mid-session). Newest at the bottom. H2 headers: `## Checkpoint — YYYY-MM-DD (session N)`.

Canonical checkpoint shape — see `schema/templates/study-log.md`:

- **What we covered** — topics touched this session
- **What I now understand** — incremental learning (the delta)
- **Candidate questions / decisions** — inline `[?question]` / `[?decision]` tags. **Not auto-promoted.** User must explicitly ask to promote a tag to `questions/` or `decisions/`.
- **Related sources touched** — wikilinks to other `study-sessions/` files; triggers the reciprocal cross-ref rule below
- **Open threads → next session** — resume hints for future-you

## Cross-reference rule (bidirectional)

When a session on Source A meaningfully touches Source B:
- A's study file gets the full checkpoint with `[[study-sessions/B]] §checkpoint-N` under "Related sources touched"
- B's study file gets a **short reciprocal checkpoint** — one sentence, pointer back, no primary-study progress claimed

Both sides know about the link. Readable without a grep.

## Concept-log twin

Concept study logs live at `concepts/<slug>/study-log.md` (same `type: study-log`, same body shape, same checkpoint rules). Difference: source study log has `source:` in frontmatter; concept study log has `concept:` instead.

## What this folder is NOT

- **Not a second brainstorm.** Project-angle takes go in `brainstorming/`. Study logs capture *learning process*, not new positioning.
- **Not where decisions get made.** `[?decision]` tags flag candidates. Actual decisions go to `decisions/` via explicit promotion.
- **Not date-keyed.** One file per source, not one file per date. Session count grows within the file.

## Frontmatter

`type: study-log`, `title:`, `product:`, `source:` OR `concept:` (exactly one), `date_found:`, `last_checkpoint:`, `status:`. See `schema/templates/study-log.md` and `schema/kb-schema.yaml`.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
