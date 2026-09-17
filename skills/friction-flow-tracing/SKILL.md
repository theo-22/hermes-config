---
name: friction-flow-tracing
description: Notice and cheaply capture meaningful friction or flow that changes a real work trajectory, especially during Concept Graph neighborhood walks, for later grouped Map Curator or Instrumentation review. Do not use for constant narration, ordinary difficulty, direct graph edits, or one work item per observation.
metadata:
  category: database-integrated
  write_mode: shared
  one_line_use: capture a tiny evidence trace now and curate recurring patterns later
  fast_pick: "yes"
---

# Friction-Flow Tracing

Keep one light observational posture active during real work: notice only events that materially change the route, record them while the evidence is live, and immediately return to the user's task.

## When to capture

Capture when a node, road, neighborhood, representation, sequence, tool, authority boundary, or handoff materially changes understanding or execution. Useful signals include:

- a graph neighborhood suddenly makes the discussion click;
- Ted has to repeat or reframe meaning the map should have carried;
- a neighborhood sends the session down a wrong or unhelpful path;
- missing context, a tool, or a handoff causes a real detour;
- a sequence or representation produces unusually strong flow;
- a role, tool, authority, or runtime seam repeats as friction.

Do not capture routine effort, every tool call, or vague dissatisfaction. Do not interrupt the work to adjudicate the observation. In an unusually long session, briefly re-prime this posture once if it has clearly fallen out of view; a timer or repeated reminder is not required.

## Capture one evidence lead

Record only what the later reviewer needs:

- timestamp, actor, and session reference;
- `friction` or `flow`;
- current task/topic;
- node ids, edge ids, or neighborhood when applicable;
- what happened and what changed the trajectory;
- an inspectable evidence pointer when one exists;
- an optional possible improvement, explicitly a candidate;
- route: `map_curator`, `instrumentation`, or `owner` plus the owner target.

Use the runtime's `friction_flow_trace` tool with `op=capture`. Shell-capable actors may instead run `scripts/friction_flow_trace.py capture ...`. The helper writes one claim-protected append-only event and releases the checkout; it creates neither a work item nor an inbox packet.

## Route by type

- Map meaning, wiring, or context delivery → `map_curator`.
- Recurring role/tool/runtime machinery friction → `instrumentation`.
- A bounded domain-local implementation issue with a known owner → `owner` and name that owner.
- Keep positive flow specimens. They show what may be worth reproducing.

If the same event touches more than one route, capture it once at the route best able to decide the next transition. The reviewer can route the evidence onward; do not duplicate the trace.

## Grouped review

Map Curator and Instrumentation receive their open traces in their startup bundle. Reviewers may also call `friction_flow_trace` with `op=list`; the result groups open traces by route, neighborhood/topology, and kind.

For each coherent group:

1. Inspect the cited evidence and current graph or machinery.
2. Compare recurrence and nearby traces.
3. Make any earned change through the owner's normal reversible operation.
4. Append a disposition: `curated`, `routed`, `dismissed`, `needs_evidence`, or `duplicate`.

Disposition records are append-only. They do not rewrite the original observation.

## Boundaries

- A trace is a lead, not graph state, a settled finding, or authority.
- Observers gain no node/edge mutation authority.
- No automatic graph mutation follows capture.
- No per-trace work item or inbox packet.
- This agenda does not replace `work_items`; if grouped review earns real work, use normal admission/routing once for that coherent obligation.
- Curator Harvest remains the session-close path for already-persisted graph candidates. This trace lane reuses its evidence-first, grouped-review discipline without forcing mid-session observations through a session-close package.

## Success

The trace takes seconds, the original work resumes immediately, the ledger remains parseable and append-only, grouped startup review can retrieve it, and any consequential mutation still occurs through the established owner tool with its own evidence and authority.

## Runtime notes

- Codex and Claude Code: use the bundled script or the MCP tool; do not edit the ledger by hand.
- ChatGPT role runtimes: the universal startup bundle includes this skill, and eligible roles receive `friction_flow_trace`.
- Read-only or disconnected runtimes: keep one compact trace in the current session and route it once through an actor with the helper; do not invent a parallel queue.

## Update backstop

This skill names a live ledger, MCP tool, startup injection, and Control helper. If any is missing, preserve the capture/group/disposition boundaries and repair the shared mechanism rather than creating a local fork.
