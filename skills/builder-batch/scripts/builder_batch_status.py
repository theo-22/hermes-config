#!/usr/bin/env python3
"""Summarize Builder batch queue state without requiring manual curl/grep."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

STATUS_URL = "http://localhost:5555/api/gpt-status"
BATCH_PATH = Path("/Users/ted/Operations/Builder_Update_Batch.md")
RECEIPT_ROOT = Path("/Users/ted/Operations/reports/GPT_Builder_Receipts")

STATUS_RE = re.compile(r"^\s*(?:[-*]\s*)?\*\*Status:\*\*\s*(.+?)\s*$", re.IGNORECASE)
HEADING_RE = re.compile(r"^#{2,4}\s+(.+?)\s*$")


def fetch_status(timeout: float) -> tuple[dict[str, Any] | None, str | None]:
    request = urllib.request.Request(STATUS_URL, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8")), None
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        return None, str(exc)


def parse_batch(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []

    entries: list[dict[str, str]] = []
    current = "Unheaded item"
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            current = heading.group(1).strip()
            continue
        status = STATUS_RE.match(line)
        if status:
            entries.append({"item": current, "status": status.group(1).strip()})
    return entries


def classify(entries: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    classes = {"pending": [], "done": [], "other": []}
    for entry in entries:
        status = entry["status"].lower()
        if (
            "proof pending" in status
            or "needs proof" in status
            or "needs builder" in status
            or "pending" in status
        ):
            classes["pending"].append(entry)
        elif "proof received" in status or "verified" in status or "complete" in status:
            classes["done"].append(entry)
        else:
            classes["other"].append(entry)
    return classes


def count_receipts(root: Path) -> int:
    if not root.is_dir():
        return 0
    return sum(1 for path in root.rglob("*.json") if path.is_file())


def print_entries(label: str, entries: list[dict[str, str]]) -> None:
    print(f"{label}: {len(entries)}")
    for entry in entries:
        print(f"- {entry['item']}: {entry['status']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize GPT Builder batch queue state.")
    parser.add_argument("--pending", action="store_true", help="print pending batch items only")
    parser.add_argument("--timeout", type=float, default=5.0, help="status API timeout in seconds")
    args = parser.parse_args()

    status, error = fetch_status(args.timeout)
    entries = parse_batch(BATCH_PATH)
    classes = classify(entries)

    if status:
        summary = status.get("summary") or {}
        print(
            "API: "
            f"work_queue={summary.get('work_queue', '?')} "
            f"builder_needs_proof={summary.get('builder_needs_proof', '?')} "
            f"builder_verified={summary.get('builder_verified', '?')}"
        )
    else:
        print(f"API: unavailable ({error})")

    print(f"Batch file: {BATCH_PATH if BATCH_PATH.is_file() else 'missing'}")
    print(f"Receipt files: {count_receipts(RECEIPT_ROOT)}")

    if args.pending:
        print_entries("Pending batch items", classes["pending"])
        return 0

    print_entries("Pending batch items", classes["pending"])
    print_entries("Done batch items", classes["done"])
    if classes["other"]:
        print_entries("Other status items", classes["other"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
