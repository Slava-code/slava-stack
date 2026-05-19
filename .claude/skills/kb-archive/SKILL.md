---
name: kb-archive
description: "Move a fully-superseded project-kb file to archive/. Preserves the original subfolder structure inside archive/ (so restoration is trivial). Regenerator automatically removes the entry from the source folder's INDEX.md. Enforces archive criteria from CONVENTIONS § \"Growth rules\" (supersedes + uncited past ARCHIVE_UNCITED_MONTHS + no active decision references). Use when: user says archive X, retire Y, clean up outdated content, this brainstorm is superseded."
---

# /kb-archive <path>

Usage: `/kb-archive brainstorming/2026-04-05-example-slug.md`.

1. Acquire `runs/.lock`.
2. Verify archive criteria per CONVENTIONS §"Growth rules":
   - **Fully superseded:** file has `supersedes:` coming from a newer file OR user confirms it's retired.
   - **Uncited for `ARCHIVE_UNCITED_MONTHS`**: `git log -S '[[<slug>]]' --since="<ARCHIVE_UNCITED_MONTHS> months ago"` returns empty; grep repo for `[[<slug>]]` returns only the file itself.
   - **No active decision references it:** check `decisions/*.md` for `[[<slug>]]` matches.
   If any criterion fails, report to user and ask if they want to override. Do not override silently.
3. Move: `git mv <path> archive/<path>` (creates `archive/<subfolder>/<file>` preserving structure).
4. If the archived file has `supersedes:` or is cited by a current file, add a note to the archive/ version stating which file replaced it (for historical continuity).
5. Regenerate INDEXes: `python3 scripts/rebuild-indexes.py`. The source folder's INDEX.md will lose the entry; archive/INDEX.md (if configured for listing) will gain it. Stage all modified INDEX.md files.
6. Commit: `archive: <slug>`. Push.
7. Release the lock.
