---
name: kb-audit
description: "Audit the project-kb for freshness + consistency. Runs scripts/kb-lint.py (frontmatter validation), checks for stale raw drafts, oversized files, undecided comparisons, orphan files (no inbound citations), broken wikilinks. Thresholds reference named constants (STALE_DRAFT_DAYS, OVERSIZED_FILE_LINES, UNDECIDED_COMPARISON_DAYS) defined in CONVENTIONS.md § \"Growth rules\". Writes report to runs/YYYY-MM-DD-audit.md. Use when user asks: audit the KB, health check, freshness review, what's stale, what's broken. Also run before synthesis refresh or before onboarding a teammate."
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
5. Stage + commit: `catalog: audit <date>`. Push.
6. Release the lock.
7. Report summary to user: counts per category + report path.

The audit is diagnosis, not remediation. Surfacing the issues is the skill's job; `/kb-archive`, `/kb-promote`, etc. fix them.
