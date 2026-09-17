---
name: calibrate-advisory-hook
description: Review recurring advisory-hook alerts, distinguish genuine catches from false positives or insufficient evidence, make authorized narrow tuning changes, and verify recurrence closeout. Use for noisy detector work items; not for disabling safeguards, promoting warnings to blocks, or reviewing every hook.
metadata:
  category: meta
  write_mode: file
  one_line_use: classify and tune one recurring advisory without hiding real catches
  fast_pick: "yes"
---

# Calibrate an advisory hook

Turn one recurring alert into an evidence-backed keep, tune, or authorized-retire decision. Counted alerts are not confirmed failures.

## Entry and boundaries

Start from the named work item and its observation source. Refresh state, ownership, claims, and the installed detector before selecting a slice. Reuse the existing item; do not create a shadow task.

Read the relevant `_shared/Hook_Quality_Bar.md` and `_shared/Detection_Without_Conversion.md` sections before changing detection behavior. Claim the source and affected shared outputs. Review-only authorization permits classification, not editing. Saving or invoking this skill grants no new authority over another actor's protected hooks, credentials, blocking policy, or production logs.

Keep one failure class in scope. A narrow lexical correction does not authorize general detector redesign, historical-log cleanup, a new recurring job, or disabling recurrence reporting. Leave blocking/advisory posture unchanged unless explicitly authorized otherwise.

## Classify before tuning

1. **Bound the evidence.** Record the log path, snapshot cutoff, row count, and selected observation IDs. Use stable event IDs when available; otherwise bind line numbers to the snapshot cutoff. For a sample, state its selection rule and limits. Do not report sampled classifications as a full-corpus error rate.
2. **Inspect safely.** Start with timestamps, counts, hit categories, and schema. Observation contexts can contain credentials or personal data copied from earlier responses. Inspect only needed context through a redacting view; do not print or copy raw log tails. If safe inspection is unavailable, use metadata and mark the classification uncertain.
3. **Separate verdicts.** Classify selected rows as genuine catch, false positive/harmless friction, or insufficient evidence. Attach a short reason and source pointer. Preserve observations; append judgments to the existing calibration surface or a bounded receipt. Do not silently rewrite earlier verdicts.
4. **Check intended meaning.** Compare the detector's condition with current owner documentation. A role name, host name, model identifier, historical explanation, or discussion of the detector may contain the same substring as a real failure without being that failure.
5. **Keep evidence limits visible.** Truncated contexts may omit the actual trigger or an exclusion. Replaying them proves only saved-context behavior. Use an authorized full event or a synthetic paired case to isolate the suspected defect. A retained hit is not automatically a genuine catch.
6. **Trace upstream obligations.** A compliance detector can correctly report a missed requirement that an upstream router created incorrectly. Correlate the observation with the routing event and the relevant turn before deciding which component to tune. A shell keyword search is not automatically equivalent to a required document Read; preserve the documented contract unless changing it is authorized.

## Make the earned change

For **keep**, record why the observed alerts are useful or too uncertain to tune. For **tune**, change only the confirmed false-positive class while retaining positive controls. For **retire**, verify the governing exit condition and authorization; low precision alone does not authorize removing a mandated fence.

Prefer a small regression matrix grounded in behavior:

- a legitimate nearby expression that must not alert;
- the actual prohibited expression that must still alert, including when both occur together;
- relevant historical/model/host variants;
- malformed or absent input under the existing failure contract.

Run the same relevant cases against the pre-change and changed detector when practical. A failing negative control before and passing control after demonstrates the correction; unchanged genuine catches constrain its scope. Do not import the specific regex from an earlier repair without checking this detector's language and payload.

## Verify the consumer without polluting telemetry

Trace `live registration -> command -> resolved artifact -> entry point -> consequence`. Check symlinks, copies, interpreter, working directory, and loaded-process behavior where relevant.

Exercise positive and negative cases at the entry point, checking exit status, advisory/block output, heartbeat, and observation behavior. Route fixture logs to temporary destinations using supported injection or an isolated test harness. Never append synthetic alerts to production observations just to claim live proof.

Distinguish these layers explicitly:

- importing the installed file and calling `main()` with patched destinations is an **installed-artifact fixture**;
- executing the configured command proves the **command boundary**;
- an actual host turn proves the **host invocation**.

Do not label the first as either of the latter. If higher-layer proof is required but would touch protected or live surfaces, preserve the remaining gate. Use `verify-real-invocation-path` for the detailed consumer-proof procedure; independent acceptance remains separate from author tests.

## Close the recurrence, not its visibility

Preserve the original tracking key and the reviewed count/cutoff consumed by the recurrence producer. Use its existing lifecycle operation to close the item only after its acceptance clauses are met. Do not alter counts to suppress future alerts.

Read back terminal state, then exercise the producer's actual eligibility logic: reviewed observations should not immediately recreate the item, while genuinely new observations should remain eligible at the current threshold. A dry-run that merely lists all historical logs is not proof of eligibility behavior.

Record the classification, change, verification layers, remaining uncertainty, and recurrence result. Refresh affected derived views and close owned claims through the current closeout workflow. Keep unresolved implementation or acceptance gates open rather than treating a completed review as a completed repair.

## Local pointers and proven instances

In Ted's workspace, the shared root is `/Volumes/Extra/Substrate`. Work-item authority is the local Control API and `Control/backend/system.db`; the current recurrence implementation is `Operations/scripts/check_recurring_hook_fires.py`. Inspect current code before using its notes parser or threshold; neither is a universal contract.

The WI-1145 example is `Operations/reports/Work_Item_Closeouts/WORK_ITEM_1145_GPT_TERMINOLOGY_REVIEW.md`. Its lexical repair excluded ChatGPT host references and numbered GPT models while retaining standalone GPT/Builder warnings. Five regression tests exercised the installed artifact; saved-context replay covered 12 rows, not the entire log. It did not prove a future interactive Claude turn.

The WI-1144 example is `Operations/reports/Work_Item_Closeouts/WORK_ITEM_1144_ROUTING_COMPLIANCE_REVIEW.md`. The router treated “spending 20 minutes” as financial planning, creating a needless document-reading obligation. The repair changed one pattern in `Operations/config/shared_routing_map.json`; the downstream Stop detector and its Read contract stayed intact. Seven tests in `Operations/tests/test_routing_spending_time.py` exercised the installed prompt/action/Stop artifacts with isolated telemetry, retaining money-spending and mixed time-and-money controls. Of 12 sampled observations, four were false-positive/harmless-friction cases, two were missing-Read signals under the existing contract, and six remained uncertain. This was installed-artifact fixture proof, not a future host-turn observation. Original watermark 722 was preserved despite a 723-row snapshot; the actual recurrence consumer still allowed review at 725.

If these paths or contracts drift, verify their live successor and propose a focused skill correction; do not reconstruct a missing consumer from this example.
