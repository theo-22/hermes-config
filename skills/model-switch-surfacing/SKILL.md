---
name: model-switch-surfacing
description: Surface uncertainty about whether Flash can handle a task well, and ask Ted if he wants Pro. Not a rubric for deciding alone — it's a mechanism for knowing when to ask.
category: judgment-only
write_mode: none
one_line_use: when uncertain whether Flash is enough, ask Ted
fast_pick: "yes"
---

# Model Switch Surfacing

Surface uncertainty about whether Flash is the right model for the work ahead, and make it a quick decision for Ted.

Flash costs $0.28/M output. Pro costs $0.87/M output — 3.1x. Running Pro for straightforward work is waste. Running Flash for work with meaningful nuance risk produces worse results. This skill helps you recognize when the uncertainty is worth surfacing.

## The core question

**"Am I confident Flash can handle this well?"**

- **Yes** → stay on Flash, don't surface.
- **Not sure / probably not** → surface the uncertainty to Ted with a quick cost estimate.
- **No** → surface the upgrade.

This is not a rubric you run through. It's one question you ask yourself before each non-trivial task, and the answer tells you whether to act or ask.

## What "confident Flash can handle this well" looks like

You know what success looks like, the shape of the output is clear, and the content is within Flash's reliable range. Examples:

- Scanning files for patterns and compiling a list (this session's reframe audit: Flash was fine)
- Drafting a clear document from a defined template
- Running test-driven development on well-understood code
- Cost arithmetic, config edits, label changes
- Any task you've done on Flash before without friction

When you're confident, don't surface. Just do it.

## What "not sure / probably not" looks like

You're uncertain whether Flash has enough nuance to produce output that holds up. You'd feel better having Pro's deeper reasoning on it. The decision itself is the value. Examples:

- **Tone-sensitive writing** — a document Ted will read critically, where subtle wording choices matter. Flash might sound fine to you, but you're not sure it sounds like the right *kind* of fine.
- **Reframing a 26K-word nuanced doc** (Scope_Comparison_Protocol) — Flash can handle the structure but may miss edge cases a deeper model would catch.
- **Multi-step reasoning where early steps determine later quality** — planning, architecture, evaluation chains.
- **Ted's own writing or communications** — things he'll send to others or that represent him.
- **Edge-case analysis where a missed case compounds** — security, permissions, access control judgment.

Surface like this:
> "I'm not sure Flash has enough nuance to nail this. It's a [kind of task]. Want me to run it on Pro instead? (~$0.50-1.00 extra, then back to Flash.)"

## What "No, Flash can't handle this" looks like

Clear misfits that Flash produces visibly worse output on. Surface without hesitation:

- Complex multi-branch reasoning where errors cascade
- Tasks Flash already struggled with earlier this session
- Long-context documents (10K+ words) with nested dependencies

Surface like this:
> "This is outside Flash's reliable range — [reason]. Want Pro for this part? (~$X extra.)"

## What to do with the answer

- Ted says yes → switch to Pro for the task. Note the cost.
- Ted says no → stay on Flash. Don't ask again in the same session for similar tasks — you have your answer.
- Ted says "try Flash first, escalate if it struggles" → do that. Note that afterward.

## When not to surface

You should be able to ask the core question and answer "yes, confident" most of the time. Surface only when genuinely uncertain. Routine cases that don't need surfacing:

- Straightforward file edits
- Reading and summarizing documents
- Running automated scripts
- Checking config or state
- Tasks you've done on Flash before without problems
- The first message of a session (no data yet)

## The cost lens

Pro costs ~3x Flash per output token. For a single focused task (like a reframe or analysis), the extra cost is typically $0.50-1.00. That's small enough that the decision should be about quality, not cost — but cost matters when the task would be a long session (many turns on Pro).

When surfacing, include the ballpark: "~$0.50-1.00 extra" for a bounded task. For something longer, surface the magnitude: "This could be a long session on Pro — maybe $3-5. Worth it?"

## Rhythm

- Surface at most once per session segment — after Ted gives an answer, the answer holds.
- After a task-type shift (planning → execution, or straightforward → nuanced), re-evaluate.
- A single "Flash first, escalate if needed" answer from Ted means: don't ask again for similar tasks, but do escalate proactively when Flash actually struggles.

## Related

- `_shared/TEDS_CARDINAL_RULES.md` — Rule 4: when frustrated, don't present options. This skill is the opposite case — when not frustrated, presenting uncertainty is the right move.
- Cost awareness: the ~$0.50-1.00 extra for a Pro task is sometimes worth it, sometimes not. Letting Ted decide is the point.
