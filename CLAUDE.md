# project-kb — agent entry

A closed-loop, AI-native knowledge base for running a startup: research, decisions, brainstorms, experiments, competitor analyses, customer and advisor conversations, strategy, GTM, fundraising, cash flow. Git-backed and shared by the whole team across machines, so everything an agent needs is in the repo, not in machine-local memory.

## What is always in your context

- This file, and the two files it imports below: `STATE.md` (what is true about the project right now) and `ALIASES.md` (shorthand → canonical name → file to open).
- `.claude/rules/kb-retrieval.md` (which file wins, inference discipline) and `.claude/rules/drafting.md` (anything the team will send or publish). `.claude/rules/kb-writes.md` and `.claude/rules/research-framing.md` load when you read content files.
- Hook output (`.claude/settings.json`): at session start, a staleness report and, if present, the gitignored `SOUL.md` (chat tone only; it never changes how documents are written). On each prompt, the KB files that match it. Treat that list as "open these first", not as the answer.

@STATE.md

@ALIASES.md

## Answering

1. Questions about us, a person, a company, a program, or "what did we do": the answer is in the KB. Start from `STATE.md` and `ALIASES.md`, open the files they and the prompt hook point to, and only then answer. First-person phrases ("our pilot", "what we built", "the meeting last week") are KB queries even though nothing is named.
2. If the KB has it, the KB wins; the web extends it, never replaces it. If the KB is silent, say so and ask.
3. Comparing anything to your product: ground our side first. See `AGENT-GUIDE.md` § "Comparison protocol".
4. Drafting anything outbound: `.claude/rules/drafting.md`; `/write-as` if the optional voice plugin (`plugins/voice/`) is installed.

## Writing

Read `CONVENTIONS.md` (rulebook) and `AGENT-GUIDE.md` (where things go) before the first write of a session; do not guess a convention. Skills do the filing: `/add-entry`, `/meeting`, `/add-todo`, `/complete-todo`, `/finance`; `/kb` lists them all. One writer at a time (`runs/.lock`; browser-tool sessions count as writes). Git hooks lint every commit and push it.

Two things every write must leave true:

- **`STATE.md` matches reality.** If what you filed changes an outcome, a status, a number or a price, update the line and its `as-of:` date in the same session.
- **Old files say they are old.** A new version back-stamps the one it replaces; a closed thread gets an outcome banner on the files that still read as open.

Optional active-user preferences: if `SOUL.md` declares an active user (e.g. `Active user: founder-template`), read `team/<slug>/preferences.md` and apply it to the main agent's writes. Subagents don't load it.

## Map

| Need | Where |
|---|---|
| Folder purposes and one-line listings | `INDEX.md`, then `<folder>/INDEX.md` (auto-generated; superseded entries are tagged) |
| Vocabulary | `GLOSSARY.md` |
| Hubs (current truth per entity) | `discovery/<firm>/README.md`, `competitions/<program>/README.md`, `advisors/<person>/README.md` |
| Scope boundaries, human quickstart, reading paths | `LIMITS.md`, `USER-MANUAL.md`, `READING-GUIDES.md` |
| Gitignored, on disk only | `team/<slug>/private/` (`grep -r` finds it; the lookup script skips it unless `KB_LOOKUP_INCLUDE_PRIVATE=1`) |

History of "when did we X": `git log --follow <file>`.
