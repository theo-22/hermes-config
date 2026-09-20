---
name: cron-job-health-audit
description: Audit a named scheduler and its report-consumption chain using live job records, run evidence, and documented expectations. Use to distinguish execution failure, overdue work, missing output, and unconsumed findings without treating a silent job or an old report as automatic failure.
metadata:
  category: meta
  write_mode: file
  one_line_use: verify cron health and report consumption with an evidence-bearing receipt
  fast_pick: "no"
---

# Cron Job Health Audit

Check the named scheduler through its actual outputs and consumers. A scheduler
status alone does not prove that the job accomplished its purpose.

## Scope and authority

Start with the routed job, profile, or reporting chain. Read its live scheduler
record and implementation before selecting checks. Inventory job ID, profile,
schedule/timezone, enabled state, command, last/next run, status, execution error,
delivery error, output destination, and expected consumer. Do not infer a fleet
inventory from one profile's jobs file.

This audit is observation-only except for its receipt. Repair, disable, rerun,
model changes, delivery, and service restarts require task authority; an audit
does not supply it. Do not run metered jobs merely to test freshness.

## Verification

1. Compare current status with the latest run evidence. Separate a historical
   failure from the current result, and distinguish execution from delivery.
2. Check whether enabled work is actually due, accounting for its schedule,
   timezone, running instance, and any documented grace period. If no grace or
   freshness threshold is documented, report the measured lateness and the
   uncertainty; do not invent a universal 30-day threshold.
3. Verify the expected effect: output contents/counts, destination, or downstream
   state. A zero exit code or `ok` label is insufficient if the intended write
   failed. Silence is healthy only when it matches the job's explicit contract.
4. Trace who consumes the output and whether findings were routed or resolved.
   Report-only files are not proof that someone acted on their findings.
5. Record each finding with a job ID or exact path, observation time, evidence,
   applicable expectation, and concrete next action. Keep unknowns separate from
   failures. Preserve run evidence; do not delete or retire it during diagnosis.

## Existing `cron_health_receipt` pattern

Source verified 2026-09-20:
`/Users/ted/.hermes/scripts/cron_health_receipt.py`.
It reads only `/Users/ted/.hermes/cron/jobs.json` and writes dated plus latest
Markdown receipts under
`/Volumes/Extra/Substrate/Hermes/Hermes_Operator_Integration/Hermes_Records/`.
This is default-profile coverage, not fleet-wide coverage.

Its implemented classification is:

- failure: a nonempty `last_status` outside `ok`, `silent`, and `skipped`;
- overdue: an enabled job whose parseable `next_run_at` precedes the check time;
- receipt status: `watch` when either set is nonempty, otherwise `ok`.

These are script observations, not conclusive health verdicts. The script counts
old statuses from disabled jobs, has no lateness grace, and computes an error
list without using it to set the receipt status. Missing/invalid timestamps do
not prove health. Read `last_error` and `last_delivery_error` separately, and
verify output effects before accepting `ok`. Do not change these runtime rules
as a side effect of using this skill.

The existing receipt includes observation time, status, job/mode counts, failure
and overdue details, next/recent runs, routing guidance, and an
`Intentionally Not Changed` section. For an audit supplement, use:

```markdown
# Cron Health Audit — <observation timestamp and timezone>
Scope: <profile, scheduler, exact inventory source, job IDs>
Result: healthy | attention | unknown
Expected behavior: <schedule/output/consumer and source of expectations>
Evidence: <current run state, output proof, delivery, consumer state>
Findings: <specific target, actual vs expected, classification, next action>
Intentionally Not Changed: <jobs, services, routing, credentials, retained evidence>
```

Save to the routed audit/receipt destination and reconcile the existing work
item when authorized. Do not create a second work item for the same finding.

## Related checks

- [Proactive repair receipt pattern](references/proactive-repair-receipt-pattern.md)
  supplies evidence and scope-boundary requirements.
- [Room verification pattern](references/hermes-room-verification-pattern.md)
  applies when a room-level stale flag triggered the investigation. Its scoring
  is specific to that pattern, not a scheduler-health threshold.

## Update check

Re-read the live scheduler schema and receipt source before using the dated
implementation notes. If the runtime changed, correct this canonical skill and
regenerate its published copy; do not invent a parallel local policy.
