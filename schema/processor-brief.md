# Processor Brief — distilled rules for `/kb-process-inbox` subagents

**Purpose.** A single file that `/kb-process-inbox` subagents can read instead of re-discovering rules across `AGENT-GUIDE.md` + `CONVENTIONS.md` + `schema/templates/*` + folder `INDEX.md` files on every dispatch. The originals remain authoritative; when this brief conflicts with them, fix the brief.

**When to read this vs the originals.** If you are processing a single inbox drop end-to-end, this brief is enough. Read the originals if: (a) destination classification is non-obvious after consulting the table below; (b) you are touching a file type this brief does not cover (e.g. `experiments/`, `research-dispatches/`); (c) a rule here seems inconsistent with something you read elsewhere.

---

## 1. Flow (in order)

1. **Acquire the lock.** `echo "<purpose> $$" > runs/.lock`. If the file exists with a different token, abort with a clear message. Do NOT overwrite another writer's lock.
2. **Read the drop fully** — the captured URL, source_kind, any commentary.
3. **Fetch the external content.** `WebFetch` for regular URLs. `mcp__claude-in-chrome__*` for login-walled (x.com, linkedin.com). Never parallel Chrome tasks.
4. **Verify upstream claims the drop made.** Venue, author affiliations, headline numbers, framing — cross-check against the fetched content. Drop authors (incl. research-sweep subagents) reliably over-state; the processor is the first corrective layer.
5. **Classify destination** (§2).
6. **Write entries** from the matching templates in `schema/templates/`. Fill frontmatter strictly (§3). Required body sections per type (§4). Cross-link (§5).
7. **Update CATALOG.md** — one line per new file. Match the section style of existing entries.
8. **One commit** — staging: new files + CATALOG edit + inbox drop deletion. Message format (§7). Trailer required.
9. **Push.** If offline, note it to parent; commit is local.
10. **Release the lock.** `rm -f runs/.lock`.
11. **Return one line** to parent: `<N> drops → <destination path(s)>`. Optionally append classification tensions / overclaim flags.

---

## 2. Destination classification

From `AGENT-GUIDE.md §"Where does this piece of content go?"`. Most-common processor outcomes first.

| The drop is... | Primary entry | Companion? |
|---|---|---|
| Academic paper / preprint with direct architectural bearing | `sources/YYYY-MM-DD-<slug>.md` | `brainstorming/YYYY-MM-DD-<slug>-in-<project>.md` — our take |
| Academic paper / preprint with thin bearing (survey, landscape, tangential) | `sources/...` only | Skip brainstorm — don't force relevance |
| Vendor product page, tool, repo (with implications) | `sources/...` + `brainstorming/...-vs-<project>.md` | Same pair pattern |
| Competitor analysis (head-to-head, we care about positioning) | `comparisons/YYYY-MM-DD-<slug>.md` (flat) or `.../<slug>/` (multi-chapter >300 lines) | — |
| Op-ed / article / blog post (argues a position) | `sources/...` + optional `brainstorming/...` | Brainstorm iff the position conflicts with or extends ours |
| LinkedIn / X post with content worth saving | `sources/...` | Brainstorm only if there's architecture implication; many are pointer-only |
| Research question the drop implicitly opens | `questions/YYYY-MM-DD-<slug>.md` (optional, on top of source) | — |

**Source + brainstorm pair convention** — `AGENT-GUIDE.md §"Source + brainstorm pair"`. Same date, sibling slugs (`-in-<project>` or `-vs-<project>`), cross-linked. Sources stay factual; brainstorms carry opinions.

**No-brainstorm default for surveys.** A paper that describes the landscape gets a `sources/` digest only unless its evaluation-gaps / methodology section surfaces concrete actionable project work.

**Multi-drop merge.** If ≥2 inbox drops share a URL (after tracker-stripping), produce ONE pair with all distinct commentary angles merged — not N duplicate files.

---

## 3. Frontmatter (minimal, processor-facing)

Every file gets YAML frontmatter per `schema/kb-schema.yaml`. For the source + brainstorm pair:

```yaml
# sources/YYYY-MM-DD-<slug>.md
---
title: "<paper title, canonical>"
type: source
product: track-a | track-b | shared
source: "<arxiv/blog/repo URL>"
date_found: YYYY-MM-DD
tags: [...]
status: raw
---
```

```yaml
# brainstorming/YYYY-MM-DD-<slug>-in-<project>.md
---
title: "<paper-name> vs/in <project> — <angle>"
type: brainstorm
product: track-a | track-b | shared
date_found: YYYY-MM-DD
tags: [...]
status: raw
---
```

`product:` selection — pick ONE of your project's tracks as defined in `schema/kb-schema.yaml` (`enums.product`). Default to `shared` when the paper is architecture-general / spans tracks.

Set `status: raw` on creation. Subsequent reviewers bump to `reviewed` / `incorporated`.

---

## 4. Required body sections

**Source entry** (`type: source`) — no opinions. Factual digest. Template sections: What it is / How it works / Key facts / Source links.

**Brainstorm entry** (`type: brainstorm`) — template sections: Problem or question / Options considered (A, B, C…) / Leaning or decision / Open questions / Related.

**Anti-sycophancy requirements** — from `CONVENTIONS.md §"Required body sections"`:
- Brainstorms SHOULD carry explicit `## Counter-arguments` and `## Data gaps` subsections (borrowed from synthesis rule; processor-added convention for this batch). Counter-arguments = what would flip the leaning; Data gaps = what we don't know that matters.
- Synthesis files MUST have them (hard rule).
- Decisions MUST have `## Why` + `## What we're giving up`.
- Comparisons MUST have `## Decision` with `decision_status`.

**Substrate discipline for papers.** When the drop commentary (or my own first instinct) frames a paper as "validates our approach" or "applies directly," run the three-clause check before writing the brainstorm:
1. *Surface similarity* — what shared vocabulary invites the comparison? Name it.
2. *Substrate difference* — where does the mechanism diverge? (weights vs corpus, training vs inference, gradient vs prompt, model-vs-operator vs user-as-operator, extracted vs authored relations)
3. *Actual bearing* — after 1+2, is there a real claim left?
If clause (3) collapses, the brainstorm's leaning should be "file + landscape only," not "architecture validated." See `memory/feedback_research_sweep_framings.md` for the pattern this guards against.

**Convergence tagging.** When a brainstorm notes "this is the Nth time X has surfaced" — i.e. the same deferred action, open question, or thread keeps recurring across multiple brainstorms — add a `convergence:` list to the brainstorm's frontmatter with a short slug-cased tag per theme:

```yaml
convergence: [eval-harness-build, graph-db-threshold]
```

Pick tags that future processors will independently arrive at (prefer the recurring phrase already used in brainstorm bodies). `scripts/kb-convergence-scan.py` tallies tags across brainstorming/; `/kb-audit` surfaces any tag on ≥3 brainstorms as a promotion candidate. Tagging is how a cross-drop pattern escapes the individual brainstorm — without it, the observation stays buried.

---

## 5. Citation + cross-linking

Three-tier wikilinks from `CONVENTIONS.md §"Citation discipline"`:

| Tier | Form | Use |
|---|---|---|
| Whole doc | `[[sources/2026-04-18-foo]]` | Pointing at a concept |
| Section-precise | `[[sources/2026-04-18-foo]] §"Key facts"` | Default; where a section fits in a reader's context |
| Quote-precise | `[[sources/2026-04-18-foo]] §"Key facts" ("the exact claim")` | When the reader must see the verbatim line |

**No line-range citations** — they rot silently. Section headings only for any self-firing artifact (skills, hooks, scripts, memory, brainstorm cross-refs).

**Cross-project wikilinks** use relative paths: `[[../<sibling-repo>/...]]` when this KB sits alongside other repos that hold authoritative docs.

**Mandatory cross-links when processing a paper drop:**
- Source ↔ brainstorm (each cites the other).
- Brainstorm → any prior brainstorms in the same thread (find via CATALOG grep by topic keywords).
- If the paper extends / supersedes a prior entry, add `supersedes:` frontmatter on the new file.

---

## 6. Inference discipline (copy from `CLAUDE.md`)

- Preserve hedges. `e.g.`, `possible`, `target`, `exploring` are load-bearing; don't collapse them.
- Who is the actor of a claim? A "we need X" dependency describes US, not the counterparty.
- Cite when it matters. `file.md §"Section"` beats confident paraphrase when the reader might act.
- When unsure, quote. A short verbatim + pointer beats a summary that inflates.
- Absence ≠ denial. "The KB doesn't say" is the right frame when the KB is silent.

For external-paper processing specifically: the paper's hedges are ALSO load-bearing. Anthropic-style alignment papers are usually scrupulously hedged; strip a hedge and the finding flips from "we observed X under conditions Y" to "X is true." Preserve the original paper's caveats in the source digest verbatim or near-verbatim.

---

## 7. Commit + return format

**Commit message** (one commit per drop processed):
```
inbox: process <slug> → sources/ + brainstorming/

<optional body enumerating distinct input drops if merged>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

For singleton drops the body is usually empty. For merged groups, enumerate the input drop slugs in the body.

If the drop is discarded (low-signal, unverifiable, duplicate), commit with:
```
inbox: discard <slug> — <reason>

Co-Authored-By: ...
```

**Return to parent** — one line, specific: `1 drop → sources/<full-path> + brainstorming/<full-path>`. Optionally append a short list of tensions / corrections / overclaim flags caught during processing — the parent aggregates these across drops to surface patterns.

**Inbox-drop provenance — do NOT wikilink.** When writing the source entry's provenance section, it is tempting to cite the inbox drop via `[[inbox/YYYY-MM-DD-HHMMSS-slug]]`. Don't. The drop file is deleted in the same commit that creates the source entry, so the wikilink rots the instant the commit lands. Provenance lives in the git log — the `inbox: process <slug>` commit is the authoritative pointer. If you want to preserve the drop's raw content (drop author's framing, captured URL, topic tag) for the record, paste a short backtick-fenced quote of the drop body in the source's "Provenance" section. Cite the commit by short SHA if precision matters. A 2026-04-18 audit found 23 source entries with dangling `[[inbox/...]]` wikilinks from exactly this mistake — treat it as a non-obvious failure mode.

---

## 8. Lock + concurrency

**Single-writer rule** (`CONVENTIONS.md §"Single-writer rule"`). One agent writes at a time; Chrome extension ops count as writes (single Chrome session).

- Acquire first (`runs/.lock`), release last (`rm -f runs/.lock`).
- If lock held by a different token, abort cleanly — do not block.
- Manual override: `rm runs/.lock` if a previous session died (operator action, not processor action).
- Never parallelize subagent processing; the lock serializes by design.

---

## 9. What this brief deliberately omits

This brief covers the `/kb-process-inbox` path for **external papers / articles / posts becoming `sources/` (+ optional `brainstorming/`) entries**. It does NOT cover:
- `experiments/` writes (ask CONVENTIONS)
- `decisions/` writes (ask CONVENTIONS)
- `synthesis/` rolls (ask `/kb-synthesize`)
- `comparisons/` multi-chapter splits (ask `/kb-add-folder` or CONVENTIONS)
- Entity-folder READMEs (advisors, team, discovery)
- Todo handling (`/add-todo` + `/complete-todo`)

If the inbox drop is one of those types, read the full originals.
