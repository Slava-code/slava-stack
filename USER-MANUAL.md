# User Manual — project-kb

Practical quickstart for humans working with this KB. Not the rulebook (that's `CONVENTIONS.md`); not the routing table (that's `AGENT-GUIDE.md`). This is "how do I actually use the thing."

---

## What this KB is

A git-backed knowledge base for a startup project — research, decisions, competitors, architecture, customer interviews, strategy, fundraising, team, advisors. Everything that matters at the *company* level sits here.

Most work happens inside Claude Code (the CLI / desktop app). Claude does the writing; you steer it with skills.

This reference implementation is public; your fork will typically be a private repo you clone into your dev tree.

---

## First-time setup on a new machine

This section is structured so an agent (Claude Code, or similar) can walk a new contributor through it — or execute the safe steps itself.

### Prerequisites

Install these first. If any is missing, the later steps will fail.

- **git** + **gh CLI** (`brew install gh`, then `gh auth login` — needs repo access)
- **Python 3** with **PyYAML** (`python3 -m pip install pyyaml`) — used by lint + generator
- **Claude Code** — desktop app or CLI; skills in this repo are Claude-specific

### Clone + install hooks

```bash
# Pick any parent directory you like.
git clone <your fork> project-kb
cd project-kb
bash scripts/install-hooks.sh                    # installs pre-commit hook (required)
```

**About the hooks** — git hooks live in `.git/hooks/` which is NOT tracked by git (by design). The committed hooks in `scripts/hooks/` are the source of truth; `install-hooks.sh` copies them into `.git/hooks/` and makes them executable. Each clone needs this step **once**. See "Pre-commit hooks" section below for what they enforce.

**Re-run `install-hooks.sh` whenever** `scripts/hooks/*` is updated upstream (git pull brings in new hook content, but existing `.git/hooks/*` is stale until you re-copy). If `python3 scripts/rebuild-indexes.py --check` exits 0 but your commits don't run it, your local hook is stale.

### Shell aliases (optional but recommended)

```bash
# Expand ~ so the alias uses an absolute path (the alias won't expand ~ at call time).
kb_path="$HOME/path/to/project-kb"
echo "alias kbdrop=\"$kb_path/scripts/kb-drop.sh\"" >> ~/.zshrc
echo "alias kbprocess=\"$kb_path/scripts/kb-process.sh\"" >> ~/.zshrc
source ~/.zshrc
```

- `kbdrop` — quick-capture a drop to inbox from any terminal
- `kbprocess` — trigger `/kb-process-inbox` via Claude Code (no need to cd + claude manually)

### Optional: `SOUL.md` for voice + active-user config

`SOUL.md` at the repo root is **gitignored** — personal to each machine. It controls:
- **Conversational tone** — how Claude talks to *you* (not how it writes files)
- **Active user slug** — a single line `Active user: <your-slug>` tells Claude which `team/<slug>/` preferences and voice corpus to load for your session

Skip if you only use this KB programmatically. See `CLAUDE.md` for the format.

### Verify your setup

Run these — all three should succeed:

```bash
python3 scripts/kb-lint.py              # "kb-lint: OK (N checked, M exempt)"
python3 scripts/rebuild-indexes.py --check   # exits 0 (no output = clean)
ls .git/hooks/pre-commit                # file exists, executable
```

If the lint fails with "PyYAML missing" → `python3 -m pip install pyyaml`.
If `--check` exits 1 → your working tree has edits that haven't been regenerated; run `python3 scripts/rebuild-indexes.py` and commit the regenerated `INDEX.md` files.
If the hook is absent → re-run `bash scripts/install-hooks.sh`.

### Tell an agent to set this up

If you hand the repo to Claude Code or another agent, the self-contained instruction is: *"Walk the 'First-time setup' in `USER-MANUAL.md`. Ask me before running anything that touches `~/.zshrc` or requires auth (`gh auth login`). Everything else inside the repo is fine to run."*

---

## Activating the skills

Skills live inside the repo at `.claude/skills/`. They activate **when you run Claude Code from the KB directory**:

```bash
cd project-kb
claude
```

From there, all `/kb*`, `/add-entry`, `/drop`, `/add-todo`, `/write-as`, etc. are available. Running Claude Code from a parent directory won't have them loaded.

---

## Daily tasks

### 1. I have a thing to capture but can't think about it now

```bash
kbdrop "quick thought or research topic"                       # content drop
kbdrop "https://github.com/foo/bar"                            # URL drop, kind auto-set from host
kbdrop "https://x.com/a" "https://linkedin.com/b"              # 2 drops, one per arg
kbdrop "https://x.com/foo — my take: why this matters is ..."  # URL + note on one drop
```

**Each quoted arg = one drop.** If an arg starts with `http(s)://`, the URL goes into `source_url` and the kind (`x-post`, `linkedin-post`, `url`) is inferred from host. Anything after the URL on the same arg becomes attached commentary. Separate quoted args never cross-bundle — to keep a URL and a note together, put them in the **same** quoted string.

Creates timestamped file(s) in `inbox/`. Auto-commits + pushes.

Or, if you're already inside Claude Code: `/drop <content>`.

### 2. I want to process my inbox

From any terminal:

```bash
kbprocess                   # drain all drops; groups near-duplicate URLs into one task
kbprocess <slug>            # process one specific drop
```

(Equivalent to opening Claude Code inside the KB dir and running `/kb-process-inbox`.)

Walks each group of drops sequentially, each handled by a fresh subagent (keeps context clean). Near-duplicate drops that share a URL are merged into ONE entry — not N redundant ones. LinkedIn / X drops use Chrome extension (respects single-writer rule — never parallel).

### 3. I want to add a specific thing

```
/add-entry
```

Asks you what kind of content (source, comparison, decision, interview, etc.), copies the right template from `schema/templates/`, fills frontmatter with you, commits with a proper prefix, pushes.

### 4. I have a deadline to remember

```
/add-todo
```

Prompts for title, deadline, priority, related entities.

### 5. What do I need to do today?

```
/deadlines
```

Subagent reads only frontmatter from `todos/*.md` (cheap — doesn't bloat context), returns items due today + overdue + pending. User-invoked — won't surprise-run every session.

### 6. I completed a todo

```
/complete-todo <slug>
```

Moves file to `todos/completed/`, sets `completed_at`, and auto-appends a one-line entry to each `related:` entity file's timeline (no permission prompt). So `/complete-todo 2026-04-20-email-advisor` adds a line to the matching `advisors/<advisor-slug>/README.md`.

### 7. I want an audit of the KB's health

```
/kb-audit
```

Checks broken citations, stale `raw` drafts, oversized files, orphan files, `considered` comparisons that never got decided, etc. Writes a report to `runs/YYYY-MM-DD-audit.md`.

### 8. Time for a fresh architecture snapshot

```
/kb-synthesize track-a
/kb-synthesize track-b
```

Rolls up all material written for the given product track since the last synthesis, writes new dated file with `supersedes:` frontmatter. The generator regenerates INDEX.md; the prior file stays in the folder (with its description) until archived.

---

## Navigating the KB as a human

| If you want... | Start at |
|---|---|
| High-level overview | `CLAUDE.md` |
| Current architecture | most recent file in `synthesis/` for the product track you care about |
| Rules for contributing | `CONVENTIONS.md` |
| Routing / skills list | `AGENT-GUIDE.md` |
| Vocabulary | `GLOSSARY.md` |
| Content index | root `INDEX.md` + per-folder `INDEX.md` (auto-generated) |
| Per-persona reading path | `READING-GUIDES.md` |
| Scope boundaries | `LIMITS.md` |
| A specific folder's rules | `<folder>/INDEX.md` |

---

## Commit format

Every commit uses a folder-or-type prefix. See `CONVENTIONS.md` §"Commit convention" for the full table. Skills handle this automatically. If you're committing manually, match the pattern:

```
source: add 2026-04-17-<slug>
advisor: contact 2026-04-17-<slug>-email-sent
decision: add 2026-04-17-<slug>
inbox: drop 2026-04-17-090234-<slug>
```

`git log --oneline --grep='^advisor:'` filters by prefix.

---

## Pre-commit hooks

The pre-commit hook (installed via `scripts/install-hooks.sh`) runs two checks on every commit. Either failing blocks the commit.

**1. Frontmatter lint** (`scripts/kb-lint.py`)
Validates every staged `.md` file against `schema/kb-schema.yaml`. Catches:
- Missing required frontmatter fields for the file's `type:`
- Enum values outside the allowed set (status, product, confidence, etc.)
- Missing required body sections (e.g. `## Counter-arguments` on synthesis files)
- `description:` field longer than 120 chars or containing forbidden substrings (`[[`, `](http`)

Fix the content or update the schema — don't `--no-verify`. If the lint is wrong, that's a schema bug; edit `schema/kb-schema.yaml` (commit separately with `schema:` prefix).

**2. INDEX freshness check** (`scripts/rebuild-indexes.py --check`)
Verifies every auto-generated `INDEX.md` is in sync with the current `description:` frontmatter of its folder's children. If you edit a file's description but don't regenerate the indexes, the commit fails with:

```
kb-pre-commit: auto-generated INDEX.md files are stale.
  Fix: run `python3 scripts/rebuild-indexes.py` then `git add` the regenerated INDEX.md files.
```

The hook deliberately does NOT auto-write — silent modifications from hooks are a footgun. Run the regenerator yourself, stage the output, retry the commit.

**Stale-hook symptom.** If your commits pass but `rebuild-indexes.py --check` on a fresh clone exits 1, your local `.git/hooks/pre-commit` is out of date with the committed version. Re-run `bash scripts/install-hooks.sh`.

---

## Gotchas

- **Skills only load when Claude is run from inside the KB directory.** If your slash commands aren't appearing, check your CWD.
- **Single-writer lock.** Only one agent writes at a time. If a skill says "another agent is writing, retry later," and you're sure nothing else is running, `rm runs/.lock`.
- **LinkedIn / X content is login-walled.** Chrome extension only. One Chrome task at a time.
- **Don't commit by hand in the middle of a skill's work.** Skills handle staging, commit, push as a unit. Manual interleaving breaks the lock contract.
- **Dropping via `kbdrop` auto-commits.** The history gets noisy — that's expected. Filter with `git log --grep='^inbox:' --invert-grep` if you want a clean view excluding drops.

---

## Sharing this KB with a teammate

1. Add them to the GitHub repo as a collaborator (gh CLI: `gh repo view --web` then GitHub UI, or `gh api repos/<your-username>/<your-repo>/collaborators/<username> -X PUT`).
2. Point them at this file. They follow "First-time setup."
3. Add their profile to `team/<their-slug>/README.md` via `/add-entry` (type: team-member).

---

## Adopting this for your own project

This repo is a framework, not a finished product. To adopt it, do the following find-and-replace pass once — roughly an hour of mechanical work — and then it's yours.

**Repo + path.** Rename the cloned directory and the GitHub repo to whatever you call your project. Update the `kb_path=` line in the shell-alias snippet above.

**Schema enums** in `schema/kb-schema.yaml`:
- `enums.product` — replace `track-a / track-b / shared` with your real product tracks. Single-track projects can collapse to one value.
- `enums.strategic_thread` — replace the placeholder threads (`oss`, `gtm`, `fundraising`, etc.) with your actual cross-cutting initiatives.
- `enums.persona` — replace generic personas (`customer`, `user`, `stakeholder`) with the ones relevant to your domain.
- `enums.stage` — pipeline / lead stages relevant to your GTM motion.

After editing, run `python3 scripts/kb-lint.py` against any existing demo content — fix or delete entries that no longer satisfy the new enums.

**`team/founder-template/`** — copy this directory to `team/<your-slug>/` and fill in `README.md` (role, focus, context). If you want `/write-as` to work for you, also populate `team/<your-slug>/voice/` per the optional voice plugin.

**Demo content.** Each content folder (`sources/`, `comparisons/`, `decisions/`, etc.) ships with a small number of demo entries so the patterns are legible. Delete or archive them once your own entries exist.

**Optional voice plugin** under `plugins/voice/`. If you don't want `/write-as`, leave the directory alone — the skill simply won't trigger usefully without a configured corpus. To enable: follow the plugin README to build `team/<your-slug>/voice/style-card.md` + `reverse-prompts.md` from a corpus of the active user's own writing.

Commit each of these as a separate change with a clear prefix (`schema:`, `kb:`, `team:`) so the adoption diff stays scannable.

---

## Questions / issues

- Broken wikilink or failed lint you don't understand? Run `/kb-audit` first — it often tells you what's wrong.
- Want to add a new folder? `/kb-add-folder` — it enforces the growth rules.
- Unsure which skill fits your task? `/kb` lists them all with one-line purpose.
