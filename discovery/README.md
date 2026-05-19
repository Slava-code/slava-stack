---
type: folder
description: "Customer discovery — interviews (post-call quote capture) and leads (pre-call signup/outreach log)"
---

# discovery/

**Customer / prospect material, pre- and post-call.** The highest-signal content in the KB once business development is active. Two file types live here:

- **`type: lead`** — pre-call prospects from inbound channels (website demo form, warm referrals). Tracks the outreach loop before the first call: signup metadata, OSINT, emails sent, scheduling. Promote into `type: interview` once a call happens and there are quotes/themes worth preserving.
- **`type: interview`** — post-call capture: context, verbatim quotes, themes, objections, follow-ups.

**Default pattern:** entity folder per firm once calls accumulate. One-off calls and early leads stay flat.

```
discovery/
├── YYYY-MM-DD-<lead-slug>-lead.md              type: lead, flat
├── YYYY-MM-DD-<other-lead>-lead.md             type: lead, flat
├── YYYY-MM-DD-acme-capital-partner-call.md     type: interview, flat
└── acme-capital/                               entity folder (2+ events)
    ├── README.md                               current state of relationship
    ├── YYYY-MM-DD-partner-intro-call.md        type: interview
    └── YYYY-MM-DD-followup.md                  type: interview
```

**File naming (flat):** `YYYY-MM-DD-<identifier>-<kind>.md`
- Leads: `YYYY-MM-DD-<lead-slug>-lead.md`
- Interviews: `YYYY-MM-DD-acme-capital-partner-call.md`

**File naming (entity folder):** `<firm-slug>/README.md` + dated call / event files. Promote from flat → folder on second interaction.

## Lead files (`type: lead`)

**Frontmatter required:** `type: lead`, `product:`, `status: new | contacted | demo-booked | demo-completed | converted | dead`, `date_found:`, `email:`.
**Frontmatter optional:** `name`, `firm`, `persona`, `stage`, `tags`, `redacted`, `description`.

**Structure:** Context (source, signup time, captured fields) · Research (public OSINT, sourced) · Outreach log (emails sent, replies received, times offered, verbatim) · Next step.

**Status progression:** `new` (just signed up) → `contacted` (outreach sent, awaiting reply) → `demo-booked` (time scheduled) → `demo-completed` (call happened) → `converted` / `dead`.

**Promotion to interview:** when the demo call happens and produces quotable content, create a sibling `type: interview` file (or promote the lead folder → entity folder if interactions recur). Keep the lead file as the pre-call record; don't delete.

## Interview files (`type: interview`)

**Structure (per-call file):**
1. Context: who, what firm, what stage (discovery / validation / pilot / paying), what triggered the call
2. Verbatim quotes (most valuable part — preserve voice)
3. Themes observed
4. Objections / concerns raised
5. Follow-ups committed

**Frontmatter required:** `type: interview`, `product:`, `persona: <role>`, `stage: discovery | validation | pilot | paying`, `firm:`, `confidence:`, `status:`, `redacted: true | false`. Persona values are project-specific — define your own set in `schema/kb-schema.yaml`.

**Privacy:** if discussing a firm under NDA or sharing sensitive details, set `redacted: true` and scrub identifying details beyond what's safe to version-control. Git history is the repo's memory.

**Written on:** leads after each inbound signup or outreach event; interviews after each call, when asked to log it.

Rules: [../CONVENTIONS.md](../CONVENTIONS.md). Entries: [INDEX.md](INDEX.md) — auto-generated.
