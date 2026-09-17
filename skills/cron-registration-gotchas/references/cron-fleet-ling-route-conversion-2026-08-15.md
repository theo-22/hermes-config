# Cron Fleet Model-Route Conversion — ling26_flash (2026-08-15)

Worked example of moving agent crons from `deepseek-v4-flash` direct to `inclusionai/ling-2.6-flash`
via OpenRouter after lab-hermes's model replacement scan. Companion to Gotcha 18 and the model-route
conversion section in SKILL.md.

## The model decision

- `ling26_flash` = `inclusionai/ling-2.6-flash` via OpenRouter, $0.01/$0.03 per M tokens (~$0.004 per cron suite).
- Test source: `Roles/model_testbench/reports/model_replacement_scan_2026-08-15.md` — passed 5/5 standard
  tasks + strict teacher-student contract test; NO `[thinking]` preamble leakage (unlike DeepSeek flash,
  which breaks machine-checkable contract compliance). 14× cheaper than direct flash pre-hike, ~23× after.
- 14 direct-flash crons were the target; 3 already on `nemotron-free` stayed; 1 (`model-discount-page-review`)
  already on OR flash promo; ~5 unpinned (see below).

## Fleet split (93 jobs)

- 21 agent (LLM) jobs — cost money, all candidates for conversion.
- 72 no-agent (script-only) jobs — $0, no change needed.
- Parse with the snippet in Gotcha 18; keys are `no_agent` (bool) + `model` (null ⇒ unpinned).

## What got flipped (first batch)

Same-turn `cronjob action=update job_id=... model='{"model": "inclusionai/ling-2.6-flash", "provider": "openrouter"}'`:

| cron | schedule | route before |
|------|----------|--------------|
| substrate-morning-briefing (531b6e8e5f51) | daily 07:45 | deepseek/deepseek-v4-flash |
| inbox_triage_clerk (a02d92429cfc) | daily 08:00 | deepseek/deepseek-v4-flash |
| pieces-digest-router (5f6579fdedf4) | daily 07:30 | deepseek/deepseek-v4-flash |
| threads_review_artifact (ffde6b82adcd) | M/W/F 08:00 | deepseek/deepseek-v4-flash |
| knowledge-harvest-review (0ff8128d44c9) | Sun 06:30 | deepseek/deepseek-v4-flash |

Then the two drift-blocked Telegram-facing ones (dead anyway → zero-risk flip):
- shopping-guru-saturday-order (ed7f38daf0f5) — daily 09:00
- morning-live-crosscheck (2c714ac7329b) — daily 07:06

## First real-run signals (all within an hour)

- ✅ pieces-digest-router 07:33 — clean
- ⚠️ substrate-morning-briefing 07:48 — **HTTP 429** (rate limit) — burst signal: two ling26 jobs within 25 min
- ✅ inbox_triage_clerk 08:03 — clean (15 min after the 429 — same model, no burst)

Interpretation: burst rate-limit on promo route, not quality failure. If it recurs at the same window,
spread schedules so no two converted crons fire inside the same few-minute burst.

## Drift cohort (4 more blocked same day)

| cron | profile | fix |
|------|---------|-----|
| shopping-guru-saturday-order | substrate | pinned ling26 (dead anyway) |
| morning-live-crosscheck | substrate | pinned ling26 (dead anyway) |
| Brain Test-Probe Sweep | brain-hermes | surfaced, not mine to touch |
| coordinator-morning-sweep | coordinator-hermes | surfaced, not mine to touch |

Lesson: fixing one drift-skip is not enough — sweep the whole registry (all profiles) for `model: null`
agent crons. The spend-guard will have blocked them ALL.

## Ted's pacing signal

"Let's be sure about them but no curtailment type gating." = monitor after the fact, don't handicap the
converted jobs (no read-only / approval-gate wrappers). Confirm quality by reading first-run outputs.

## Rate-limit fallback chain (second pass, same session)

The 07:48 morning-briefing 429 (first burst signal) triggered the fallback work:

1. Inspect current chain: `grep fallback_providers ~/.hermes/profiles/<profile>/config.yaml` — was
   `nvidia/nemotron-3-ultra-550b-a55b:free`, the same flaky model that gave audit_preflight its
   ResourceExhausted/404 streak. Not a sane first fallback for a cheap-cron fleet.
2. Write via CLI — direct `patch`/`write_file` on config.yaml is REFUSED ("Refusing to write to Hermes
   config file ... use 'hermes config' instead"):
   ```bash
   hermes --profile substrate-hermes config set fallback_providers '[{"model": "upstage/solar-pro4", "provider": "openrouter"}, {"model": "qwen/qwen3-30b-a3b-instruct-2507", "provider": "openrouter"}, {"model": "nvidia/nemotron-3-ultra-550b-a55b:free", "provider": "openrouter"}]'
   ```
3. Verify: `grep -n -A1 fallback_providers <profile>/config.yaml` → three-entry chain.
4. No gateway restart needed — cron scheduler calls `load_config()` per tick (scheduler.py ~513/1350/
   1904/3461), and the agent loop activates `fallback_providers` after retries exhaust on 429
   (conversation_loop.py `_try_activate_fallback()` at ~1122/1468). Chain applies to cron agent runs
   because the scheduler passes `fallback_providers` into the run (scheduler.py ~2835/2909).
5. Finished the fleet flip in the same pass: remaining deepseek-direct crons + the 3 nemotron-free
   proposers + the 2 Telegram-facing drift-blocked ones all → ling26. Final: 20/21 agent crons on
   ling26; only `model-discount-page-review` stays on `~deepseek/deepseek-v4-flash-latest` (its whole
   job is reviewing OR pricing). All 21 pin a model/provider — no unpinned agent crons remain.
6. Monday-morning observation to carry forward: watch whether the 429 recurs at the 07:33/07:48 burst
   window now that the chain exists — if ling26 429s, the run should roll to solar-pro4 and still
   deliver (vs the pre-chain behavior of a hard error).

## Also fixed same session (unrelated crons)

- proactive-repair: 3× EINTR retry + path constants canonicalized, both script copies synced (Gotcha 17 / Gotcha 16).
- pieces-continuity-daily: transient — Pieces OS was down at 07:00 (process up 07:08); script verified clean
  under uv-3.11 interpreter which has `pieces_os_client`; system `/usr/local/bin/python3` (3.14) lacks the
  package → always test cron scripts with the interpreter that carries their deps (uv 3.11 here), not bare `python3`.