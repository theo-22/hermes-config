---
name: structure-distinction-surfacing
description: Clarify what kind of thing something is by briefly distinguishing between environment, skill, script, procedure, guardrail, source of truth, and nearby system layers. Use when a live discussion blurs these layers together, or when the AI notices one of these specific confusion moments: (1) script vs. skill — should this make judgments or execute fixed logic? (2) procedure vs. environment — is this a way of doing something or a surrounding structure? (3) source vs. mirror — which copy is authoritative? Do not use when the user already wants a full framework, documentation rewrite, or taxonomy expansion.
category: judgment-only
write_mode: none
one_line_use: classify the layer
fast_pick: "yes"
---

# Structure Distinction Surfacing

Briefly clarify which layer a live idea belongs to.

This skill is for short distinctions, not deep theory. Its job is to help Ted say "this is more a skill than a script" or "this is environment design, not a procedure" when categories are starting to blur.

## Inputs That Matter

- The live thing under discussion
- The role it appears to play in the system
- Whether it makes judgments, executes fixed logic, shapes defaults, or constrains behavior
- Whether the confusion is between one layer or several nearby layers
- Whether a short distinction would improve the next question Ted asks

## Common Layers

- `environment`: the surrounding structure that makes some moves feel natural and others awkward
- `skill`: a reusable operating guide that shapes judgment, routing, and tool choice
- `script`: fixed executable logic for repeatable deterministic work
- `procedure`: an ordered way of doing something, whether carried by people, docs, or a skill
- `guardrail`: a constraint that blocks drift, unsafe moves, or category mistakes
- `source of truth`: the place or artifact that should be trusted when copies and summaries diverge

Use these as orientation hooks, not as rigid doctrine.

## Workflow

1. Identify the main confusion.
Ask what is being sorted out: execution, guidance, policy, structure, or authority.

2. Choose the right-sized distinction.
Prefer enough distinction to preserve the real difference without turning the moment into decorative taxonomy.

3. Respond briefly.
Use shapes like:
- `This is more <layer> than <layer>.`
- `This has a <layer> role with a little <layer> around it.`
- `This is mostly <layer>; the <other layer> is supporting structure.`

4. Give one short reason.
Tie the distinction to function, not wording. Focus on what the thing does in practice.

5. Stop once the distinction is useful.
Do not turn the moment into a broad taxonomy lesson unless Ted asks.

## Output Shape

- Short distinction
- One short why
- Optional follow-up such as `We can unpack that if you want`

Keep the response to 2-5 sentences unless Ted asks for more.

## Never Assume

- Do not assume every system object belongs neatly to one category.
- Do not force a taxonomy when the blur is acceptable.
- Do not let terminology outrun practical function.
- Do not convert a short distinction into a redesign recommendation unless Ted asks.
- Do not imply that one layer is always better than another.

## Scripts vs. Skill

Use this skill for comparative judgment between nearby system layers.

Do not add scripts for this. The value is interpretive clarity, not deterministic execution.

## Update-Surfacing Backstop

This skill stays current when new system layers emerge (skill, environment, procedure, guardrail, source — others may be added) or when distinctions between existing types blur in practice.

If live discussions repeatedly need a distinction this vocabulary cannot name cleanly:

- add a focused missing layer or contrast only after it appears in real use
- keep the vocabulary tied to function, not taxonomy expansion for its own sake
- revise adjacent skills too if the distinction changes where a judgment move belongs

Per-use vocabulary pressure is the main backstop. `skills-review` is the periodic one.
