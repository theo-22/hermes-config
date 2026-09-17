---
name: reconcile-runtime-authority
description: Diagnose and repair a runtime whose startup, continuity, configuration, generated reports, or documentation disagree about which surface is authoritative. Use when multiple files claim to be canonical, a session-start or root instruction appears twice, active consumers still point to a retired path, an old file keeps being rewritten, or a change needs static, injected-context, and genuinely fresh-runtime proof without erasing historical evidence.
metadata:
  category: meta
  write_mode: file
  one_line_use: reconcile competing runtime authority surfaces and prove the live chain
  fast_pick: "yes"
---

# Reconcile Runtime Authority

Establish one live activation authority, give every neighboring surface one clear function, and prove that real consumers follow the corrected chain.

## Boundary

Treat diagnosis and implementation as separate authorities.

- For diagnosis-only work, inspect and report; do not mutate.
- For authorized repair, change only the authority chain and the consumers required to make it effective.
- Do not enable disabled automations, broaden permissions, delete history, or redesign neighboring runtimes solely to obtain proof.
- Do not treat a file's `canonical` label, a symlink, a recent edit, or existence on disk as evidence that the runtime reads it.
- Stop when the requested runtime is reconciled. Route fleet rollout or unrelated stale-surface cleanup separately.

## Workflow

### 1. Start from the named conflict

Read the files, runtime, handoff, or report the user named before searching broadly. Record the exact observed duplication or disagreement.

Identify the actual entry paths that could activate the surfaces, such as:

- global and project instruction files;
- launchers, hooks, sentinels, wrappers, or environment injection;
- session-start and session-end procedures;
- scheduled automation definitions;
- generators, factual-review jobs, and documentation exporters;
- local adapters, manifests, registries, and compatibility links.

Search for exact path and distinctive-content references. Keep historical citations separate from active consumers.

### 2. Establish the active-system and retirement boundary

Before accepting any artifact as authority, classify it using live evidence:

| Class | Meaning |
|---|---|
| activation authority | The procedure or configuration a new runtime is required to execute |
| current state | Rolling continuity, status, or work-in-progress read by the authority |
| generated observation | Report or snapshot derived from other sources; evidence, not control |
| compatibility tombstone | Retired path retained only to redirect old citations safely |
| historical evidence | Old receipt, transcript, commit, or archive that must remain truthful |
| unknown | A surface whose current consumer cannot yet be proven |

Use live wiring, process configuration, consumer code, direct runtime behavior, and current write paths as evidence. Use memory and old reports only as leads.

### 3. Reconstruct why the duplicate persists

Determine both readers and writers.

- Use repository history, blame, timestamps, and generator source to identify origin and latest writer.
- Distinguish a duplicate read from a file that is merely refreshed during closeout.
- Check whether a generated report copied an obsolete declaration back into current documentation.
- Check root/path parity when `/Users/...` and relocated `/Volumes/...` paths may refer to the same or different object.
- Inspect enabled state separately from stored automation definitions. A disabled job can still preserve stale instructions without causing current execution.

Write a short causal chain: `writer -> surface -> consumer -> observed duplicate`. If a link remains inferred, label it.

### 4. Design one authority chain

Assign one function to each retained surface:

```text
runtime entrypoint -> activation authority -> current state
                                      \-> generated observations
retired citations -> compatibility tombstone -> activation authority
```

Require these properties:

- exactly one live activation authority for the runtime;
- current state contains state, not a second startup procedure;
- generated reports describe the chain but do not become part of it;
- retired paths cannot plausibly look live;
- historical records remain unchanged unless they falsely present themselves as current instructions;
- active consumers point directly to the new authority or an explicit compatibility redirect.

Prefer a retirement tombstone over deleting a widely cited legacy path. The tombstone should say that it is retired, name the live authority, and contain no runnable duplicate procedure.

### 5. Claim and implement the complete cutover

Before writing shared surfaces, claim the exact files or directories using the workspace's coordination mechanism. Inventory repository roots, branches, dirty state, and background auto-commit behavior.

Update the complete active slice in one bounded pass:

- canonical authority and current-state pointer;
- runtime injection or sentinel configuration;
- session-end writer or closeout procedure;
- active generators and their generated outputs;
- root-level orientation and compatibility tombstone;
- enabled consumers and stored automation definitions that would revive the legacy path;
- architecture map or handoff only where the change altered durable system truth.

Do not rewrite historical receipts just to remove old path strings. Do not assume a background commit watcher fenced inherited changes; inspect status and commits before and after mutation.

### 6. Add a deterministic authority check

Create or update a focused verifier when the runtime has several consumers. It should fail clearly if any invariant regresses:

1. one and only one canonical activation declaration exists;
2. the activation authority points to the intended current-state surface;
3. current state does not declare itself canonical or contain the full startup procedure;
4. the legacy surface is an explicit tombstone;
5. active launchers, hooks, generators, and enabled automations contain no legacy reference;
6. stored disabled automation definitions are reported separately;
7. relocated/root path relationships match the intended architecture.

Keep policy in this skill and system-specific paths in the verifier. Print concise pass/fail evidence and the exact offending consumer.

### 7. Verify in layers

Keep these evidence layers distinct:

1. **Static proof** — targeted searches, parser checks, diffs, and the deterministic verifier pass.
2. **Injected-context proof** — inspect what the actual runtime bootstrap, hook, or sentinel supplies.
3. **Fresh-runtime proof** — start a genuinely new client or session and confirm it follows only the intended authority.
4. **Scheduled proof** — observe an already-enabled automation when relevant; do not enable one solely for acceptance.
5. **Independent verification** — use a verifier that did not author the change when the repair is broad or high-risk.

A process being alive, a file existing, or a test fixture passing is not fresh-runtime acceptance. Report each completed layer and each layer not exercised.

### 8. Close out without recreating drift

Record:

- the sole activation authority;
- the current-state surface;
- retired/tombstone paths;
- consumers and writers changed;
- static, injected, fresh-runtime, scheduled, and independent proof;
- untouched historical evidence and unrelated dirty files;
- repository commits, push state, and any local-only repository;
- remaining uncertainty or separately authorized next step.

Release claims. Ensure the closeout procedure writes state without reintroducing a second authority declaration.

## Evidence Standard

A successful repair demonstrates all of the following:

- the duplicate mechanism is explained, not merely removed;
- authority follows actual runtime wiring rather than document self-description;
- every retained surface has one named class and function;
- active consumers cannot silently reactivate the retired path;
- a deterministic check guards the invariants;
- a fresh runtime reads the corrected chain once;
- historical evidence and unrelated work remain intact.

## Failure Modes

- **label-as-proof** — trusting `canonical` in a file without proving a consumer reads it
- **reader-only diagnosis** — finding both files but not the writer that keeps refreshing one
- **string-count cleanup** — deleting every legacy path mention, including truthful history
- **tombstone that still runs** — leaving the retired procedure inside the compatibility file
- **generated-authority inversion** — allowing a report or export to control the runtime it describes
- **implementation-session acceptance** — calling the same warmed client a fresh-runtime proof
- **automation activation for proof** — changing enabled state merely to exercise a scheduled path
- **partial cutover** — updating the main file while a hook, generator, or closeout writer still restores the duplicate
- **shared-worktree contamination** — committing inherited changes because an auto-commit watcher raced the repair

## Runtime Notes

### Codex and Claude Code

Use local path inspection, repository history, configuration reads, and focused validators. Open a genuinely fresh task/session for client acceptance when authorized. Preserve the distinction between the global instruction source and project-local overlays.

### Hermes and other managed profiles

Inspect the live profile/config home, not only editable mirrors. Use the supervising runtime's start mechanism and require a proof artifact naming exact files read.

### GPT or browser-managed runtimes

Inspect the live Builder/action/Knowledge surface when available. If direct access is unavailable, route a bounded verification request instead of inferring live state from a manifest export.

## Proven Pattern

This method was extracted from a Codex repair where two session-start files both appeared canonical. The durable fix was not deletion: one file became the sole activation authority, rolling continuity became non-authoritative state, the legacy path became a tombstone, all active writers and consumers were reconciled, a deterministic verifier was added, and a genuinely fresh Codex session proved the new chain.
