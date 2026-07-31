---
name: repair-pieces-runtime
status: active
description: Diagnose and repair PiecesOS when Pieces "isn't working" — the MCP is disconnected, an ambient/LTM query fails, the desktop app shows "Pieces Core Services Unavailable," or a troubleshooting page pops up claiming a corrupted database. Use this whenever Pieces appears broken, and especially right after a Pieces auto-update, before restarting the Mac or letting the app "clean" anything. Three occurrences to date with three different root causes and the same fix, and the database has never actually been corrupt. Also use when Pieces seems slow to come back after a restart — a large database legitimately takes minutes, and impatience is the usual mistake. Do not use for Pieces MCP client-config questions (Pieces writes those itself; see Notes) or for deciding whether Pieces is worth keeping (that's `pieces-ambient-lead-evaluation`).
category: meta
write_mode: file
one_line_use: alive but not serving → back up, quit fully, relaunch, verify with a real query
fast_pick: "yes"
---

# Repair Pieces Runtime

**PiecesOS fails in one characteristic way: alive but not serving.** The process is up, so a restart of the Mac doesn't help — it relaunches straight back into the broken state. Three occurrences, three unrelated causes, one fix.

**The database has never been corrupt.** Not once, including the time the app said so in its own error URL. Assume it is fine until a *bundled-sqlite* check says otherwise.

## Recognise it in one command

```bash
pgrep -fl "Pieces OS"; curl -s -o /dev/null -w "health:%{http_code}\n" --max-time 5 http://localhost:39300/.well-known/health
```

`health:000` (connection refused) while the process is running **is** the signature. Then separate the two states that look identical from outside:

```bash
PID=$(pgrep -f "Pieces OS.app/Contents/MacOS" | head -1)
ps -o pid,etime,%cpu -p $PID
lsof -p $PID 2>/dev/null | grep -c couchbase.cblite2
```

| reading | meaning | action |
|---|---|---|
| **0% CPU, 0 open handles** | already finished failing, parked | repair — go to the sequence |
| **150–200% CPU, handles open, a child `sqlite3` visible** | still doing its startup integrity check | **wait.** This is normal and can take minutes |

Waiting is the most common correct action and the most commonly skipped one.

## The repair sequence

**1. Back up first — always.** The app may offer to "clean" a database it wrongly believes corrupt.

```bash
mkdir -p /Volumes/Extra/PiecesOS_Backup && \
cp /Volumes/Extra/com.pieces.os/production/Pieces/couchbase.cblite2/db.sqlite3 /Volumes/Extra/PiecesOS_Backup/ && \
cmp /Volumes/Extra/com.pieces.os/production/Pieces/couchbase.cblite2/db.sqlite3 /Volumes/Extra/PiecesOS_Backup/db.sqlite3 && echo "backup verified identical"
```

~1.5GB, seconds, and Extra has hundreds of GB free. Never skip it.

**2. Quit fully, then relaunch.** A Mac restart is not a substitute.

```bash
kill -TERM $PID; sleep 4; pgrep -fl "Pieces OS"     # expect empty
open -a "/Volumes/Extra/Apps/Pieces OS.app"
```

**3. Wait for the integrity check.** It runs `PRAGMA quick_check(1)` on startup. At 1.3GB this took 2–3 minutes; at 1.5GB it took ~50s after a clean relaunch. Connection-refused during this window is **not** failure.

```bash
for i in $(seq 1 90); do
  c=$(curl -s -o /dev/null -w "%{http_code}" --max-time 4 http://localhost:39300/.well-known/health)
  [ "$c" = "200" ] && { echo "healthy after ~$((i*10))s"; break; }
  pgrep -f "Pieces OS.app/Contents/MacOS" >/dev/null || { echo "process died"; break; }
  sleep 10
done
```

**4. Verify with a REAL query — a port check is not verification.** (From Codex's saved repair knowledge; a 200 can precede data being reachable.)

```bash
/Users/ted/.hermes/hermes-agent/venv/bin/python3 /Users/ted/.hermes/scripts/pieces_query.py count
```

Expect conversations / ltm_vision_events / assets. **Only this counts as fixed.**

**5. The desktop app does not auto-retry.** If it still shows "Pieces Core Services Unavailable… POST /connect", click its own **Try again** once health returns 200.

## The three occurrences — different causes, same fix

| date | cause | note |
|---|---|---|
| 2026-07-09 | data dir trashed as "unused" | `/Volumes/Extra/com.pieces.os` is LIVE, symlinked from `~/Library/com.pieces.os`. Never move it. Data was intact throughout |
| 2026-07-22 | Ted and CC independently restarted it during a high-CPU episode | coincidental with a Hermes cleanup; **verify each failure against its own dependency chain before assuming a shared cause** |
| 2026-07-31 | **auto-update** (Sparkle) wrote a new version, whose startup check timed out on a DB grown 1.3→1.5GB | error URL read `failed_to_clean_corrupted_database&os=UNKNOWN_TIMEDOUT`. Symlink held fine; install location was not the cause |

**Expect recurrence on future updates, and increasingly as the database grows** — timeout is the failure mode. The first launch after an update deserves patience, not intervention.

## Notes that save time

**Only the bundled sqlite can read that database.** The system `sqlite3` fails with `unknown tokenizer: unicodesn` — Couchbase Lite's stemming tokenizer. That is a missing extension on your side, **not** damage to the file. Use:

```
/Volumes/Extra/Apps/Pieces OS.app/Contents/Resources/sqlite3
```

**A crash report at the moment you `kill -15` is macOS logging your own signal.** Check the report's `procLaunch` timestamp against when you sent it before treating it as a new fault.

**Client MCP configs are Pieces' own.** It writes `~/.claude.json`, `~/.codex/config.toml`, and VS Code's `mcp.json` itself under the name `pieces` at `localhost:39300`, and creates the matching skill file. Do not hand-repair those or assume a duplicate will be created — verified 2026-07-31.

**Ports:** 39300 plus a dynamic second port. Any other port seen in Pieces marketing screenshots is not this machine.

## Watch status

Watch for: someone restarting the Mac instead of the app; someone skipping the backup; someone reading a slow integrity check as a hang and killing it mid-check; a "fixed" call made on a health 200 without a real query. Review after 3 invocations or 30 days.

Related: `reference_pieces_os_live_data_dir` (the incident history this generalises) · `pieces-mcp` (tool guide, written by the app) · `pieces-ambient-lead-evaluation` (whether Pieces earns its place — a different question).
