---
name: verify-real-invocation-path
description: Verify a claimed fix, hook, script, service, launcher, integration, or runtime behavior through the exact path the real consumer uses. Use when tests may have bypassed executable permissions, symlinks, launchers, settings wiring, payload contracts, environment selection, service boundaries, installed artifacts, or fresh-client state; when a proxy test such as `python script.py`, an in-process call, a health 200, or a warmed session is being offered as proof that production behavior works; or before accepting confident `verified`, `confirmed`, `tested`, `done`, `complete`, or `working correctly` claims.
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
- **self-acceptance** — the author defines, runs, and accepts the proof without an independent layer where one is required

## Runtime Notes

### Codex and Claude Code

Use filesystem identity, `readlink`/realpath, mode checks, live settings or launch definitions, and direct subprocess probes. Run focused unit tests as a lower layer. Use a fresh task/session only when client acceptance is part of the contract.

### Hermes and managed workers

Resolve the selected profile home, launcher, model/provider configuration, and exact worker command. Gateway health does not prove on-demand worker execution. Return a receipt with the effective profile and command.

### GPT, browser, or connector runtimes

Use the live Builder/action/connector surface or a genuinely fresh conversation. If direct access is unavailable, route a bounded acceptance request instead of accepting exported schemas or local server tests as client proof.

## Update Backstop

This skill deliberately names principles rather than one product's current hook codes or payload schema. When a task depends on a versioned contract, verify the installed version and primary documentation, then record the effective live contract in the task receipt. Update this skill only when the cross-runtime method changes.

## Proven Pattern

This method was extracted after a hook was reported as live-proven through `python3 hook.py` while the real settings invoked it directly and its executable bit was missing. A later completion-claim blocker repeated the risk during implementation: replacing the file cleared its executable mode, and the direct-path test caught the failure immediately. The durable method is the layered comparison—proxy test, exact installed invocation, observable consequence, independent verification, then fresh-client acceptance when required.
