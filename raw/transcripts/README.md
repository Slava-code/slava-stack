---
name: raw/transcripts — verbatim meeting and session transcripts
description: "Verbatim transcripts of meetings, calls and founder brainstorms; primary artifact that notes cite by line"
type: folder
---

# raw/transcripts/

Verbatim transcripts of every meeting and call, plus founder brainstorms and recorded working sessions — the **primary artifact**. Never edit a transcript after filing: notes cite it by line number (`[T:NN](../raw/transcripts/<file>.md#LNN)`), and an edit shifts every citation. Digested, opinionated write-ups live in [`../../brainstorming/`](../../brainstorming/) (or `strategy/`) and **cite back here** rather than copying, so the digest can be reshaped without losing the source words.

Meeting notes live in [`../../meetings/`](../../meetings/) under the same slug and link here line by line (written by `/meeting`). Brainstorm digests in `brainstorming/` cite here the same way.

**File naming:** `YYYY-MM-DD-<participants-or-topic-slug>.md` — a short header (what it is, link to the notes file), then the verbatim text, never reworded. Carries `type: source` + a `description:` so it appears in the parent INDEX. Demo: [`2026-01-15-example-advisor-pricing.md`](2026-01-15-example-advisor-pricing.md).

Excluded from default Grep results by the root `.ignore` (transcripts match almost any term and outrank the notes that hold the answer); use `grep -r` or `rg --no-ignore` to search them.

Cite from elsewhere with the relative path, e.g. `[[../raw/transcripts/YYYY-MM-DD-topic-slug-brainstorm]]`.
