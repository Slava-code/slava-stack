#!/bin/bash
# project-kb — CLI trigger for /kb-process-inbox.
# Cd's into the KB repo, runs Claude Code in one-shot mode to drain the inbox.
# Aliased as `kbprocess` in ~/.zshrc.
#
# Usage:
#   kbprocess                 drain all inbox drops (groups near-duplicates)
#   kbprocess <slug>          process one specific drop

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"

cd "$repo_root"

if ! command -v claude >/dev/null 2>&1; then
    echo "kbprocess: Claude Code (claude) not found in PATH. Install from https://claude.com/claude-code" >&2
    exit 1
fi

# Build the prompt. Non-interactive: skill must group near-duplicate drops by
# URL, process without confirmation prompts, run to completion, and report
# results at the end.
if [ $# -eq 0 ]; then
    prompt="Run /kb-process-inbox non-interactively: process all inbox drops, group near-duplicate drops by URL automatically, do not ask for confirmation before dispatching subagents, and run to completion. Report final summary when done."
else
    slug="$1"
    prompt="Run /kb-process-inbox for the single drop with slug or path '$slug'. Non-interactive — do not ask for confirmation, run to completion, report results."
fi

exec claude -p "$prompt"
