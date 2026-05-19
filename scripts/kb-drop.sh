#!/bin/bash
# kbdrop — CLI helper to drop content into the KB inbox.
#
# Usage:
#   kbdrop "quick note or research topic"                     # content drop
#   kbdrop "https://..."                                       # URL drop (kind auto-inferred)
#   kbdrop "https://a" "https://b"                             # multiple drops, one per arg
#   kbdrop "https://... — my take: ..."                        # URL + note, bundled
#
# Each positional arg becomes ONE inbox file. If the arg starts with
# http:// or https://, source_url is set and kind is inferred from host:
#   x.com, twitter.com   → x-post
#   linkedin.com         → linkedin-post
#   (else)               → url
# Any text after the URL on the same arg (e.g. " — my take: ...") is
# attached as commentary body on the same drop. Separate quoted args
# always mean separate drops — there's no way to cross-bundle them.
# To attach commentary to a URL, include it inline in the same quoted arg.
#
# Writes inbox/YYYY-MM-DD-HHMMSS-<slug>.md, auto-commits (`inbox: drop <slug>`),
# and pushes to origin.
#
# Escape-hatch flags (rarely needed):
#   --url <u>       force URL (legacy single-drop mode)
#   --kind <k>      override auto-inferred kind
#   --file <path>   read body from a file
#   --from <src>    override captured_from (default: terminal)
#
# Installed as: alias kbdrop='<repo>/scripts/kb-drop.sh'

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
inbox="$repo_root/inbox"

kind_override=""
url_flag=""
file=""
captured_from="terminal"
positional=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --url) url_flag="$2"; shift 2;;
        --kind) kind_override="$2"; shift 2;;
        --file) file="$2"; shift 2;;
        --from) captured_from="$2"; shift 2;;
        -h|--help) sed -n '3,29p' "$0"; exit 0;;
        *) positional+=("$1"); shift;;
    esac
done

infer_kind() {
    local lc
    lc=$(echo "$1" | tr '[:upper:]' '[:lower:]')
    case "$lc" in
        https://x.com/*|http://x.com/*|https://www.x.com/*|http://www.x.com/*|\
        https://twitter.com/*|http://twitter.com/*|https://www.twitter.com/*|http://www.twitter.com/*)
            echo "x-post" ;;
        https://linkedin.com/*|http://linkedin.com/*|https://www.linkedin.com/*|http://www.linkedin.com/*)
            echo "linkedin-post" ;;
        *)
            echo "url" ;;
    esac
}

do_drop() {
    local d_kind="$1" d_url="$2" d_content="$3" d_from="$4"
    local slug_source="${d_content:-$d_url}"
    local slug
    slug=$(printf '%s' "$slug_source" \
        | tr '\n\r\t' '   ' \
        | tr '[:upper:]' '[:lower:]' \
        | sed -E 's/[^a-z0-9]+/-/g' \
        | sed -E 's/^-+|-+$//g' \
        | cut -c1-40 \
        | sed -E 's/-+$//')
    [ -z "$slug" ] && slug="drop"

    local ts_file ts_iso
    ts_file=$(date +%Y-%m-%d-%H%M%S)
    ts_iso=$(date +%Y-%m-%dT%H:%M:%S)
    local filename="$inbox/${ts_file}-${slug}.md"

    mkdir -p "$inbox"
    {
        echo "---"
        echo "type: inbox-drop"
        echo "source_kind: $d_kind"
        [ -n "$d_url" ] && echo "source_url: \"$d_url\""
        echo "captured_at: $ts_iso"
        echo "captured_from: $d_from"
        echo "status: inbox"
        echo "---"
        echo
        if [ -n "$d_content" ]; then
            echo "$d_content"
        elif [ -n "$d_url" ]; then
            echo "$d_url"
        fi
    } > "$filename"

    local rel
    rel=$(realpath --relative-to="$repo_root" "$filename" 2>/dev/null || \
          python3 -c "import os; print(os.path.relpath('$filename', '$repo_root'))")

    cd "$repo_root"
    # Regenerate inbox/INDEX.md so the pre-commit hook's freshness check
    # passes. Without this, the hook aborts every drop because adding a new
    # inbox file always staleness-triggers inbox/INDEX.md. Cheap (~50ms).
    python3 scripts/rebuild-indexes.py > /dev/null
    git add "$rel" inbox/INDEX.md
    git commit -m "$(cat <<EOF
inbox: drop ${ts_file}-${slug}

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)" > /dev/null
    echo "dropped: $rel"
}

# Escape-hatch path: --url or --file given → legacy single-drop mode.
# All positional args concatenate into content; file body appends to it.
if [ -n "$url_flag" ] || [ -n "$file" ]; then
    content=""
    if [ ${#positional[@]} -gt 0 ]; then
        for arg in "${positional[@]}"; do
            if [ -z "$content" ]; then content="$arg"; else content="$content $arg"; fi
        done
    fi
    if [ -n "$file" ]; then
        if [ ! -f "$file" ]; then
            echo "kbdrop: file not found: $file" >&2
            exit 1
        fi
        file_content=$(cat "$file")
        if [ -z "$content" ]; then content="$file_content"; else content="$content"$'\n\n'"$file_content"; fi
    fi
    if [ -z "$content" ] && [ -z "$url_flag" ]; then
        echo "kbdrop: need content, --url, or --file" >&2
        exit 1
    fi
    if [ -n "$kind_override" ]; then
        kind="$kind_override"
    elif [ -n "$url_flag" ]; then
        kind=$(infer_kind "$url_flag")
    else
        kind="note"
    fi
    do_drop "$kind" "$url_flag" "$content" "$captured_from"
    cd "$repo_root"
    git push > /dev/null 2>&1 || echo "kbdrop: committed locally but push failed (offline?)"
    exit 0
fi

# Main path: auto-detect per positional arg. Each arg is its own drop.
# An arg starting with http(s):// is a URL drop; any trailing prose
# (whitespace-separated) becomes commentary body on that same drop.
if [ ${#positional[@]} -eq 0 ]; then
    echo "kbdrop: need at least one argument (content or URL)" >&2
    exit 1
fi

first=true
for arg in "${positional[@]}"; do
    if ! $first; then sleep 1; fi   # second-precision timestamps need spacing across multi drops
    first=false
    if [[ "$arg" =~ ^(https?://[^[:space:]]+)([[:space:]]+(.+))?$ ]]; then
        url_part="${BASH_REMATCH[1]}"
        commentary="${BASH_REMATCH[3]:-}"
        kind="${kind_override:-$(infer_kind "$url_part")}"
        do_drop "$kind" "$url_part" "$commentary" "$captured_from"
    else
        kind="${kind_override:-note}"
        do_drop "$kind" "" "$arg" "$captured_from"
    fi
done

cd "$repo_root"
git push > /dev/null 2>&1 || echo "kbdrop: committed locally but push failed (offline?)"
