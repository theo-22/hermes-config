#!/usr/bin/env python3
"""Validate and fingerprint a Markdown work packet against work_packet.v1."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = SCRIPT_DIR.parent / "references" / "work_packet.v1.schema.json"
META_RE = re.compile(r"^\*\*([^*]+):\*\*\s*(.*?)\s*$")
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$")
ABS_PATH_RE = re.compile(r"`(/[^`]+)`")


def parse_packet(text: str) -> tuple[dict[str, str], dict[str, str]]:
    metadata: dict[str, str] = {}
    sections: dict[str, list[str]] = {}
    current: str | None = None
    fence: str | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            fence = None if fence == marker else (marker if fence is None else fence)
            if current is not None:
                sections[current].append(line)
            continue
        if fence is not None:
            if current is not None:
                sections[current].append(line)
            continue
        section_match = SECTION_RE.match(line)
        if section_match:
            current = section_match.group(1).strip()
            sections.setdefault(current, [])
            continue
        if current is None:
            meta_match = META_RE.match(line)
            if meta_match:
                metadata[meta_match.group(1).strip()] = meta_match.group(2).strip()
        else:
            sections[current].append(line)
    return metadata, {key: "\n".join(lines).strip() for key, lines in sections.items()}


def contains_placeholder(value: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, value, flags=re.IGNORECASE) for pattern in patterns)


def report_for(
    path: Path,
    mode: str,
    check_source_paths: bool,
    legacy_authority_override: Path | None = None,
) -> dict[str, object]:
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    metadata, sections = parse_packet(text)
    errors: list[str] = []
    warnings: list[str] = []
    declared_schema = metadata.get("Packet schema")

    report: dict[str, object] = {
        "path": str(path.resolve()),
        "content_sha256": hashlib.sha256(raw).hexdigest(),
        "schema_version": declared_schema or "legacy_unversioned",
        "linter_version": schema["linter_version"],
        "mode": mode,
        "status": "pending",
        "errors": errors,
        "warnings": warnings,
        "legacy_authority_override": (
            str(legacy_authority_override.resolve()) if legacy_authority_override else None
        ),
    }

    if not declared_schema:
        warnings.append("legacy_unversioned: packet has no Packet schema metadata")
        legacy_action = schema["legacy_policy"].get(mode, "warn")
        if legacy_action == "block_requires_recompile":
            errors.append("legacy_dispatch_requires_recompile_to_current_schema")
        elif legacy_action == "block_without_recompile_or_explicit_override":
            if legacy_authority_override is None:
                errors.append("legacy_requires_recompile_or_explicit_authority_override")
            elif not legacy_authority_override.is_file():
                errors.append(
                    f"legacy_authority_override_not_found: {legacy_authority_override}"
                )
        report["status"] = (
            "blocked"
            if errors
            else (
                "legacy_override_pass"
                if legacy_authority_override is not None and mode in {"activation", "dispatch"}
                else "legacy_inspectable"
            )
        )
        return report

    if declared_schema != schema["schema_version"]:
        errors.append(
            f"unsupported_schema: expected {schema['schema_version']}, got {declared_schema}"
        )

    patterns = schema["placeholder_patterns"]
    for field in schema["metadata"]["critical"]:
        value = metadata.get(field, "").strip()
        if not value:
            errors.append(f"missing_critical_metadata: {field}")
        elif contains_placeholder(value, patterns):
            errors.append(f"placeholder_in_critical_metadata: {field}")

    for field in schema["metadata"]["quality"]:
        value = metadata.get(field, "").strip()
        if not value or contains_placeholder(value, patterns):
            warnings.append(f"missing_or_placeholder_quality_metadata: {field}")

    for heading in schema["sections"]["critical"]:
        value = sections.get(heading, "").strip()
        if not value:
            errors.append(f"missing_critical_section: {heading}")
        elif contains_placeholder(value, patterns):
            errors.append(f"placeholder_in_critical_section: {heading}")

    for heading in schema["sections"]["quality"]:
        value = sections.get(heading, "").strip()
        if not value or contains_placeholder(value, patterns):
            warnings.append(f"missing_or_placeholder_quality_section: {heading}")

    status = metadata.get("Packet status", "")
    if status and status not in schema["allowed_packet_statuses"]:
        errors.append(f"invalid_packet_status: {status}")
    if mode in {"activation", "dispatch"} and status != schema["activation_packet_status"]:
        errors.append(
            f"activation_requires_status: {schema['activation_packet_status']}"
        )

    authority_value = metadata.get("Authority reference", "")
    authority = authority_value.lower()
    packet_id = metadata.get("Packet ID", "").lower()
    if authority in {"this packet", "self", packet_id}:
        errors.append("self_authorizing_packet: authority must be external")

    if mode in {"activation", "dispatch"}:
        authority_paths = ABS_PATH_RE.findall(authority_value)
        if not authority_paths:
            errors.append("authority_reference_missing_backticked_absolute_receipt_path")
        for authority_path in authority_paths:
            authority_file = Path(authority_path)
            if authority_file.resolve() == path.resolve():
                errors.append("self_authorizing_packet_path: authority resolves to packet")
            elif not authority_file.is_file():
                errors.append(f"authority_reference_not_found: {authority_path}")

    verification_lines = sections.get("Verification and acceptance gates", "").splitlines()
    matched_gate_lines: list[int] = []
    for label in schema["required_verification_terms"]:
        matches = [
            index
            for index, line in enumerate(verification_lines)
            if re.match(
                rf"^\s*-\s*(?:\*\*)?{re.escape(label)}:(?:\*\*)?\s*\S",
                line,
            )
        ]
        if len(matches) != 1:
            errors.append(f"verification_gate_not_separated: expected one labeled line '{label}'")
        else:
            matched_gate_lines.append(matches[0])
    if len(matched_gate_lines) == 3 and len(set(matched_gate_lines)) != 3:
        errors.append("verification_gate_not_separated: gates share a line")

    return_contract = sections.get("Return contract", "")
    if return_contract and not ABS_PATH_RE.search(return_contract):
        errors.append("return_contract_missing_absolute_durable_path")

    if check_source_paths:
        source_section = sections.get("Source surfaces", "")
        source_paths = ABS_PATH_RE.findall(source_section)
        if not source_paths:
            errors.append("source_surfaces_missing_backticked_absolute_path")
        for source_path in source_paths:
            if not Path(source_path).exists():
                errors.append(f"source_surface_not_found: {source_path}")

    if mode == "dispatch":
        probe_section = sections.get("Cold-probe receipt", "")
        probe_paths = ABS_PATH_RE.findall(probe_section)
        if not probe_paths:
            errors.append("dispatch_requires_cold_probe_receipt_path")
        elif len(probe_paths) > 1:
            errors.append("dispatch_requires_one_cold_probe_receipt_path")
        else:
            probe_path = Path(probe_paths[0])
            if not probe_path.is_file():
                errors.append(f"cold_probe_receipt_not_found: {probe_path}")
            else:
                probe_text = probe_path.read_text(encoding="utf-8")
                packet_hash = report["content_sha256"]
                probe_metadata, _ = parse_packet(probe_text)
                for label in schema["probe_receipt_required_metadata"]:
                    if not probe_metadata.get(label, "").strip():
                        errors.append(f"cold_probe_receipt_missing_metadata: {label}")
                if probe_metadata.get("Result", "").strip() != "PASS":
                    errors.append("cold_probe_receipt_missing_pass_result")
                recorded_hash = probe_metadata.get("Packet SHA-256", "").strip().strip("`")
                if recorded_hash != str(packet_hash):
                    errors.append("cold_probe_receipt_hash_mismatch")

    report["status"] = "blocked" if errors else ("pass_with_warnings" if warnings else "pass")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--mode", choices=("inspect", "activation", "dispatch"), default="inspect")
    parser.add_argument("--check-source-paths", action="store_true")
    parser.add_argument("--legacy-authority-override", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    if not args.packet.is_file():
        print(f"packet not found: {args.packet}", file=sys.stderr)
        return 2

    report = report_for(
        args.packet,
        args.mode,
        args.check_source_paths,
        args.legacy_authority_override,
    )
    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['status']}: {report['path']}")
        print(f"sha256: {report['content_sha256']}")
        for error in report["errors"]:
            print(f"ERROR: {error}")
        for warning in report["warnings"]:
            print(f"WARNING: {warning}")
    return 2 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
