---
name: proposal-packet
description: Turn an already-formed idea, recommendation, system change, or handoff into a compact durable proposal packet. Preserve the generic evaluation/handoff function; when the intended next transition is independent Projection and Build State has been reached, produce the stricter Build State / Projection launch packet with governing intent, acceptance conditions, projector freedom, concrete stop conditions, and self-critique. Do not use to discover the proposal; use proposal-candidate-surfacing first when meaning/shape are still forming.
metadata:
  category: database-integrated
  write_mode: file
  one_line_use: write the Build State / Projection launch packet
  fast_pick: "yes"
---

# Proposal Packet

Turn an already-shaped proposal into a compact durable packet that another AI or Ted can evaluate without the full chat.

There are two valid dispositions:
- **Generic proposal packet** — for durable evaluation, human decision, or handoff when independent Projection is not the next transition. Build State is not required.
- **Build State / Projection launch packet** — for substantial work that is deliberately crossing from shared planning into independent Projection. This compact packet is required before that Projection begins.

The packet is not the implementation design. In the Projection branch, its job is to preserve governing intent and shape well enough that a capable projector has freedom to infer the realization without Ted continuing to prescribe mechanisms.

Do not use for routine notes, open-ended brainstorming, or bounded deterministic work that should simply be done.

If the proposal is still ambiguous for its intended disposition, return to proposal-candidate-surfacing. Packet authoring should primarily transcribe and compress what is already settled.

## Inputs that matter

- Concrete proposal/change under consideration
- Observations/evidence that led to it
- Intent and desired outcome
- Enough-for-use shape
- Conditions/boundaries and explicit exclusions
- Acceptance conditions
- Known genuine human/authority gates
- Important unresolved assumptions
- Named owner/destination only when actually settled

## Workflow

### 1. Determine the packet disposition and readiness

If this is a generic proposal for evaluation/decision/handoff, preserve the already-shaped proposal without inventing Build State.

If the intended next transition is independent Projection, confirm Build State before writing the launch packet: a capable assistant must be able to project from the settled understanding without Ted reconstructing the conversation or prescribing the mechanism. If not, stop and return the missing Build State element(s).

### 2. Separate observation from intent from proposed change

Keep distinct:
- what is observed/evidenced;
- what the system is trying to accomplish;
- what change/recommendation is being proposed.

Do not let evidence masquerade as the recommendation, or an earlier mechanism suggestion masquerade as a requirement.

### 3. Preserve the enough-for-use shape

State the smallest coherent version that serves the current need and leaves room to grow.

Larger expansions are future possibilities unless they are part of the settled intent.

### 4. State acceptance conditions

For a Projection launch packet, write conditions that a separate evaluator could use to judge the finished Projection. Prefer outcome/behavior/constraint tests over implementation instructions.

For a generic proposal packet, include acceptance/decision criteria when they materially help evaluation; do not manufacture them merely to imitate the Projection branch.

### 5. State projector freedom when Projection is the next transition

For a Build State / Projection launch packet, explicitly name what the projector may decide independently.

Default: mechanisms, internal structure, routes, sequencing, tooling, and other ordinary design choices inside the established intent envelope belong to the projector unless they cross a named stop condition.

Do not over-specify a mechanism merely because it was discussed during planning. If a mechanism is genuinely load-bearing, say why it is part of the requirement.

For a generic proposal packet, this section is optional unless design freedom itself matters to the evaluation.

### 6. State stop / human gates

For a Projection launch packet, write **work-specific concrete stop conditions** that require re-entry of Ted or another authority. The categories below are prompts for finding those conditions, not acceptable substitutes for naming the actual stop in this work:
- genuine meaning/value fork;
- accepted-risk decision;
- new authority/ownership boundary;
- materially consequential durable-state change outside standing authority;
- spend/credential/privacy/clinical or other protected consequence boundary;
- contradictory evidence that invalidates the governing intent.

Normal design uncertainty is not a human gate. If no concrete human/authority stop condition applies, say `none identified inside the current standing authority envelope` rather than copying a generic category.

### 7. Apply the poka-yoke check

Name any new memory-dependent step, accumulating surface, convention-only dependency, or deferred decision without a resurfacing rule.

Either remove the memory dependence structurally or name and explicitly accept the failure mode with rationale.

### 8. Add self-critique

Name assumptions, weak spots, ambiguous edges, and where a reasonable projector/evaluator could disagree.

Do not omit self-critique merely because the packet is short.

### 9. Write the durable packet and track it

Resolve the current approved file/inbox/work-item path at runtime through the live owner/capability routing surface. Do not hardcode a historical destination. If no destination is settled or discoverable, keep the packet on the current actor’s governed staging/continuity surface and name destination unresolved rather than inventing an owner.

The durable packet should be sufficient for a cold projector to reconstruct the governing intent without the full originating chat.

### 10. Enter independent Projection — Projection branch only

A compact Build State packet is required before independent Projection begins. After the packet is complete, the projector re-anchors on it as governing input and independently constructs the realization. Independence is a process boundary, not necessarily a new persistent identity: earlier mechanism suggestions are non-binding unless the packet makes them requirements. A fresh session, model, worker, or context is optional when it materially improves independence or capability fit; continuing the same collaborative momentum without re-anchoring on the packet does not satisfy this boundary.

The projector may:
- traverse the Concept Graph and current State progressively;
- activate bounded capabilities;
- change mechanisms from earlier planning when a better realization satisfies the same intent;
- solve ordinary design uncertainty without Ted.

The projector should stop only at a named human/authority boundary or a newly discovered genuine fork.

### 11. Independent evaluation

Use an evaluator that did not participate in constructing the Projection. To count as independent, invoke it through a fresh evaluator carrier/context when the runtime supports that, give it only the Build State packet, finished Projection, and needed evidence, and record the evaluator run/receipt so non-participation is inspectable. If the evaluator shares construction context or only self-review is available, label it degraded; do not represent it as satisfying the independent-evaluation gate.

Give the evaluator:
- this Build State packet;
- the finished Projection;
- evidence needed to test load-bearing claims.

Ask the evaluator to judge:
- fidelity to intent/outcome;
- acceptance conditions;
- hidden assumptions/omissions;
- boundary violations;
- unnecessary machinery/failure modes;
- whether the projector preserved appropriate freedom and simplicity.

The evaluator should report findings, not replace the Projection with its preferred architecture. Findings return to the projector for revision. A finding goes to Ted only when it exposes a genuine human gate.

### 12. Hand authorized execution forward

For Projection-bound work, only after independent evaluation should execution pass through the existing live owner/capability/authority check. The projector does not self-classify itself as authorized. Work already inside standing authority may proceed through the governed execution path; work outside it or crossing a concrete stop condition requires the relevant external authority first.

Do not turn this proposal skill into execution authority.

## Output shape

Use the smallest shape that fits the disposition.

**Generic proposal packet:**
- Topic
- Why now
- Observation / evidence
- Proposed change / recommendation
- Enough-for-use shape
- Boundaries / what is ruled out
- Open questions / assumptions
- Poka-yoke check
- Self-critique
- Suggested destination / owner — only when known; otherwise label as suggestion
- Confidence / status

**Build State / Projection launch additions (required for Projection-bound work):**
- Intent / desired outcome
- Acceptance conditions
- Projector freedom
- Work-specific concrete human / authority stop conditions
- Status — Build State / projection-ready

Keep either packet terse. The goal is durable reconstruction for its intended next transition, not transcript preservation.

## Never assume

- Build State is not execution authorization.
- Alignment is not approval.
- An implementation idea discussed during planning is not automatically a requirement.
- Destination, owner, deadline, or authority are not inferred from tone.
- The projector should not ask Ted to choose ordinary mechanisms inside the envelope.
- The evaluator should not take over authorship merely because it sees another valid design.
- A verified landed Projection becomes State; it does not remain a permanent special Projection layer.
- A generic proposal does not become a Projection merely because it was written with this skill.

## Scripts vs skill

Use this skill for judgment and durable packet shaping.

Use deterministic packet compilation/linting only after external authorization when consequential asynchronous/cross-actor work needs a fixed execution contract.

Keep proposal formation, Build State, independent Projection, evaluation, authorization, execution compilation, dispatch, and verification as distinct gates.

## Update-surfacing backstop

If packets are repeatedly rewritten downstream, projectors cannot reconstruct intent without the originating chat, evaluators cannot judge them cold, or routine design choices keep returning to Ted, treat that as evidence that this skill's Build State contract is incomplete or over-prescriptive and revise the skill rather than normalizing the workaround.
