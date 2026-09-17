---
name: cron-registration-gotchas
description: "Silent cron-registration and execution failure modes, and THE POINTER RULE: a file in a profile scripts dir must be a shim pointing at the tracked script, never a copy of it. Use whenever registering, editing or debugging a Hermes cron job, whenever adding a file to a profile scripts directory, and whenever a script fix appears not to have taken effect."
version: 2.0.0
author: Hermes
authority: "Single source. Lives in /Volumes/Extra/Substrate/Skills and is read by every profile via skills.external_dirs. Do not copy this skill into a profile."
platforms: [macos, linux]
metadata:
  hermes:
    tags: [cron, hermes, debugging, gotcha]
---

# Cron Registration & Execution Gotchas

Every gotcha in this file was earned by a real incident. Underneath the 23
historical numbers there are four recurring failure shapes. This file is
organized by shape, with a symptom table first. Full text of every historical
entry lives in [references/full-gotcha-archive.md](references/full-gotcha-archive.md)
and [references/profile-consolidated-gotchas.md](references/profile-consolidated-gotchas.md) —
consult them when the table doesn't match; they are the evidence base, not the working set.

## Symptom → cause table

| Symptom | Cause | Jump to |
|---|---|---|
| Fix a script, cron still runs the old behavior | Two copies exist; cron runs the profile-local one | A1 |
| `Script not found: <profile>/scripts/<name>.py` but the file exists elsewhere | Script never copied/shimmed into the profile execution dir — authoring it in the source repo is NOT registration | A2 |
| `Script not found` and the script sits in `scripts/_attic*/` | Cleanup sweep orphaned an enabled job (check wrapper children too) | A3 |
| Fix didn't take and the profile file is a *copy*, not a shim | Forked implementations; fix one, the other silently stale | A1 |
| Whole cohort of agent jobs skipping with "config drifted ... spend-guard" | Unpinned model crons broke when fleet config moved; pin them | B1 |
| Pinned cron fails 429 and the fallback chain never engages | Per-job pins bypass `fallback_providers` by design | B2 |
| Cron runs but output never arrives; `last_status: ok` | `deliver:` target mismatch (esp. `origin` from background context) | B3 |
| Silent-when-healthy cron never speaks; can't tell if it ran | No-op watchdog pattern; check `last_run_at` + output dir | B4 |
| Same report filed twice / duplicate sections in a routing log | Same job registered in two profiles, both enabled | C1 |
| Job works but is invisible from the owning profile's cron list | Lives in the default (system-level) registry instead | C2 |
| `cronjob remove` says "not found" though the job exists | The tool is profile-scoped; system-level entries need direct JSON edit | C3 |
| Guard script fires a false duplicate-instance alert | Process counter matched a launcher/wrapper's embedded cmdline | C4 |
| Cron job runs after reboot with `SubstrateRootNotConfigured` | serve-process env lost the launchctl setenv race; fix is `~/.hermes/.env` | C5 |
| Cron "stopped running" on an old date but `last_run_at` is recent | Output moved to the `<job-id>/` dated-dir layout; you globbed the legacy flat pattern | C6 |
| Cron task needs login/user state and delivered a useless "please log in" | Interactive-pattern task authored for cron context; use autonomous-extraction pattern | D1 |
| EINTR `Interrupted system call` kills a sweep mid-run | `iterdir()` over symlinked dir under FS pressure; 3-retry guard | D2 |
| Scan reports zero forever and the metric looks "healthy" | Profile copy has a stale path constant + `if not exists: return 0` | A1 |

## A — Which copy runs? (the #1 recurring failure)

### The pointer rule — read before adding ANY file to a profile scripts dir

**Never put a second copy of a script in a profile scripts directory. Put a pointer.**

Hermes cron resolves a job's `script` field against `$HERMES_HOME/scripts` and
*blocks* any path that resolves outside it (`cron/scheduler.py`). So a file must
exist there. That is a real constraint and it is not going away. What is optional
is whether that file contains logic.

Every "two copies drifted" incident — 2026-06-29, 2026-08-02, 2026-08-13 (a
silently dead scan) — has the same cause: the file in the profile was a copy, so
there were two implementations, and only one of them got fixed. Each of those
entries used to prescribe *remember to sync both*. That prescription is why the
problem recurred three times. Work item #1574 measured the result: 82 diverged
pairs, 17 of them live under cron.

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

TARGET = resolve_substrate_path("Operations/scripts/<name>.py")


if __name__ == "__main__":
    if not TARGET.exists():
        raise SystemExit(f"Missing tracked <thing>: {TARGET}")
    runpy.run_path(str(TARGET), run_name="__main__")
```

Notes that matter in practice:

- **Exit codes propagate.** `runpy` lets `SystemExit` through, so a script that
  exits 1 on findings still reports 1 to cron. Proven in production.
- **`sys.argv` is inherited**, so `--verbose`-style flags still reach the target.
- **Do not use a shim for a script that reads `__file__`** to locate its own
  neighbours; fix the script to take an explicit root first.
- **`os.execv` is an equally valid pointer** when you want a clean process.
- **`substrate_root.py` lives only in the profile scripts dir.** The profile
  resolves *where* Substrate is mounted; the tracked script holds *what to do*.

If a job's prompt (agent mode) also names a script path, delete that instruction —
the `script` field already ran it.

### A1 — The profile-local copy is what executes; it drifts silently

Cron resolves `script` against the profile's scripts dir (default profile:
`~/.hermes/scripts/`; named profile: `~/.hermes/profiles/<profile>/scripts/`).
A copy there can diverge from the canonical source: same function names, stale
path constants. The worst shape is `if not path.exists(): return 0` — the scan
dies silently and the metric reads healthy-zero.

- Diagnose: `diff` the two copies; look at `Path(...)` constants first.
- Fix: repoint the constant **in the copy the cron executes** (or better, convert
  the profile file to a shim per the pointer rule).
- **Watch the metric-activation effect:** after the fix the metric legitimately
  jumps 0 → N. That's the scan turning on, not a regression — say so in the report.
- Registration gotchas in the same family: the `script` field is a literal
  filename (no `python3 foo.py --bar` — use a wrapper for args or non-default
  interpreters); absolute paths are rejected; symlinks out of the dir may be
  rejected (test first).

### A2 — "Authored" is not "registered": the profile execution dir

A script written into `Operations/scripts/` (or any canonical source repo) does
not exist for cron purposes until a file appears in the profile scripts dir the
gateway resolves against. Two batches of jobs broke exactly this way (2026-08-21
and 2026-09-06 creations; repaired 2026-09-07): every tick failed `Script not
found: /Users/ted/.hermes/profiles/<profile>/scripts/<name>.py`.

Rule: **registration = source file + shim/copy in the profile dir + one
successful `cron run`.** Smoke-run immediately after registering; the recorded
`last_error` only self-clears at the next scheduled fire.

### A3 — Attic/orphan sweeps orphan ENABLED jobs' scripts (2026-09-09)

Cleanup passes that move "orphaned" scripts into `scripts/_attic*/` verified
paused/removed jobs but not enabled jobs' references. Two incidents in one week:
`worker-ttl-reaper`'s script and `ht_weekly_sales_fetcher.py` (called by enabled
`shopping-guru-weekly-crossref` **through a shell wrapper** — a two-hop reference
invisible to a job-name/script-field grep).

**Sweep-time rule:** before attic-ing any script, check ALL of:
1. every profile's `cron/jobs.json` `script` field,
2. `.sh` wrapper bodies in every profile scripts dir (wrappers ARE jobs),
3. `grep -r <filename>` across all profile scripts dirs.

If any enabled job resolves to it within two hops, it is not orphaned.

**Repair:** `cp _attic/<script> scripts/<script>`, smoke-run the parent chain
exactly as the cron would (`bash <wrapper>.sh`, not just the swept file), then
`hermes --profile <p> cron run <job>` to clear the recorded error.

Detection: the session-start cron health pulse already catches these — a
`Script not found` on an ENABLED job whose script sits in `_attic*/` is this
gotcha. Restore, don't re-register.

### B — Model config and delivery

#### B1 — Drift-skip: unpinned agent crons break when fleet config moves

Agent crons registered without `model`/`provider` inherit the global config at
registration time. When the fleet default moves (it has twice: 08-14 and 09-08),
every unpinned job skips with `RuntimeError: [drift_skip] Skipped to prevent
unintended spend...`. **The guard is working** — no spend occurred — but it
surfaces as a batch of pulse errors, and the job stays skipped until pinned.

Fix per job: `hermes --profile <p> cron edit <id> --provider <p> --model <m>`
(then `cron run` once to verify and clear the stale error). Sweep the whole
cohort, not one job — grep all profile registries for agent jobs with
`model: null`.

### B2 — Per-job pins bypass `fallback_providers`

A pinned model is a hard override: the global fallback chain never engages for
it. A shared-pool 429 (e.g. Novita congestion on an OpenRouter-routed model)
will fail all pinned jobs 3× then die. Fix is a fleet-level model switch to a
different serving provider, not script debugging. Spot the difference: same
model failing in bursts with `provider_name: <host>`, `is_byok: False`, but
succeeding off-peak = congestion, not a bug.

**Verify which model actually served a session via `state.db`, never the
model's self-report.** `session_model_usage` records every API call as
`(session_id, model, billing_provider, billing_base_url, task)`. This
disambiguates the two shapes that look identical from the outside:

- Config resolution broken → the *primary* model string never appears; nothing
  served.
- Fallback engaged (working as designed) → `session_model_usage.model` shows
  the fallback target with `billing_provider` set — the ONLY route to that
  model when it isn't the primary, so its presence is proof the chain works.

The model answering "I am X" is unreliable (it guesses from its context);
rate-limit fallback mid-test can flip the answer between runs. Ground truth:
the DB row. Verified live 2026-09-12 (lab-hermes → ling-3.0-flash-vl:free:
run 1 served primary, runs 2–3 fell back to z-ai/glm-5.3-flash via openrouter
after rapid-fire 429s). When verifying a new free-tier model, SPACE
verification calls — back-to-back `-z` probes trip the per-key rate window
and fail over, making a correct config look broken.

### B3 — `deliver:` target mismatch: output silently lost

`deliver: "telegram"` fails when the registering profile has no Telegram
gateway; `deliver: "origin"` resolves to nothing from background cron context.
Both show `last_status: ok` — the script ran, the output went nowhere.

- Most reliable: `deliver: "telegram:<chat_id>"` (hardcoded target).
- Silent-failure tell: user says "I didn't get it", `last_delivery_error` null,
  but the output file at `cron/output/<job-id>/` has content → delivery path,
  not the script.

### B4 — No-op watchdog pattern (silent-when-healthy crons)

With `no_agent: true`: empty stdout → nothing delivered; non-empty stdout →
delivered verbatim; non-zero exit → alert. Design health checks to exit 0
silently when healthy, print + exit 1 when not. Verify a silent job ran via
`last_run_at` and the `cron/output/<job-id>/` dir.

Escalation (only with explicit authorization): the same script can attempt
bounded repair (launchctl kickstart/reload), re-verify, and exit 0 on success —
alert only when repair was attempted and failed. Keep a `--no-repair` flag for
testing. Re-verify after repair: a kickstart can succeed while the replacement
process comes up wedged.

## C — Registry topology (which registry, which profile, which process)

### C1 — Duplicate registrations across profiles

Same script, or same named job, registered in two profiles with overlapping
schedules → double-fire, overwritten reports, or duplicate appends to shared
routing logs. Names differing by one character defeat name-based collision
detection. Diagnose by grepping BOTH registries for script name AND job name;
two different ids, same schedule, both enabled = double-fire.

Fix: surface both ids to Ted, disable the non-canonical one (direct JSON edit
for the default registry — the `cronjob` tool can't reach it). Digest/routing
jobs should also dedupe-before-route: if the routing log was written after the
digest was generated, the window is already covered.

### C2 — System-level vs profile registries

Jobs accumulate in the default profile's `jobs.json` while everyone assumes they
run under a named profile. Migrations: create in target first, disable in source
second (zero-gap), same schedule/deliver, shim the script per the pointer rule,
then REMOVE the paused source job after 1–2 verified cycles — paused-forever
zombies pile up (39 were swept 2026-09-07).

### C3 — The `cronjob` tool is profile-scoped

`cronjob list/remove` only sees the current profile's registry. System-level
(default) entries need direct JSON edits or the CLI with `HERMES_HOME` set:
`HERMES_HOME=/Users/ted/.hermes ~/.hermes/hermes-agent/venv/bin/hermes cron run <id>`.

### C4 — Process-counting guards and wrapper processes

A guard matching a command-line substring counts wrapper/launcher processes
whose argv embeds the real invocation (e.g. `hermes_cli.stderr_timestamp -- ...
gateway run`). Fix the filter to match the owning module, not the bare
substring; verify against live `ps` output before trusting the count.

### C5 — System-level crons inherit the `hermes serve` env; reboot race

Default-profile no-agent scripts run as children of the desktop app's serve
process. A `launchctl setenv` var can be missing after a reboot race, killing
every `substrate_root`-importing wrapper with `SubstrateRootNotConfigured`.
Race-free fix: put the var in `~/.hermes/.env` (loaded by every Hermes
invocation). Not retroactive — one app restart heals a running env-less serve.

### C6 — Output layout: legacy flat files vs `<job-id>/` dated dirs

Both shapes coexist on disk. Globbing only the flat `<job-id>_*.txt` pattern
makes a live job look dead. Always `ls -lt` the output root AND the
`<job-id>/` directory before declaring a job stopped.

## D — Cron-context behavior

### D1 — No user in the loop: autonomous extraction pattern

A cron that says "first, ask Ted to log in" is useless in cron context. Try
every dependency independently; skip and note what's blocked; deliver a complete
report (accomplished / blocked / needed-next-time). The cron's stdout IS the
delivery — format it read-now, never as a request awaiting a reply.

### D2 — EINTR kills sweeps over symlinked dirs

`Path.iterdir()` over a symlinked path (the `_AI_Inbox` symlink is the recurring
one) intermittently dies with `Interrupted system call` under filesystem
pressure, aborting the whole run before the report writes. Guard: 3-attempt
retry of the same read; after N failures append a flag and return (skipped
subcheck beats dead sweep). Apply to any `iterdir()`/`scandir()` over symlinked
or network-backed paths.

## Operating preferences (Ted, recurring)

- **Test a small subset before expanding fleet-wide.** Flip a few safe jobs,
  prove them, then fan out. No artificial gating on converted jobs —
  verification-after-run, not restriction-before-run.
- **Migrated/paused jobs get removed after a safety period**, not left paused
  forever.
- **Stale `last_error` self-clears only at the next scheduled fire** — after any
  fix, `cron run` the job once and read the result instead of trusting the
  recorded status.

## Reference material

- [references/full-gotcha-archive.md](references/full-gotcha-archive.md) — every
  historical entry preserved verbatim (per-gotcha real examples, code samples,
  job ids, the model-route conversion workflow and 429 analysis).
- [references/profile-consolidated-gotchas.md](references/profile-consolidated-gotchas.md) —
  per-profile gotchas consolidated from advisor / brain-hermes / lab-hermes /
  default-home copies in the Sept 2026 skills cleanup. Covers profile-dir
  resolution, watchdog-script design, cross-profile job-ID collisions, cron-mode
  tool restrictions, z.ai peak-hour scheduling.
