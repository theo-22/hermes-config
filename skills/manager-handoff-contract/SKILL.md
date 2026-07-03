---
name: manager-handoff-contract
description: Shape an idea, observation, mismatch, suggestion, or cheap-model/Hermes finding into a manager-ready handoff for Ted, Codex, and Claude. Use when a lower-cost worker, overnight monitor, project Home, dashboard report, conversation, or quick planning pass has produced something that might become a decision, Home update, room, work order, proposal, implementation task, or discard. The skill defines required handoff outcomes without prescribing how the worker must think. Do not use to approve, implement, promote to Canon, or preserve every thought.
category: judgment-only
write_mode: none
one_line_use: shape manager-ready handoffs from lower-cost worker output
fast_pick: "yes"
---

# Manager Handoff Contract

Use this skill to make handed-over work usable by the primary managers: Ted, Codex, and Claude.

The purpose is not to make every idea durable. The purpose is to give a worker a simple outcome contract: if it hands something to the managers, the handoff must be shaped enough that the managers can accept, reject, discard, fold into existing work, or route forward without reconstructing the whole conversation.

## Core Rule

Define outcomes, not method.

Do not tell the worker how to reason, brainstorm, rank, or write internally. Tell it what the handoff must contain if it wants manager attention.

Most ideas should not become handoffs. Allow ordinary thoughts to evaporate unless they have enough shape, evidence, connection, or repeated signal to deserve manager review.

## When To Use

Use this skill when:

- Hermes, an overnight worker, or a cheaper model noticed something that may need manager review.
- A conversational idea is becoming shaped enough to hand to Ted, Codex, and Claude.
- A Project Home or room needs to decide whether material belongs in Home state, a Home room, a work order, a proposal, or no action.
- A report says "this needs attention" but does not yet say what output should happen.
- A worker wants to hand off planning without silently deciding or implementing it.

## When Not To Use

Do not use this skill when:

- Ted has already asked for direct implementation.
- The item is a fleeting thought with no current use.
- The item can be handled immediately as small bounded work.
- The worker is trying to promote something to Canon, `_shared`, or project standard.
- The handoff would create more overhead than value.

## Idea Metabolism

Classify the material before writing a handoff:

| State | Meaning | Manager effect |
|---|---|---|
| Evaporate | Interesting in the moment but not worth preserving. | No handoff. |
| Simmer | Worth watching briefly, but not ready for action. | Optional light note or future observation; no manager decision required. |
| Shape | Enough signal to ask managers what it should become. | Write a manager-ready handoff. |
| Commit | Managers accepted it into Home state, work order, proposal, implementation, or another durable lane. | Follow the routed process for that lane. |

This skill starts at **Shape**. It should not turn **Evaporate** or **Simmer** material into paperwork.

## Handoff Outcomes

A manager-ready handoff must include these outcomes in plain language:

1. **What is being handed over?**
   - Name the idea, issue, mismatch, opportunity, or proposed work.

2. **Why does it matter now?**
   - Name the current trigger: changed state, repeated signal, risk, opportunity, cost, user friction, project connection, or active Home need.

3. **What state is it in?**
   - Use one: tossed idea, simmering idea, shaped candidate, guided decision needed, bounded work ready, blocked, proof needed, or discard recommended.

4. **What output should happen next?**
   - Name the requested manager effect: decision, Home update, Home room, work order, Builder batch, implementation pass, report, archive/retire, or no action.

5. **What evidence or source is attached?**
   - Provide files, links, screenshots, dashboard state, logs, prior decisions, repeated observations, or say `conversation only; no external evidence yet`.

6. **What should not happen?**
   - Name boundaries: do not implement yet, do not promote to Canon, do not edit runtime, do not spend high-cost model time, do not preserve unless accepted, or do not touch protected surfaces.

7. **What would count as accepted?**
   - Name the manager-facing acceptance test: what would let Ted/Codex/Claude say this is ready for the next lane.

## Output Format

Use this compact shape:

```markdown
# Manager Handoff: <short title>

## What
<one to three sentences>

## Why Now
<trigger, risk, opportunity, or active Home/project connection>

## Current State
<tossed idea | simmering idea | shaped candidate | guided decision needed | bounded work ready | blocked | proof needed | discard recommended>

## Requested Manager Effect
<decision | Home update | Home room | work order | Builder batch | implementation pass | report | archive/retire | no action>

## Evidence
<paths, links, screenshots, observations, or "conversation only; no external evidence yet">

## Boundaries
<what should not happen from this handoff>

## Acceptance Test
<what would make this ready for the next lane>
```

Keep it short. A handoff that requires managers to read a long essay has failed the skill unless the evidence itself is complex.

## Routing Guidance

After shaping the handoff, do not assume it should be saved.

- If Ted asked only to discuss, present the handoff in chat.
- If Ted asked to save it, route it to the active owner surface.
- If the owner surface is unclear, use `surface-routing`.
- If the item is proposal-shaped but not ready, use `proposal-candidate-surfacing`.
- If it is ready to become a proposal packet, use `proposal-packet`.
- If it is ready to become a guided or bounded work lane, use `workflow-orchestration`.

## Hermes Use

Hermes may use this skill as a lightweight handoff contract for monitoring and conversational idea work.

Hermes should not decide the manager outcome by itself. It should package shaped material so Ted, Codex, and Claude can decide whether to discard, simmer, fold into existing work, or route forward.

For Hermes or any LaunchAgent-backed worker, logs and runtime writes must follow the current Hermes runtime rules. This skill does not authorize Hermes configuration edits, cron changes, model changes, LaunchAgent changes, or writes to protected surfaces.

## Failure Modes

- **Over-capture:** every thought becomes a handoff. Fix by using the idea metabolism gate and allowing most ideas to evaporate.
- **Hidden decision:** the worker routes or implements instead of asking managers. Fix by separating requested manager effect from authorization.
- **Vague attention item:** the handoff says "needs attention" but not what output should happen. Fix by naming the requested manager effect.
- **Evidence fog:** the handoff sounds confident but has no source. Fix by naming the evidence or saying it is conversation-only.
- **Premature promotion:** the handoff calls something Canon, standard, or v1 before managers accept it. Fix by labeling actual maturity.

## Done Standard

The skill is complete when the handoff lets a manager answer:

- discard or keep watching?
- fold into existing work or make a new room?
- guide a decision or run bounded work?
- preserve as state or leave it in conversation?
- what proof or boundary matters before action?

If those answers are still hidden, the handoff is not ready.
