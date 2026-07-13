---
name: poka-yoke
description: Recognize when a process depends on memory, discipline, or convention rather than structure, then name the failure mode and choose a contained sufficient mechanism that prevents it. Use when recurring mistakes, manual sync, stale accumulation, duplicate-on-rename risk, or "someone has to remember" processes appear. Boundary with andon: poka-yoke prevents; andon surfaces what prevention cannot cover.
category: judgment-only
write_mode: none
one_line_use: choose structural prevention
fast_pick: "yes"
---

# Poka-Yoke

Make structural prevention visible before maintenance dependence hardens into doctrine.

This skill is for the judgment move where a recurring risk stops being "be careful" and becomes "change the structure so care is not the only defense."

Use it to name the failure mode, decide whether prevention is possible, and pick the lightest mechanism that actually removes remembering from the loop.

## When to Trigger

- A process depends on someone remembering to do the right thing
- The same failure shows up again in a new instance
- A list, mirror, queue, or reminder surface accumulates without a cleanup path
- Identity is tied to a mutable attribute like path, position, or timestamp
- A manual sync step is treated as normal operating procedure
- A "we should remember to check" rule is standing in for enforcement
- The right move may be prevention, but the system only has surfacing

Fire proactively when a task requires a remembered follow-up step — especially sync, cleanup, or duplicate-prevention work. Do not wait for the pattern to recur before naming it.

## Failure-Mode Vocabulary

- `drift` - source of truth diverges from mirror, projection, or summary
- `duplicate-on-rename` - identity tied to a mutable attribute
- `stale-surface` - intake or tracking surface accumulates without cleanup
- `forgotten-deferral` - deferred work has no exit condition or resurfacing rule
- `reminder-rot` - a standing reminder survives after its reason is gone
- `orphan` - source disappears while projection or reference remains
- `convention-creep` - the documented habit and the real operating pattern diverge
- `articulation-lag` - a stable principle is articulated in conversation but durable capture (memory, Planning doc, doctrine) lags by one or more sessions; re-articulation continues until someone captures it. Distinct from `reinvention` (the principle isn't rebuilt, it's just absent from durable surfaces) and `forgotten-deferral` (no task was ever opened). Common when capture decisions are gated on present-tense usefulness; counter-example to the deferred-value collection principle.
- `reinvention` - existing infrastructure is missed and rebuilt in parallel
- `context-fade` - explicit doctrine loaded at session/task start loses behavioral force as context grows; behavior reverts to training defaults despite the doctrine still being present in context. Distinct from convention-creep (the doctrine is correct, not divergent) and reminder-rot (the doctrine has not outlived its purpose). The failure is that an active, correct doctrine becomes inactive without anyone changing it. Common in long-running AI sessions and in any process where attention to a standing rule decays under operational pressure.

Coin a new term when none of these fits better than a vague description.

## Mechanism Taxonomy

- `watch-triggered sync` - an event fires the update instead of a person remembering
- `upsert by stable id` - identity follows durable content, not location
- `orphan sweep` - missing items are marked and recover cleanly if restored
- `generated-not-edited` - projections are regenerated from source each run
- `hash invariant` - mismatch becomes a visible signal instead of silent drift
- `self-extinguishing schedule` - reminders or checks shut off when their job is done
- `import-not-copy` - the live source is referenced directly
- `structural read-only` - projection surfaces omit write paths
- `boundary validation` - required fields or shape are enforced at the schema or handler boundary, so malformed writes are rejected up front
- `examine-before-build` - check for existing infrastructure before authoring new structure
- `output-pattern-intercept` - a check at the output boundary that scans for known failure-mode language or structure and either blocks the output or annotates it before it reaches the receiver. Survives the cognitive drift it is checking for because it does not depend on the producer being calibrated. Fits AI-output drift, output-shape violations, or any case where the producer cannot be trusted to detect its own pattern in real time. Real-time interception is the strong form; post-process scanning is weaker (closer to andon).
- `articulation-as-capture-trigger` - listener-side intercept: when stated input matches stance/principle/repetition language patterns ("again", "before", "many times", "I've said", "what drives me is", "my view is", "the real question"), fire a capture step (write feedback memory, log signal evidence, draft a Planning doc) before continuing the conversation. A specific application of `output-pattern-intercept` operating on inputs rather than outputs. Implemented 2026-05-03 as `~/.claude/hooks/userprompt_ted_signal_recognition.py` with catalog at `~/.claude/hooks/ted_trigger_phrases.txt`; that implementation surfaces routing to relevant calibration file + concept_key + skill suggestion when Ted's signal phrases hit. The hook is one realization; the mechanism generalizes (could also be implemented as a skill that GPTs read, or as a pre-prompt classifier). The principle is structural recognition of stated-input patterns instead of relying on the listener's judgment to notice in real time.

## Boundary With Andon

Poka-yoke prevents the failure. Andon surfaces a failure that slipped through, or a condition that cannot yet be prevented structurally.

If the best available move is surfacing, say that plainly. Do not call a notification, dashboard, or reminder prevention unless it actually removes remembering from the loop.

## Boundary With FMEA

FMEA names and assesses failure modes. Poka-yoke chooses and applies the prevention mechanism.

Do not jump straight to a mechanism without first naming what is failing and why.

## Core Workflow

Before accepting a manual step as normal operating procedure, ask whether the step itself is a poka-yoke candidate. If the answer requires remembering, it probably is.

1. Name the failure mode.
Use the vocabulary above or coin a better term.

2. Decide whether the problem is preventable or surface-only.
Some risks can be removed structurally. Others can only be surfaced well.

3. Choose a contained sufficient mechanism.
Prefer the lightest move that actually removes remembering from the loop.

4. Test the mechanism itself.
If the proposed prevention still depends on someone remembering to run, update, or clean it, it is not poka-yoke yet.

5. Note the taxonomy delta when needed.
If this case reveals a new failure mode or mechanism, propose the addition inline so the skill can stay current.

## Output Shape

- `Failure mode`
- `Preventable or surface-only`
- `Mechanism`
- `Why structural`
- `Taxonomy delta` (only if needed)

Keep the output compact and decision-ready.

## Never Assume

- Do not assume every annoyance deserves structural prevention
- Do not confuse a policy, reminder, or convention with enforcement
- Do not call andon prevention
- Do not add ceremony when an existing structure already prevents the problem
- Do not propose a mechanism before naming the failure mode
- Do not ignore the cleanup half of prevention for accumulating surfaces

## Update-Surfacing Backstop

This skill stays current by adding new failure modes or mechanisms only when live use exposes one that the current taxonomy cannot name cleanly. If a recurring failure mode in real work cannot be named with the existing vocabulary, or if a new prevention mechanism appears that doesn't fit the existing taxonomy:

- check the failure-mode and mechanism lists above for the closest existing fit before coining a new term
- coin only when no existing entry fits cleanly
- propose the addition with a one-line rationale tying it to the live case that exposed the gap. By default, write the proposal to `PROPOSED_DELTAS.md` (next to this SKILL.md) for batch evaluation at the next `skills-review` pass. Apply directly to SKILL.md (skipping the holding file) only when the urgency criteria in `PROPOSED_DELTAS.md` apply (critical bug, purely additive zero-risk fix, or live-use block).

`skills-review` is the periodic backstop and reads `PROPOSED_DELTAS.md` on each pass. Per-use surfacing is the main one — this skill's own per-use rule for naming a delta is what keeps the taxonomy current.

## Scripts vs. Skill

Use this skill for judgment about what kind of prevention is appropriate.

Add scripts only when a mechanism becomes stable enough to validate or execute mechanically. The recognition step should stay here.
