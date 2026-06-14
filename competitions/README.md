---
type: folder
description: "External competitions & multi-round programs we enter — entity-folder per program (logs, forms, snapshots, results)"
---

# competitions/

**External competitions and multi-round programs the project enters** — pitch competitions, accelerator/fellowship challenges, structured venture programs. The defining feature is *accumulation over time*: a single program throws off a stream of artifacts (experiment logs, submission snapshots, organizer forms, inbound correspondence, round results, deliverables) across multiple stages and deadlines.

**Default pattern: entity folder per program.** Mirrors `advisors/<person>/` and `discovery/<firm>/`. Each program gets `competitions/<program-slug>/` holding a hub doc plus dated artifacts.

```
competitions/example-program/
├── README.md                                  program hub: stage, team-id, status, timeline
├── 2026-01-15-example-program.md              competition strategy + rubric + timeline
├── 2026-01-15-venture-snapshot.md             snapshot submitted with the application
├── 2026-01-10-experiment-log-1.md             submitted experiment log (one per learning cycle)
├── 2026-01-20-stage1-organizer-email.md       inbound organizer correspondence
└── submission-form/                           the submission form's field reference (type: tool)
```

Distinct from:
- `strategy/` — reusable positioning / pitch copy that isn't bound to one program (investor blurb, application answers, elevator pitch). A program-specific snapshot or submission lives here; cross-program positioning stays in `strategy/`.
- `sources/` — external *material* we digest (papers, articles). A program's public rules page can be a `source`; the *program* and our submissions to it live here.
- `tools/` — bookmark-class utilities. A program's submission form (field reference we reuse) co-locates here under the program, not in `tools/`.

**Promote a one-off → folder when it accumulates.** A single application (one-shot, no rounds) can stay in `strategy/`. Spin up a `competitions/<slug>/` folder once a program reaches `NEW_FOLDER_MIN_FILES` worth of artifacts or enters a multi-round structure.

**Frontmatter:** the program hub README and dated artifacts keep their natural `type:` (`folder` for the hub, `strategy` / `source` / `tool` for artifacts — lint keys off `type:`, not location). A dedicated `competition` type (with stage/status tracking) is a candidate future schema addition if programs accumulate enough state to warrant it.

**Written on:** when entering a competition/program, submitting to it, or logging a round result or organizer communication.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
