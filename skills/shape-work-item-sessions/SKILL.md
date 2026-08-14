---
name: shape-work-item-sessions
description: Reconcile one or more live Control work_items with current user decisions and turn each surviving row into a cold-readable future-session contract. Use when Ted reviews the backlog, says to set items up for sessions, reroutes several items, identifies discussion/waiting/runnable lanes, or asks which queue items are ready next. Verifies closure evidence, updates existing rows instead of duplicating work, and separates session shaping from execution, conductor chains, work packets, and QuickSave.
metadata:
  category: database-integrated
  write_mode: shared
  one_line_use: turn live queue rows and current decisions into bounded future-session contracts
  fast_pick: "yes"
---

# Shape Work Item Sessions

Convert a queue review into future sessions that can start from the live row
without reconstructing the originating conversation. Shape the work; do not
silently execute it.

## Boundaries

- Treat `/Users/ted/Control/backend/system.db#work_items`, read through
  `GET /api/work-items`, as work-status authority.
- Treat Ted's current statement as authority for routing, priority, and
  discussion gates. Preserve older notes as history; append the new decision.
- Update an existing row when it already represents the work. Do not create a
  replacement row merely to improve its wording.
- Close a row only after mapping live evidence to every material clause.
- Keep `owner` as a best-fit hint. Set `required_owner` only for a real hard
  gate such as Ted's decision or an actor-only capability.
- Do not turn session shaping into implementation, proposal approval, a
  conductor chain, or a work packet unless Ted also asks for that next action.

## Workflow

### 1. Read live state and named sources

Query the current rows first:

```bash
curl -sS 'http://127.0.0.1:5555/api/work-items?state=pending'
```

Read only the source/owner files needed to understand the named items. Check
active claims before writes. If remembered counts or summaries disagree with
the API, use the API and correct the discrepancy explicitly.

### 2. Classify every named item

Give each row exactly one current session shape:

- **runnable** — bounded, authorized, decision-free, and externally checkable;
- **guided decision** — Ted or another authority must settle a real fork;
- **discussion/review** — compare an idea with live behavior before authorizing
  implementation;
- **waiting/triggered** — name the actor, date, or observable exit condition;
- **multi-session program** — define one batch and stop condition per session;
- **routed** — another actor owns the next move; name whether that is a soft
  owner hint or a hard required-owner gate;
- **closeable** — every acceptance clause has current evidence;
- **unresolved** — the row cannot yet be shaped without a missing authority or
  source; name the exact gap.

Do not label a row `deferred` merely because it is inconvenient. Use a waiting
shape with an observable trigger, and use the database's deferred state only
when the live lifecycle convention calls for it.

### 3. Write the session contract

Append a dated note containing enough of these fields for the actual shape:

1. current authority or decision;
2. session type and objective;
3. exact source/owner surfaces to read first;
4. in-scope work;
5. exclusions and protected surfaces;
6. actor routing and any genuine hard gate;
7. evidence or acceptance criteria;
8. stop condition and expected return;
9. source-item disposition when the row came from durable intake.

Use ordinary language. Preserve unresolved judgment as a discussion gate; do
not encode it as an implementation instruction.

### 4. Apply metadata safely

Use the bundled helper for title, owner, required-owner, priority,
destination, and appended-note changes. It acquires a task claim, guards the
notes snapshot, writes one transaction, logs a `work_item_session_setup`
event, and releases the claim.

```bash
python3 scripts/shape_work_item_session.py show --item-id 123

python3 scripts/shape_work_item_session.py apply \
  --item-id 123 \
  --actor codex \
  --expected-notes-sha256 '<hash from show>' \
  --owner 'codex' \
  --priority normal \
  --append-note 'SESSION CONTRACT YYYY-MM-DD — ...'
```

Use `--required-owner NAME` or `--clear-required-owner`, never both. The helper
does not change lifecycle state.

For terminal transitions, use the canonical endpoint separately after proof:

```bash
curl -sS -X POST http://127.0.0.1:5555/api/work-items/state \
  -H 'Content-Type: application/json' \
  -d '{"item_id":123,"state":"acted","actor":"codex"}'
```

If the item has an `_AI_Inbox` source packet, use
`reconcile-inbox-work-items` so packet and work lifecycle remain paired.

### 5. Establish the next-session order

Rank runnable work ahead of items waiting for an actor or decision. Recommend
one next session, not an equal menu, unless Ted explicitly asks for options.
Do not let a low-priority maintenance row displace a high-priority authorized
lane without naming the reason.

### 6. Route stronger artifacts only when earned

- Use `workflow-orchestration` when Ted wants a conductor/session-chain lane
  staged or run.
- Use `compile-work-packet` for consequential authorized asynchronous or
  cross-actor dispatch.
- Use `context-extension-surfacing` for determinate immediate side work that
  should leave the primary conversation.
- Use `quick-save` or the actor's full session-end protocol to close the
  shaping session; these save the work but do not own intake shaping.

## Verification and Closeout

Before reporting completion:

1. Read every changed row back through `/api/work-items`.
2. Confirm the pending count and correct arithmetic mistakes explicitly.
3. Confirm every terminal transition and its event record.
4. Confirm no task/file claim from this lane remains active.
5. Update priority/continuity only when the order or future-session reality
   materially changed.
6. Report what is runnable now, what is discussion-gated, what is waiting, and
   what questions genuinely remain.

## Failure Modes

- **Chat-only shaping** — good session boundaries evaporate instead of landing
  in the live row.
- **Duplicate queue rows** — a rewritten item is added instead of updating the
  authoritative existing row.
- **Premature execution** — shaping language is mistaken for authorization to
  perform the future session.
- **False closure** — adjacent machinery is treated as evidence for an unmet
  connecting behavior.
- **Owner inflation** — a likely actor is encoded as a hard gate.
- **Vague waiting** — “later” or “when available” lacks the exact actor/date/
  state that resumes the work.
- **One giant backlog session** — a program row has no per-session batch or
  stop condition.
- **Stale total** — item-level reconciliation is correct but the reported
  queue count is not recomputed.

## Resources

- `scripts/shape_work_item_session.py` — guarded metadata/note updater and
  readback helper.
- `scripts/test_shape_work_item_session.py` — disposable-database regression
  for snapshot guarding, metadata updates, event logging, and duplicate-note
  refusal.
