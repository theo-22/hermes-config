---
name: quick-save
description: Save the current bounded task without running full session-end. Use when Ted asks to save work, quick-save, checkpoint, update CHANGES_LOG, or wrap a short one-task session where the work is already done and no full closeout is needed. Updates the correct durable continuity surfaces, verifies touched repo state, names any uncommitted/unpushed work, and decides whether full session-end is required instead. Do not use for sprawling multi-workstream sessions, unresolved advisory closeout, cross-AI handoff, architecture drift, or when Ted explicitly asks for /session-end.
category: meta
write_mode: file
one_line_use: save a bounded task without full session-end
fast_pick: "yes"
---

# Quick Save

Save a finished bounded task without running full `/session-end`.

QuickSave is for short sessions: one task, durable surfaces updated, repo state checked, and a clean handoff back to Ted. It is not a substitute for full session-end when the session created broad continuity obligations.

## Closeout Chooser

Use this simple user-facing split:

- **QuickSave:** one contained task, already finished or intentionally paused, where the next actor only needs a clean saved state.
- **Full session-end:** broad session, multiple workstreams, shared skills, Project Rooms, commits/pushes, cross-AI handoff, architecture/startup changes, or any situation where future continuity would be unclear without a sweep.

Ted should not need to choose among actor-local closeout files. In a Codex window, full session-end means `/Users/ted/Operations/Codex_Handoff/SESSION_END.md`. In a Claude Code window, full session-end means `/Users/ted/Operations/SESSION_END.md`. Legacy routers are fallback mechanics, not the normal decision surface.

## Use When

- Ted says `quick-save`, `save work`, `save this`, `checkpoint`, or asks for `CHANGES_LOG etc.`
- The task is one coherent unit and the work is already complete or intentionally paused
- The main need is durable continuity, not a full operational sweep
- A full `/session-end` would add ceremony without improving the next session's ability to resume

## Escalate To Full Session-End

Use the full session-end protocol instead when any of these are true:

- Ted explicitly asks for `/session-end`, `wrap`, or a full closeout
- Multiple workstreams changed and the next priority/order may have shifted
- There are unresolved advisories, open closeout checks, or promised follow-ups that need sweeping
- Cross-AI handoff is required
- Architecture drift was created or resolved
- Startup/session-end instructions changed
- Git commit/push is part of the requested closeout
- You cannot confidently name what changed and what remains

If unsure, say why and run full session-end. QuickSave should reduce overhead, not hide loose ends.

## Workflow

1. **Name the bounded task.**
State the work being saved in one sentence. If it is not one coherent task, escalate.

2. **Verify the live surface.**
Check the actual files or runtime state that were changed. Do not save from memory.

For receipt proof, prefer the narrowest surface that proves the task: a completion report, source packet, generated receipt, room-local state file, or exact output file. Use `CHANGES_LOG.md` as the proof path only when the log entry itself is the changed surface or when it contains the exact verification needed. For multi-item closure, avoid pointing only at `CHANGES_LOG.md`; write or name a focused proof/report/source packet so future review does not have to mine history.

3. **Find touched repo roots.**
Use the repo map or `git rev-parse --show-toplevel` before git inspection. Check status for each touched repo. Do not stage, commit, pull, or push unless Ted asked.

4. **Update continuity only where earned.**
Use the lightest durable surface that future actors will actually read:

- `Operations/CHANGES_LOG.md` for permanent system-change history
- session event DB if this is a Codex session event and the backend/token path is available
- `Operations/RECENT.md` only as fallback or when that surface is the current local continuity target
- `Operations/PRIORITY.md` only if priority/order changed
- project room README/log when the work belongs to a Project Room
- inbox/work item state only if the task resolved or rerouted that item

Do not update every surface by habit.

5. **Reconcile the source TODO or chain item.**
Always identify whether the saved work came from a TODO, orchestration-chain item, Project Room next action, inbox item, or no durable source item.

Then make an explicit source-item disposition:

- `none` — no durable source item started this work
- `still open` — parent work is not complete yet
- `completed and removed` — source TODO is done and was deleted from `TODO.md`
- `rewritten` — source item still exists but was narrowed, rerouted, or reframed
- `parked` — source item remains but is no longer active until its trigger/date

If a source TODO or chain item is completed, remove or rewrite it in the same QuickSave pass and log the disposition. Do not leave completed parent TODOs behind for Ted or a future AI to rediscover. If you cannot safely decide whether the source item is complete, say `Source item: still open` and name the evidence needed.

6. **Update the active ledger when one exists.**
If the work came through a conductor board, session-chain ledger, Project Room status surface, DB work-item board, or similar active tracking ledger, update that ledger in the same QuickSave pass so it no longer advertises stale work.

For each relevant ledger, record the current state using the same source disposition language as the receipt: `still open`, `completed`, `rewritten`, or `parked`. If the ledger already matches live state, say `Ledger update: already current` in the final response. If no active ledger applies, say `Ledger update: not applicable`.

Do not create new ledger work from adjacency. This step only reconciles the ledger that actually routed or advertised the saved task.

7. **Close owned surface reservations.**
If the task opened a reservation in `/Users/ted/Operations/session_chains/SURFACE_RESERVATIONS.md`, close it before claiming QuickSave is done.

Use one of:

- `released` - the reserved write is complete and no coordinator handoff is needed
- `parked` - the reservation remains intentionally blocked, with the reason and next trigger recorded
- `coordinator_handoff` - shared reconciliation is needed after one or more chains finish

Do not close reservations owned by other active chains unless Ted explicitly routes a coordinator reconciliation pass.

8. **Preserve source-vs-current routing.**
If a path moved or a canonical surface changed, name the current path and avoid re-saving stale copies.

9. **Report repo state.**
Name whether touched repos are clean, modified, staged, untracked, committed, or not committed. If there are unrelated changes, say they were left alone.

10. **Decide whether a next-session prompt is earned.**
Always make an explicit verdict: `Next-session prompt: needed` or `Next-session prompt: not needed`.

Only mark a prompt as needed when there is a real next bounded action that a future session should run, such as an ongoing staged effort, Project Room next action, checklist item, implementation-session map, unresolved next target, or policy decision review.

Do not invent a prompt for a completed chain, a closed slice, a no-op verification, or a vague "continue from here" situation. If no next action is earned, say `Next-session prompt: not needed` and stop there.

If a prompt is needed, include the copy/paste prompt for the next session.

The prompt should be short and operational:

- Name the startup authority or project authority to read first.
- State the landed current state from live evidence, not memory.
- Name the next likely bounded target.
- Include cautions that would prevent a known bad promotion, broad scan, stale authority read, or policy overreach.
- State whether QuickSave or full session-end is preferred next time and why.

If a next action exists but needs a policy choice, write the next-session prompt as a decision-review prompt, not an implementation prompt.

11. **Return a compact save receipt.**
Before the final response, append and validate a machine-readable closeout row when the work came from a TODO, orchestration-chain item, Project Room next action, or other durable source item:

```bash
/Users/ted/Operations/scripts/quicksave_closeout_receipt.py append \
  --task "<bounded task>" \
  --quicksave "done|not done" \
  --source-path "<path to source queue, default Operations/TODO.md>" \
  --source-item "<exact source item text, if any>" \
  --source-disposition "none|still open|completed and removed|rewritten|parked" \
  --proof-path "<path to proof/report, if any>" \
  --next-session-prompt "needed|not needed"
/Users/ted/Operations/scripts/quicksave_closeout_receipt.py check
```

Before appending, check whether `--proof-path` is a strong proof surface for this task. A history log can support the receipt, but if the task closed several items or rewrote a source queue, the receipt should point at the focused report, archived packet, generated receipt, or owner file that shows the closure directly.

If the receipt check fails, the QuickSave closeout is not done. `source_disposition=none` requires `--allow-no-source`; do not use it for TODO/chain/Project Room work. `still open`, `parked`, and `rewritten` receipts require notes explaining the current state.

Keep the final response short. The receipt must explicitly answer whether QuickSave happened and whether Ted needs a next-session prompt:

- `QuickSave:` `done` or `not done`
- `Saved:` durable files/surfaces updated, or what is missing if QuickSave is not done
- `Verified:` live checks performed
- `Source item:` `none`, `still open`, `completed and removed`, `rewritten`, or `parked`
- `Ledger update:` `updated`, `already current`, or `not applicable`
- `Surface reservation:` `none`, `released`, `parked`, or `coordinator_handoff`
- `Repo state:` clean or pending changes
- `Next-session prompt:` `needed` or `not needed`; include the prompt only when the verdict is `needed`
- `Not full session-end because:` one sentence

If QuickSave was not completed, do not imply it was. Say `QuickSave: not done` and name the exact missing action or blocker. If the task is fully complete and no continuation is earned, say `Next-session prompt: not needed`; do not include a decorative or inert prompt. If the source item was completed, do not leave it in the active TODO list.

## CHANGES_LOG Entry Shape

Use this only when the work changed durable system state:

```markdown
## YYYY-MM-DD — concise title [Codex]
- **What changed:** One sentence.
- **What's now true:** One sentence the next actor needs.
- **Verification:** Path, command, report, or live state checked.
```

If the work was only a local note, draft, or no-op verification, skip CHANGES_LOG and say why.

## Boundaries

- QuickSave does not clear all inboxes.
- QuickSave does not run advisory closeout unless the current bounded task is about that advisory.
- QuickSave does not replace backup verification.
- QuickSave does not declare architecture complete.
- QuickSave does not commit/push by default.
- QuickSave can say "this needs full session-end" and stop being QuickSave.

## Update-Surfacing Backstop

If session-end requirements, repo boundaries, or continuity surfaces change, update this skill in the same pass. Check:

- `/Users/ted/Operations/Codex_Handoff/SESSION_END.md`
- `/Users/ted/Operations/SESSION_END.md` when CC parity matters
- `/Users/ted/Canon/System/REPO_WORKSPACE_MAP.md`
- `/Users/ted/Operations/CHANGES_LOG.md` for current entry style
