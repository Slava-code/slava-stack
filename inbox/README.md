---
type: folder
description: "Untriaged drop queue — /drop captures go here, /kb-process-inbox drains; never long-lived content"
---

# inbox/

**Queue of untriaged drops.** URLs, notes, screenshots, email snippets, X/LinkedIn posts, topics to research later. Processed by `/kb-process-inbox` — each drop handled by a **fresh subagent** to protect main context.

**This is one of two folders written unprompted.** When user drops via `/drop` or the shell-alias drop CLI, a new timestamped file lands here.

**File naming:** `YYYY-MM-DD-HHMMSS-<slug>.md` (second precision avoids collisions on rapid drops).

**Minimal frontmatter:**
```yaml
---
type: inbox-drop
source_kind: url | email | note | x-post | linkedin-post | research-topic | screenshot
source_url: "..."                      # if applicable
captured_at: 2026-04-17T09:02:34
captured_from: mobile | desktop | claude-chat | terminal | manual
status: inbox
---
```

**Body:** whatever was dropped — URL, pasted text, one-liner. No classification required at drop time.

**Processing flow** (`/kb-process-inbox`):
1. List `inbox/*.md` (filenames only — main context stays clean)
2. Dispatch an Agent per drop, sequentially (respects single-writer lock on writes / Chrome)
3. Subagent: read drop → fetch external content if needed → classify → create proper entry in destination folder → commit → delete inbox file

**LinkedIn / X drops** are login-walled; the subagent uses Chrome extension (`mcp__claude-in-chrome__*`) to fetch content. Subject to single-writer rule — never parallel Chrome tasks.

**Cadence:** drain when queue reaches ~10 items or every few days. Not enforced.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Routing for destination classification: [../AGENT-GUIDE.md](../AGENT-GUIDE.md).
