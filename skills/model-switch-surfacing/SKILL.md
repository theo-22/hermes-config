---
name: model-switch-surfacing
description: Recognize when a task or usage pattern suggests upgrading (Flash→Pro) or downgrading (Pro→Flash) the active model, and surface it to Ted as a quick decision. Use when the model in use is wrong for the work — Flash on a deep reasoning task, or Pro on simple edits. Do not switch automatically. Do not surface for every task — only when the mismatch is clear and would save money or improve outcomes.
category: judgment-only
write_mode: none
one_line_use: surface model upgrade/downgrade opportunities before the cost or quality cost mounts
fast_pick: "yes"
---

# Model Switch Surfacing

Recognize when the active model is wrong for the task in front of the conversation, and surface a quick switch decision to Ted.

Flash costs $0.28/M output. Pro costs $0.87/M output — 3.1x. Running Pro for simple file edits, label changes, or cost arithmetic is waste. Running Flash for multi-step reasoning chains or deep analysis produces worse results. This skill catches both.

Fire proactively when the mismatch is clear. Do not fire for every task — that's noise. Fire when the cumulative impact matters.

## Current default

`deepseek-v4-flash` is the default for all profiles except brain-hermes (Pro for search quality). Pro is available on request. The SOUL.md rule: "Flash by default, escalate to Pro on request."

## Flash → Pro trigger (upgrade)

Surface when:

1. **Complex reasoning needed** — multi-step analysis, plan evaluation, trade-off weighing, or architecture review that Flash will handle poorly.
2. **Task spans many context turns** — deep planning sessions where early errors cascade.
3. **Flash already struggled** — user corrected Flash twice or Flash produced confused output on a reasoning task.
4. **Cost-appropriate** — the task is high-value (planning session, system design) and the extra ~$0.50-1.00 for Pro is worth it.

Surface like this:
> "This is a reasoning-heavy task. Flash might struggle. Want me to switch to Pro for this session? (~$0.50-1.00 extra, then back to Flash.)"

## Pro → Flash trigger (downgrade)

Surface when:

1. **Simple work on Pro** — file reads, targeted edits, label changes, cost arithmetic, dashboard config. Pro is overkill.
2. **Pattern of simple requests** — the session started with reasoning but has drifted to straightforward execution.
3. **Cost accumulating** — session is long, the work is routine, and the Pro premium is adding up for no benefit.

Surface like this:
> "We've been on Pro for a while but the work is straightforward now. Switch back to Flash? Saves ~$0.60/M output."

## Do not surface

- On the very first message of a session (no pattern yet).
- When the task is borderline — only when the mismatch is clear.
- When Ted explicitly chose the current model (he knows).
- For brain-hermes (Pro is intentional for search quality).
- When the savings are trivial (< $0.10 difference).

## Rhythm

- At most once per session segment — don't nag.
- After a task type shift — if the session moved from planning to execution, mention once.
- When Ted expresses frustration with output quality — that's a Flash→Pro trigger.

## Update backstop

Revise if:
- it overfires and Ted starts ignoring it.
- the cost difference between Flash and Pro changes (repricing).
- new models are added that change the escalation path.
- Ted sets a hard rule that overrides the skill.
