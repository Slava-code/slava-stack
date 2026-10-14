---
name: raw/emails — verbatim external email threads
description: "Verbatim external email threads (intros, scheduling, deal comms); primary artifact that entity files cite"
type: folder
---

# raw/emails/

Verbatim email threads with external counterparties (intros, scheduling, deal comms) — the **primary artifact**. Digested state lives in the entity file that owns the relationship ([`../../discovery/`](../../discovery/) lead or interview, [`../../advisors/`](../../advisors/) profile, [`../../competitions/`](../../competitions/) hub) and **cites back here** rather than copying, so the outreach log stays a one-liner per event and the exact words stay recoverable.

Distinct from [`../transcripts/`](../transcripts/) (verbatim meeting and session transcripts, cited by line from `meetings/` notes). Emails have no digest of their own — the citing entity file is the digest.

**File naming:** `YYYY-MM-DD-<counterparty-or-thread-slug>.md` — date = latest message in the thread at save time. Message order preserved, headers kept (from / date / to), body text unchanged. Carries `type: source` + a `description:` so it appears in the parent INDEX. Update the same file (bump `date_found`, append messages) when the thread continues.

Cite from elsewhere with the relative path, e.g. `[[../raw/emails/YYYY-MM-DD-example-intro-thread]]`.
