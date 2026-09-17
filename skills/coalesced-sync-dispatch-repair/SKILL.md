---
name: coalesced-sync-dispatch-repair
description: Repair a demonstrated duplicate or retry re-entry in a long-running synchronous worker dispatch path by coalescing identical in-flight calls while preserving claim mutual exclusion. Use when a live trace shows an overlapping retry reaches the same claim owner; do not use for generic claim redesign, completed-result caching, or an unproven transport symptom.
metadata:
  category: judgment-only
  write_mode: file
  one_line_use: coalesce identical in-flight synchronous dispatches without weakening claims
  fast_pick: "yes"
---

# Coalesced synchronous dispatch repair

Use this skill when a long-running synchronous entry point can be re-entered while its original execution is still active. The repair belongs at the demonstrated dispatch boundary: the first caller owns one underlying execution, and an identical overlap adopts that execution instead of reaching the claim layer again.

## When to use

- Live claim history shows an original call still running and a later same-identity call blocked by that original claim.
- The affected synchronous wrappers and the underlying single claim owner are identified.
- The implementation scope and exact files are authorized.

## When not to use

- Do not weaken claim mutual exclusion or make claims generally re-entrant.
- Do not rename targets to evade collisions.
- Do not add a completed-result cache unless separately authorized and designed.
- Do not broaden from demonstrated wrappers to every dispatch or verification path without evidence.
- Do not treat an HTTP timeout alone as proof of duplicate invocation; preserve it as a transport limitation until claim/receipt evidence connects it to re-entry.

## Canonical procedure

1. Establish the failure from live evidence. Read the owning wrapper, the underlying claim owner, claim audit rows, and durable worker receipts. Distinguish the original execution from the duplicate caller's response.
2. Define a deterministic fingerprint from normalized inputs that materially identify the dispatch. Include the wrapper identity and every effective `run_cycle` input that can change the work, actor, target, model, grant, TTL, timeout, or prompt. Normalize only equivalent representations.
3. Add a process-local in-flight registry keyed by the fingerprint and the current event loop or runtime identity. The first caller creates one asynchronous task for the underlying blocking execution.
4. Make overlapping identical callers await the existing task through `asyncio.shield` or an equivalent cancellation boundary. Cancellation or transport loss for one waiter must not cancel the shared execution.
5. Remove the registry entry when the shared task reaches terminal completion, deleting only if the registry still points to that exact task. Retrieve unobserved exceptions so a disconnected final waiter does not hide failures.
6. Keep different fingerprints independent. They must still reach genuine claim conflicts when their targets or effective work collide.
7. Keep result handling immutable across waiters. If a wrapper adds metadata, return a copy instead of mutating the shared terminal result.

## Regression proof

Add focused tests for every affected wrapper that prove:

- identical overlapping calls invoke the underlying cycle once and receive the same terminal result;
- materially different inputs invoke independently;
- one waiter's cancellation does not cancel the shared task;
- success and failure both clean the registry, and a later call starts fresh;
- the existing terminal-result preservation behavior still passes.

Capture a pre-fix failing overlap assertion when practical. Run the focused suite from the owning module directory with its required import path, then compile/lint the changed files and inspect the diff.

## Live acceptance

After tests pass, reload or restart the actual runtime and verify the installed consumer path. From a genuinely fresh role/client activation, run two separate standalone calls on initially free disposable or ordinary targets. For each call preserve:

- target-free preflight;
- one coherent claim acquisition;
- actual worker start;
- terminal PASS/PARTIAL/FAIL/UNKNOWN result;
- durable receipt;
- clean claim release;
- no same-actor blocked event.

Use fresh targets for stability. A connector timeout is not a terminal success claim: inspect the original receipt and claim audit, disclose the timeout, and keep the acceptance specimen excluded unless the required terminal result is observable. A retry after the registry entry is cleaned may legitimately start a new execution; this skill does not cache completed results.

## Closeout

Report the exact source files, regression commands and results, runtime reload, live targets, claim IDs and audit events, receipt paths, terminal results, and any transport or harness limitations. Close the gap only after the required live specimens pass. Release implementation checkouts and record the result on the owning Operations surface.

## Runtime notes

Codex can use the local owning-directory tests, launchd/service inspection, Control claims APIs, and installed MCP connector. Other runtimes should preserve the same evidence layers and adapt only the commands or transport tools; do not create a parallel proof standard.
