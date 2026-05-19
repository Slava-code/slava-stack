---
name: study
description: "Start or resume a /study session on a source or concept in the project-kb. Source sessions deepen understanding of a specific paper/article/repo already digested in sources/; concept sessions tackle cross-cutting themes (example-concept-a, example-concept-b, etc.) as a folder under concepts/ with README (research digest) + study-log (append-only checkpoints). Writes one H2 checkpoint at session end — not mid-session. [?question] / [?decision] tags stay inline until user explicitly asks to promote. Bidirectional cross-refs when a session touches other sources/concepts. Respects the single-writer lock. Use when: user says 'study X', 'let's learn Y', 'start a study session on Z', 'continue studying W', 'study the concept of V', 'walk me through paper U'. Do NOT use for ambient KB Q&A — that's CLAUDE.md §'KB-first for named-entity queries' (no session needed). Do NOT use for brainstorming (use the brainstorm template via /add-entry). Do NOT use if the user wants to quickly capture something (/drop)."
---

# /study — Deep-study session on a source or concept

Opens an interactive study session. Teaches the material in chunks, appends one durable H2 checkpoint to the matching `study-sessions/<filename>.md` (for sources) or `concepts/<slug>/study-log.md` (for concepts) at session end.

## Arguments

- **`/study <source-slug>`** — study an existing source (filename prefix match in `sources/`). Example: `/study example-paper`.
- **`/study <concept-slug>`** — study a concept (folder under `concepts/`). Example: `/study example-concept`. If the folder doesn't exist, prompts to create it.
- **`/study next`** — invoke `/study-unstudied`, pick the top suggestion, confirm with user, proceed.
- **`--mode text|voice`** — renderer mode. Default `text`. Voice mode = stub for v0 (shorter chunks, no tables, progressive disclosure). Retrieval is identical in both modes.

## Required reading first time

- [CONVENTIONS.md §"Study logs — checkpoint + cross-reference rules"](../../../CONVENTIONS.md)
- [study-sessions/README.md](../../../study-sessions/README.md)
- [concepts/README.md](../../../concepts/README.md)
- [schema/templates/study-log.md](../../../schema/templates/study-log.md)
- [schema/templates/concept.md](../../../schema/templates/concept.md)

## Flow

### 1. Resolve target

Parse argument. Fuzzy-match if needed:

- First try exact filename match in `sources/` (strip date prefix for user ergonomics): `sources/*-<arg>-*.md` and `sources/*-<arg>.md`
- Then try `concepts/<arg>/`
- Then try slug-contains / tag-match / title-keyword across `sources/` + `concepts/`
- If ambiguous, print candidates, ask user to pick
- If zero matches: ask "this looks like a concept — create `concepts/<slug>/`?"

### 2. Check for existing study log

- **Source session:** does `study-sessions/<source-filename>.md` exist?
- **Concept session:** does `concepts/<slug>/study-log.md` exist (and non-empty)?

If yes → **resume mode**. Invoke `/study-status` internally to pull latest checkpoint summary; open the session with:

```
Picking up from [[study-sessions/<X>]] §checkpoint-<N> (<date>):

- Last session intent: <next_session_intent from prior checkpoint>
- Open threads: <bullet list from prior Open threads section>
- Recent checkpoints (last 3): <...>

Continue this thread, or start a new angle?
```

If no existing log → **new session mode**.

### 3. New session setup — source mode

- Acquire `runs/.lock` (briefly, to create the study-log file). Write `<session-id> <ISO-timestamp>` to the lock.
- Copy `schema/templates/study-log.md` → `study-sessions/<source-filename>.md`. Fill frontmatter:
  - `title:` `"Study log — <source title>"`
  - `type:` `study-log`
  - `description:` per template rule (≤120 chars, stable, no wikilinks)
  - `product:` inherit from source
  - `source:` `[[sources/<source-filename>]]`
  - `brainstorm:` `[[brainstorming/<matching-brainstorm>]]` if one exists, else omit
  - `date_found:` today
  - `last_checkpoint:` today
  - `status:` `ongoing`
  - `tags:` inherit from source
- Leave body empty (no placeholder checkpoint yet — the first real checkpoint is written at session end).
- Release the lock.
- **Dispatch a subagent** (Explore or general-purpose) to deep-read the source + matching brainstorm, return a teaching plan (2–4 main concepts to cover, 3–5 suggested questions to probe).
- Present the teaching plan to the user. Confirm before proceeding.

### 3b. New session setup — concept mode (concept folder doesn't exist)

- Ask user to confirm concept slug + 1-paragraph definition scope.
- Acquire `runs/.lock`.
- Create `concepts/<slug>/` directory.
- Copy `schema/templates/concept.md` → `concepts/<slug>/README.md`.
- **Dispatch a subagent** to run the initial concept research:
  - Grep the KB for sources/brainstorms/decisions/questions/comparisons touching this concept
  - Web-search for 5–10 authoritative external signals (papers/articles/projects)
  - Return a draft `README.md` body (definition + KB signals + external signals + scoping question)
- Present the draft to the user. User confirms or edits. Finalize `README.md`.
- Copy `schema/templates/study-log.md` → `concepts/<slug>/study-log.md`. Fill frontmatter with `concept: [[concepts/<slug>]]` (no `source:`).
- Release the lock. Proceed to teach.

### 4. Teach in chunks (progressive disclosure)

- One concept at a time. Explain, then confirm: "got it? or want to push on this?"
- If user has questions → answer, then check in.
- User may say "make this a question" or "draft a decision" mid-session → **prompted promotion only**: pick up the relevant text, invoke `/add-entry` for the right type, append the new artifact's wikilink under "Artifacts created this session" in the draft checkpoint. Never auto-create.
- If the session pulls in related sources → note them (they'll trigger the cross-ref write at session end).

### 5. End-of-session checkpoint — draft + user confirm

When user signals end-of-session ("that's enough for today", "let's wrap", "save it"):

Draft a checkpoint block following `schema/templates/study-log.md`:

```markdown
## Checkpoint — <YYYY-MM-DD> (session <N>)

**What we covered**
- <bullet>

**What I now understand**
- <delta>

**Candidate questions / decisions** (flagged, not created)
- [?question] <tag>
- [?decision] <tag>

**Related sources touched**
- [[study-sessions/<other>]] §checkpoint-<M> — <one-line note>

**Open threads → next session**
- <resume hint>
```

Rules:
- Full sentences, not shorthand — voice-portability
- `[?question]` / `[?decision]` tags inline, only for candidates user flagged or for ones the agent is surfacing with explicit user acknowledgement
- **Never promote tags to `questions/` / `decisions/` automatically**. If user already asked to promote mid-session, that happened then; don't re-promote from tags at end.

Show draft to user. Wait for confirm or edits.

### 6. Write + cross-refs + commit

- Acquire `runs/.lock`.
- Append the confirmed checkpoint to the primary study-log file.
- Update its frontmatter `last_checkpoint:` to today.
- **For each entry in "Related sources touched":**
  - Append a short reciprocal checkpoint to the referenced study-log file (create it first if it doesn't exist — same new-session-setup, skip teaching):
    ```markdown
    ## Cross-ref — <YYYY-MM-DD> (from [[study-sessions/<primary>]] session <N>)

    Touched briefly: <one-sentence angle>. Full context in <primary> checkpoint <N>. No primary study progress here.
    ```
  - Update referenced file's `last_checkpoint:` too.
- Run `python3 scripts/rebuild-indexes.py` to refresh affected INDEX.md files.
- Run `python3 scripts/kb-lint.py` to verify frontmatter.
- Stage all modified files. Commit with prefix `study:`:
  - Source session: `study: checkpoint <source-slug> session <N>`
  - Concept first session: `study: seed concept <slug> + session 1`
  - Concept later session: `study: checkpoint <slug> session <N>`
- `git push`.
- Release the lock.

### 7. Close

Brief confirmation to user: "session <N> logged to [[study-sessions/<X>]] §checkpoint-<N>. Cross-refs written to: <list>. Next session intent: <repeat from checkpoint>."

## Promotion (user-prompted only)

If user says "promote the [?question] to questions/" or similar:
- Find the tagged line (grep `[?question]` or `[?decision]` in the relevant checkpoint)
- Extract the text after the tag
- Invoke `/add-entry` for type `question` or `decision` — let that skill handle template + frontmatter
- In the question/decision body, add `## Related` section with `[[<source-study-log>]] §checkpoint-<N>` as the provenance pointer
- Append to the session's checkpoint under a new section `**Artifacts created this session**` with the new wikilink + short "why now" gloss
- Never do this without explicit user ask.

## Voice mode stub

`--mode voice` today:
- Suppress markdown tables (not dictation-friendly)
- Replace wikilink render with natural phrasing: "the <source> study log checkpoint 2" instead of "double-bracket study dash sessions slash..."
- Chunk explanations smaller (1–2 sentences per chunk, explicit "continue?" prompts)
- Retrieval identical to text mode

Full voice renderer deferred until real walk sessions surface needs.

## Interruption handling

- If user drops off mid-session and returns later, another `/study <same-slug>` picks up via resume mode (§2).
- If session is cut short before end-of-session checkpoint, no durable write happens — learning is lost. Design tradeoff: simpler state machine over interruption-safety. If this becomes painful in practice, add mid-session draft saves.
- If the lock was acquired and session crashed, manual override: `rm runs/.lock`.

## What `/study` is NOT

- **Not `/kb-synthesize`.** No architecture snapshots produced.
- **Not `/add-entry` with a brainstorm.** Opinions about project-angle belong in `brainstorming/`. Study logs capture *learning process*.
- **Not automated.** No auto-promotion, no auto-cross-link-discovery beyond what user names in-session.
