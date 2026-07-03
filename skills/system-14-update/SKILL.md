---
name: system-14-update
description: >
  Update the System 14 release plan with current work — chapter-first, then
  thread upward into the spine and home files. No parallel plans, no chat-only
  summaries.
trigger: >
  Ted says "update System 14", or work has landed in a chapter room and the
  plan needs re-threading.
---

# System 14 Update

Update the System 14 plan with the current work.

## Prompt

Update the System 14 plan with the current work.

Start here:

1. Read `README.md`, `CURRENT_STATE.md`, `NEXT_ACTION.md`, and `Planning_Docs/System_14_Plan.md`.
2. Identify which chapter room owns the work. If the chapter is still skeletal but live work has begun, open it as a room with `README.md`, `CURRENT_STATE.md`, and `NEXT_ACTION.md`.
3. Update the chapter first, then thread the change upward into the spine, Home `CURRENT_STATE.md`, `NEXT_ACTION.md`, `README.md`, and `TREE.md` only where needed.
4. Preserve the distinction between current state, standards/goals, proof, and next action.
5. Verify there are no stale contradictions, commit/push the repo, and record closeout in Operations if durable state changed.

Do not create a parallel plan or chat-only summary. The plan is the System 14 spine; chapter rooms carry the live detail.

## System 14 Architecture (Supplementary Context)

### Repo Path

```
/Volumes/Extra/Substrate/Projects/Substrate_v14/
```

This is a git repo. Commit and push after updates.

### Version Model

System 14 is a **release definition** — a set of documented goals the live Substrate is being grown to meet. When every chapter goal is met, that state gets stamped as the System 14 release. The plan document clones forward per release; the system itself evolves in place at `/Volumes/Extra/Substrate/`.

> "The live system is always the same thing in the same place. It just changes to fit a definition. Repeat." (Ted, 2026-07-02)

### What Each File Is

| File | Role |
|------|------|
| `README.md` (Home root) | Operating manual — version model, structure, actor roles, closure rules |
| `CURRENT_STATE.md` (Home root) | What's true right now about the overall release |
| `NEXT_ACTION.md` (Home root) | Immediate next steps across all chapters |
| `TREE.md` | Directory listing with annotations |
| `Planning_Docs/System_14_Plan.md` | **The spine** — version document telling the story of the release |
| `Planning_Docs/README.md` | Chapter index and room pattern |
| `Planning_Docs/<NN>_Name/README.md` | What this chapter is and how it works |
| `Planning_Docs/<NN>_Name/CURRENT_STATE.md` | What's true right now in that chapter |
| `Planning_Docs/<NN>_Name/NEXT_ACTION.md` | Immediate next steps in that chapter |

### Update Flow (Bottom-Up)

1. **Chapter first** — update the chapter room's `CURRENT_STATE.md` and `NEXT_ACTION.md`
2. **Thread into the spine** (`System_14_Plan.md`) — the spine tells the story of the release. Add resolution, proof, and status changes.
3. **Home files only where needed** — touch `CURRENT_STATE.md`, `NEXT_ACTION.md`, `README.md`, `TREE.md` only if the change affects the overall release picture.
4. **Preserve the four-state distinction**:
   - **Current state** — what's true now (lives in `CURRENT_STATE.md`)
   - **Standards/goals** — what we're building toward (lives in chapter READMEs, spine)
   - **Proof** — evidence that a capability landed (lives in chapter rooms)
   - **Next action** — what to do next (lives in `NEXT_ACTION.md`)
5. **Verify no stale contradictions** — scan for conflicting dates, statuses, or claims
6. **Commit and push** the repo
7. **Record closeout** in `/Users/ted/Operations/CHANGES_LOG.md` if durable state changed

### Active Chapters (as of 2026-07-02)

| # | Room | Domain | Status |
|---|------|--------|--------|
| 01 | Role_Runtime | Role runtime architecture | ACTIVE |
| 02 | Portability | Runtime portability | Planned |
| 03 | Coordinator_Access | Coordinator read/write access | In progress |
| 04 | Project_Homes | Project Home governance | Planned |
| 05 | Inbox_Routing | Cross-actor inbox routing | Planned |
| 06 | Memory_Pieces_Brain | Memory layer | Planned |
| 07 | Canon_Runtime | Canon governance runtime | Planned |
| 08 | Audit_Closure | Audit role closure and verification | Planned |
| 09 | Domain_Migrations | Domain migration patterns | Planned |
| 10 | Coordinator-Hermes | CH profile + Coordinator partnership | ACTIVE |
| 11 | Hermes_Role | Canonical Hermes role definition | ACTIVE |
| 12 | Dashboard_Standards | Dashboard redesign standards | ACTIVE |
| 13 | Async_Communication | Shared async communication layer | ACTIVE |

### Closure Rules

Status language is honest. These apply to *bounded asks*, not to homes/rooms:

| Status | Meaning |
|--------|---------|
| `DONE` | Asked capability matches delivered capability |
| `PILOT VALIDATED / PARITY INCOMPLETE` | Path works but predecessor parity or requested breadth missing |
| `INTENTIONALLY CHANGED` | Delivered shape differs by design, difference is explicit |
| `BLOCKED` | Named missing input or protected boundary prevents progress |
| `NOT EXECUTED` | No implementation happened |

> **`DONE` closes a capability, never a home or room.** No home or room is ever "done" — the substrate is under continuous development.

### Pitfalls

- **Do not create a parallel plan.** The spine is the plan. Chapter rooms carry the live detail. A chat-only summary or separate plan doc is wrong — update in place.
- **Do not rewrite the spine as a task list.** The spine is a story of growth, not a TODO list.
- **Do not mark a home or room as "done."** Status labels describe bounded asks. Homes and rooms carry living `CURRENT_STATE`s.
- **Do not skip the chapter-to-spine thread.** Updating a chapter room without threading into the spine creates drift that looks like contradictory planning.
- **Do not update home files speculatively.** Only touch `CURRENT_STATE.md`, `NEXT_ACTION.md`, `README.md`, or `TREE.md` at Home root when the change genuinely affects the overall release picture.
- **The prompt file is in the project home.** The update prompt itself lives at `/Volumes/Extra/Substrate/Projects/Substrate_v14/System 14 Update Prompt.md`. It should remain as-is; this skill is the portable version.
