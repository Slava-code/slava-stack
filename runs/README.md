---
type: folder
description: "KB maintenance runs — audits, syntheses, migrations + single-writer lock; history of KB evolution"
---

# runs/

**KB maintenance runs** — audits, syntheses, migrations, and the single-writer lock.

**Files written here:**
- `.lock` — single-writer coordination. Contains session ID + timestamp of the currently-writing agent. Removed by the agent on completion. Manual override: `rm runs/.lock` if a previous session died.
- `YYYY-MM-DD-audit.md` — `/kb-audit` output: freshness issues, broken citations, aged raw drafts, oversized files, orphan references.
- `YYYY-MM-DD-synthesis-<product>.md` — metadata log when `/kb-synthesize` runs (not the synthesis itself; that goes to `synthesis/`).
- `YYYY-MM-DD-migration-<slug>.md` — structural migrations (folder adds, renames, schema changes).

**Frontmatter required:** `type: run-log`, `kind: audit | synthesis | migration | lock`, `date_found:`.

**Retention:** kept indefinitely for historical record. The runs log is a history of *how the KB evolved*, distinct from the content it holds.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Lock behavior: [../AGENT-GUIDE.md](../AGENT-GUIDE.md) §"Single-writer rule".
