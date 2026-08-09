---
name: image-factory-16x9-replacement-workflow
description: Capture, verify, place, recover, and optionally export Ted-approved native-16:9 Image Factory keepers. Use for one keeper or a frozen batch when exact image identity, collision-safe placement, sidecar preservation, recoverable retries, and proof stronger than output counts are required.
category: meta
write_mode: file
one_line_use: capture exact keepers, finish placement recoverably, and verify optional All_Burn export
fast_pick: "no"
---

# Image Factory 16:9 Replacement Workflow

One canonical cross-runtime procedure for moving approved replacement images from
chat acceptance to verified Image Factory placement. Runtime tools may differ;
the authority, identity checks, evidence, and failure rules do not.

## When to use

- Ted accepts a generated native-16:9 image for Image Factory.
- One accepted keeper needs exact capture and placement.
- A keeper batch is collecting, frozen, awaiting retrieval, or ready to finish.
- A previously interrupted placement needs evidence-based recovery.
- Ted asks to refresh the derived `All_Burn` export after placement.

## When not to use

- Ordinary image exploration with no accepted keeper.
- Files are already in `_Incoming` and no keeper or replacement workflow is
  involved; use Production Intake.
- Canonical Museum taxonomy or exhibit design is the primary task.
- The request is to recreate an old image exactly.

## Core rules

1. Old images and filenames are subject seeds only. Generate fresh native-16:9
   compositions; do not recreate the old composition.
2. Acceptance, exact-byte capture, placement, and export are separate state
   transitions. Never treat one as proof of another.
3. Verify identity before any move. A filename, preview, count, or worker message
   is not image identity.
4. Preserve durable partial state and retry from evidence. Never blindly replay a
   failed multi-step operation.

## Canonical workflow

### A. Audit and generate

1. Start Image Factory in Replacement Program mode.
2. Audit the target category and choose one subject seed or coherent cluster.
3. Generate one native-16:9 candidate at a time and show it to Ted.
4. On rejection, do not capture, stage, or place it.
5. On hold, preserve undecided state without counting it as accepted.

### B. Record acceptance and capture exact bytes

1. Record the accepted title, intended filename, category, chat anchor, verdict,
   and dimensions when known in the canonical keeper manifest.
2. If the exact full-resolution bytes are available in the current session,
   capture them immediately through `image_factory_capture_generated` using
   exact base64 bytes or an allowlisted path visible to the server.
3. Reject thumbnails and previews by comparing dimensions and SHA-256 evidence.
4. Treat capture as durable retrieval only. It does not authorize or prove
   placement.
5. If exact bytes are not available, leave the item accepted but uncaptured and
   use the frozen-batch retrieval route in section C.

Remote ChatGPT paths such as `/mnt/data/...` are not assumed to be mounted on the
Mac MCP host. Do not pass a path merely because it exists in the chat runtime.

### C. Freeze and retrieve only when needed

For a batch whose exact bytes could not be captured at acceptance:

1. Resolve superseded items and ambiguous chat anchors.
2. Require exact unique intended filenames and a server-derived accepted count.
3. Freeze the accepted set and record its digest. Do not mutate frozen membership;
   clone a new collecting batch if membership must change.
4. Prepare retrieval read-only, then dispatch one bounded browser/Hermes worker.
5. The worker may locate only the listed images, download each once under its
   intended filename, and report type, dimensions, bytes, and SHA-256. It must
   stop on ambiguity and has no curatorial authority.
6. Record the worker reference only when the manifest hash and frozen digest
   match.

Do not dispatch a worker per keeper when exact bytes are already available.

### D. Finish placement

Use `image_factory_finish_keeper` for one item or an `items[]` batch.

For every item:

1. Require identity-strength evidence: `known_host_sha256` or a prior exact-capture
   retrieval SHA-256.
2. Preview the exact source, final filename, target category, collision result,
   sidecar, and any retirement proposal.
3. Use dry-run first. Live placement must be no-overwrite and same-folder rename
   semantics must remain recoverable.
4. Preserve the approved title in the sidecar; do not replace it with a filename
   stem or regenerated label.
5. Read back the placed image and sidecar. Verify type, native aspect, dimensions,
   bytes, SHA-256, and final path.
6. Retire an older original recoverably only after the new placement is verified.
7. Record a terminal manifest disposition and durable receipt.

Reject non-publishable targets such as `Rejects`, `assets`, underscore-prefixed,
or dot-prefixed categories.

### E. Recover interrupted operations

Before retrying, inspect the live manifest, filesystem, sidecar, and receipts.

- If capture completed but manifest mutation failed, recover from the durable
  capture evidence rather than downloading again.
- If placement and sidecar completed but the final manifest/receipt write failed,
  use receipt-only recovery after verifying the placed bytes and sidecar.
- If identity evidence, target state, or provenance is ambiguous, stop and report
  the mismatch. Do not infer success or rerun the full operation.
- Repair missing manifest state from verified durable evidence; never overwrite a
  conflicting live state.

### F. Optional `All_Burn` export

Use `image_factory_export_all_burn` only when Ted requests or the authorized
workflow requires the derived export.

1. Preview by default.
2. On confirmed execution, use the fixed refresh implementation rather than an
   arbitrary command path.
3. Treat output names as globally reserved across the export, not merely unique
   within one category.
4. Verify the exact expected name set and, for every output, image decoding,
   dimensions, byte count, and SHA-256.
5. Never accept output count alone as export proof.

### G. Close

Complete only when every accepted item in scope has an explicit terminal state
and all placements, sidecars, retirements, receipts, and requested exports are
verified. Fresh-client ChatGPT acceptance is a separate evidence layer from local
implementation tests or installed-connector proof.

## Capsule handling

For composite operations that require a current capability capsule:

- A valid, same-boot, recently expired capsule may be auto-refreshed once.
- An old, invalid, cross-boot, or otherwise untrusted capsule must fail closed.
- Freshness guards must retain an explicit force-repair path; they must not turn a
  stale or corrupted derived artifact into an unrecoverable dead end.

## Evidence and success criteria

- Acceptance wording and intended filename are preserved in canonical state.
- Captured bytes have verified image type, dimensions, byte count, and SHA-256.
- Placement requires identity-strength evidence and is dry-run/no-overwrite safe.
- Sidecar title and placed image are read back before any retirement.
- Recovery resumes from verified partial state without duplicating work.
- Export verification proves exact names and each file's validity, not just count.
- Local tests, installed-consumer proof, and fresh-client acceptance are reported
  as distinct evidence layers.

## Failure modes

- Treating keeper acceptance as proof that placement happened.
- Passing a chat-runtime path that the MCP host cannot see.
- Capturing a preview or thumbnail as the original.
- Guessing an image, chat anchor, SHA-256, or terminal state.
- Blindly replaying a composite operation after a partial failure.
- Treating worker text, filename, or output count as sufficient proof.
- Checking output-name collisions only inside one category.
- Deleting, overwriting, or retiring before replacement verification.
- Letting a freshness guard block the authorized repair route.
- Claiming fresh-client acceptance from server-side or connector tests.

## Runtime notes

### Image Factory MCP

- `image_factory_keeper_manifest`: keeper and batch lifecycle authority.
- `image_factory_capture_generated`: exact-byte capture when current-session bytes
  are available.
- `image_factory_finish_keeper`: dry-run and live one/batch placement, plus bounded
  evidence-based recovery.
- `image_factory_export_all_burn`: dry-run by default; confirmed refresh uses the
  fixed `refresh_all_burn.sh --force` implementation and verifies all outputs.
- `dispatch_worker`: fallback for one frozen retrieval pass when exact bytes are
  unavailable to the current session.

### Filesystem runtimes

Treat `Image_Factory/ChatGPT/manifests/` as canonical role state and preserve the
same identity, revision, recovery, and evidence rules. Do not hand-edit a live
manifest when the composite tool can perform or recover the transition.

## Update-surfacing backstop

This skill names live tools, schemas, and paths. If live capability truth differs,
preserve the workflow boundaries, record the mismatch, and update this shared
skill rather than creating a local doctrine fork.
