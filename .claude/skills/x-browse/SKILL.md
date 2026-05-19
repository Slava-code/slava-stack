---
name: x-browse
description: "Scroll X (Twitter) for ~30 min on the user's behalf via the Chrome extension, capture posts, write a structured findings file to runs/, cross-reference everything against the existing KB, and batch-drop the best net-new items to inbox/. The user is outsourcing 'doomscrolling' as research. Use when the user says: browse X for me, scroll Twitter, do an X scan, see what's happening on X today, run an X-browse session, outsource X for 30 min, what's new on AI Twitter. Default duration 30 min, configurable via arg (e.g., /x-browse 45m). Do NOT use for fetching one specific named X post (use /drop with the URL or /kb-process-inbox). Do NOT use for general web research (use /study or WebSearch). Do NOT auto-trigger from ambient mention of Twitter — the user must explicitly invoke."
---

# /x-browse — Outsourced X scrolling with KB sync

The user wants you to scroll X for them, take notes, see what overlaps with the KB, and queue the worthwhile bits for later processing. They are spending coffee-time, not deep-work time, on this. Match the energy: skim breadth, surface signal, don't go deep on individual posts unless one is clearly worth it.

## Step 1 — Setup (1 min)

1. Acquire `runs/.lock` at repo root (per CONVENTIONS §"Single-writer rule"). Write `<session-id> x-browse <ISO>` to it. If held, abort.
2. Verify Chrome via `mcp__claude-in-chrome__tabs_context_mcp`. If not connected, abort cleanly and tell the user to restart Chrome.
3. Verify the active tab is on `x.com` and logged in (check for `home` or `For you` in title/url). If logged out, abort — don't try to log in.
4. Parse duration arg if given (e.g., `30m`, `45m`). Default 30 min.

## Step 2 — Scrape loop (most of the time)

Initialize a JS scraper in `window.__captured` that dedupes by status URL and captures `{user, handle, text, time, url, card, links}` per `article[data-testid="tweet"]`. Cap text at ~1200 chars to keep payload small.

**Critical pitfall #1 — programmatic scrolling does not load new posts.** X uses intersection-observer-based lazy loading. `window.scrollBy()` and `window.scrollTo()` from the JS tool move the viewport but don't fire the observers. Only the real mouse-wheel scroll via `mcp__claude-in-chrome__computer` `action: "scroll"` triggers content load. Use the computer tool, not JS, for every scroll.

**Critical pitfall #2 — the JS tool blocks responses with cookie-like data.** Sanitize URLs in your output: strip `?...` query strings and replace any path segment longer than ~15 chars with `/[id]`. Otherwise you'll get `[BLOCKED: Cookie/query string data]` from the tool and lose the batch.

Loop body (each cycle ~10–15s):
- `computer.scroll` down ~10 ticks at the timeline column (~640, ~400 in standard window).
- `wait 2s`.
- Run `window.__scrape()` via JS to grab + dedupe new posts.
- Every ~3 cycles, log `{y, total, fresh.users[]}` to track progress.

**Coverage targets:** 100+ unique posts per 30-min session is realistic. If `fresh.length === 0` for 3 cycles in a row, the feed is exhausted — refresh ("See new posts" banner if visible, otherwise navigate to `x.com/home`) and re-init `window.__captured`. Alternate For You ↔ Following at least once.

**Cost reminder:** every `computer.scroll` returns a screenshot (~1.5K tokens). 30 min of scrolling = ~120 screenshots = a real context cost. That's why we scrape via JS after each scroll instead of relying on the screenshot — one cheap text payload per scroll, not a 1.5K-token image. Don't take additional screenshots unless something specific needs visual inspection.

## Step 3 — Notes file (5 min)

Write `runs/YYYY-MM-DD-x-browse-notes.md` (today's UTC date). The structure is the most important part of this skill — it's what makes the session useful afterward instead of a wall of tweets.

Required sections (customize categories to match the project's actual research beat):
- **A. On the project's beat** — the user's actual interest area. Define this in the project's GLOSSARY/CLAUDE.md.
- **B. Adjacent infra / industry context** — adjacent but loud category.
- **C. Other notable categories** — additional rubrics the project tracks.
- **D. Junk filter** — one paragraph naming what you scrolled past (politics, sports, ads). Honest noise floor.
- **E. What I would do next** — 3-5 prioritized follow-ups.
- **F. Methodology notes** — anything you learned about the scraping/feed that would help future sessions.

Per-item format inside A/B/C/etc.:
- **Handle (@handle)** with date — direct quote in blockquote, then 1-2 sentences on why it matters.
- **Preserve hedges.** Per the KB's GLOSSARY § "inference discipline": don't collapse "exploring" into "decided," don't drop "e.g." from a hedged example. X posts are full of soft language and the rounding error compounds. If a post is truncated mid-sentence at the 1200-char cap, mark it `[cut off]` — don't extrapolate the punchline.
- **Translation marker.** Non-English posts: write the language + translation note explicitly.
- **Cite the handle even if uncertain about the URL.** A handle + date lets the user find the post later; a confident paraphrase with no handle is worthless.

## Step 4 — KB sync (5 min)

For each named tool/person/concept/paper in your notes, grep the KB before recommending it as new:

```bash
grep -ril "<entity>" --include="*.md" .
```

For each match:
- Read the existing entry briefly. Did the architecture change? New numbers appear? Framing shift? File those as **source UPDATE** candidates, not new sources.
- If our entry already covers the same claim better, note it.

For each non-match, mark as net-new candidate.

Surface naming collisions explicitly when two distinct entities share a name.

## Step 5 — Best-of selection + drop (5 min)

Pick 8–15 items that pass the bar for inbox. Don't drop everything you noted — most posts are noise even when they're on-topic.

Bar for a drop:
- Named entity not in KB
- Numeric or architectural delta on entity already in KB
- Explicit market framing aligned with the project's thesis
- Conf talks worth tracking for slides when they post
- Counter-arg / disconfirming evidence to a position we've taken

**Pattern:** call `scripts/kb-drop.sh` with all N positional args in one invocation. Each arg becomes one drop file with its own commit; the script runs `rebuild-indexes.py` per drop (so pre-commit's INDEX-freshness check passes), then pushes once at the end.

```bash
./scripts/kb-drop.sh \
  "https://x.com/handle/status/<id> — <commentary>" \
  "https://x.com/handle/status/<id> — <commentary>" \
  ...
```

Constraints to be aware of:
- `captured_from:` is hard-coded to `terminal` by the script — don't worry about it. (The schema only allows `['mobile', 'desktop', 'claude-chat', 'terminal', 'manual']`; custom values fail kb-lint.)
- `source_kind:` is auto-inferred from the URL host (`x.com` → `x-post`, `linkedin.com` → `linkedin-post`, else `url`). Override via `--kind` flag if needed (e.g., `--kind research-topic` when you have no URL — then pass the topic as a plain non-URL arg, no leading `https://`).
- For one drop where you want multi-line commentary, use `--url <u> --file <body-file>` instead of inline.

Each drop file body should be: 2-4 sentences of context, naming (a) what cluster it joins, (b) what to do with it (process as new sources/, or merge into existing X), (c) any cross-link suggestions. The richer the commentary, the less work `/kb-process-inbox` has to do later.

## Step 6 — Subagent option (parallel processing)

If a single artifact (article, paper, long thread) is clearly worth its own ingest pipeline, you can spawn one subagent to do `/kb-process-inbox`-style work on it while you continue with the KB sync and drops in main. The subagent acquires its own lock when main releases — never overlap. Don't run subagents during the Chrome scrape phase (single-writer Chrome).

## Step 7 — Wrap-up

1. Release `runs/.lock`.
2. Return a 5-bullet summary to the user:
   - Total posts captured
   - Top 3 most relevant items (handle + 1-line why)
   - Total drops to inbox
   - KB updates needed (existing entries to refresh)
   - Open Chrome trips deferred (e.g., threads not expanded — mention this so the user can ask for it next)

Time budget: setup 1 + scrape ~20 + notes 5 + sync + drop 5 + wrap 1 = ~30 min for the default invocation. Adjust scrape time if the user passes a different duration.

## When NOT to use

- **Fetching one specific named X post** the user just sent you — use `/drop` with the URL or process directly with `/add-entry`. /x-browse is for open-ended scanning, not targeted retrieval.
- **General web research** on a topic — use `/study` (sources/concepts) or WebSearch. /x-browse is X-only.
- **The user mentioned Twitter ambiently** ("oh I saw on Twitter that…") — that's a one-off, not a request to scroll. Wait for explicit invocation.
- **The Chrome extension is not connected** — abort cleanly, tell user. Do not try alternative paths (WebFetch is blocked on x.com per AGENT-GUIDE.md § "Login-walled content").
- **You're already in another long-running task** — finish that first, don't yak-shave into a 30-min X session.

## Recurrence

This skill is a strong candidate for `/schedule` — a weekly run of `/x-browse 30m` would maintain a steady drip of inbox candidates and an evolving runs/ archive. After the first manual run, ask the user if they want it scheduled. Don't auto-schedule.

## Required reading first time

- `CONVENTIONS.md` §"Single-writer rule" + §"Commit convention"
- `CLAUDE.md` §"KB-first for named-entity queries"
- `scripts/kb-drop.sh` — for the exact frontmatter format the inbox processor expects
