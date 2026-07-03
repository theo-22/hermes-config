---
name: affected-gpt-hearing
description: Decide whether a proposed GPT/system change affects another GPT's startup behavior, runtime path, handoff expectation, continuity surface, authority boundary, or action/tool shape; draft the exact paste prompt for Ted to run in the affected GPT; and specify how the response becomes settlement evidence. Use before settling GPT changes that alter how another GPT starts, acts, remembers, hands off, reads/writes, or uses tools. Do not use for behavior-neutral polish or ordinary internal prose cleanup.
category: judgment-only
write_mode: none
one_line_use: hear the GPT whose operating surface would change
fast_pick: "yes"
---

# Affected GPT Hearing

Use this skill when a proposed change may alter how a GPT operates. The affected GPT's response is required evidence for settlement, not approval authority or veto power.

## Trigger

Use this skill when a proposed change touches an affected GPT's:

- Builder Instructions or required startup behavior
- Knowledge upload set, manifest source, live-read overlay, or behavior overlay
- Action schema, action description, auth/scope expectation, operationId, proxy/backend route, or tool-call sequence
- continuity surface, memory boundary, briefing path, session-start file, or persistent state convention
- handoff expectation, inbox routing, decision authority, or responsibility boundary
- visible workflow, starter/button behavior, import/export path, or artifact lifecycle

Trigger even when the change is probably beneficial. The question is whether the GPT's operating surface changes.

## Skip

Do not use this skill for:

- typo, grammar, or formatting fixes that do not change behavior
- behavior-neutral source refreshes where intended operation is unchanged and verified
- proposal discussion before a concrete affected surface exists
- GA-local reconciliation format changes that do not affect another GPT
- internal rationale moved between files when runtime behavior is preserved

If uncertain, draft a brief targeted hearing prompt rather than silently skipping.

## Inputs

- Proposed change in one sentence
- Affected GPT name
- Affected surface path, Builder field, action name, or workflow
- What behavior could change
- What Ted/system decision is already settled
- What remains open for evidence

## Workflow

1. **Name the affected surface.**
State exactly what would change and where: startup, runtime, handoff, continuity, action shape, Builder Instructions, Knowledge, schema, or route.

2. **Decide trigger status.**
Choose one: `hearing required`, `hearing not required`, or `uncertain - hearing recommended`.

3. **Draft the paste prompt for Ted.**
Keep it short enough for a quick exchange. Ask the affected GPT to evaluate operational impact, not to approve the change.

4. **Preserve authority boundary.**
Tell the affected GPT what is already settled, what is still open, and that it is providing evidence only.

5. **Capture the response as settlement evidence.**
Settlement records one of: `incorporated`, `no change needed after review`, `overridden with reason`, or `deferred because response exposed missing evidence`.

6. **Do not settle a material affected-surface change before review.**
Silence is not consent. If the response is unavailable, explicitly defer or override with reason.

## Paste-Prompt Template

```text
You are being asked for affected-GPT input, not approval authority.

Proposed change:
[one-sentence change]

Affected surfaces:
[paths / Builder fields / action names / workflow]

Already settled:
[what Ted or the system has already decided, if anything]

Open question for you:
Would this change alter your startup behavior, runtime behavior, handoff expectations, continuity assumptions, action/tool use, or ability to do your job correctly?

Please answer in this shape:
1. Impact: none / minor / material / blocking
2. What would change for your operation
3. Any risk, missing context, or better wording
4. Whether the proposal can proceed as written, should be amended, or should be deferred for more evidence

Reminder: your response is required evidence for settlement, not a veto.
```

## Output Shape

- `Trigger status`
- `Affected GPT`
- `Affected surface`
- `Why hearing is / is not required`
- `Paste prompt for Ted`
- `How to use the response`
- `Settlement status`

## Boundaries

- Use `proposal-candidate-surfacing` when the proposal is still forming and the affected surface is not concrete.
- Use `proposal-packet` when the proposal itself needs a durable handoff packet.
- Use `surface-routing` when the main question is where the response or packet should land.
- Use `gpt-environment-build` for full GPT build/repair across Builder, schema, backend, and live verification.
- Use this skill when the main question is whether affected-GPT input is required and how to obtain it cleanly.

## Never Assume

- Do not treat silence as consent.
- Do not let the affected GPT veto Ted's decision.
- Do not hide settled authority boundaries from the affected GPT.
- Do not ask broad speculative questions; ask about concrete operating-surface impact.
- Do not trigger hearings for behavior-neutral polish.

## Update-Surfacing Backstop

If Canon, Active Team Agreements, GA settlement protocol, or Builder platform behavior changes the hearing threshold, update this skill in the same pass.

If live use shows overfiring on harmless edits, tighten skip conditions. If a GPT change lands without hearing and later produces runtime or handoff drift, tighten trigger conditions.
