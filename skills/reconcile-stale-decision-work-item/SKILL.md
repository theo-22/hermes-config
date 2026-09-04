---
name: reconcile-stale-decision-work-item
description: Verify and close a live work item that says a decision is still open when primary authority, audited history, or canonical state may show it was already settled. Use for stale decision rows, open-question prose, mirrors, indexes, or receipts that need evidence-backed reconciliation. Do not use to make a new decision, infer an absent decision, change ownership, or implement the underlying decision.
metadata:
  category: database-integrated
  write_mode: shared
  one_line_use: reconcile a stale open-decision row to already-settled authority without re-deciding it
  fast_pick: "yes"
---

# Reconcile Stale Decision Work Item

Prove whether a named decision is genuinely open, then either preserve the gate or reconcile stale operational surfaces to the already-settled authority.

## Authority and Boundaries

- Treat the live Control work-item row as lifecycle authority, not as proof that its decision question is still substantively open.
- Treat the primary decision record and its audited event history as decision authority. A dashboard, generated summary, memory note, receipt, search result, or stale prose field is evidence or a lead, not stronger authority.
- Preserve the exact decision's scope. Do not turn a narrow adjudication into a broader relationship, ownership, implementation, or acceptance decision.
- Never manufacture, infer, or silently reinterpret Ted's decision. If the evidence is incomplete or conflicting, leave the item open and surface one concrete question.
- A decision relay records an already-existing decision. It is not a new decision and does not grant new authority.
- Keep implementation of the underlying decision outside this skill unless separately authorized.

## Canonical Workflow

### 1. Read the named live surfaces

Start at the work item or authority surface named by the user. Read:

- the exact work-item row, including type, state, owner, required owner, decision contract, source references, timestamps, and evidence;
- active claims on the item and every surface that may need mutation;
- the canonical object or relationship named by the decision;
- its event or audit history;
- the current consumer-visible prose, generated artifacts, mirrors, indexes, and receipts that repeat the claim.

Inspect the live API and schema before assuming field names, state vocabulary, actor gates, or mutation semantics.

### 2. Classify the decision state

Choose exactly one result:

1. **Genuinely open:** no authoritative decision exists. Preserve the pending state and present the exact question, recommendation, evidence, and recheck condition.
2. **Already settled, canonical state correct:** the authoritative decision and live canonical object agree, but one or more secondary surfaces still call it open. Reconcile only those stale surfaces.
3. **Already settled, canonical state stale:** the authoritative decision is unambiguous but the canonical object has not absorbed it. Use the narrow audited operation authorized for that object, then refresh dependent surfaces.
4. **Conflicting or incomplete:** authority cannot be resolved without new judgment. Preserve `UNKNOWN` or open state and ask the required owner one concrete question.

Do not count repeated summaries as independent evidence. Prefer the earliest primary decision statement plus the audit event that applied or confirmed it.

### 3. Claim only the mutation lanes

Before writing, acquire live claims for the exact files, objects, or work item being changed.

- Use only supported grains: `surface`, `task`, or `domain`.
- Remember that a task claim may bind or change `work_items.owner`. Use it only when that side effect is intended and authorized.
- Do not clear `required_owner`, seize another actor's claim, or use a claim as routing authority.
- Carry stable idempotency keys and observed-state guards into mutations when the installed operation supports them.

Stop if another actor holds an overlapping lane.

### 4. Build the relay proof

Before attributing a terminal transition to Ted or another required owner, record all of:

- the exact decision, in the required owner's words or an exact faithful proposition;
- the primary source and timestamp;
- the audit event or canonical state that shows the decision was applied or confirmed;
- the narrow scope that remains unchanged;
- why the present action is a relay or stale-surface reconciliation rather than new judgment.

Use the required owner's actor identity only when the installed lifecycle explicitly requires it and the evidence proves an exact pre-existing decision by that person. Never use `actor=ted` merely to pass a gate.

### 5. Reconcile the narrowest authoritative surface

Apply the smallest change that makes the operational surfaces truthful:

- remove or replace stale “still open” language without changing the settled object;
- use audited APIs rather than direct database edits;
- preserve before/after state, source reference, actor, timestamp, and idempotency evidence;
- keep confirmed relation types, lifecycle states, ownership, and unrelated notes unchanged;
- regenerate canonical projections and mirrors only from their owning generator;
- refresh indexes or caches only when they are actual consumers of the stale field.

If a legacy field cannot be cleared safely because its schema is append-only or uses coalescing updates, name that bounded residue. Do not broaden the task to redesign the schema.

### 6. Prove convergence before closure

Verify independently from the write response:

1. the primary decision remains unchanged and inspectable;
2. the canonical object matches that decision;
3. affected prose and projections no longer claim the decision is open;
4. generated artifacts and mirrors match their canonical source;
5. relevant indexes or consumers see the corrected state;
6. the work item is terminal through persisted readback;
7. no claim remains active for the lane.

Write a durable receipt that distinguishes the old stale statement, the settled authority, the reconciliation performed, and any deliberately preserved residue. Commit only bounded files and leave unrelated dirty work untouched.

## Evidence Standard

Completion requires:

- exact live work-item readback before and after;
- exact primary decision source and timestamp;
- audited object or event-history proof;
- before/after evidence for every mutated surface;
- generator or mirror parity when affected;
- consumer or index verification when affected;
- terminal work-item readback;
- released-claim proof;
- a focused commit and durable receipt for shared changes.

A terminal row alone is insufficient. So are a historical summary alone, an unchanged hash without semantic inspection, a mutation response without readback, or the operator's own interpretation of an ambiguous decision.

## Failure Modes

- **Gate bypass:** setting the required owner's actor identity without an exact prior decision.
- **Re-decision by cleanup:** changing relation meaning, lifecycle, ownership, or scope while removing stale prose.
- **Queue literalism:** assuming a pending decision row proves the substantive question is still open.
- **Summary promotion:** treating memory, a receipt, or a generated view as stronger than primary authority and audit history.
- **Canonical-only closure:** correcting the database but leaving the stale source or consumer that will recreate the contradiction.
- **Projection-only closure:** editing a mirror or report while the canonical object remains wrong.
- **Claim side effect:** using a task claim without noticing that it changed the work-item owner.
- **Unsupported certainty:** collapsing conflicting evidence into a confident answer instead of preserving `UNKNOWN`.
- **Residue sprawl:** redesigning a legacy review-note schema when a bounded, named residue does not affect the settled decision.

## Runtime Notes

- Prefer installed Control APIs or role tools for reads and audited mutations. Direct SQLite writes are not an acceptable recovery path.
- Endpoint names and actor gates can drift. Inspect the installed schema and implementation before mutating.
- If the runtime cannot perform an authority-bearing relay, produce the exact evidence packet and requested transition for the required owner; do not report closure.
- Historical memory can accelerate discovery, but current live state must be reverified before action.

## Update Backstop

If decision fields, claim effects, actor gates, audited operations, or projection ownership change, update this shared skill and its adapters together. Do not create a runtime-local fork.
