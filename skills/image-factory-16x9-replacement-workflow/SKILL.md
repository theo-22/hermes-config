---
name: image-factory-16x9-replacement-workflow
description: Queue atomic replacement subjects, capture Ted-approved raw keepers exactly, hand them to the deterministic Image Processor, and preserve separate downstream placement/retirement proof. Use when exact identity, resumable lifecycle, safe replay, and receipts stronger than output counts are required.
metadata:
  category: meta
  write_mode: file
  one_line_use: queue atomic subjects, capture exact keepers, process deterministically, and keep placement separate
  fast_pick: "no"
---

# Image Factory 16:9 Replacement Workflow

One canonical cross-runtime procedure for moving replacement subjects through
durable queue, creative judgment, exact raw capture, deterministic processing,
and a separate downstream placement boundary. Runtime tools may differ; the
authority, identity checks, evidence, and failure rules do not.

## When to use

- Ted accepts a generated native-16:9 image for Image Factory.
- One accepted keeper needs exact capture and deterministic processing.
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
2. Generation, judgment, exact-byte capture, processing, placement, and export are separate state
   transitions. Never treat one as proof of another.
3. Verify identity before any move. A filename, preview, count, or worker message
   is not image identity.
4. Preserve durable partial state and retry from evidence. Never blindly replay a
   failed multi-step operation.

## Canonical workflow

### A. Audit and generate

1. Start Image Factory in Replacement Program mode.
2. Audit the target category and choose one subject seed or coherent cluster.
3. Create or resume an `image_factory_work_queue` range tagged
   `image_factory` and the program tag, with one atomic child per intended image.
4. Generate one native-16:9 candidate per child and show it to Ted.
5. On rejection or retry, record the durable side outcome/history; do not
   capture, process, or place that candidate.
6. On hold, preserve undecided state without counting it as accepted.

### B. Record acceptance and capture exact bytes

1. Record keep/reject judgment on the atomic work item. Historical keeper
   manifests remain compatibility state; new lists use the tagged queue.
2. If the exact full-resolution bytes are available in the current session,
   capture them immediately through `image_factory_capture_generated` using
   exact base64 bytes or an allowlisted path visible to the server, linked to
   `work_item_id` and its expected typed revision.
3. Reject thumbnails and previews by comparing dimensions and SHA-256 evidence.
4. Treat capture as durable raw-source preservation only. It does not authorize
   or prove processing, placement, export, or retirement.
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

### D. Hand off to Image Processor

1. Require the captured source path, SHA-256, and dimensions on the typed child.
2. Call `image_factory_work_queue(op=queue_processing)` explicitly. This is the
   Image Factory → Image Processor handoff; end creative-role authority here.
3. Start Image Processor and process only `processing_queued` items.
4. Verify source identity before pixels change.
5. Require a deterministic derivative, output SHA-256/dimensions, durable
   receipt, and `processed` state.
6. Replay must verify and reuse the same output/receipt. Conflicting or orphaned
   output fails closed.
7. Verify the receipt says generation, keeper judgment, placement, and retirement
   did not occur.

### E. Separate downstream placement

`processed` is a handoff state, not placement or completion. Placement,
sidecars, export, and recoverable retirement require a separately explicit
downstream capability and authority. Historical `image_factory_finish_keeper`
and `image_factory_process_candidate` remain compatibility tools only; do not
route new generation sessions through them as the canonical flow.

### F. Recover interrupted operations

Before retrying, inspect the live manifest, filesystem, sidecar, and receipts.

- If capture completed but manifest mutation failed, recover from the durable
  capture evidence rather than downloading again.
- If processor output and receipt completed but state mutation failed, verify
  both identities and use safe replay; do not generate or recapture again.
- If identity evidence, target state, or provenance is ambiguous, stop and report
  the mismatch. Do not infer success or rerun the full operation.
- Repair missing manifest state from verified durable evidence; never overwrite a
  conflicting live state.

### G. Optional `All_Burn` export

Use the legacy `image_factory_export_all_burn` only when Ted requests or a
separately authorized downstream workflow requires the derived export. It is
never implied by keeper acceptance, capture, or processing.

1. Preview by default.
2. On confirmed execution, use the fixed refresh implementation rather than an
   arbitrary command path.
3. Treat output names as globally reserved across the export, not merely unique
   within one category.
4. Verify the exact expected name set and, for every output, image decoding,
   dimensions, byte count, and SHA-256.
5. Never accept output count alone as export proof.

### H. Close

Close Image Factory once every accepted item in its scope is captured or has an
explicit side outcome and every processor handoff is recorded. Close Image
Processor once every item it accepted is processed or explicitly blocked. Do
not claim whole replacement completion until the separately authorized
downstream placement/retirement states are verified. Fresh-client ChatGPT
acceptance is distinct from local or installed-connector proof.

## Capsule handling

For composite operations that require a current capability capsule:

- A valid, same-boot, recently expired capsule may be auto-refreshed once.
- An old, invalid, cross-boot, or otherwise untrusted capsule must fail closed.
- Freshness guards must retain an explicit force-repair path; they must not turn a
  stale or corrupted derived artifact into an unrecoverable dead end.

## Evidence and success criteria

- Acceptance wording and intended filename are preserved in canonical state.
- Captured bytes have verified image type, dimensions, byte count, and SHA-256.
- Processor input requires identity-strength evidence and output receipts.
- Image Factory stops at raw source; Image Processor stops at processed derivative.
- Placement and retirement remain separate downstream evidence.
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

- `image_factory_work_queue`: prospective range/atomic-child lifecycle authority.
- `image_factory_keeper_manifest`: historical keeper-batch compatibility lane.
- `image_factory_capture_generated`: exact-byte capture when current-session bytes
  are available.
- `image_processor_start`, `image_processor_work_queue`, and
  `image_processor_process`: separate deterministic pixels-only capability.
- `image_factory_finish_keeper`: historical placement compatibility, not the
  canonical new-list flow.
- `image_factory_export_all_burn`: dry-run by default; confirmed refresh uses the
  fixed `refresh_all_burn.sh --force` implementation and verifies all outputs.
- `dispatch_worker`: fallback for one frozen retrieval pass when exact bytes are
  unavailable to the current session.

### Filesystem runtimes

Treat `work_items` plus the typed `image_work_*` companion as canonical
prospective queue state. Preserve historical `Image_Factory/ChatGPT/manifests/`
without rewriting old semantics. Do not hand-edit either ledger.

## Update-surfacing backstop

This skill names live tools, schemas, and paths. If live capability truth differs,
preserve the workflow boundaries, record the mismatch, and update this shared
skill rather than creating a local doctrine fork.
