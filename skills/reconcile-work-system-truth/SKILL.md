---
name: reconcile-work-system-truth
description: Repair cross-surface work-state drift when inbox rows, canonical work items, orchestration runs, staged packets, generated indexes, Planning documents, or project projections disagree. Use for a bounded system-wide reconciliation, not for processing one ordinary inbox packet.
metadata:
  category: database-integrated
  write_mode: shared
  one_line_use: reconcile work lifecycle, recoverable archives, projections, and stable identity from canonical truth
  fast_pick: "yes"
---

# Reconcile Work-System Truth

Restore one coherent lifecycle across the Control database and its file projections without turning reports, filenames, or sidebar placement into authority.

## When to use

Use this skill when drift spans several of these surfaces at once:

- inbox messages or packet files;
- canonical `work_items`;
- `orchestration_runs` and staged handoff packets;
- Active Index, Project Room, or scheduled-follow-up projections;
- Planning documents whose lifecycle is implicit;
- project identity inferred from a Room, Home, or sidebar entry.

For one ordinary `_AI_Inbox` packet, use `reconcile-inbox-work-items`. For one stale decision row, use `reconcile-stale-decision-work-item`.

## Authority model

1. Current Control database rows and installed APIs own lifecycle state.
2. Source packets and receipts provide provenance and evidence.
3. Filesystem presence proves whether a packet is live or recoverably archived.
4. Generated indexes, dashboards, Room/Home views, and scheduled summaries are projections only.
5. Filenames and index sections never imply work state.

Refresh the live rows immediately before mutation and again before closeout. Preserve unrelated dirty or staged work.

## Canonical workflow

### 1. Bound and back up the cohort

- Identify exact row IDs, destinations, orchestration IDs, packet paths, and projection consumers.
- Inspect schemas and the code that reads each surface before changing it.
- Take a timestamped `system.db` backup; record its SHA-256, `PRAGMA quick_check`, and pre-existing foreign-key exceptions.
- Acquire file checkouts for every file that may change.

### 2. Repair admission and classification

- Do not promote monitoring summaries, aggregate counts, or synthetic wrappers into Ted-owned work.
- A Ted decision must contain a concrete question, recommendation, evidence, and recheck condition.
- Classify path findings structurally. Audit receipts, continuity, provenance, command arguments, examples, and explicit retirement statements are not current broken dependencies.
- Retain a negative control proving that an ordinary missing active dependency remains actionable.

### 3. Reconcile canonical lifecycle and orchestration identity

- Settle each source row from current evidence: implemented, responded, dismissed, intentionally open, or another supported state.
- Preserve supersession lineage; do not rewrite terminal history.
- Create or reuse one canonical orchestration for each `work_item_id`. Replays with the same effective target return the existing orchestration. Conflicting targets fail closed.
- Reconcile stale orchestration state only after the canonical work item and successor relationship are proven.

### 4. Archive recoverably

- Move disposed inbox and terminal staged packets into dated `Archived/<date>/` locations; do not delete them.
- Update every database filepath or `packet_ref` in the same bounded operation.
- Append lifecycle/archive events where the schema supports them.
- Treat `accepted`, `cancelled`, and `failed` orchestration packets as terminal for automatic filing. Do not silently treat `parked` or `blocked` as disposable.
- On failure, roll back the database transaction and restore moved files.

### 5. Rebuild projections and explicit registries

- Regenerate Active Index, Project Room attention, scheduled-run, and follow-up surfaces from current canonical rows.
- Write or refresh `projection_receipts` with source and output hashes.
- Give each project a stable canonical ID, then map Room/Home/sidebar locations as replaceable projections.
- Register Planning documents with explicit lifecycle and linkage. Leave uncertain records honestly `unreviewed` and `unlinked`; never infer status from filenames.

Current deterministic implementations:

- `/Volumes/Extra/Substrate/Operations/scripts/inbox_triage.py`
- `/Volumes/Extra/Substrate/Operations/scripts/inbox_archive.py`
- `/Volumes/Extra/Substrate/Operations/scripts/archive_terminal_orchestration_packets.py`
- `/Volumes/Extra/Substrate/Operations/scripts/regenerate_work_system_projections.py`
- `/Users/ted/Control/backend/orchestrator_control_plane.py`
- `/Users/ted/Control/backend/work_registry.py`

## Evidence and done standard

Require all applicable checks:

- focused tests for each changed seam, including idempotent replay and classifier negative controls;
- `PRAGMA quick_check = ok`, with foreign-key findings compared to the pre-change backup rather than assumed new;
- every archived database path exists and no eligible terminal packet remains directly in a live `staged` root;
- the intentionally open inbox remainder is named explicitly;
- regenerated projections have current receipts and match live source counts;
- project and Planning registry counts are read back from the database;
- installed service restart and live health or connector proof after runtime code changes;
- canonical work items, orchestration rows, and successor links reread immediately before reporting closure;
- all task and file claims released, and remote-backed repositories committed and pushed.

Report genuine remaining work separately from reconciliation defects. A detector that now exposes a real current inconsistency is working, even when its actionable count is nonzero.

## Failure modes

- Treating a dashboard or filename as authority.
- Deleting packets after changing only their database status.
- Calling a duplicate handoff idempotent while creating another orchestration row.
- Hiding unknown Planning state by guessing lifecycle from its directory or title.
- Counting historical/evidence path references as active defects, or suppressing all missing paths and losing the negative control.
- Reporting `0` because the target cohort is clean while unrelated live exceptions still exist.
- Using local unit tests as a substitute for installed-path proof.

## Runtime notes

Actors without direct database or filesystem access should route a bounded proposal or handoff naming the exact cohort and required readbacks. They must not maintain a parallel work ledger in chat, inbox metadata, or a generated document.

## Update backstop

The paths and schemas above are current implementation pointers, not permanent authority. If they drift, inspect the installed consumer and update this shared skill rather than creating an actor-local doctrine fork.
