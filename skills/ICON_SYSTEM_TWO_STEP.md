# Icon System two-step capabilities

**Status:** live 2026-08-27
**Authority:** Ted, Grok Bot chat, promote two-step Icon pipeline
**Owner:** Icon System
**Not:** a new bot or Coordination role

Two shared skills, one trigger.

## icon-image-processor

Skill: `Skills/icon-image-processor/SKILL.md`
Packet: `IconSystem/Capabilities/ICON_IMAGE_PROCESSOR.md`

Owns pixels. Crop, cutout, land canonical 1024×1024 RGBA, hash, mapping. Stop. Writes `IconSystem/ChatGPT/receipts/processor_batches/batch_<id>.json` with `status: ready_for_apply`.

## icon-apply-sort

Skill: `Skills/icon-apply-sort/SKILL.md`
Packet: `IconSystem/Capabilities/ICON_APPLY_SORT.md`

Owns scripts and Finder. Starts from that receipt. One family `apply_registry.py --apply`. One Finder refresh. Never recuts.

## Contract

`IconSystem/ROLE_CONTRACT.md` SHA-256 `e858980bb9a319ea6662e549bced86661061bc971be6bd6ad20bf8ee184d5e3b`

Keeper Intake is the processor. Apply/Rollout is Apply/Sort. `complete_keeper` is not the batch path.

## Index follow-up

`SKILL_INDEX.md` picker rows and the Phase 0 lookup snapshot are a separate exact-path add. Operating packets and SKILL.md files are already live.
