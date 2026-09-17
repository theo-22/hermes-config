---
name: repair-claim-effect-truth
description: Diagnose and repair claim or lease paths that mutate canonical work-item ownership or misreport effects, especially when composite coordination labels are parsed as one work item. Use when claim audit shows an unexpected owner write, a blocked retry says nothing changed despite earlier effects, or lock identity has been confused with execution ownership. Do not use for ordinary authorized rerouting, a simple active-claim collision with truthful effects, or file-checkout conflicts.
metadata:
  category: database-integrated
  write_mode: file
  one_line_use: restore truthful claim effects without turning coordination locks into ownership changes
  fast_pick: "yes"
---

# Repair Claim-Effect Truth

Use this skill when a claim, lease, or orchestration retry has two different stories:

- the coordination layer says it only acquired, blocked, or released a target;
- canonical work-item state or the audit trail shows an ownership or routing effect.

The core invariant is:

> A coordination target identifies what must not run concurrently. It does not, by itself, authorize a canonical ownership change.

## Boundaries

This skill repairs implementation and state after the invariant has been violated or reported falsely.

Use `route-work-item-ownership` instead when Ted or the Coordinator has already authorized a real queue-owner change. Use `verify-real-invocation-path` as a companion when installed-path proof is the remaining gate. Use the ordinary file-checkout workflow for file collisions.

Do not:

- infer routing authority from a claim actor, target string, or retry;
- treat a composite coordination label as one canonical work-item address;
- repair owner fields with direct SQLite writes;
- reopen terminal work merely to obtain a convenient test fixture;
- call a blocked retry effect-free until the entire attempt lineage has been checked;
- broaden a focused repair into a general claims-system redesign.

## 1. Start from live authority

Read the session-start authority for the current runtime. When this touches shared orchestration, claims, work items, or handoffs, consult the routed `_shared` doctrine before planning.

Resolve the current equivalents of:

- the canonical work-item row;
- the active and historical claims for the exact coordination target;
- claim-audit events, including owner-write effects;
- the parser or resolver that maps a target string to a work item;
- the caller that summarizes blocked, acquired, released, and terminal outcomes;
- the installed service or client path that exercises the code.

Record exact IDs and timestamps. Historical summaries are leads, not current authority.

## 2. Write the effect ledger before editing

For each attempt in the lineage, write a compact ledger:

| Attempt | Target | Claim result | Canonical owner before/after | Audit effect | Reported effect |
|---|---|---|---|---|---|
| first | exact target | acquired/blocked | value → value | exact event or none | exact response |
| retry | exact target | acquired/blocked | value → value | exact event or none | exact response |

Classify the defect:

- **identity defect** — a composite or descriptive target was parsed as one work item;
- **authority defect** — claim acquisition was treated as permission to rewrite owner;
- **accounting defect** — an earlier attempt changed state but a retry reported no effect;
- **mixed defect** — more than one of the above.

Preserve `UNKNOWN` where evidence is missing. A timeout, absent event, or truncated response is not proof of no effect.

## 3. Separate coordination identity from canonical identity

Inspect the target resolver. A target is a canonical single-work-item address only when the full target matches the current runtime's exact single-item grammar and resolves to one live row.

Fail closed for labels such as:

- ranges or lists of work items;
- coordination batches;
- descriptive strings that merely begin with a work-item token;
- parent/successor labels whose routing meaning is not explicit;
- opaque keys owned by another subsystem.

Do not fix this with a longer collection of string exceptions. Make the positive single-item grammar explicit; everything else remains coordination-only unless a typed mapping says otherwise.

## 4. Preserve legitimate single-item behavior

Before changing code, identify the valid path that must remain:

- exact single-item claims can enforce any documented `required_owner` constraint;
- an explicitly authorized single-item claim may write the actor as owner if that is the live contract;
- blocked claims must return the held claim's already-recorded effects when those effects matter to the caller;
- releases and expirations must not invent reverse ownership writes unless separately authorized.

The repair must narrow the false path without disabling valid claim, block, expiry, audit, or routing behavior.

## 5. Repair state through the control plane

If canonical ownership was changed incorrectly:

1. re-read the work item and audit trail immediately before recovery;
2. confirm the intended owner from authoritative routing evidence;
3. use the supported claim or queue transition that records actor, reason, and audit history;
4. read back the owner and the new audit event;
5. preserve the erroneous event as history rather than rewriting it away.

If routing intent is not settled, stop and ask Ted. This skill does not create that authority.

## 6. Patch the smallest responsible layer

Typical repair points are:

- exact target parsing;
- owner-write gating;
- propagation of held-claim effects into blocked results;
- response wording that distinguishes `this attempt wrote nothing` from `the held claim already changed state`.

Keep effect data structured. Prefer fields such as `held_claim_effects` or the runtime's existing equivalent over prose-only warnings.

Add a code comment only where the distinction between coordination identity and canonical ownership would otherwise be easy to collapse again.

## 7. Test the semantic matrix

At minimum, prove:

1. an exact single-item target keeps legitimate owner-write behavior;
2. a composite target can be claimed without changing any constituent owner;
3. a descriptive target beginning with an item token is not misparsed;
4. `required_owner` still blocks the wrong owner on a canonical single item;
5. a retry blocked by an active claim reports the held claim's prior effects truthfully;
6. release and expiry behavior remain intact;
7. unrelated claim types and file checkouts are unchanged.

Run the focused tests first, then the relevant surrounding suite.

## 8. Prove the installed path

When the repaired code is consumed by a service, plugin, bridge, or long-lived client:

1. verify which tracked file the installed process imports;
2. restart or reload only the affected consumer, if required and authorized;
3. use a bounded composite or descriptive target that cannot legitimately change a canonical owner;
4. capture the returned claim result;
5. query the claim audit for the probe's exact claim ID and target;
6. prove zero owner-write events for the composite target;
7. separately prove the valid exact-single-item path if safe.

A passing unit test or health endpoint is not installed-path proof.

## 9. Close the lifecycle

Before reporting completion:

- read back every recovered work-item owner;
- verify probe claims are terminal or deliberately retained;
- verify no file checkout or coordination claim remains active;
- receipt the code commit, tests, installed-path result, audit query, and state recovery;
- reconcile any originating work item or inbox packet through its normal lifecycle;
- name unrelated global noise separately instead of folding it into this result.

Completion means the false mutation is prevented, historical effects are reported truthfully, affected state is recovered through an audited route, and the real consumer path has been exercised.

## Runtime notes

The control-plane schema, target grammar, service launcher, and audit event names vary by runtime. Inspect current schemas and tool help before composing queries or commands. Use the local session-end or QuickSave authority for durable closeout.

## Update surfacing

Before a future repair, check the current claims API, work-item transition API, audit schema, installed consumer path, and shared routing doctrine. If any have changed, flag the drift and adapt the workflow rather than replaying stale commands.
