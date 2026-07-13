---
name: image-factory-16x9-replacement-workflow
description: Run one 16:9 replacement candidate through Image Factory end-to-end — generate, stage, inspect, label, place, sidecar, and record. Use when Ted says things like "let's generate a replacement," "pick a random image in IF or Museum Exhibits and generate a replacement," "do a 16:9 replacement run," "continue the replacement program," or "place this replacement where it belongs." Do not use for plain image generation with no placement intent, or for sorting/cleanup work that isn't tied to a specific replacement candidate.
category: meta
write_mode: file
one_line_use: generate + place one 16:9 replacement candidate, with sidecar and change record
fast_pick: "no"
---

# Image Factory — 16:9 Replacement Workflow

Originated as a proposal from the Image Factory ChatGPT runtime (`_AI_Inbox/2026-06-29_chatgpt_propose_image_factory_16x9_replacement_workflow_skill.md`) after the first live end-to-end replacement run. Built by Claude Code per Ted's go-ahead, 2026-06-29.

## When to use

Ted names a category, says "random," or otherwise signals he wants a fresh native-16:9 image generated and placed into the Museum exhibit structure to replace (or sit alongside) an existing non-16:9 file.

## When not to use

- Plain image generation with no placement intent — just generate, no workflow needed.
- Bulk sorting/cleanup of `_Incoming` unrelated to a specific replacement candidate.
- Any step that requires deleting an old file outright — this workflow never deletes; retirement/rejection is a separate, explicit, Ted-approved step.

## Core doctrine

- Old filenames and categories are idea seeds only — never recreate the old image exactly.
- Generate a fresh native 16:9 image in the same exhibit/category spirit.
- No labels, text, or UI baked into the generated image itself.
- Never pass filenames or operational paths into the image prompt as visual content.
- Confirm true 16:9 fit before placement.
- Place only after Ted accepts the candidate or gives explicit go-ahead.
- Never delete old files. Retire/reject/archive only after acceptance — and that's a separate decision, not part of this workflow.
- Collision-safe: never overwrite. `move_to_category` 409s on a name clash by design — respect that, don't force it.
- Always write the sidecar and record the change after a live placement — a move with no sidecar and no change record is an incomplete run, not a finished one.

## Canonical workflow

1. **Orient.** Call `image_factory_start`. Read the `start_card` block first — it names continuity status, the available tool list, any known-degraded tools, and the valid `change_type` enum values. Confirm the role packet and continuity loaded before doing anything else.
2. **Select seed.** Use Ted's named category, or pick one existing file/category as a concept seed if he says "random." The seed is inspiration only — never the visual target.
3. **Generate.** Produce a native 16:9 candidate: specimen-forward, non-narrative, structural, museum-suitable — matching Image Factory's general posture, not this skill's own invention.
4. **Ted review.** Show the candidate. Wait for accept/reject before doing anything to the filesystem. No silent staging of a rejected candidate.
5. **Stage.** `image_factory_stage_write` (subdir `staged`) lands the accepted candidate directly in `_Incoming`. (Path/file-reference staging is a known future improvement — base64 is the current mechanism; see Known Gaps.)
6. **Confirm intake — visually.** `image_factory_list_incoming` to find the new file. If the filename alone doesn't make the subject obvious (unnamed/auto-named files), use `image_factory_preview_image` (or `image_factory_contact_sheet` for a whole batch) to actually look at it before deciding anything — don't guess category/placement for a file you haven't seen. `image_factory_inspect_image` confirms dimensions and true 16:9 aspect.
7. **Decide the label.** Work out the clean human-facing name and exhibit before moving anything. `image_factory_label_preview` checks intent without writing. Required field: `human_name`. Common optional fields: `exhibit`, `canonical_name`, `material`, `form`.
8. **Place — prefer `image_factory_process_candidate`.** Pass `filename`, `category`, `human_name` (and `exhibit` if you have one); it runs inspect → label-preview → dry-run move → live move → sidecar upsert → sidecar read-back → post-move inspect → `record_change` as one call, and its `status` field tells you exactly where it stopped if anything failed. This replaces steps 8-11 below as separate calls — use the manual chain only if `process_candidate` itself errors and you need to diagnose which sub-step is broken.
   - *Manual fallback chain, if needed:* `image_factory_move_to_category` with `dry_run=true`, then live (`dry_run=false`) → `image_factory_upsert_sidecar` with at least `human_name` → `image_factory_read_sidecar` to confirm → `image_factory_inspect_image` on the placed file → `image_factory_record_change`.
9. **Write continuity before ending the session.** Call `image_factory_stage_write` (subdir `continuity`) with a structured note, not free prose — use exactly this shape so the next session's `image_factory_start` surfaces it cleanly:
   ```
   Completed:
   - <what actually finished, e.g. "Lotus sidecar verified, change #75">
   Still blocked:
   - <anything left in a known-bad state, or "none">
   Next:
   - <the next concrete action, e.g. "Marine Life: 67/71 flagged, next replacement target">
   ```

## Evidence / success criteria

A finished run has, in order: a real file in the target category (not still in `_Incoming`), a sidecar with at least `human_name` set, a passing aspect-ratio check, and a change-record id. `image_factory_process_candidate`'s `status: "complete"` confirms all four at once; if it returns anything else, report exactly which step it names, not a generic "done."

## Failure modes

- **Silent incomplete placement.** Moving the file but skipping the sidecar call and reporting "done" anyway. If using the manual chain, always check `image_factory_read_sidecar` before declaring success. `process_candidate`'s `status`/`warnings` fields exist specifically to make this failure visible instead of silent.
- **Visual recreation instead of inspiration.** The old filename/category should shape mood and subject domain, not be treated as a brief to literally reproduce.
- **Guessing at categorization for an unseen file.** Don't infer subject/category from a generic filename alone — preview it first (step 6). Naming a blocked state plainly ("can't categorize, haven't seen it yet") beats a confident guess.
- **Skipping the dry run.** `move_to_category` is collision-safe, but a dry run catches naming mistakes before they become a 409 mid-workflow.
- **Forcing a name collision.** If `move_to_category` 409s, pick a different filename — never retry with overwrite intent; this surface has none.
- **Guessing an unsupported `change_type`.** Use only the enum `image_factory_start`'s `start_card` lists (`build, move, rename, patch, note, audit, reject, config, other`) — there is no `replace`. A live run failed exactly this way before the start card existed.
- **Retrying a blocked step instead of naming it.** If a step fails (preview, move, sidecar — anything), stop and report which step and why rather than retrying the same call repeatedly hoping it resolves itself.

## Known gaps (as of 2026-06-29)

- **Staging is base64-only.** `image_factory_stage_write` requires `content_base64`; there's no path/file-reference staging yet. Large images make for an awkward, fragile transcript. Tracked, not yet built.
- **No bulk/batch replacement.** This skill covers one candidate per run. Running several in sequence is just repeating the loop — there's no batch primitive.
- **`start_card` doesn't auto-extract "open work"/blockers from continuity prose.** It surfaces the raw continuity snippet and the facts it can compute reliably (tools, tool health, enum values). Writing continuity in the Completed/Still blocked/Next shape (step 9) is what makes the next session's read-back actually useful — the structure has to come from the write, not a guess at parse time.

## Connected doctrine

- `_shared/SKILL_Portability_Convention.md` — shape this file follows.
- `_shared/SKILL_Authority_And_Local_Adapters.md` — this is a shared skill; Image Factory (or any role) should not silently fork its own variant of the doctrine above.
- `Projects/Role_Runtime_Architecture/FLEET_TRACKER.md` — Image Factory's exhibit-operation MCP tools this skill calls were ported there.
