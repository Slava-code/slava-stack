---
name: kb-add-folder
description: "Add a new top-level folder to the project-kb. Enforces CONVENTIONS § \"Growth rules\" (named constants NEW_FOLDER_MIN_FILES + NEW_FOLDER_INDEX_MAX_LINES, doesn't fit existing folders, structural not topic difference). Creates folder + README.md (hand-authored rules/purpose with type: folder frontmatter) + AGENT-GUIDE routing update. Generator auto-creates INDEX.md. If a new file type is introduced, also updates schema + templates + CONVENTIONS. Use when: user says add a new folder / new content category, you think current folders don't fit a new class of content, you need a new type."
---

# /kb-add-folder

1. Acquire `runs/.lock`.
2. Confirm growth-rule compliance per CONVENTIONS § "Growth rules" (values are the named constants in that section):
   - Are there at least `NEW_FOLDER_MIN_FILES` existing files (committed or drafted) that fit this category?
   - Do they not fit existing folders? (Re-check AGENT-GUIDE.md routing table before saying "no.")
   - Is this a STRUCTURAL difference (new file type, new lifecycle, new required sections) OR just a topic tag?
   - Can the new `<folder>/README.md` (rules + purpose) be written within `NEW_FOLDER_INDEX_MAX_LINES` without hand-waving?
   If any fails, report to user with specifics and stop. Do not create the folder.
3. Create the folder: `mkdir -p <folder-name>`.
4. Write `<folder-name>/README.md` with frontmatter `type: folder`, `description:` (≤120 chars, rule-not-summary — describes the folder's purpose as a stable rule). Body: purpose, naming, structure, frontmatter requirements, when-written, pointer to CONVENTIONS for rules and INDEX.md for entries.
5. **If a new file type is introduced:**
   - Add an entry under `types:` in `schema/kb-schema.yaml` with required fields, extra_fields, status_values, body_required_sections.
   - Add new enums to `enums:` if needed.
   - Create `schema/templates/<type>.md` with frontmatter (including `description:` placeholder with inline example) + required section skeleton.
   - Update CONVENTIONS.md §"Folder layout" table with the new folder row.
6. Update AGENT-GUIDE.md:
   - Add a row to the "Where does this piece of content go?" table.
   - Add to "Common queries" if applicable.
7. Regenerate INDEXes: `python3 scripts/rebuild-indexes.py`. Creates `<folder-name>/INDEX.md` (will show `_(empty)_` until content lands) and refreshes root `INDEX.md` to include the new subfolder. Stage all modified INDEX.md files.
8. Commit(s) — prefer multiple atomic commits:
   - `kb: add <folder>/`
   - `schema: add <type> type` (if applicable)
   - `conventions: document <folder>/` (if applicable)
   Push after each.
9. Release the lock.
