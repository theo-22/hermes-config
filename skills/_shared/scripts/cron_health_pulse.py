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

# Default profile
jobs_file = BASE / "cron" / "jobs.json"
if jobs_file.exists():
    with open(jobs_file) as f:
        data = json.load(f)
    for job in data.get("jobs", []):
        if job.get("last_status") == "error" and job.get("enabled", True) is not False:
            errors.append({
                "profile": "default",
                "name": job.get("name", "?"),
                "error": (job.get("last_error") or job.get("last_delivery_error") or "?")[:200]
            })

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
            errors.append({
                "profile": prof_dir.name,
                "name": job.get("name", "?"),
                "error": (job.get("last_error") or job.get("last_delivery_error") or "?")[:200]
            })

if not errors:
    sys.exit(0)

print(f"⚠️  Cron health: {len(errors)} job(s) with errors")
for e in errors:
    print(f"   [{e['profile']}] {e['name']}: {e['error']}")
    print()
sys.exit(0)
