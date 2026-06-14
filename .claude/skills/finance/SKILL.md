---
name: finance
description: "Ingest a cash-flow transaction into the project-kb ledger (finances/ledger.csv). Three input modes: verbal ('$40 to Example SaaS today'), a receipt/screenshot image, or a bank statement (local file path). Parses fields, categorizes via the merchant map, deduplicates + reconciles against the existing ledger, CONFIRMS everything with the user before writing, then appends/enriches rows, stores receipts, writes redacted statement snapshots, commits with finance: prefix, pushes. Use when user says: log this expense, record this payment, add this transaction, here's a receipt, here's my bank statement, we got paid X, we spent X on Y, track this cost."
---

# /finance

Ingests transactions into `finances/ledger.csv`. **One in-session skill — no deferral.** Finances want completeness now, and every write is confirmed with the user.

**Read first (T2):** `finances/README.md` — the schema, controlled category vocab, merchant→category map, dedup rules, and redaction rules. This skill enforces that contract; it does not restate it.

## Procedure

1. **Acquire `runs/.lock`.** If present, abort ("another agent is writing, retry later").
2. **Read `finances/README.md`** for the column schema, category vocab, merchant map, and dedup/redaction rules.
3. **Detect input mode:**
   - **Verbal** — free text from the user.
   - **Receipt** — an image path / attachment.
   - **Statement** — a **local file path** the user points you at (PDF/CSV/image). NEVER ingest a raw statement from `inbox/` or any committed location; if the user dropped one there, move/copy it out first and ensure the raw is not committed.
4. **Parse → normalized records** (columns per the README schema):
   - **Verbal:** extract `date` (default today), `amount`, `direction` (infer; ask if ambiguous), `counterparty`, `account` (ask if unknown), `note`. No `ext_id`. `status: pending`. Set `owner` from the account→owner map; if the account isn't mapped, ask whose it is and append the mapping.
   - **Receipt:** vision-read merchant, date, total, currency, the card last-4, and any invoice/order number (`ext_id`). Copy the original image to `finances/receipts/<id>-<slug>.<ext>`; set `source: receipt:<filename>`. **Set `status: pending`** — a receipt is our capture, not statement-confirmed; rule 4 flips it to `cleared` when the bank line lands. Set `owner` from the account→owner map (card last-4 → owner); if unmapped, ask and append the mapping. (If the image exposes a full card number, do NOT store it — keep the row only, note redaction.)
   - **Statement:** parse all rows. For a large statement, dispatch a **subagent** to parse → return structured rows (keeps main context clean). **Redact in memory:** strip full account/routing/card numbers (keep last-4), drop addresses/other PII. Write the redacted snapshot to `finances/statements/<YYYY-MM>-<account-nick>.csv`. Capture each row's bank reference as `ext_id`; set `source: statement:<snapshot-filename>`. `owner` = the statement account's owner (per the map — a snapshot is single-account).
5. **Categorize** each record via the merchant→category map in the README. If the counterparty is unknown, propose a category and ask; record the new mapping in the README's merchant-map table.
6. **Dedup + reconcile** each record against `finances/ledger.csv` per the README rules:
   - `(account, ext_id)` already in ledger → skip (report "already recorded, ref X"). Scope by account — bank refs are only unique within an account.
   - `ext_id` differs but fields look identical → separate transaction → keep.
   - no `ext_id` + fingerprint `(date, amount, counterparty, account)` matches → **suspected duplicate**: show the existing row and **ask** same-or-separate. If separate, prompt for a distinguishing `note`.
   - statement row matches an existing `pending` entry by `(amount, counterparty, date ±2d)` → **enrich** that row (attach `ext_id`, `status: cleared`) instead of appending.
   - For statements, also flag **in-ledger-but-not-in-statement** rows for the period back to the user.
7. **CONFIRM EVERYTHING.** Present the proposed change as a table — new rows, enrichments, skipped duplicates, and any flags. Get explicit user OK before writing. (Current policy: confirm even single clean entries.)
8. **Assign `id`** = `<date>-<NN>`, NN = next sequential index for that date already in the ledger.
9. **Write:** append new rows / edit enriched rows in `finances/ledger.csv`. Store receipt images and the redacted statement snapshot. Update the README merchant-map table if new mappings were learned.
10. **Regenerate + lint:** `python3 scripts/rebuild-indexes.py finances/` then `python3 scripts/kb-lint.py finances/README.md`.
11. **Commit + push.** Prefix `finance:` — e.g. `finance: log 2026-05-30 Example SaaS $40 (saas)` or `finance: reconcile statement 2026-05 (+3 new, 5 confirmed)`. Push immediately.
12. **Release the lock.**

## Notes

- **Never store full account/routing/card numbers** anywhere (ledger, statements, notes) — last-4 or nickname only.
- **Never commit a raw bank statement.** Redact in memory; write only the snapshot CSV.
- `amount` is always positive; `direction` carries the sign. `transfer` rows are net-zero and excluded from spend/income totals.
- One logical commit per ingest event (one verbal entry, one receipt, or one statement reconciliation).
