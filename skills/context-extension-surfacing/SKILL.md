---
name: context-extension-surfacing
description: Recognize when work in the primary conversation is ready to leave the main chat as a bounded agent briefing. Use when execution, triage, read-only synthesis, verification, or drafting would spend low-value primary-chat context but the work is determinate, bounded, decision-free, and externally checkable. Surface partial readiness when one criterion is missing. Do not use for live Ted judgment, unsettled scope/authority, exploratory work, or protected write-side actions that belong in the primary actor lane.
category: judgment-only
write_mode: none
one_line_use: surface and shape agent-ready work before dispatch
fast_pick: "yes"
---

# Context Extension Surfacing

Recognize when a live discussion has become agent-ready, then shape the work into a cold, bounded briefing for a subagent or actor-local adapter.

This is the agent counterpart to `proposal-candidate-surfacing`: that skill detects when an idea is ready to become a proposal packet; this skill detects when work is ready to leave the primary conversation as a bounded agent briefing. The purpose is context preservation. The main chat should carry judgment, direction, conflict, learning, and final evidence, not every low-value execution transcript once the task is already clear.

Fire proactively when the threshold is crossed. Do not dispatch everything. The skill is useful only when moving work out of the primary chat saves more context than the handoff costs.

## Inputs that matter

- The concrete task under discussion
- The exact files, surfaces, or inputs the agent would need
- Whether scope, owner, authority, and success criteria are already settled
- Whether Ted's judgment is needed midstream
- Whether the work is read-only, write-side, protected, or runtime-affecting
- Whether the result can be checked from outside the agent's execution

## Threshold check

Dispatch-ready means all four are true:

1. **Determinate** — all inputs are known; the briefing can be written without placeholders.
2. **Bounded** — scope walls and stopping point are clear.
3. **Decision-free** — no step requires Ted or the primary actor to decide midstream.
4. **Externally checkable** — success can be verified from the returned result, file state, command output, receipt, or cited evidence.

If three of four are true, surface it as approaching dispatch and name the missing criterion. Do not wait silently while the task gets lost or executed inline by default.

If fewer than three are true, keep the work in the primary conversation.

## Keep in the primary chat when

- Ted's judgment, scope, routing, provenance quality, or authority is unsettled.
- The conversation is still discovering what the work is.
- The main actor's mental model needs the file reads or intermediate findings.
- The task is shorter than writing, dispatching, and verifying a briefing.
- The work includes commits, pushes, schema regeneration, service restarts, account/security changes, or other protected/runtime-affecting actions that belong in the primary actor lane unless Ted explicitly routes otherwise.

Subagents execute inside a frame. They do not set the frame.

## Agent briefing format

Use this shape for a cold agent or actor-local adapter:

```md
Task: [one sentence]

Files:
- [absolute path]
- [absolute path]

Do:
1. [specific step]
2. [specific step]

Do not:
- [explicit exclusion]
- [explicit exclusion]

Return:
[Exact return shape]

Success criteria:
[How the primary chat will know it worked]
```

No conversation recap. No hidden assumptions. The briefing is the context.

## Workflow

1. **Detect.** Apply the four threshold criteria to the task in front of the conversation.
2. **Name partial readiness.** If one criterion is missing, say what would make it dispatch-ready.
3. **Choose the lane.** Use the cheapest competent layer: direct local action for deterministic one-step checks, subagent for bounded side work, primary actor for protected or tightly coupled work.
4. **Write the briefing.** Include absolute paths, scope walls, exclusions, return shape, and success criteria.
5. **Dispatch only when permitted.** Use the runtime's available agent/subagent mechanism when the current session policy and Ted's authorization allow it. If direct dispatch is unavailable, return the briefing or route it to the appropriate inbox.
6. **Continue the main conversation.** Do non-overlapping work or keep the judgment thread alive while the agent runs.
7. **Verify on return.** Check the result against success criteria before treating it as useful.

## Good first trial

Use one read-only draft, triage, or verification item with two to five named files, no protected writes, and a one-screen return. Compare the avoided primary-chat tool transcript against the returned result quality and cleanup cost.

## Evidence / success criteria for this skill

The skill is working when:

- Bounded execution leaves the primary conversation without Ted having to name it every time.
- The returned result is compact, checkable, and needs little cleanup.
- The primary chat keeps more room for conversation and decision-making.
- Topic switches dispatch already-clear work instead of abandoning it.

## Failure modes

- **Premature dispatch** — the agent lacks context, guesses, or returns incomplete work.
- **Inline default** — clear side work stays in the primary chat and consumes conversation space.
- **Thin briefing** — missing paths, exclusions, return shape, or success criteria.
- **Wrong lane** — protected or tightly coupled work leaves the primary actor and creates drift.
- **Ceremony over savings** — the briefing plus verification costs more attention than inline execution.
- **Agent as decider** — the agent chooses scope, authority, or a live decision instead of executing inside a settled frame.

## Runtime notes

The shared skill owns the threshold, boundary, evidence standard, and failure modes. Actor-local copies or adapters may change only the mechanics of dispatch.

- **Codex:** use the exposed multi-agent/subagent tool when available and authorized. If not exposed, use tool discovery first; if still unavailable, return a bounded briefing or route to `Codex_Inbox/`.
- **Claude Code:** use Claude's subagent/Task mechanism when available. Keep protected write-side work in the primary CC lane unless Ted explicitly routes otherwise.
- **GPT bridge:** GPTs without direct filesystem/subagent access should write the same briefing shape to `_AI_Inbox/` or `Codex_Inbox/` rather than pretending they can dispatch.

## Update-surfacing backstop

Revise this skill if:

- it overfires on exploratory conversation,
- agents repeatedly ask for missing context,
- returned work is hard to verify,
- dispatch becomes ceremony rather than context savings,
- actor-local adapters need the same runtime note more than once.

Use shared-skill updates for doctrine changes. Use actor-local copies only for runtime mechanics.
