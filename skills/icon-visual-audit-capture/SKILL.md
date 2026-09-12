---
name: icon-visual-audit-capture
description: Build a repeatable production-grade visual QA package for an Icon System family from a real Finder screenshot plus canonical PNGs. Use before cleanup, batch review, or family acceptance so apparent scale, real navigation salience, and artwork quality are judged separately instead of being collapsed into one normalized contact sheet.
metadata:
  category: icon-system
  write_mode: shared
  one_line_use: capture real-use Finder truth, true-scale family comparison, normalized detail inspection, and measurements without touching canonical icons
  fast_pick: "yes"
---

# Icon Visual Audit Capture

Produce an evidence package optimized for AI and human review of an icon family in production.

## Governing principle

Preserve three different truths and never substitute one for another:

1. **Real-use truth** — how Ted actually sees and navigates the icons in Finder.
2. **Scale truth** — how large each canonical object actually occupies its 1024×1024 canvas relative to peers.
3. **Design-detail truth** — what each object's materials, silhouette, badge, color, and character look like when normalized only for close inspection.

A normalized contact sheet is useful for design critique but is invalid evidence for apparent-size balance. A Finder screenshot is useful for salience but not sufficient for inspecting fine artwork. Keep both.

## Inputs

Required when available:
- one current full-monitor screenshot showing the relevant Finder icon view at Ted's normal working icon-size setting;
- canonical family PNG directory;
- declarative mapping registry for the family;
- family name.

Optional:
- a clean Finder-window crop;
- a focused list of targets;
- prior audit package for before/after comparison;
- effective Finder-render verification receipts.

Never modify a canonical icon while creating an audit package.

## Recommended output location

Create a timestamped directory under the owning Icon System reference/audit area, for example:

`IconSystem/Reference/Audits/<family>_<YYYYMMDD-HHMMSS>/`

The exact root may be adapted to the installed Icon System layout, but keep the package together and report the final path.

## Required artifacts

### `01_full_monitor_context.png`

Preserve the supplied full-monitor screenshot byte-for-byte when possible. If it must be copied, verify hash equality. Do not resize individual icons, change Finder spacing, or alter the screenshot.

Purpose: real working context, peripheral competition, Finder chrome, labels, and overall navigation field.

### `02_finder_field_crop.png`

Crop only to the Finder icon field. Do not resize the icon field after cropping. Preserve original screenshot pixels.

Purpose: easier visual review of production salience without unrelated desktop chrome.

### `03_true_scale_canonical_board.png`

Build from the canonical PNGs, not from subjective estimates.

Rules:
- every canonical PNG gets an identical cell size;
- place each entire 1024×1024 canvas into its cell at the same scale factor;
- do **not** trim alpha before placement;
- do **not** independently enlarge small icons;
- preserve aspect ratio and transparency;
- use a neutral dark background compatible with Finder dark mode;
- label each item with a short row/column id such as `A1` plus filename;
- keep the board large enough that relative object occupancy is obvious.

Purpose: compare apparent icon size while preserving the real amount of empty canvas around each object. This board should make a 62%-occupancy object visibly smaller than an 85%-occupancy peer.

### `04_normalized_detail_board.png`

Build a second board specifically for design inspection.

Rules:
- trim each icon to its nontransparent alpha bounding box;
- preserve aspect ratio;
- fit the trimmed object into a common detail box;
- never distort;
- label with the same row/column ids and filenames used in the true-scale board;
- record clearly in the board header that sizes are normalized for detail and are **not production-scale evidence**.

Purpose: judge silhouette, material treatment, glow, contrast, badges, color, character, and family resemblance without a small object being hard to see.

### `05_metrics.csv` and `05_metrics.json`

For each canonical PNG record at minimum:
- row/column id;
- filename;
- canonical path;
- SHA-256;
- pixel dimensions;
- image mode;
- alpha bounding box;
- visible width and height in pixels;
- visible width and height as percentages of canvas;
- visible alpha-bbox area as percentage of canvas;
- center offset from canvas center in pixels and percent;
- mapping active/inactive when available;
- mapped Finder target when available;
- effective Finder-render verification score/status when directly available; otherwise `unknown`, never inferred.

Do not automatically convert measurements into KEEP/REFINE/REDESIGN decisions.

### `06_index.md`

Write a compact manifest containing:
- audit timestamp;
- family;
- screenshot source path and SHA-256;
- screenshot pixel dimensions;
- canonical family path;
- mapping-registry path and hash when available;
- paths and hashes of every generated audit artifact;
- any targets omitted and why;
- any evidence source that was unavailable;
- exact command or helper used to generate the package.

## Optional artifact: `07_before_after.png`

When a prior package exists, produce a paired before/after comparison for only the changed targets. Keep production-scale and normalized-detail comparisons separate or clearly labeled.

## Measurement behavior

Use deterministic image tooling such as Python + Pillow for board generation and geometry. Do not use an image-generation model to create, beautify, reinterpret, or redraw audit evidence.

The alpha threshold for the primary bounding box should default to `alpha > 0`. If a second threshold is useful for faint glow, record both thresholds explicitly rather than silently changing the metric.

For center offset, compute the alpha-bbox center relative to canvas center. Report the number; do not assume off-center is a defect.

For occupancy, report width and height independently. Do not use one scalar threshold to decide quality because deliberately wide, shallow, tall, or narrow silhouettes may be correct.

## Visual-review doctrine

The package gathers evidence. It does not redesign the family.

When reviewing the package:
- family consistency should primarily come from apparent scale, material language, lighting, contained glow, edge treatment, and finish;
- preserve deliberate silhouette diversity when it improves recognition and long-term visual memory;
- hierarchy should come through decoration, badges, accent color, surface richness, and personality rather than making low-priority icons smaller;
- literal recognizable cues are allowed when they help navigation;
- low-salience icons may be simpler and quieter without appearing unfinished;
- judge actual production friction at Finder scale before recommending redesign.

## Finder screenshot protocol

For repeatable production captures:
- keep Finder in the same icon-view mode;
- keep the icon-size slider unchanged between baseline and follow-up captures;
- keep the same display scaling when practical;
- show filenames;
- avoid selection highlights when practical unless the selected item is part of the evidence;
- capture the whole display once, then derive the Finder-field crop from that same source image;
- do not manually zoom or rescale the screenshot before analysis.

A full-monitor screenshot is valuable because it captures the actual visual field Ted uses. The Finder crop is derived convenience, not a replacement for the full-monitor source.

## Actor split

Prefer **Codex or another deterministic shell-capable actor** for capture-package production because the work is mostly file discovery, hashing, alpha geometry, and Pillow compositing.

Use **Claude or ChatGPT** for a second-pass visual/design critique when useful, but do not ask a language model to fabricate the evidence images. The deterministic package is the shared input to those judgments.

## Suggested implementation contract for Codex / Claude Code

Use this prompt shape when delegating the package build:

> Run the `icon-visual-audit-capture` skill for the requested Icon System family using the latest supplied full-monitor Finder screenshot and the live canonical PNG directory. Do not modify any canonical PNG, mapping, or Finder state. Produce the complete audit package, use deterministic Pillow-based compositing and geometry, preserve true scale in the canonical board, normalize only the detail board, hash every output, verify read-back, and report the package path plus any missing evidence. Stop after the audit package is complete.

## Acceptance

The capture pass is complete only when:
- the original screenshot identity is preserved and hashed;
- both scale-preserving and normalized-detail boards exist and are clearly distinguished;
- metrics cover every included canonical icon;
- filenames/row-column ids agree across boards and metrics;
- no canonical asset or Finder state changed;
- generated files read back successfully;
- the manifest records exact inputs, outputs, hashes, and limitations.

If any of those fail, report the package as partial rather than rounding it up to complete.
