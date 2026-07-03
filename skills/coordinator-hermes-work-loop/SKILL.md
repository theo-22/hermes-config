---
name: coordinator-hermes-work-loop
title: Coordinator-Hermes Work Loop
description: Use when Ted and Coordinator are discussing, designing, or deciding something that should become durable work, a file placement, a scan, a report, or a cleanup task. Coordinator shapes the intent into a bounded Hermes handoff, Hermes evaluates, and executes.
---

# Coordinator-Hermes Work Loop

## When to use

Use this skill when Ted is thinking through a problem and the discussion produces something that should be acted on outside the chat, such as:

- placing a note in a Project Room or Canon_Reshape;
- scanning a path Coordinator cannot read directly;
- saving continuity or Brain notes;
- asking Lab to evaluate a tool or method;
- turning a conversation insight into a durable artifact;
- checking whether something is done, not done, or not worth pursuing.

## Core pattern

Ted thinks / names intent → Coordinator shapes the work → Hermes evaluates the handoff for flow and friction → Coordinator-Hermes executes → result comes back → Coordinator and Ted decide what survives.

## Governing principle

> **Slow = smooth = fast.**

The goal is to do the work well enough the first time that it does not need changes. Think it through before dispatching. The evaluation step is a quality gate that incentivizes good upstream work, not a process to lean on.

If the author does a thorough job — clear scope, defined success, relevant context, no trip wires — Hermes executes in one pass. No iteration needed. That is the fastest path.

The settlement loop (send back → revise → execute) is a safety net for cases the author missed, not the default workflow. If you find yourself depending on it to fix sloppy handoffs, fix the handoff discipline instead.

## Learned-through-use adoption rule

Expect early manual triggering. Ted may need to say "use the work loop," "this is a Coordinator-Hermes thing," or otherwise point at the pattern several times before the trigger becomes reliable.

Treat those repetitions as training data, not failure. When Ted has to manually trigger the skill, ask what signal Coordinator missed and refine the trigger surface or skill wording if the miss is likely to recur.

The goal is gradual reduction of Ted's reminder burden through use, not perfect upfront prediction.

## Coordinator responsibilities

1. Listen for Ted's actual intent, not just the literal task.
2. Decide whether the work belongs in chat, Hermes, Lab, Canon_Reshape, Brain, Coordinator continuity, or another surface.
3. Create the smallest useful Hermes handoff:
   - target path or destination;
   - exact requested action;
   - relevant context;
   - done criteria;
   - stop rules.
4. Send the handoff to Coordinator-Hermes / Hermes.
5. Report back status-first:
   - done / not done / unknown;
   - where it landed;
   - one next action, if any.

## Hermes responsibilities

1. Evaluate the handoff before executing:
   - Is the scope clear and bounded?
   - Are there trip wires or traps in the request?
   - Are the done criteria / success criteria clearly stated?
   - If success is not defined, flag that — a handoff without a clear "done" state is not ready to execute.
   - Is there a simpler / cheaper / faster way?
   - Is this something that should not happen at all?
2. If the handoff is clean, execute it. (Per Act and Report: bounded reversible work does not need a round trip.)
3. If evaluation reveals a real concern, use judgment on how to respond:
   - **Small adjustments** (scope too wide, better path available, cheaper route) → adjust silently, execute, report what changed and why. One round.
   - **Structural concerns** (trip wires, undefined success, protected-surface risk, genuine "should not happen") → send back to Coordinator with the specific concern and concrete suggestion. Do not change the handoff yourself.
   - Coordinator absorbs the finding, revises, sends back. Settlement usually takes 1–3 rounds. Then Hermes executes.
4. Do not send a handoff back for minor polish or preference. The goal is more eyes catching real issues, not ceremony that stops forward motion.
5. Avoid expanding scope unless needed for safe completion.
6. Return a short receipt with paths, IDs, and what changed.
7. Archive the handoff when complete.

## Evaluation signals

These patterns suggest the handoff should be sent back to Coordinator for revision:

- **Scope creep** — the handoff asks for more than the original discussion needed.
- **Redundancy** — this work was already done or is already covered by an existing surface.
- **Over-engineering** — the task builds infrastructure for something that could be done directly.
- **Expensive route** — the handoff sends work to Claude/Codex that Hermes could do.
- **Conservation risk** — the handoff adds ceremony or process when what Ted needs is a simple answer.
- **Curtailment disguised as efficiency** — the handoff suggests cutting something Ted actually needs.

## Not-change-for-the-sake-of-change rule

Do not send a handoff back just to revise it. Every revision must have a real reason:

- A genuine blocker or risk.
- A materially better path.
- A cost or time saving.
- A trip wire Coordinator did not see.

If the handoff is clean enough to execute, execute it. Revision-for-revision's-sake wastes the loop.

## Ted's role

Ted stays in the intent, judgment, and promotion seat. Ted does not have to manually convert every insight into file operations or routing instructions.

## Success-over-method rule

Ted should not have to prescribe the implementation path.

Coordinator's job is to translate Ted's intent into a clear success condition, not to over-specify how Hermes must achieve it.

A good handoff says:

- what success looks like;
- what must be preserved;
- what would count as failure or curtailment;
- what boundaries cannot be crossed;
- where the result should land, if known.

Hermes then uses its own skills, tools, and local judgment to choose the best route.

When Ted's language is approximate, treat it as valid intent. Ask clarifying questions about intent and success, not about low-level implementation mechanics unless implementation details are truly necessary for safety.

When reporting back, show what changed and what it means. Do not drag Ted into unnecessary implementation detail.

## Good uses

- "This should be saved somewhere."
- "Can you make this something for Lab?"
- "Look in a path Coordinator cannot read."
- "This sounds like a skill."
- "Anything from today worth saving?"
- "Can you verify if this is actually done?"

## Bad uses

Do not use this skill to:

- route everything outward by default;
- avoid answering a simple question in chat;
- create process artifacts just because a conversation was interesting;
- spend expensive Claude/Codex tokens when Hermes can do the work;
- bypass Ted's sign-off for Canon or production changes.

## Style rules

- Status first.
- No long proof frameworks unless Ted asks.
- For UI troubleshooting: ask what the screen shows, use the UI's words, give one action.
- For video/tool interpretation: ask Ted for a Gemini/YouTube summary when direct video access is limited.
- Prefer one clean handoff over scattered partial actions.

## Done criteria for a handoff

A good handoff answers:

- What should be done?
- Where should it land?
- What context matters?
- What should not be changed?
- How will Hermes know it is done?

## Output pattern

After Hermes returns:

```text
Status: done.
Landed: <path or ID>.
Handled by: Coordinator-Hermes / Hermes.
Next action: none / <one action>.
```
