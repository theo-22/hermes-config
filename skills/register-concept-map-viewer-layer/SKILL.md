---
name: register-concept-map-viewer-layer
description: Add an already-curated Concept Graph domain to the human-visible viewer layer registry, regenerate the canonical visual and mirrors through the installed builder, and prove exact isolated and Merged behavior. Use when nodes already carry one settled domain tag but the viewer lacks its filter button, or when completing a viewer-only follow-up after Map Curator has closed meaning/data work. Do not use to create, edit, classify, or connect nodes or roads, redesign layer membership, change filtering logic, or merge separate graph stores.
metadata:
  category: meta
  write_mode: file
  one_line_use: register and prove one already-curated Concept Graph viewer layer without changing graph data
  fast_pick: "yes"
---

# Register Concept Map Viewer Layer

Expose one settled graph domain as an isolatable viewer layer without reopening graph meaning or treating generated HTML as authority.

## Authority and boundaries

- Start from the exact routed packet or Ted instruction and the live `LAYERS` registry in `/Volumes/Extra/Substrate/Operations/scripts/build_concept_graph_viz.py`.
- Treat `/Users/ted/Control/backend/system.db` as general-graph data authority and the builder as generated-view authority.
- Require the domain membership and expected roads to be settled before editing. Stop and route back to Map Curator if node or road meaning is still open.
- Change one `LAYERS` row only: `dom`, human label, descriptive title, and a distinct color. Preserve node/edge queries, membership logic, empty-layer hiding, filter behavior, and unrelated code.
- Do not add, rewrite, reject, or confirm nodes or roads.
- Treat the canonical map, Daily Desk mirrors, and the separate Clinical outputs the builder rewrites as protected shared surfaces.

## Workflow

### 1. Resolve current state

Read the source packet, target registry, current regeneration receipt, and exact node/road rows. Check each touched repository for inherited changes and resolve the real repo roots before git writes.

Record:

- exact domain, label, expected node IDs, and expected confirmed external neighbors;
- the builder command from the latest valid receipt;
- baseline source/map hashes and mirror parity;
- any existing dirty generated state that belongs to the completed curation pass.

### 2. Claim every write surface

Acquire DB-backed surface claims for:

- `build_concept_graph_viz.py`;
- `/Volumes/Extra/Substrate/Concept_Graph/map.html`;
- `/Users/ted/Control/frontend/public/map.html` and `build/map.html`;
- the canonical and mirror Clinical map paths, because the installed builder rewrites them too;
- the new receipt path.

Stop on any collision. Do not substitute a direct edit of generated HTML.

### 3. Add the registry row

Follow the existing Clinical/State row shape. Choose a color already settled by the packet or presentation system; otherwise choose a distinct accessible color and report that judgment.

Before regeneration, require the source diff to show exactly one registry insertion. If it touches membership or filtering code, stop and repair the diff.

### 4. Run the installed builder

Invoke the same interpreter and script path recorded by the latest accepted receipt. For the current installation:

```bash
/usr/local/bin/python3 /Volumes/Extra/Substrate/Operations/scripts/build_concept_graph_viz.py
```

Capture exit status, stdout counts, canonical/mirror hashes, and whether separate-store outputs stayed byte-identical where no separate-store data changed.

### 5. Run deterministic checks

Use the bundled read-only validator:

```bash
python3 scripts/verify_viewer_layer.py \
  --domain transition \
  --label Transition \
  --expected-node-ids 300,301,302,303,304,305,306,307 \
  --expected-cross-neighbors 239,244,248,249,252,254
```

The validator must return `PASS` for registry presence, exact DB and embedded-payload membership, confirmed external-neighbor equality, embedded crossings, and mirror parity. Treat a failure as a real acceptance failure; do not relax expected IDs to match unexpected live state.

### 6. Prove the live browser behavior

Open the actual served viewer, currently `http://127.0.0.1:5050/map.html`, in a real browser.

1. Snapshot and confirm the new button is visible.
2. Click the new layer and re-snapshot.
3. Read the viewer's visible node IDs: they must equal the expected set.
4. Run the negative control: visible nodes outside the new domain must be empty.
5. Confirm the displayed concept and internal-road counts match the isolated payload.
6. Click `Merged`, re-snapshot, and prove every expected layer node plus every named crossing is visible through the viewer's own `nvis`/`evis` behavior.
7. Inspect console output; separate harmless missing-asset noise from viewer runtime errors.

Static HTML inspection does not replace this step.

### 7. Receipt and closeout

Write one JSON receipt under `/Volumes/Extra/Substrate/Concept_Graph/Regeneration_Receipts/` containing:

- exact source diff and source hash;
- builder command, exit code, counts, canonical path, map hash, and matching mirrors;
- isolated visible IDs, negative-control result, counts, and Merged crossing evidence;
- explicit `nodes_changed: 0` and `edges_changed: 0`;
- prior data-layer receipt and `PASS`, `PARTIAL`, or `FAIL` verdict.

Commit and push only the touched files in each real repository. Preserve unrelated dirty work. If the task came from inbox intake, close its authoritative work-item/packet lifecycle only after every acceptance clause passes. Release all claims and verify none remain for the lane.

## Evidence standard

`PASS` requires all of the following:

- one-row-only source diff;
- installed builder exit 0;
- deterministic validator PASS;
- canonical/general mirror byte parity;
- actual browser button and exact isolated IDs;
- negative control with zero off-domain visible nodes;
- Merged visibility for all expected nodes and crossings;
- zero node/road mutations;
- durable receipt, pushed repositories, and released claims.

Lower-layer proof with browser verification pending is `PARTIAL`.

## Failure modes

- **Meaning reopened:** viewer work quietly edits graph data or membership.
- **Generated-file shortcut:** `map.html` is edited directly instead of rebuilt.
- **Incomplete checkout:** the builder rewrites an unclaimed Clinical or mirror surface.
- **Registry-only assertion:** the row exists, but no served button or exact filter behavior is proven.
- **Merged regression:** isolation works while expected cross-layer roads disappear in Merged.
- **Dirty-state overwrite:** accepted curator output or unrelated changes are discarded or claimed as new work.
- **Receipt inflation:** a prior regeneration receipt is presented as proof of the new viewer row.

## Runtime notes

- Filesystem-capable actors should use live DB/file reads, the installed builder, the bundled validator, and a real browser.
- A role without Operations write authority should route the exact registry task to a full execution seat rather than widening its fence.
- If the builder paths, database, mirrors, server URL, or receipt schema drift, verify the installed path and update this shared skill rather than creating a local fork.
