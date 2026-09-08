#!/usr/bin/env python3
"""CLI adapter for the shared friction-flow trace ledger."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CONTROL_BACKEND = Path("/Users/ted/Control/backend")
if str(CONTROL_BACKEND) not in sys.path:
    sys.path.insert(0, str(CONTROL_BACKEND))

import friction_flow  # noqa: E402


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Capture or review friction/flow traces")
    sub = root.add_subparsers(dest="operation", required=True)
    capture = sub.add_parser("capture")
    capture.add_argument("--kind", choices=sorted(friction_flow.TRACE_KINDS), required=True)
    capture.add_argument("--actor", required=True)
    capture.add_argument("--session-ref", required=True)
    capture.add_argument("--task", required=True)
    capture.add_argument("--happened", required=True)
    capture.add_argument("--trajectory-change", required=True)
    capture.add_argument("--route", choices=sorted(friction_flow.ROUTES), default="map_curator")
    capture.add_argument("--owner-target", default="")
    capture.add_argument("--node", action="append", default=[])
    capture.add_argument("--edge", action="append", default=[])
    capture.add_argument("--neighborhood", default="")
    capture.add_argument("--evidence-pointer", default="")
    capture.add_argument("--possible-improvement", default="")
    capture.add_argument("--work-ref", default="")

    listing = sub.add_parser("list")
    listing.add_argument("--status", default="open")
    listing.add_argument("--route", choices=sorted(friction_flow.ROUTES), default="")
    listing.add_argument("--limit", type=int, default=100)

    close = sub.add_parser("disposition")
    close.add_argument("--trace-id", required=True)
    close.add_argument("--status", choices=sorted(friction_flow.DISPOSITIONS), required=True)
    close.add_argument("--actor", required=True)
    close.add_argument("--session-ref", required=True)
    close.add_argument("--note", required=True)
    close.add_argument("--evidence-pointer", default="")
    close.add_argument("--work-ref", default="")
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.operation == "capture":
            result = friction_flow.capture(
                kind=args.kind, actor=args.actor, session_ref=args.session_ref,
                task=args.task, happened=args.happened,
                trajectory_change=args.trajectory_change, route=args.route,
                owner_target=args.owner_target, node_ids=args.node, edge_ids=args.edge,
                neighborhood=args.neighborhood, evidence_pointer=args.evidence_pointer,
                possible_improvement=args.possible_improvement,
                work_ref=args.work_ref or None,
            )
        elif args.operation == "list":
            result = friction_flow.list_traces(
                status=args.status, route=args.route, limit=args.limit,
            )
        else:
            result = friction_flow.disposition(
                trace_id=args.trace_id, status=args.status, actor=args.actor,
                session_ref=args.session_ref, note=args.note,
                evidence_pointer=args.evidence_pointer, work_ref=args.work_ref or None,
            )
    except friction_flow.FrictionFlowError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
