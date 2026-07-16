---
name: repair-capability-truth
description: Reconcile an AI role or runtime's live callable capability, static scope declarations, current documentation, and typed operational-query mappings. Use when fresh-session proof contradicts first-rung or stale capability docs, when connected apps or cached tool schemas are being conflated with actual calls, or when typed SQLite queries fail against a live schema. Preserve existing capability and role-mobility boundaries; do not use this skill to authorize permission expansion, database migration, or adjacent feature stages.
category: meta
write_mode: file
one_line_use: reconcile live role capability, current docs, and typed operational queries
fast_pick: "yes"
---

# Repair Capability Truth

Restore one evidence-backed account of what a role can do now, then repair
existing observability without changing authority or schema unless separately
authorized.

## Canonical Workflow

### 1. Freeze the authorized slice

- Start from the named review, proof, continuity, role, and code authorities.
- Restate the exact implementation stages and every parked stage.
- If authorization is report-only or no-write, run the evidence comparison and
  return the repair checklist, tests, and blockers. Do not return repair `PASS`:
  the current state remains `FAIL`, `PARTIAL`, or `UNKNOWN` until authorized
  edits, full verification, and durable proof exist.
- Treat missing authority for schema, permission, connector, spend, or protected
  changes as a hard boundary.
- Take claims before changing shared, role-owned, Control, or Operations
  surfaces. Check for conflicting claims first.
- Inventory dirty repositories and stage only task-owned files or hunks.

### 2. Separate capability evidence layers

Record these as distinct facts:

1. static server or role-scope declaration;
2. connector-advertised schema;
3. schema cached by the current conversation;
4. account-level connected apps;
5. tools actually callable in the fresh session;
6. calls exercised successfully;
7. tools exposed but intentionally not exercised because they mutate state,
   spend money, or trigger unnecessary role transitions.

Do not invent a connector-mode label that the product does not expose. Describe
behavior from evidence, such as “the fresh trusted session exposed the broader
callable surface.”

Preserve intentional role inhabitation. A role may enter a registered specialist
surface while still preserving the specialist's packet, authority, tools,
continuity destination, receipt identity, origin, and return condition. Do not
misdescribe this as either universal ambient authority or inability to use the
specialist role.

### 3. Prove the fresh session

- Run the role start operation and record health plus the declared tool count.
- Exercise representative read-only calls across Home/state, claims/receipts,
  memory, connected apps, and lifecycle/status surfaces when relevant.
- List exposed mutating tools separately; do not create proof state merely to
  show their schemas exist.
- Record unavailable checks as `UNKNOWN`, not successful.
- Let current direct proof outrank stale descriptions and historical assumptions.

### 4. Reconcile typed queries with the live schema

- Inspect the live database read-only with schema introspection such as
  `sqlite_master` and `PRAGMA table_info`.
- Compare every selected field, filter field, and ordering field with the live
  table—not only the first column named in an error.
- Expect cascading defects: SQLite commonly reports the first missing selected
  column while later selected or ordering columns are stale too.
- Repair the complete typed mapping and use an explicit per-table ordering map
  when tables do not share one timestamp or primary-key name.
- Do not migrate tables, rewrite data, add compatibility columns, or widen raw
  SQL access when the authorized task is mapping repair.

### 5. Repair only current descriptive surfaces

Update the current role profile, capability/status card, current state, next
action, role map, launch registry, Project instructions, handoff contract, and
live edge when evidence shows they are stale.

- Distinguish declared, advertised, cached, connected, callable, exercised, and
  unavailable capability.
- Preserve explicit specialist boundaries and existing capability.
- Remove current first-rung language only where later accepted proof supersedes
  it.
- Leave historical receipts, telemetry, and old acceptance records unchanged as
  historical evidence.
- Keep adjacent plans and later stages visibly parked.

### 6. Verify the whole typed surface

For every intended operational table:

- call its typed query directly with a read-only bounded limit;
- require `ok=true` and either valid rows or an honest empty result;
- verify returned fields exactly match the typed mapping;
- confirm previously working tables still work;
- call the aggregate summary and require a numeric count for every table;
- record exact counts and bounded exact direct results in the receipt.

Add a regression test that performs this sweep. Run syntax/compile checks and
scoped diff checks. If normal deployment requires a service reload, distinguish
that reload from building a separately parked restart-recovery capability. When
possible, repeat at least the aggregate through the connected role tool after
reload.

### 7. Leave durable proof

Write one owner-readable implementation receipt containing:

- authority and authorization boundary;
- claim IDs;
- documentation corrections;
- old-to-live mapping changes, including ordering fixes;
- exact individual and aggregate read-only results;
- tests and live-service proof;
- files changed, commits, and pushes;
- explicitly untouched stages and surfaces;
- remaining acceptance step, if any.

Update current continuity and closeout surfaces only after the implementation
proof is stable. Release every claim and verify the active-claim list is empty.

## PASS Standard

Return `PASS` only when:

- current documentation matches fresh-session evidence;
- no unsupported mode label or capability claim was added;
- no existing capability or intentional role mobility was narrowed;
- every named typed table passes individually and through the aggregate;
- previously working tables remain working;
- schema and data stayed unchanged unless separately authorized;
- parked stages stayed untouched;
- exact proof is durable and claims are released.

Use `PARTIAL`, `FAIL`, or `UNKNOWN` honestly when any condition is missing.

## Failure Modes

- Treating the first SQLite error as the complete mapping defect.
- Fixing selected columns while leaving a stale generic `ORDER BY id` fallback.
- Treating local tool registration as fresh-session callability.
- Treating an account-connected app as callable in the current chat.
- Naming a connector mode that the product never exposed.
- Treating a broad trusted surface as ambient mutation authority.
- “Preserving boundaries” by erasing intentional specialist-role inhabitation.
- Rewriting historical receipts instead of repairing current state surfaces.
- Combining truth repair with schema migration, new connectors, scheduling, or
  later feature stages.
- Committing unrelated dirty work or leaving claims active.

## Runtime Notes

- **Codex or Claude Code:** use live files, read-only database introspection,
  scoped tests, claims, and repository-specific commits.
- **Chat role:** gather fresh-session callable proof and write only through its
  owned tools; route protected code or shared-document repair to an authorized
  execution surface.
- **Other runtimes:** preserve this evidence model and PASS standard while
  adapting only the mechanics. Do not create a local doctrine fork.

## Update Backstop

This skill names patterns, not permanent paths or column names. Re-check the
live role scope, connector, database schema, claim mechanism, receipt home, and
repo roots every run. Update the shared skill when repeated use changes what
counts as evidence, complete repair, or safe closeout.
