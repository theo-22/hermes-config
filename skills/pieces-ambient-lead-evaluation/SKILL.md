---
name: pieces-ambient-lead-evaluation
description: Evaluate and use Pieces or another ambient-memory tool as a lead finder for Codex, Claude, Hermes, Coordinator, or another runtime. Use when Ted asks how Pieces can serve the system, how it can serve Codex, what useful information is in Pieces, whether Pieces is worth keeping, or when a Pieces/Pieces-MCP lead should be turned into verified local work. Treat Pieces as overview and perspective, not authority: read nearby sessions and suggestions, classify common threads, verify actionable claims against live owner files, and score usefulness using the Pieces trial dimensions.
category: judgment-only
write_mode: none
one_line_use: turn ambient memory into verified system leads
fast_pick: "yes"
---

# Pieces Ambient Lead Evaluation

Evaluate ambient memory as a system aid, then convert only verified leads into bounded work.

Pieces is useful when the question is not "what does the owner file say?" but "what happened around this work across chats, browsers, apps, and adjacent sessions that Codex or another actor may not otherwise see?"

## When To Use

Use this skill when:

- Ted asks to evaluate Pieces, Pieces MCP, or an ambient-memory tool.
- Ted asks what Pieces can do for Codex or the system.
- Ted asks for overview, perspective, common threads, or nearby-session context.
- A Pieces lead packet, hint, suggested chat, or workstream summary may contain Codex-routable work.
- Codex needs off-filesystem context before deciding what live owner surface to verify.

## When Not To Use

Do not use this skill when:

- The owner file or live runtime already answers the question directly.
- The task is clinical/PHI, credentials, account/security, spend, or another protected surface unless Ted explicitly routes that exact action.
- Ted asks for GPT Builder craft; route Builder wording, GPT behavior tuning, Knowledge shape, and conversation-starter work to GA unless the work is local packaging or proof.
- Pieces would become the only proof source for implementation state, authorization, queue status, privacy posture, or payment decisions.

## Core Boundary

Pieces produces leads. It does not produce authority.

The authority sequence is:

1. Ted's current intent.
2. Live owner surface: project room, inbox item, planning file, CHANGES_LOG, dashboard/API, runtime, or protected-surface rule.
3. Pieces as ambient context around that surface.
4. Verified local action or explicit blocker.

If Pieces and the owner surface disagree, the owner surface wins unless live proof overturns it.

## Canonical Workflow

1. Name the evaluation question.
   Keep it narrow enough to test. Examples: "What nearby-session context helps Codex act on this Pieces lead?" or "What common Codex work threads did Pieces capture around this session?"

2. Read the owner surface first when one is named.
   Examples: `Planning/Pieces_Trial_Evaluation_Log.md`, `Codex_Inbox/pieces_leads_*.md`, a Project Room `NEXT_ACTION.md`, or a specific thread.

3. Query Pieces for ambient context.
   Prefer questions that ask for surrounding sessions, common threads, suggestions, hints, or off-filesystem activity. Do not ask Pieces to decide authority.

4. Read suggestion affordances.
   Check suggested chats, follow-up hints, related questions, "next steps", and nearby conversation titles. These often reveal what Pieces thinks is the next useful angle.

5. Classify each lead.
   Use these labels:
   - `Codex-routable`: local file/script/API verification or bounded implementation.
   - `CC/authority`: needs Claude Code, Canon authority, broad system judgment, or another actor's protected lane.
   - `GA/GPT-craft`: Builder instructions, GPT wording, Knowledge layout, or ChatGPT UX.
   - `protected`: credentials, PHI, spend, account/security, or another actor's persistent memory.
   - `background`: useful context, no action.
   - `false positive`: contradicted by live owner state.

6. Verify before acting.
   For every actionable lead, check live files, DB/API output, runtime behavior, or the named owner surface. Pieces alone is not proof.

7. Execute only the first bounded Codex-routable item unless Ted widened scope.
   If no Codex-routable item exists, return the first real blocker or the best-routed next owner.

8. Score the Pieces contribution.
   Use the trial dimensions:
   - `uniqueness`: what did Pieces surface that owner files would not?
   - `accuracy`: did it match live proof, overstate, or go stale?
   - `cost/noise`: how much latency, duplication, or filtering did it require?
   - `boundary risk`: did it touch protected or privacy-sensitive surfaces?
   - `catch`: did it reveal a useful thing the runtime was likely to miss?

9. Record only when the evaluation adds a real receipt.
   If the pass materially informs the Pieces trial, append a short dated receipt to `Planning/Pieces_Trial_Evaluation_Log.md` or the current owner surface. Do not create a new parallel evaluation log.

## Output Shape

Use this compact shape:

- `Question tested`
- `Pieces view`
- `Suggestion layer`
- `Lead classification`
- `Live verification`
- `Codex action or blocker`
- `Pieces score`
- `Where recorded`

Keep the answer behavioral: what Pieces helped the system do, what Codex verified, and what changed.

## Evidence Standard

Useful evidence includes:

- a specific Pieces event, hint, suggestion, conversation, or workstream summary;
- a live owner file or API/runtime check that confirms or rejects the lead;
- a bounded action taken by Codex;
- a clear non-action result such as "background only" or "routed to GA".

Weak evidence includes:

- Pieces saying a thing is done without owner-surface proof;
- broad summaries with no timestamp or route;
- privacy/config claims about Pieces that were not checked in the live app or actual settings;
- repeated generic matches that do not change the next action.

## Failure Modes

- Treating Pieces as truth instead of reconnaissance.
- Producing a report when a bounded Codex action is available.
- Asking Ted to route work that the live files already route.
- Reading only the main Pieces answer and skipping suggestions/hints.
- Letting broad ambient context sprawl into unrelated inbox or protected-surface work.
- Recording another evaluation artifact instead of appending to the existing trial log.
- Repeating the same "Pieces is useful as a lead finder" conclusion without a new receipt.

## Runtime Notes

### Codex

Use Pieces MCP when available:

- `search_memory` for ranked surrounding-session evidence.
- `ask_pieces_ltm` for a direct ambient-memory question.
- `hints_vector_search` or `hints_full_text_search`, then `hints_batch_snapshot`, for the suggestion layer.

Then verify with local reads, scripts, APIs, or runtime probes. Codex work is the conversion step: classify, verify, execute bounded local work, and record the outcome when needed.

### Claude Code

Use local Pieces scripts or MCP if available. Preserve the same authority boundary: Pieces leads are checked against live files, hooks, DB/API state, or UI proof before acting.

### GPTs / Coordinator

Use any available read-only Pieces action only as a context lead finder. Route actionable claims to the right owner surface instead of asserting live state.

## Existing Evaluation Surfaces

Read these before creating new evaluation structure:

- `Planning/Pieces_Trial_Evaluation_Log.md` - main receipt log and scoring dimensions.
- `_shared/Pieces_Integration_Findings.md` - technical integration findings and current tool limits.
- `Codex_Inbox/pieces_leads_*.md` - Codex-specific lead packets when present.
- `Coordinator/Working/*Pieces_Evaluation*` - Coordinator-specific read-only posture when relevant.

## Update-Surfacing Backstop

If Pieces MCP tool names change, the trial log moves, or a new authoritative Pieces evaluation surface replaces the current log, surface that mismatch and patch this skill instead of silently using stale paths.
