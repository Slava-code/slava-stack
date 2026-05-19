---
type: folder
description: "Bookmark-class entries — utility URLs/GPTs/reference docs to find/reuse later; not digested sources, not temporary inbox"
---

# tools/

> The auto-generated list of entries lives in [`INDEX.md`](INDEX.md) — rebuilt by `scripts/rebuild-indexes.py` from each file's `description:` frontmatter. Do not hand-edit INDEX.md.

**Bookmark-class entries** — utility URLs, custom GPTs, web tools, reference docs the user wants to find or reuse later. A tool is *an address you revisit*. A source is *a claim about the world*. They're different jobs.

**This is one of three folders written unprompted** (alongside `sources/` and `inbox/`). Bookmarks should be cheap to add — when the user shares a useful tool or URL that they'll want to find again, drop it here without asking.

**File naming:** `YYYY-MM-DD-<slug>.md`. Date = when we filed it.

**Frontmatter required:** `type: tool`, `product:`, `url:`, `kind:` (web-app | gpt | cli | api | template | reference-doc | gist), `tags:`, `status:`, plus the standard `description:` field. Schema: [../schema/kb-schema.yaml](../schema/kb-schema.yaml) §`tool:`.

**Body cap ~15 lines, no required sections.** The `description:` frontmatter field IS the entry preview — that's what surfaces in `INDEX.md`. The body is one to two sentences (what it does + when you'd reach for it), optionally a gotcha or alternative. Anti-thinning rule does **not** apply: a one-line tool entry is the design, not a sign of a stub.

**Separate from:**
- `sources/` — which requires a factual digest (How it works, Key facts, etc.). If the URL has facts you'd cite (architecture, customer count, benchmark numbers), it belongs in `sources/` instead.
- `inbox/` — which is a temporary triage queue. Inbox drops get classified and moved out within days. Tools live here permanently.
- `raw/` — which is for founder-authored binaries (decks, recordings) outside any classified folder.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated. Template: [../schema/templates/tool.md](../schema/templates/tool.md).
