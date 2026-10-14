---
name: raw/renders — HTML/PDF renders of KB docs
description: "HTML/PDF renders of KB docs (one-pagers, briefs, updates); each names its source .md; never the repo root"
type: folder
---

# raw/renders/

Rendered copies of KB documents made for sending or printing (one-pagers, briefs, investor updates). The markdown file is canonical; a render is a snapshot of it on the date in its filename and goes stale when the source changes.

**File naming:** `YYYY-MM-DD-<slug>.html` (or `.pdf`). Say in the first lines (an HTML comment is enough) which `.md` it was rendered from, e.g. `<!-- rendered from strategy/YYYY-MM-DD-example-one-pager.md -->`.

**Never at the repo root.** Renders go here even when a user-level or tool default says "write HTML in the current directory".

Before sending a render, check that its source `.md` hasn't changed since the render date; if it has, re-render rather than sending the stale copy.
