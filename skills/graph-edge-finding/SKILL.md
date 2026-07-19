---
name: graph-edge-finding
description: Given a thin or stranded node in a concept/knowledge graph, find its real missing edges to other nodes — the connections that are honest (a true instance/mechanism/dependency/tension), not merely same-topic. Use when a graph has orphan or rim nodes, when zooming into a region to enrich its links, or when a node "feels" disconnected from things it should touch. Do not use to invent nodes (use concept-bridge-surfacing) or to force similar-looking nodes together.
category: database-integrated
write_mode: db
one_line_use: connect a stranded node
fast_pick: "yes"
---

# Graph Edge-Finding

Find where a lightly-connected node *actually* connects — at any zoom level of Ted's graphs (concept bridges now; Substrate spine, AI-history lineage, role-access maps later). Sibling to [concept-bridge-surfacing]: that skill creates **nodes** (local term → standard concept); this one creates **edges** between nodes that already exist.

## When to use
- A graph view has orphan (degree-0) or rim (degree 1–2) nodes.
- Zooming into a region and enriching the links inside it.
- A node reads as disconnected from concepts it clearly touches.

## When not to use
- The node doesn't exist yet → `concept-bridge-surfacing`.
- You only have topic-similarity ("both about learning") → that is **not** an edge; stop.
- You'd be forcing two near-duplicate rim nodes together to tidy the picture → tidiness is not a relationship.

## Canonical workflow

1. **Read the full node text.** Not the truncated label — the whole thing. A concept's edges live in its details.
2. **Break it into facets.** One concept touches several things. ("ADR sidecar" = documenting decisions + preventing rework + a durable rationale trail + sits-next-to-a-schema.) Each facet is a *candidate* edge to a *different* node.
3. **For each facet, find the node that shares that exact mechanism** — not the same subject, the same *move*. Pull that node's full text and confirm the mechanism genuinely matches.
4. **Name the relation type precisely** from the live vocabulary (see Runtime Notes). Directed types matter: `depends_on`, `enables`, `motivates`, `evolved_from`, `sub_shape` (A is an instance of B), `extends`, `deepens`; axis types `same_dimension`, `meaning_family`; and the high-value **`anti_pattern`** (genuine tension/contradiction).
5. **Prefer a hub when the claim is equally honest.** A hub edge both pulls the node inward and is a stronger structural statement. But **honesty outranks centralizing** — see failure modes.
6. **Reject the weak ones.** Better one real edge than three similarity edges. Every edge is a **proposal** (dashed / candidate) until Ted confirms; his confirm/reject is the training signal.

## Evidence / success criteria
- Each new edge names a *specific shared mechanism*, not a shared topic.
- After regeneration, the node moves toward its true neighbors (verify positions, don't assume).
- At least one edge per enrichment pass is a **tension**, not a similarity, when the material supports it — tensions are the map's highest-value output (they surface contradictions to resolve).

## Traverse-test (quality check, not just edge-adding)
Before adding edges, *walk the node's existing edges as if you were an assistant answering "what is this node and what does it connect to."* Where you can't tell what an edge means without reading its note, or where two edges seem to point at different senses of the same node, you've found a quality defect to fix — not just a missing link. Enrichment includes *correcting* bad edges, not only adding new ones.

## Failure modes
- **Similarity-as-edge.** "Both about safety" is noise. The graph-builder's own rule: same topic area ≠ relationship.
- **The bundled / umbrella node.** When one node packs several distinct concepts, its edges silently attach to *different* members, and traversal becomes ambiguous — you can't tell which sub-concept an edge means. *(Learned 2026-07-18 on node 24 "incidental learning + constructivism + knowledge gardening": its 4 edges each pointed at a different one of the three theories, and one `sub_shape` edge was wrong because grounded-theory is a child of the constructivism third, not of the whole bundle.)* **Cheap detector:** `SELECT id, standard_concept FROM concept_bridges WHERE standard_concept LIKE '% + %'` — nodes joining theories with "+" are candidates (18/115 as of 2026-07-18; some are intentional UMBRELLA nodes, so confirm). **Fix, lightest first:** (1) name the touched facet in each edge's note so traversal is unambiguous; (2) re-point a mis-aimed edge to the correct sub-concept; (3) if the bundle genuinely holds separable ideas Ted works with distinctly, route a **node-split** proposal to `concept-bridge-surfacing` (node creation is that skill's domain, and splitting needs Ted). Do not silently split or delete.
- **Generic-hub destination.** An edge into a bucket so broad it barely distinguishes anything ("Learning Loops", "knowledge reinforcement loop") is a weak link — arriving there tells an assistant little. Prefer the most *specific* honest target; a generic hub edge is a last resort, not a win.
- **Centralizing over honesty.** Connecting a thin node to a hub *just* to pull it to the center is dishonest layout. The most honest edge may point at another rim node — then the node stays at the rim, and **that is correct**: it reveals a genuine off-center cluster (a sparse real region of Ted's thinking), not a misplacement. *(Learned 2026-07-18: node 108 "Model Home / inheritance-with-overrides" barely moved because its honest links — Foundation, knowledge-distillation — are themselves peripheral. Right call, not a miss.)*
- **Over-connecting the similar cluster.** Adding a 3rd/4th edge among already-linked look-alikes inflates degree without adding knowledge. Spend edges on *distinct* facets.
- **Rim = failure assumption.** Low degree after honest enrichment means "lightly connected," which is a true signal worth keeping, not a defect to hide.

## Runtime Notes

### Claude Code / Codex (live DB)
Nodes and edges are `concept_bridges` and `concept_bridge_relations` in `/Users/ted/Control/backend/system.db`.
- Full node text: `SELECT id, local_term, standard_concept FROM concept_bridges;`
- Current neighbors: query `concept_bridge_relations` on `from_bridge_id`/`to_bridge_id`.
- Valid `relation_type` values are CHECK-constrained: `sibling, sub_shape, anti_pattern, failure_mode_of, extends, same_dimension, dynamics_frame_for, governance_boundary_for, meaning_family, depends_on, enables, evolved_from, motivates, deepens`.
- Write edges with `promotion_status='candidate'` (renders dashed/proposed), `lifecycle_status='active'`, a real `notes` (the shared-mechanism rationale), and `created_by`/`evidence_ref` stamped to the session. Never write `confirmed` — only Ted's review flips that.
- Regenerate the map after writing: `python3 Operations/scripts/build_concept_graph_viz.py`. Verify node positions actually moved (`javascript_tool` reads `GRAPH.nodes[].x/.y`); don't assume.

### At scale (don't hand-do hundreds)
`Operations/scripts/build_concept_bridge_graph.py` does the bulk version: embed all nodes with local nomic-embed-text → nearest-neighbor candidate pairs → cheap-lane classifier picks the directed type → writes proposed edges. Use the manual method here for a focused region or a stubborn node; use that script to seed a whole graph. Same evidence standard applies to both.

### GPT bridge
No direct DB write. Route the proposed edges (with rationale) to `_AI_Inbox/` or the concept-bridge Action endpoint; do not pretend filesystem access.

## Update-surfacing backstop
This skill names live paths (`system.db`, `build_concept_graph_viz.py`, `build_concept_bridge_graph.py`) and the `relation_type` CHECK vocabulary. If any drift, fix here or leave a review note — a stale relation-type list will silently fail the INSERT.
