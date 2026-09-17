---
name: verify-curator-return
description: "Process what a live verifying actor (Map Curator, or any actor with reach CC lacks) reports back — read raw state not the verdict, apply corrections including ones rejecting CC's own work, separate what they fixed from what only CC can reach. Use right after such an exchange. Not for running the exchange itself."
metadata:
  status: active
  category: judgment-only
  write_mode: file
  one_line_use: read the verifier's raw state, don't just file the verdict
  fast_pick: "no"
---

# Verify Curator Return

A verifying actor's report is a finding, not a receipt. This skill is the discipline for the receiving side of a live exchange — what CC does with what comes back, after `live-multi-actor-negotiation` or `live-surface-verification` has already run.

**Built 2026-07-29** from three identical runs on 2026-07-28 against Map Curator (24 CC-authored Transition edges verified: 9 confirmed, 11 corrected, 4 rejected). Full account: [project_2026_07_28_live_actor_to_actor_and_buoyancy_reread.md](/Users/ted/.claude/projects/-Users-ted/memory/project_2026_07_28_live_actor_to_actor_and_buoyancy_reread.md). No prior skill covered this — `live-surface-verification` covers verifying *disputed* state, `live-multi-actor-negotiation` covers running the exchange. Neither says what to do with the answer.

## Why this exists

Ted's standing rule already covers reports generally: [feedback_review_reports_on_read](/Users/ted/.claude/projects/-Users-ted/memory/feedback_review_reports_on_read.md) — apply judgment to any report in `Operations/reports/`, don't just acknowledge it. This skill is the same discipline sharpened for one specific, higher-stakes case: **a report that comes from a different actor, about CC's own prior work, delivered live.** The temptation there is different from a routine health report — it's easier to skim past a correction to your own claim than a red flag in a health check.

## Core rule

The verifier is only useful if it reports raw state, not a verdict. Mirror that discipline on the receiving side: read the raw rows it touched, not just its summary sentence.

## Workflow — five steps, run every time

1. **Read the report, then read the live rows.** Never accept the account at face value. The verifier's own usefulness came from reporting raw state (`event_count: still 3, updated_at unchanged`) rather than a conclusion — do the same check back on what it changed. Pull the actual node/edge/row it touched and confirm the report matches the live state, not just that the report sounds right.

2. **Apply its verdicts, including the ones that reject your own work.** In the worked instance the verifier rejected two CC-authored edges and downgraded a third. Rejecting your own prior proposal on the verifier's reading is the point of having asked — don't quietly keep the rejected version live, and don't relitigate the rejection without new evidence.

3. **Correct the attribution, don't rewrite the event.** If the write path stamps the verifier's operations under the wrong actor (e.g. a shared `ted_local` default because the connection carries no role), append a correction note — never edit or overwrite the original event. The verifier asked for exactly this shape; preserve its record as it made it, add the correction alongside.

4. **Separate what it changed from what only CC can reach.** The verifier's diagnosis can be right while the actual repair sits in a layer only CC can touch — an endpoint, a schema, a process restart, a config file. Its report is a finding, not a work order: don't treat "verifier flagged it" as "verifier fixed it." List what still needs a CC-side fix and do those before the next round, not after.

5. **Catch the claims it corrected in prose, not just the structural ones.** A verifier can correct a *relation type* (easy to spot — it's a diff) or correct something CC *asserted in a note* (easy to skim past — it's a sentence, not a diff). In the worked instance the verifier twice corrected prose claims CC had written: that a rising catch-rate implies a falling claims-gap, and that a metric depended on buoyancy. Prose corrections are worth more than relation corrections and are the ones most likely to get missed — read every sentence the verifier disagreed with, not just every edge it relabeled.

## When an earlier verifier timed out

A timeout is not FAIL and must not be rounded up to PASS. Preserve each timed-out attempt and its `UNKNOWN` verdict as historical evidence. If the implementation and live specimen already exist, do not rerun implementation merely to obtain a verdict; a later independent actor may instead inspect the current implementation, tests, original E2E receipts, and live claim rows, then issue a new explicit terminal PASS or FAIL.

Treat the later verdict as a separate event:

- read the new receipt and its claimed live rows rather than accepting its summary;
- require evidence for every still-open acceptance condition and confirm the verifier did not silently broaden scope or rerun implementation;
- link the new receipt without rewriting the timed-out attempts;
- advance `verification_pending → verified → accepted` only for a concrete PASS through the authoritative lifecycle; and
- close the work item and archive its intake separately through their canonical lifecycle, with read-back and zero item-specific exceptions.

Work item #1347 is the bounded example: automatic verifier claims `5333` and `5334` remained `worker_timeout / UNKNOWN`; a later Audit direct inspection supplied a distinct terminal PASS, after which the orchestration and work item closed without another implementation run or any change to predecessor #957.

## Also encode

- **If the verifier reports a defect in a tool CC owns, fix it before the next round** rather than working around it in the current one. A verifier that has to route around the same bug twice is doing CC's job for it.
- **Log what the verifier could not do**, not just what it did. A gap the verifier couldn't reach (wrong tool access, missing parameter, stale schema) is itself a finding — if it isn't written down, the gap becomes invisible the next time someone assumes the verifier covers that ground.

## Evidence / success criteria

- Every accepted/rejected/corrected item from the report has been checked against the live row it refers to, not just read as a sentence.
- For a correction review, at least one verifier finding changes a CC-authored artifact (edge, claim, prose note). For a timeout-resolution return, do not invent a correction: the legitimate effect may instead be a separately evidenced lifecycle settlement.
- Attribution corrections are appended, not destructive edits.
- A short list exists of what the verifier flagged that CC still owes a fix for, separate from what's already resolved.

## Failure modes

- **Treating the verdict as the whole report.** Filing "9 confirmed, 11 corrected, 4 rejected" as the outcome without reading which 11 and why is the exact discipline this skill exists to prevent.
- **Defending the rejected work.** Re-arguing a rejection instead of accepting the verifier's reading defeats the purpose of asking a different actor in the first place.
- **Overwriting instead of appending.** Rewriting a verifier's original event to fix attribution destroys the record it asked to keep.
- **Marking a finding "fixed" because the verifier named it.** The verifier's tools may not reach the actual repair layer — confirm CC did the fix, not that the verifier did the diagnosis.
- **Scanning for edge/relation corrections only.** Missing the prose corrections is the highest-cost failure mode observed so far — it's the one that happened twice in three runs.
- **Rewriting an unresolved attempt.** A later PASS does not convert an earlier timeout or `UNKNOWN` into PASS; preserve both records and link the new verdict separately.

## Cross-references

`live-multi-actor-negotiation` (runs the live exchange this skill processes the output of) · `live-surface-verification` (verifies disputed state; this skill is the receiving-side counterpart when the verifier is another standing actor rather than a one-off probe) · [feedback_review_reports_on_read](/Users/ted/.claude/projects/-Users-ted/memory/feedback_review_reports_on_read.md) (the general doctrine this skill sharpens for the live-verifier case) · [feedback_live_actor_to_actor_beats_relay](/Users/ted/.claude/projects/-Users-ted/memory/feedback_live_actor_to_actor_beats_relay.md) · [feedback_ai_cannot_verify_another_ai_claim_about_ted](/Users/ted/.claude/projects/-Users-ted/memory/feedback_ai_cannot_verify_another_ai_claim_about_ted.md) · [project_2026_07_28_live_actor_to_actor_and_buoyancy_reread](/Users/ted/.claude/projects/-Users-ted/memory/project_2026_07_28_live_actor_to_actor_and_buoyancy_reread.md) (the source instance)
