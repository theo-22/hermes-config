# Ted's Hermes Agent Configuration

A multi-profile Hermes Agent setup for personal AI infrastructure.

## Architecture

Two kinds of profile, by design:

**Always-on** — a standing gateway (messaging listener) plus scheduled crons.
Reachable by chat; do recurring work whether or not anyone's watching.

| Profile | Role |
|---|---|
| **default** | General-purpose chat, primary working surface, cron host |
| **coordinator-hermes** | Session continuity, routing, morning sweep |
| **substrate-hermes** | System health monitoring, cross-actor verification, largest cron fleet |
| **brain-hermes** | Brain/knowledge quality, ingestion, cross-profile coordination |
| **advisor** | Daily check-in interview, family backup watchdog |
| **here-hermes** | Shared group-chat presence, no crons |

**On-demand** — no standing gateway, no daily cron. Zero cost while idle;
activated only when dispatched or explicitly opened for a bounded task.

| Profile | Role |
|---|---|
| **claude-hermes** | Pro-tier reasoning escalation for cross-file synthesis |
| **lab-hermes** | R&D, provider evaluation (config-publish cron now runs on substrate-hermes) |
| **migrator** | Bounded move-packet execution (mutating, reversible) |
| **verifier** | Independent receipt/live-state checking (read-only) |
| **reconciler** | Reference-integrity checks after moves/renames (read-only) |
| **doc-reconciler** | Doc-vs-disk consistency checks (read-only) |

migrator/verifier/reconciler/doc-reconciler are dispatched the same way regardless
of gateway state — dispatch is a one-shot CLI call, never routed through a
gateway — so "on-demand" costs nothing structural, only the absence of direct
chat reachability.

## Routing Chain

Default: `Flash → Pro → Hermes 3 (free) → GLM 5.2 → GPT-5.5 (sub) → Claude Sonnet 4.6 (sub)`

Manifest.build routes through existing ChatGPT Plus / Claude Pro subscriptions at zero marginal cost.
Direct DeepSeek bypass available for `--provider deepseek` override.

## Skills

36 curated shared skills organized by domain. Not community plugin bloat — each skill is a tested, documented procedure.

## Cron

This export includes a live sample of one profile's registered cron jobs
(see `cron/`) as a reference for schedule/job shape — not an exhaustive list of
every cron running across the fleet.

## Notes

Secrets are auto-redacted on sync. This repo is regenerated from live config — treat as reference, not source of truth.
