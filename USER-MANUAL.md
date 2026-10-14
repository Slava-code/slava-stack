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
- **gitleaks** (`brew install gitleaks`) — the pre-commit hook scans every commit for secrets and refuses to commit without it
- **jq** (`brew install jq`) — used by the PreToolUse hooks in `.claude/settings.json`
- **Claude Code** — desktop app or CLI; skills in this repo are Claude-specific

### Clone + install hooks

```bash
# Pick any parent directory you like.
git clone <your fork> project-kb
cd project-kb
bash scripts/install-hooks.sh                    # enables the tracked hooks (required)
```

**About the hooks** — the committed hooks in `scripts/hooks/` are the source of truth. `install-hooks.sh` sets `git config core.hooksPath scripts/hooks`, so git runs the tracked files directly; a `git pull` that updates a hook takes effect immediately, with nothing to re-copy. `core.hooksPath` is per-clone config, so each clone needs this step **once**. See "Pre-commit hooks" section below for what they enforce.

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
git config core.hooksPath               # prints "scripts/hooks"
gitleaks version                        # gitleaks is installed
```

If the lint fails with "PyYAML missing" → `python3 -m pip install pyyaml`.
If `--check` exits 1 → your working tree has edits that haven't been regenerated; run `python3 scripts/rebuild-indexes.py` and commit the regenerated `INDEX.md` files.
If `core.hooksPath` prints nothing → re-run `bash scripts/install-hooks.sh`.

### Tell an agent to set this up

If you hand the repo to Claude Code or another agent, the self-contained instruction is: *"Walk the 'First-time setup' in `USER-MANUAL.md`. Ask me before running anything that touches my shell profile or requires auth (`gh auth login`). Everything else inside the repo is fine to run."*

---

## Activating the skills

Skills live inside the repo at `.claude/skills/`. They activate **when you run Claude Code from the KB directory**:

```bash
cd project-kb
claude
```

From there, all `/kb*`, `/add-entry`, `/add-todo`, `/meeting`, etc. are available (plus `/write-as` if you installed the optional voice plugin). Running Claude Code from a parent directory won't have them loaded.

---

## Daily tasks

### 1. I want to add something — or save it for later

```
/add-entry
```

Asks you what kind of content (source, comparison, decision, interview, etc.), copies the right template from `schema/templates/`, fills frontmatter with you, commits with a proper prefix, pushes. Also the path for "save this for later": hand it a URL you haven't read and the agent fetches, classifies, and files it now — there is no deferred-capture queue.

### 2. I have a deadline to remember

```
/add-todo
```

Prompts for title, deadline, priority, related entities.

### 3. What do I need to do today?

```
/deadlines
```

Subagent reads only frontmatter from `todos/*.md` (cheap — doesn't bloat context), returns items due today + overdue + pending. User-invoked — won't surprise-run every session.

### 4. I completed a todo

```
/complete-todo <slug>
```

Moves file to `todos/completed/`, sets `completed_at`, and auto-appends a one-line entry to each `related:` entity file's timeline (no permission prompt). So `/complete-todo 2026-04-20-email-advisor` adds a line to the matching `advisors/<advisor-slug>/README.md`.

### 5. I want an audit of the KB's health

```
/kb-audit
```

Checks broken citations, stale `raw` drafts, oversized files, orphan files, `considered` comparisons that never got decided, etc. Writes a report to `runs/YYYY-MM-DD-audit.md`.

### 6. Time for a fresh architecture snapshot

```
/kb-synthesize track-a
/kb-synthesize track-b
```

Rolls up all material written for the given product track since the last synthesis, writes new dated file with `supersedes:` frontmatter. The generator regenerates INDEX.md; the prior file stays in the folder (with its description) until archived.

### 7. I want to track money in/out

```
/finance
```

Log a transaction into `finances/ledger.csv` — three ways: just tell it ("$40 to Example SaaS today"), hand it a receipt screenshot, or point it at a bank statement file. It parses the fields, categorizes, checks for duplicates / reconciles against what's already logged, and **confirms with you before writing**. Don't commit a raw bank statement — point `/finance` at a local file; it redacts account numbers before storing anything.

For a period summary: `/financial-summary 2026-05` (writes a formatted breakdown to `finances/summaries/`). One-off questions like "how much did we spend on SaaS in May?" need no skill — just ask.

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
todo: add 2026-04-17-<slug>
```

`git log --oneline --grep='^advisor:'` filters by prefix.

---

## Pre-commit hooks

The pre-commit hook (enabled via `scripts/install-hooks.sh`) runs three steps on every commit. A failing check blocks the commit.

**1. Secret scan** (`gitleaks git --staged`)
Scans the staged changes with gitleaks' built-in ruleset plus the generic extras in `.gitleaks.toml`. A hit refuses the commit — remove the secret (secrets never belong in the working tree) or, for a genuine false positive, add an allowlist entry to `.gitleaks.toml`. If gitleaks is not installed the hook fails with an install hint; `KB_SKIP_GITLEAKS=1` bypasses the scan (not advised).

**2. Frontmatter + reference lint** (`scripts/kb-lint.py`)
Validates every staged `.md` file against `schema/kb-schema.yaml`. Catches:
- Missing required frontmatter fields for the file's `type:`
- Enum values outside the allowed set (status, product, confidence, etc.)
- Missing required body sections (e.g. `## Counter-arguments` on synthesis files)
- `description:` field longer than 120 chars or containing forbidden substrings (`[[`, `](http`)
- Broken `[[wikilinks]]`, and `supersedes:` pointers whose target lacks `status: superseded` + `superseded_by:`
- Routing files (CLAUDE.md, AGENT-GUIDE.md, `.claude/rules/`, skill descriptions) pointing at missing paths, missing `/skills` or superseded files

Fix the content or update the schema — don't `--no-verify`. If the lint is wrong, that's a schema bug; edit `schema/kb-schema.yaml` (commit separately with `schema:` prefix).

**3. INDEX auto-sync** (`scripts/rebuild-indexes.py`)
Rebuilds every auto-generated `INDEX.md` from the current `description:` frontmatter of its folder's children, then stages any that changed — so a stale index can never block a commit. If you edit a file's description, the matching index is regenerated and folded into the same commit automatically; no manual regen step.

This is the one place the hook deliberately *does* auto-write. INDEX.md files are derived purely from frontmatter — nobody hand-reviews them, so re-staging them isn't the "silent write of unreviewed intent" footgun the rest of the hook guards against; it's keeping a derived artifact in sync. Source files are never auto-staged. (It also kills a force-push trap: with the old `--check`-and-reject, a forgotten index meant commit → amend, and since post-commit already pushed, the amend needed a force-push.)

**Hooks-not-running symptom.** If your commits pass but `rebuild-indexes.py --check` on a fresh clone exits 1, the hooks are not enabled in your clone (`git config core.hooksPath` is empty). Run `bash scripts/install-hooks.sh`.

---

## Gotchas

- **Skills only load when Claude is run from inside the KB directory.** If your slash commands aren't appearing, check your CWD.
- **Single-writer lock.** Only one agent writes at a time. If a skill says "another agent is writing, retry later," and you're sure nothing else is running, `rm runs/.lock`.
- **LinkedIn / X content is login-walled.** WebFetch is blocked there by a hook; the main agent uses a logged-in browser tool (subagents report "could not fetch"). One browser task at a time, and it takes the lock. See `AGENT-GUIDE.md` § "Login-walled content".
- **Don't commit by hand in the middle of a skill's work.** Skills handle staging, commit, push as a unit. Manual interleaving breaks the lock contract.

---

## Sharing this KB with a teammate

1. Add them to the GitHub repo as a collaborator (gh CLI: `gh repo view --web` then GitHub UI, or `gh api repos/<your-username>/<your-repo>/collaborators/<username> -X PUT`).
2. Point them at this file. They follow "First-time setup."
3. Add their profile to `team/<their-slug>/README.md` via `/add-entry` (type: team-member).

---

## Adopting this for your own project

This repo is a framework, not a finished product. To adopt it, do the following find-and-replace pass once — roughly an hour of mechanical work — and then it's yours.

**Repo + path.** Rename the cloned directory and the GitHub repo to whatever you call your project.

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
