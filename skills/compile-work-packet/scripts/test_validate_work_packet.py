#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_work_packet.py")
SPEC = importlib.util.spec_from_file_location("validate_work_packet", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def valid_packet(source_path: Path, authority_path: Path, receipt_path: Path) -> str:
    return f"""# Work Packet: Test

**Packet schema:** work_packet.v1
**Packet ID:** test-001
**Packet status:** externally_authorized
**Requested actor:** codex
**Authority reference:** `{authority_path}`
**Compiler version:** compile-work-packet.v1
**Priority:** normal
**Requested completion:** not specified

## Provenance
Ted authorized this bounded test.
## Scope comparison
- Asked: test. Proposing: test. Gap: none. Gap reason: not applicable.
## Why now
The validator needs regression proof.
## Objective
Produce one validated fixture.
## Source surfaces
- `{source_path}`
## Execution lane
Codex, local filesystem, bounded to this fixture.
## In scope
- Validate the fixture.
## Out of scope and boundaries
- No runtime mutation.
## Implementer-owned choices
- Formatting within the fixture.
## Stop-worthy meaning forks
- None; return if authority changes.
## Acceptance criteria
- Validator exits zero.
## Verification and acceptance gates
- Implementation/local proof: unit test.
- Independent verification: separate reviewer.
- Fresh receiving-role acceptance: not required for fixture.
## Return contract
Write the durable return to `{receipt_path}`.
## Stop condition
Stop after validation and return.
## Self-critique
This proves structure, not semantic quality.
## Legacy compatibility
Not applicable; v1 packet.
## Cold-probe receipt
Pending before dispatch with profile, model, hash, and verdict.
"""


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "source.md"
        self.authority = self.root / "authority.md"
        self.receipt = self.root / "receipt.md"
        self.source.write_text("source", encoding="utf-8")
        self.authority.write_text("authority", encoding="utf-8")
        self.packet = self.root / "packet.md"
        self.packet.write_text(
            valid_packet(self.source, self.authority, self.receipt), encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_valid_activation_packet_passes(self) -> None:
        report = MODULE.report_for(self.packet, "activation", True)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["errors"], [])

    def test_missing_authority_blocks(self) -> None:
        text = self.packet.read_text(encoding="utf-8").replace(
            f"**Authority reference:** `{self.authority}`\n", ""
        )
        self.packet.write_text(text, encoding="utf-8")
        report = MODULE.report_for(self.packet, "activation", False)
        self.assertIn("missing_critical_metadata: Authority reference", report["errors"])

    def test_quality_omission_warns_without_blocking(self) -> None:
        text = self.packet.read_text(encoding="utf-8").replace(
            "## Self-critique\nThis proves structure, not semantic quality.\n", ""
        )
        self.packet.write_text(text, encoding="utf-8")
        report = MODULE.report_for(self.packet, "activation", False)
        self.assertEqual(report["status"], "pass_with_warnings")
        self.assertEqual(report["errors"], [])

    def test_legacy_inspect_warns_and_activation_blocks(self) -> None:
        self.packet.write_text("# Historical handoff\n\nDo the bounded thing.\n", encoding="utf-8")
        inspect = MODULE.report_for(self.packet, "inspect", False)
        activation = MODULE.report_for(self.packet, "activation", False)
        self.assertEqual(inspect["status"], "legacy_inspectable")
        self.assertEqual(inspect["errors"], [])
        self.assertIn(
            "legacy_requires_recompile_or_explicit_authority_override",
            activation["errors"],
        )

    def test_legacy_activation_accepts_existing_explicit_override(self) -> None:
        self.packet.write_text("# Historical handoff\n\nDo the bounded thing.\n", encoding="utf-8")
        override = self.root / "legacy-override.md"
        override.write_text("Ted authorizes this legacy packet activation.", encoding="utf-8")
        report = MODULE.report_for(self.packet, "activation", False, override)
        self.assertEqual(report["status"], "legacy_override_pass")
        self.assertEqual(report["errors"], [])

    def test_missing_source_path_blocks_when_checked(self) -> None:
        missing = self.root / "missing.md"
        self.packet.write_text(
            valid_packet(missing, self.authority, self.receipt), encoding="utf-8"
        )
        report = MODULE.report_for(self.packet, "activation", True)
        self.assertIn(f"source_surface_not_found: {missing}", report["errors"])

    def test_hash_is_stable(self) -> None:
        first = MODULE.report_for(self.packet, "inspect", False)["content_sha256"]
        second = MODULE.report_for(self.packet, "inspect", False)["content_sha256"]
        self.assertEqual(first, second)

    def test_self_authorizing_packet_blocks(self) -> None:
        text = self.packet.read_text(encoding="utf-8").replace(
            f"**Authority reference:** `{self.authority}`",
            "**Authority reference:** this packet",
        )
        self.packet.write_text(text, encoding="utf-8")
        report = MODULE.report_for(self.packet, "activation", False)
        self.assertIn("self_authorizing_packet: authority must be external", report["errors"])

    def test_missing_authority_receipt_path_blocks_activation(self) -> None:
        missing = self.root / "ghost-authority.md"
        text = self.packet.read_text(encoding="utf-8").replace(
            f"`{self.authority}`", f"`{missing}`"
        )
        self.packet.write_text(text, encoding="utf-8")
        report = MODULE.report_for(self.packet, "activation", False)
        self.assertIn(f"authority_reference_not_found: {missing}", report["errors"])

    def test_authority_path_resolving_to_packet_blocks_activation(self) -> None:
        text = self.packet.read_text(encoding="utf-8").replace(
            f"`{self.authority}`", f"`{self.packet}`"
        )
        self.packet.write_text(text, encoding="utf-8")
        report = MODULE.report_for(self.packet, "activation", False)
        self.assertIn(
            "self_authorizing_packet_path: authority resolves to packet",
            report["errors"],
        )

    def test_collapsed_verification_gates_block(self) -> None:
        text = self.packet.read_text(encoding="utf-8")
        start = text.index("## Verification and acceptance gates")
        end = text.index("## Return contract")
        collapsed = (
            "## Verification and acceptance gates\n"
            "- Implementation proof, independent verification, and fresh acceptance "
            "are all confirmed by the implementer.\n"
        )
        self.packet.write_text(text[:start] + collapsed + text[end:], encoding="utf-8")
        report = MODULE.report_for(self.packet, "activation", False)
        self.assertEqual(
            len([error for error in report["errors"] if error.startswith("verification_gate_not_separated")]),
            3,
        )

    def test_invalid_status_and_unsupported_schema_block(self) -> None:
        text = self.packet.read_text(encoding="utf-8")
        text = text.replace("work_packet.v1", "work_packet.v2", 1)
        text = text.replace("**Packet status:** externally_authorized", "**Packet status:** complete")
        self.packet.write_text(text, encoding="utf-8")
        report = MODULE.report_for(self.packet, "activation", False)
        self.assertTrue(any(error.startswith("unsupported_schema:") for error in report["errors"]))
        self.assertIn("invalid_packet_status: complete", report["errors"])
        self.assertIn("activation_requires_status: externally_authorized", report["errors"])

    def test_return_requires_absolute_durable_path(self) -> None:
        text = self.packet.read_text(encoding="utf-8").replace(
            f"Write the durable return to `{self.receipt}`.",
            "Return in chat after completion.",
        )
        self.packet.write_text(text, encoding="utf-8")
        report = MODULE.report_for(self.packet, "activation", False)
        self.assertIn("return_contract_missing_absolute_durable_path", report["errors"])

    def test_dispatch_requires_current_pass_receipt(self) -> None:
        probe = self.root / "probe.md"
        text = self.packet.read_text(encoding="utf-8").replace(
            "Pending before dispatch with profile, model, hash, and verdict.",
            f"Pending at `{probe}` before dispatch.",
        )
        self.packet.write_text(text, encoding="utf-8")
        missing = MODULE.report_for(self.packet, "dispatch", False)
        self.assertIn(f"cold_probe_receipt_not_found: {probe}", missing["errors"])

        packet_hash = MODULE.report_for(self.packet, "activation", False)["content_sha256"]
        probe.write_text(
            f"**Result:** PASS\n"
            f"**Packet SHA-256:** `{packet_hash}`\n"
            "**Requested profile:** verifier\n"
            "**Actually served profile:** Hermes Verifier\n"
            "**Actually served model/provider:** flash / provider\n",
            encoding="utf-8",
        )
        passed = MODULE.report_for(self.packet, "dispatch", False)
        self.assertEqual(passed["status"], "pass")

        probe.write_text(
            "**Result:** PASS\n"
            "**Packet SHA-256:** `stale`\n"
            "**Requested profile:** verifier\n"
            "**Actually served profile:** Hermes Verifier\n"
            "**Actually served model/provider:** flash / provider\n",
            encoding="utf-8",
        )
        stale = MODULE.report_for(self.packet, "dispatch", False)
        self.assertIn("cold_probe_receipt_hash_mismatch", stale["errors"])

    def test_legacy_dispatch_requires_recompile_even_with_override(self) -> None:
        self.packet.write_text("# Historical handoff\n\nDo the bounded thing.\n", encoding="utf-8")
        override = self.root / "legacy-override.md"
        override.write_text("Ted authorizes bounded preflight.", encoding="utf-8")
        report = MODULE.report_for(self.packet, "dispatch", False, override)
        self.assertIn("legacy_dispatch_requires_recompile_to_current_schema", report["errors"])

    def test_markdown_autolink_is_not_a_placeholder(self) -> None:
        text = self.packet.read_text(encoding="utf-8").replace(
            "Ted authorized this bounded test.",
            "Ted authorized this bounded test at <https://example.com/decision>.",
        )
        self.packet.write_text(text, encoding="utf-8")
        report = MODULE.report_for(self.packet, "activation", False)
        self.assertEqual(report["errors"], [])

    def test_fenced_heading_does_not_split_section(self) -> None:
        text = self.packet.read_text(encoding="utf-8").replace(
            "Write the durable return to",
            "```text\n## Example heading\n```\nWrite the durable return to",
        )
        self.packet.write_text(text, encoding="utf-8")
        report = MODULE.report_for(self.packet, "activation", False)
        self.assertEqual(report["errors"], [])


if __name__ == "__main__":
    unittest.main()
