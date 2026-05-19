#!/bin/bash
# project-kb hook installer — run once after `git clone`.
# Copies scripts/hooks/* into .git/hooks/ and makes them executable.

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
hooks_src="$repo_root/scripts/hooks"
hooks_dst="$repo_root/.git/hooks"

if [ ! -d "$hooks_src" ]; then
    echo "install-hooks: $hooks_src not found" >&2
    exit 1
fi

for hook in "$hooks_src"/*; do
    name=$(basename "$hook")
    cp "$hook" "$hooks_dst/$name"
    chmod +x "$hooks_dst/$name"
    echo "installed: $name"
done

echo "install-hooks: done"
