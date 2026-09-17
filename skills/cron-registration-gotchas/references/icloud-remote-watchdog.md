# Remote System Monitoring via iCloud File Sync

Monitor a remote computer by watching for files it pushes to a shared iCloud location. No agent/software to install on the remote machine — you detect drift by observing what stops arriving.

## The Pattern

1. Remote machine (e.g. Jackie's Mac) saves files to its iCloud Drive → syncs to shared account → appears locally
2. A cron job on your Mac checks the local iCloud sync directory for file freshness
3. Silent when files are appearing; alerts when they stop

## When to Use

- Monitoring a family member's automated backup (Reunion, Time Machine, etc.)
- Any remote system that pushes check-in files to a shared cloud folder
- Things you'd otherwise need Chrome Remote Desktop to check manually

## When NOT to Use

- The remote machine must be on and have iCloud sync working
- Syncing introduces delay — a file created at 3am may not appear locally until later depending on iCloud sync timing
- Not suitable for real-time monitoring (iCloud is not real-time)

## Script Template

```python
#!/usr/bin/env python3
"""Watchdog: Check if [thing] is still running on remote Mac.

Checks a local iCloud-synced directory for a new file in the last N hours.
Silent exit (no output) = everything fine.
Non-zero exit + alert = may have stopped.
"""
import os
import time
from datetime import datetime, timedelta, timezone

SYNCED_DIR = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/RemoteMac/Backups/"
)
HOURS_THRESHOLD = 48
FILE_PREFIX = "ExpectedFile_"  # or a directory name pattern

now = datetime.now(timezone.utc)
cutoff = now - timedelta(hours=HOURS_THRESHOLD)

if not os.path.isdir(SYNCED_DIR):
    print(f"ALERT: Sync directory not found at {SYNCED_DIR}")
    exit(1)

newest_mtime = 0
for entry in os.listdir(SYNCED_DIR):
    if entry.startswith(FILE_PREFIX):
        entry_path = os.path.join(SYNCED_DIR, entry)
        mtime = os.path.getmtime(entry_path)
        if mtime > newest_mtime:
            newest_mtime = mtime

if newest_mtime == 0:
    print(f"ALERT: No matching files found at all in {SYNCED_DIR}")
    exit(1)

newest_dt = datetime.fromtimestamp(newest_mtime, tz=timezone.utc)
if newest_dt < cutoff:
    age_hours = (now - newest_dt).total_seconds() / 3600
    print(
        f"ALERT: No new file in {HOURS_THRESHOLD}h. "
        f"Newest: {newest_dt.strftime('%Y-%m-%d %H:%M UTC')} "
        f"({age_hours:.0f} hours ago)."
    )
    exit(1)

# Silent — everything fine
```

## Cron Registration

```bash
cronjob action=create \
  name="remote-watchdog" \
  schedule="0 9 * * *" \
  script="remote_watchdog.py" \
  no_agent=true \
  deliver=origin
```

## Real Example: Family Backup Watchdog

Created 2026-07-09 for Ted's family (Jackie's Mac → Reunion → iCloud → Ted):

- **What it checks:** `~/Library/Mobile Documents/com~apple~CloudDocs/Mom Files/Reunion_Backups/` for new `.familyfile14` folders
- **Threshold:** 48 hours since last snapshot
- **Failure detected:** No new backup since July 5 — ~113 hours stale at first alert
- **Outcome:** Ted now knows to remote into Jackie's Mac and check Reunion's backup scheduler, rather than discovering weeks later

### Diagnostics: Don't be fooled by folder-name dates

When the watchdog alerts but you see folder names extending to present/future dates (e.g., `...-2026-07-10.familyfile14`, `...-2026-07-11.familyfile14`), check the **actual filesystem modification time**, not the date in the folder name.

If all folders have identical older mtime (e.g., all `Jul 5 16:21`), the remote Mac created the directory **structures** in a batch at that old timestamp — iCloud synced the skeletons, not live backup data. The watchdog correctly uses `os.path.getmtime()` on the directory, so it ignores the name and flags the true staleness.

### Verification Steps When Watchdog Alerts

1. Confirm the watchdog isn't broken: run the script manually and check for `ALERT:` vs a traceback
2. Check if iCloud sync is current: look for recently-modified non-backup files in the same iCloud directory
3. Read the backup status log in the synced directory (e.g., `Reunion Backup Status.txt`, `Reunion Backup History.log`)
4. If steps 1-3 confirm the alert is genuine, the fix requires remote access to the source machine (Chrome Remote Desktop, TeamViewer, etc.)
5. On the remote machine: check if the backup app's scheduler is running, if the source file exists, and if disk space is adequate

## Why This Works for Non-Technical Users

- Jackie doesn't have to install or maintain anything on her Mac
- She doesn't even know the watchdog exists
- The check uses the iCloud sync that's already running
- Ted only hears about it when something breaks
