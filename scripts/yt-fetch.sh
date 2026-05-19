#!/usr/bin/env bash
# yt-fetch.sh — fetch YouTube video metadata + transcript for KB digestion.
# Output goes to stdout, or to --out <path> (intended: runs/fetches/<slug>.txt).
# The digesting subagent reads the output, writes the source/ entry, and cites
# the runs/fetches/ path in the entry's `## Fetched from` section.
#
# Caveats:
#   - Auto-captions are ASR — punctuation rough, occasional misheard words.
#     Fine for "what's the gist + key claims"; not suitable for verbatim quoting.
#   - When no captions exist, header marks TRANSCRIPT_SOURCE: none and the
#     digester should write a stub source entry noting the video must be watched.

set -euo pipefail

URL="${1:-}"
if [[ -z "$URL" ]]; then
  echo "usage: yt-fetch.sh <youtube-url> [--out <path>]" >&2
  exit 2
fi

OUT_PATH=""
if [[ "${2:-}" == "--out" ]]; then
  OUT_PATH="${3:?--out requires a path}"
fi

command -v yt-dlp  >/dev/null 2>&1 || { echo "ERROR: yt-dlp not installed. brew install yt-dlp" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not found" >&2; exit 1; }

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Single yt-dlp call: metadata JSON + auto/manual subs as VTT
yt-dlp \
  --skip-download \
  --write-auto-subs --write-subs --sub-langs "en.*,en" --sub-format vtt \
  --write-info-json \
  --output "$TMPDIR/v.%(ext)s" \
  --quiet --no-warnings \
  "$URL" 1>&2 || { echo "ERROR: yt-dlp failed for $URL" >&2; exit 1; }

INFO_JSON=$(ls "$TMPDIR"/v.info.json 2>/dev/null | head -1 || true)
VTT_FILE=$(ls "$TMPDIR"/v*.vtt    2>/dev/null | head -1 || true)

[[ -f "$INFO_JSON" ]] || { echo "ERROR: yt-dlp produced no metadata JSON" >&2; exit 1; }

render() {
  python3 - "$INFO_JSON" "$VTT_FILE" <<'PYEOF'
import json, re, sys

info_path, vtt_path = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "")
info = json.load(open(info_path))

# Header
print(f"TITLE: {info.get('title', '(unknown)')}")
print(f"CHANNEL: {info.get('channel', '(unknown)')}")
print(f"DURATION: {info.get('duration_string', '(unknown)')}")
print(f"UPLOADED: {info.get('upload_date', '(unknown)')}")
print(f"VIEWS: {info.get('view_count', '(unknown)')}")
print(f"URL: {info.get('webpage_url', '(unknown)')}")
desc = (info.get('description') or '').strip()
if desc:
    desc_short = re.sub(r'\s+', ' ', desc)[:600]
    print(f"DESCRIPTION: {desc_short}")
print("---")

if not vtt_path:
    print("TRANSCRIPT_SOURCE: none")
    print()
    print("WARNING: no captions (manual or auto) available. Video must be watched manually.")
    sys.exit(0)

# Detect manual vs auto from VTT file naming convention
basename = vtt_path.rsplit("/", 1)[-1].lower()
# yt-dlp names auto subs with the language code only when manual subs exist;
# otherwise, presence of auto-sub track is signaled by automatic_captions in info.
auto_langs = list((info.get("automatic_captions") or {}).keys())
manual_langs = list((info.get("subtitles") or {}).keys())
src_label = "manual subtitles" if manual_langs and any(basename.endswith(f".{l}.vtt") for l in manual_langs) else "auto-captions (ASR)"

print(f"TRANSCRIPT_SOURCE: {src_label}")
print(f"TRANSCRIPT_PATH: {vtt_path}")
print()
print("--- TRANSCRIPT ---")
print()

# Clean VTT → plaintext, dedupe rolling-window repeats
text_lines = []
seen = set()
with open(vtt_path, encoding="utf-8") as f:
    for raw in f:
        line = raw.strip()
        if not line: continue
        if line.startswith(("WEBVTT", "NOTE", "STYLE", "Kind:", "Language:", "X-TIMESTAMP")): continue
        if "-->" in line: continue
        # Strip inline VTT/HTML tags
        line = re.sub(r"<[^>]+>", "", line).strip()
        if not line: continue
        if line in seen: continue
        seen.add(line)
        text_lines.append(line)

print("\n".join(text_lines))
PYEOF
}

if [[ -n "$OUT_PATH" ]]; then
  mkdir -p "$(dirname "$OUT_PATH")"
  render > "$OUT_PATH"
  echo "Wrote $OUT_PATH ($(wc -l < "$OUT_PATH") lines)" >&2
else
  render
fi
