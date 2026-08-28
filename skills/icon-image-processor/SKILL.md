---
name: icon-image-processor
description: Turn accepted or generated folder-icon pixels into canonical 1024x1024 RGBA keepers with a transparent exterior, mapped, hashed, and receipted. Use after Ted keeps an icon, after a host-generated PNG lands, or when IconDownloads has a keeper to process. Stop before Finder. Do not use this skill to apply icons, run apply_registry, or call complete_keeper for a batch.
category: file-write
write_mode: file
one_line_use: cut out and land icon keepers, then write a ready_for_apply receipt
fast_pick: "yes"
---

# Icon Image Processor

Owner: Icon System. Canonical packet: `/Volumes/Extra/Substrate/IconSystem/Capabilities/ICON_IMAGE_PROCESSOR.md`.

Turn accepted or generated icon pixels into canonical 1024×1024 RGBA keepers with a transparent exterior, mapped, hashed, and receipted. Stop before Finder. Processor completion triggers `icon-apply-sort`.

## Trigger

Ted names folders or drops keepers. ChatGPT downloads in `IconDownloads` also count. A host-generated PNG counts the same as a download.

## Inputs

- Named folder targets and their canonical PNG paths
- Or files in `IconSystem/Icon_Families/IconDownloads/`
- Family (default Metallic Glow unless Ted names another)

## Steps

1. Start Icon System (`icon_system_start`). Work in Keeper Intake / processor mode.
2. Inspect each source. If alpha already has a transparent exterior, skip cutout and record `already_cut`.
3. If the host emitted 1536×1024, center-crop to 1024×1024 before cutout.
4. `icon_system_asset_pipeline` `prepare_cutout_variants`. Default selection: balanced.
5. Archive the opaque canonical, then `icon_system_home_op` move the selected variant onto the canonical path. Do not overwrite in place.
6. `icon_system_verify` for exists, sha256, 1024, RGBA, transparent exterior, mapping. Do not treat Finder signals as processor proof.
7. Write `IconSystem/ChatGPT/receipts/processor_batches/batch_<id>.json` with every path, hash, skip, and `status: ready_for_apply`.

## Outputs

- Canonical PNGs under `Icon_Families/<Family>/`
- Batch receipt that `icon-apply-sort` consumes

## Prohibited

- Generating a montage or one prompt for a set
- Applying Finder icons
- Running family apply scripts
- `complete_keeper` for a named batch
- Deleting; archive only
- Mixing apply into the processor turn

## Proof

`icon_system_verify` PASS on pixel/mapping checks. Receipt lists hashes. Finder presence or absence is out of scope.

## What fires next

Receipt `ready_for_apply` is the trigger for `icon-apply-sort`. Do not apply from this skill.
