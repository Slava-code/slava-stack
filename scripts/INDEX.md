# scripts/

Helper + validation scripts.

**Files:**
- `kb-lint.py` — validates frontmatter across all `*.md` files against `schema/kb-schema.yaml`. Called by pre-commit hook; also invoked manually via `/kb-audit`.
- `kb-drop.sh` — CLI drop helper. Wrapped by `kbdrop` shell alias; creates a timestamped file in `inbox/`. Auto-commits + pushes.
- `kb-process.sh` — CLI trigger for `/kb-process-inbox`. Wrapped by `kbprocess` shell alias; runs Claude Code in one-shot mode from the KB repo to drain the inbox.
- `install-hooks.sh` — installs the pre-commit hook from version control into `.git/hooks/`. Run once after `git clone` on a fresh machine.
- `hooks/pre-commit` — the hook itself. Probes multiple Python install locations for one with PyYAML; robust against git's stripped-env hook execution.

**Dependencies:**
- Python 3 + PyYAML (anaconda base usually has it; otherwise `python3 -m pip install pyyaml`)
- git + gh
- Claude Code (for `kbprocess`)

Rules: [../CONVENTIONS.md](../CONVENTIONS.md).
