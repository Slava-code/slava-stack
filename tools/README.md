---
type: folder
description: "Per-tool folders — each holds a README (tool entry) + optional manuals/playbooks/changelogs as tool-note files"
---

# tools/

> The auto-generated list of entries lives in [`INDEX.md`](INDEX.md) — rebuilt by `scripts/rebuild-indexes.py` from each tool folder's README `description:`. Do not hand-edit INDEX.md.

**Per-tool folders.** Each tool we use or reference gets its own folder: `tools/<slug>/`. Inside each folder:
- `README.md` — canonical tool entry (`type: tool`). For light tools, a one-line body is fine. For heavy tools, the README can be a full manual with H2s.
- Optional companion files — `manual.md`, `operational-playbook.md`, `changelog.md`, dated event notes, etc. Each is `type: tool-note` with `tool: <slug>` matching the parent folder. Pick filenames that read in `ls` (lowercase, hyphenated).

Mirrors the `advisors/<slug>/` and `discovery/<firm>/` pattern. One entity = one folder. Light entries stay light; heavy entries get the room they need without polluting `brainstorming/` or `sources/` with operational content.

**A tool is *an address you revisit*. A source is *a claim about the world*.** Different jobs:
- If we use it operationally (CLI, plugin, MCP server, GPT, web tool, reference doc we open repeatedly) → `tools/<slug>/`.
- If it's external content we digest but don't operate (paper, article, op-ed, repo we studied but don't run) → `sources/`.

**This is one of three folders written unprompted** (alongside `sources/` and `inbox/`). When the user shares a useful tool or URL, file it here without asking.

## Slug rules

- Kebab-case, no date prefix. Slug = folder name.
- Match the tool's canonical name when possible (e.g. `example-cli`, `example-mcp-server`, `example-icon-library`).
- Drop articles only when they hurt readability.

## When to add a tool-note vs grow the README

- README absorbs setup + key constraints inline if it fits in ~60 lines and one reader could digest it in one sitting.
- Split out a `tool-note` when:
  - The README becomes hard to scan (more than ~80 lines, multiple operational concerns mixed).
  - There's a repeatable runbook for failure recovery → `operational-playbook.md`.
  - You want a separately-dated artifact (token rotation log, breaking-change notice) → `2026-MM-DD-<event>.md` with `kind: notes` or `changelog`.
  - There's a long-form walkthrough that's not setup but a deep-dive → `manual.md`.

## Frontmatter

**For `README.md`** (the tool entry): `type: tool`, `title`, `product`, `url`, `kind:` (web-app | gpt | cli | api | template | reference-doc | gist | plugin | mcp-server), `date_found`, `tags`, `status`, plus standard `description:`. Schema: [../schema/kb-schema.yaml](../schema/kb-schema.yaml) §`tool:`. Template: [../schema/templates/tool.md](../schema/templates/tool.md).

**For companion files** (`type: tool-note`): `type`, `tool:` (must match parent folder name), `kind:` (manual | playbook | changelog | notes), `date_found`, `status`, plus optional `title`, `source`, `tags`, `product`. Schema: §`tool-note:`. Template: [../schema/templates/tool-note.md](../schema/templates/tool-note.md).

## Separate from

- `sources/` — academic-style factual digest of external content. If it's a paper/post/op-ed we studied (not a tool we use), it goes there.
- `inbox/` — temporary triage queue. Tool entries live permanently in `tools/`.
- `raw/` — founder-authored binaries (decks, recordings).
- `brainstorming/` — opinion/analysis. If you're writing "here's what I think about this tool," that's a brainstorm; the tool itself stays factual in its `tools/<slug>/` folder.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md).
