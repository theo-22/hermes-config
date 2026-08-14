---
name: route-work-item-ownership
description: Apply an already-authorized Coordinator routing decision to canonical Control `work_items` by retargeting a live item to Orchestrator or Map Curator, or superseding an obsolete item with a linked prepared successor. Use when queue ownership is stale after a routing decision, a specialist cannot see work because `work_items.owner` still names the old role, or obsolete framing must become terminal without losing history. Requires live-state readback, an existing authority file, a Coordinator-origin successor orchestration, task claims, atomic audited mutation, receiving-role proof, and released claims. Do not use for backlog/session shaping, direct implementation authorization, arbitrary owner changes, required-owner rows, terminal-item reopening, or role redesign.
metadata:
  category: database-integrated
  write_mode: db
  one_line_use: retarget or supersede canonical work-item ownership without widening authority or rewriting history
  fast_pick: "yes"
---

# Route Work Item Ownership

Land one settled queue-routing decision in the canonical work-item and orchestration history without granting execution authority or creating a parallel routing ledger.

## Authority and Boundaries

- Treat `/Users/ted/Control/backend/system.db#work_items`, read through the live Control API or installed MCP tools, as queue authority.
- Require an existing readable authority file from Ted or Coordinator. A chat summary or proposed destination is not enough.
- Require a prepared or delivered Coordinator-origin orchestration naming the same work item. Its target must match a retarget destination.
- Retarget only to the operation's current allowlist: `orchestrator` or `map_curator`. Do not expand the allowlist inside a routing session.
- Retarget changes the soft queue owner only. It must not grant, extend, or imply implementation authority.
- Supersede makes the old work item terminal and links its prepared successor. It must not rewrite the historical owner or reopen an old attempt.
- Reject generic routing for any row with `required_owner`, any unsupported lifecycle state, revoked work, missing successor, missing authority source, or stale observed fields.
- Keep broader role design between Coordinator and Orchestrator, execution, acceptance, and queue cleanup outside this skill.

## Canonical Workflow

### 1. Read the live row and routing record

Read the complete named authority file first. Then read:

- the current work-item row, including `owner`, `required_owner`, `state`, and exact `state_changed_at` value, including `null`;
- the proposed successor orchestration and its `origin_role`, `target_name`, `work_item_id`, `lifecycle_state`, and `authority_state`;
- existing route/successor links and events, so an earlier completed transition is treated as an idempotent replay rather than duplicated.

Stop if the decision, row, and successor do not describe the same work.

### 2. Choose exactly one transition

- Use `retarget` when the work remains live but the canonical receiving role is wrong.
- Use `supersede` when the old framing is obsolete and the prepared orchestration is its successor.
- Use neither when the item is already terminal for another reason, needs a new decision, lacks a prepared successor, or has a hard `required_owner` gate.

Do not use a direct database update or the generic work-item state endpoint for this transition.

### 3. Claim the mutation lane

Acquire DB-backed task claims for `work_items:<id>` and the successor orchestration before invoking the operation. If another actor holds either target, stop or coordinate; do not bypass the claim.

Record an idempotency key tied to the authority decision and work item. Reuse that exact key on retry.

### 4. Invoke the canonical operation

Use `orchestrator_control_op` with `op="route_work_item"`, the successor orchestration as the outer `orchestration_id`, and the operation fields inside the outer key `args`. The installed dispatcher key is exactly `args`, not `arguments`:

```json
{
  "op": "route_work_item",
  "orchestration_id": "orch_example_successor",
  "args": {
    "work_item_id": 337,
    "transition_kind": "retarget",
    "successor_orchestration_id": "orch_example_successor",
    "expected_owner": "codex",
    "expected_state": "pending",
    "expected_state_changed_at": null,
    "target_owner": "map_curator",
    "reason": "Authorized design-judgment route",
    "authority_actor": "coordinator",
    "source_ref": "/absolute/path/to/authority.md",
    "idempotency_key": "route-work-item:337:authorized-decision"
  }
}
```

For `supersede`, set `transition_kind` to `supersede` and omit `target_owner`. `successor_orchestration_id` must still equal the outer orchestration ID.

Never weaken stale guards to make a rejected call pass. Re-read live state and obtain a new decision if observed state has changed materially.

### 5. Prove canonical read-side visibility

Read back the work item, successor orchestration, link, and event:

- retarget: owner changed, work-item state stayed unchanged, link kind is `work_item_route`, lifecycle is delivered or already delivered, and authority state is unchanged;
- supersede: old owner stayed unchanged, state is `superseded`, link kind is `work_item_successor`, and the successor remains separately authorized or draft according to its prior state;
- both: the event contains old/new snapshots, reason, actor/authority, source, timestamp, and idempotency key.

Use the receiving role's actual assigned-work surface to prove it now sees the item from `work_items.owner`. When the receiver supports acknowledgement, acknowledge once and verify that acknowledgement does not promote draft authority. A start attempt may be used as a non-mutating negative control only when it is safe and expected to fail closed.

### 6. Verify independently and close

For consequential or multi-row routing, obtain an independent read-only verification covering:

1. exact work-item rows;
2. orchestration lifecycle and authority separation;
3. link/event lineage and idempotency;
4. database integrity;
5. no unrelated queue mutations;
6. receiving-role visibility where required.

Write a durable receipt, release every task/file claim, and verify the active-claim set is empty for the lane. Archive the source packet only after every acceptance clause passes. Leave broader umbrella work pending when the routed slice does not settle it.

## Evidence Standard

Completion requires all of the following:

- canonical row readback;
- orchestration, link, and event readback;
- authority unchanged by retarget;
- receiving-role visibility when the route targets a specialist;
- focused tests for the operation and affected receiving surface when code changed;
- independent verification when the task requires it;
- database integrity check;
- durable receipt and released claims.

A delivered packet, changed owner field, health response, or local unit test alone is insufficient.

## Failure Modes

- **Parallel routing ledger:** a Home packet or local role file becomes a competing queue instead of a content pointer.
- **Authority smuggling:** owner retarget is treated as permission to start implementation.
- **Historical rewrite:** an obsolete item is reopened or renamed instead of superseded with lineage.
- **Stale overwrite:** expected owner/state/timestamp are guessed or omitted after another actor changed the row.
- **Unlinked supersession:** the old row becomes terminal without a prepared successor and queryable link.
- **Protected-row bypass:** `required_owner` is cleared or ignored to force generic routing.
- **Receipt-only completion:** mutation is recorded but the receiving role never sees the canonical address.
- **Cached-client overwork:** a stale connector enum blocks before MCP and is misdiagnosed as server failure. Record the enforcement point and refresh the connector normally; do not weaken the operation.

## Runtime Notes

- **Codex or Claude Code:** use the installed MCP operation when available; use local Control reads only for evidence and diagnosis, never a direct SQLite write.
- **Coordinator or Orchestrator role:** preserve the same authority, stale-state, idempotency, and receipt requirements even if the client exposes a role-specific wrapper.
- **Receiving specialist:** use its assigned-work tool for visibility and acknowledgement. It does not decide its own retarget.
- **Client with cached schema:** reconnect or refresh before the next mutation attempt. A client-side enum rejection is valid bounded evidence that no server mutation occurred.

## Update Backstop

This skill names live operation fields, owner allowlists, and role tools. Before use, inspect the installed `orchestrator_control_op` schema and current Control implementation. If they differ, preserve this skill's authority, history, stale-guard, and evidence rules while proposing one shared-skill update; do not create a local doctrine fork.
