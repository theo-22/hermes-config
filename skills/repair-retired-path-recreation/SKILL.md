---
name: repair-retired-path-recreation
description: Trace and repair a retired filesystem path that reappears because an active scheduler, installed script, generated prompt, runtime profile, launcher, skill copy, or other consumer still writes there. Use when a moved or deleted root comes back, a supposedly retired directory gains fresh files, multiple runtime copies disagree about the replacement path, or a relocation needs preservation-first cleanup plus proof through the exact installed consumer path.
metadata:
  category: meta
  write_mode: file
  one_line_use: trace every live recreator, repoint the full consumer chain, preserve state, and prove the retired path stays absent
  fast_pick: "yes"
---

# Repair Retired Path Recreation

Stop the live recreation chain. Do not merely remove the directory again.

## Boundary

- Start with the named retired path and the settled canonical destination.
- Treat diagnosis as read-only until repair is authorized.
- Do not create a compatibility symlink or empty stub; either can hide a stale writer.
- Do not delete recreated reports, browser profiles, credentials, backups, or unknown state. Preserve first and show any irreversible choice.
- Do not infer that tracked source is the installed consumer. Prove which copy the scheduler, launcher, service, or actor actually reads.
- Keep historical outputs and explicit retirement notes unless they can execute or direct a current writer.
- Stop at the named relocation. Route unrelated dead-path cleanup separately.

## Workflow

### 1. Freeze the retirement contract

Record the retired path, canonical replacements, required old-path state, recreated data classes, and unauthorized destructive actions. If the destination is disputed, use `reconcile-runtime-authority` before editing.

### 2. Establish a recreation timeline

Inspect the recreated root before moving anything:

- directory and file birth/modification times;
- sizes and top-level contents;
- open files and running process command lines;
- scheduler job history, last-run times, outputs, and errors;
- browser history or service logs only when they can correlate a writer without exposing unnecessary personal data.

Match timestamps to actual jobs and processes. A path mention is a lead, not proof of authorship.

### 3. Trace every executable reference

Search narrowly first, then widen only as evidence requires:

1. enabled scheduler definitions and prompts;
2. exact scripts resolved by those jobs;
3. installed runtime instructions, profile-local skills, launchers, services, and hooks;
4. tracked source and sync/publish machinery;
5. shared or public skill copies;
6. dormant profiles that may be re-enabled;
7. generated output and historical records last.

Classify each match:

| Class | Meaning | Action |
|---|---|---|
| active writer | Can currently create or write the path | Repoint and live-prove |
| active reader | Reads the old path but does not create it | Repoint and prove readback |
| revivable copy | Disabled or dormant but likely to return | Repoint if mechanically identical and in scope |
| generated state | Scheduler counters, logs, output receipts | Preserve; do not treat as source |
| history/tombstone | Correctly records the retired path | Keep |

Check for dual-copy drift explicitly: tracked versus installed, global versus profile-local, source versus published, and shared skill versus cloned profile skill.

### 4. Claim and repair the full live chain

Claim shared targets before mutation. Change the smallest complete chain: authoritative source, installed consumer, enabled job prompt or command, shared/published skill or launcher, and mechanically cloned revivable copies when leaving them stale would recreate the fault later.

If two jobs write the same artifact, settle one writer. Make other jobs read-only or give them a different output contract.

Do not bulk-commit unrelated scheduler counters, timestamps, or inherited workspace changes. Stage only repair-owned hunks.

### 5. Preserve and relocate recreated state

Before removing the retired root:

1. check for destination collisions;
2. move unique authoritative artifacts into their canonical home;
3. preserve opaque or merge-sensitive state, such as browser profiles, as a dated intact archive;
4. avoid merging profiles, databases, cookies, or credentials without a separate reconciliation;
5. remove the retired root by moving the remaining tree to the recovery archive when practical.

Report exactly what moved, where it moved, and whether it is recoverable.

### 6. Add a deterministic regression guard

Create or extend a verifier that fails when:

- the retired root exists;
- an enabled job names the retired path;
- an active script, installed instruction, launcher, hook, or shared/published skill contains an operative retired-path reference;
- the canonical replacement is missing;
- the real scheduled script does not resolve to the canonical output.

Allow only explicit history/tombstone lines using narrow markers such as `retired`, `moved from`, or `was`. Do not globally ignore a file merely because one historical line exists.

Run the guard once before relocation to demonstrate that it catches the live fault, then again after repair.

### 7. Prove exact consumers

Use `verify-real-invocation-path` and require paired evidence:

- positive: the installed scheduler, service, launcher, or application writes or opens the canonical path;
- negative: the retired root remains absent during and after the invocation.

Prefer a bounded no-agent job, dry-run, harmless browser launch, or read-only service probe. Do not trigger shopping, financial, messaging, or other consequential actions solely for proof.

For each consumer record command, cwd/environment, resolved executable, observable output, and postcondition. Compilation and static search are supporting evidence, not acceptance.

### 8. Hear affected runtimes and close out

If another standing actor's startup, continuity, or tools changed, ask it for impact evidence after the repair. Treat its response as a seam-finding pass, not approval. Verify every raised seam against live state.

Write a durable receipt containing the recreation timeline, proven writers, changed source/installed/published surfaces, preservation locations, guard result, exact-consumer proof, remaining historical references, validator mismatches, and commit/push state.

## Completion gate

Declare the repair complete only when all are true:

- every proven active recreator is repointed or retired;
- canonical data is present and opaque recreated state is recoverable;
- the retired root is absent;
- the deterministic guard passes;
- at least one exact installed consumer has run successfully;
- the retired root remains absent after that run;
- tracked and installed authority agree;
- affected-role seams are resolved or explicitly routed;
- repair-owned changes are committed without absorbing unrelated work.

If the root reappears after this gate, preserve it again and compare its new timestamps against scheduler/service activity. Treat that as evidence of an untraced writer, not as permission to delete it repeatedly.
