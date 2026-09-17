#!/usr/bin/env python3
"""
verify_sqlite_lock_wait.py — Ad-hoc probe for "script should wait on SQLite lock" fixes.

Holds an exclusive BEGIN EXCLUSIVE lock on a SQLite DB in a background thread,
runs a target script mid-lock, and asserts the script waited (didn't fail
instantly with "database is locked") and exited 0.

Use after editing a cron script to add sqlite3.connect(db, timeout=N):
    python3 verify_sqlite_lock_wait.py <target_script.py> <db_path> [lock_seconds]

Exit 0 = PASS (script waited and succeeded under contention).
Exit 1 = FAIL (script died on the lock or didn't wait).
"""

import os
import subprocess
import sys
import tempfile
import threading
import time
import sqlite3

LOCK_SECONDS = float(sys.argv[3]) if len(sys.argv) > 3 else 8.0
MIN_WAIT = max(1.0, LOCK_SECONDS - 2.0)  # script must have waited most of the hold


def main():
    if len(sys.argv) < 3:
        print("usage: verify_sqlite_lock_wait.py <script.py> <db_path> [lock_seconds]")
        sys.exit(2)

    script = sys.argv[1]
    db_path = sys.argv[2]

    if not os.path.exists(script):
        print(f"FAIL: script not found: {script}")
        sys.exit(1)
    if not os.path.exists(db_path):
        print(f"FAIL: db not found: {db_path}")
        sys.exit(1)

    results = []
    fd, tmp_path = tempfile.mkstemp(prefix="hermes-verify-lock-", suffix=".txt")
    os.close(fd)

    def write(msg):
        results.append(msg)
        with open(tmp_path, "a") as f:
            f.write(msg + "\n")

    def lock_and_release():
        conn = sqlite3.connect(db_path, timeout=0.5)
        try:
            conn.execute("BEGIN EXCLUSIVE")
            write(f"lock: acquired exclusive lock on {os.path.basename(db_path)}")
            time.sleep(LOCK_SECONDS)
            conn.rollback()
            write("lock: released")
        except Exception as e:
            write(f"lock: FAILED to acquire lock: {e}")
        finally:
            conn.close()

    locker = threading.Thread(target=lock_and_release, daemon=True)
    locker.start()
    time.sleep(1.5)  # let the lock settle

    start = time.time()
    proc = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True, timeout=60,
    )
    elapsed = time.time() - start

    write(f"script: exit={proc.returncode} after {elapsed:.1f}s")
    if proc.stdout.strip():
        write(f"script: stdout={proc.stdout.strip()}")
    if proc.stderr.strip():
        write(f"script: stderr={proc.stderr.strip()}")

    locker.join(timeout=10)

    ok = proc.returncode == 0 and elapsed >= MIN_WAIT
    write(f"VERDICT: {'PASS' if ok else 'FAIL'}")
    print("\n".join(results))
    try:
        os.unlink(tmp_path)
    except OSError:
        pass
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
