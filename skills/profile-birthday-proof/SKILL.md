---
name: profile-birthday-proof
description: Run a clean birth, promotion, or first-wake proof for a new AI profile, role runtime, agent, or major operating surface. Use when a profile is created, re-homed, given new memory/session-start rules, or promoted from staged/mirror state to live use. Requires live path verification, start artifact, proof note, correction handling, and CHANGES_LOG when durable state changes.
category: meta
write_mode: file
one_line_use: birth a profile with proof and log
fast_pick: "yes"
---

# Profile Birthday Proof

Birth the profile where it actually runs, then leave a proof trail.

This skill captures the pattern proven during the Coordinator-Hermes birthday: a new or changed profile is not considered live just because files exist or a chat says it worked. It becomes live when the runtime wakes, reads the intended live files, writes proof artifacts, corrects any path confusion, and records durable state change.

## Use When

- A new Hermes profile, GPT role, agent, or role-runtime surface is created
- A profile gets new `SOUL.md`, memory, session-start, session-end, or wake rules
- A staged/editable mirror is promoted back to a live runtime profile
- There is risk that the actor will read the wrong copy of a file
- Ted says birthday, first wake, prove it, make it real, or similar
- Work changed durable profile behavior and needs `CHANGES_LOG`

## Do Not Use When

- The work is only ordinary task completion inside an already-proven profile
- Nothing durable changed
- The task is a broad session-end rather than a profile proof
- The only question is live-vs-doc disagreement; use `live-surface-verification` first if no profile lifecycle event is happening

## Core Rule

Runtime truth outranks editable mirrors, intended-state docs, memory summaries, and chat reports.

A profile birthday is not complete until the profile proves which live files it read and writes proof where Coordinator can verify it.

## Required Surfaces

Name the intended live paths before the wake test.

For Hermes profile work, distinguish:

```text
Live profile runtime:
/Users/ted/.hermes/profiles/<profile>/SOUL.md
/Users/ted/.hermes/profiles/<profile>/memories/MEMORY.md

Editable mirror:
/Users/ted/Coordinator/Working/<profile>-profile-edit/

Coordinator-readable proof:
/Users/ted/Coordinator/Inbox/
/Users/ted/Operations/Hermes_Handoff/
/Users/ted/Operations/CHANGES_LOG.md
```

Do not let the profile treat an editable mirror as runtime truth unless Ted explicitly says the mirror is the runtime for this test.

## Birthday Workflow

1. **Name the birth event.**
State what is being born or promoted: profile name, model if relevant, and why this is a lifecycle event.

2. **Give the profile a bounded wake prompt.**
Ask it to run normal session-start, read the intended live files, and write proof. Include the exact live paths when path confusion is possible.

Minimum prompt requirements:

```text
Wake as <profile>.
Run normal session-start.
Read live SOUL and memory from <absolute live paths>.
Do not substitute the editable mirror.
Write a session-start artifact.
Write a short proof note.
Keep it brief and profile-shaped.
```

3. **Require a session-start artifact.**
For Hermes profiles, use a Coordinator-readable path such as:

```text
/Users/ted/Operations/Hermes_Handoff/<Profile>_Session_Start_YYYY-MM-DD.md
```

The artifact should include:

- timestamp
- profile name
- model/provider
- exact files read
- preflight status
- communication status if relevant
- top current items
- immediate risks
- next recommended action

4. **Require a proof note.**
For Coordinator-readable proof, use:

```text
/Users/ted/Coordinator/Inbox/<profile>_birth_proof.md
```

The proof note should be short: one-line awake summary, preflight status, and path to the session-start artifact.

5. **Verify from the outside.**
Coordinator or the supervising actor reads the proof files and checks:

- proof note exists
- session-start artifact exists
- exact model/profile reported
- files read are the live runtime paths, not mirrors
- status is bounded and honest
- yellow items are actionable and owned

6. **Handle correction immediately.**
If the profile read from the wrong path, overreached, missed a file, or misreported state, ask for a correction note rather than burying the mistake.

Use a path like:

```text
/Users/ted/Coordinator/Inbox/<profile>_birth_path_check.md
```

Correction note must include:

- exact paths read
- intended live paths
- whether live paths exist
- whether editable mirror was used
- whether content matched
- recommended fix
- whether persistent memory/session-start behavior was corrected

7. **Set status honestly.**
Use a compact status phrase:

- `BORN / GREEN` — live proof complete, no active yellow items
- `BORN / YELLOW-GREEN` — live proof complete, bounded follow-ups remain
- `BORN / YELLOW` — live proof worked but important setup remains
- `NOT BORN` — proof artifact missing, wrong profile, wrong paths, or no live wake

Do not call it green when path correction, communication setup, or config cleanup remains.

8. **Write CHANGES_LOG for durable profile changes.**
If the birthday changed durable system state, profile behavior, memory, runtime wiring, or role status, append to `/Users/ted/Operations/CHANGES_LOG.md`.

Include:

```markdown
## YYYY-MM-DD — <Profile> birthday proof completed

- Change: <what was born/proven and what artifacts were written>
- Verification: <proof note, session-start artifact, correction note if any>
- Status: <BORN / ...>
- Remaining: <bounded yellow items>
- Reasoning: <why this belongs in CHANGES_LOG>
```

If the current actor cannot write `CHANGES_LOG.md`, route a concrete request to the actor/profile that can, including the exact suggested entry.

9. **Capture the convention.**
If this birthday changed how future sessions should start or close, update the profile's memory, SOUL, session-start rule, or relevant skill. Do not rely on one chat remembering it.

## Common Failure Modes

- `mirror confusion` — profile reads from editable mirror instead of live runtime path
- `proof without session-start` — one-line proof exists but no reusable session artifact
- `birth without log` — durable role change is absent from CHANGES_LOG
- `greenwashing` — status says green while communication/config/path issues remain
- `chat-only correction` — mistake is acknowledged in chat but not written to a durable note
- `unowned yellow` — follow-up items are named without owner or next action

## Relationship To Other Skills

- Use `live-surface-verification` when the main problem is disputed live state.
- Use `quick-save` when saving one bounded completed task, not birthing a profile.
- Use `poka-yoke` when a birthday reveals a recurring memory-dependent failure that should be structurally prevented.
- Use `manager-handoff-contract` when a worker produced material that needs manager intake, not runtime birth proof.

## Output Shape

Use this compact closeout:

```text
Profile: <name>
Birth event: <what changed>
Proof: <paths>
Correction: none | <path and summary>
CHANGES_LOG: written | routed | skipped with reason
Status: BORN / GREEN|YELLOW-GREEN|YELLOW or NOT BORN
Remaining yellow: <bounded items>
```

Keep it short. The proof files carry detail.