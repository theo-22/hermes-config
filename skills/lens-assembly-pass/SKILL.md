---
name: lens-assembly-pass
description: The full working loop for turning a live topic into wired, durable structure — assemble the topic's nodes, optionally cold-probe and refine a load-bearing or delegation-facing inference surface, check what the spine says, then persist the result to Brain, memory, and a touch. Use when a topic has deepened enough to be worth laying down or when understanding would otherwise evaporate. Do not use to mint one node (concept-bridge-surfacing) or connect one stranded node (graph-edge-finding).
metadata:
  category: database-integrated
  write_mode: db
  one_line_use: assemble a topic, gauge the spine, persist it
  fast_pick: "yes"
---

# Lens Assembly Pass

**The engine, not a one-off.** Core flow: **assemble → fortify → persist.** When the cold-probe trigger applies: **assemble → probe → refine → fortify → persist.** When the pass surfaced material Map Curator hasn't seen yet: **… → persist → harvest.**

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

## Optional Stage 2 — PROBE → REFINE

Run [cold-probe-refine] (`Skills/cold-probe-refine/SKILL.md`) only when the assembled surface is load-bearing, newly refined, meant for delegation to a cheap model, or explicitly being measured for reconstructability.

The cheap/fast cold reader goes first. A stronger independent reader reviews second, compares semantic recovery rather than exact wording, and classifies the failure before any change. The reviewer diagnoses; it does not automatically own concept meaning or edit the graph.

Skip this stage for trivial assemblies and assemblies with current comparable proof. A skipped probe is explicit (`probe: not triggered`), not an unreported omission.

**Output:** the Lab result pointer plus `pass`, `projection_failure`, `instruction_or_traversal_failure`, `reader_limitation`, `infrastructure_failure`, or `inconclusive`. If an authorized refinement lands, preserve a same-question rerun; otherwise record why no rerun occurred.

## Stage 3 — FORTIFY

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

## Stage 4 — PERSIST

Run [persist] (`Skills/persist/SKILL.md`) — Brain, memory file + `MEMORY.md` pointer, and a buoyancy touch.

**This stage is the andon: it does not yield.** It is the step that gets dropped under end-of-session token pressure, precisely because the understanding still feels present and the map already shows the artifact. Nodes and edges are the artifact; persist is the record that the pass happened and what it decided.

**If budget is short, persist first and cut depth elsewhere.** An assembled-but-unpersisted topic is worse than an unassembled one — it looks done in the map while the reasoning that produced it is gone.

## Optional Stage 5 — HARVEST

**Added 2026-08-15**, from `_AI_Inbox/2026-08-15_chatgpt_proposal_session_end_curator_harvest_pipeline.md` (Ted + Map Curator). Run this only when the pass surfaced graph-relevant material Map Curator has not already been told about — a durable Concept worth a node, a State reading, a v14/durable-intent implication, or a plausible road between nodes you noticed but didn't verify. Most passes end at stage 4 and owe nothing here; skip explicitly (`harvest: not triggered`) rather than manufacturing a package.

This is deliberately **not** a widening of persist and **not** a Scribe task. Persist (stage 4) already closed the idea on Brain/memory/touch — harvest records a separate, distinct obligation: that the graph itself may need to change because of it. It does not judge State-vs-Concept-vs-v14 with authority (that stays Map Curator's call) and it does not write the graph — it hands Map Curator a well-shaped lead.

**Mechanism — reuses the existing Curator queue, nothing new:**
1. Shape each candidate per `Concept_Graph/Curator_Harvest_Candidate_Schema.md` — one sentence claim, source, candidate_kind, freshness, nodes already consulted, possible roads (leads only), the persist pointer from stage 4, and a meaning-fork question if one genuinely remains.
2. Aggregate the **whole session's** candidates into **one** package — never one work item per finding.
3. File it as **one** `work_items` row: `type='report'`, `owner='map_curator'`, `source_surface` pointing at a `Concept_Graph/CC_To_Map_Curator_Curator_Harvest_<slug>.md` content file holding the full package, `notes` holding the compact summary. Full field-by-field detail and the exact API call are in the schema file.
4. Map Curator's own session start already surfaces `work_items.owner=map_curator` — no further delivery step exists or is needed.

**Output:** either `harvest: not triggered` (the normal case), or the `work_items` id filed plus a one-line count of what it carries (candidates by kind, nodes touched, roads, forks).

---

## Evidence / success criteria

- The connected subset walks as a through-line; breaks are named, not papered over.
- Every edge names a real shared mechanism; every Pieces lead was verified against a live surface.
- Probe state is explicit: `not triggered`, or a cold-first result and stronger-review verdict with a durable Lab pointer.
- A spine verdict is stated explicitly — including "realized, nothing owed."
- All three persist surfaces written and named. **A pass is not complete without stage 4.**
- Harvest state is explicit: `not triggered`, or a filed `work_items` id with the package it carries.

## Failure modes

- **Stopping after stage 1.** The most likely failure: the map looks wired, the session ends, nothing durable was written. This is the whole reason the engine exists as one skill instead of three loose ones.
- **Mandatory probe ceremony.** Running a model test on every trivial assembly obscures the cases where reconstructability evidence matters.
- **Strong model goes first.** Pre-teaching with the evaluator defeats the cold reader's value as a sensor of the environment.
- **Manufacturing a spine edit.** Most passes are "realized." Inventing a gap to justify the stage corrupts the gauge.
- **Confusing the two gauges.** Running `spine_gauge.py` and calling stage 3 done. It answers a different question.
- **Assembling a fog.** If the pass won't reduce to one claim at persist time, it wasn't ready. Stop rather than persist noise.
- **Spraying the Curator queue.** One `work_items` row per candidate instead of one aggregated package per session — exactly what stage 5 exists to prevent.
- **Harvest doing Map Curator's job.** Asserting a candidate as settled, or writing the graph directly, instead of handing over a lead. Stage 5 never calls a `map_*` write tool.
- Inherited from [topic-assembly]: forcing total connectivity, Pieces-as-authority, harvest sprawl, generic-hub and similarity-as-edge.

## Runtime Notes

### Claude Code
Stages 1, optional 2, and 4 are their own skills — invoke them, don't inline them. Stage 3 needs no tooling beyond reading the relevant chapter and `System_14_Plan.md`. Stage 5 is a direct `POST /api/work-items` call (or `system_db.add_work_item(...)`) plus one content file under `Concept_Graph/` — no new tool, see the schema file for the exact call shape.
Map regeneration and DB paths are in [topic-assembly]'s runtime notes; the persist surfaces are in [persist]'s.

### GPT bridge
No direct DB write. Route the assembled proposal, the spine verdict, the three persist payloads, and (if triggered) the harvest package to `_AI_Inbox/` for an actor with write access.

## Update-surfacing backstop
Depends on [topic-assembly], [cold-probe-refine], [persist], `Operations/scripts/spine_gauge.py`, and `Concept_Graph/Curator_Harvest_Candidate_Schema.md`. If any is renamed, moved, or retired, fix the reference here.
