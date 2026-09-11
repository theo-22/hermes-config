---
name: diagnose-codex-hook-liveness
description: Distinguish Codex hook execution failure from hook-script or heartbeat-recording failure by tracing the installed CLI and desktop consumers and running paired trust-enforced and one-invocation controls. Use for configured hooks that produce no expected events or telemetry; do not use it as authorization to change trust or hook configuration.
metadata:
  category: judgment-only
  write_mode: none
  one_line_use: isolate Codex hook execution from heartbeat recording failure
  fast_pick: "no"
  version: 1.1.0
  platforms: [macos]
  tags: [codex, hooks, liveness, trust, verification]
---

# Diagnose Codex Hook Liveness

Determine whether the installed Codex consumer suppresses hooks before launch or launches them and then loses their expected observable consequence.

## When to use

Use when Codex hook registrations exist but expected `hook_started` / `hook_completed` events, heartbeat rows, or hook effects are absent or disputed.

## When not to use

- Do not use for authoring a new hook; use the hook-creation workflow.
- Do not infer permission to approve hashes, edit configuration, restart applications, or repair matchers. Diagnosis and repair are separate authority boundaries.
- Do not treat a direct script invocation as proof that the installed hook consumer invokes it.

## Canonical workflow

1. **Pin the consumers.** Resolve the actual CLI executable, version, `CODEX_HOME`, and the live desktop/app-server command line. Establish whether CLI and desktop share the same binary and configuration rather than assuming they do.
2. **Pin the loaded registry.** Start a fresh installed app-server process and use its supported hooks inventory method. Record registration count, enabled state, trust state, current hash, persisted trusted hash, warnings, and errors. Compare canonical paths by inode and digest when aliases or symlinks are involved.
3. **Pin the actual event envelope.** Capture the consumer's real event and tool-input shape before judging matcher reach. Current Codex freeform patches carry patch text in `tool_input.command`; fields such as `patch`, `input`, or `cmd` are not interchangeable evidence. Desktop dispatch may also omit the prompt-state artifact produced by CLI, so distinguish missing prompt-state capture from missing user intent in the same session transcript.
4. **Choose observable consequences.** Identify one or more hook events with durable, attributable effects, such as session-keyed heartbeat rows. Capture exact pre-probe counts and the tail fields needed to match a new row to one probe session. Count executions by one canonical command identity as well as by log rows: overlapping matcher groups can invoke the same hook twice for one operation.
5. **Run the trust-enforced control.** Invoke the installed CLI normally with a unique, no-tool prompt. Record hook event output and post-run counts. This is the ordinary-path observation, not automatically a negative case.
6. **Run a one-invocation execution control when authorized.** Repeat the same prompt shape and working directory with the runtime's ephemeral hook-trust bypass. Never persist bypass or trust changes. Record hook starts/completions and exact row deltas, including the probe session ID.
7. **Classify the failing layer.** Use the evidence table below; do not leap from “no heartbeat” directly to “broken hook.”
8. **Propose, but do not silently implement, the narrowest layer-specific repair.** Preserve a separate gate for event/matcher reach, especially when CLI and desktop differ in tool envelope or prompt-state capture.

| Ordinary run | One-run execution control | Heartbeat/effect | Classification |
|---|---|---|---|
| no hook events | hook events present | matching effect present | execution is gated before launch; script and recorder work |
| hook events present | not needed | matching effect absent | hook launches; investigate script, payload, permissions, or recorder |
| no hook events | no hook events | no effect | loader/event/registry path remains suspect; bypass did not discriminate |
| hook events present | not needed | matching effect present | checked event is live; investigate a narrower matcher/event or attribution problem |

## Repair selection

Match the proposal to the proven failing layer:

- If current handlers are enabled but `modified` or `untrusted`, propose refreshing only the exact runtime-returned trust key/hash pairs through the supported review/config surface. Do not rewrite the registry or scripts to solve a trust mismatch.
- If hooks launch but effects fail, diagnose the invoked script with the exact hook payload and runtime environment. Preserve the installed-consumer proof requirement after any repair.
- If one event works but a write boundary does not, compare the actual top-level tool name and envelope against the matcher. For freeform patches, inspect `tool_input.command`. Treat matcher adaptation as a separate change from trust or recorder repair.
- If one operation produces duplicate records, inspect matcher-group overlap before proposing log deduplication. One operation should reach one canonical guard identity; structural registration overlap is different from two model attempts.
- If desktop lacks CLI prompt-state capture, prove whether same-session transcript input still carries the bounded user or delegation instruction. A transcript fallback is a separately authorized repair candidate and must exclude injected developer, plugin, and environment text.

## Verification contract for an authorized repair

Require both positive and negative evidence:

1. Fresh inventory readback shows the intended registrations enabled and trusted with zero warnings/errors.
2. CLI control trio: one authorized write must succeed with one attributable guard record, one instruction-forbidden write must be blocked with its real target and text visible, and one ordinary read must succeed without invoking the write guard.
3. Desktop control trio: after restart/reload, a fresh desktop task must pass the same authorized-write, instruction-forbidden-write, and ordinary-read controls with same-session attribution. CLI success does not prove desktop acceptance, and desktop prompt-state omission is not grounds to skip the forbidden-write control.
4. When trust gating is the diagnosed layer, pair the ordinary run with one ephemeral hooks-disabled or execution-bypass control appropriate to the installed interface; persist no trust or bypass change beyond the authorized repair.
5. Matcher identity check: each tested write produces exactly one execution of the intended guard identity. A nonmatching or ordinary-read envelope produces none.

## Evidence standard and stop condition

A diagnosis is complete only when one layer is positively demonstrated while the competing layer is controlled, or when the remaining ambiguity is stated precisely. Report executable paths, versions, registry/trust summary, exact before/after counts, session attribution, and the proposed repair boundary.

Stop at diagnosis when the user requested diagnosis only. Do not create child work, mutate trust, edit hooks, or restart the desktop unless separately authorized.

## Failure modes

- Counting configured or enabled handlers as executable without reading trust status.
- Proving a script directly and calling the hook path live.
- Using a bypass result without a normal paired control.
- Crediting unrelated ambient log growth instead of matching the probe session.
- Treating CLI proof as desktop proof.
- Treating desktop prompt-state absence as absence of a current instruction without checking same-session transcript evidence.
- Reading freeform patch text from a legacy field instead of the current `tool_input.command` envelope.
- Deduplicating logs after execution instead of removing an overlapping matcher registration that invokes the guard twice.
- Combining trust refresh, matcher adaptation, and script changes into one repair.

## Runtime notes

On macOS, use process inspection plus the installed CLI's doctor/version output to locate the desktop and CLI consumers. Prefer a fresh app-server protocol client for inventory over static config parsing. Tool names and protocol methods can change; inspect the installed interface rather than copying version-specific names from an old receipt.

## Provenance and update backstop

Extracted from the paired installed-runtime proof recorded in `/Volumes/Extra/Substrate/Operations/reports/WORK_ITEM_1706_ADMISSION_18_HOOK_STARTUP_RE_CREEP_ASSESSMENT_2026-09-10.md` and the CLI-plus-desktop repair acceptance in `/Volumes/Extra/Substrate/Operations/reports/WORK_ITEM_1706_CODEX_GUARDRAIL_REPAIR_2026-09-11.md`. Revalidate protocol method names, trust fields, payload fields, and diagnostic flags against the installed Codex version whenever they drift.
