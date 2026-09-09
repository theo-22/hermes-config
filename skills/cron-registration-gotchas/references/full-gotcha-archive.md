# Full Gotcha Archive — cron-registration-gotchas

This is the complete pre-v2 SKILL.md (every historical entry verbatim, with all
real examples, job ids, and code samples). The working skill now lives in
../SKILL.md, organized by failure shape with a symptom table; entries here are
the evidence base. Nothing was deleted — the numbering below is the historical
numbering (note it has gaps and duplicate numbers across eras; that's the
historical record).

Historical addendum note: "Gotcha 23 — Attic/orphan sweeps" (2026-09-09) was
written after this archive was cut; its full text is in the v2 SKILL.md (A3).

---


# Cron Registration & Execution Gotchas

Silent failure modes that break `no_agent` cron jobs. All leave the job scheduled but failing or skipping, with no surface signal until you inspect the cron output.


## The pointer rule — read this before adding any file to a profile scripts dir

**Never put a second copy of a script in a profile scripts directory. Put a pointer.**

Hermes cron resolves a job's `script` field against `$HERMES_HOME/scripts` and
*blocks* any path that resolves outside it (`cron/scheduler.py`). So a file must
exist there. That is a real constraint and it is not going away. What is optional
is whether that file contains logic.

Every incident this skill documents under "the two copies drifted" — Gotcha 4
(2026-06-29), Gotcha 14 (2026-08-02), Gotcha 16 (2026-08-13, a silently dead
scan) — has the same cause: the file in the profile was a copy, so there were two
implementations, and only one of them got fixed. Each of those entries used to
prescribe *remember to sync both*. That prescription is why the problem recurred
three times. Work item #1574 measured the result: 82 diverged pairs, 17 of them
live under cron.

Write this instead, as `~/.hermes/profiles/<profile>/scripts/<name>.py`:

```python
#!/usr/bin/env python3
"""Hermes wrapper for the tracked <thing>.

Single source of truth: /Volumes/Extra/Substrate/Operations/scripts/<name>.py,
git-tracked in the Operations repo.
This file holds no logic of its own.
"""

import runpy

from substrate_root import resolve_substrate_path

TARGET = resolve_substrate_path("/Volumes/Extra/Substrate/Operations/scripts/<name>.py")


if __name__ == "__main__":
    if not TARGET.exists():
        raise SystemExit(f"Missing tracked <thing>: {TARGET}")
    runpy.run_path(str(TARGET), run_name="__main__")
```

Notes that matter in practice:

- **Exit codes propagate.** `runpy` lets `SystemExit` through, so a script that
  exits 1 on findings still reports 1 to cron. Proven in production —
  `stale_path_scanner` has been a shim for months and its job reports exit 1
  correctly.
- **`sys.argv` is inherited**, so `--verbose`-style flags still reach the target.
- **Do not use a shim for a script that reads `__file__`** to locate its own
  neighbours; fix the script to take an explicit root first.
- **`os.execv` is an equally valid pointer** (`audit_rotation.py` uses it) when
  you want a clean process rather than an in-process run.
- **`substrate_root.py` lives only in the profile scripts dir.** That is the
  point: the profile resolves *where* Substrate is mounted, the tracked script
  holds *what to do*. Keep that split.

If a job's prompt (agent mode) also names a script path, delete that instruction —
the `script` field already ran it. A prompt that re-executes the target is how one
job ends up running two versions (see `meta-agent-sweep`, repaired 2026-09-04).


## Gotcha 1 — Args baked into script field

The cron gateway treats the `script` field as a **literal filename**. It does NOT split `python3 foo.py --bar` into `python3` + `foo.py --bar`. So this registration:

```json
{ "script": "pieces_evaluation_review.py --verbose", ... }
```

…will fail with `Script not found: pieces_evaluation_review.py --verbose` because no file with that literal name exists.

**Fix:** strip args from the `script` field. If the script needs args, one of:

- Make args optional with sensible defaults (the cron only runs unattended — extra args are usually noise anyway)
- Pass args via an env var the script reads
- Wrap in a shell script: `script: "run_pieces_eval.sh"` and have the wrapper pass args

**How to spot:** `cronjob list` will show the job with a normal-looking `script` field. Check `~/.hermes/cron/output/<job-id>/<timestamp>.md` — error message names the literal path it tried.

## Gotcha 2 — Symlinks rejected (UPDATED 2026-06-28: profile scripts dir required)

The cron gateway resolves the `script` field against `~/.hermes/scripts/` for the **default profile**, but for **named profiles** (e.g., `substrate-hermes`), it resolves against `~/.hermes/profiles/<profile>/scripts/`.

In some versions/configurations, it checks the **resolved** path is inside the profile's scripts directory and rejects symlinks pointing outside that directory (historically e.g. to the pre-migration `/Users/ted/Operations` alias of the Operations tree) with:

> `Blocked: script path resolves outside the scripts directory (/Users/ted/.hermes/scripts): 'foo.py'`

**However:** As of 2026-06-26, symlinks from `~/.hermes/scripts/` → `~/Operations/scripts/` ARE working for the default profile. The gateway may have relaxed this check. **Test before assuming symlinks are blocked.**

**Fix options (in order of preference):**
1. **Symlink** (try first — works in current default profile; path shown in its pre-migration form): `ln -sf /Volumes/Extra/Substrate/Operations/scripts/foo.py ~/.hermes/scripts/foo.py`
2. **Real file copy** (if symlinks are rejected in your version): `cp /Volumes/Extra/Substrate/Operations/scripts/foo.py ~/.hermes/scripts/foo.py`
3. **Move** the script to `~/.hermes/scripts/` and update any source-of-truth references

**For named profiles:** You MUST copy or symlink into `~/.hermes/profiles/<profile>/scripts/`. We tested: copying works; symlinks also work from the main scripts dir.

**How to spot:** `ls -la ~/.hermes/profiles/<profile>/scripts/<script_name>` shows `->` and a target outside the scripts dir. If the cron job still errors after symlink creation, your gateway version rejects symlinks — fall back to real copy.

## Verification after registration

Always re-trigger the cron after fixing and read the output:

```bash
# Re-run
cronjob action=run job_id=<id>

# Read output
LATEST=$(ls -t ~/.hermes/cron/output/<job_id>/*.md | head -1)
cat "$LATEST"
```

If the output file ends with `Status: script failed` or `Status: error`, the fix didn't take. If it ends with normal output / `Status: ok`, you're good.

## Affected crons (resolved)

- `pieces-evaluation-review` (`4a4dada82720`) — Gotcha 1 (args in script field)
- `knowledge-harvest-extract` (`b4d103634162`) — Gotcha 1 (args in script field)
- `meta-agent-sweep` (`81dec503afb9`) — Was Gotcha 2 historically; now resolved via symlink from `~/.hermes/scripts/` → `Operations/scripts/`
- `audit-request-daily-triage` (`0cc8b09a75eb`) — Naming mismatch: cron referenced `audit_request_daily_triage.py`, actual file `audit_triage_daily.py`. Fixed by updating `script` field.
- `overnight-consolidated-morning` (`af1ec7ddb125`) — No-agent cron, script `overnight_consolidated_morning.py` copied to profile scripts dir
- `project-room-health-check` (`fda85e8353d1`) — No-agent cron, uses existing `project_room_drift_check.py` from Operations/scripts (symlinked)
- `audit-router` (`4220d47880ba`) — No-agent cron, script `audit_router.py` in profile scripts dir
- `audit-gpt-dispatch` (`d5f7aeeaf95b`) — No-agent cron, script `audit_gpt_dispatch.py` in profile scripts dir
- `grocery-receipt-fetcher` (`e96bc456a310`) — No-agent cron, script `grocery_receipt_fetcher.py` in profile scripts dir
- `substrate-archive-reports` (`c46790a1ffc8`) — Agent cron, script `substrate_archive_reports.py` in profile scripts dir

## Gotcha 4 — Profile scripts dir cache (2026-06-29)

After fixing a no-agent cron script at the shared location (`~/.hermes/scripts/`), the next `cronjob(action='run')` may still execute the **old cached copy** in the profile-specific scripts directory (`~/.hermes/profiles/<profile>/scripts/`).

**Symptom:** You fix a script, test it manually (works), trigger the cron (still errors with the old bug).

**Fix (SUPERSEDED 2026-09-04 — do NOT copy):** This section used to say "always sync
both locations" with a `cp`. That instruction is what created the fork this skill
kept re-diagnosing; see **The pointer rule** at the top of this file. The profile
file must be a *pointer* to the tracked script, not a copy of it. If you are here
because a fix did not take effect, the answer is to convert the profile file to a
shim, not to re-copy it.

**Real example (2026-06-29):** Fixed `print(OUTPUT.read_text())` stdout leak + `NameError: yesterday` in `overnight_consolidated_morning.py` at `~/.hermes/scripts/`. Ran `cronjob(action='run')` — still got the NameError because cron ran from the profile-local copy at `~/.hermes/profiles/substrate-hermes/scripts/`.

## Gotcha 6 — Absolute script path rejected; use wrapper for non-standard interpreter

The `script` field in `cronjob(action='create')` **must be a relative filename** — resolved against `~/.hermes/scripts/` (default) or `~/.hermes/profiles/<profile>/scripts/` (named profile). An absolute path like `/Volumes/Extra/Substrate/Operations/scripts/foo.py` is rejected:

> `Script path must be relative to ~/.hermes/scripts/. Got absolute path`

BUT the real script often lives in a shared location (`/Volumes/Extra/Substrate/Operations/scripts/`) AND may need a non-default Python interpreter (e.g., `/usr/local/bin/python3` for MCP server module deps like `starlette`, `mcp`).

**Fix:** Create a thin wrapper shell script in the profile scripts dir that calls the real script with the correct interpreter. Pattern:

```bash
#!/bin/bash
# Wrapper for <script-name> — calls the real script with correct interpreter
SCRIPT="/Volumes/Extra/Substrate/Operations/scripts/<real_script>.py"
PYTHON="/usr/local/bin/python3"
if [ ! -f "$SCRIPT" ]; then echo "[FATAL] $SCRIPT not found"; exit 2; fi
"$PYTHON" "$SCRIPT" --json 2>&1
exit $?
```

**Symlink doesn't work here** because the interpreter path is hardcoded in the cron gateway's execution environment — there's no way to tell it "use `/usr/local/bin/python3`" for a no-agent script. The wrapper IS the workaround.

**Real example (2026-07-06):** `check_role_workspace_access.py` lives in `/Volumes/Extra/Substrate/Operations/scripts/` and needs `/usr/local/bin/python3` (imports MCP server module). Created `check_role_workspace_access.sh` in `~/.hermes/profiles/substrate-hermes/scripts/` — cron runs it as `script: "check_role_workspace_access.sh"` with `no_agent: true`. All 7 roles pass, exit 0.

**Also works for agent-based crons** that run a script before the LLM prompt: you can split into a no-agent data-collection script (via wrapper) plus an agent prompt that reads its output.

## Gotcha 9 — Duplicate cron across profiles (agent + no-agent of same script)

**Problem:** The same script can be registered as a cron in TWO different profiles — one as an **agent-based** cron (with an LLM prompt) in a named profile, and one as a **no-agent** script-only cron in the default profile. Both fire, both write to the same output path. The second one overwrites the first's report.

This wastes tokens (the agent run that analyzed output gets its report overwritten) and scrambles timestamps.

**How to spot:** Check both locations for the same script name:
```bash
grep '"script": "meta_agent_sweep.py"' ~/.hermes/cron/jobs.json
grep '"script": "meta_agent_sweep.py"' ~/.hermes/profiles/substrate-hermes/cron/jobs.json
```

**Fix:** Disable the duplicate in the less-appropriate profile. If an agent-based cron is the primary (analyzes output, extracts action items), the no-agent duplicate should be disabled.

**Real example (2026-07-09):** `meta-agent-sweep` ran as an agent cron at 00:30 in substrate-hermes AND as a no-agent script at 06:10 in the default profile. Default duplicate was disabled.

### Variant — TWO agent copies of the SAME NAMED JOB across profiles (2026-08-08)

The dangerous variant is not agent-vs-no-agent but **the same named job registered as an agent cron in two different profiles, both enabled, same schedule**. Both fire at the same tick and both execute the same prompt against the same working files.

**Symptom differs from the overwrite case:** instead of one report overwriting another, BOTH runs **append to the same append-only routing logs** (summaries/decisions/handoff files). Result: duplicate dated sections for the same digest window in one file — and each run independently routes the same findings, so double-filing of inbox items is a real risk (this is exactly the failure mode that got `pieces-digest-router` flagged for re-filing resolved items).

**How to spot:** grep for the JOB NAME (not script — agent crons have no script field) in both registries:
```bash
grep -n 'pieces-digest-router' ~/.hermes/cron/jobs.json
grep -n 'pieces-digest-router' ~/.hermes/profiles/substrate-hermes/cron/jobs.json
# Or check via python for both job dicts side by side
python3 - <<'PY'
import json
for p in ['/Users/ted/.hermes/cron/jobs.json',
          '/Users/ted/.hermes/profiles/substrate-hermes/cron/jobs.json']:
    d = json.load(open(p))
    jobs = d if isinstance(d, list) else d.get('jobs', d)
    if isinstance(jobs, dict): jobs = list(jobs.values())
    for j in jobs:
        if 'pieces-digest-router' in j.get('name',''):
            print(p, '->', j.get('id'), 'enabled:', j.get('enabled'), 'schedule:', j.get('schedule'))
PY
```
Two DIFFERENT job ids with the same name + same schedule + both `enabled: True` = double-fire. Also: when a routing-log file shows duplicate same-window sections, suspect a duplicate registration before blaming the run itself.

**Fix:** Disable/remove one registration. But when the duplicate lives in another profile's registry (e.g. default profile's `~/.hermes/cron/jobs.json`), the `cronjob` tool cannot reach it from a named profile — edit the JSON directly (`enabled: false`, add `paused_reason`), or remove per the Gotcha 8 removal procedure. **Ted's call when the duplicate is a named job that both profiles legitimately claim** — surface the two ids and let him pick which registration is canonical.

**Real example (2026-08-08):** `pieces-digest-router` registered in default (`9730ec605cf2`) AND substrate-hermes (`5f6579fdedf4`), both enabled, both `30 7 * * *`. Both ran at 07:30 and appended the same digest window to `Hermes/Working/pieces_copilot_summaries.md` and `pieces_decisions_log.md`. Repair: deduped the files (kept the more accurate second pass, merged the two unique items from the first), then surfaced the two ids to Ted. Full repair recipe in `references/duplicate-registration-double-append-2026-08-08.md`.

**Dedup-before-routing check (2026-08-14):** even with a single registration, a digest router must verify the digest hasn't already been routed before appending/filing — the double-fire incident is not the only way same-window duplicates happen. Method: compare file mtimes — if the routing log (`pieces_copilot_summaries.md` / `pieces_decisions_log.md`) was written AFTER the digest file was generated, the window was likely already processed; read the log's last section header (it names the digest window) to confirm coverage. Only route genuinely new windows. Worked example: 08-13 digest (07:00) vs routing logs (07:48) → already routed → zero new inbox items, no duplicate append. This is the guard that prevents the re-filing failure mode the job was flagged for.

### Variant — Same no-agent SCRIPT registered under TWO profiles, different job names, same schedule (2026-08-15)
A variant that looks harmlessly like the same automation happening twice: the same no-agent script (`proactive_repair.py`) is registered as a cron job in two separate profiles — default (`proactive_repair`) and substrate-hermes (`proactive-repair`) — with the SAME schedule (both `0 6 * * *`) and both enabled. The names are slightly different (`repair` vs `repair`) so collision detection by name won't fire.

**Why it happens:** An actor or migration registered the same script twice — once in a system-level sweep, once in a profile migration — with names that differ by one character. Each profile "owns" its copy; neither sees the other.

**Why it's worse than having one registration:**
1. **Double execution** at the same tick — both fire at 06:00, both write to the same output path (or both call `check_cron_fleet()` and generate duplicate flagged items from the same cron state). The second one muddles the first.
2. **Drift in path constants** — the profile-local copy can pick up stale paths from the profile's older config (`Path("/Users/ted/...")`) while the default copy gets updated to canonical (`Path("/Volumes/Extra/Substrate/...")`). The cron executes the profile-local copy, so it silently operates on stale paths.
3. **Asymmetric fix risk** — you fix the shared copy and sync it to the primary profile's copy, but the other registration's script is still the old version. The pulse shows multiple errors from the same script family, and each fix must reach two script locations.
4. **Pulse inflates error count** — when one copy crashes and the other doesn't, the cross-profile pulse reports `[error] proactive-repair` twice.

**Detection:**
```bash
# Check both registries for the same script filename
grep '"script": "proactive_repair.py"' ~/.hermes/cron/jobs.json
grep '"script": "proactive_repair.py"' ~/.hermes/profiles/substrate-hermes/cron/jobs.json
# If both return hits and schedule is the same, you have a duplicate
```
Also diff the two registries' copies of the script to check for path-constant drift:
```bash
diff ~/.hermes/scripts/proactive_repair.py ~/.hermes/profiles/substrate-hermes/scripts/proactive_repair.py
```

**Fix:** Surface to Ted which registration should be canonical; remove the other. While both run, sync BOTH script copies after every edit, matching path constants to the canonical volume path.

**Real example (2026-08-15):** `proactive_repair` in default (`proactive_repair`) and `proactive-repair` in substrate-hermes (`proactive-repair`), both `0 6 * * *`. The profile-local copy had 3 stale `/Users/ted/` path constants (REPORT_DIR, OUTBOUND, CC_OUTBOUND) while the default copy had canonical `/Volumes/Extra/Substrate/` paths. Fixed by syncing both copies to the canonical paths and adding the EINTR retry. Surfaced the duplicate to Ted for consolidation.

## Gotcha 8 — Cron migration between profiles: orphaned-registration trap (2026-07-09)

**Problem:** Cron jobs accumulate in the default profile's `jobs.json` even when they logically belong under a named profile (e.g. `substrate-hermes`). The job keeps running from the wrong home — it *works*, but it's invisible from the owning profile's cron list.

**Symptom:** `cronjob(action='list')` on a named profile shows N crons, but `~/.hermes/cron/jobs.json` (default) has M additional crons doing work for that domain. Ted assumes reporting is consolidated under substrate-hermes but the daily report is actually fired from the default profile.

**How to spot:** grep for the job name or script in both locations:
```bash
grep -n '"script": "substrate_daily_report.py"' ~/.hermes/cron/jobs.json
grep -n '"script": "substrate_daily_report.py"' ~/.hermes/profiles/substrate-hermes/cron/jobs.json
```

### Migration procedure (zero-gap)

1. **GET EXACT DETAILS** from source profile's jobs.json (name, schedule, no_agent, deliver, script)
2. **CREATE IN TARGET PROFILE** using `cronjob action=create` (runs in current session's profile)
3. **DISABLE IN SOURCE PROFILE** by editing `~/.hermes/cron/jobs.json` directly — set `enabled: false`, `state: paused`, add `paused_reason`
4. **VERIFY BOTH SIDES** — target shows new cron in `cronjob list`, source shows `enabled=False` in jobs.json

**Critical rules:**
- **Create first, disable second** — prevents a gap where the cron misses a tick.
- **Script must exist in target profile scripts dir** — no-agent crons resolve scripts against `~/.hermes/profiles/<target>/scripts/`. If missing, add a **shim** there pointing at the tracked script (see *The pointer rule*), never a copy.
- **Same schedule, same deliver** — preserve the original schedule expression and deliver target exactly.
- **disabling in default profile requires direct JSON edit** — `cronjob` tool only manages the current profile's store.

**Remove after safety period (Ted's preference, 2026-07-15):** Migrated crons should be **removed, not left paused indefinitely.**
1. Wait 1-2 full schedule cycles to confirm the target-profile replacement runs successfully (check `last_status`, read output)
2. Remove: for named profiles, use `cronjob(action='remove', job_id='...')`. For **system-level entries** (default profile), the `cronjob` tool cannot reach them from a named profile — edit `/Users/ted/.hermes/cron/jobs.json` directly: remove the job's dict from the `jobs` array entirely. (The old `/Volumes/Extra/Substrate/.hermes/` volume home is RETIRED — that path no longer exists; the system-level registry lives under the local home.)
3. Verify the job count dropped; check `updated_at` field bumped

**First real pass (2026-07-15):** Removed 8 orphaned crons from system-level registry — `drift_deltas`, `substrate_status`, `bridge_health_check`, `manifest_phase1_audit`, `substrate_rollup`, `silent_failure_detector`, `substrate-daily-report`, `weekly_answer_shoring_review`. All had verified replacements in substrate-hermes profile.

## Gotcha 7 — No-op watchdog pattern for silent-when-healthy no-agent crons (2026-07-08)

A no-agent cron that runs on schedule but only speaks when something is wrong must use the **no-op watchdog** pattern:

```python
if stale:
    print("WARNING: reading is N days stale. Visit URL to refresh.")
    sys.exit(1)  # non-zero exit ensures stdout is delivered as alert
sys.exit(0)  # silent exit — empty stdout means nothing is delivered
```

With `no_agent=True`, the cron gateway's delivery semantics are:
- **Empty stdout → nothing delivered.** The user sees nothing. The cron ran and updated its last_run_at but produced no message.
- **Non-empty stdout → message delivered verbatim.** What the script prints IS the message the user receives.
- **Non-zero exit + empty stdout → error alert.**
- **Non-zero exit + non-empty stdout → error + stdout both delivered.**

This is different from agent-based crons where the LLM decides what to say. For no-agent crons, stdout IS the message — design scripts to stay quiet when healthy.

**Real examples (2026-07-08):**
- `ai-cost-dashboard-freshness-check` (daily 9am): checks if dashboard readings >3d stale. Silent if fresh. Prints warning with URLs if stale. Non-zero exit triggers alert.
- `deepseek-balance-logger` (every 2h): logs balance to file, prints current balance. Always exits 0 — log file is the data, not stdout.

**Verification:** To confirm a silent no-agent cron ran, use `cronjob(action='list')` — check `last_run_at`. The output file at `~/.hermes/cron/output/<job-id>/` shows captured stdout.

## Gotcha 15 — Auto-repair watchdog: detection-only becomes repair-aware (2026-08-02)

The Gotcha 7 no-op watchdog **detects** a down service and alerts. When Ted
explicitly authorizes auto-repair ("I'd like to get it working and tested"), the
same script can escalate from detection to bounded repair:

- LaunchAgent **loaded** but service unresponsive → `launchctl kickstart -k gui/$(id -u)/<label>`.
- LaunchAgent **not loaded** → `launchctl load -w <plist>`.
- After either, re-verify; **exit 0 if repair worked** (no alert needed — record only).
- Only write the alert + exit 1 when repair was ATTEMPTED and still failed.

```python
if not args.no_repair:
    if loaded:
        ok = kickstart_bridge()
        if ok:
            time.sleep(AFTER_KICKSTART_DELAY_S)
            if curl_status(LOCAL_URL) in HEALTHY: return 0
    else:
        ok = reload_bridge()
        if ok:
            time.sleep(AFTER_KICKSTART_DELAY_S)
            if curl_status(LOCAL_URL) in HEALTHY: return 0
# fell through: repair failed -> alert
```

Key design points:
- **`--no-repair` flag keeps the legacy detection-only behavior** for testing/manual runs.
- **Re-verify after repair** — a kickstart can succeed as a command while the
  replacement process comes up wedged (that happened live 2026-08-02: watchdog
  kicked, new PID appeared, but `/sse` still hung; the fix was kill + kickstart).
- **Auto-quiet when no TTY**: `argparse` default `not sys.stderr.isatty()` makes
  the cron run silent when healthy while a manual terminal run still prints.
- **Alert body becomes a record**: `repair_attempted: yes/repair_ok: yes` means
  "filed for record, no human action" — different from the old "cry for help."
- Still write the daily report even when silent (that's the evidence surface).

Real example: `mcp_bridge_watchdog.py` upgraded 2026-08-02 from detection-only
to kickstart/reload auto-repair, with `--no-repair` escape hatch, verified live
by unloading the LaunchAgent, watching the watchdog reload it and return 401.
Related: the event-loop-freeze root cause that kept triggering the watchdog is
captured in the `mcp-bridge-freeze-diagnosis` skill.

## Gotcha 16 — Profile-local script copy diverges from root copy in path constants → silently dead scan (2026-08-13)

**Problem:** The cron executes the **profile-local** copy of a script (`~/.hermes/profiles/<profile>/scripts/`), not the root copy (`~/.hermes/scripts/`). The two copies can drift apart: same function name, different path constants. When the profile-local copy holds a stale path that no longer exists, a guard like `if not path.exists(): return 0, 0` makes the whole scan **silently dead** — it returns a clean zero instead of erroring, and the metric reads healthy.

**Real example (2026-08-13):** `substrate_daily_report.py` — profile-local copy had `audit_runs = Path("/Users/ted/Projects_GPT/Audit/Runs")` (nonexistent → early return `(0,0)`, stale-audit findings always reported 0) while the root copy had the correct `Path("/Volumes/Extra/Substrate/Audit/Runs")`. The digest-router's verification pass found the divergence by diffing the two copies.

**How to spot:**
```bash
diff ~/.hermes/scripts/<script>.py ~/.hermes/profiles/<profile>/scripts/<script>.py
```
Look especially at path constants (`Path(...)`, `JOBS_PATH`, `*_DIR`) — the profile-local copy is the one the cron actually runs, so IT is the authoritative consumer path, not the prettier root copy.

**Fix:** Repoint the stale constant to the canonical path in the copy the cron executes; re-verify with a focused check (see Gotcha 4 sync + the `hermes-verify-` ad-hoc pattern).

**Watch the metric activation effect:** after the fix, the metric legitimately jumps from 0 → N (real findings the scan was hiding). That's the metric turning on, not a new problem appearing — say so explicitly in the report so the jump isn't read as a regression.

**Related:** Gotcha 4 (profile scripts dir cache) is about *which copy runs*; this is about the copies *drifting apart* in the paths they scan. Same sync-both-locations fix, different failure shape.

## Gotcha 17 — EINTR crash on symlinked-dir `iterdir()` in no-agent scripts (2026-08-15)

**Problem:** A no-agent cron script walking a symlinked directory (`Path.iterdir()` over `~/ _AI_Inbox` → canonical volume path) intermittently dies with `InterruptedError: [Errno 4] Interrupted system call: '<path>'`. `interrupt()` lands during the syscall under filesystem pressure and, unhandled, aborts the whole sweep before `write_report()` — the run exits 1 with a bare traceback and NO report is written.

**Fix — 3-attempt retry guard inside the function, then bail-to-flag:**
```python
inbox_entries = []
for attempt in range(3):
    try:
        inbox_entries = list(INBOX.iterdir())
        break
    except InterruptedError:
        if attempt == 2:
            flagged.append("Inbox aging check interrupted (EINTR 3x); skipped this run")
            return
for f in inbox_entries:
    ...
```
Key points:
- Retry the *same* read inside the loop, not just catch-and-continue.
- After N retries, **append a flag and return**, don't re-raise — a skipped subcheck is better than a dead sweep (the rest of the script still writes its report).
- Apply the guard to ANY `iterdir()`/`scandir()`/`readdir()` over a symlinked or network-backed path (the `_AI_Inbox` symlink is the recurring one on this box).

**Real example (2026-08-15):** `proactive_repair.py` crashed in `check_inbox_aging()` for several 06:00 runs. One copy (default profile) ALREADY had the retry; the profile-local copy lacked it AND had drifted to stale `/Users/ted/Projects/...` path constants (see Gotcha 16). Fixed by syncing both copies to the canonical path + the retry guard; verified byte-identical and exit 0.

## Gotcha 18 — Agent cron drift-skip: unpinned `model` inherits the global config → spend-guard blocks after config drift (2026-08-15)

**Problem:** Agent-based crons registered with NO `model`/`provider` pin inherit the current global inference config at registration time. When the global default later changes (e.g. the 08-14 fleet move: `deepseek` direct → `openrouter` promo route), every unpinned agent cron starts skipping with:
> `RuntimeError: Skipped to prevent unintended spend: global inference config drifted since this job was created (provider 'deepseek' -> 'openrouter'; model 'deepseek-v4-flash' -> '~deepseek/deepseek-v4-flash-latest')`

The spend-guard is CORRECTLY refusing to run a job whose billing assumption is stale — this is the guard doing its job, not a new failure. But it surfaces in batches: **all** unpinned agent crons break at once when the fleet config moves, and the pulse reports them as N separate "[error]" rows.

**How to spot the whole cohort (don't fix one at a time):**
```python
import json
d = json.load(open('/Users/ted/.hermes/profiles/substrate-hermes/cron/jobs.json'))
jobs = d.get('jobs', d) if isinstance(d, dict) else d
if isinstance(jobs, dict): jobs = jobs.get('jobs', [])
for j in jobs:
    if isinstance(j, dict) and not j.get('no_agent') and j.get('model') is None:
        print(f"UNPINNED agent cron: {j.get('name')} id={j.get('job_id')} status={j.get('last_status')}")
```
Also grep the other profile registries — the same drift blinds brain-hermes/coordinator-hermes unpinned jobs too.

**Fix:** pin `model` + `provider` explicitly on every agent cron (`cronjob action=update job_id=... model={...}`). Pinning gives the drift-guard a stable compare target — it no longer trips when the global moves again.

**Real example (2026-08-15):** `ai-inbox-claude-triage` was first to hit it; a fleet sweep found **4 more** unpinned agent crons across profiles (shopping-guru Saturday, morning-live-crosscheck, Brain Test-Probe Sweep, coordinator-morning-sweep) all blocked by the same drift. Pinned the two in-substrate ones; surfaced the other two profiles' jobs.

## Model-route conversion for the cron fleet — workflow & Ted's pacing preference (2026-08-15)

When moving agent crons to a newly-tested cheaper model (e.g. lab-hermes model scan → `ling26_flash` = `inclusionai/ling-2.6-flash` via openrouter at $0.01/$0.03, 14× cheaper than direct flash):
- **Split agent (LLM, costs money) vs no-agent (script-only, $0) jobs first.** Only the agent cohort changes. On this box: ~21 of 93 crons are agent jobs; 72 no-agent need zero work.
- **Conversion itself is 1 `cronjob action=update` per job** — all 21 fit in a few turns. The pacing question is verification, not migration speed.
- **Tier the flip by user-facing-ness:** flip internal-reporting crons first (inbox triage, thread review, digest routing), then user-facing (Telegram) ones last. BUT if a user-facing job is already drift-blocked, flipping it is zero-risk — it was dead anyway.
- **Ted's pacing preference (2026-08-15): "Let's be sure about them but no curtailment type gating."** Watch the first real run(s) for quality/rate-limit signals, but do NOT add artificial gates to the converted jobs (no read-only flags, no approval-wait steps, no "must review before acting" wrappers). Trusted conversion means the jobs keep full powers; monitoring is verification-after-run, not restriction-before-run.
- **Watch for 429 on promo-route models:** two cheap-model crons firing within minutes of each other (e.g. 07:33 + 07:48) can hit a per-model burst rate limit (`HTTP 429: Provider returned error`) while non-burst runs 15 min away succeed. If it recurs at the same window, spread the converted jobs' schedules so no two hit the promo model in the same few-minute burst.
- **Rate-limit resilience = `fallback_providers` chain, not per-job restart (2026-08-15).** Hermes already retries 3× with backoff, then activates the global `fallback_providers` chain from config.yaml. The cron scheduler reads the chain fresh per tick (`load_config()` at fire time — scheduler.py lines ~513/1350/1904/3461), so editing the chain needs NO gateway restart. Always check what the chain currently is (`grep fallback_providers <profile>/config.yaml`) before assuming it's sane — the 08-15 default was `nemotron-free`, the same historically-flaky model that gave audit_preflight its ResourceExhausted/404s. Put a contract-clean second model first in the chain, ideally a DIFFERENT provider (burst limits are often per-model/per-provider):
  ```bash
  hermes --profile <profile> config set fallback_providers '[{"model": "upstage/solar-pro4", "provider": "openrouter"}, {"model": "qwen/qwen3-30b-a3b-instruct-2507", "provider": "openrouter"}, {"model": "nvidia/nemotron-3-ultra-550b-a55b:free", "provider": "openrouter"}]'
  ```
  Selection from the model scan: solar-pro4 $0.03/$0.12 (5/5 pass, contract-clean), qwen3-30b $0.048/$0.193 (contract-clean), nemotron-free last-resort ($0). **CONFIG-GUARD PITFALL:** you CANNOT `patch`/`write_file` config.yaml — Hermes refuses with "Refusing to write to Hermes config file ... use 'hermes config' instead". Must use `hermes --profile <name> config set <key> '<json>'`. Verify with `hermes --profile <name> config show | grep -A2 fallback`.

Full worked example (which jobs flipped, drift cohort, 429 signal, fallback chain): `references/cron-fleet-ling-route-conversion-2026-08-15.md`.

Retired path keeps being recreated despite a literal sweep? Search **derived** path construction too (`HOME / "Operations"`, `Path.home() / ...`, `pathlib.Path.home() / ...`, `os.path.expanduser("~/...")`) — see `references/retired-path-derived-construction-sweep-2026-08-17.md`.

## Gotcha 19 — Per-job model pins BYPASS the `fallback_providers` chain → a pinned rate-limited model never falls over (2026-08-17)

**Problem:** Every agent cron that pins `model` + `provider` (per Gotcha 18) executes on EXACTLY that pin. The global `fallback_providers` chain in `config.yaml` is only consulted when the **unpinned global default** fails — a per-job pin is a hard override, so the scheduler just retries the same dead/rate-limited model 3× and then fails. The chain is NOT a safety net for pinned jobs, no matter how robust it is.

**Real example (2026-08-17):** All 20 agent crons were pinned on `inclusionai/ling-2.6-flash` (openrouter, served by **Novita's shared pool**). That pool returned `HTTP 429: Provider returned error` (upstream `provider_name: Novita`, `is_byok: False`, `limit_source: upstream_provider_shared_pool`) — every OpenRouter user without a Novita BYOK key shares one cap. 10 of the 20 pinned jobs errored on 429; the `fallback_providers` chain (solar-pro4 → qwen3-30b → nemotron-free, set 08-15) never engaged because every job had a hard pin. The 429 is not "our usage / our key" — it's OpenRouter's shared allocation of a third party's GPUs running hot.

**Fix — switch the whole pinned fleet to a model served by a DIFFERENT provider, not just "a cheaper model":**
- Confirm the replacement's provider on OpenRouter (`curl -s https://openrouter.ai/api/v1/models | grep <id>` → read `pricing`; the served `provider_name` appears in 429 metadata or on the model page). `upstage/solar-pro4` is served by Upstage directly — escaping Novita's pool.
- Update each pinned job without touching schedule/deliver/script: `cronjob action=update job_id=<id> model={"model": "upstage/solar-pro4", "provider": "openrouter"}`.
- Verify by re-running a non-destructive sample through `cronjob action=run` and reading `last_status`. Do NOT trust an old `last_status: error` — it reflects the run before the model change.
- Cost is negligible for cron workloads (solar-pro4 $0.03/$0.12 per M).
- Also update any model-policy memory entry that records the old fleet pin so the next session starts from the new reality.

**How to spot a shared-pool 429 vs a real bug:** scheduler log shows `HTTP 429` → `Retrying API call ... policy=default` → fails after 3 retries, always on the same model, with `provider_name: <host>` and `is_byok: False`. If the same model succeeds at a different time of day (outside the burst window), it's shared-pool congestion, not a code bug — model-switch, don't debug the script.

## Gotcha 20 — Process-counting guard double-counts launcher/wrapper processes → recurring false alert (2026-08-19)

**Problem:** A detection guard that counts live processes **by matching on a command-line substring** absorbs launcher/wrapper processes whose command *embeds* the real process's invocation. Result: the guard reports N+1 processes for one profile and fires a false "two-homes fight / duplicate instance" alert on every tick.

**Real example (2026-08-19):** `hermes_launcher_home_guard.py` (launchd, every 30 min) reported `default` and `orchestrator-hermes` each having **2** live `gateway run` processes. Live `ps` showed only 1 real gateway each. The phantom second was the `hermes_cli.stderr_timestamp` wrapper — a process whose full command line embeds the wrapped gateway's invocation as text:
```
python -m hermes_cli.stderr_timestamp --error-log .../gateway.error.log \
    -- python -m hermes_cli.main --profile orchestrator-hermes gateway run --replace
```
The guard's filter `"gateway run" in line` matched BOTH the real gateway AND the wrapper. Wrappers only appeared for gateway profiles launched with `--external-supervisor` (default + orchestrator-hermes), which is exactly why only those two profiles false-flagged.

**How to spot — verify live before trusting the count:**
```bash
ps aux | grep -E 'hermes_cli' | grep -v grep | grep -E 'gateway' | head
```
Compare the real process table to the guard's claimed count. If every real gateway has exactly one, but the guard reports 2, look for a wrapper/launcher process whose command line *contains* the string you match on.

**Fix — exclude the wrapper, don't just raise the threshold:**
```python
return [l for l in out.splitlines() if GATEWAY_PROC_MATCH in l and "grep" not in l
        and "gateway run" in l
        and "hermes_cli.stderr_timestamp" not in l]   # wrapper embeds the real cmdline
```
Match on the **module that OWNS the process** (`hermes_cli.main`), not the bare substring — a wrapper legitimately carries `gateway run --replace` in its own argv.

**This is a false-positive bug, not real drift.** Fix the detection script (it's the launchd-run source of truth), don't just suppress the alert. LaunchD reads the file fresh each tick — editing the canonical script takes effect without reloading the plist.

**Verification (ad-hoc, no suite exists):** `_ps_lines()` shells out to `ps`, so test it by monkeypatching `subprocess.run` to return a canned process table containing a real gateway + its wrapper + a plain gateway:
```python
def fake_ps(out):
    class R:
        def __init__(s, stdout): s.stdout = stdout
    guard.subprocess.run = lambda *a, **k: R(out)
    return guard._ps_lines()
lines = fake_ps(REAL_GATEWAY + "\n" + WRAPPER + "\n" + PLAIN_GATEWAY + "\n")
assert sum("stderr_timestamp" in l for l in lines) == 0   # wrapper filtered
assert len(lines) == 2                                     # real + plain only
```
Then run the real script end-to-end: `python3 hermes_launcher_home_guard.py` → `OK — 8 profile(s), 1 process each`. Clean up the temp verify script after.

## Gotcha 21 — Auto-push fails on a repo that has git history but NO origin remote (2026-08-19)

**Problem:** A git-inited repo with no remote configured keeps failing `git push origin` in the auto-push routine, alerting repeatedly. The error `fatal: 'origin' does not appear to be a git repository` is NOT a credentials/network failure — it means **no remote exists at all** for that repo.

**How to spot:** `git remote -v` in the repo prints nothing, and `git status -sb` shows `## main` with no upstream. The push routine (`auto_push_all.py`, launchd every 2h) auto-discovers git repos under the home root and tries to push each to origin, so a deliberately-local repo gets flagged every tick.

**Fix — registry `no_push`, don't hardcode a skip in the script:**
`BACKUP_TARGETS.txt` is the **one shared exclusions registry** read by all three scripts (auto-commit-watcher.sh, git_repo_health_check.py, auto_push_all.py). Add the exception there once, not in a script:
```
no_push|/Volumes/Extra/Substrate/_Personal|Ted's personal files; git-inited with no origin remote. Local history only.
```
- `no_push` = still git-commit locally, never push to GitHub. Same as `~/.hermes` (remote-less) and `Clinic` (policy).
- `skip_entirely` = excluded from all git automation. Use `no_push` for a normalized local repo you still want version history on.
- The canonical script's `load_excluded()` parses it — verify: `Personal excluded: True`.

**Also sync the profile copy:** `auto_push_all.py` lives at both `Operations/scripts/` (canonical, launchd-run) and `~/.hermes/profiles/<profile>/scripts/` (stale `github_repo`-only variant). `cp` canonical → profile copy so the two can't drift (Gotchas 4/16). The launchd plist runs the **canonical** path, which honors the registry — so the fix takes effect immediately.

**Resolve the open alert artifact:** `alert_writer.py --resolve --route ai --source auto_push_all.py --title "Auto push failed — <repo>" --resolution "<why cleared>"` moves it `alerts/open/` → `alerts/resolved/`. Then confirm `alerts/open/` no longer holds it.

## Ted's pacing preference (reinforced 2026-08-17) — "test a small subset before expanding everywhere"

A recurring, explicit correction from Ted across sessions and again this one: when a change touches MANY files/jobs, **do not apply it fleet-wide in one pass**. Apply to a small, clearly-defined subset first, **prove it works on that subset** (actually run the changed things and read the result), and get his go-ahead before fanning out to the rest.

- "I wanted to make sure a smaller set fix was going to work before expanding everywhere."
- "test some again ... quicker ones. local script crons and hermes crons" — he names the subset to test.
- "no, not that you changed too many, that we did not do the whole thing ... That's too much at once."

Practical shape:
- For a cron-model change: flip a few internal/non-user-facing jobs, re-run them, confirm `ok`, THEN do the rest.
- For a path/symlink migration: fix and live-verify a handful of writers, confirm the dead path stays absent, then sweep the remaining references — but only after showing the subset worked.
- When he says "test some again," PICK quick local/script crons (no shopping/financial/scraper jobs, no destructive archive/rotate ops) — and state that selection so he knows you avoided the consequential ones.
- Declare the explicit stop — "no further bulk changes until you say so" — after each batch rather than continuing to the next batch autonomously.

## Gotcha 3 — Cloud browser (Browserbase) instability for grocery automation

**Problem:** The cloud browser (Browserbase) has intermittent 502 Bad Gateway errors, timeouts, and slow responses that break automated grocery receipt fetching. The grocery cron (`grocery-receipt-fetcher-auto`, Sun 10am) runs but often fails due to infrastructure instability.

**Workarounds tested:**
1. **Local Playwright script** — Works when not headless (visible browser), but fails in headless mode due to bot detection (ERR_HTTP2_PROTOCOL_ERROR, timeouts)
2. **computer_use tool** — Available in Hermes (`computer_use` toolset enabled) but not directly callable from cron context; drives actual macOS Chrome/Safari
3. **Cloud browser with retry logic** — Current approach: cron job with 3 retries + 30s delay, but infrastructure instability remains

**Best path forward:** Use `computer_use` tool with visible browser for Stage 2 watched sessions, then build session capture → headless replay for Stage 3 unwatched automation. The `computer_use` tool drives your actual macOS Chrome/Safari in background without stealing focus — this bypasses Browserbase entirely.

**Key learning:** Cloud browser infrastructure is not reliable enough for production cron jobs. For critical automated scraping, prefer local browser automation (`computer_use` or non-headless Playwright) over cloud browser.

## Gotcha 5 — Kroger B2C OAuth blocks cloud browsers (2026-06-29)

**Problem:** Harris Teeter (Kroger) uses Microsoft Azure B2C OAuth for login. The redirect chain (harristeeter.com → login.microsoftonline.com → b2clogin.com → back) **blocks cloud/automated headless browsers** (Browserbase, Playwright headless). Cloud browsers cannot complete the OAuth flow.

**Working solution:** Local Playwright with **persistent browser context**.
1. Ted logs in **once manually** in visible browser → cookies + session saved to `/tmp/ht_cookies.json` and persistent profile at `/tmp/ht_session_persist`
2. Cron job reuses the saved session (cookies + profile dir) for all future runs — no login required
3. Script: `grocery_receipt_fetcher.py` at `~/.hermes/scripts/` (synced to profile scripts dir)
4. Cron: `grocery-receipt-staged-fetcher` (weekly Sun 10am, no-agent)

**Key implementation details:**
- Use `launch_persistent_context` with `user_data_dir` to persist the session
- Save cookies explicitly as backup: `await context.cookies()` → `/tmp/ht_cookies.json`
- On subsequent runs: load cookies via `context.add_cookies()` + reuse `user_data_dir`
- Headless mode still fails — must run visible (`headless=False`) even for cron
- Sam's Club still blocked by 2FA/OTP — use print view method when available

**Cron staging pattern (reliability gate):**
- `grocery-receipt-preflight` (Sun 9:30am) checks safe posture before fetch
- `grocery-receipt-staged-fetcher` (Sun 10am) runs only after preflight passes
- Output stages to `Substrate_Finance_Planning/Evidence/Grocery_Receipt_Staging/`
- Human review step before ledger integration

**Key learning:** Kroger B2C OAuth requires persistent browser session. Cloud browsers fail on redirect chains. Local Playwright + saved cookies + persistent profile is the reliable path. Visible browser required (headless detected).

## Gotcha 10 — Cron job user-state dependency pattern (2026-07-11)

**Problem:** Some cron tasks need user state (authenticated browser session, logged-in account, active SSH agent, mounted drive). The cron has no way to request this interactively — it must either succeed autonomously or report cleanly. A cron that says "first do X" without attempting the autonomous path produces a useless delivery.

**The wrong pattern:**
```
1. Tell Ted to log into Store A and Store B
2. Wait for response
3. Then extract receipts
```
This does not work in a cron context — there is no user to respond.

**The right pattern (autonomous attempted extraction):**

1. **Try every dependency independently.** If a dependency is missing (redirect to sign-in, file not found, service unreachable), skip it and note it. Do not abort the whole run because one input is unavailable.
2. **Extract what you can.** The partial result is more valuable than "I couldn't do anything."
3. **Deliver a complete report, not a request.** Structure the output as:
   - What was accomplished (which dependencies succeeded, what was found or not found)
   - What was blocked (which dependencies failed, and how)
   - What's needed for next time (which accounts need a fresh session)
4. **Use the delivery channel correctly.** The cron's final stdout IS the delivery. Format it as a read-now summary. Do NOT prepend "Ted, please..." or "First, make sure..." as a standalone request — those belong as the "What's needed" section of the report.

**When a task explicitly says "message Ted first" and runs as a cron:** The task author designed it for interactive use. A cron run should honor the intent (try to do the work autonomously) but substitute its own deliverable format (a status report summarizing what was achieved and blocked) for the interactive "ask Ted" step. Do not silently skip the task nor hang waiting for a reply that will never come.

**Verification:** The cron output should be actionable without Ted needing to re-run it. If Ted has to trigger a manual re-run after reading the output, the pattern was not followed correctly.

**Real example (2026-07-11):** Grocery receipt cron ("Sunday Night") ran on Saturday. Harris Teeter redirected to sign-in (no active session). Sam's Club was logged in — extraction showed no new orders since Jun 27. Result: partial success delivered as a single report with clear blocked/accomplished breakdown. No re-run needed.

## Gotcha 12 — `deliver:` target mismatch: "no delivery target resolved" (2026-07-17)

**Problem:** Cron jobs with `deliver: "telegram"` (or `"discord"`, `"sms"`, etc.) fail with `last_delivery_error: "no delivery target resolved for deliver=telegram"` when the current profile doesn't have that platform wired up. The job runs and produces output, but the output never reaches the user — it's silently lost to a delivery error.

**Root cause:** The cron author assumed a platform was connected, but:
- The current Hermes profile doesn't have that gateway platform configured
- The profile has the platform configured but the specific chat/channel isn't set
- The `deliver` field references a platform the user connected from a different profile

**How to spot:** `cronjob(action='list')` shows `last_delivery_error` is non-null with a message like `"no delivery target resolved for deliver=telegram"`. The `last_status` may still show `"ok"` — the script ran fine, only delivery failed.

**Fix (in order of preference):**
1. **`deliver: "telegram:<chat_id>"`** (or `"discord:<channel>"`, etc.) — most reliable for agent-based crons that need to reach a specific user DM. Use the chat ID from the user's current session context. This is a hardcoded target that doesn't depend on session state.
2. **`deliver: "origin"`** — sends output to wherever the cron was created (typically the DM of the profile that registered it). **Caveat:** "origin" can fail silently from background cron context — the cron runs and produces output, but the delivery never reaches the user. The `last_status` shows `"ok"` but no message arrives. If the user reports "I didn't get the check-in," switch to option 1.
3. **`deliver: "all"`** — fans out to every connected platform (only if the message should go everywhere).

**Real example (2026-07-18):** `shopping-guru-saturday-order` (job `ed7f38daf0f5`) ran at 9:10am with `last_status: "ok"` and no delivery error, but Ted never received the output in his DM. The cron used `deliver: "origin"` which resolved to the session context where the job was last updated — but the cron runs as a separate background process, so "origin" had no active delivery channel. Fixed by changing to `deliver: "telegram:8547176321"` (Ted's specific Telegram chat ID). Next Saturday's run confirmed delivery worked.

**How to spot a silent delivery failure:** Check `last_delivery_error` on the cron job — if it's `null` (no error) but the user says they didn't receive it, the issue is likely a stale/invalid "origin" target. Read the output file at `~/.hermes/cron/output/<job-id>/<timestamp>.md` to verify the cron actually generated content — if it did, the delivery path is the problem.

**Real example (2026-07-17):** `shopping-guru-wednesday-checkin` (job `399120b5127f`) had `deliver: "telegram"` but no Telegram gateway was configured for the substrate-hermes profile. Fixed by changing to `deliver: "origin"` — the weekly check-in now comes through Ted's DM.

**Note:** This is distinct from the `deliver: "local"` false-error pattern (covered in cron-job-health-audit skill). `local` fails because there's no active chat context. `telegram` fails because the platform isn't wired. Both produce delivery errors but have different root causes.

## Gotcha 14 — Script copied to volume path but cron resolves against LOCAL home (2026-08-02)

**Problem (historical form):** On this Mac there were TWO home paths: the local home `/Users/ted/.hermes/` and the substrate volume `/Volumes/Extra/Substrate/.hermes/` (now RETIRED — that path no longer exists). The gotcha survives in a new form: a script authored in a canonical source dir (e.g. `/Volumes/Extra/Substrate/Operations/scripts/`) but never copied into the **profile execution dir** (`/Users/ted/.hermes/profiles/<profile>/scripts/`) fails identically — see the 2026-09-07 addendum below. Historical statement: copying a script to the volume profile dir while the gateway resolved against the local home caused:

> `Script not found: /Users/ted/.hermes/profiles/substrate-hermes/scripts/mcp_bridge_watchdog.py`

even though the file exists on the volume.

**Real example (2026-08-02):** `mcp-bridge-watchdog` cron created with `script: "mcp_bridge_watchdog.py"` failed on every 10m tick with `Script not found`. The script had been copied to `/Volumes/Extra/Substrate/.hermes/profiles/substrate-hermes/scripts/` but NOT to `/Users/ted/.hermes/profiles/substrate-hermes/scripts/`. Fix: `cp` to the local home path too, then `cronjob(action='run', job_id=...)` to verify.

**Fix:**
```bash
# After writing/editing a no-agent cron script in its canonical source dir,
# ALWAYS copy it into the profile execution dir the cron gateway resolves against:
cp /Volumes/Extra/Substrate/Operations/scripts/<script>.py \
   /Users/ted/.hermes/profiles/substrate-hermes/scripts/<script>.py
# Then re-run the cron and confirm execution_success
```

**How to spot:** `cronjob(action='run')` returns `execution_success: false` with `execution_error: "Script not found: /Users/ted/.hermes/profiles/<profile>/scripts/<name>.py"`. The `ls` of the volume path shows the file exists — don't trust that; check the local path.

**Related:** this is the cron-side variant of the same two-home confusion that breaks script sync (see Gotcha 4 — always sync both locations after editing).

**Addendum (2026-09-07, two-home era over, failure mode alive):** the identical `Script not found: /Users/ted/.hermes/profiles/substrate-hermes/scripts/<name>.py` error recurred twice in one dead-path scan: `worker-ttl-reaper` (d26792493d6b, created 09-06 after the worker-TTL ruling) and `project-room-needs-action-autopickup` (0334b0092139, created 08-21) had both been erroring every tick because their scripts were authored in `/Volumes/Extra/Substrate/Operations/scripts/` and never copied into the profile execution dir. Fix: `cp` into `/Users/ted/.hermes/profiles/substrate-hermes/scripts/` + smoke-run; both verified exit 0. Rule: **a cron script is not registered until it exists in the profile scripts dir — writing it in the source repo is not registration.**

## Gotcha 13 — `cronjob` tool is profile-scoped; system-level entries invisible (2026-07-15)

**Problem:** The `cronjob(action='list')` and `cronjob(action='remove')` Hermes tools operate ONLY on the **current profile's** cron data. They do NOT see entries in the **system-level** registry or other profiles' stores. Calling `cronjob(action='remove', job_id='...')` on a job that lives in the system-level registry returns `"Job with ID '...' not found."` — even though the job exists and is visible in the raw JSON.

**Three cron registries on disk:**
- **System-level (default profile):** `/Users/ted/.hermes/cron/jobs.json`
- **Profile-specific:** `/Users/ted/.hermes/profiles/<profile>/cron/jobs.json`
- (Volume home `/Volumes/Extra/Substrate/.hermes/` retired — do not reference it.)
- The `cronjob` tool only queries the latter from the currently loaded profile.

**How to detect orphaned system-level entries:**
```bash
# Profile-level (what cronjob list shows you)
python3 -c "import json; d=json.load(open('/Users/ted/.hermes/profiles/substrate-hermes/cron/jobs.json')); print(len(d['jobs']))"
# System-level (invisible from cronjob list)
python3 -c "import json; d=json.load(open('/Users/ted/.hermes/cron/jobs.json')); print(len(d['jobs']))"
```

If system-level count > profile-level count, you have orphaned/disabled entries in the system-level registry that `cronjob` can't see or manage.

**Fix — remove system-level entries directly:**
```python
import json
data = json.load(open('/Users/ted/.hermes/cron/jobs.json'))
data['jobs'] = [j for j in data['jobs'] if j.get('id') not in remove_ids]
json.dump(data, open('/Users/ted/.hermes/cron/jobs.json', 'w'), indent=2, default=str)
```

**Verify:**
```python
d = json.load(open('/Users/ted/.hermes/cron/jobs.json'))
print(f'Total: {len(d[\"jobs\"])}, Disabled: {sum(1 for j in d[\"jobs\"] if not j.get(\"enabled\"))}')
```

**First real pass (2026-07-15):** Removed 8 orphaned crons from system-level registry — all were `enabled: false` with migration/paused reasons. None were visible from `cronjob(action='list')` on the substrate-hermes profile. Result: system-level 44 all-enabled, profile-level 49 all-enabled.

## Gotcha 22 — System-level no-agent crons execute in the `hermes serve` process env; reboot race with `launchctl setenv` LaunchAgents (2026-08-29)

**Problem:** Default-profile (`~/.hermes/cron/jobs.json`) no-agent scripts run as children of the **`hermes serve` process spawned by the desktop app** — they inherit THAT process's environment, not launchd's. If the env var a script needs was installed via a `launchctl setenv` LaunchAgent (e.g. `com.ted.hermes-app-home` setting `SUBSTRATE_ROOT`), a reboot can spawn the app (window-restore) BEFORE the setenv agent loads → serve comes up env-less → every wrapper script importing the fail-closed `substrate_root` module dies with `SubstrateRootNotConfigured` on every tick until the app restarts after setenv exists.

**How to attribute the executor:** `sqlite3 ~/.hermes/cron/executions.db` records `pid` per run → `ps -p <pid> -o command`. Serve executor = `hermes_cli.main serve --host 127.0.0.1 --port 0` whose parent is `/Applications/Hermes.app/Contents/MacOS/Hermes`. Check its env with `ps eww -p <pid>`. Jobs run under other pids (profile gateway LaunchAgents with their own plist `EnvironmentVariables`) are unaffected — that's why only system-level jobs broke while profile gateways stayed green.

**Scan the whole at-risk class, not just the failures** — wrappers that haven't fired since the spawn still show `ok` and will fail at next fire (2026-08-29: 2 failing + 3 latent of 5 substrate_root wrappers).

**Fix (race-free, no code change):** Hermes loads `~/.hermes/.env` via `load_hermes_dotenv()` at import time in EVERY invocation (serve, gateway, CLI). Adding the needed var to `.env` makes every future spawn immune to setenv ordering. Caveats: `.env` is nominally secrets-only per vendor docs — a path constant there is pragmatic and was Ted-approved on this box; the scheduler builds script env via `build_subprocess_env()` snapshotting `os.environ`, so a RUNNING env-less serve still needs one app restart to heal (the fix is not retroactive).

**Live verification:** system-level jobs are invisible to the profile-scoped `cronjob` tool AND to the bare CLI. Trigger via:
```bash
HERMES_HOME=/Users/ted/.hermes ~/.hermes/hermes-agent/venv/bin/hermes cron run <job_id>
```
(the CLI resolves `HERMES_HOME` from the caller's shell — a profile shell points it at the profile registry and returns "not found"). Note: a CLI-triggered run executes under the CLI's pid, NOT serve — it proves script health but not the serve env; scheduled ticks keep testing serve until the app restarts.

**Real example (2026-08-29):** Reboot 12:46 → app restored 12:48:45 before setenv ran → serve pid 2971 env-less → `hermes_profile_name_backfill_check` (hourly) + `system_db_contention_monitor` (2-hourly) failed `SubstrateRootNotConfigured`; 3 more substrate_root wrappers (ai-inbox-hygiene, expire_routine_hook_notes, mac-studio-price-alert) latent. Fix: `SUBSTRATE_ROOT=/Volumes/Extra/Substrate` appended to `~/.hermes/.env` (backup `.env.bak-substrateroot-20260829`); contention monitor re-run → `ok`; backfill-check then surfaced its previously-masked REAL finding (desktop-source empty `profile_name`, 5 distinct days). Side find: `~/bin/hermes` stale — real binary `~/.hermes/hermes-agent/venv/bin/hermes`.

---

## Gotcha 23 — Locating a job's output when the layout has changed: legacy dated files vs `<job-id>/` dated dirs (2026-09-07)

**Problem:** Older guidance says output lives at `~/.hermes/cron/output/<job-id>/*.md` (default profile) or
`~/.hermes/profiles/<profile>/cron/output/<job-id>/<timestamp>.md`. In practice the SAME job can have BOTH
shapes on disk at once: legacy flat files `output/<job-id>_YYYYMMDD_HHMMSS.txt` (some jobs stopped writing
those months ago) alongside a CURRENT `<job-id>/` directory holding `<YYYY-MM-DD_HH-MM-SS>.md` files.
If you glob only the legacy flat pattern you conclude "stopped running Aug 13" — false. The job has been
writing into the directory layout the whole time.

**How to check (default profile):**
```bash
ls -lt ~/.hermes/cron/output/ | grep <job-id-prefix>     # both flat files AND the dir show up
ls -lt ~/.hermes/cron/output/<job-id>/                    # dated .md runs inside
```
For named profiles: `~/.hermes/profiles/<profile>/cron/output/<job-id>/`.
A bare hash entry with NO extension may be the live run directory, not a file — always `ls -lt` it.

**Lesson:** when a cron's output looks stale, list the output root with `-t` and check BOTH the flat
`<job-id>*` pattern and the `<job-id>/` directory before declaring the job dead. This bit a live session
2026-09-07: `substrate-morning-briefing` (531b6e8e5f51, substrate-hermes) had flat .txt files ending 2026-08-13
but fresh dated .md runs inside `531b6e8e5f51/` — the "latest" bare-hash file was empty and the dated dir
held today's briefing.


## Annex moved to references/ (2026-09-09)

The per-profile gotchas consolidated during the Sept 2026 skills cleanup
(advisor, brain-hermes, lab-hermes, default-home copies) now live in
[references/profile-consolidated-gotchas.md](references/profile-consolidated-gotchas.md).
Consult it when a cron symptom doesn't match any gotcha above — it covers
profile-dir resolution, watchdog-script design, cross-profile job-ID
collisions, cron-mode tool restrictions, z.ai peak-hour scheduling, and more.
