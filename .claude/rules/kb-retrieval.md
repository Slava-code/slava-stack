# Retrieval: how to answer from this KB

Always loaded. Each rule below guards against a failure that recurs when agents answer from a KB: stale files read as current, a silent search taken as "not in the KB", a hedge rounded up into a fact.

## Order of work

1. `STATE.md` and `ALIASES.md` are in context. For anything about us (status, customers, traction, pricing, programs, what we did, who someone is), start there, then open the file the line or row points to, plus anything newer on that topic.
2. The prompt hook lists matching files. Open the relevant ones before answering. To search by hand: `python3 scripts/kb-prompt-lookup.py "<terms>"`. It ranks current files first and labels superseded ones.
3. **The built-in Grep and Glob tools follow ignore files.** The root `.ignore` re-includes gitignored `private/` notes for Grep and keeps `raw/transcripts/` and fetch dumps (`runs/fetches/<slug>.txt`) out of default results. To search everything, use `grep -r` in Bash (in zsh, quote globs: `--include="*.md"`).
4. Never say "not in the KB" until you have searched for it. If the KB is silent, say "the KB doesn't say" and ask. Do not fill the gap from the web or from memory, and do not substitute a similarly named thing.
5. An unknown name, acronym or nickname is a KB query first (check `ALIASES.md`, then search), a question to the user second, and a web search last.
6. Read cheaply: a meeting file's notes, not the whole transcript; the newest version of a versioned doc; a hub README's status section.

## Which file wins

- Evidence order: primary text (emails in `raw/emails/`, transcripts in `raw/transcripts/`, customer-written documents) > documents we submitted > `decisions/` > `synthesis/` > `strategy/` > `brainstorming/` and agent-written notes. Within a tier the newest wins. Say which file and date a claim comes from.
- History, not current truth: anything with `status: superseded` or `superseded_by:`; an older `-vN` or `draft-N` sibling; a synthesis older than the files that postdate it.
- An agent-written brainstorm or session note is a hypothesis. A claim about a person or a customer needs a primary source or the team's own words.
- Application and pitch text is not a fact source for numbers or biography: it was written to persuade, in a past week. Use `STATE.md`, the newest `traction/` file and the hubs.
- A pending todo past its deadline means **unknown**, not "not done". Ask before building on it.
- `status: raw` says nothing about whether a file is current; most files carry it.

## Inference discipline

Report what sources say, not what they imply. Inflated claims about customers, advisors and competitors are the dangerous kind because they leak into pitches and outreach.

- Preserve hedges: `e.g.`, `possible`, `target`, `exploring`, `verbal`. "e.g. a subset of Example Co" is not "an Example Co pilot".
- Keep the actor straight: a dependency on our timeline describes us, not the counterparty.
- Cite `file.md:42` in chat when the user may act on the claim. When unsure, quote.
- Absence is not denial: "the KB doesn't say".
- Claims about how a tool, product or API behaves today need a fetched source or the code; otherwise say "unverified".

## Keeping it true

When the user tells you something that changes what is true now (an outcome, a meeting that happened, a number, a correction), fix it where it lives in the same session: `STATE.md` (bump `as-of:`), the hub README, and the stale line you found. Do not leave the correction only in the chat.

## Subagents

Sweeps of this KB use `general-purpose` subagents. `Explore` agents do not load `CLAUDE.md`, `STATE.md` or these rules, so they miss the currency rules. Subagents never drive a browser: when WebFetch cannot read a page, they report "could not fetch" and move on.
