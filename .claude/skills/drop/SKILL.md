---
name: drop
description: "Quick-capture to the project-kb inbox. Accepts raw content, a URL, or a file path. Writes a timestamped file to inbox/, auto-commits, pushes. No classification — that happens later via /kb-process-inbox. Use when: user says 'drop this', 'save this to inbox', 'queue this', 'capture this for later'; user shares a URL without analyzing it; user mentions a research topic worth chewing on later; user has a quick thought to remember. Do NOT use for structured entries (use /add-entry) or deadlines (use /add-todo). Do NOT use if you've already read or analyzed the content in this conversation — classification is not deferred, use /add-entry instead (often twice: sources/ for the factual digest + brainstorming/ for our take; see AGENT-GUIDE.md §Source + brainstorm pair)."
---

# /drop — Inbox capture

1. Acquire `runs/.lock`. (Lightweight write; still respects the single-writer rule.)
2. Invoke `scripts/kb-drop.sh` with appropriate flags:
   - Plain content: `scripts/kb-drop.sh "<content>"`
   - With URL: `scripts/kb-drop.sh --url <url> "<optional commentary>"`
   - LinkedIn post: `scripts/kb-drop.sh --kind linkedin-post --url <url>`
   - X post: `scripts/kb-drop.sh --kind x-post --url <url>`
   - Email forward: `scripts/kb-drop.sh --kind email --file <path>`
   - Research topic: `scripts/kb-drop.sh --kind research-topic "<topic>"`
3. The script writes `inbox/YYYY-MM-DD-HHMMSS-<slug>.md`, stages, commits with `inbox: drop <slug>`, and pushes.
4. Release the lock.
5. Report back: one-line path of the dropped file.

If the script's `git push` fails (e.g., offline), note it to user — the commit was made locally and will push on next connectivity.

Do not classify or fetch external content here — that's `/kb-process-inbox`'s job.

## When NOT to use /drop

- **You already analyzed the content in this conversation.** Use `/add-entry` directly. If it's an external source that sparked project implications work, create the source + brainstorm pair (see `AGENT-GUIDE.md` §"Source + brainstorm pair"). `/drop` is for deferred reading, not for hiding finished analysis in a queue.
- **The content type is already clear.** Use `/add-entry` — it routes to the right folder and template.
- **It's a todo / deadline.** Use `/add-todo`.
