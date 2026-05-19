# Voice plugin — `/write-as`

Optional plugin that adds the `/write-as` skill: draft text in the active user's voice using a personal voice-imitation system (style card + reverse-prompt pairs).

## Installation

To enable the `/write-as` skill in this project:

1. Copy `.claude/skills/write-as/` from this plugin directory to your main `.claude/skills/` directory:

   ```bash
   cp -r plugins/voice/.claude/skills/write-as .claude/skills/
   ```

2. Create your personal voice folder at `team/<your-slug>/voice/`. Use the scaffold in `plugins/voice/team-voice-template/` as a starting point:

   ```bash
   mkdir -p team/<your-slug>/voice
   cp plugins/voice/team-voice-template/style-card.md team/<your-slug>/voice/
   cp plugins/voice/team-voice-template/reverse-prompts.md team/<your-slug>/voice/
   ```

   Then fill in the two files with your own voice samples and rules. Optional: also add a `corpus.md` of 15–20 raw writing samples to derive the style card from (no AI-assisted drafts — use only pure human-written text).

3. Declare the active user in `SOUL.md` at repo root (gitignored). Add a line:

   ```
   Active user: <your-slug>
   ```

   The skill resolves the active user from this line. If absent, the skill aborts with a clear message.

## How it works

`/write-as` loads `team/<active-user-slug>/voice/style-card.md` into context, then stitches register-matched prompt→sample pairs from `reverse-prompts.md` as few-shot examples, and produces a single draft in your voice.

The voice system is keyed to the active user only — it does not ghostwrite for third parties.

## Files

- `.claude/skills/write-as/SKILL.md` — the skill definition (move into your main `.claude/skills/` to activate)
- `team-voice-template/style-card.md` — template for the per-user style card
- `team-voice-template/reverse-prompts.md` — template for the per-user prompt→sample pairs
