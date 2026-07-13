---
name: workflow-orchestration
description: Start, complete, stage, or revise one bounded Operations session-chain lane from the conductor board. Use when Ted says "Let's get some work done", asks to work through session chains, start from the conductor, pick a work lane, turn current work into a chain, create/stage/revise a chain, or advance Operations chain work. Reads startup, presents the chain menu when no lane is named, reads CONDUCTOR.md, selects/confirms exactly one routed chain, stages exactly one new chain, or revises exactly one prior chain plan when context requires it, executes only the selected lane when running existing work, writes the completion report, validates it, appends and checks a QuickSave receipt, and stops. Do not use for broad priority review, unrelated project work, runtime/security/clinical/finance/Builder/schema/automation changes, or full session-end unless the selected chain explicitly authorizes that work.
category: meta
write_mode: file
one_line_use: run, stage, or revise one conductor-routed work lane
fast_pick: "yes"
---

# Workflow Orchestration

Advance, stage, or revise one bounded Operations session-chain lane from the conductor board.

This skill uses the standard bridge term **workflow orchestration** for Ted's local conductor/session-chain workflow: coordinate a state transition across one actor, one source chain, one proof report, and one closeout receipt.

## Use When

- Ted says "Let's get some work done."
- Ted asks to start from the conductor, session chains, or Operations work lanes.
- Ted wants one bounded chain selected and carried through completion.
- Ted says current project work is ready to become a chain, asks to create/stage/revise a chain, or asks to turn a discussion/artifact into a runnable Operations lane.

## Do Not Use When

- Ted names a specific different skill, project room, file, or non-chain task.
- Ted asks for broad priority review, brainstorming, or a status inventory rather than execution.
- The work would require runtime, security, clinical implementation, finance, Builder/schema, automation, startup/session-end, or DB mutation unless the selected chain explicitly authorizes that surface.
- Ted asks for full session-end instead of QuickSave.

## Workflow

### Entry Mode

Use one of two modes.

**Run existing lane** — Ted wants to choose or run an already staged chain.

**Stage new or revised lane** — Ted wants current project work, a discussion, a decision point, or a local artifact turned into a bounded session-chain lane, wants a prior chain plan revised because context changed, or wants a small ordered install sequence for a Project Room. Staging/revision creates or updates the chain surface and conductor row; it does not execute the chain unless Ted separately routes execution.

If Ted has not named a lane, read `/Users/ted/Operations/session_chains/00_START_HERE.md` and present a compact menu of chain names grouped by topic:
- include Ted-routable QuickSave chains;
- include ready-only-with-specific-context chains separately;
- include completed-since-refresh only as reference, not selectable work;
- mark archived room-routed prompts as archived/reference only.

Stop and ask Ted to choose one lane unless exactly one lane is clearly routed by Ted's wording.

### Run Existing Lane

1. Read your runtime's session-start surface and run its startup checks (see Runtime Notes).
2. Read `/Users/ted/Operations/session_chains/CONDUCTOR.md`, `/Users/ted/Operations/session_chains/SURFACE_RESERVATIONS.md`, and `/Users/ted/Operations/session_chains/SEQUENCE_GATES.md`.
3. Select exactly one `active`, `staged`, `ready`, or explicitly routed chain. If more than one is plausible and Ted did not name one, choose the safest currently routed lane and state why.
4. Read only that chain file and directly named proof/source files.
5. Before edits, state:
   - selected chain;
   - active domain/work type, if the lane touches a domain or work-type boundary;
   - checked-out domains/work types that must not be pulled into this lane;
   - source surfaces;
   - allowed write surfaces;
   - reserved shared write surfaces, if any;
   - exclusions;
   - stop condition.
6. If the chain may write shared state, add a narrow reservation in `/Users/ted/Operations/session_chains/SURFACE_RESERVATIONS.md` before the first edit. Shared state includes conductor/status/start files, `CHANGES_LOG.md`, QuickSave receipts, `PROJECT_ROOMS_STATUS.md`, room-local `CURRENT_STATE.md` / `NEXT_ACTION.md`, DB work-item boards, and other active status or closeout ledgers.
7. Execute only the selected lane. Park adjacent work instead of widening. If the lane discovers it needs a surface reserved by another chain, or an undeclared shared surface, record the finding and leave the write for the owning chain or a coordinator reconciliation pass. If the lane discovers that a future lane must wait for proof, record or update a sequence gate in `SEQUENCE_GATES.md` while the context is fresh; do not turn the gated future lane into runnable work.
8. Write the required completion report under `/Users/ted/Operations/reports/TODO_Session_Completions/`.
9. Run `/Users/ted/Operations/scripts/todo_session_completion_check.py <completion-report-path>` when the chain is TODO/session-chain derived.
10. If this lane opened a surface reservation, close it as `released`, `parked`, or `coordinator_handoff` before claiming QuickSave is done.
11. Append and validate a QuickSave receipt with `/Users/ted/Operations/scripts/quicksave_closeout_receipt.py append ...` and `check`.
12. Stop after reporting:
   - `QuickSave: done|not done`;
   - saved surfaces;
   - verification;
   - source-item disposition;
   - surface reservation disposition, if any;
   - repo state;
   - next-session prompt status.

### Stage New Or Revised Lane

Use this mode only when Ted explicitly wants the current work turned into a chain, wants a prior chain plan revised, or wants a few planned installs lined up for a room. Do not use it just because a project has possible next steps.

1. Read your runtime's session-start surface and run its startup checks (see Runtime Notes).
2. Read `/Users/ted/Operations/session_chains/CONDUCTOR.md`, `/Users/ted/Operations/session_chains/00_START_HERE.md`, `/Users/ted/Operations/session_chains/SURFACE_RESERVATIONS.md`, `/Users/ted/Operations/session_chains/SEQUENCE_GATES.md`, and any owner surface Ted named for the current work.
3. Before creating new chain rules, categories, templates, or reusable process language, check existing homes first: `/Users/ted/_shared/WHEN_TO_READ.md`, directly routed `_shared` docs, relevant existing skills, and the owner room's `CURRENT_STATE.md` / `NEXT_ACTION.md` / `README.md`. Reuse or link existing doctrine when it covers the shape; add only the chain-specific procedure needed for this lane.
4. Define exactly one new or revised chain with:
   - chain name;
   - chain type: bounded execution, guided decision, or adaptive stewardship/scout;
   - owner surface;
   - input/source surfaces;
   - allowed write surfaces;
   - exclusions/protected surfaces;
   - stop condition;
   - closeout requirement;
   - source-item disposition rule;
   - trigger/start condition.
5. For a Project Room install sequence, define a small ordered set of linked chains only when each chain has its own stop condition and can still run one at a time. Record dependencies explicitly: "Chain 3 may revise Chain 1 settings/scope if X changes." Later-chain discoveries may revise earlier chain files/Conductor rows before execution; do not treat the earlier plan as locked when the room context has changed.
6. If a later planned chain changes assumptions, settings, scope, or allowed writes for an earlier chain, revise the earlier chain first and mark the reason. Do not run the stale earlier chain and do not silently widen it during execution.
7. Before declaring the staging/revision done, run a consistency pass against:
   - every chain in the same named sequence;
   - every conductor row with the same owner surface;
   - every conductor row with overlapping allowed write surfaces;
   - every chain file directly referenced by those rows.
   Compare dependency order, owner surface, allowed writes, exclusions, stop condition, trigger/start condition, and closeout requirement. Repair the conflict if it is inside the staged/revised chain scope; otherwise record the conflict and mark the affected chain `needs_restage` or waiting for Ted/owner-surface review.
8. If the staged or revised sequence has a future lane blocked by proof, add or update exactly one sequence gate in `/Users/ted/Operations/session_chains/SEQUENCE_GATES.md`. The gate must name the blocked lane, proof required, allowed prover, unlock action, failure path, protected surfaces, and viability review trigger. Do not use `ready` as a gate state; gates advance by proof or viability review.
9. If the chain would touch protected runtime, security, clinical implementation, finance, Builder/schema, automation, startup/session-end, or DB mutation surfaces, stage it as planning/review only unless Ted explicitly authorized those writes.
10. Write one chain file under `/Users/ted/Operations/session_chains/` using the existing chain-file style, or revise the existing chain file if the work is already staged. Keep it runnable by a future worker without requiring broad context.
11. Add or revise exactly one row in `/Users/ted/Operations/session_chains/CONDUCTOR.md` with state `staged`, `waiting`, `condition-triggered`, or `parked` as appropriate. Do not mark it ready if it still needs Ted input or an external trigger.
12. Update `/Users/ted/Operations/session_chains/00_START_HERE.md` only if the new chain should appear in the launch menu. If it is protected, blocked, or future-triggered, place it under the right non-ready section.
13. If shared state is edited, use `/Users/ted/Operations/session_chains/SURFACE_RESERVATIONS.md` the same way as an execution lane.
14. Write a compact staging note or completion report when needed to make the intake durable.
15. Append and validate a QuickSave receipt if this staging closes or rewrites a real source item; otherwise report `Source item: none` only when no source item existed.
16. Stop after reporting:
   - `Chain staged/revised: yes|no`;
   - chain file or linked chain files;
   - existing doctrine/surface reuse checked;
   - dependency/revision notes, if any;
   - sequence gate created/revised, if any;
   - conflict scan result;
   - conductor/start-menu placement;
   - saved surfaces;
   - verification;
   - source-item disposition;
   - whether execution is now routable or still waiting.

## Runtime Notes

The canonical procedure above is runtime-agnostic (generalized 2026-07-12 — it previously hardcoded Codex's startup). Only the session-start read differs by actor:

- **Claude Code / Sonnet:** read `/Users/ted/Operations/SESSION_START.md`.
- **Codex:** read `/Users/ted/Operations/CODEX_SESSION_START.md`.
- **Other runtimes:** read that actor's own session-start; if none exists, run the universal `Canon/SESSION_SIDECAR.md` steps.

Reservation mechanics: shared-surface reservations are now DB-backed via `claims.py` surface-grain claims (System 14 Ch15). `SURFACE_RESERVATIONS.md` is an auto-generated *view* of live claims — do not hand-edit it to reserve; take a surface-grain claim (e.g. `/api/claims/claim` with `grain=surface`, `target=<abs path>`) and release it at closeout. The steps below that say "reserve in `SURFACE_RESERVATIONS.md`" mean this.

## Guardrails

- One lane per window.
- Reservations and sequence gates are separate processes. Reservations protect active shared writes; sequence gates protect future-lane proof dependencies.
- When a worker creates a sequence gate, it is preserving context, not authorizing the gated lane. A later proof pass must advance, fail, revise, or retire the gate.
- Lanes separate work types and domains. At lane start, check in to exactly one active domain/work type when applicable; check out unrelated domains/work types. If a finding requires another domain, stage a handoff or revised lane instead of crossing streams inside the current lane.
- Treat Ted's ideas as intent and source material, not an implementation plan to copy blindly. Preserve the goal, then choose the chain shape, boundaries, write surfaces, and verification standard that will actually work.
- Question Ted's proposed plan when the chain shape, sequence, scope, write surface, dependency, or verification standard looks weak, unsafe, stale, or likely to create rework. Do not encode a flawed plan just because Ted suggested it; surface the concern and implement the structurally stronger version when the intent is clear.
- Do not duplicate doctrine that already exists. Before adding reusable process language, prefer linking or extending existing `_shared`, Canon, Planning, Project Room, or skill surfaces; chain files should carry lane-specific procedure, not parallel doctrine.
- When Hermes, database, memory, receipts, or routing infrastructure appear in chain planning, treat Ted's primary intent as continuity improvement unless the owner surface or Ted's current instruction says otherwise. Do not reduce that intent to generic automation, dashboarding, or runtime work.
- Staging or revising a lane and executing that lane are separate actions unless Ted explicitly authorizes both.
- Concurrent chains can run only when their write surfaces are disjoint or when shared writes are reserved and later released, parked, or handed to a coordinator.
- Do not execute underlying work discovered during status reconciliation unless the selected chain authorizes it.
- Do not mutate DB rows from a board or inventory unless the selected chain explicitly authorizes DB reconciliation.
- Do not invent a next-session prompt when the lane is complete.
- Do not report QuickSave done while a reservation opened by this lane remains active without a recorded disposition.
- If receipt validation fails, QuickSave is not done; repair the source/disposition mismatch or report the blocker.
