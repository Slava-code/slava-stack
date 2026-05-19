#!/usr/bin/env bash
# github-deep-fetch.sh — pass-1 mechanical fetch for a GitHub repo.
# Output goes to stdout, or to --out <path> (intended: runs/fetches/<slug>.txt).
#
# Two-pass design:
#   PASS 1 (this script, mechanical, always runs):
#     - Repo metadata (stars, language, license, dates)
#     - Full README (base64-decoded)
#     - File tree (paths only, top 200)
#     - Common manifest files (package.json, pyproject.toml, etc.)
#   PASS 2 (digesting subagent, judgment-driven, on demand):
#     - Reads pass-1 output
#     - Picks 2-5 high-signal files based on README hints + tree structure
#     - Reads each via:
#         gh api repos/<OWNER>/<REPO>/contents/<PATH> --jq '.content' | base64 -d
#     - Hard caps: 5 files OR 2000 total lines, whichever first
#
# A README ≠ a repo. Pass 1 surfaces the menu; pass 2 actually reads code.

set -euo pipefail

INPUT="${1:-}"
if [[ -z "$INPUT" ]]; then
  echo "usage: github-deep-fetch.sh <github-url-or-owner/repo> [--out <path>]" >&2
  exit 2
fi

OUT_PATH=""
if [[ "${2:-}" == "--out" ]]; then
  OUT_PATH="${3:?--out requires a path}"
fi

command -v gh      >/dev/null 2>&1 || { echo "ERROR: gh not installed. brew install gh" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not found" >&2; exit 1; }

# Normalize → OWNER/REPO
if [[ "$INPUT" =~ github\.com[:/]([^/]+)/([^/]+) ]]; then
  OWNER="${BASH_REMATCH[1]}"
  REPO="${BASH_REMATCH[2]%.git}"
  REPO="${REPO%%/*}"
elif [[ "$INPUT" =~ ^([^/]+)/([^/]+)$ ]]; then
  OWNER="${BASH_REMATCH[1]}"
  REPO="${BASH_REMATCH[2]}"
else
  echo "ERROR: cannot parse '$INPUT' — expected github.com/OWNER/REPO or OWNER/REPO" >&2
  exit 1
fi
REPO_FULL="$OWNER/$REPO"

render() {
  echo "REPO: $REPO_FULL"
  echo "URL:  https://github.com/$REPO_FULL"
  echo

  # Metadata via gh api (more fields available than gh repo view)
  echo "--- METADATA ---"
  gh api "repos/$REPO_FULL" 2>/dev/null \
  | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
except Exception as e:
    print("(metadata fetch failed:", e, ")"); sys.exit(0)
def g(k, sub=None):
    v = d.get(k)
    if v is None: return "(unset)"
    if sub:
        return v.get(sub, "(unset)") if isinstance(v, dict) else str(v)
    return str(v) if not isinstance(v, (list, dict)) else json.dumps(v)
print("DESCRIPTION:     ", g("description"))
print("STARS:           ", g("stargazers_count"))
print("FORKS:           ", g("forks_count"))
print("DEFAULT_BRANCH:  ", g("default_branch"))
print("PRIMARY_LANGUAGE:", g("language"))
print("LICENSE:         ", g("license", "name"))
print("HOMEPAGE:        ", g("homepage"))
print("TOPICS:          ", g("topics"))
print("CREATED:         ", g("created_at"))
print("UPDATED:         ", g("updated_at"))
print("PUSHED:          ", g("pushed_at"))
print("ARCHIVED:        ", g("archived"))
print("OPEN_ISSUES:     ", g("open_issues_count"))
'
  echo

  # README
  echo "--- README ---"
  echo
  if README_B64=$(gh api "repos/$REPO_FULL/readme" --jq '.content' 2>/dev/null); then
    echo "$README_B64" | tr -d '\n' | base64 -d 2>/dev/null || echo "(README decode failed)"
  else
    echo "(no README found at repo root)"
  fi
  echo
  echo

  # File tree (paths only, capped)
  echo "--- FILE TREE (type, path, size; first 200 entries) ---"
  echo
  if ! gh api "repos/$REPO_FULL/git/trees/HEAD?recursive=1" \
        --jq '.tree[] | "\(.type)\t\(.path)\t\(.size // "-")"' 2>/dev/null \
       | head -200; then
    echo "(tree fetch failed — large repo or rate limit)"
  fi
  TREE_FULL_COUNT=$(gh api "repos/$REPO_FULL/git/trees/HEAD?recursive=1" --jq '.tree | length' 2>/dev/null || echo "?")
  echo
  echo "(showing first 200 of $TREE_FULL_COUNT entries)"
  echo

  # Common manifest files
  echo "--- MANIFEST / CONFIG FILES ---"
  echo
  for cfg in package.json pyproject.toml requirements.txt Cargo.toml go.mod setup.py setup.cfg Pipfile composer.json Gemfile Makefile; do
    if CONTENT=$(gh api "repos/$REPO_FULL/contents/$cfg" --jq '.content' 2>/dev/null); then
      DECODED=$(echo "$CONTENT" | tr -d '\n' | base64 -d 2>/dev/null || echo "")
      if [[ -n "$DECODED" ]]; then
        echo "## $cfg"
        echo
        echo "$DECODED" | head -100
        echo
        echo "---"
        echo
      fi
    fi
  done

  # Pass-2 hint
  echo "--- PASS-2 INSTRUCTIONS (for the digesting subagent) ---"
  echo
  echo "PASS 1 above contains: metadata, README, file tree, manifest files."
  echo "PASS 2 (your job): identify 2-5 high-signal files based on README + tree."
  echo
  echo "Read each via:"
  echo "  gh api repos/$REPO_FULL/contents/<path> --jq '.content' | tr -d '\\n' | base64 -d"
  echo
  echo "Hard caps: 5 files OR 2000 total lines, whichever first."
  echo
  echo "Heuristics:"
  echo "  - README mentions specific paths (\"core logic in src/X.py\") → those first"
  echo "  - For libraries: read the entry point named in package.json/pyproject.toml/Cargo.toml/etc."
  echo "  - For agents/RAG/eval projects: src/agents, src/eval, benchmarks/, evals/"
  echo "  - For ML papers' code: src/model.py, train.py, configs/, scripts/eval.py"
  echo "  - Skip: tests/, examples/, docs/, .github/, vendored deps"
}

if [[ -n "$OUT_PATH" ]]; then
  mkdir -p "$(dirname "$OUT_PATH")"
  render > "$OUT_PATH"
  echo "Wrote $OUT_PATH ($(wc -l < "$OUT_PATH") lines, $(wc -c < "$OUT_PATH") bytes)" >&2
else
  render
fi
