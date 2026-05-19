---
type: folder
description: "Meta-topic folders spanning multiple sources — README (research digest) + study-log (checkpoint appends)"
---

# concepts/

> The auto-generated list of entries lives in [`INDEX.md`](INDEX.md) — rebuilt by `scripts/rebuild-indexes.py`. Do not hand-edit INDEX.md.

**Meta-topics that span multiple sources.** Where `sources/` holds individual papers/tools/repos and `brainstorming/` holds per-source takes, `concepts/` holds the *cross-cutting themes* that emerge from studying many sources — e.g. "graph databases," "retrieval evaluation," "parametric vs non-parametric memory."

**Folder-per-concept** (not file-per-concept). Each concept folder contains:

```
concepts/<concept-slug>/
  README.md       # type: concept — research digest (KB signals + external signals + scoping question)
  study-log.md    # type: study-log — append-only checkpoint log, same shape as source study logs
```

**Written by `/study`** — never unprompted. When you invoke `/study <concept-slug>` and the folder doesn't exist, the skill runs an initial research step (KB grep + web search), drafts `README.md`, asks you to confirm, then starts the first session which appends to `study-log.md`.

## README (type: concept) — the research digest

The foundational doc for a concept. Contains:

- **1-paragraph definition** — what this concept is, in plain English
- **KB signals** — wikilinks to existing sources / brainstorms / decisions / questions / comparisons that touch this concept
- **External signals** — curated web links with 1-line descriptions (papers, articles, talks, OSS projects outside the KB)
- **Scoping question** — the question studying this concept is meant to answer

Not opinionated. Opinions about how a concept applies to the project emerge in the `study-log.md` checkpoints or in `brainstorming/`.

## study-log.md (type: study-log)

Same shape as source study logs — see `study-sessions/README.md` for the checkpoint format and cross-reference rules. Frontmatter uses `concept:` pointer instead of `source:`.

## Promotion from source to concept

If a source study session keeps revealing cross-cutting themes, `/study` will **suggest** promoting the theme to a concept folder. User-prompted only — never automatic. Promotion creates `concepts/<new-slug>/` with a seeded `README.md` drawn from the relevant source study-log checkpoints.

## Growth rule

Per CONVENTIONS §"Growth rules" — `concepts/` clears `NEW_FOLDER_MIN_FILES=3` once 3 concept folders exist. Each concept folder itself is an entity folder (README + study-log), not subject to that rule.

## What concepts are NOT

- **Not glossary entries.** GLOSSARY.md handles vocabulary. Concepts are multi-session study targets.
- **Not decisions.** `decisions/` holds resolved architectural choices. A concept can inform a decision; the concept folder itself never resolves one.
- **Not synthesis material.** `synthesis/` holds architecture snapshots per product. Concepts are study scaffolding, not product state.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
