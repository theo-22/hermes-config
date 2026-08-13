#!/usr/bin/env python3
"""Verify active file checkouts or byte parity for generated artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_API = "http://127.0.0.1:5555/api/file-checkouts/active"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized(path: str) -> str:
    return os.path.realpath(os.path.abspath(os.path.expanduser(path)))


def load_checkouts(api: str, timeout: float) -> list[dict[str, Any]]:
    separator = "&" if "?" in api else "?"
    url = f"{api}{separator}{urllib.parse.urlencode({'limit': 500})}"
    with urllib.request.urlopen(url, timeout=timeout) as response:
        payload = json.load(response)
    checkouts = payload.get("checkouts")
    if not isinstance(checkouts, list):
        raise ValueError("checkout API response has no checkouts list")
    return checkouts


def checkout_keys(checkout: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    for field in ("caller_path", "canonical_path", "target"):
        value = checkout.get(field)
        if value:
            keys.add(normalized(str(value)))
    return keys


def checkouts_command(args: argparse.Namespace) -> int:
    try:
        active = load_checkouts(args.api, args.timeout)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": f"checkout API failed: {exc}"}, indent=2))
        return 1

    results: list[dict[str, Any]] = []
    ok = True
    for raw_path in args.path:
        canonical = normalized(raw_path)
        matches = [item for item in active if canonical in checkout_keys(item)]
        item = next((entry for entry in matches if entry.get("actor") == args.actor), None)
        path = Path(canonical)
        exists = path.is_file()
        current_hash = sha256(path) if exists else None

        if item is None:
            result = {
                "path": canonical,
                "ok": False,
                "error": "no active checkout owned by requested actor",
                "holders": sorted({str(entry.get('actor')) for entry in matches}),
            }
            ok = False
        else:
            expected_exists = bool(item.get("expected_exists"))
            expected_hash = item.get("expected_sha256")
            state_matches = exists == expected_exists and (
                not exists or current_hash == expected_hash
            )
            result = {
                "path": canonical,
                "ok": state_matches,
                "claim_id": item.get("id"),
                "actor": item.get("actor"),
                "expected_exists": expected_exists,
                "current_exists": exists,
                "expected_sha256": expected_hash,
                "current_sha256": current_hash,
                "state_matches": state_matches,
            }
            if not state_matches:
                result["error"] = "live file state differs from checkout expectation"
                ok = False
        results.append(result)

    print(json.dumps({"ok": ok, "mode": "checkouts", "results": results}, indent=2))
    return 0 if ok else 1


def parity_command(args: argparse.Namespace) -> int:
    results: list[dict[str, Any]] = []
    hashes: set[str] = set()
    ok = True
    for raw_path in args.path:
        canonical = normalized(raw_path)
        path = Path(canonical)
        if not path.is_file():
            results.append({"path": canonical, "ok": False, "error": "file missing"})
            ok = False
            continue
        digest = sha256(path)
        hashes.add(digest)
        results.append({"path": canonical, "ok": True, "sha256": digest, "bytes": path.stat().st_size})

    identical = ok and len(hashes) == 1
    if not identical:
        ok = False
    print(
        json.dumps(
            {
                "ok": ok,
                "mode": "parity",
                "identical": identical,
                "sha256": next(iter(hashes)) if identical else None,
                "results": results,
            },
            indent=2,
        )
    )
    return 0 if ok else 1


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    subparsers = root.add_subparsers(dest="command", required=True)

    checkouts = subparsers.add_parser("checkouts", help="verify active actor-owned checkout state")
    checkouts.add_argument("--actor", required=True)
    checkouts.add_argument("--path", action="append", required=True)
    checkouts.add_argument("--api", default=DEFAULT_API)
    checkouts.add_argument("--timeout", type=float, default=5.0)
    checkouts.set_defaults(func=checkouts_command)

    parity = subparsers.add_parser("parity", help="verify that all artifacts are byte-identical")
    parity.add_argument("--path", action="append", required=True)
    parity.set_defaults(func=parity_command)
    return root


def main() -> int:
    args = parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
