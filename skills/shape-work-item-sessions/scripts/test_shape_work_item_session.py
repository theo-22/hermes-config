#!/usr/bin/env python3

import json
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("shape_work_item_session.py")


class ShapeWorkItemSessionTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "system.db"
        conn = sqlite3.connect(self.db)
        conn.executescript(
            """
            CREATE TABLE work_items (
              id INTEGER PRIMARY KEY, title TEXT, type TEXT, source_surface TEXT,
              destination_surface TEXT, owner TEXT, state TEXT, deferred_reason TEXT,
              created_at TEXT, state_changed_at TEXT, related_item_id INTEGER,
              related_session_id INTEGER, notes TEXT, priority TEXT,
              required_owner TEXT, weight TEXT
            );
            CREATE TABLE events (
              id INTEGER PRIMARY KEY, timestamp TEXT, event_type TEXT,
              entity_type TEXT, entity_id INTEGER, actor TEXT, old_value TEXT,
              new_value TEXT, notes TEXT
            );
            INSERT INTO work_items
              (id,title,type,owner,state,notes,priority,required_owner)
            VALUES (7,'Old title','task','claude_code','pending','historical note','low','ted');
            """
        )
        conn.commit()
        conn.close()

    def tearDown(self):
        self.temp.cleanup()

    def run_script(self, *args, expect=0):
        completed = subprocess.run(
            ["python3", str(SCRIPT), "--db", str(self.db), *args],
            text=True,
            capture_output=True,
        )
        self.assertEqual(completed.returncode, expect, completed.stderr)
        return completed

    def test_guarded_update_and_event(self):
        shown = json.loads(self.run_script("show", "--item-id", "7").stdout)[0]
        note_hash = shown["notes_sha256"]
        result = json.loads(
            self.run_script(
                "apply",
                "--item-id",
                "7",
                "--actor",
                "codex",
                "--expected-notes-sha256",
                note_hash,
                "--title",
                "Discussion first",
                "--owner",
                "ted + codex",
                "--clear-required-owner",
                "--priority",
                "normal",
                "--append-note",
                "SESSION CONTRACT 2026-08-13 — discuss before implementation.",
                "--skip-claim",
            ).stdout
        )
        self.assertEqual(result["status"], "ok")
        conn = sqlite3.connect(self.db)
        row = conn.execute(
            "SELECT title,owner,required_owner,priority,notes FROM work_items WHERE id=7"
        ).fetchone()
        event = conn.execute(
            "SELECT event_type,actor FROM events WHERE entity_id=7"
        ).fetchone()
        conn.close()
        self.assertEqual(row[:4], ("Discussion first", "ted + codex", None, "normal"))
        self.assertIn("SESSION CONTRACT", row[4])
        self.assertEqual(event, ("work_item_session_setup", "codex"))

        verified = json.loads(self.run_script("show", "--item-id", "7").stdout)[0]
        self.assertEqual(len(verified["session_setup_events"]), 1)
        self.assertEqual(verified["session_setup_events"][0]["actor"], "codex")

        stale = self.run_script(
            "apply",
            "--item-id",
            "7",
            "--actor",
            "codex",
            "--expected-notes-sha256",
            note_hash,
            "--append-note",
            "another note",
            "--skip-claim",
            expect=1,
        )
        self.assertIn("notes snapshot changed", stale.stderr)


if __name__ == "__main__":
    unittest.main()
