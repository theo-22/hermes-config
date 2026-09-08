---
name: accepted-image-finishing
description: Carry an already accepted image from the human handoff into a durable verified destination without losing exact source identity or forcing unnecessary processing. Use after Ted accepts/downloads an image or a producer has an accepted candidate that still needs capture, optional deterministic processing, canonical naming, placement, downstream rebuild/index checks, or lifecycle reconciliation. Do not use for generation, creative acceptance, category invention, or pixel processing that has not been justified.
metadata:
  category: meta
  write_mode: shared
  one_line_use: finish an accepted image from exact source capture through verified destination state
  fast_pick: "yes"
---

# Accepted Image Finishing

Move an accepted visual artifact from the human/producers' handoff point to its real durable destination while preserving source truth, role boundaries, and downstream verification.

## When to use

Use when the image has already been accepted and one or more of these remain:

- discover the exact downloaded or staged source;
- preserve exact bytes into the producer's governed intake lane;
- settle a canonical filename from the destination owner's naming rules;
- decide whether deterministic pixel processing is actually needed;
- hand off to the processor when needed;
- place/publish through the destination-owned capability;
- rebuild or refresh a derived index/display surface;
- reconcile the artifact's lifecycle and verify the final user-visible result.

## When not to use

Do not use this skill to:

- decide whether an image is good enough to keep;
- generate or creatively refine the image;
- invent a category, exhibit, family, or destination;
- route every keeper through a processor merely to obtain a receipt;
- treat a preview, recompressed copy, or renamed lookalike as the accepted source;
- bypass a destination-specific publisher with a generic file copy when the publisher owns build/index/display verification.

## Canonical workflow

### 1. Re-establish the exact accepted source

Begin at the actual handoff surface: Downloads, producer candidate cache, governed intake, or another explicitly allowed source root. Discover rather than guess the filename.

Record and carry forward:

- exact source path;
- SHA-256;
- decoded dimensions and format;
- acceptance provenance;
- batch/range/item identity when one exists.

If the runtime provides a batch-intake claim, acquire it before registering or capturing the batch. A blocked claim means coordinate with the existing owner rather than duplicate the intake.

### 2. Preserve first; transform later

Capture or register the exact accepted bytes into the producer's governed intake lane before any optional processing. Capture is preservation, not placement and not processing.

Verify the captured hash/dimensions against the accepted source. If exact identity cannot be proved, stop rather than silently substituting another file.

### 3. Settle destination semantics before mechanics

The producer/curator decides the semantic facts the mechanical layer must not invent:

- destination/category/exhibit/family;
- canonical filename or human-facing title;
- replacement/supersession intent when applicable;
- destination-specific metadata.

Inspect the existing destination neighborhood before naming. Prefer descriptors that are supported by the visible artifact and destination doctrine; do not encode inferred process or identity as fact.

### 4. Decide whether processing earns a place

Ask: **What pixel change is required for the destination contract?**

- If a deterministic transform is required, create the processor handoff and use the processor's verified derivative as the placement source.
- If the accepted source already satisfies the destination contract, record **no processing required** and continue with the exact captured source.

A processor is a pixel capability, not a ceremonial checkpoint.

### 5. Use the destination-owned finishing capability

Prefer the most specific typed publisher/placement operation available. The destination owner may add requirements beyond byte placement, such as sidecars, mappings, generated indexes, build steps, served-surface checks, or reversible retirement.

Run a dry/preflight path when the destination capability supports one. On live execution, preserve the exact source/processor receipt and authority/work references expected by that capability.

Do not replace a missing destination publisher with a lower-level generic placer if doing so would skip destination-specific verification.

### 6. Verify the actual downstream state

Completion means the artifact is usable where the user expects it, not merely that bytes were copied.

Verify the destination-specific evidence, which can include:

- destination hash/dimensions/format read-back;
- sidecar or declarative mapping read-back;
- exact derived-index inclusion;
- successful build/export;
- served/browser-visible inclusion when that surface is part of the contract;
- lifecycle reconciliation or reversible retirement evidence when applicable.

Preserve truthful partial states. If placement passed but build/index/display verification failed, say exactly that.

### 7. Reuse or inspect the finished artifact

When the artifact is a reference vocabulary item, immediately exercise the returned handle once in the producing system if practical. When it is a display artifact, inspect the refreshed visual surface. This closes the gap between filesystem success and lived usability.

## Evidence / success criteria

A finishing pass succeeds when:

1. the accepted source identity is explicit and preserved;
2. any processing decision is justified by a real pixel requirement;
3. semantic destination choices came from the owning role/user, not the mechanical placer;
4. destination-owned placement/publish verification passed;
5. any derived index/build/display surface expected by the destination was checked;
6. the final state is reported as PASS, truthful partial, or blocked at the first genuine boundary.

## Failure modes

- **Guessing the download** — filename reconstruction replaces discovery.
- **Processing by ritual** — a correct native artifact is cropped/resized solely because a processor exists.
- **Source substitution** — a preview or recompressed derivative is treated as the accepted original.
- **Semantic leakage** — a mechanical tool invents category, title, material identity, or replacement meaning.
- **Generic-placement shortcut** — bytes land but the destination's build/index/browser contract never runs.
- **Receipt inflation** — capture or processor success is described as final placement.
- **Duplicate intake** — two sessions register/capture the same Downloads batch because the intake claim was skipped.
- **Filesystem-only verification** — a human-facing reference/browser/mapping surface is assumed refreshed without checking it.

## Runtime notes

### Image Factory

Use producer-native discovery/capture and typed image-work lifecycle tools. For Materials Reference, processing may be explicitly skipped when the accepted sample already satisfies the artifact contract; finish with the Materials-specific publisher, not generic placement alone.

### Icon System

Use the icon intake/processor/family pipeline and preserve accepted-source identity through normalization/mapping/application. Finder application is a distinct downstream state from canonical PNG placement.

### Image Processor / Icon Processor

Own deterministic pixel transforms only. Do not absorb creative acceptance, naming/category judgment, or destination publishing merely to make the workflow feel continuous.

### Codex / Claude Code

When a role runtime lacks one executable transition, implement or repair the typed capability under an exact authorized envelope; do not replace the missing transition with an ad-hoc file move that weakens evidence.

## Update backstop

This skill intentionally names capability shapes rather than hard-coding one runtime's complete tool list. If a producer's intake, processor, placer/publisher, or downstream verification contract changes, preserve the seven-step procedure and update only the runtime adapter. If the same new finishing behavior recurs across two visual systems, promote it here rather than forking role-local copies.
