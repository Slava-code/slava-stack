# Reverse prompts — `<your-slug>`

A library of (prompt → sample) pairs that the `/write-as` skill stitches into context as few-shot examples. Each pair shows the skill: "given a prompt like this, here's what your actual writing looks like."

## How to build this file

For each real piece of writing in your `corpus.md` (or wherever you keep raw samples), reverse-engineer a prompt that *could have produced it*. Tag the pair by register so `/write-as` can pick relevant ones.

## Format

```
## Pair <N> — <register-tag>

**Prompt:** <what someone might have asked you to write>

**Sample:**
<the actual text you wrote>
```

## Recommended register tags

Use these so `/write-as` can match pairs to the user's ask:

- `customer-complaint` — reply to a service issue / refund
- `strategy-dump` — email to co-founder / teammate, brain-dump style
- `urgent-ping` — short async ask
- `warm-investor` — warm intro / advisor / investor reply
- `casual-teaching` — explainer to an acquaintance
- `one-liner-zinger` — short X reply
- `x-longform` — longer X reply / conversational thread
- `opinion-with-hedge` — X original post, opinion with measured hedge
- `diagnosis-prescription` — X post structured as "problem → fix"
- `linkedin-recap` — LinkedIn narrative post (event recap, milestone)
- `longform-reflection` — analytical / reflective essay
- `idea-fragments` — raw brainstorm dump
- `telegraphic` — discovery-call notes, internal scratch
- `single-arc-bet` — short application answer, claim-and-bet shape
- `multi-paragraph-trajectory` — longer application answer, history/breadth shape

Aim for 15–20 pairs across the registers you use most. More than 20 starts to dilute few-shot signal.

## Example skeleton

```
## Pair 1 — customer-complaint

**Prompt:** A customer emails saying the product broke on day 2 and they want a refund.

**Sample:**
<your actual reply text here — the real one, not a rewritten version>
```
