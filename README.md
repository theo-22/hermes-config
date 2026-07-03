# Ted's Hermes Agent Configuration

A multi-profile Hermes Agent setup for personal AI infrastructure.

## Architecture

**4 profiles** — each an independent Hermes instance with distinct responsibilities:

| Profile | Role |
|---|---|
| **coordinator-hermes** | Task routing, orchestration, cross-profile coordination |
| **substrate-hermes** | Operational monitoring, cron reliability, system health |
| **brain-hermes** | Memory management, knowledge capture, Brain/Supabase |
| **lab-hermes** | Model testing, tool evaluation, experimentation |

## Routing Chain

Default: `Flash → Pro → Hermes 3 (free) → GLM 5.2 → GPT-5.5 (sub) → Claude Sonnet 4.6 (sub)`

Manifest.build routes through existing ChatGPT Plus / Claude Pro subscriptions at zero marginal cost.
Direct DeepSeek bypass available for `--provider deepseek` override.

## Skills

36 curated shared skills organized by domain. Not community plugin bloat — each skill is a tested, documented procedure.

## Cron

- Daily routing health check (no-agent watchdog)
- Model boundary testing (chained)

## Notes

Secrets are auto-redacted on sync. This repo is regenerated from live config — treat as reference, not source of truth.
