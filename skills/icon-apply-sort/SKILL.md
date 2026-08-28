---
name: icon-apply-sort
description: After Icon Image Processor writes a ready_for_apply receipt, confirm mappings and run one family apply_registry so Finder icons match the landed canonicals. Use when a processor batch receipt is ready, or when Ted says apply now. Do not use this skill to cut out, crop, generate, or replace PNG bytes.
category: file-write
write_mode: file
one_line_use: run one family apply from a processor receipt
fast_pick: "yes"
---

# Icon Apply / Sort

Owner: Icon System. Canonical packet: `/Volumes/Extra/Substrate/IconSystem/Capabilities/ICON_APPLY_SORT.md`.

Sort mappings if needed, then run the family apply script once so Finder icons match the canonicals the processor just landed.

## Trigger

`icon-image-processor` finished. Receipt path:

`/Volumes/Extra/Substrate/IconSystem/ChatGPT/receipts/processor_batches/batch_<id>.json`

`status` must be `ready_for_apply`. No receipt, no apply, unless Ted explicitly says apply anyway.

## Inputs

- Processor batch receipt (folder list, canonical paths, hashes, family)
- `IconSystem/Icon_Families/folder_icon_mappings.v1.json`

## Steps

1. Start Icon System if not already inhabiting it.
2. Read the receipt. Fail closed if any listed canonical is missing or hash-mismatched.
3. Confirm each folder has an active mapping. Sort/repair mapping only when a landed canonical has no mapping; do not remap unrelated folders.
4. Dry-run: `icon_system_home_op` run `Icon_Families/apply_registry.py --family <Family>`.
5. Live apply once: `apply_registry.py --apply --family <Family>`.
6. One Finder refresh at the end of that script, not per folder.
7. Mark the receipt `applied` with the apply summary (`matched`, `missing_icon`, `missing_target`, `failed`).

## Outputs

- Finder icons applied for the receipt set (and the rest of that family if apply_registry is family-wide)
- Receipt updated `status: applied`

## Prohibited

- `--only` loops that apply one folder per invocation when Ted asked for a batch apply
- Recutting or replacing PNG bytes
- `complete_keeper` as the apply path for a batch
- Starting without a processor receipt unless Ted overrides

## Proof

Dry-run then live summary: `failed=0`. Independent `icon_system_verify` may add Finder custom-icon signals afterward. That still does not prove rendered pixel identity.
