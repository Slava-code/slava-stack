---
name: write-as
description: "Draft anything the active user will send or publish, in their voice: email, reply, DM, application answer, bio, script, X or LinkedIn post. Gathers the facts from STATE.md and the KB first, then applies the voice card. Use when the user says: draft, write, reply to, respond to, help me answer, make this sound like me, iterate on this. Not for third-party ghostwriting, code or KB documents."
---

# /write-as — draft in the active user's voice

## 0. Resolve active user

The voice system is per-user. Resolve the active slug before doing anything else.

1. Read `SOUL.md` at repo root. Look for an `Active user:` line declaring a slug (e.g. `founder-template`). If absent, stop and tell the user: *"No active user declared in SOUL.md — voice is per-user. Add `Active user: <your-slug>` to SOUL.md and set up `team/<your-slug>/voice/` first (see `plugins/voice/team-voice-template/` for a scaffold)."*
2. Confirm `team/<slug>/voice/style-card.md` exists. If missing, fall back: see § "Missing voice folder" below.

## 1. Collect the facts before any prose

A draft in a perfect voice with an invented fact is worse than no draft. Before writing:

1. Every statement about us (what we did, numbers, customer status, pricing, dates, program outcomes) must come from `STATE.md` (the always-loaded current-truth card, if your KB has one) or from a KB file you open in this session.
2. Open the recipient's or program's hub (resolve the name through `ALIASES.md`: e.g. `advisors/<slug>/README.md`, `competitions/<program>/README.md`, `discovery/<firm-slug>/README.md`) and the most recent interaction with them, so the draft does not re-explain what they already know or were present for.
3. For numbers, use the newest file in `traction/` and say nothing it marks as not-for-external-use.
4. If a fact the draft needs is in neither `STATE.md` nor a file you opened, do not guess and do not pull it from the web: leave a `[placeholder]` and name it after the draft.
5. Keep it plain: no internal KB vocabulary, no narration of how the draft was made, one purpose per message.

After the draft, add one line listing the KB files the facts came from, outside the draft text.

## 2. Load the voice system

Read in order:
1. `team/<slug>/voice/style-card.md` — always. This is the system-prompt-equivalent content.
2. `team/<slug>/voice/reverse-prompts.md` — scan the pair register tags. Do NOT load all pairs into your reasoning; pick 4–8 whose registers match the user's ask (see next step).

## 3. Classify the ask, then pick pairs

Identify the register of what the user wants drafted. Common ones (match the table in the user's `style-card.md`):

| If the ask is… | Load pairs tagged… |
|---|---|
| Reply to a customer-service issue / complaint / refund | customer-complaint, warm-professional |
| Email to a co-founder / teammate — strategy dump | strategy-dump, urgent-ping |
| Warm intro / investor / advisor reply | warm-investor, casual-teaching |
| Short X reply to hot-take | one-liner-zinger |
| Longer X reply / conversational thread | x-longform |
| X original post — opinion or take | opinion-with-hedge, diagnosis-prescription |
| LinkedIn recap / narrative post | linkedin-recap |
| Reflective / analytical essay | longform-reflection |
| Raw brainstorm dump | idea-fragments |
| Discovery-call notes | telegraphic |
| Teaching-mode explainer to an acquaintance | casual-teaching |
| Accelerator / fellowship / pitch-competition / residency application answer (short, conviction shape) | reflective + warm-investor + single-arc-bet |
| Accelerator / fellowship / pitch-competition / residency application answer (longer, trajectory shape) | reflective + warm-investor + multi-paragraph-trajectory |
| Customer / pitch follow-up email (post-demo, objection handling) | warm-investor wrapper + bet-language substance (hybrid: warm wrapper, application-register substance inside) |

When in doubt, pick 3 pairs closest to the register and one pair from a different register to prevent over-fitting.

**Register-sensitivity caveat — formal application copy.** When the ask is an accelerator, fellowship, pitch-competition, residency, or any competitive application answer with a hard word/character cap, **dial DOWN the most casual tics** before drafting (suppress `idk`, `imo`, `gonna`, `bruh`, `REALLY` ALL-CAPS, parenthetical self-commentary mid-sentence). Keep the structural voice (hyphens not em-dashes, scare quotes on industry jargon, terminal fragments for emphasis, anglo-saxon vocabulary, personal-anchor → general-lesson arc). See the active user's `style-card.md` for the full register rules.

**Register-sensitivity caveat — customer / pitch follow-up email.** When the ask is a follow-up email to a prospect after a demo or pitch call (especially when the prospect raised a substantive objection on the call), engage the active user's `style-card.md` § "Warm-prospect / customer-pitch follow-up mode" for voice rules — read it before drafting. Then apply these **substance defaults** BEFORE writing prose:

1. **Prospect-specific example questions.** If the email uses a concrete "imagine asking this" example to demonstrate the product's value, it must use the prospect's actual operating-model vocabulary — not a generic template. A generic framing signals "we didn't do the homework" and undercuts the substantive argument. Surface the prospect's actual workflow language. The example should require synthesis across multiple data sources — single-tool examples defeat any cross-tool pitch. If you don't know the prospect's operating shape, surface it via a quick subagent web research pass before drafting.

2. **Common objections — identify the form before rebutting.** Many objections come in multiple flavors. Each needs a different rebuttal, and defending against the wrong form makes the email a strawman.

   **Before drafting:**
   - If the conversation context makes the prospect's specific form clear, argue against that form.
   - **If unclear, ask the active user to quote the prospect's actual phrasing before drafting.** Don't guess and don't default to a generic version — the wrong form produces a strawman.
   - Hedge absolute denials. Absolute denial reads naive to a technical reviewer.

## 4. Draft

Apply `style-card.md` rules. Specifically enforce:

- The right **opener** for the register (per the table at the end of `style-card.md`)
- The right **closer** (usually `Best, <FirstName>` for email; none for X/casual)
- **Anti-slop list** from `style-card.md` — treat these as hard bans
- **Hedge-parens, ALL CAPS on key words, hyphens-not-em-dashes, terminal fragments** — use if the register supports them, don't force
- **Preserve register-appropriate typos / lowercase abbreviations** (`idk`, `imo`, `gotta`) — don't over-polish

Output the draft with no preamble ("Here's the draft:"), no postscript ("Let me know if you want changes") and no multiple versions. The only additions allowed after the prose are the source line from step 1 and any `[placeholder]` list.

If the user gives iteration feedback ("shorter", "less enthusiastic", "add a P.S."), revise in-context — no need to re-invoke the skill.

## 5. When ambiguous — one question, then draft

If the ask is genuinely unclear (e.g., "draft something about the hackathon" — but which register? LinkedIn, X, email?), ask **one** clarifying question about register/audience/length. Then draft. Don't ping-pong.

## Missing voice folder

If `team/<slug>/voice/` doesn't exist:

Tell the user: *"You don't have a voice system set up yet. Copy the structure from `plugins/voice/team-voice-template/` — you'll need `corpus.md` (15–20 pure samples, no AI-assisted drafts), `style-card.md` (distilled voice rules), and `reverse-prompts.md` (prompt → sample pairs). Once set up, rerun `/write-as`."*

Do NOT attempt to draft generically. Voice requires the source material.

## When NOT to use /write-as

- **Writing as a third party.** The voice system is keyed to the active user only.
- **Summaries, code, internal notes.** Voice matters for prose the user will send/publish — not for internal scaffolding.
- **Documents that belong in the KB.** Source digests, decisions, synthesis, comparisons follow CONVENTIONS, not personal voice. Use `/add-entry`.
- **Short factual replies.** If the user is just asking you to fill in a yes/no or a URL, don't invoke the whole pipeline.

## Iteration note

This skill is read-only — it never writes to the KB or commits. If the user wants the draft saved, follow up with `/add-entry` separately.
