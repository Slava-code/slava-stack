#!/usr/bin/env bash
# arxiv-fetch.sh — fetch arxiv paper PDF + abstract-page metadata for KB digestion.
# Output goes to stdout, or to --out <path> (intended: runs/fetches/<slug>.txt).
# The digesting subagent reads the output, writes the source/ entry, and cites
# the runs/fetches/ path in the entry's `## Fetched from` section.
#
# Caveats:
#   - pdftotext -layout preserves tables roughly but mangles math equations
#     and drops figures entirely. For papers where equations or visuals
#     carry the argument, supplement with the abstract page or HTML version.
#   - Some recent papers (especially 2026+) only have v1 on arxiv; older
#     papers may have multiple versions. This script normalizes to the
#     latest version; pass an explicit ID with vN to pin.

set -euo pipefail

INPUT="${1:-}"
if [[ -z "$INPUT" ]]; then
  echo "usage: arxiv-fetch.sh <arxiv-url-or-id> [--out <path>]" >&2
  exit 2
fi

OUT_PATH=""
if [[ "${2:-}" == "--out" ]]; then
  OUT_PATH="${3:?--out requires a path}"
fi

command -v pdftotext >/dev/null 2>&1 || { echo "ERROR: pdftotext not installed. brew install poppler" >&2; exit 1; }
command -v curl      >/dev/null 2>&1 || { echo "ERROR: curl not found" >&2; exit 1; }
command -v python3   >/dev/null 2>&1 || { echo "ERROR: python3 not found" >&2; exit 1; }

# Extract arxiv ID — accepts new-style (YYMM.NNNNN) or old-style (cs/0001001)
ARXIV_ID=$(echo "$INPUT" | grep -oE '([0-9]{4}\.[0-9]{4,5}(v[0-9]+)?|[a-z\-]+/[0-9]{7})' | head -1 || true)
if [[ -z "$ARXIV_ID" ]]; then
  echo "ERROR: cannot extract arxiv ID from '$INPUT' (expected e.g. 2502.14802 or arxiv.org/abs/2502.14802)" >&2
  exit 1
fi
ARXIV_ID_NOV=$(echo "$ARXIV_ID" | sed -E 's/v[0-9]+$//')

PDF_URL="https://arxiv.org/pdf/${ARXIV_ID_NOV}.pdf"
ABS_URL="https://arxiv.org/abs/${ARXIV_ID_NOV}"

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Download PDF
curl -fsSL --retry 2 --retry-delay 2 -o "$TMPDIR/paper.pdf" "$PDF_URL" \
  || { echo "ERROR: PDF download failed: $PDF_URL" >&2; exit 1; }

# Convert to plaintext with -layout (better tables; degrades equations the same as default)
pdftotext -layout "$TMPDIR/paper.pdf" "$TMPDIR/paper.txt" \
  || { echo "ERROR: pdftotext failed" >&2; exit 1; }

# Fetch abstract page HTML for venue/title/authors metadata
ABS_HTML=""
if curl -fsSL --retry 2 --retry-delay 2 -o "$TMPDIR/abs.html" "$ABS_URL" 2>/dev/null; then
  ABS_HTML="$TMPDIR/abs.html"
fi

render() {
  python3 - "$TMPDIR/paper.txt" "${ABS_HTML:-}" "$ARXIV_ID_NOV" "$ABS_URL" "$PDF_URL" <<'PYEOF'
import re, sys, html as htmllib

paper_txt = open(sys.argv[1], encoding="utf-8", errors="replace").read()
abs_html  = open(sys.argv[2], encoding="utf-8", errors="replace").read() if sys.argv[2] else ""
arxiv_id, abs_url, pdf_url = sys.argv[3], sys.argv[4], sys.argv[5]

def m(p, src, default="(unknown)"):
    res = re.search(p, src, re.S | re.I)
    return htmllib.unescape(res.group(1)).strip() if res else default

title    = m(r'<meta name="citation_title" content="([^"]+)"', abs_html)
authors  = m(r'<meta name="citation_authors?" content="([^"]+)"', abs_html)
date     = m(r'<meta name="citation_date" content="([^"]+)"', abs_html)
abstract = m(r'<blockquote class="abstract[^"]*">([\s\S]+?)</blockquote>', abs_html, default="")
abstract = re.sub(r'^Abstract:\s*', '', abstract).strip()
abstract = re.sub(r'\s+', ' ', abstract)
comments = m(r'<td class="tablecell comments[^"]*">([\s\S]+?)</td>', abs_html, default="")
comments = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', comments)).strip()

print(f"ARXIV_ID: {arxiv_id}")
print(f"TITLE: {title}")
print(f"AUTHORS: {authors}")
print(f"DATE: {date}")
print(f"ABS_URL: {abs_url}")
print(f"PDF_URL: {pdf_url}")
if comments:
    print(f"COMMENTS: {comments}")
if abstract:
    print(f"ABSTRACT: {abstract}")
print("---")
print("WARNING: equations rendered as garbage; figures dropped; tables approximate.")
print("WARNING: cite the PDF for verbatim claims; cross-reference visuals with the HTML version if argument is figure-driven.")
print("---")
print()
print("--- PAPER TEXT (pdftotext -layout) ---")
print()
print(paper_txt)
PYEOF
}

if [[ -n "$OUT_PATH" ]]; then
  mkdir -p "$(dirname "$OUT_PATH")"
  render > "$OUT_PATH"
  echo "Wrote $OUT_PATH ($(wc -l < "$OUT_PATH") lines, $(wc -c < "$OUT_PATH") bytes)" >&2
else
  render
fi
