---
name: trace-claim-evidence
description: Trace and independently challenge a concrete state, count, completion, implementation, or capability assertion against the evidence boundary that existed when it was stated. Use when designing or reviewing claim detectors, running an external check of another actor's fix or measurement, replaying known wrong assertions, auditing AI reports against tool transcripts, separating a real core defect from an inaccurate submitted count or explanation, deciding whether evidence supports a claim, or evaluating whether a watch-only detector has earned promotion. Do not use it to repair the reviewed implementation unless repair is separately authorized.
metadata:
  category: judgment-only
  write_mode: none
  one_line_use: attribute and adversarially replay each assertion against its exact evidence boundary
  fast_pick: "yes"
---

# Trace Claim Evidence

Evaluate assertions in event order. A tool call is context; only its available result can support a claim.

## Boundary

- Treat the current transcript, trace, logs, files, or live runtime as evidence authority for the bounded claim.
- Keep this read-only unless the user separately authorizes detector, ledger, or runtime changes.
- Treat the submitted report as claims under review, not as a briefing or test plan to inherit.
- Do not convert watch-only evidence into blocking policy. Promotion requires separate authority and calibration.
- Keep implementation proof, independent reproduction, fresh-client evidence, and human settlement distinct.

## Workflow

### 1. Define one claim unit

Extract the smallest consequential assertion containing:

- the specific named object;
- the decisive predicate or state;
- the claimed value, count, scope, or completion status.

Preserve the original words. Split compound statements when their evidence differs.

Examples:

- object: `_stage_write_guard`; claim: `one insertion covers thirteen tools`
- object: `settings.json`; claim: `the harness blocks editing it`
- object: `three work items`; claim: `all three remain open`

Skip questions, clearly marked hypotheses, and statements whose uncertainty is explicit unless the task is to audit that uncertainty itself.

### 2. Reconstruct event order

Read every assistant text block, including intermediate commentary before later tool calls. For each assertion, establish its exact position among:

1. user input;
2. assistant text;
3. tool invocation;
4. tool result;
5. later correction or final response.

Credit only evidence whose result was available before the assertion. Later evidence may correct the claim; it cannot retroactively support what was already said.

### 3. Attach the evidence-producing call

Record the closest relevant prior call with:

- tool name and call ID when available;
- exact target, query, path, command, or endpoint;
- success/error state;
- bounded result excerpt or structured value;
- subject overlap or mismatch.

If no call is relevant, still preserve the nearest prior call when it explains the failure shape. Mark it irrelevant rather than omitting it. This makes "a tool ran, but it did not support this assertion" inspectable.

### 4. Classify support conservatively

Use exactly one support status:

- `supported` — the prior result directly establishes the named object and decisive state/count.
- `contradicted` — the prior result directly conflicts with the assertion.
- `not_established` — evidence is absent, failed, about another subject, too weak, or requires an inference the result does not earn.

Allow `not_established`. Do not force uncertainty into supported or contradicted.

Subject overlap is relevance, not entailment. Matching a filename, number, or tool name is insufficient unless the result establishes the claimed relationship.

### 5. Run independent external-check mode when another actor submitted the claims

Use this mode for a fix report, counter result, detector claim, implementation receipt, or evidence-bearing handoff.

#### Freeze the evidence boundary

Before replaying anything, record the immutable slice being judged:

- exact commit and parent, or before/after artifact hashes;
- exact session, transcript, run, or receipt identity;
- time range, row range, event IDs, and current row count where available;
- relevant configuration, installed path, and consumer state;
- whether the underlying source can continue changing while the review runs.

If a transcript or log is mutable, judge the submitted claim against the pinned slice first. Report observations from the larger current file separately. A later row must not silently change the verdict on an earlier evidence claim.

#### Write the falsification matrix first

For every material claim, record:

```text
claim_id
claim_as_submitted
what_would_refute_it
author_evidence_boundary
independent_check
verdict
evidence_anchor
correction_or_limit
```

Use the requester's verdict vocabulary. The default is `CONFIRMED`, `REFUTED`, or `UNCERTAIN`. Use `UNCHECKABLE` only when the request permits it; otherwise explain the missing prerequisite under `UNCERTAIN`.

Start with the cheapest plausible falsifier. Do not begin by reproducing the author's preferred happy path.

#### Replay and independently reconstruct

Run both of these when feasible:

1. replay the author's stated method at the frozen boundary;
2. reconstruct the result independently from the underlying events, repository history, filesystem, runtime, or consumer.

Triangulate across distinct evidence surfaces when the claim permits it:

- artifact or code behavior;
- ordered runtime, transcript, log, or tally evidence;
- an independent side channel such as git history, filesystem state, receipt identity, installed consumer behavior, or capability probing.

Do not count two views of the same derived artifact as independent evidence.

#### Test identity, association, and denominator

For any count or rate, verify:

- which session, run, actor, and time window each row belongs to;
- whether the unit is events, unique targets, assertions, sessions, or files;
- whether duplicate observations are intentionally deduplicated;
- whether the denominator excludes unobserved or unclassifiable cases;
- whether a tally row actually belongs to the transcript slice being cited.

Hand-inspect representative positives, negatives, boundary cases, and apparent misses. A correct core phenomenon does not make an incorrect number exact.

#### Probe the rule's real semantic width

Compare the prose claim with what the implementation can actually recognize. Test likely blind spots such as:

- relative paths, variables, aliases, and dynamically constructed targets;
- operations or tools omitted by a string or regex classifier;
- quoted fixtures, documentation, or test data that resemble live events;
- ambiguous zeroes that could mean either "no defect" or "detector did not run";
- capability exclusions inferred from folder labels instead of the actor's actual access;
- thresholds calibrated before the sensor's recall and precision are known.

For capability claims, probe the live actor/tool boundary for each disputed path when safe. A directory name or role label is not capability proof.

#### Separate the verdict layers

Report these independently:

1. whether the underlying defect or behavior is real;
2. whether the submitted implementation fixes or detects it at the claimed boundary;
3. whether the submitted numeric count and event association are exact;
4. whether the proposed threshold or policy is calibrated well enough to adopt.

An exact claim can be `CONFIRMED` with a stated correction only when the correction does not meet the requester's falsifier condition. Otherwise mark it `REFUTED` or `UNCERTAIN` even if the broader concern is valid.

### 6. Keep human outcome separate

Machine support status describes the evidence relationship. Human calibration describes whether the detector helped.

Use these review labels when the detector vocabulary matches the live system:

- `true_catch` — it surfaced a consequential unsupported or contradicted assertion.
- `harmless_friction` — technically unsupported, but surfacing it added no useful protection.
- `false_alarm` — the assertion was supported, not actually asserted, or outside the detector's stated failure class.

Key verdicts by a stable observation ID in an append-only ledger. Let the latest valid verdict be effective while retaining review history.

### 7. Decide whether promotion is earned

Before recommending stronger enforcement, require all of:

- heartbeat proof that the detector actually runs;
- stable IDs and complete human labels for the review window;
- replay of every known motivating failure;
- paired supported controls through the same boundary;
- low false-alarm and harmless-friction rates at the proposed escalation rung;
- fail-safe behavior and an explicit non-retroactive boundary;
- independent reproduction and any named fresh-client or human gate;
- explicit authority for the policy change.

Fire count proves liveness, not calibration. Green fixtures prove the implementation's model, not real-world precision.

## Evidence Standard

A satisfactory trace contains:

```text
assertion_id
assertion_text
named_object
decisive_claim
assertion_position
evidence_tool_call
evidence_target
evidence_result_excerpt
evidence_position
support_status
support_reason
human_label or pending-review state
source_pointer
```

Return `PASS`, `PARTIAL`, or `FAIL` for the evidence layer being reviewed. A working watch-only detector with unmeasured live precision is `PARTIAL`, not accepted for blocking.

For an external check, also return:

- one anchored verdict per submitted claim;
- corrections and limitations beside the affected verdict, not buried in prose;
- an overall disposition such as `leave as-is`, `needs change`, or `revert`;
- the exact artifact, hook, counter, or policy that disposition applies to;
- untested surfaces and why they remain untested.

## Failure Modes

- **final-text-only scan** — misses wrong claims emitted in intermediate commentary.
- **retroactive evidence credit** — treats a later check as support for an earlier assertion.
- **tool-presence fallacy** — assumes any successful call clears every claim in the turn.
- **target-match fallacy** — assumes mentioning the same object proves the predicate or count.
- **forced binary** — converts insufficient evidence into true or false instead of `not_established`.
- **unlabelled observation pile** — accumulates fires with no calibration truth.
- **fixture self-acceptance** — promotes from implementer-authored replays without ordinary-use or independent evidence.
- **policy creep** — turns a tracing method into a blocker without explicit authorization.
- **mutable-boundary drift** — evaluates a growing transcript or log without pinning the submitted row/time slice.
- **core-truth rounding** — treats a real underlying defect as proof that the submitted count, association, or explanation is exact.
- **derived-view triangulation** — calls two renderings of the same derived data independent evidence.
- **unit confusion** — mixes events, unique targets, assertions, files, or sessions in one count.
- **semantic-width mismatch** — accepts broad prose while the classifier recognizes only a narrow literal form.
- **zero-as-success** — treats an empty result as clean without proving the detector ran and could observe the target.
- **premature thresholding** — tunes policy around a sensor whose recall, precision, or exclusions are still unknown.

## Runtime Notes

### Local transcript runtimes

Preserve block order and tool-result timing. Pin mutable transcript slices by stable row/event identity when available. Resolve installed hooks or launchers through their actual configuration before claiming runtime proof. Keep deterministic transcript parsing in actor-local adapters when formats differ.

### GPT or connector runtimes

If the runtime does not expose ordered tool/result history, return the bounded claim and exact missing evidence. Route a verification request instead of pretending the assertion was traceable.

### Detector implementations

Keep fires/liveness, assertion observations, and human outcomes as distinct surfaces. Do not fork the evidence standard inside actor-local code.

## Update Backstop

When a transcript schema, hook boundary, tool-result contract, or outcome vocabulary changes, verify the live consumer and update this canonical skill before adapting local parsers. Do not silently weaken chronology or the promotion gate.

## Provenance

Extracted from Codex work item #333 on 2026-08-11. The live build caught the key design defect that a Stop-boundary scanner must inspect intermediate assistant text and must not credit evidence produced after the assertion. Source receipt: `/Volumes/Extra/Substrate/Operations/reports/Codex_Work_Item_333_Claim_Evidence_Detector_Receipt_2026-08-11.md`.

Independent external-check mode was added after replaying the Bash sole-path counter report on 2026-08-25. The review confirmed the underlying sole-path-overwrite defect but refuted or limited several submitted measurement claims because the evidence mixed transcript slices, event units, semantic coverage, and capability assumptions. Source return: `/Volumes/Extra/Substrate/_AI_Inbox/external_check_sole_path_counter_fix_RESPONSE_CODEX_2026-08-25.md`.
