#!/usr/bin/env python3
"""Safely append a cold-readable session contract to one live work item."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


LIVE_DB = Path("/Users/ted/Control/backend/system.db")
DEFAULT_CLAIMS_URL = "http://127.0.0.1:5555/api/claims"
PRIORITIES = {"high", "normal", "low"}


def notes_hash(notes: str | None) -> str:
    return hashlib.sha256((notes or "").encode("utf-8")).hexdigest()


def row_dict(conn: sqlite3.Connection, item_id: int) -> dict:
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM work_items WHERE id = ?", (item_id,)).fetchone()
    if row is None:
        raise RuntimeError(f"work item #{item_id} not found")
    result = dict(row)
    result["notes_sha256"] = notes_hash(result.get("notes"))
    return result


def post_json(url: str, payload: dict) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"claim API HTTP {exc.code}: {body}") from exc


def acquire_claim(claims_url: str, item_id: int, actor: str) -> int:
    result = post_json(
        f"{claims_url}/claim",
        {
            "grain": "task",
            "target": f"work_item:{item_id}",
            "actor": actor,
            "purpose": "Shape live work item into a future-session contract",
        },
    )
    if not result.get("ok"):
        raise RuntimeError(f"claim refused: {json.dumps(result, sort_keys=True)}")
    return int(result["claim_id"])


def release_claim(claims_url: str, claim_id: int, actor: str) -> dict:
    return post_json(
        f"{claims_url}/release", {"claim_id": claim_id, "actor": actor}
    )


def show(args: argparse.Namespace) -> int:
    conn = sqlite3.connect(args.db)
    try:
        output = []
        for item_id in args.item_id:
            item = row_dict(conn, item_id)
            conn.row_factory = sqlite3.Row
            events = conn.execute(
                """SELECT id,timestamp,event_type,actor,old_value,new_value,notes
                   FROM events
                   WHERE entity_type = 'work_item' AND entity_id = ?
                     AND event_type = 'work_item_session_setup'
                   ORDER BY id""",
                (item_id,),
            ).fetchall()
            item["session_setup_events"] = [dict(event) for event in events]
            output.append(item)
        print(json.dumps(output, indent=2))
    finally:
        conn.close()
    return 0


def apply(args: argparse.Namespace) -> int:
    db_path = Path(args.db).expanduser().resolve()
    if args.skip_claim and db_path == LIVE_DB.resolve():
        raise RuntimeError("--skip-claim is forbidden for the live work-items database")
    if args.required_owner is not None and args.clear_required_owner:
        raise RuntimeError("use --required-owner or --clear-required-owner, not both")
    if args.priority is not None and args.priority not in PRIORITIES:
        raise RuntimeError(f"priority must be one of {sorted(PRIORITIES)}")

    requested = {
        "title": args.title,
        "owner": args.owner,
        "priority": args.priority,
        "destination_surface": args.destination_surface,
    }
    if args.required_owner is not None:
        requested["required_owner"] = args.required_owner
    elif args.clear_required_owner:
        requested["required_owner"] = None
    if not args.append_note and all(value is None for value in requested.values()):
        raise RuntimeError("no metadata or session-note change requested")

    claim_id = None
    release_result = None
    if not args.skip_claim:
        claim_id = acquire_claim(args.claims_url, args.item_id, args.actor)

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("BEGIN IMMEDIATE")
        before = row_dict(conn, args.item_id)
        if before.get("state") != args.expected_state:
            raise RuntimeError(
                f"state changed: expected {args.expected_state!r}, found {before.get('state')!r}"
            )
        if before["notes_sha256"] != args.expected_notes_sha256:
            raise RuntimeError(
                "notes snapshot changed; run show again before applying the session contract"
            )

        after = dict(before)
        for field, value in requested.items():
            if field in requested and (value is not None or field == "required_owner"):
                after[field] = value

        if args.append_note:
            note = args.append_note.strip()
            if not note:
                raise RuntimeError("--append-note cannot be blank")
            existing = before.get("notes") or ""
            if note in existing:
                raise RuntimeError("the exact session note is already present")
            after["notes"] = existing.rstrip() + ("\n\n---\n" if existing.strip() else "") + note

        columns = [
            "title",
            "owner",
            "required_owner",
            "priority",
            "destination_surface",
            "notes",
        ]
        conn.execute(
            "UPDATE work_items SET "
            + ", ".join(f"{column} = ?" for column in columns)
            + " WHERE id = ?",
            tuple(after.get(column) for column in columns) + (args.item_id,),
        )
        timestamp = datetime.now(timezone.utc).isoformat()
        old_summary = {column: before.get(column) for column in columns[:-1]}
        new_summary = {column: after.get(column) for column in columns[:-1]}
        conn.execute(
            """INSERT INTO events
               (timestamp,event_type,entity_type,entity_id,actor,old_value,new_value,notes)
               VALUES(?,?,?,?,?,?,?,?)""",
            (
                timestamp,
                "work_item_session_setup",
                "work_item",
                args.item_id,
                args.actor,
                json.dumps(old_summary, sort_keys=True),
                json.dumps(new_summary, sort_keys=True),
                "Cold-readable future-session contract reconciled",
            ),
        )
        conn.commit()
        current = row_dict(conn, args.item_id)
    except Exception:
        if conn is not None:
            conn.rollback()
        raise
    finally:
        if conn is not None:
            conn.close()
        if claim_id is not None:
            release_result = release_claim(args.claims_url, claim_id, args.actor)

    print(
        json.dumps(
            {
                "status": "ok",
                "item_id": args.item_id,
                "notes_sha256": current["notes_sha256"],
                "claim_id": claim_id,
                "claim_release": release_result,
                "current": {
                    key: current.get(key)
                    for key in (
                        "title",
                        "owner",
                        "required_owner",
                        "priority",
                        "destination_surface",
                        "state",
                    )
                },
            },
            indent=2,
        )
    )
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--db", default=str(LIVE_DB))
    sub = result.add_subparsers(dest="command", required=True)

    show_parser = sub.add_parser("show", help="read rows and notes hashes")
    show_parser.add_argument("--item-id", type=int, action="append", required=True)
    show_parser.set_defaults(func=show)

    apply_parser = sub.add_parser("apply", help="guard and apply one session contract")
    apply_parser.add_argument("--item-id", type=int, required=True)
    apply_parser.add_argument("--actor", required=True)
    apply_parser.add_argument("--expected-state", default="pending")
    apply_parser.add_argument("--expected-notes-sha256", required=True)
    apply_parser.add_argument("--title")
    apply_parser.add_argument("--owner")
    apply_parser.add_argument("--required-owner")
    apply_parser.add_argument("--clear-required-owner", action="store_true")
    apply_parser.add_argument("--priority")
    apply_parser.add_argument("--destination-surface")
    apply_parser.add_argument("--append-note")
    apply_parser.add_argument("--claims-url", default=DEFAULT_CLAIMS_URL)
    apply_parser.add_argument(
        "--skip-claim",
        action="store_true",
        help="disposable non-live databases only",
    )
    apply_parser.set_defaults(func=apply)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        return args.func(args)
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
