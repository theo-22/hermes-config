#!/usr/bin/env python3
"""Read-only Hermes session-continuity snapshot and comparison."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import plistlib
import re
import sqlite3
import subprocess
import sys
from typing import Any


def read_backend_version(agent_root: Path) -> str | None:
    init_file = agent_root / "hermes_cli" / "__init__.py"
    try:
        match = re.search(r'^__version__\s*=\s*["\']([^"\']+)', init_file.read_text(), re.MULTILINE)
        return match.group(1) if match else None
    except OSError:
        return None


def read_app_version(app_path: Path) -> str | None:
    try:
        with (app_path / "Contents" / "Info.plist").open("rb") as handle:
            return plistlib.load(handle).get("CFBundleShortVersionString")
    except (OSError, plistlib.InvalidFileException):
        return None


def read_build_stamp(app_path: Path) -> dict[str, Any] | None:
    stamp = app_path / "Contents" / "Resources" / "install-stamp.json"
    try:
        data = json.loads(stamp.read_text())
        return {
            key: data.get(key)
            for key in ("commit", "branch", "builtAt", "dirty", "source")
            if key in data
        }
    except (OSError, json.JSONDecodeError):
        return None


def running_hermes_commands() -> list[str]:
    try:
        output = subprocess.check_output(
            ["ps", "-axo", "command="], text=True, stderr=subprocess.DEVNULL
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    return [
        line.strip()
        for line in output.splitlines()
        if (
            "Hermes.app/Contents/MacOS/Hermes" in line
            or "hermes_cli.main serve" in line
            or "hermes_cli.main dashboard" in line
            or "hermes_cli.main gateway run" in line
        )
        and "hermes_update_continuity.py" not in line
    ]


def snapshot(home: Path, app_path: Path) -> dict[str, Any]:
    db_path = home / "state.db"
    if not db_path.is_file():
        raise FileNotFoundError(f"Hermes database not found: {db_path}")

    uri = f"file:{db_path}?mode=ro"
    connection = sqlite3.connect(uri, uri=True, timeout=10)
    try:
        connection.execute("PRAGMA query_only=ON")
        quick_check = connection.execute("PRAGMA quick_check").fetchone()[0]
        total = connection.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        archived = connection.execute(
            "SELECT COUNT(*) FROM sessions WHERE archived=1"
        ).fetchone()[0]
        null_profiles = connection.execute(
            "SELECT COUNT(*) FROM sessions WHERE profile_name IS NULL OR trim(profile_name)=''"
        ).fetchone()[0]
        profile_rows = connection.execute(
            """
            SELECT COALESCE(NULLIF(trim(profile_name), ''), '<unassigned>'), COUNT(*)
            FROM sessions
            GROUP BY 1
            ORDER BY 1
            """
        ).fetchall()
        newest_started_at = connection.execute(
            "SELECT MAX(started_at) FROM sessions"
        ).fetchone()[0]
    finally:
        connection.close()

    db_stat = db_path.stat()
    wal_path = Path(f"{db_path}-wal")
    agent_root = home / "hermes-agent"
    return {
        "schema": "hermes_update_continuity.v1",
        "home": str(home),
        "database": {
            "path": str(db_path),
            "quick_check": quick_check,
            "total_sessions": total,
            "archived_sessions": archived,
            "null_profile_sessions": null_profiles,
            "sessions_by_profile": dict(profile_rows),
            "newest_started_at": newest_started_at,
            "size_bytes": db_stat.st_size,
            "wal_size_bytes": wal_path.stat().st_size if wal_path.exists() else 0,
        },
        "runtime": {
            "backend_version": read_backend_version(agent_root),
            "installed_app_path": str(app_path),
            "installed_app_version": read_app_version(app_path),
            "installed_app_build": read_build_stamp(app_path),
            "commands": running_hermes_commands(),
        },
    }


def compare(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_db = before["database"]
    after_db = after["database"]
    before_profiles = before_db.get("sessions_by_profile", {})
    after_profiles = after_db.get("sessions_by_profile", {})
    profile_deltas = {
        profile: after_profiles.get(profile, 0) - before_profiles.get(profile, 0)
        for profile in sorted(set(before_profiles) | set(after_profiles))
        if after_profiles.get(profile, 0) != before_profiles.get(profile, 0)
    }
    total_delta = after_db["total_sessions"] - before_db["total_sessions"]
    findings: list[str] = []
    severity = "ok"
    if after_db["quick_check"] != "ok":
        severity = "critical"
        findings.append(f"SQLite quick_check is {after_db['quick_check']!r}")
    if total_delta < 0:
        severity = "critical"
        findings.append(f"physical session row count dropped by {-total_delta}")
    if after["home"] != before["home"]:
        severity = "warning" if severity == "ok" else severity
        findings.append("Hermes home changed")
    if before["runtime"].get("installed_app_build") != after["runtime"].get("installed_app_build"):
        findings.append("installed desktop build changed")
    if not findings:
        findings.append("session corpus and selected runtime identity are stable")
    return {
        "severity": severity,
        "total_session_delta": total_delta,
        "profile_deltas": profile_deltas,
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--home",
        type=Path,
        default=Path(os.environ.get("HERMES_HOME", "/Users/ted/.hermes")),
    )
    parser.add_argument(
        "--app",
        type=Path,
        default=Path("/Applications/Hermes.app"),
    )
    parser.add_argument("--snapshot", type=Path, help="Write the current JSON snapshot")
    parser.add_argument("--compare", type=Path, help="Compare against a prior JSON snapshot")
    args = parser.parse_args()

    try:
        current = snapshot(args.home.expanduser().resolve(), args.app.expanduser())
    except (FileNotFoundError, sqlite3.Error) as exc:
        print(json.dumps({"severity": "critical", "error": str(exc)}, indent=2))
        return 2

    output: dict[str, Any] = {"current": current}
    exit_code = 0 if current["database"]["quick_check"] == "ok" else 2
    if args.compare:
        try:
            prior = json.loads(args.compare.read_text())
            if "current" in prior:
                prior = prior["current"]
            output["comparison"] = compare(prior, current)
            if output["comparison"]["severity"] == "critical":
                exit_code = 2
        except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
            output["comparison"] = {"severity": "critical", "error": str(exc)}
            exit_code = 2

    rendered = json.dumps(output, indent=2, sort_keys=True)
    print(rendered)
    if args.snapshot:
        args.snapshot.parent.mkdir(parents=True, exist_ok=True)
        args.snapshot.write_text(rendered + "\n")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
