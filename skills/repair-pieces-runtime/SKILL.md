---
name: repair-pieces-runtime
description: Diagnose and repair Pieces when PiecesOS, ambient/LTM queries, scheduled ingestion, continuity digests, or downstream reporting appear broken. Use this before restarting the Mac, letting Pieces clean its database, changing a model pin, or accepting an ambient answer as current runtime truth. Distinguishes the PiecesOS runtime from Hermes producer jobs and their report consumers. Do not use for Pieces MCP client-config questions (Pieces writes those itself; see Notes) or for deciding whether Pieces is worth keeping (that's `pieces-ambient-lead-evaluation`).
metadata:
  status: active
  category: meta
  write_mode: file
  one_line_use: prove runtime, producer jobs, and report consumers separately; repair only the failed layer
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

## If a real query works but reporting still looks stopped

Do **not** restart PiecesOS. A healthy Pieces query proves only the capture/runtime layer. Check the complete chain:

| layer | current proof | common false diagnosis |
|---|---|---|
| PiecesOS | `pieces_query.py count` returns real corpus counts | process or HTTP health alone |
| producer jobs | exact active-profile job has current `ok`, zero failure streak, and expected snapshots | an old error or paused duplicate is treated as current |
| consumer | current digest exists and the installed reader returns it | missing report is blamed on PiecesOS or ingestion |

### 1. Verify the producers, by profile

Inspect the live dashboard or the exact profile registries. Do not confuse the paused legacy copies under the default profile with the active jobs:

- `brain-hermes`: `pieces-to-brain-ingestion`
- `substrate-hermes`: `pieces-continuity-daily`, `pieces-digest-router`, `pieces-capture-review`, and `meta-agent-sweep`

For each relevant job, check `enabled`, `last_run_at`, `last_status`, `last_error`, `failure_streak`, and `next_run_at`. For agent jobs protected by the spend-drift guard, also require `provider_snapshot` and `model_snapshot` to match the current explicit provider/model. A model-drift error in an ambient transcript may describe a real **past** failure that has already been pinned and cleared.

Silence is not automatically failure:

- `pieces-to-brain-ingestion` is weekly, not daily.
- `pieces-capture-review` deliberately returns `[SILENT]` when nothing clears its durability bar.
- `pieces-continuity-daily` writes the digest file silently by default.

### 2. Verify the producer artifact

The live digest directory is:

```text
/Volumes/Extra/Substrate/Hermes/Working/
```

Require a current `pieces_continuity_YYYY-MM-DD.md` with real content before calling continuity generation healthy.

### 3. Verify the actual consumer path

The Project Room reader has two active copies:

```text
/Volumes/Extra/Substrate/Operations/scripts/meta_agent_sweep.py
/Users/ted/.hermes/profiles/substrate-hermes/scripts/meta_agent_sweep.py
```

`PIECES_DIGEST_DIR` must resolve to `/Volumes/Extra/Substrate/Hermes/Working`. `/Users/ted/Hermes/Working` is retired and does not exist. If a digest exists but a Project Room report says `Pieces digest: not found`, inspect both copies for that retired path before touching PiecesOS, cron schedules, or model settings.

After a path repair, compile both scripts and exercise each copy's `get_pieces_digest()` against the current digest header. The installed profile copy is what the `meta-agent-sweep` scheduler executes; changing only the Operations source is not runtime proof.

### 4. Treat Pieces' own explanation as a lead

Pieces can synthesize captured ChatGPT, Claude, Terminal, and Hermes text. That makes it useful for locating evidence, but it does not give the answer live authority over current processes, registries, or files. Reconcile every present-tense claim against the live layer it names.

## The four occurrences — different causes, same fix

| date | cause | note |
|---|---|---|
| 2026-07-09 | data dir trashed as "unused" | `/Volumes/Extra/com.pieces.os` is LIVE, symlinked from `~/Library/com.pieces.os`. Never move it. Data was intact throughout |
| 2026-07-22 | Ted and CC independently restarted it during a high-CPU episode | coincidental with a Hermes cleanup; **verify each failure against its own dependency chain before assuming a shared cause** |
| 2026-07-31 | **auto-update** (Sparkle) wrote a new version, whose startup check timed out on a DB grown 1.3→1.5GB | error URL read `failed_to_clean_corrupted_database&os=UNKNOWN_TIMEDOUT`. Symlink held fine; install location was not the cause |
| 2026-08-14 | down most of a week; process had **already exited** — no process at all, health `000` — at DB 1.7GB / 434,321 pages | clean relaunch reached health 200 in **~10 seconds**; verified by real query (127 conversations, 768 ltm_vision_events). Database healthy: `quick_check` returns `ok` |

**Expect recurrence on future updates, and increasingly as the database grows** — timeout is the failure mode. The first launch after an update deserves patience, not intervention.

**Size alone does not predict a slow check (added 2026-08-14).** At 1.7GB — larger than the 1.5GB that timed out on 07-31 — the startup check finished in ~10 seconds on a clean relaunch. A check that grinds for minutes is therefore evidence of a **contended or stuck prior instance**, not of the database being too big. If the check is slow, look for another process holding the file before concluding the store needs trimming.

**A wedged instance can leave no process behind.** On 08-14 the "won't boot" state was `pgrep` empty and health `000` — nothing to wait for and nothing to kill. Check for the process before deciding whether to wait: the table near the top of this skill covers alive-but-busy and alive-but-parked, and this is a third state, *gone*. Relaunch immediately; do not wait.

### Diagnostic traps hit on 2026-08-14 — all cost time, all avoidable

- **Piping the integrity check kills it.** `sqlite3 ... 'PRAGMA quick_check(1);' | head -5` returns in seconds with no output because `head` closes the pipe. That is SIGPIPE, not a result. Run it unpiped and let it finish.
- **`du -sh` on the data dir reports 0B.** It does not follow the symlink. Use `du -sh -H`, or measure `/Volumes/Extra/com.pieces.os` directly.
- **Do not reformat `ls -ld` output on that path.** A `sed` that strips the line's tail removes the `-> /Volumes/Extra/com.pieces.os` target and makes a symlink look like a real directory — which then makes 9.3GB appear to sit on the internal drive (16GB free) rather than on Extra (542GB free). Read the raw `ls -ld` output.

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
