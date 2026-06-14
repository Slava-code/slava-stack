---
name: financial-summary
description: "Generate an on-demand cash-flow summary from the project-kb ledger (finances/ledger.csv) for a given period, persisted to finances/summaries/. Computes total in/out/net, per-category breakdown, top counterparties, pending vs cleared, and notable items; format overridable per call (e.g. 'group by account', 'board format', 'just SaaS'). Use when user says: summarize finances for May, monthly cashflow summary, how did we do financially in Q2, generate a finance summary, spending breakdown for <period>. For one-off lookups ('how much on travel in May?') just read the ledger and answer in chat — no skill needed."
---

# /financial-summary

Generates a formatted, **persisted** cash-flow summary for a period from `finances/ledger.csv`. On-demand only — summaries are never auto-generated on transaction writes.

**Read first (T2):** `finances/README.md` — the ledger schema and category vocab.

**When NOT to use:** a one-off question ("what did we spend on cloud last month?") doesn't need this skill — read `finances/ledger.csv` and answer in chat. This skill is for a *persisted, formatted* period summary.

## Procedure

1. **Acquire `runs/.lock`** (this writes a file).
2. **Resolve the period** from args: a month (`2026-05`), quarter (`2026-Q2`), a date range, or relative ("last month"). Resolve relatives against today's date.
3. **Resolve the format:** default format below, unless the user specified an override ("group by account", "board-update format", "only SaaS/cloud", etc.).
4. **Read `finances/ledger.csv`**, filter rows to the period (`date` in range).
5. **Compute** (exclude `direction: transfer` from in/out totals — report transfers separately):
   - Total **in**, total **out**, **net** for the period.
   - **Per-category breakdown** (outflow by category; inflow by category), sorted by amount.
   - **Top counterparties** by total spend.
   - **Pending vs cleared** split (how much is unconfirmed by a statement).
   - **Notable items** — largest individual transactions; anything flagged.
6. **Write** `finances/summaries/<period>.md` with frontmatter:
   ```yaml
   ---
   type: finance-summary
   title: "Cash-flow summary — <period>"
   period: "<period>"
   description: "<one-line: net / in / out for the period>"
   date_found: <today>
   status: reviewed
   ---
   ```
   Body = the computed sections above, in the chosen format. Note the row count and the as-of date (summaries are point-in-time; the ledger keeps changing).
7. **Regenerate + lint:** `python3 scripts/rebuild-indexes.py finances/` then `python3 scripts/kb-lint.py finances/summaries/<period>.md`.
8. **Commit + push.** Prefix `finance:` — e.g. `finance: summary 2026-05`. Push immediately.
9. **Release the lock.**

## Default format

```
# Cash-flow summary — <period>

**Net: <±$X>**  ·  In: $<in>  ·  Out: $<out>  ·  (Transfers: $<t>)

## Outflow by category
- <category> — $<amount>  (<n> txns)
...

## Inflow by category
- <category> — $<amount>  (<n> txns)
...

## Top counterparties (out)
- <counterparty> — $<amount>

## Status
- Cleared: $<x>  ·  Pending: $<y>

## Notable
- <largest / flagged items>

_As of <date>, <N> transactions in period. Source: finances/ledger.csv._
```
