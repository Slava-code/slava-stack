---
name: kb-audit
description: "Health check of the KB: lint, stale drafts, oversized files, undecided comparisons, orphans, broken links, overdue todos, STATE.md age. Writes a report to runs/. Use when the user asks: audit the KB, what's stale, what's broken, health check; also before a synthesis."
---

# /kb-audit — Audit KB health

1. Acquire `runs/.lock`.
2. Run lint: `python3 scripts/kb-lint.py`. Capture errors.
3. Walk the content folders and check (named thresholds defined in CONVENTIONS.md § "Growth rules"):
   - **Stale raw drafts:** `status: raw` or `status: prospect` (for advisors) where `date_found` or `created_at` is older than `STALE_DRAFT_DAYS`.
   - **Oversized files:** any `*.md` larger than `OVERSIZED_FILE_LINES` (use `wc -l`). Candidates for multi-chapter promotion.
   - **Undecided comparisons:** `decision_status: considered` with no commit touching the file in the last `UNDECIDED_COMPARISON_DAYS` days.
   - **Orphan files:** content files with no inbound `[[<slug>]]` citations from any other file. Use grep.
   - **Broken wikilinks:** `[[<path>]]` where the target file does not exist. Use grep + file checks.
   - **Overdue todos:** `todos/*.md` with `status: pending` and a `deadline` before today. Report them as *outcome unknown* (nobody recorded it), not as "not done".
   - **STATE.md age:** if `STATE.md` exists, compare its `as-of:` date with the newest `synthesis/` file and the newest dated content file; flag it when either is newer.
   - **Convergence promotion candidates:** `python3 scripts/kb-convergence-scan.py` — any `convergence:` tag on ≥3 brainstorms means the pattern has escaped its origin and deserves its own `questions/` or `research-dispatches/` file. Capture the script's "Promotion candidates" section.
4. Compose report: `runs/YYYY-MM-DD-audit.md` with frontmatter:
   ```yaml
   ---
   type: run-log
   kind: audit
   date_found: YYYY-MM-DD
   ---
   ```
   Body: sections for each check category; counts + file lists. If zero issues in a category, say so.
5. Stage + commit: `kb: audit <date>`. Push.
6. Release the lock.
7. Report summary to user: counts per category + report path.

The audit is diagnosis, not remediation. Surfacing the issues is the skill's job; `/kb-archive`, `/kb-promote`, etc. fix them.
