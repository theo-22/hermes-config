---
name: topic-assembly
description: Given a topic under live discussion, go find its nodes in the concept map yourself (do the pointing Ted has been doing by hand), check whether the connected ideas flow into a coherent through-line, then harvest the missing connecting nodes — from the rest of the map and from Pieces (cross-session / other-app mentions) — and lay the topic down as a connected multidimensional structure with tails for re-entry. Invoke when a topic is deepening in conversation and would benefit from being assembled and connected, not just discussed. Do not use to invent a single node (concept-bridge-surfacing) or to enrich one already-placed node (graph-edge-finding) — this is the whole-topic composition of those.
category: database-integrated
write_mode: db
one_line_use: assemble a topic's nodes and connect them
fast_pick: "yes"
---

# Topic Assembly

Turn a live discussion topic into its assembled, connected, multidimensional node-neighborhood in the concept map — **the AI does the pointing.** This composes [concept-bridge-surfacing] (create a missing node), [graph-edge-finding] (find a node's edges), the Pieces ambient harvest, and the conversation-tail idea (leave a re-entry handle).

The origin (Ted, 2026-07-18): *"This works because I point at them. You could quickly become good at pointing at them… go find the nodes, are they connected such that the conversation makes sense — not all of it, but the connected ideas flow. Then you can follow them. They become tails. If you wanted you could go harvesting nodes all over, to Pieces to get the connecting nodes. Lay down a topic in multidimensions and connect them."*

## When to use
- A topic is deepening across several turns and its pieces are scattered across the map / other sessions.
- You'd otherwise wait for Ted to point at each node by screenshot — instead, point yourself.
- After a Pieces harvest surfaces a theme worth assembling.

## When not to use
- One missing node → `concept-bridge-surfacing`. One stranded node's edges → `graph-edge-finding`.
- The topic is settled and already well-connected — don't re-assemble for tidiness.

## Canonical workflow

1. **Name the topic and its facets.** One line for the topic; list its distinct angles. A topic is multidimensional — each facet is a search axis and, later, a dimension of the assembled structure.
2. **Find the nodes (the pointing).** Query `concept_bridges` for nodes matching the topic and each facet — keyword search plus judgment on the full node text. This is the step Ted has been doing manually; here the AI does it.
3. **Check the flow (coherence, not completeness).** Traverse the found nodes' existing edges. Do the *connected* ideas form a through-line the conversation can walk? **Not all nodes need to connect** — the test is whether the connected subset flows, and *where it breaks* (two nodes that clearly belong, no edge between them). Ted's exact standard: "not all of it, but the connected ideas flow."
4. **Harvest the connecting nodes — two sources.**
   - **The rest of the map:** nodes the topic touches that weren't in the first find.
   - **Pieces:** ask about the topic across sessions and other apps — the connecting ideas that live off-substrate (ChatGPT, browser, prior sessions). Pieces is a **lead-finder, not authority**: verify each lead against live files/DB before wiring it (see [pieces-ambient-lead-evaluation]).
5. **Lay it down in multidimensions and connect.** Wire the verified connections as **proposed** edges (candidate / dashed), grouped by facet/axis so the topic reads as a legible volume, not a line. Each edge names a real shared *mechanism* (not topic-similarity). Create a node only if a genuine concept is missing, following concept-bridge-surfacing discipline.
6. **Leave a tail.** The assembled neighborhood IS a re-entry handle — record it (a memory, a thread, or just the wired map region) so the topic can be dropped back into later instead of re-derived. The assembly's own output is a conversation tail.

## Evidence / success criteria
- The connected subset walks as a coherent through-line; breaks are named, not papered over.
- Each new edge names a specific shared mechanism; every Pieces lead was verified against a live surface before wiring.
- The topic is legible across ≥2 dimensions with clear pointers (node ids + surfaces on disk).
- A re-entry tail exists.

## Failure modes
- **Forcing total connectivity.** Ted's standard is the connected subset flowing, not every node linked. A topic legitimately has loose members; wiring them all to force a clean picture is dishonest (same family as the generic-hub and similarity-as-edge failures in [graph-edge-finding]).
- **Pieces-as-authority.** Ambient hits are leads. Wiring one without checking the live file invents structure. Most of a Pieces return is noise co-occurring with the query — filter to the 2–3 real signals.
- **Harvest sprawl.** Harvesting so wide the topic loses focus. Stay scoped to the named facets; a topic is a volume, not the whole map.
- **Bundled / generic-hub / similarity-as-edge.** Inherited from [graph-edge-finding] — apply its traverse-test and detectors.

## Runtime Notes

### Claude Code / Codex
- Nodes/edges: `concept_bridges` + `concept_bridge_relations` in `/Users/ted/Control/backend/system.db`. Create nodes via `POST http://localhost:5555/api/concept-bridges`; write edges direct as `promotion_status='candidate'`, honest `notes`, stamped `created_by`/`evidence_ref` (use a `pieces:` prefix when the edge came from an ambient harvest, for an auditable trail).
- Regenerate the map after writing: `python3 Operations/scripts/build_concept_graph_viz.py`; verify positions moved via `javascript_tool` on `GRAPH.nodes`.
- Pieces harvest: `mcp__pieces__ask_pieces_ltm` scoped to the topic across apps/sessions.

### At scale
`Operations/scripts/build_concept_bridge_graph.py` bulk-harvests edges (embed → nearest-neighbor → classify) across the whole map. Use it to seed; use this skill to assemble one topic with judgment and a Pieces pass the bulk script can't do.

### GPT bridge
No direct DB write — route the assembled proposal (nodes + edges + rationale) to `_AI_Inbox/` or the concept-bridge Action endpoint.

## Update-surfacing backstop
Names live paths (`system.db`, `build_concept_graph_viz.py`, `build_concept_bridge_graph.py`, the concept-bridge API) and the `relation_type` CHECK vocabulary. If any drift, fix here or leave a review note.
