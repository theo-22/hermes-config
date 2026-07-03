---
name: workspace-orchestration-coordination
description: Multi-actor check-in/check-out coordination for shared GPT file editing. Extends the existing SURFACE_RESERVATIONS.md + CONDUCTOR.md pattern (from workflow-orchestration) to GPT source files. Prevents lost-update overwrites when multiple AI actors (default Hermes, ga-hermes, CC, Codex) edit the same files.
category: gpt
write_mode: none
one_line_use: check in before editing shared GPT files, check out after
fast_pick: "yes"
---

# Workspace Orchestration — GPT File Coordination

Multi-actor check-in/check-out coordination for shared GPT file editing.

Extends the existing `SURFACE_RESERVATIONS.md` + `CONDUCTOR.md` pattern (from `workflow-orchestration` skill) to GPT source files. Prevents lost-update overwrites when multiple AI actors edit the same files.

**Canonical coordination directory:** `/Users/ted/Operations/gpt_coord/`

## The Problem

4-5 actors (default Hermes, ga-hermes, CC, Codex) edit ~100 shared markdown files. No check-in/check-out. Same-day overwrites and 3+ Builder repastes are now normal. Root cause: lost-update problem — Actor B overwrites Actor A's changes because B doesn't know A edited the file.

## Installed Infrastructure (do not rebuild)

| Surface | Location | What it does |
|---------|----------|-------------|
| SURFACE_RESERVATIONS.md | `Operations/session_chains/` | Reservation ledger for Operations chains |
| CONDUCTOR.md | `Operations/session_chains/` | Chain status board |
| SEQUENCE_GATES.md | `Operations/session_chains/` | Gate rules between chains |
| workflow-orchestration skill | `Skills/workflow-orchestration/` | Skill governing chain execution |

This skill applies the same patterns to GPT file surfaces instead of Operations chains.

## Coordination Directory

```
/Users/ted/Operations/gpt_coord/
  changes.jsonl       ← append-only change events (one per edit)
  queue.jsonl         ← builder deployment queue (extends Builder_Update_Batch concept)
  reservations.jsonl  ← active file leases with timeouts
```

All JSONL (append-only, no overwrites of the coordination surface itself). Machine-readable. Human-readable by `cat | python3 -c "..."`.

## The Write Protocol

### Before editing any GPT file:

1. **Read** the tail of `changes.jsonl` for this GPT → know recent history
2. **Check** `reservations.jsonl` → is this file already reserved?
3. **Reserve** → append a reservation entry with actor, file, intent, base hash, 30-min timeout
4. **Verify hash** → `sha256sum <file>` matches the base hash in your reservation. If not, someone edited while you planned — abort and re-plan.

### After editing:

5. **Write temp, rename atomic** → write to `<file>.tmp`, then `mv <file>.tmp <file>` (POSIX atomic rename)
6. **Log change** → append one event to `changes.jsonl`
7. **Queue Builder** → append one item to `queue.jsonl`
8. **Store in Brain** → `mcp_open_brain_store_thought(summary, source="gpt-change-log")`
9. **Release reservation** → update reservation to `status: released`

### When Ted pastes into Builder:

10. **Log deploy** → append event with `event_type: builder_pasted` to `changes.jsonl`
11. **Update queue** → update queue item to `status: pasted`

### After smoke test:

12. **Log test** → append event with `event_type: smoke_test` to `changes.jsonl`
13. **Update queue** → update queue item to `status: smoke_tested` or `status: failed`

## Reservation Entry Format

```json
{"reservation_id":"res_2026-06-24T14:02:11Z_ga-hermes_01",
 "file":"/Users/ted/Projects_GPT/Clinical/Clinical_Instructions.md",
 "project":"Clinical GPT",
 "actor":"ga-hermes",
 "intent":"Add brain-first reflex to session-start",
 "base_sha256":"b9d1c6d3...",
 "status":"active",
 "lease_started_at":"2026-06-24T14:02:11Z",
 "lease_expires_at":"2026-06-24T14:32:11Z"}
```

## Change Event Format

```json
{"change_id":"chg_2026-06-24T14:11:49Z_ga-hermes_01",
 "project":"Clinical GPT",
 "file":"/Users/ted/Projects_GPT/Clinical/Clinical_Instructions.md",
 "actor":"ga-hermes",
 "reservation_id":"res_2026-06-24T14:02:11Z_ga-hermes_01",
 "base_sha256":"b9d1c6d3...",
 "new_sha256":"4f8a0020...",
 "changed_at":"2026-06-24T14:11:49Z",
 "change_type":"edit",
 "summary":"Added brain-first reflex section",
 "reason":"Fleet-wide brain-first reflex rollout",
 "builder_status":"pending",
 "brain_status":"indexed"}
```

## Queue Entry Format

```json
{"queue_id":"q_2026_06_24_001",
 "change_id":"chg_2026_06-24T14:11:49Z_ga-hermes_01",
 "project":"Clinical GPT",
 "target":"Builder Instructions",
 "resource":"Clinical/Clinical_Instructions.md",
 "queued_at":"2026-06-24T14:12:00Z",
 "status":"pending_paste",
 "assigned_to":"Ted",
 "smoke_test":"pending",
 "notes":"Paste Instructions. Run session-start smoke after."}
```

## One-Sentence Policy

> Reserve first, verify hash second, write atomically, log the change, queue Builder deployment, then release.

## What Builder_Update_Batch.md Becomes

The 521-line `Builder_Update_Batch.md` becomes a **generated view** of `queue.jsonl`. A script (`generate_builder_batch.py`) reads JSONL and renders human-readable markdown. Ted reads the generated markdown; JSONL remains the machine-truth.

## Project-Level Reservations

For coordinated multi-file sweeps (e.g., brain-first reflex rollout touching 10 GPTs):

```json
{"reservation_id":"res_2026-06-24_batch_001",
 "project_wide":true,
 "projects":["all GPTs"],
 "files":["*/Instructions.md"],
 "actor":"ga-hermes",
 "intent":"Fleet-wide brain-first reflex rollout",
 "status":"active",
 "lease_expires_at":"2026-06-24T16:00:00Z"}
```

## Failure Modes

| Failure mode | Guardrail |
|---|---|
| Actor skips reservation | Skill enforcement — protocol mandatory in gpt-environment-build |
| Stale context (old file version) | Hash verification before write — abort if changed |
| Reservation rot (crashed actor) | 30-minute timeout, auto-expire |
| Coordination surface overwritten | JSONL is append-only, no rewrites |
| Same file, different path | Canonical absolute paths only |

## Anti-Patterns

- **Do not use shared markdown as authoritative coordination state** — this recreates the overwrite problem one layer higher
- **Do not skip hash verification** — this is the guard against stale context
- **Do not hold reservations beyond timeout** — release promptly after editing
- **Do not edit the JSONL files directly** — use the Python helper module

## Boundary With Nearby Skills

- `workflow-orchestration` — governs Operations session chains. This skill adapts those patterns for GPT file surfaces. Do not modify.
- `gpt-environment-build` — governs GPT build/repair. This skill adds the pre-edit check + post-edit log mandate.
- `gpt-instructions-discipline` — governs Instructions field content/limits. This skill adds the check-before-edit step.
- `proposal-candidate-surfacing` — use when the coordination design itself needs to be discussed before implementation.

## Deliverables (Implementation Order)

### Phase 1: Foundation
- [ ] Create `/Users/ted/Operations/gpt_coord/` directory with README
- [ ] Write `gpt_coordination.py` — Python module with `reserve()`, `release()`, `log_change()`, `queue_builder()`, `get_history()`, `check_conflict()`
- [ ] Write `generate_builder_batch.py` — reads JSONL, renders Builder_Update_Batch.md
- [ ] Write `changes.jsonl`, `queue.jsonl`, `reservations.jsonl` with headers
- [ ] Store policy in Brain

### Phase 2: Skill Integration
- [ ] Update `gpt-environment-build` skill with reserve-verify-write-log-queue-release as mandatory
- [ ] Update `gpt-instructions-discipline` with pre-edit check step
- [ ] All profiles (default Hermes, ga-hermes) load coordination before GPT edits
- [ ] CC and Codex get protocol in their GPT workflows
- [ ] Surface in GA_HERMES_START.md and default Hermes SESSION_START.md

### Phase 3: Brain + Search
- [ ] Every change event stored in Brain
- [ ] Before GPT work: `search_brain("<GPT> changes")` returns recent summaries

### Phase 4: Builder_Update_Batch Integration
- [ ] Replace手动 curation with generated view from queue.jsonl
- [ ] Ted's workflow stays the same

### Phase 5 (Optional): Watcher
- [ ] Python Watchdog over `Projects_GPT/` directories
- [ ] Appends "observed changed" events (not authoritative)
- [ ] Refreshes generated dashboards

## Never Assume

- Do not assume the current manual workflow is acceptable just because it has existed
- Do not assume Builder visibility means the action is actually usable
- Do not assume `saved: true` means the content changed
- Do not assume a contaminated chat is a trustworthy verifier
- Do not jump to cleanup philosophy before the active path works
