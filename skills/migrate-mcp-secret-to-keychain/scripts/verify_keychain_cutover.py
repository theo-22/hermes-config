#!/usr/bin/env python3
"""Verify one Keychain-backed MCP cutover without printing the secret."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--service", required=True, help="macOS Keychain service name")
    parser.add_argument("--account", required=True, help="macOS Keychain account name")
    parser.add_argument(
        "--scan-path",
        action="append",
        type=Path,
        required=True,
        help="Active regular file that must not contain the Keychain value; repeat as needed",
    )
    return parser.parse_args()


def load_key(service: str, account: str) -> bytes:
    try:
        result = subprocess.run(
            [
                "security",
                "find-generic-password",
                "-s",
                service,
                "-a",
                account,
                "-w",
            ],
            check=True,
            capture_output=True,
        )
    except FileNotFoundError:
        raise RuntimeError("macOS security command is unavailable") from None
    except subprocess.CalledProcessError:
        raise RuntimeError(
            f"Keychain entry unavailable: service={service!r} account={account!r}"
        ) from None

    key = result.stdout.strip()
    if not key:
        raise RuntimeError(
            f"Keychain entry is empty: service={service!r} account={account!r}"
        )
    return key


def resolve_scan_paths(paths: list[Path]) -> list[Path]:
    resolved: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        try:
            candidate = path.expanduser().resolve(strict=True)
        except FileNotFoundError:
            raise RuntimeError(f"scan path does not exist: {path}") from None
        if not candidate.is_file():
            raise RuntimeError(f"scan path is not a regular file: {candidate}")
        if candidate not in seen:
            seen.add(candidate)
            resolved.append(candidate)
    return resolved


def main() -> int:
    args = parse_args()
    try:
        key = load_key(args.service, args.account)
        paths = resolve_scan_paths(args.scan_path)
    except RuntimeError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1

    contaminated = [path for path in paths if key in path.read_bytes()]
    if contaminated:
        print("FAIL plaintext Keychain value remains in active file(s):", file=sys.stderr)
        for path in contaminated:
            print(f"- {path}", file=sys.stderr)
        return 1

    print(
        f"PASS Keychain entry present: service={args.service!r} account={args.account!r}"
    )
    print(f"PASS active plaintext copies absent across {len(paths)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
