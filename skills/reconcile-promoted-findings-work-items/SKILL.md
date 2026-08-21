---
name: reconcile-promoted-findings-work-items
description: Reconcile a suspected bulk promotion from findings_index into Control work_items when old, duplicate, or unauthorized findings have inflated the live queue. Preserve unresolved findings, close only evidence-proven rows, retire stale projections, and prove the live queue after an atomic guarded apply. Do not use for ordinary inbox intake or routine single-item closure.
metadata:
  category: database-integrated
  write_mode: db
  one_line_use: withdraw an invalid findings-to-work bulk promotion without losing unresolved findings
  fast_pick: "yes"
---

# Reconcile Promoted Findings Work Items

Repair the promotion lifecycle, not merely the visible count. `work_items` is the
live work authority; `findings_index` is an evidence/backlog surface. A finding
whose status is `new` is undispositioned, not necessarily current, actionable, or
authorized work.

## When to use

Use this skill when a work queue suddenly expands from an audit/findings sweep,
many rows share one creation timestamp or provenance marker, a manual decision
queue disagrees with the live API, or old findings appear as new current tasks.

Do not use it for:

- ordinary `_AI_Inbox` classification or linked packet closure — use
  `reconcile-inbox-work-items`;
- shaping legitimate surviving work into sessions — use
  `shape-work-item-sessions`;
- stamping audit yield without changing work lifecycle — use `audit-yield-stamp`;
- bulk-closing rows merely because they are old.

## Authority and invariants

- Read current work from `GET http://127.0.0.1:5555/api/work-items?state=pending`
  and `/Users/ted/Control/backend/system.db#work_items`.
- Treat historical Markdown queues, dashboards, memory, and `findings_index.status`
  as leads until reconciled against live state.
- Preserve unresolved findings. Withdrawing an unauthorized work-item projection
  sends its source finding to `known_backlog`; it does not mark the finding resolved.
- Use `acted` or `superseded` only with item-specific current evidence.
- Never directly close an inbox-linked work item; the installed inbox lifecycle must
  archive the source packet and commit both sides atomically.
- Preserve rollback evidence, events, receipts, and stale-state guards. Do not delete
  the source findings or erase the historical work-item rows.

## Canonical workflow

### 1. Freeze the live baseline

Capture the pending API count and exact IDs. Inspect the database schema before
querying it. Record active claims and run the installed work-item integrity checker.

Identify the suspected cohort by exact provenance, not an approximate age filter:
creation timestamp, notes marker, source sweep, ID range, or promotion receipt. Prove
the cohort membership and separately count rows already terminal before changing
anything.

### 2. Trace the promotion source

Find the script, session note, receipt, or manual projection that created the rows.
Determine whether an active importer can repeat the promotion. Stop or repair an
active inflator before cleanup; if it was a one-time manual action, record that fact
and do not invent an importer.

Compare what the promotion assumed with what the source field actually means. The
known failure shape is treating `findings_index.status='new'` as proof of current
authorized work.

### 3. Decide at the cohort level before item review

First decide whether the promotion itself was authorized and valid. When it was not,
the default correction for unresolved rows is `withdrawn`: terminalize the projected
work item as `superseded` while preserving the finding as `known_backlog`.

Use expensive or item-by-item review only for likely terminal exceptions. A cheap
worker may find evidence, but its classification is a lead until exact files, DB
rows, receipts, or installed behavior support it. Do not spend a model pass
re-auditing every old finding when the cohort-level defect already establishes that
the work-item projection should be withdrawn.

Manifest actions supported by the installed guarded applier:

- `withdrawn` — invalid promotion; work item `superseded`, finding `known_backlog`;
- `acted` — completion directly proven; work item `acted`, finding `resolved`;
- `superseded` — obsolete or overtaken with direct proof; both become terminal;
- `duplicate` — terminal duplicate with a valid survivor link;
- `retain` — authorized current work remains pending; finding becomes
  `known_backlog` so it is not promoted again as `new`.

Every manifest row requires `item_id`, `finding_id`, `action`, `reason`, and a
non-empty `evidence_refs` list. `duplicate` additionally requires `duplicate_of`.

### 4. Dry-run the guarded apply

Use the installed adapter:

```bash
python3 /Users/ted/Control/backend/scripts/reconcile_promoted_findings_work_items.py \
  /path/to/manifest.jsonl
```

The dry run must prove every work item is still pending, the notes contain the exact
`finding_id`, each finding exists, no row is duplicated in the manifest, and no item
has an inbox link. Resolve every refusal rather than weakening the guard.

### 5. Apply atomically

Acquire a DB-backed task claim for the exact reconciliation cohort and a surface
claim for the receipt. Apply only after reviewing the dry-run action counts:

```bash
python3 /Users/ted/Control/backend/scripts/reconcile_promoted_findings_work_items.py \
  /path/to/manifest.jsonl \
  --apply \
  --actor <actor> \
  --claim-id <active-claim-id> \
  --receipt /absolute/path/to/receipt.json
```

The helper creates a timestamped SQLite rollback backup, applies work-item and
finding changes in one transaction, writes evidence-bearing events for both
lifecycles, rejects stale rows at apply time, and runs `PRAGMA quick_check`.

### 6. Reconcile survivors and stale projections

Re-read the live pending API. Review only the smaller survivor set for exact
duplicates, completed returns, summary-only alerts, overtaken work, or fake owners.
Use canonical state/lifecycle operations; do not bypass inbox-linked packets.

Retire or visibly tombstone any manual queue projection that could re-present the
withdrawn rows as current. Keep its contents as historical evidence and point it to
the live API. Do not replace one competing queue with another.

### 7. Prove completion

Require all of the following:

- live API pending count and exact survivor IDs;
- zero pending rows in the identified promotion cohort;
- expected work-item and finding action counts;
- matching work-item and finding events;
- rollback backup and durable receipt paths;
- `PRAGMA quick_check=ok` and the installed work-item integrity checker passing;
- no active claims left for the lane;
- stale manual projections retired or corrected;
- unresolved findings still queryable as `known_backlog`.

Record any missing archived inbox evidence, failed worker route, timeout, or
nonexistent owner as an exception. Never manufacture proof or close the row merely
to make the survivor count smaller.

## Cost and delegation discipline

Hermes is useful for bounded evidence checks after the cohort decision is stable.
Keep batches small enough for the installed timeout, require exact JSON output, and
save receipts. If a worker times out or a named profile does not exist, retain the
uncertain row or consolidate only when independent live evidence supports it.

The premium runtime owns cohort framing, guarded apply review, and final acceptance.
It should not burn tokens asking a worker to rediscover the same invalid-promotion
premise hundreds of times.

## Failure modes

- **Status-as-authority:** `finding.status='new'` is treated as current work.
- **Count-only cleanup:** rows disappear but unresolved findings are falsely resolved
  or deleted.
- **Per-item token sink:** an invalid cohort is exhaustively re-audited before the
  promotion defect is corrected.
- **Inbox bypass:** a linked row is terminalized without packet archival/receipt.
- **Projection resurrection:** a historical Markdown queue remains visibly current
  and later re-seeds the same rows.
- **False completion:** worker output, a stale receipt, or adjacent machinery is
  accepted without current evidence.
- **Unowned survivor:** cleanup leaves items assigned to a runtime/profile that does
  not exist.

## Worked evidence

The 2026-08-21 reconciliation reduced 298 pending rows to 27 while preserving 226
unresolved findings as `known_backlog`. The full receipt is:

`/Volumes/Extra/Substrate/Operations/reports/Work_Item_Closeouts/2026-08-21_WORK_ITEMS_BACKLOG_RECONCILIATION.md`

## Update backstop

Before use, confirm the live API, database fields, terminal-state vocabulary, inbox
lifecycle, and guarded helper still match this skill. If they differ, preserve the
authority, evidence, rollback, and unresolved-finding invariants while proposing one
shared-skill update; do not create a local doctrine fork.
