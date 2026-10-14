#!/bin/bash
# project-kb hook installer — run once after `git clone`.
# Sets core.hooksPath to scripts/hooks so the tracked hooks run directly.

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
hooks_src="$repo_root/scripts/hooks"

if [ ! -d "$hooks_src" ]; then
    echo "install-hooks: $hooks_src not found" >&2
    exit 1
fi

# Point git at the tracked hooks directory instead of copying files into
# .git/hooks/: a copy goes stale the next time a hook is edited.
chmod +x "$hooks_src"/*
git -C "$repo_root" config core.hooksPath scripts/hooks
echo "core.hooksPath -> scripts/hooks"

# The pre-commit hook scans staged changes for secrets with gitleaks.
if ! command -v gitleaks >/dev/null 2>&1; then
    echo "install-hooks: WARNING — gitleaks not found; commits will be refused until it is installed." >&2
    echo "  Install: brew install gitleaks   (or see https://github.com/gitleaks/gitleaks#installing)" >&2
fi

echo "install-hooks: done"
