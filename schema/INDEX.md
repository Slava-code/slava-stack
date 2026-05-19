# schema/

Source of truth for frontmatter + required body sections per file type. Machine-readable. Drives `scripts/kb-lint.py` (pre-commit hook) and is the authority that templates are derived from.

**Files:**
- `kb-schema.yaml` — the contract. Defines allowed values for every frontmatter field per type, required body sections, citation rules.
- `templates/<type>.md` — ready-to-copy templates per file type, derived from the schema. Used by `/add-entry`.

**When to edit:** when a new file type is introduced, or when a required field / section changes. Schema changes commit as `schema: <change>` and typically touch:
1. `kb-schema.yaml`
2. `templates/<type>.md` (regenerate)
3. `CONVENTIONS.md` §"Required body sections" (if sections changed)

**Do not bypass.** The lint hook blocks commits that fail schema validation. Fix the content or update the schema — don't `--no-verify`.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md).
