# scripts/

Helper + validation scripts.

**Files:**
- `kb-lint.py` — validates frontmatter across all `*.md` files against `schema/kb-schema.yaml`, plus reference checks: broken `[[wikilinks]]`, `supersedes:` without the back-stamp on the old file, routing/config files (CLAUDE.md, AGENT-GUIDE.md, `.claude/rules/`, skill descriptions) pointing at missing paths, missing skills or superseded files, the always-loaded config size budget, and the `as-of:` line in `STATE.md` (when present). Files named on the command line get errors; a whole-repo sweep reports reference problems as warnings. Optional `NAME_RULES` warn on ambiguous short entity names. Called by the pre-commit hook; also invoked via `/kb-audit`.
- `rebuild-indexes.py` — regenerates every auto-generated `INDEX.md` from entries' `description:` frontmatter, prefixing currency tags (`[superseded]`, `[cancelled]`, `[archived]`, `[dead]`). `--check` exits 1 if any index is stale. Run by the pre-commit hook.
- `propagate-oneliner.py` — copies the canonical product one-liner from the newest `synthesis/` file into AUTOGEN blocks (e.g. GLOSSARY.md). `--check` verifies.
- `kb-convergence-scan.py` — tallies `convergence:` tags across `brainstorming/` to surface ideas ready for promotion.
- `kb-session-status.py` — SessionStart hook (`.claude/settings.json`): prints a short staleness report (STATE.md age if the KB keeps one, synthesis lag per track, overdue pending todos, days since the last audit). Read-only; silent on error.
- `kb-prompt-lookup.py` — UserPromptSubmit hook: lists up to 12 KB files most likely to answer the prompt, ranking superseded / older-version files down. Expands shorthand through `ALIASES.md` if present. Skips gitignored `private/` folders unless `KB_LOOKUP_INCLUDE_PRIVATE=1`. Also usable by hand: `scripts/kb-prompt-lookup.py "<terms>"`.
- `arxiv-fetch.sh`, `yt-fetch.sh`, `github-deep-fetch.sh` — dedicated fetchers that write to `runs/fetches/<slug>.txt` for `/add-entry` to cite.
- `install-hooks.sh` — sets `git config core.hooksPath scripts/hooks` so the tracked hooks run directly (no copies to go stale). Run once per fresh clone.
- `hooks/pre-commit` — secret scan of staged changes (`gitleaks git --staged`, rules in `.gitleaks.toml`), `kb-lint.py` on staged `*.md`, then rebuilds and stages `INDEX.md` files. Probes multiple Python install locations for one with PyYAML; robust against git's stripped-env hook execution.
- `hooks/post-commit` — pushes to the tracked upstream after every commit.

**Dependencies:**
- Python 3 + PyYAML (anaconda base usually has it; otherwise `python3 -m pip install pyyaml`)
- gitleaks (`brew install gitleaks`; the pre-commit hook refuses commits without it unless `KB_SKIP_GITLEAKS=1`)
- jq (used by the `.claude/settings.json` PreToolUse hooks)
- git + gh
- Claude Code

Rules: [../CONVENTIONS.md](../CONVENTIONS.md).
