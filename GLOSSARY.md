# Glossary — vocabulary used across this KB

One-line definitions for terms used across the KB. For people, companies, programs and nicknames see [`ALIASES.md`](ALIASES.md); for what is true right now see [`STATE.md`](STATE.md). Internally-distinct terms get separate entries even when closely related (entity vs alias, source vs reference). Update on demand — not append-only.

---

## Architecture vocabulary

<!-- AUTOGEN:product-oneliner — source: newest synthesis/ one_liner: — edit there, run scripts/propagate-oneliner.py -->
- **Your Product** — One-line current framing of what you're building. This block is GENERATED from the `one_liner:` field of your newest `synthesis/` snapshot — do not hand-edit it; edit the synthesis and run `scripts/propagate-oneliner.py` (or `/kb-synthesize`). Until you write a synthesis with a `one_liner:`, this placeholder stays.
<!-- /AUTOGEN:product-oneliner -->
- **project-kb** — The OSS framework: a closed-loop, AI-native knowledge base scaffold for startups (and other small organizations) to capture, refine, and act on their own knowledge.
- **Closed-loop** — Capture → classify → refine → cite → decide → act all happen inside the same repo. No external SaaS in the critical path; the KB is the system of record.
- **AI-native** — Designed for agent operation as a first-class user. Frontmatter, indexes, skills, and conventions exist so an LLM can navigate, write, and cite the KB without scraping or guessing.
- **KB** — This knowledge base. A git repo of markdown + frontmatter + indexes + skills; both human-readable and agent-readable.
- **Schema-as-contract** — `schema/kb-schema.yaml` drives validators, templates, and (eventually) specialized agents. Single source of truth for what a "valid" entry looks like.
- **Single-writer rule** — Only one agent writes to the KB at a time, enforced via `runs/.lock`. Browser-tool operations count as writes.

## KB-management terms

- **STATE / ALIASES** — The two always-loaded files imported by `CLAUDE.md`: current truth about the project (with an `as-of:` date that lint requires), and shorthand → canonical name → hub file (parsed by `scripts/kb-prompt-lookup.py`). Updated in the same session as any write that changes what is true.
- **Rules files** (`.claude/rules/`) — Native Claude Code rule files that hold retrieval, writing, drafting and framing rules. Unscoped ones are always loaded; ones with `paths:` frontmatter load only when a matching content file is read.
- **Hub** — An entity-folder `README.md` that states current truth for a customer, program or project and lists the current version of each related doc.
- **AGENT-GUIDE** — The routing file that answers "where does X go?" and "which skill for Y?" Distinct from CONVENTIONS (rules) and INDEX.md files (auto-generated content listings).
- **Product track** (`product:`) — Frontmatter field declaring which product or workstream a file belongs to. Configure the allowed values in `schema/kb-schema.yaml` to match your org.
- **Strategic thread** (`strategic-thread:`) — Orthogonal frontmatter tag for cross-cutting initiatives (e.g. fundraising, gtm, oss). Cross-folder rollup is not auto-generated; use `grep -l 'strategic-thread:.*<name>'` for a given thread.
- **Supersedes** (`supersedes:`) — Explicit pointer to the file this one replaces. Forms the semantic chain; `git log --follow` gives the syntactic.
- **Back-stamp** — The other half of a supersede: in the same commit, the old file gets `status: superseded`, `superseded_by:` and a `> ⚠️ Superseded by [[...]]` banner. `kb-lint` rejects a `supersedes:` whose target is not back-stamped, and the INDEX tags the old entry `[superseded]`.
- **Transcript line link** (`[T:NN]`) — A citation from meeting notes into the verbatim transcript in `raw/transcripts/`, written `[T:NN](../raw/transcripts/<file>.md#LNN)`. Safe only because transcripts are never edited after filing.
- **Decision status** (`decision_status:`) — Comparisons only: `considered | adopted | rejected | borrowed-partial`. Rolls competitor/option piles up into positioning.
- **Confidence** (`confidence:`) — `high | medium | low | uncertain`. Required on synthesis, comparisons, and decisions (anti-sycophancy).
- **Entity folder** — Pattern where a subject (competitor, advisor, customer, team member) gets its own subdirectory with `README.md` (current truth) + dated event files (timeline). Promoted from a flat file when content grows or events accumulate.
- **Cite, don't copy** — Principle: link to authoritative content via wikilinks rather than duplicating it. The KB is an overlay; duplicated text rots.
- **Promotion path** — `questions/` → `research-dispatches/` → `decisions/` → `synthesis/`. Content moves up as it formalizes.

## KG primitives

- **Entity** — A first-class thing in the KB (person, company, product, deal, etc.). Has its own file (or folder) and frontmatter.
- **Alias** — An alternative name for an entity that resolves to the canonical entity page (e.g. "Acme Co." → "Acme").
- **Citation** — A pointer from a KB fact back to the source document + location. Preserved across derived content.
- **Wikilink** — `[[path/to/file]]` — markdown cross-reference between KB files. Three-tier citation format: whole-doc, section-precise, quote-precise.
- **Entity merging** — Process of detecting that two entries refer to the same real-world thing and consolidating them.

## Skills + scripts vocabulary

- **Skill** — A Claude-invocable command (e.g. `/add-entry`). Lightweight pointer to rules + steps; never duplicates CONVENTIONS.
- **Progressive disclosure** (Anthropic) — Skills design pattern: name + description always loaded (~100 tokens each); skill body loads only on invocation. Lets you ship many skills cheaply.
- **Lint hook** — `scripts/kb-lint.py` invoked by `scripts/hooks/pre-commit` (enabled via `core.hooksPath`) — validates frontmatter against `schema/kb-schema.yaml` and checks links/references on every commit.

## Named entities — canonical names

Use the full canonical name every time, in every file and in every draft (email, application, deck, chat). Shortened forms drift into outward-facing text and read as sloppy to the people being named. Add one entry per entity whose short form is ambiguous; nicknames and acronyms go in `ALIASES.md`. Optionally add a matching `NAME_RULES` row in `scripts/kb-lint.py` so lint warns on the short form.

- **Example Co** *(DEMO — replace)* — Never bare "Example": that is a different word, not a nickname. "ExCo" is acceptable internal shorthand, never in external text.

## External patterns we've borrowed

- **Three-layer model** (Karpathy) — `/raw/` (inputs) → `/wiki/` (compiled) → `/schema/` (contract). Mirrored here as `sources/` → compiled entries → `schema/`.
- **Compiled-truth + dated timeline** (Garry Tan, GBrain) — Entity README holds current truth and is rewritten as it changes; dated sibling files form an append-only evidence trail. Applied here as the entity-folder pattern.
- **Counter-arguments / data-gaps / confidence** (Shannon Holmberg, LLM-wikid) — Anti-sycophancy sections required on decision-carrying files.
- **Anti-cramming / anti-thinning** (farzaa) — Rules preventing files from growing too large or too small. Enforced in CONVENTIONS §"Growth rules."
