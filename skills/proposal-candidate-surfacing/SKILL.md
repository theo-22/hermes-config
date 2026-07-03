---
name: proposal-candidate-surfacing
description: Recognize when a discussion is becoming proposal-shaped, then help shape the candidate through conversation until it is ready for `/proposal-packet` to write. Use when the work is substantial enough that building without alignment would create rework. Do NOT use when the work is bounded and clear — just build it. Do not use when Ted already wants the packet written, when the task is routine note capture, or when implementation readiness is already settled.
category: judgment-only
write_mode: none
one_line_use: surface and shape the proposal candidate (only for substantial work)
fast_pick: "yes"
---

# Proposal Candidate Surfacing

**When to use:** The work is substantial and the direction isn't fully clear yet. Building without alignment would create rework.

**When NOT to use:** The work is bounded and clear. Ted described it, you understand it, and the path is obvious. Just build it. Don't force proposal-candidate surfacing on work that doesn't need it.

This is the core distinction: **bounded clear work doesn't need proposal-candidate surfacing.** It needs implementation. Save the surfacing for when the idea is still forming, the scope is ambiguous, or getting it wrong would mean significant rework.

---

## Workflow

### 1. Detect the threshold

Look for one or more of these:
- Observation and recommendation are starting to mix
- The enough-for-use version and growth boundary need to be made explicit
- A durable packet would help another AI or Ted evaluate the idea cleanly
- The discussion is drifting toward action without a compact proposal shape

If none of these is true — if the work is bounded and clear — **don't fire this skill.** Just build what was asked.

### 2. Shape the candidate

When the threshold is crossed, help bring the proposal into focus through conversation:

- **What the proposal is** — one sentence naming the concrete change, recommendation, or handoff
- **What's already clear** — observations, evidence, named scope, owner, destination
- **What's still fuzzy** — open questions, ambiguous boundaries, missing authority/owner/destination

Carry forward partial answers. If Ted answers only some items, answers out of order, revises as he reads, or skips part of a long question list, preserve what is clear and name only the remaining fuzzy items. Don't restart the whole list. Don't treat missing answers as refusal or failure.

Ask one or two targeted questions to push fuzzy items toward clear. Not a form — conversationally.

When fuzzy items are addressed enough that another AI could write the packet without reconstructing the conversation, name the readiness:
- **Ready for `/proposal-packet`** — concrete proposal, enough-for-use version, boundaries, open questions, suggested destination all visible
- **Not yet ready** — name what's still missing in one line

### 3. Hard boundary — discovery only

This skill never writes the packet, never saves anything, never routes to an inbox, never implies approval. Even when the candidate is fully shaped, the skill stops at the readiness call. Packet writing belongs to `/proposal-packet`, invoked by Ted or by clear authorization.

---

## Output Shapes

**Bounded clear work (skill doesn't fire):**
> Just build it. No proposal surfacing needed.

**Not yet a candidate:**
> `Not a proposal candidate yet.` [one-line reason]

**Candidate forming, still fuzzy:**
> `Proposal-candidate moment.` [one-sentence likely proposal] What's clear: [...]. Still fuzzy: [...]. [One or two targeted questions.] Not yet ready for `/proposal-packet`.

**Candidate fully shaped:**
> `Proposal-candidate moment.` [one-sentence proposal]. Enough-for-use version: [...]. Boundaries: [...]. Open questions: [...]. Ready for `/proposal-packet` if Ted wants it written.

---

## Never Assume

- Surfacing or shaping does not mean approval
- Readiness does not mean "go write the packet" — wait for Ted's invocation
- Agreement during surfacing means "include this in the plan," not "execute"
- Most ideas don't need proposal treatment — only the ones where building blind would create rework

## Watch Status

- **Bureaucratic overfire** — turning ordinary bounded work into proposal paperwork. If the work is clear, build it. Don't force surfacing.
- **Premature stop** — recognizing the threshold but stopping before the candidate is shaped enough
- **Partial-answer loss** — Ted answers in pieces; carry forward what's answered, don't restart the list
