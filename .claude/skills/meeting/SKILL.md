---
name: meeting
description: "Save a meeting/call transcript to the project-kb and propagate its contents. Writes meetings/YYYY-MM-DD-<counterparty>-<topic>.md (digest on top via mandatory ## TL;DR, full verbatim transcript collapsed at the bottom), then EXTRACTS action items, strategy/positioning insights, contacts met, and shared artifacts — and propagates each (after confirming with the user) to todos/, strategy/ (or brainstorming/), advisors/, and raw/. Wires bidirectional wikilinks. Respects the single-writer lock; commits + pushes each artifact atomically. Use when the user says: save this meeting, log this call, here's a transcript, record our meeting with X, add this Otter/Granola/Fireflies transcript. Do NOT use for a pure customer-discovery digest with no transcript (use /add-entry interview) or a quick URL capture (use /drop)."
---

# /meeting — Save a meeting + propagate its contents

The defining feature of this skill is **propagation**: a meeting file is a *source*, not a destination. `/add-entry` files one thing in one place; `/meeting` files the record AND fans the load-bearing bits out to where they're actionable.

Required reading first time: `CONVENTIONS.md` (esp. §"Single-writer rule", §"Commit convention", §inference discipline), `schema/kb-schema.yaml` (`meeting` type), `meetings/README.md`.

## Steps

1. **Acquire the single-writer lock.** Check `runs/.lock`. If it exists, abort with "another agent is writing, retry later." Otherwise write `<session-id> <ISO-timestamp>` to it. Release it in the final step (and on any abort).

2. **Acquire the transcript + metadata.** The user pastes the transcript, gives a file path, or points at a recording. Elicit (or infer from the transcript header) what's needed for frontmatter:
   - **Date** (meeting date → `date_found` + filename). If only "today", use today.
   - **Participants** (list — names + roles where known; "Unknown" is acceptable, don't invent names).
   - **Counterparty kind** — `advisor | customer | investor | partner | internal | networking | other`.
   - **Product** — `track-a | track-b | shared`.
   - **Topic** (→ slug + title).
   - **Source** — how it was captured (Otter / Granola / Fireflies / live notes / recording).
   - Ask only for what you can't infer. Don't stall the save on optional fields.

3. **Write the meeting file.** Copy `schema/templates/meeting.md` → `meetings/YYYY-MM-DD-<counterparty-slug>-<topic-slug>.md` (lowercase, hyphenated, slug ≤ ~50 chars). Fill:
   - Frontmatter — all required fields (`title, type, product, date_found, participants, counterparty_kind, status`). `status: reviewed`. Write a `description:` (≤120 chars, rule-not-summary, no wikilinks/links). Set `redacted: true` if the meeting is sensitive/NDA and scrub accordingly.
   - **`## TL;DR`** (mandatory — lint enforces it) — 3–5 bullets a future agent reads *instead of* the transcript.
   - `## Key points / advice`, `## Action items` (`[ ]` checkboxes), optional `## Strategy / positioning notes`, `## Notable quotes`, `## Artifacts shared`.
   - **`## Transcript`** — paste the FULL verbatim transcript inside the collapsed `<details>` block, unedited. This is the record; never trim it for length.
   - **Inference discipline (load-bearing):** the digest reports what the transcript SAYS, not what it implies. Preserve hedges (`maybe`, `we should ask`, `e.g.`). Attribute advice to the speaker. A timeline/dependency about us is not a commitment by the counterparty. When unsure, quote. (CONVENTIONS §inference discipline.)

4. **Extract propagation candidates.** Read the transcript and the digest you just wrote, and collect candidates in four buckets:
   | Bucket | Looks like | Destination |
   |---|---|---|
   | **Action items** | "we should do X", "ask about Y", "send them Z", a deadline | `todos/` (one file each, via the `/add-todo` shape) |
   | **Strategy / positioning** | a GTM/positioning/pricing/competition insight worth keeping | `strategy/` if it's a settled stance; `brainstorming/` if still open |
   | **Contacts** | a person worth tracking (advisor, mentor, intro) | `[[wikilink]]` in the meeting's `related:` now; offer an `advisors/<slug>/` stub if they'll recur |
   | **Artifacts** | files/links exchanged | `raw/` (binaries: decks, PDFs, recordings) or `tools/` (utilities) — note them; the user supplies the actual files |
   | **Resolved threads** | the meeting *settles* an open question recorded elsewhere — a `## Open threads` bullet, a `[?question]` / `[?decision]` tag, a pending decision | inline **resolution stamp** on that doc (CONVENTIONS §"Resolution stamps"), NOT a supersede/rewrite. `**Resolved YYYY-MM-DD → [[meetings/<file>]]:** <one line>` at the head of the resolved bullet; back-link from the meeting's `## Related`. |

5. **Confirm before writing — every propagation.** Present the candidates as a grouped checklist and let the user approve/edit/drop each. **Nothing in step 4 is written without explicit confirmation.** This is the inference-discipline gate: transcripts overflow with "maybe" and "we should look into" that an eager agent rounds up into commitments. Default to *fewer*, higher-confidence propagations; it's cheap to add another later. For todos, confirm the deadline — never invent one; if the transcript gives no date, ask or leave it out.

6. **Write the approved propagations.**
   - **Todos** → `todos/<deadline>-<slug>.md` per `schema/templates/todo.md` (`type: todo`, `kind:` if event/meeting, `status: pending`, `priority`, `created_at:` today, `related:` wikilinks back to the meeting + any entity). Match `/add-todo`.
   - **Strategy / brainstorm** → `strategy/YYYY-MM-DD-<slug>.md` or `brainstorming/YYYY-MM-DD-<slug>.md` per the matching template. Cite the meeting: `[[meetings/<file>]]`.
   - **Advisor stub** (only if user opts in) → `advisors/<slug>/README.md` per `schema/templates/advisor.md`.
   - **Resolution stamps** → edit the host doc in place: `**Resolved YYYY-MM-DD → [[meetings/<file>]]:** <one line>` at the head of the resolved bullet, original text left below. No new file, no `supersedes:` frontmatter, host doc stays live.
   - **Bidirectional wikilinks:** every propagated file links back to `[[meetings/<file>]]`, and the meeting's `## Related` lists each propagated file. Both sides know about the link.

7. **Regenerate INDEXes + lint.** `python3 scripts/rebuild-indexes.py`, then `python3 scripts/kb-lint.py <changed files>`. Fix content (or amend schema in a separate `schema:` commit) on failure — never `--no-verify`.

8. **Commit + push — one atomic commit per artifact, push after each** (CONVENTIONS §"Commit convention", §"Commit + push together"):
   - `meeting: add <date>-<slug>` — the meeting file (+ regenerated `meetings/INDEX.md`)
   - `todo: add <deadline>-<slug>` — each todo
   - `strategy: add <date>-<slug>` / `brainstorm: add <date>-<slug>` — each insight doc
   - `advisor: add <slug>` — the stub, if created
   - `<host-prefix>: resolve <host-slug> thread` — each resolution stamp (prefix = the stamped doc's type, e.g. `brainstorm: resolve <slug> thread`)
   Each commit ends with the `Co-Authored-By:` trailer per CONVENTIONS.

9. **Release the lock.** `rm runs/.lock`.

10. **Report.** Summarize: the meeting file path + every propagated artifact, as a short list, so the user sees the fan-out.

## Notes

- **Customer/prospect meetings:** the verbatim transcript still lives in `meetings/`. If the call warrants a discovery digest, ALSO create a `discovery/` `type: interview` file (themes, objections, quotes keyed to the firm) that links to the full transcript here — don't duplicate the transcript into `discovery/`.
- **Recurring counterparty:** if someone already has an `advisors/<slug>/` or `discovery/<firm>/` folder, still file the transcript in `meetings/` and link it from their folder. Don't move the transcript into the entity folder.
- **Privacy:** `redacted: true` + scrub for NDA/sensitive meetings before committing. Git history is permanent.
