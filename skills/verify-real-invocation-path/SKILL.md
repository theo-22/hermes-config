---
name: verify-real-invocation-path
description: "Verify a claimed fix, hook, script, service, launcher, or integration through the exact path the real consumer uses. Use when a proxy test (in-process call, health 200, warmed session) is offered as proof, or before accepting \"verified\" / \"done\" / \"working correctly\" claims."
metadata:
  category: judgment-only
  write_mode: none
  one_line_use: prove the exact installed consumer path instead of a proxy
  fast_pick: "yes"
---

# Verify Real Invocation Path

Prove the claim at the boundary where the real consumer depends on it. Treat narrower tests as useful layers, never as substitutes for the claimed layer.

## Boundary

- Verification is read-only unless the user separately authorizes repair.
- Start from the exact claim and named consumer. Do not broaden into a system audit.
- Do not manufacture acceptance by enabling disabled jobs, changing production state, spending money, or using protected data.
- Use disposable fixtures or synthetic payloads when they exercise the real invocation mechanism without mutating production content.
- Keep implementation proof, independent verification, fresh-client acceptance, and human settlement separate.

## Workflow

### 1. State the claim as a testable contract

Write one sentence naming:

- the behavior claimed;
- the real consumer;
- the invocation boundary;
- the observable result that would make the claim true.

Example: "Claude Code invokes this executable from its live Stop settings, receives exit `0` plus JSON `decision:block`, and continues with a correction turn."

If the claim is only syntax, importability, or file content, keep it that narrow. Do not silently promote it to runtime behavior.

### 2. Resolve the active artifact and consumer path

Inspect the live wiring before running tests:

- resolve symlinks and aliases;
- identify the active checkout, installed artifact, bundle, container, or profile;
- inspect executable permissions and ownership;
- read the real launcher, settings entry, service definition, hook registration, route, or client configuration;
- identify payload, environment, working-directory, authentication, and exit/output contracts;
- separate active, cached, generated, retired, and historical paths.

Record the chain:

`consumer -> launcher/configuration -> resolved artifact -> dependency/runtime -> observable result`

Every link must be observed or labeled unverified.

### 3. Inventory existing proof by layer

Classify each prior check honestly:

| Layer | Examples | What it proves |
|---|---|---|
| static | parse, compile, grep, config read | structure and declared wiring |
| direct local | execute the artifact itself | local executable behavior |
| installed-path | invoke the exact command/path from live configuration | permissions, resolution, payload, and harness contract |
| service/runtime | call the live route or restarted process | deployed behavior |
| fresh client | new session/client discovers and exercises it | client exposure, caching, and real user path |
| independent | uncommitted verifier repeats the acceptance contract | protection against author self-acceptance |

Never round a completed lower layer up to a higher one.

### 4. Design paired probes

Run at least one negative and one positive probe through the same real boundary.

- **Negative/control:** reproduce the failure shape or use a payload that must be rejected, blocked, or fail visibly.
- **Positive:** use a payload that should pass and confirm normal behavior remains intact.

Keep inputs identical except for the condition under test when practical. Capture command, resolved path, exit status, stdout/stderr or response body, and durable telemetry.

For executable or hook claims, compare proxy and real invocations explicitly. Examples:

- `python3 hook.py` versus the exact executable path configured in the harness;
- importing a function versus the launcher or service calling it;
- direct backend call versus authenticated client route;
- port/health response versus a real workload;
- warmed conversation versus a genuinely fresh client.

A proxy may remain a useful unit test. It does not prove the installed path.

#### Provider API contract drift

When a live provider rejects a request field or response shape, place one regression at
the final serialization boundary immediately before network transmission. Capture the
value-safe outbound body and assert the exact effective field set for the selected model
or endpoint. Mocking the higher-level transport helper can prove downstream handling while
silently preserving the malformed request that caused the incident.

Verify the current contract against primary provider documentation, then keep the layers
separate: serialized-body proof, a real provider canary, installed service deployment, and
fresh affected-client acceptance. A successful direct function canary does not prove a
long-running daemon loaded the new source.

For concurrent fan-out tests, bind simulated results and assertions to stable request
identity (job ID, prompt, correlation ID), not call index or thread arrival order. Scheduler
order is not a behavioral contract; order-dependent fixtures create intermittent failures
and can attribute a failure to the wrong job.

#### Installed UI actions

When the claim concerns visible pending, success, or error feedback, read
[references/ui-action-feedback.md](references/ui-action-feedback.md). Use the
installed browser consumer. If exercising the real failure would require
stopping a healthy service or otherwise disrupting production, control the
browser response instead and label the result as rendered-client proof—not
backend or end-to-end proof.

#### Transaction and checkout closeout

When a helper writes receipts while releasing task resources, read
[references/transaction-closeout.md](references/transaction-closeout.md).
Verify the real API's counting scope, source format, failure ordering, and
terminal resource state; a mock returning zero remaining resources is not proof.

#### Semantic indexes and derived-source freshness

When recent embeddings, equal counts, or a `current` label are offered as proof
that a changing source is discoverable, read
[references/semantic-index-freshness.md](references/semantic-index-freshness.md).
Verify exact source coverage, content and consumer-model embeddings, then probe
real semantic retrieval separately from exact-ID lookup. Include concurrent
source edits and overlapping refreshes when testing freshness publication.

### 5. Check the result, not only the command

Require the observable consequence named in the contract:

- a blocker actually prevents stop or mutation;
- a service performs the real workload, not merely returns health;
- a file lands at the consumer-visible path with correct mode and content;
- telemetry distinguishes "invoked with no hit" from "never invoked";
- a fresh client exposes and calls the capability;
- rollback or unaffected behavior still works.

If transport status, logs, UI state, and durable receipts disagree, report each layer rather than choosing the convenient one.

### 6. Use independent verification when the claim is consequential

Give the verifier the artifacts and acceptance contract, not the implementer's conclusion. Ask it to rerun the real-path probes read-only and return exact commands/results plus defects.

Independent verification does not replace fresh-client or human acceptance when those are separate gates.

### 7. Return an evidence-layered verdict

Report:

- exact claim;
- active consumer chain and resolved paths;
- proxy checks run and their limited meaning;
- real-path negative and positive results;
- telemetry or durable receipt;
- independent verdict, if used;
- completed evidence layers;
- still-pending layers and their exact acceptance step;
- files changed, if repair was separately authorized.

Use `PASS`, `PARTIAL`, or `FAIL`. A lower-layer pass with fresh-client proof still pending is `PARTIAL`, not complete.

## Repair Loop When Independent Acceptance Contradicts Green Tests

Use this loop when an uncommitted verifier exercises the real consumer and a
locally green implementation fails.

1. **Adopt the observed verdict immediately.** Mark the claimed layer `FAIL` or
   `PARTIAL`; do not defend the implementation from its own tests.
2. **Reproduce the verifier's exact boundary.** Preserve the command, payload,
   client/session state, cwd, environment, fixture size, installed path, and
   observable consequence. Read durable telemetry before changing code.
3. **Compare preview state with execution state.** Look especially for hidden
   differences in cwd, inline `cd`, shell expansion, symlink resolution,
   authentication, cached schemas, environment variables, and target counts.
4. **Audit the verifier harness too.** A threshold test must create a
   threshold-sized fixture and pass its cwd explicitly. Correct a
   context-dependent harness without weakening its acceptance contract or
   converting a real miss into a pass by changing expectations.
5. **Repair the smallest demonstrated mechanism.** Add the independent phrasing
   as a regression, plus one neighboring negative control. Preserve the
   original safety boundary; do not broaden fail-closed behavior merely to make
   the score green.
6. **Rerun three layers:** focused implementation tests, the independent sweep,
   and the exact installed-path probe that failed. Confirm the real-world
   consequence (for example, no files changed), not only the exit code.
7. **Return to the verifier and human gate.** Report the root cause, changed
   contract, exact evidence, and remaining acceptance action. The repair author
   does not retroactively become the independent verifier or human acceptor.

Treat an independently authored sweep as a durable regression asset when it is
self-contained and exercises the real boundary. Tests written solely from the
implementer's model of the code remain useful unit proof, but they are not an
independent acceptance layer.

## Evidence Standard

A `PASS` requires:

1. the tested artifact is the one the consumer actually resolves;
2. invocation matches the consumer's command, permissions, environment, payload, and output contract;
3. a negative probe catches the target failure;
4. a positive probe preserves legitimate behavior;
5. the claimed observable result occurs;
6. telemetry or a receipt proves the mechanism ran;
7. every acceptance layer named by the task is completed.

## Failure Modes

- **interpreter bypass** — `python script.py` hides a missing executable bit in a directly invoked hook
- **stale checkout proof** — tests run against a mirror or retired path rather than the installed artifact
- **declaration-as-wiring** — a settings string exists, but the consumer never loads or calls it
- **health-as-workload** — process, port, or HTTP 200 is reported as functional behavior
- **in-process shortcut** — direct function calls bypass launcher, authentication, serialization, environment, or transport
- **warmed-client acceptance** — the implementation session is presented as a genuinely fresh client
- **success-code fixation** — exit status passes while stdout, durable state, or user-visible consequence is wrong
- **telemetry ambiguity** — no observations is treated as no defects without proving the detector ran
- **stale self-test roster** — paired fixtures stay green against retired or unregistered targets while the live configured consumer is untested; derive the exercised target set from current configuration and fail on any configured target without a contract fixture
- **self-acceptance** — the author defines, runs, and accepts the proof without an independent layer where one is required
- **mock-overclaim** — a controlled browser response proves client rendering, but is reported as proof that the backend or service performed the action

## Runtime Notes

### Codex and Claude Code

Use filesystem identity, `readlink`/realpath, mode checks, live settings or launch definitions, and direct subprocess probes. Run focused unit tests as a lower layer. Use a fresh task/session only when client acceptance is part of the contract.

### Hermes and managed workers

Resolve the selected profile home, launcher, model/provider configuration, and exact worker command. Gateway health does not prove on-demand worker execution. Return a receipt with the effective profile and command.

### GPT, browser, or connector runtimes

Use the live Builder/action/connector surface or a genuinely fresh conversation. If direct access is unavailable, route a bounded acceptance request instead of accepting exported schemas or local server tests as client proof.

For installed browser UI actions, use the controlled-response method in
[references/ui-action-feedback.md](references/ui-action-feedback.md) when a
safe real action cannot exercise every visible branch.

## Update Backstop

This skill deliberately names principles rather than one product's current hook codes or payload schema. When a task depends on a versioned contract, verify the installed version and primary documentation, then record the effective live contract in the task receipt. Update this skill only when the cross-runtime method changes.

## Proven Pattern

This method was extracted after a hook was reported as live-proven through `python3 hook.py` while the real settings invoked it directly and its executable bit was missing. A later completion-claim blocker repeated the risk during implementation: replacing the file cleared its executable mode, and the direct-path test caught the failure immediately.

The contradiction-repair loop was added after 19 implementer-authored tests
passed while a fresh Claude Code command rewrote 11 disposable files. Telemetry
showed the guard previewed the session cwd while Bash executed after an inline
`cd`; the independent sweep also depended on incidental cwd contents. Repairing
both the runtime cwd model and the sweep's fixture produced 25 focused passes,
a self-contained 15/15 sweep, and an installed-path block of the exact failed
command, while human acceptance remained separate. The durable method is the
layered comparison—proxy test, exact installed invocation, observable
consequence, independent contradiction repair, then fresh-client and human
acceptance when required.
