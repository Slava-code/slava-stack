# slava-stack

A framework for running a startup's knowledge base inside [Claude Code](https://claude.com/claude-code), with agents as first-class readers *and* writers.

You talk to the agent in chat. It files what you hand it (a URL, a call transcript, a decision you just talked through) into a typed, git-tracked entry, lints it against a schema, regenerates the folder indexes, and pushes. There is no deferred-capture queue: `/add-entry` fetches, classifies and files in one step.

**Naming.** The GitHub repo is `slava-stack`. Inside the docs the framework calls itself `project-kb`, a placeholder you replace with your own project's name when you adopt it (see [Adapting it](#adapting-it-to-your-project)).

It is a framework, not a product. The skills, scripts, schema and rulebook are reusable as-is. The content folders ship nearly empty, with a few clearly marked DEMO files so the patterns are legible.

---

## What's inside

```
slava-stack/
├── CLAUDE.md            # always-loaded agent entry; @-imports STATE.md and ALIASES.md
├── STATE.md             # one screen of current truth, with an as-of: date (DEMO skeleton)
├── ALIASES.md           # shorthand → canonical name → file to open (DEMO rows)
├── CONVENTIONS.md       # the rulebook: frontmatter, growth rules, supersede rules, single-writer lock
├── AGENT-GUIDE.md       # routing: "where does X go?" and "which skill for Y?"
├── GLOSSARY.md          # vocabulary and credited external patterns
├── LIMITS.md            # what this KB deliberately does NOT capture
├── USER-MANUAL.md       # practical setup and daily use, for humans
├── READING-GUIDES.md    # per-persona entry paths
├── INDEX.md             # auto-generated top-level folder listing
│
├── .claude/skills/      # slash commands (/add-entry, /meeting, /kb-audit, ...)
├── .claude/rules/       # retrieval, writing, drafting and research-framing rules
├── .claude/settings.json# hooks: session status, prompt-time file lookup, WebFetch and deploy guards
├── scripts/             # lint, INDEX generator, fetchers, git hooks, session/prompt hooks
├── schema/              # frontmatter contract (kb-schema.yaml) and per-type templates
├── plugins/voice/       # OPTIONAL: /write-as, drafting in the active user's voice
│
└── <content folders>    # sources/, decisions/, meetings/, raw/, todos/, ... (see INDEX.md)
```

The dependency direction: skills cite `CONVENTIONS.md`, the schema enforces it, `INDEX.md` files are derived from frontmatter, and agents read in the order `CLAUDE.md` prescribes. Nothing duplicates anything else.

---

## Why it is built this way

Most "second brain" setups are read-mostly. An agent can browse and quote them, but adding the next entry still needs a human to pick a folder, write the frontmatter and update the index. These pieces make the agent a full participant:

1. **A current-truth layer.** `STATE.md` is one screen of what is true right now, each line pointing at its source file and carrying an `as-of:` date; `ALIASES.md` maps nicknames and transcription variants to canonical names and files. Both are always in context, so the agent starts from current facts instead of whichever old file a search surfaced first. A session-start hook flags `STATE.md` when dated files pile up behind it.
2. **A machine-checked schema** (`schema/kb-schema.yaml` + `scripts/kb-lint.py`). Required fields, enums and body sections per `type:`, broken `[[wikilinks]]`, supersede pairs that are not back-stamped, routing files pointing at missing paths, and a size budget for always-loaded files.
3. **Skills as the steering layer** (`.claude/skills/`). Each skill is a short pointer to the rules plus a step list, not a copy of the rulebook.
4. **Auto-generated `INDEX.md` files** (`scripts/rebuild-indexes.py`). One line per child, fed by frontmatter, tagged `[superseded]` / `[cancelled]` when stale. Cheap agent context that is always fresh.
5. **Old files say they are old.** A new version back-stamps the one it replaces; the lint checks it.
6. **Rationale is mandatory.** Decisions need `## Why` and `## What we're giving up`; syntheses need `## Counter-arguments` and `## Data gaps`. Anti-sycophancy by validator.
7. **Line-cited transcripts.** A call's verbatim transcript lives in `raw/transcripts/`; each claim in the meeting notes links to its line as `[T:NN](...#LNN)`.
8. **Secret scanning and immediate push.** The pre-commit hook runs gitleaks, the lint and the INDEX sync; the post-commit hook pushes. A single-writer lock (`runs/.lock`) keeps two agents from clobbering each other.

---

## Prerequisites

- **git** and **gh** (GitHub CLI, authenticated)
- **Python 3** with **PyYAML** (`python3 -m pip install pyyaml`): lint and INDEX generator
- **gitleaks**: the pre-commit hook refuses to commit without it
- **jq**: used by the guard hooks in `.claude/settings.json`
- **Claude Code** (CLI or desktop app)

On macOS: `brew install gh gitleaks jq`.

## Quick start

```bash
git clone https://github.com/<you>/<your-fork>.git project-kb
cd project-kb
bash scripts/install-hooks.sh                 # sets core.hooksPath to scripts/hooks
python3 scripts/kb-lint.py                    # should pass on a clean checkout
python3 scripts/rebuild-indexes.py --check    # exits 0 when indexes are current
claude
```

Skills load when Claude Code runs from inside the repo. Start with `/kb` if you are not sure which one to use. Full setup and daily use are in [USER-MANUAL.md](USER-MANUAL.md).

---

## Skills

Sixteen core skills ship in `.claude/skills/`:

| Skill | What it does |
|---|---|
| `/kb` | Chooser: lists every skill with a one-line purpose |
| `/add-entry` | File content now: source, comparison, decision, brainstorm, strategy, interview, experiment, advisor or team profile. Unread URLs are fetched and filed on the spot |
| `/meeting` | Save a call: verbatim transcript to `raw/transcripts/`, line-cited notes to `meetings/`, action items and outcomes propagated to todos and hubs |
| `/add-todo` | Add a todo, event or meeting; the filename date is the deadline |
| `/complete-todo` | Close a todo, move it to `todos/completed/`, log it on each related entity, update `STATE.md` if an outcome changed |
| `/deadlines` | What is due today and overdue (reads frontmatter only) |
| `/finance` | Log a transaction to `finances/ledger.csv` from a note, receipt or statement; dedups and confirms first |
| `/financial-summary` | Write a cash-flow summary for a period to `finances/summaries/` |
| `/kb-audit` | Health check: lint, stale drafts, oversized files, orphans, broken links, overdue todos, `STATE.md` age |
| `/kb-synthesize <track>` | New dated state snapshot for a product track, and refresh `STATE.md` from it |
| `/kb-promote <path>` | Move content along questions → research-dispatches → decisions → synthesis |
| `/kb-archive <path>` | Retire a fully superseded file to `archive/` and fix inbound links |
| `/kb-add-folder` | Add a top-level folder, enforcing the growth rules |
| `/study` | Start or resume a study session on a source or concept; appends a checkpoint |
| `/study-status` | Where you left off on a source or concept |
| `/study-unstudied` | Sources and concepts with no study log yet, by priority |

Plus one optional plugin:

| Plugin | What it does |
|---|---|
| `plugins/voice/` (`/write-as`) | Draft outbound text in the active user's voice from their corpus and a style card |

---

## What this is NOT

- **Not a hosted product.** The KB lives on your filesystem under git. No server, no database, no SaaS.
- **Not a generic note-taking app.** It is opinionated about how a startup's running knowledge is structured: entity hubs, decision records with explicit trade-offs, dated snapshots instead of append-only mega-files. See [LIMITS.md](LIMITS.md).
- **Not finished.** It is a snapshot of one team's working setup, published so others can fork it.

---

## External prior art

The KB remixes public ideas, credited inline where each shows up and collected in [GLOSSARY.md](GLOSSARY.md) under "External patterns":

- **Three-layer model** (`raw/` → compiled wiki → `schema/`): Andrej Karpathy's LLM Wiki
- **Compiled-truth plus dated-timeline entity pages**: Garry Tan's GBrain pages
- **Counter-arguments, data gaps and confidence as anti-sycophancy levers**: Shannon Holmberg's LLM-wikid
- **Anti-cramming and anti-thinning growth rules**: farzaa's KB conventions
- **Progressive disclosure for skills**: Anthropic's skill design

---

## Adapting it to your project

[USER-MANUAL.md, "Adopting this for your own project"](USER-MANUAL.md#adopting-this-for-your-own-project) walks the replacement list:

- the `project-kb` name, and the repo and directory names
- schema enums (`product: track-a | track-b | shared`, `persona`, `stage`, `strategic_thread`)
- `STATE.md` and `ALIASES.md` (replace the DEMO lines)
- `team/founder-template/` → your team
- the DEMO content in each folder
- the optional voice plugin, if you want `/write-as`

Roughly an hour of mechanical work.

---

## License

MIT. See [LICENSE](LICENSE).
