# Fleet cron ownership split — 2026-08-07 (reference)

Canonical ownership model after the advisor → substrate-hermes/brain-hermes migration.
The class-level procedure is SKILL.md Gotcha 14; this is the concrete result + inventory.

## Ownership model (final)

| Profile | Job count | Owns |
|---|---|---|
| advisor | 4 | Advisory core only: `morning_advisor_interview`, `curtailment_summary`, `pre-op-reminder`, `surgery-morning-check` |
| substrate-hermes | 89 | System health, monitoring, report pipeline, audit surfaces, pieces lanes, cost, inbox hygiene, grocery/shopping, backups |
| brain-hermes | 4 | Brain ops: `Brain Daily Dump`, `pieces-to-brain-ingestion`, `brain-health-scan`, `Brain Test-Probe Sweep` |

Zero name overlap and zero shared job IDs across profiles (verified mechanically 2026-08-07).

## What moved (advisor → substrate-hermes, 32 jobs)

audit_case_lifecycle_check, audit_preflight, audit_rotation, audit_rotation_pattern_review,
audit_rotation_surface, brain_ingest_health, cc_inbound_rollup, changes_log_size_rotate,
clear_do_queue_refresh, closure_stamp_proposer, codex_cost_offload, codex_review_generator,
decisions_pair_check, family-backup-watchdog, gate_conversion_ratio, gpt_self_check_drift,
icon-gallery-freshness-watchdog, inbox_aging, inbox_triage_clerk, knowledge-harvest-extract,
knowledge-harvest-review, manifest_phase1_audit, memory_index_proposer, pieces-continuity-daily,
pieces-digest-router, pieces-evaluation-review, proposal_lifecycle_check, reunion-backup-pruner,
schema_bridge_audit, stale-path-scanner, threads_review_artifact, yield_refresh

Plus `Brain Daily Dump` → brain-hermes. Removed `pieces-capture-review` LLM duplicate from
advisor (substrate-hermes already owned a copy — invisible to script-key dedup because LLM jobs
have `script: null`; only a name-based cross-profile scan caught it).

## Prior dedup pass (same day, 17 jobs removed, not moved)

ai_cost_posture, ai-inbox-hygiene ×2, audit-request-daily-triage, bridge_health_check,
cron_health_receipt, deepseek-balance-check, drift_deltas, meta-agent-sweep, morning_digest,
proactive_repair, silent_failure_detector, stale_todo_check, substrate-daily-report,
substrate_rollup, substrate_status, weekly_answer_shoring_review — all had healthy substrate
copies already, so removal only.

## Schedule deltas on moved jobs (substrate copy differs from advisor's)

- `bridge-health-check`: every 20m (advisor ran every 2m)
- `meta-agent-sweep`: 00:30 (advisor ran 06:10)
- `audit-request-daily-triage`: 06:45 (advisor ran 06:00)
- `deepseek-balance-logger`: every 2h (supersedes advisor's daily check — better)

## Scripts copied to target dirs

brain_ingest_health.py, codex_cost_offload_check.py, family_backup_watchdog.py,
icon_gallery_freshness_watchdog.py, cross_session_knowledge_harvest_cron.sh,
knowledge_harvest_review_prep.py, reunion_backup_pruner.sh, stale_path_scanner.py
→ substrate-hermes; brain_daily_dump.sh → brain-hermes.

## LLM jobs pinned to deepseek/deepseek-v4-flash (Gotcha 6)

audit_preflight, closure_stamp_proposer, inbox_triage_clerk, knowledge-harvest-review,
memory_index_proposer, pieces-digest-router, threads_review_artifact, Brain Daily Dump.

## Environment issue surfaced during verification (not migration-caused)

`pieces-continuity-daily` errors against port 39300 (Pieces workstream engine not listening).
Fails identically from terminal — the PiecesOS local engine must be running for this job.
Not a path/ownership problem.

## Backups

`~/.hermes/profiles/{advisor,substrate-hermes,brain-hermes}/cron/jobs.json.bak-migrate-20260807_143242`
