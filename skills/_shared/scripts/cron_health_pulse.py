#!/usr/bin/env python3
"""Cron health pulse — check all Hermes profiles for jobs with last_status='error'.
Outputs a summary line if any errors found, nothing if clean.
Designed for session-start checks (quiet when healthy)."""

import json, os, sys
from pathlib import Path

BASE = Path(os.environ["HOME"]) / ".hermes"
PROFILES_DIR = BASE / "profiles"

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
