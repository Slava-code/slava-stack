---
type: folder
description: "Digested external references — articles/papers/repos dropped into chat; factual, not opinionated"
---

# sources/

> The auto-generated list of entries lives in [`INDEX.md`](INDEX.md) — rebuilt by `scripts/rebuild-indexes.py` from each file's `description:` frontmatter. Do not hand-edit INDEX.md.

**Digested external references** — articles, papers, repos, tools dropped into chat. **Factual, not opinionated.** Opinions about how a source relates to the project go in `brainstorming/`, `comparisons/`, or `research-dispatches/` — never inside a source file.

**This is one of two folders written unprompted.** When user drops a URL / paper / repo / file, we fetch, digest, and save without asking.

**File naming:** `YYYY-MM-DD-<source-slug>.md`. Date = when we digested it.

**Structure:**
1. What it is (1-2 sentences)
2. How it works / key architecture / mechanism
3. Key facts (funding, metrics, customers, dates) if relevant
4. Source links (URL, DOI, repo)

**Frontmatter required:** `type: source`, `product:`, `source:` (the URL/DOI/origin), `tags:`, `status:`.

**De-duplication rule:** before creating a new `sources/` entry, check if a digest already exists in a sibling KB (if you maintain more than one). If yes, *link to it* rather than duplicating. This folder only holds sources that are genuinely cross-cutting or strategic.

**Separate from:**
- `advisors/` — which is for *outreach-target intel on specific people* (professors, potential advisors). A professor's *paper* belongs here; the *professor* belongs in `advisors/`.
- LinkedIn / X content — login-walled; use Chrome extension to fetch, respects single-writer rule. See [../AGENT-GUIDE.md](../AGENT-GUIDE.md).

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
