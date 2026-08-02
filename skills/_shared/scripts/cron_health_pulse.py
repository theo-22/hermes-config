#!/usr/bin/env python3
"""Cron health pulse — check all Hermes profiles for jobs with last_status='error'.
Outputs a summary line if any errors found, nothing if clean.
Designed for session-start checks (quiet when healthy)."""

import json, os, sys
from pathlib import Path

# Live Hermes home moved to the Substrate drive in the 2026-07 flatten migration;
# ~/.hermes is a dormant twin. Honor HERMES_HOME, fall back to the live Substrate
# path, and only then to the legacy ~/.hermes. (Fixed 2026-07-16 after the pulse
# silently reported "healthy" while 8 live cron jobs sat in error state.)
_candidates = [
    os.environ.get("HERMES_HOME"),
    "/Volumes/Extra/Substrate/.hermes",
    str(Path(os.environ["HOME"]) / ".hermes"),
]
BASE = next(
    (Path(p) for p in _candidates if p and (Path(p) / "cron" / "jobs.json").exists()),
    Path(_candidates[1]),
)
# Profiles directory — cannot derive from BASE because HERMES_HOME may point
# to a specific profile dir (common in cron context), making BASE / "profiles"
# resolve to e.g. ~/.hermes/profiles/substrate-hermes/profiles which doesn't
# exist. Look in canonical locations instead.
KNOWN_PROFILES_DIRS = [
    Path.home() / ".hermes" / "profiles",
    Path("/Volumes/Extra/Substrate/.hermes") / "profiles",
    BASE / "profiles",
]
PROFILES_DIR = next(
    (p for p in KNOWN_PROFILES_DIRS if p.exists()),
    BASE / "profiles",
)

errors = []
findings = []
seen_job_ids = set()


def classify(job):
    """Classify a job's last_status='error' into a real error or a by-design finding.

    No-agent watchdog jobs (silent on success, loud on findings) exit 1 with
    stdout when they find something to report — that is a *finding*, not a
    failure. Exit-2+ or exit-1-with-stderr stays a real error. The stdout/stderr
    sections are embedded in the last_error string itself ('\nstdout:\n' vs
    '\nstderr:\n'). (Patch 2026-08-01 per brain-hermes finding: pulse was
    conflating watchdogs with broken jobs.)
    """
    job_id = job.get("id")
    if job_id and job_id in seen_job_ids:
        return  # already counted — avoids double-read when HERMES_HOME is a profile dir
    if job_id:
        seen_job_ids.add(job_id)
    err = job.get("last_error") or job.get("last_delivery_error") or ""
    err_lower = err.lower()
    has_stdout = "\nstdout:\n" in err
    has_stderr = "\nstderr:\n" in err
    is_watchdog_finding = (
        "exited with code 1" in err_lower
        and has_stdout
        and not has_stderr
    )
    entry = {
        "name": job.get("name", "?"),
        "error": err[:200],
    }
    if is_watchdog_finding:
        findings.append(entry)
    else:
        errors.append(entry)


# Default profile
jobs_file = BASE / "cron" / "jobs.json"
if jobs_file.exists():
    with open(jobs_file) as f:
        data = json.load(f)
    for job in data.get("jobs", []):
        if job.get("last_status") == "error" and job.get("enabled", True) is not False:
            classify(job)

# Per-profile
for prof_dir in sorted(PROFILES_DIR.iterdir()):
    if not prof_dir.is_dir():
        continue
    jpath = prof_dir / "cron" / "jobs.json"
    if not jpath.exists():
        continue
    with open(jpath) as f:
        data = json.load(f)
    for job in data.get("jobs", []):
        if job.get("last_status") == "error" and job.get("enabled", True) is not False:
            classify(job)

if not errors and not findings:
    sys.exit(0)

if errors:
    print(f"⚠️  Cron health: {len(errors)} job(s) with errors")
    for e in errors:
        print(f"   [error] {e['name']}: {e['error']}")
        print()
if findings:
    print(f"🔎 Cron watchdogs: {len(findings)} finding(s) (by-design exit 1 — inspect, not an error)")
    for e in findings:
        print(f"   [finding] {e['name']}: {e['error']}")
        print()
sys.exit(0)
