---
type: folder
description: "Closed-loop, AI-native knowledge base framework for running a startup inside Claude Code — skills, schema, conventions"
---

# project-kb

A reference implementation for running a startup's knowledge base **closed-loop** and **AI-native** inside Claude Code.

- **Closed-loop** — the chat → drop → process → digest → cite cycle closes without anyone re-keying anything. Drop a URL in any terminal; an agent fetches it, classifies it, writes the structured entry, commits, pushes.
- **AI-native** — agents are first-class readers *and* writers. The schema is a contract they check at commit time. Folder `INDEX.md` files are auto-generated agent context. A single-writer lock prevents two agents from clobbering each other. Skills (slash commands) are how humans steer the loop.

It is a framework, not a product. The skills, scripts, schema, and rulebook are reusable as-is. The content folders ship empty (with a few demo files so the patterns are legible). Adopt it by cloning, replacing the demo content, and renaming a handful of placeholders called out in [USER-MANUAL.md](USER-MANUAL.md).

---

## What's inside

```
project-kb/
├── CLAUDE.md            # T0 — always-loaded agent boot anchor
├── CONVENTIONS.md       # the rulebook: frontmatter, growth rules, single-writer rule
├── AGENT-GUIDE.md       # routing: "where does X go?" + "which skill for Y?"
├── GLOSSARY.md          # vocabulary
├── LIMITS.md            # what this KB deliberately does NOT capture
├── USER-MANUAL.md       # practical quickstart for humans
├── READING-GUIDES.md    # per-persona entry paths
├── INDEX.md             # auto-generated top-level folder listing
│
├── .claude/skills/      # 17 slash commands (/add-entry, /drop, /kb-audit, etc.)
├── scripts/             # validators, INDEX regenerator, fetchers, git hooks
├── schema/              # frontmatter contract + per-type templates
├── plugins/voice/       # OPTIONAL: write-as plugin (voice imitation per active user)
│
└── <content folders>    # sources/, brainstorming/, decisions/, etc. — ship empty
```

The dependency direction: **skills cite CONVENTIONS, schema enforces CONVENTIONS, INDEX files are derived from frontmatter, agents read everything in the order CLAUDE.md prescribes.** Nothing duplicates anything else.

---

## Why this exists

Most "second brain" systems are read-mostly. An agent landing in them can browse, search, and quote — but adding the next entry still requires a human picking a folder, writing the frontmatter, updating the index. The loop doesn't close.

A few things have to be in place for agents to be full participants:

1. **A schema that's machine-checked** (`schema/kb-schema.yaml` + `scripts/kb-lint.py`). Agents follow rules by reading the contract, not by intuiting from neighbors.
2. **Skills as the steering layer** (`.claude/skills/`). Each skill is a thin pointer to the rules + a step list — not a duplication of the rulebook. Slash commands let the human stay in chat instead of navigating folders.
3. **Auto-generated INDEX.md files** (`scripts/rebuild-indexes.py`). Every folder has a one-line description per child, fed by frontmatter. INDEX files are agent context — cheap to read, always fresh.
4. **A single-writer lock** (`runs/.lock`). Two parallel agents would otherwise stomp each other. The lock is taken by every write-capable skill and by every Chrome-extension session (login-walled fetches count).
5. **Frontmatter that names rationale, not just type.** `## Why` and `## What we're giving up` on every decision; `## Counter-arguments` and `## Data gaps` on every synthesis. The schema enforces these sections exist — anti-sycophancy by validator.
6. **Commits push immediately** (post-commit hook). No local-only buffering — every change reaches the remote before the next one starts. Makes the KB legible from `git log --oneline` and survives any single laptop dying.

---

## Quick start

```bash
git clone <your fork> project-kb
cd project-kb
bash scripts/install-hooks.sh         # installs pre-commit + post-commit hooks
python3 -m pip install pyyaml         # used by the lint
python3 scripts/kb-lint.py            # should pass on a clean checkout
```

Then open Claude Code from inside the directory:

```bash
claude
```

The 17 skills load automatically. Start with `/kb` if you're not sure which one to invoke.

Full setup (gh CLI, shell aliases, optional voice plugin, schema customization) is in [USER-MANUAL.md](USER-MANUAL.md).

---

## Core skills

| Skill | What it does |
|---|---|
| `/kb` | Skill chooser — lists every skill with a one-line purpose |
| `/drop` | Quick-capture content or a URL to the inbox (no classification yet) |
| `/add-entry` | Add a typed entry now — classifies, fills template, commits, pushes |
| `/kb-process-inbox` | Drain the inbox; each drop handled by a fresh subagent |
| `/kb-audit` | Health check — stale drafts, broken links, oversized files |
| `/kb-synthesize <track>` | Roll up an architecture snapshot for one product track |
| `/kb-promote <path>` | Move content along: questions → research-dispatches → decisions → synthesis |
| `/kb-archive <path>` | Retire fully-superseded content to `archive/` |
| `/kb-add-folder` | Add a new top-level folder; enforces growth rules |
| `/add-todo`, `/complete-todo`, `/deadlines` | Lightweight task layer with deadline-as-filename |
| `/study <source\|concept>` | Append-only checkpoint log per source or cross-cutting concept |
| `/study-status`, `/study-unstudied` | Read-only queries against the study system |

Plus one optional plugin:

| Plugin | What it does |
|---|---|
| `plugins/voice/` (`/write-as`) | Draft text in a configured user's voice from a corpus + style card |

---

## What this is NOT

- Not a hosted product. The KB lives on your filesystem under git. No server, no database, no SaaS.
- Not a generic note-taking app. It's opinionated about how a startup's running knowledge should be structured (entity folders, decision records with explicit `## Why` and `## What we're giving up`, dated snapshots over append-only mega-files, etc.). See [LIMITS.md](LIMITS.md) for what it deliberately does not try to do.
- Not a finished framework. It's a snapshot of one team's working setup, made public so others can fork it. The version in any given commit reflects what was useful when that commit was made.

---

## External prior art credited inside

The KB is a remix of public ideas. The places where a specific external pattern shows up are credited inline in the relevant doc:

- **Three-layer model** (`raw/` → compiled wiki → `schema/`) — Andrej Karpathy's LLM Wiki
- **Compiled-truth + dated-timeline entity folders** — Garry Tan's GBrain pages
- **Counter-arguments / Data gaps / confidence as anti-sycophancy levers on decision-carrying files** — Shannon Holmberg's LLM-wikid
- **Anti-cramming / anti-thinning growth rules** — farzaa's KB conventions
- **Progressive disclosure for skills** — Anthropic's skill design

Citations live in [GLOSSARY.md](GLOSSARY.md) §"External patterns".

---

## License

MIT. Use it, fork it, change anything. Attribution appreciated but not required.

---

## Adapting this to your project

[USER-MANUAL.md §"Adopting this for your own project"](USER-MANUAL.md) walks the find-and-replace list:

- Repo name (rename `project-kb` → whatever you call yours)
- Schema enums (`product: track-a | track-b | shared` → your real tracks; `persona`, `stage`, `strategic-thread` enums)
- `team/founder-template/` → your team
- Demo content under each content folder → your content
- Optional voice plugin under `plugins/voice/` if you want `/write-as`

Roughly one hour of mechanical replacement and then it's yours.
