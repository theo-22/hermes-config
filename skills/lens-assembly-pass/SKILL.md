---
name: lens-assembly-pass
description: The full working loop for turning a live topic into wired, durable structure — assemble the topic's nodes in the concept map, check what the spine says about it, then persist the result to Brain, memory, and a touch. Use when a topic has deepened enough in conversation to be worth laying down rather than just discussed, or when a session produced real understanding that will otherwise evaporate. This is the repeatable engine; use it instead of re-deriving the sequence by hand each time. Do not use to mint one node (concept-bridge-surfacing) or connect one stranded node (graph-edge-finding).
category: database-integrated
write_mode: db
one_line_use: assemble a topic, gauge the spine, persist it
fast_pick: "yes"
---

# Lens Assembly Pass

**The engine, not a one-off.** Three stages, run in order: **assemble → fortify → persist.**

The origin (Ted, 2026-07-24): the map stopped being a thing described and became a thing *operated* — walk a node together, correct to fine definition, and encode the correction as structure so the next reader inherits the subtlety without Ted re-saying it. This skill is that loop made repeatable.

Named for the reclaimed sense of **lens** (node #173): the generative sibling of the mega-tail — it produces new structure, not just re-entry.

## When to use
- A topic has deepened across several turns and is worth laying down.
- A session produced real understanding not yet on disk.
- Ted points at a node and the conversation roams — the roam is the raw material.

## When not to use
- One missing node → `concept-bridge-surfacing`. One stranded node → `graph-edge-finding`.
- The topic is settled and already well-connected. Don't re-assemble for tidiness.
- Nothing was actually decided. An assembly pass over a fog produces a legible-looking fog.

---

## Stage 1 — ASSEMBLE

Run [topic-assembly] (`Skills/topic-assembly/SKILL.md`). It already composes the pieces: finding the nodes (the AI does the pointing), checking whether the connected subset flows, harvesting missing connectors from the map and from Pieces, and wiring honest candidate edges.

**Do not re-derive its steps here.** It is the authority for this stage; if it drifts, fix it there.

Two disciplines from it that carry the most weight:
- **Coherence, not completeness.** The test is whether the *connected* subset walks, and *where it breaks* — not whether everything links. Forcing total connectivity is dishonest.
- **Pieces is a lead-finder, never authority.** Verify every ambient hit against a live surface before wiring it.

## Stage 2 — FORTIFY

**Ask what the spine says about what you just assembled.** Three verdicts (Ted's keystone, 2026-07-20: *"the structure is the projection of the spine"*):

| Verdict | Meaning |
|---|---|
| **realized** | The spine names it and the system does it. Nothing owed. |
| **gap** | The spine names it, nothing is built. |
| **drift** | It is built and lived, and the spine is silent. |

**Output: a named verdict plus the one edit that would close it. Not a chapter rewrite.**

**This is the semantic gauge, distinct from the mechanical one.** `Operations/scripts/spine_gauge.py` already exists and is live — it compares git commit dates per v14 chapter to catch a projection that went stale relative to its definition. That is *time* drift at *chapter* grain. This stage is *meaning* drift at *topic* grain: does the spine name this idea at all. Run the script when you want the mechanical read; do this when you want the semantic one. They do not substitute for each other.

**Worked example (2026-07-25):** the second-brain practice was lived throughout the system and named **zero times** in `System_14_Plan.md` — textbook **drift**. The closing edit was one §0 Purpose section, not a rewrite. That pass is what this stage generalizes.

Most passes end at **realized** and owe nothing. Say so and move on — manufacturing an edit to look productive is the failure mode here.

## Stage 3 — PERSIST

Run [persist] (`Skills/persist/SKILL.md`) — Brain, memory file + `MEMORY.md` pointer, and a buoyancy touch.

**This stage is the andon: it does not yield.** It is the step that gets dropped under end-of-session token pressure, precisely because the understanding still feels present and the map already shows the artifact. Nodes and edges are the artifact; persist is the record that the pass happened and what it decided.

**If budget is short, persist first and cut depth elsewhere.** An assembled-but-unpersisted topic is worse than an unassembled one — it looks done in the map while the reasoning that produced it is gone.

---

## Evidence / success criteria

- The connected subset walks as a through-line; breaks are named, not papered over.
- Every edge names a real shared mechanism; every Pieces lead was verified against a live surface.
- A spine verdict is stated explicitly — including "realized, nothing owed."
- All three persist surfaces written and named. **A pass is not complete without stage 3.**

## Failure modes

- **Stopping after stage 1.** The most likely failure: the map looks wired, the session ends, nothing durable was written. This is the whole reason the engine exists as one skill instead of three loose ones.
- **Manufacturing a spine edit.** Most passes are "realized." Inventing a gap to justify the stage corrupts the gauge.
- **Confusing the two gauges.** Running `spine_gauge.py` and calling stage 2 done. It answers a different question.
- **Assembling a fog.** If the pass won't reduce to one claim at persist time, it wasn't ready. Stop rather than persist noise.
- Inherited from [topic-assembly]: forcing total connectivity, Pieces-as-authority, harvest sprawl, generic-hub and similarity-as-edge.

## Runtime Notes

### Claude Code
Stages 1 and 3 are their own skills — invoke them, don't inline them. Stage 2 needs no tooling beyond reading the relevant chapter and `System_14_Plan.md`.
Map regeneration and DB paths are in [topic-assembly]'s runtime notes; the persist surfaces are in [persist]'s.

### GPT bridge
No direct DB write. Route the assembled proposal, the spine verdict, and the three persist payloads to `_AI_Inbox/` for an actor with write access.

## Update-surfacing backstop
Depends on [topic-assembly], [persist], and `Operations/scripts/spine_gauge.py`. If any is renamed, moved, or retired, fix the reference here.
