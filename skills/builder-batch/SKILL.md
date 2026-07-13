---
name: builder-batch
description: Run the accumulated GPT Builder update queue — read /api/gpt-status for pending items, execute the batch from Builder_Update_Batch.md, require proof receipts before marking complete. Composes gpt-instructions-discipline and gpt-environment-build for fleet-level batch execution. Use when Builder changes have accumulated and Ted is ready for a Builder pass. Do not use for single-GPT ad hoc updates — use gpt-instructions-discipline and gpt-environment-build directly for those.
category: gpt
write_mode: file
one_line_use: run the Builder update queue across the fleet
fast_pick: "no"
---

# Builder Batch

Run the accumulated GPT Builder update queue as a single coordinated pass. The goal is to clear the queue with verified proof receipts — not to execute as many updates as possible without evidence that they landed.

## Before You Start

Read both context surfaces. For Codex or Claude Code, prefer the bundled helper because it performs the repeatable queue/status read the same way every time:

```bash
/Users/ted/Skills/builder-batch/scripts/builder_batch_status.py
```

If the helper is unavailable, read the surfaces directly:

```bash
# Live work queue
curl -s "http://localhost:5555/api/gpt-status" 2>/dev/null | python3 -m json.tool | head -40

# Accumulated batch queue
cat /Users/ted/Operations/Builder_Update_Batch.md
```

Read the prerequisite skills — they carry per-GPT execution discipline and must be consulted before making per-GPT decisions:
- `/gpt-instructions-discipline` — before touching any GPT's Instructions or schema
- `/gpt-environment-build` — before a full environment build (schema + knowledge + instructions)

## Core Workflow

**1. Classify each queued item: pending or already done.**

`/api/gpt-status` shows `builder_needs_proof` vs `builder_verified` rows. Items in `Builder_Update_Batch.md` that have a dated receipt (`Operations/reports/GPT_Builder_Receipts/<date>/<gpt>.json`) are done. Items with `Status: local sources synced; Builder proof pending` are genuinely pending.

**The "skip already implemented" check is mandatory.** Re-pasting unchanged content wastes Ted's time and risks accidental regression. If the local source hasn't changed since the last receipt, the item is done.

Use `scripts/builder_batch_status.py --pending` during this step when a concise pending/done split is enough. It is a classifier only; the proof decision still follows the evidence rules in this skill.

**2. Run guardrails before any paste.**

```bash
/Users/ted/Operations/scripts/check_gpt_builder_guardrails.py
```

Fix flagged issues before continuing. Instruction budget warnings for Image Factory, CoCM, and Workspace Icon System are persistent known issues — do not add Instructions prose during a batch pass. If the guardrails script is unavailable, read `_shared/GPT_Build_Standards.md` and apply its checks manually.

**3. For each genuinely pending GPT, execute the four-step checklist:**

1. **Instructions paste** — source: `Projects_GPT/<GPT>/<GPT>_Instructions.md` (not Manifests; not memory)
2. **Schema paste/import** — source: `Control/mcp/openapi-<gpt>-actions.json` (generated JSON, not the YAML source)
3. **Sync_All** — call the GPT's `syncAll` or `sync_all` operation if it has one, after schema import
4. **Knowledge upload** — from `Manifests/<GPT>/`: remove all existing files, upload the full set. Never target individual files.

For System_Context/layer changes, the Knowledge upload step is mandatory for every Builder target. A local layer edit plus manifest sync is not live GPT proof; the GPT sees the new layer only after Builder Knowledge is re-uploaded and verified by internal retrieval.

**4. Smoke-test each GPT before moving to the next.** Both tests are required per `memory/feedback_builder_smoke_test_session_start.md`:
- **New/changed operation:** call it directly and confirm correct output
- **Session-start operation:** call `loadAuditRoleContext`, `loadCoordinatorRoleContext`, or the equivalent — auth issues only appear on role-restricted routes

**5. Write proof receipt.** Save to `Operations/reports/GPT_Builder_Receipts/<date>/<gpt>.json`. Minimum fields: `gpt_name`, `date`, `operations_tested`, `smoke_result`, `session_start_result`, and `knowledge_upload_result`. For System_Context/layer changes also include `knowledge_files_uploaded` and a short internal-retrieval quote check for the changed layer files. Until this file exists and `/api/gpt-status` recognizes it, the row is not cleared.

**6. Update `Operations/Builder_Update_Batch.md`.** Mark each completed item with `Status: Builder proof received — <date>` and link the receipt. Do not delete items from the batch file; leave them as the record. Ted clears stale sections when appropriate.

**7. Verify queue cleared.**

```bash
curl -s "http://localhost:5555/api/gpt-status" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); s=d.get('summary') or d; print(f'Queue: {s.get(\"work_queue\",\"?\")} / Builder-required: {s.get(\"work_queue_requires_builder\",\"?\")} / Needs proof: {s.get(\"builder_needs_proof\",\"?\")} / Verified: {s.get(\"builder_verified\",\"?\")}')" 2>/dev/null
```

Builder batch target: `builder_needs_proof=0`, `work_queue_requires_builder=0`, and no pending items in `Builder_Update_Batch.md`. `work_queue` may remain above zero when the residual `/api/gpt-status` rows are non-Builder follow-up, such as action probes or GPT self-checks. If residual non-Builder items remain, name them explicitly with their follow-up lane rather than treating the Builder batch as still pending.

## Exit Checklist

- Each executed GPT has a dated receipt file in `Operations/reports/GPT_Builder_Receipts/<date>/`
- `/api/gpt-status` shows `builder_needs_proof=0` and `work_queue_requires_builder=0`; any residual non-Builder `work_queue` items are named with their follow-up lane
- `Builder_Update_Batch.md` has no pending Builder-proof items
- `Builder_Update_Batch.md` updated; no item marked done without a Builder save receipt
- Both smoke tests completed per GPT (new operation + session-start operation)
- Knowledge upload completed for every executed GPT; System_Context/layer batches include internal-retrieval proof that the updated Knowledge is reachable
- Instruction budget warnings noted; no Instructions prose added without Ted authorization

## Boundaries

- **This skill orchestrates the queue.** `gpt-instructions-discipline` governs Instructions decisions; `gpt-environment-build` governs full environment builds. When in doubt on a per-GPT call, invoke the relevant skill rather than deciding ad hoc.
- **Do not mark a batch item done from local file changes alone.** Builder state requires a Builder save receipt, live GPT self-check, or direct runtime proof.
- **Chrome MCP is the path for Builder automation when available.** When not available, generate the paste packet and hand off to Ted. Do not attempt AppleScript DOM access — it fails in this environment (proof: `Operations/reports/Clinical_CoCM_Builder_Automation_Attempt_2026-05-22.md`).
- **Do not bundle Instructions edits with a batch pass** unless Ted has authorized the specific edit. A batch pass executes queued changes, not new ones.

## Update-Surfacing Backstop

If `Builder_Update_Batch.md` is renamed, `/api/gpt-status` schema changes, or the receipt path convention changes, update `scripts/builder_batch_status.py` and this skill together. Check `Operations/CHANGES_LOG.md` and `Operations/reports/GPT_Builder_Receipts/` structure before assuming paths are current.
