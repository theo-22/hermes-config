# Verify transaction and checkout closeout

Use when a save, commit, or closeout helper writes durable receipts while
releasing claims, checkouts, locks, or other task resources. This is a
conditional extension of the parent skill, not a new closeout protocol.

## Hidden contracts to inspect

- **Counting scope:** An API may release explicit IDs but count remaining
  resources across the whole actor/session. Inspect both operations. A temporary
  bookkeeping checkout can make a successful task release appear incomplete.
- **Ownership:** Preserve the exact task actor/session. Separate bookkeeping
  ownership only where the existing API supports it; do not weaken ownership
  checks, subtract an assumed count, or ignore actual remaining task resources.
- **Source format:** A database path is not a text document. Use the database's
  read-only interface and explicit row identifiers; raw byte searches or lossy
  decoding cannot prove current row state and may miss WAL updates. Unknown
  formats and ambiguous identifiers should fail visibly. Terminal audit rows
  need not be physically deleted to leave an active queue.
- **Durability order:** Identify what survives each failure. For a two-phase
  closeout, durable intent precedes task release; confirmation follows verified
  release. A pending row alone is recovery evidence, not confirmed completion.

## Bounded probe set

Use disposable files and fixture ledgers through the installed command and real
API, with only authorized fixture mutations. Reproduce the original failure on
the previous artifact where available, then rerun against the repaired artifact.

| Probe | Required observation |
|---|---|
| Named task IDs with a session | Task IDs close, bookkeeping releases, confirmed receipt records the correct remaining count |
| Named IDs without a session, if supported | Same success without accidentally counting the helper or closing other work |
| One real task checkout deliberately omitted | Confirmation fails and the omitted checkout remains active |
| Initial receipt write fails | Task resources remain held; no false confirmation |
| Confirming write fails after release | Durable pending evidence survives for explicit recovery |
| Bookkeeping release fails | Command does not report complete success |
| Binary DB and text sources | Native row-state checks and text membership checks both retain their rejection cases |

Fault injection may use a controlled API model when a real failure would disrupt
production. Label those results separately from installed-command/live-API proof.
Mocks must reproduce actual actor/session count semantics, not return a fixed
`remaining_active=0` for every successful release.

Read back resource state and receipt phases after each live probe. Clean up only
fixture-owned resources, including deliberately omitted checkouts. Do not retry
an already-released task set blindly; inspect the audit trail and pending receipt
before using the supported recovery path. Preserve other actors' work.

## Verified example and limits

The 2026-08-30 QuickSave repair reproduced a SQLite UTF-8 decode failure and a
false leftover count caused by the helper's own ledger checkout. The repair used
read-only `work_items` queries and a separate helper owner while preserving task
attribution, guarded writes, and failure ordering. Fourteen tests and three live
CLI/API probes passed; the real task then closed seven checkouts with a confirmed
receipt and no recovery append.

Evidence: `/Volumes/Extra/Substrate/Operations/reports/QUICKSAVE_HELPER_REPAIR_2026-08-30.md`.
Regression owner: `/Volumes/Extra/Substrate/Operations/scripts/test_quicksave_closeout_receipt.py`.
Reinspect current code before reusing exact fields or actor names. This example
proves one helper's behavior, not distributed atomicity, independent acceptance,
or every fleet caller. Do not copy temporary claim IDs into a new probe.
