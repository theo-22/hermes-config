---
name: project-room-review
description: Review a Project Room from live room-local state, summarize current standing and next action, check v1-readiness, and prepare bounded save or QuickSave-chain handoffs without changing Control, LayoutSnapper, Builder GPTs, plugins, macOS settings, or unrelated rooms unless explicitly routed.
category: meta
write_mode: file
one_line_use: review a Project Room from live room-local state
fast_pick: "yes"
---

# Project Room Review

Use this skill when Ted asks to review, resume, orient, discuss, advance, save, or decide the next move for a Project Room. Use it when a room `NEXT_ACTION.md` says to run room review.

Do not use it for broad filesystem discovery, all-domain migration, Control implementation, LayoutSnapper changes, Builder GPT edits, plugin creation, macOS automation, or domain/account actions unless Ted explicitly routes that work.

## Boundary

- Project Rooms are durable state.
- Control is the entry interface; dashboard data is overview context, not authority over room-local files.
- LayoutSnapper/project profiles are workspace flow, not durable project state.
- Specialist GPTs/AIs are reviewers or data sources, not source truth.
- Visuals are future candidates after the basic review/workspace loop proves useful.

## Read Order

Read only the target room and directly named supporting surfaces.

1. `CURRENT_STATE.md`
2. `NEXT_ACTION.md`
3. `README.md`
4. `01_Source_Inventory.md`, if present
5. `02_Open_Questions.md`, if present
6. `03_Decisions.md`, if present
7. `04_Working_Model.md`, if present
8. recent entries from `05_Planning_Log.md`, if present
9. any room-local files named by `NEXT_ACTION.md` or Ted
10. `/Users/ted/Projects/PROJECT_ROOMS_STATUS.md` or Control Project Rooms API only as overview/dashboard context

If expected room files are missing, report a room-health flag. Do not invent contents.

## Mode Selection

Choose the lightest mode that fully answers Ted's routed request.

| Mode | Use when | Write behavior |
|---|---|---|
| `review` | Ted wants orientation, current standing, or discussion input | No writes unless Ted asks to save a durable outcome |
| `decision` | Ted is choosing between room-level options | Save the decision only if Ted decides |
| `planning` | Scope, source order, boundaries, or success signal need shaping | Write only room-local planning artifacts and handoff files |
| `v1-readiness` | The room may be close to implementation but needs a gate check | Write a readiness report only if useful for the room |
| `orchestration` | The v1-ready gate passes and Ted routes chain assembly | Write a room-local QuickSave chain; do not execute links |
| `save` | The session produced durable room state that needs closeout | Update room-local state and QuickSave receipt where required |
| `implementation handoff` | Ted routes a future implementation lane but not execution now | Write a bounded prompt or chain link with stop rules |

If Ted's wording and room state disagree, follow the room-local current state unless Ted explicitly overrides it. If the wrong mode would cause writes or implementation routing, ask one focused question.

## Room Review Card

Produce a compact card when reviewing:

```markdown
**Room Review**
- Room:
- Lifecycle:
- Current standing:
- Live next action:
- Decisions in force:
- Open questions:
- Blockers / stale flags:
- Review requests:
- Suggested next move:
- Mode verdict:
- Save / handoff:
```

Present only decisions Ted is positioned to make: bounded next move, planning versus v1-readiness, accept/reject/revise a v1 target, route an implementation lane, or consult a named specialist reviewer/data source.

Do not ask Ted to choose mechanics the AI can determine from the room, such as exact commands, parser choices, or read order.

## State Handling

- Pending work: name only live room-file or Ted-routed work. Separate planning, decision, review, implementation, and closeout/save.
- Decisions: treat `03_Decisions.md` and current state as binding unless Ted changes them.
- Open questions: group by what they block: v1 target, implementation scope, source/read order, verification, or non-blocking design.
- Blockers: name concrete missing conditions, such as no first usable outcome, unauthorized write surface, unclear verification, dashboard drift, or domain/security action requiring separate routing.
- Stale/drift flags: flag disagreement among room files, dashboard seed, missing paths, completed work still listed as next action, or GPT/plugin/dashboard surfaces treated as stronger than the room.
- Review requests: identify reviewer/source, exact question, files to provide/read, expected output, and stopping condition. Output returns to the Project Room as input.

When reviewing a room, distinguish honest blockers from pre-deferring language. If a room is truly waiting on an external event, Ted decision, elapsed time, or explicit route, keep that blocker. If the room has an intended future review but the wording says only "Hold", "Wait", or "Do not start", rewrite the room-local `CURRENT_STATE.md` / `NEXT_ACTION.md` during the saved review as: `Next review pass: <question or decision>. Owner: <actor>. Trigger: <date/event/condition>, otherwise review during the next project-room-review cycle.` Apply this per reviewed room only; do not sweep rooms without reviewing their local state.

## Digest Topic Index Check

During every Project Room review, do a light conditional check of `/Users/ted/Operations/reports/Digest_Topic_Index/LATEST.md` after the room-local files are understood. Use it only when it helps the room: the room names an external/current topic, long-running watch, research need, platform/provider/service/tool issue, clinical/policy topic, or a parked future revisit trigger. If a matching topic page exists, include the useful hit count or "zero hits" in the Room Review card under `Review requests` or `Suggested next move`. If no matching topic exists but the room clearly has a durable watch topic, suggest adding a custom profile to `/Users/ted/Operations/config/digest_topic_profiles.json`; do not add one unless Ted routes that write. Do not treat index hits as authority or implementation authorization, and do not force the check for rooms whose next action is purely local cleanup, closeout, or known-file editing.

## v1-Readiness

A room is v1-ready only when all are true:

- first usable outcome is named
- next implementation slice is bounded
- source/read surfaces are known
- write surfaces are known
- prohibited surfaces are named
- verification can be completed in-session
- QuickSave versus full session-end boundary is clear
- Ted explicitly routes the first lane

Use this output:

```markdown
**v1-Readiness**
- Outcome:
- Slice:
- Read surfaces:
- Write surfaces:
- Prohibited surfaces:
- Verification:
- Closeout:
- Ted routing:
- Verdict: ready | not ready
```

If any item fails, verdict is `not ready` and the next move should repair the highest-blocking missing condition. Do not assemble a chain for a room merely because it has ideas.

## QuickSave Chains

When a room is v1-ready and Ted routes implementation orchestration, write a room-local chain file instead of a loose TODO:

`NN_QuickSave_Chain_<short_slug>_<YYYY-MM-DD>.md`

Each chain includes source room path, purpose/v1 target, chain status, link list, stop rules, and closeout expectations.

Each link uses:

```markdown
## Link <id> - <title>

**Status:** queued
**Read order:**
**Task:**
**Allowed changes:**
**Prohibited changes:**
**Verification:**
**Closeout:**
**Next link trigger:**
```

One link equals one executable slice. Links must be runnable from startup authority plus the room. Execution runs one link at a time. Each link says whether QuickSave is enough or full session-end is required.

Source-disposition defaults:

- `still open` when the room next action remains a decision or review step
- `rewritten` when a completed next action becomes a narrower next review, decision, or implementation-routing step
- `parked` when waiting on a trigger, outside review, elapsed time, or Ted decision
- `completed and removed` only for source items in a removable TODO/checklist
- `none` only when no durable source item existed, using the receipt tool's no-source override

## Session Boundary

At the end of each room review or chain link, decide whether continuing in the warm session is better than starting fresh.

Prefer the warm session when:

- the next step is the same room and same phase
- startup checks, room files, and boundaries are already loaded
- the next action is review, decision, planning, or a narrow follow-on edit

Prefer a fresh session when:

- the next step changes write surface or risk class
- implementation begins after review/planning
- Control, LayoutSnapper, Builder GPTs, plugins, runtime behavior, schemas, services, automation, account/security, finance, or clinical surfaces become involved
- context is noisy enough that loaded state may mislead more than help

After the first pilot uses, update this skill or the owning room if the session-boundary rule proves wrong in practice.

## Save / Handoff

When reviewing only, save a planning-log note only if a durable outcome was reached.

When writing a plan/spec, save it in the room, update the planning log, rewrite `NEXT_ACTION.md` if completed, and keep source disposition explicit.

When assembling a chain, write it in the room, update `CURRENT_STATE.md`, `NEXT_ACTION.md`, and planning log, then append and validate the Operations QuickSave receipt if closing a room next-action or chain slice.

When routing to another AI/GPT, create a bounded review packet or prompt with exact files and stopping condition. Do not imply implementation authorization.

## Must Not Do Without Explicit Routing

- edit Control dashboard/frontend/backend
- edit LayoutSnapper source, layouts, app install, or macOS settings
- create or modify Builder GPTs
- create plugins
- move durable state out of Project Rooms
- write to project/domain rooms outside the named target room
- perform account, finance, clinical, WHM/cPanel, or external-service actions
- use dashboard seed state to override room-local truth
- assemble implementation chains for rooms that are not v1-ready
- execute implementation links from a review-only session
