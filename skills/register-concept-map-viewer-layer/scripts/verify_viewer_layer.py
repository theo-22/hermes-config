#!/usr/bin/env python3
"""Read-only checks for one registered Concept Graph viewer layer."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sqlite3
from pathlib import Path


DEFAULT_SOURCE = Path("/Volumes/Extra/Substrate/Operations/scripts/build_concept_graph_viz.py")
DEFAULT_MAP = Path("/Volumes/Extra/Substrate/Concept_Graph/map.html")
DEFAULT_DB = Path("/Users/ted/Control/backend/system.db")
DEFAULT_MIRRORS = (
    Path("/Users/ted/Control/frontend/public/map.html"),
    Path("/Users/ted/Control/frontend/build/map.html"),
)


def parse_ids(raw: str) -> set[int]:
    try:
        values = {int(value.strip()) for value in raw.split(",") if value.strip()}
    except ValueError as exc:
        raise argparse.ArgumentTypeError("IDs must be comma-separated integers") from exc
    if not values:
        raise argparse.ArgumentTypeError("at least one ID is required")
    return values


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_layers(path: Path) -> list[dict]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "LAYERS" for target in node.targets
        ):
            value = ast.literal_eval(node.value)
            if isinstance(value, list):
                return value
    raise ValueError(f"LAYERS assignment not found in {path}")


def embedded_json(html: str, name: str) -> object:
    match = re.search(rf"const {re.escape(name)} = (.*?);\n", html)
    if not match:
        raise ValueError(f"embedded {name} JSON not found")
    return json.loads(match.group(1))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--expected-node-ids", required=True, type=parse_ids)
    parser.add_argument("--expected-cross-neighbors", required=True, type=parse_ids)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--map", dest="map_path", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--mirror", action="append", type=Path)
    args = parser.parse_args()

    mirrors = tuple(args.mirror) if args.mirror else DEFAULT_MIRRORS
    checks: dict[str, object] = {}
    failures: list[str] = []

    layers = source_layers(args.source)
    source_matches = [
        layer for layer in layers
        if layer.get("dom") == args.domain and layer.get("label") == args.label
    ]
    checks["source_registry_matches"] = len(source_matches)
    if len(source_matches) != 1:
        failures.append("source registry must contain exactly one matching domain/label row")

    html = args.map_path.read_text(encoding="utf-8")
    graph = embedded_json(html, "GRAPH")
    rendered_layers = embedded_json(html, "LAYERS")
    rendered_matches = [
        layer for layer in rendered_layers
        if layer.get("dom") == args.domain and layer.get("label") == args.label
    ]
    checks["rendered_registry_matches"] = len(rendered_matches)
    if len(rendered_matches) != 1:
        failures.append("generated viewer must contain exactly one matching visible layer")

    with sqlite3.connect(args.db) as conn:
        db_ids = {
            row[0] for row in conn.execute(
                "SELECT id FROM concept_bridges WHERE domain=? ORDER BY id", (args.domain,)
            )
        }
        placeholders = ",".join("?" for _ in args.expected_node_ids)
        params = tuple(sorted(args.expected_node_ids)) * 4
        cross_rows = conn.execute(
            f"""
            SELECT from_bridge_id, relation_type, to_bridge_id
            FROM concept_bridge_relations
            WHERE promotion_status='confirmed'
              AND ((from_bridge_id IN ({placeholders}) AND to_bridge_id NOT IN ({placeholders}))
                OR (to_bridge_id IN ({placeholders}) AND from_bridge_id NOT IN ({placeholders})))
            ORDER BY id
            """,
            params,
        ).fetchall()

    checks["db_node_ids"] = sorted(db_ids)
    if db_ids != args.expected_node_ids:
        failures.append("database domain membership differs from expected node IDs")

    graph_nodes = {
        int(node["id"]) for node in graph["nodes"] if node.get("domain") == args.domain
    }
    checks["embedded_node_ids"] = sorted(graph_nodes)
    if graph_nodes != args.expected_node_ids:
        failures.append("embedded viewer domain membership differs from expected node IDs")

    db_neighbors = {
        other
        for source, _kind, target in cross_rows
        for other in ([target] if source in args.expected_node_ids else [source])
    }
    checks["confirmed_cross_neighbors"] = sorted(db_neighbors)
    if db_neighbors != args.expected_cross_neighbors:
        failures.append("confirmed external-neighbor set differs from expected IDs")

    embedded_edges = {
        (int(edge["f"]), edge["t"], int(edge["o"])) for edge in graph["edges"]
    }
    missing_edges = [
        {"from": source, "kind": kind, "to": target}
        for source, kind, target in cross_rows
        if (source, kind, target) not in embedded_edges
    ]
    checks["missing_embedded_crossings"] = missing_edges
    if missing_edges:
        failures.append("one or more confirmed crossings are missing from the embedded payload")

    canonical_hash = sha256(args.map_path)
    mirror_hashes = {str(path): sha256(path) for path in mirrors}
    checks["canonical_sha256"] = canonical_hash
    checks["mirror_sha256"] = mirror_hashes
    if any(value != canonical_hash for value in mirror_hashes.values()):
        failures.append("one or more general-map mirrors differ from the canonical map")

    result = {
        "verdict": "PASS" if not failures else "FAIL",
        "domain": args.domain,
        "label": args.label,
        "checks": checks,
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
