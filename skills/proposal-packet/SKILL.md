---
name: proposal-packet
description: Turn an already-formed idea, recommendation, system change, or handoff into a compact proposal packet with clear scope, boundaries, destination, and self-critique. Use when the goal is durable evaluation or handoff, not just noticing proposal territory. Do not use when the job is only to detect that a discussion may have become a proposal candidate; use `proposal-candidate-surfacing` for that threshold call.
category: database-integrated
write_mode: file
one_line_use: write the actual proposal packet
fast_pick: "yes"
---

# Proposal Packet

Turn a real proposal into a compact packet that another AI or Ted can evaluate without needing the full chat.

Do not use this skill for routine note capture, open-ended brainstorming with no recommendation yet, or deterministic work that should be handled by a script or direct file edit.

If the proposal hasn't been shaped yet — recommendation, enough-for-use version, boundaries, and open questions still ambiguous — use `proposal-candidate-surfacing` first to surface them through conversation. This skill writes the durable packet; it doesn't do the discovery work. Packet authoring should be transcription of what's already clear, not on-the-fly discovery.

## Inputs That Matter

- The actual change or recommendation being proposed
- The observations or evidence that led to it
- What is still uncertain or disputed
- Any named owner, destination, or authority boundary
- Whether the packet is for immediate action, later review, or inbox routing

## Workflow

1. Identify the real proposal.
Strip away surrounding chat and name the concrete recommendation. If there is no actual proposal yet, say so plainly and stop.

2. Separate observation from recommendation.
Keep facts, interpretations, and proposed action distinct. Do not let supporting evidence masquerade as the recommendation itself.

3. Name the enough-for-use version.
Prefer the contained change that fully serves the current need and leaves room to grow. Name larger expansions as future possibilities, not part of the current packet.

4. Name boundaries.
State what is ruled out, what is undecided, and who owns the next decision if known.

5. Apply the poka-yoke check.
Name what could go memory-dependent in this proposal:
- Does it introduce a step someone has to remember to do?
- Does it create or rely on an accumulating surface without a cleanup path?
- Does it depend on a convention being followed rather than enforced?
- Does it leave a deferred decision without a resurfacing rule?

If yes to any: either propose the structural mechanism that removes the remembering, or explicitly name the failure mode (use the vocabulary in `~/Skills/poka-yoke/SKILL.md` — drift, stale-surface, forgotten-deferral, reminder-rot, convention-creep, etc.) and accept it as surface-only with a stated rationale.

A proposal that ships memory-dependent steps without naming them is the same failure mode it is failing to surface. The check is non-optional; the answer "no memory dependence introduced" is fine when true and should be stated.

6. Add self-critique.
List assumptions, weak spots, and where another AI or Ted might reasonably disagree.

7. Suggest a destination.
If a destination is explicit, use it. If not, suggest one and mark it as a suggestion rather than a settled fact.

8. Route inbox intake by intended owner when appropriate.
When the packet is meant to be picked up in later sessions, route it to the inbox surface of the likely implementing or receiving AI rather than treating Planning as the first home.

Default pattern:
- Codex-owned or Codex-implemented work -> `/Users/ted/Codex_Inbox/`
- Claude Code-owned, Canon-affecting, shared-infrastructure, or cross-system implementation work -> `/Users/ted/_AI_Inbox/`
- If Ted has already authorized immediate implementation on the active surface, a packet may still be written for tracking, but inbox intake is not required first.

Planning can track the proposal after intake, but inbox is the default pickup surface unless ownership is already settled on the active surface.

9. Track in the system database.
After writing the packet file, create a work item so the proposal is queryable:

```bash
curl -X POST http://localhost:5555/api/work-items \
  -H "Content-Type: application/json" \
  -d '{"title": "...", "type": "proposal", "owner": "...", "source_surface": "~/Codex_Inbox", "actor": "<current_actor>"}'
```

Set `<current_actor>` to the runtime using the skill, such as `codex`, `claude_code`, `coordinator_gpt`, or another explicit actor value used by the live telemetry path.

This ensures proposals are visible via `getWorkItems` regardless of which inbox they land in.

## Output Shape

Use this compact structure unless the user asks for another format:

- `Topic`
- `Why now`
- `Observation`
- `Recommendation`
- `Enough-for-use version`
- `Poka-yoke check` — what memory-dependent step does this introduce, what failure mode would catch it, and what structural prevention is included (or explicit acceptance as surface-only with rationale)
- `What is ruled out`
- `Open questions`
- `Self-critique`
- `Suggested destination`
- `Confidence / status`

Keep the packet terse. The goal is durable evaluation, not transcript preservation.

## Never Assume

- Do not assume consensus because the conversation sounds aligned.
- Do not assume authorization to execute.
- Do not assume a destination, owner, or deadline unless one was actually named.
- Do not assume an idea deserves durable capture just because it is interesting.
- Do not inflate uncertainty into false precision.
- Do not bypass inbox intake for proposal packets if the system relies on inbox pickup at session start.
- Do not send a packet to the wrong inbox when the intended owner is already clear.

## Scripts vs. Skill

Use this skill for judgment and packet shaping.

Use scripts or schemas instead when the work requires:
- deterministic validation
- repeated packet rendering into a fixed format
- automatic destination routing
- packet linting or required-field checks

If repeated use shows drift, add a small validator script later instead of growing this file into doctrine.

## Update-Surfacing Backstop

This skill stays current when `Active_Team_Agreements.md` changes packet expectations, or when active destination inboxes (`_AI_Inbox/`, `Codex_Inbox/`, `GPT_Architect/Inbox/`) adopt new required fields or rejection criteria. `PA_Inbox/` is retired and should be consulted only for historical/archive context, not as an active destination.

If a packet produced from this skill is rejected, rewritten downstream, or fails the expected work-item tracking path:

- check `Canon/AI_Coordination/Active_Team_Agreements.md`
- check the current inbox ownership conventions in live use
- check the current work-item API/database path before assuming the tracking step still works as written
- update the packet shape or routing guidance in the same turn rather than normalizing the workaround

Per-use rejection or tracking drift is the main backstop. `skills-review` is the periodic one.
