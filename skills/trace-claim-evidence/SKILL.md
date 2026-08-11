---
name: trace-claim-evidence
description: Trace a concrete state, count, completion, or capability assertion to the exact evidence available before it was stated, then separate machine support status from human calibration outcome. Use when designing or reviewing claim detectors, replaying known wrong assertions, auditing AI reports against tool transcripts, deciding whether evidence supports a claim, or evaluating whether a watch-only detector has earned promotion.
metadata:
  category: judgment-only
  write_mode: none
  one_line_use: attribute each assertion to the evidence available when it was stated
  fast_pick: "yes"
---

# Trace Claim Evidence

Evaluate assertions in event order. A tool call is context; only its available result can support a claim.

## Boundary

- Treat the current transcript, trace, logs, files, or live runtime as evidence authority for the bounded claim.
- Keep this read-only unless the user separately authorizes detector, ledger, or runtime changes.
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

### 5. Keep human outcome separate

Machine support status describes the evidence relationship. Human calibration describes whether the detector helped.

Use these review labels when the detector vocabulary matches the live system:

- `true_catch` — it surfaced a consequential unsupported or contradicted assertion.
- `harmless_friction` — technically unsupported, but surfacing it added no useful protection.
- `false_alarm` — the assertion was supported, not actually asserted, or outside the detector's stated failure class.

Key verdicts by a stable observation ID in an append-only ledger. Let the latest valid verdict be effective while retaining review history.

### 6. Decide whether promotion is earned

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

## Failure Modes

- **final-text-only scan** — misses wrong claims emitted in intermediate commentary.
- **retroactive evidence credit** — treats a later check as support for an earlier assertion.
- **tool-presence fallacy** — assumes any successful call clears every claim in the turn.
- **target-match fallacy** — assumes mentioning the same object proves the predicate or count.
- **forced binary** — converts insufficient evidence into true or false instead of `not_established`.
- **unlabelled observation pile** — accumulates fires with no calibration truth.
- **fixture self-acceptance** — promotes from implementer-authored replays without ordinary-use or independent evidence.
- **policy creep** — turns a tracing method into a blocker without explicit authorization.

## Runtime Notes

### Local transcript runtimes

Preserve block order and tool-result timing. Resolve installed hooks or launchers through their actual configuration before claiming runtime proof. Keep deterministic transcript parsing in actor-local adapters when formats differ.

### GPT or connector runtimes

If the runtime does not expose ordered tool/result history, return the bounded claim and exact missing evidence. Route a verification request instead of pretending the assertion was traceable.

### Detector implementations

Keep fires/liveness, assertion observations, and human outcomes as distinct surfaces. Do not fork the evidence standard inside actor-local code.

## Update Backstop

When a transcript schema, hook boundary, tool-result contract, or outcome vocabulary changes, verify the live consumer and update this canonical skill before adapting local parsers. Do not silently weaken chronology or the promotion gate.

## Provenance

Extracted from Codex work item #333 on 2026-08-11. The live build caught the key design defect that a Stop-boundary scanner must inspect intermediate assistant text and must not credit evidence produced after the assertion. Source receipt: `/Volumes/Extra/Substrate/Operations/reports/Codex_Work_Item_333_Claim_Evidence_Detector_Receipt_2026-08-11.md`.
