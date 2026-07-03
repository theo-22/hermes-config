---
name: 00-shared-skills-card
description: Quick picker for Ted's shared skills. Use when Ted wants help choosing between the shared skills, wants a reminder of the exact skill names, says the slash menu is crowded, or references the shared skills index, skill card, or `/00`.
category: meta
write_mode: none
one_line_use: quick picker for the shared skills
fast_pick: "no"
---

# Shared Skills Index

Use this skill as a lightweight entrypoint to Ted's shared skills.

Read [/Users/ted/Skills/SKILL_INDEX.md](/Users/ted/Skills/SKILL_INDEX.md) and use it as the source of truth for the quick routing index.

## Workflow

1. Read the shared skill index.
2. Use it to identify the most directly matching shared skill.
3. Suggest the exact skill name or use it if the current task clearly matches.
4. Keep the response short and practical.

## Guardrails

- Do not duplicate the full card from memory if the file can be read.
- Do not invent shared skill names that are not on the card.
- Do not turn the card into a taxonomy lesson unless Ted asks.
- Do not treat this card as a replacement for the underlying skills.

## Update-Surfacing Backstop

The index content is at risk of `convention-creep` whenever a skill is added, retired, or has its trigger conditions edited. Current state: curated by hand, but validated against the live shared skill set and required skill metadata with `skills-card-check`.

If the card and the live set diverge:

- run `~/Skills/skills-card-check`
- correct missing or stale skill-name listings immediately
- if the drift is in the curated routing guidance rather than the name list, update the index text during the same pass

Longer-term candidate: move to `generated-not-edited` only after the structured metadata proves it can regenerate the current curated routing guidance faithfully. As of 2026-05-22, required metadata exists and is enforced (`category`, `write_mode`, `one_line_use`, `fast_pick`), but the index remains curated rather than generated.
