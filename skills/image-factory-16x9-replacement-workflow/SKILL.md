---
name: image-factory-16x9-replacement-workflow
description: Collect Ted-approved native-16:9 replacement keepers into one manifest, retrieve the frozen batch once through a bounded browser worker, then reconcile and curate each asset recoverably.
version: 2.0
owner: Image Factory
status: active
category: meta
write_mode: file
one_line_use: collect keepers, retrieve one frozen batch, then reconcile and curate recoverably
fast_pick: "no"
---

# Image Factory 16:9 Replacement Workflow

One canonical cross-runtime procedure for the Replacement Program. Runtime tools
may differ; the authority, ordering, evidence, and failure rules do not.

## When to use

- Ted names an Image Factory category or subject for 16:9 replacement.
- An exhibit/category contains older non-16:9 images.
- A keeper batch is collecting or ready for retrieval.
- Accepted generated images need one browser-download pass before curation.

## When not to use

- Ordinary free image exploration.
- Files are already in `_Incoming` and no keeper batch is involved; use
  Production Intake.
- Canonical Museum exhibit design or taxonomy is the primary task; use Museum
  Space.
- The request is to recreate an old image exactly.

## Core rule

Old images and filenames are subject seeds only. Generate fresh native-16:9
images covering the same useful territory; do not recreate the old composition.

## Canonical workflow

### A. Audit

1. Start Image Factory in Replacement Program mode.
2. Run the category aspect audit.
3. Review actual category coverage when practical.
4. Choose one subject seed or coherent cluster.
5. Open or resume one JSON keeper manifest.

### B. Collect keepers

1. Generate one native-16:9 candidate at a time.
2. Show Ted the image before any asset operation.
3. On acceptance, append one manifest item with title, intended filename, chat
   anchor, dimensions when known, and exact verdict wording.
4. On rejection, do not retrieve or stage.
5. On hold, preserve undecided state without counting it as accepted.
6. Continue until Ted declares the batch ready.

A keeper is not an intake trigger. `Keep it. T.` records the keeper first, then
moves to New Theme within the same category. Do not dispatch, download, move,
sidecar, or retire after each accepted image.

### C. Freeze

- Resolve superseded items and ambiguous chat anchors.
- Require exact unique intended filenames and a server-derived accepted count.
- Freeze the accepted set and record its digest.
- Do not change accepted membership after freeze. Clone a new collecting batch
  if membership must change.

### D. Retrieve once

Use the manifest tool's read-only retrieval preparation, then make one explicit
shared worker dispatch.

Worker boundary:

- locate only listed images in the originating ChatGPT thread;
- download each once under its exact intended filename;
- report valid image type, dimensions, byte count, and SHA-256;
- stop on ambiguity;
- do not categorize, sidecar, place, reject, replace, retire, or make curatorial
  choices.

Record the worker/run reference only when manifest hash and frozen digest match.

### E. Reconcile intake

1. Preview exact filename/count reconciliation against the frozen manifest.
2. Inspect type, aspect ratio, dimensions, bytes, and SHA-256.
3. Preserve host-chat and returned-file hashes separately.
4. Confirm only after the preview is correct.
5. Block with exact missing, unexpected, invalid, or wrong-aspect evidence.

Reconciliation does not move files or make curation decisions.

### F. Curate

For each verified keeper:

1. choose the best existing category and role in coverage;
2. inspect plausible older replacement targets;
3. preview label and sidecar;
4. dry-run placement;
5. perform live candidate processing;
6. read back sidecar and inspect the placed image;
7. record the change;
8. retire an original recoverably only after new placement verification;
9. verify retirement and record the terminal disposition.

A keeper may be an addition rather than a one-for-one replacement.

### G. Close

Complete only when every frozen item has a terminal disposition and all changed
paths, sidecars, retirements, records, and exceptions are verified. Typed close
verifies batch ID, manifest path, revision, SHA-256, state, and any retrieval
receipt/claim reference.

## Evidence and success criteria

- Keeper phrases mutate only the collecting manifest.
- Frozen-set membership and revision conflicts fail closed.
- One explicit worker pass matches the frozen manifest.
- Intake preview is read-only and confirmation records verified bytes.
- New placement and sidecar read-back precede recoverable retirement.
- Completion has no hidden pending accepted items.
- Production changes have collision-safe paths and receipts.

## Failure modes

- Blind retry after a named failure.
- Guessing an image or chat anchor.
- Dispatching per keeper or implicitly from the manifest tool.
- Treating the worker as curatorial authority.
- Requiring the returned hash to equal the host hash.
- Deleting, overwriting, or retiring before replacement verification.
- Claiming completion from worker text alone.

## Runtime notes

### Image Factory MCP

Use `image_factory_keeper_manifest` for lifecycle state. Use shared
`dispatch_worker` only after `freeze` and `prepare_retrieval`. Use
`image_factory_process_candidate` for verified placement where appropriate.

### Filesystem runtimes

Treat `Image_Factory/ChatGPT/manifests/` as canonical role state and use the same
schema/revision rules. Do not rewrite a live manifest by hand when the composite
tool is available.

## Update-surfacing backstop

This skill names live tools, schema, and paths. If any differ in live capability
truth, preserve the workflow boundaries, record the mismatch, and propose one
shared-skill update rather than creating a local doctrine fork.
