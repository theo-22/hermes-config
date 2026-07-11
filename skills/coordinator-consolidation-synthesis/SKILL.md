---
name: coordinator-consolidation-synthesis
title: Coordinator Consolidation Synthesis
description: Use when Ted has completed per-profile consolidation evaluations and needs Coordinator to synthesize them into a final recommendation. Covers reading 10 evaluation files, revising the original plan, responding to recommendations, and handing off to GPT Role Runtime review.
---

# Coordinator Consolidation Synthesis

## When to use

Use this skill after all Hermes profiles have submitted their consolidation self-evaluations to `_AI_Inbox/`. Ted has reviewed the landscape and needs Coordinator to produce the consolidated synthesis that drives the final decision.

## Prerequisites

- All 10 Hermes profiles have filed evaluations at `_AI_Inbox/response_consolidation_evaluation_from_*.md`
- Your original plan is at `_AI_Inbox/Actor_Consolidation_Briefing_2026-07-11.md`
- Ted has confirmed the evaluation phase is complete

## Phase 1 — Read the data

1. **Read your original plan** — `_AI_Inbox/Actor_Consolidation_Briefing_2026-07-11.md` (focus on the inventory table and the 4-profile recommendation)
2. **Read all evaluation responses** — `_AI_Inbox/response_consolidation_evaluation_from_*.md` (expect 10 files: brain, claude, coordinator, default, here, lab, migrator, substrate, verifier, advisor)
3. **Read the default profile's final recommendations** — the default evaluation has a section called "Final Recommendations for the Synthesis Plan" with 7 action items. Also note the "Config Audit Results" section documenting what was already fixed fleet-wide.

## Phase 2 — Synthesize

Produce a single consolidated document to `_AI_Inbox/response_coordinator_consolidation_synthesis_<date>.md` covering:

### 1. Topology decision

For each of the 10 Hermes profiles, state: **keep / merge / decommission** and the reasoning. The evaluations were nearly unanimous — no genuine overlap found, all profiles should stay. State whether you agree or disagree and why.

### 2. Revise your 4-profile target

Your original plan aimed for 4 profiles. Every evaluation argued against this target as arbitrary. State whether you're revising that target and to what.

### 3. Respond to default's 7 recommendations

The default evaluation provides 7 recommendations:
1. Fix the live cron errors (pieces-capture-review, backup watchdog, grocery fetcher, fundrise scraper)
2. Decouple the dashboard from coordinator-hermes morning sweep
3. Refresh stale state files across all profiles (ACTIVE_INDEX.md, CONTINUITY.md)
4. Standardize recovery procedures (gateway/launchd/bot recovery runbook)
5. Make the consolidation audit quarterly (lightweight cron)
6. Continuity surface convention (minimal template for state files)
7. Don't merge profiles (no genuine overlap found)

For each: **agree / disagree / modify** and why.

### 4. What changed

List any config fixes, continuity updates, or structural changes made during the evaluation process that should be preserved:
- `verify_on_stop: true` set on 9 profiles
- `profile.yaml` descriptions written for 5 profiles
- `.env` duplicate ANTHROPIC_API_KEY lines cleaned on 4 profiles
- Continuity files modernized where found stale

### 5. Recommendations for the GPT Role Runtime review

Ted is taking this to the ChatGPT Role Runtimes next. What should they evaluate? What questions are still open?

### 6. Ted's decision needed

What does Ted actually need to decide? Be specific. Likely areas:
- Approving the final topology
- Approving the 7 recommendations (or a subset)
- Signing off on proceeding to GPT Role Runtime review
- Any resource or cost decisions

## Phase 3 — Session end

- Write continuity note
- Add CHANGES_LOG entry
- Commit/push changes if applicable
- Write the synthesis artifact

## Output format

```
## Coordinator — Consolidation Synthesis

### Topology Recommendation

[Table or list — each profile: keep/merge/decommission + reasoning]

### Revised Target

[Did the 4-profile target change? What's the new number and why?]

### Response to Default's Recommendations

| # | Recommendation | Verdict | Reasoning |
|---|---------------|---------|-----------|
| 1 | Fix cron errors | agree/disagree/modify | ... |
| ... | ... | ... | ... |

### What Changed This Round

[List of durable changes made during evaluation]

### For the GPT Role Runtime Review

[What's still open; what role runtimes should evaluate]

### Ted's Decisions Needed

[Actionable list of what Ted must decide]
```
