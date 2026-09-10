---
name: audit-case-disposition
description: Inspect pending (unstamped) audit case files, verify their findings against live system state, and produce a disposition report categorizing each case for close/stamp, Ted decision, or routing. Use when CLOSURE_INDEX.md shows pending cases or when Ted asks for a triage pass on unstamped backlog.
category: audit
one_line_use: produce a disposition report for pending audit cases
fast_pick: "yes"
---

# Audit Case Disposition

Produce a disposition report for pending (unstamped) audit case files. This is the step BETWEEN Audit GPT running the triage and CC stamping the yield verdict — dispositions determine whether a case is ready to close, needs Ted, or must be routed elsewhere.

## When To Use

- CLOSURE_INDEX.md shows unstamped/pending cases and Ted asks for inspection.
- Session-start surfaces (ACTIVE_INDEX, Hermes/Inbox, _AI_Inbox) contain a pending-case inspection request.
- A batch of cases needs live-state verification before they can be closed.
- Ted asks "what's the state of the pending audit cases?"

## When Not To Use

- Do not use for new audit runs — that's Audit GPT's job.
- Do not use to STAMP cases (write `## CC yield rating` sections) — that's `audit-yield-stamp`.
- Do not use to implement audit findings — route implementation separately.

## Sources of Truth

Three surfaces establish the pending set:

1. **CLOSURE_INDEX.md** — `Operations/reports/Audit/CLOSURE_INDEX.md` — the case-level index. The "Pending CC review" section lists all unstamped cases.
2. **Individual case files** — `Projects_GPT/Audit/Runs/YYYY-MM-DD_Triage_<Label>.md` — each case file contains the audit question, scope, findings, and the auditor's recommended next move.
3. **FINDINGS_INDEX.md** — `Operations/reports/Audit/FINDINGS_INDEX.md` — findings-level index (optional; use for cross-reference).

## Workflow

### 1. Identify the target set

Read CLOSURE_INDEX.md. The "Pending CC review" table shows:
- Date, Label, Findings count, Output state (e.g., "Ted decision needed", "action needed", "no action")
- These are the cases that need disposition

Cap a single pass at 15 cases unless Ted authorizes more. Full verification requires reading each case file and checking live surfaces — volume is the main failure mode.

### 2. For each case, read the case file

Read `Projects_GPT/Audit/Runs/YYYY-MM-DD_Triage_<Label>.md`. Focus on:
- **Audit question** — what was the case about
- **Findings** — each finding is a claim about system state. Note the classification, confidence, and evidence cited.
- **Finding disposition check** — some case files already have this table showing per-finding disposition state
- **Output state** — the auditor's assessment: "Ted decision needed", "action needed", "backlog", "no action"

**Do not trust the case file's own claims.** Every finding that depends on live state (stale file, missing reference, unaddressed TODO) must be verified independently.

### 3. Verify key findings against live state

For each finding, ask: what observable surface would confirm or refute this finding today?

Common verification patterns:
- **Stale file reference** → check `ls -lt` or `stat` on the file. Does it still exist? Has it been modified since the case was written?
- **Missing reference / broken pointer** → check if the path exists. Try to open it.
- **Unresolved TODO item** → read the TODO file. Is the item still there, moved, or removed?
- **Outdated surface** → does the surface still have the stale content? Has it been updated?
- **Claimed fix** → the case may say something was "already resolved" or "superseded" — verify by checking current state, not by trusting the claim.

Do not use timestamp inference alone ("file was modified on date X, therefore finding is resolved" — this is not verification). Read the actual content.

### 4. For each case, determine the disposition

Four disposition categories:

**CLOSE / STAMP** — case is ready for `audit-yield-stamp`. Criteria:
- Zero findings (clean smoke test, no defects)
- All findings resolved by system change since the case was written (file removed, reference fixed, surface retired)
- All findings identified as already-superseded/stale BY THE CASE ITSELF
- Informational-only pattern monitored but no action needed

**STILL VALID → needs Ted decision** — findings are still true but only Ted can decide what to do. Criteria:
- Findings verified against live state, still accurate
- The action is a decision (keep, retire, adopt, defer) that requires Ted's authority
- No auto-routable owner surface exists

**STILL VALID → route** — findings are still true and can be routed to an owner surface. Criteria:
- Clear owner: CC for filesystem/bridge/authority, Codex for scripting/cron, Planning for design
- The action is clearly defined
- Write the routing in the disposition

**STALE / SUPERSEDED → close** — findings no longer apply. Criteria:
- The file/surface that was the subject of the finding no longer exists
- A system change made the finding moot
- The finding was a one-time snapshot that is no longer relevant

### 5. Write the disposition report

Deliver to `_AI_Inbox/` with a clearly addressed title: `YYYY-MM-DD_substrate_hermes_pending_audits_disposition_report.md`

Structure:
```
# For: Ted / CC — Pending Audit Case Dispositions
## From: Substrate-Hermes | YYYY-MM-DD

**Source:** CLOSURE_INDEX.md path
**Scope:** N pending cases

## Verdicts by Case

### N. <Case Name> — <Date> (<N findings>)
**Verdict: <VERDICT>**

- **Finding 1** (short name): <live-state assessment + evidence>
- **Finding N** (short name): <live-state assessment + evidence>
- **Route:** <next action>

## Summary

| # | Case | Verdict | Route |
|---|------|---------|-------|
| 1 | Name | verdict | owner |

**Auto-fixable this session:** <items>
**Clean closures:** <cases ready for stamp>
**Still needs Ted:** <cases>
**Routable:** <cases>
```

## Pitfalls

- **Timestamp-inference is not verification.** "This file was modified Jun 30" does not prove its content changed in the right way. Read the actual content.
- **"Already resolved" claims in case files are not proof.** The case itself may have identified a finding as superseded — always verify independently.
- **Zero-finding cases (smoke tests) are valid for close.** They don't need deep verification — just confirm the case file says "No findings" or "No defect findings."
- **Volume limit.** 15 cases is the practical ceiling for thorough per-case inspection. For larger backlogs, ask for priorities.
- **Do not stamp while doing disposition.** Disposition identifies what should happen. Stamping (writing CC yield ratings) is a separate pass. Mixing them produces false closure.
- **Live state can change between disposition and stamp.** Note this: "Verified against live state as of YYYY-MM-DD — findings may shift if surfaces change."

## Related Skills

- `audit-yield-stamp` — run AFTER disposition to write CC yield ratings on ready-to-close cases
- `audit-preflight-production` — produces the daily audit packet (complementary, not overlapping)

## Interaction with CLOSURE_INDEX.md

The CLOSURE_INDEX is regenerated periodically by `closure_index_generator_cron.py`. Dispositions in your report do not automatically update the index — they are recommendations for the stamp pass. Once cases are stamped, the next CLOSURE_INDEX rebuild will reflect the reduced pending count.
