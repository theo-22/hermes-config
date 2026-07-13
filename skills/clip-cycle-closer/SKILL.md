---
name: clip-cycle-closer
description: Recognize when a coherent CLiP arc has completed or crossed a meaningful threshold, then draft a concise evidence-backed closure record for logging, routing, or adoption follow-up. Use when a session starts sounding like "this looks like a CLiP arc," "we should log this," "this session produced something durable," or "this is probably a methodology capture event," and the evidence already shows a Canon-level cycle, domain-level cycle, bridge adoption event, adversarial review step, or synthesis-ready partial cycle. Fire proactively — do not wait to be invoked — when a session produces a confirmed finding that has gone through a full observe → capture → validate arc. Do not use for raw capture, routine proposal drafting, or promotion decisions.
category: judgment-only
write_mode: none
one_line_use: name the cycle as closed and draft the record
fast_pick: "yes"
---

# CLiP Cycle Closer

Recognize when CLiP has already happened and make the completion legible.

This skill covers the closing move after observation, capture, accumulation, synthesis, or output already exists. Its job is to name the cycle status, classify the cycle type, point to the evidence, and draft the concise durable record needed for the next surface.

Concrete trigger phrases to notice:
- "This looks like a CLiP arc."
- "We should log this."
- "This session produced something durable."
- "This feels like a methodology capture event."
- "What counts as the closure record here?"

Concrete pattern triggers to notice even without explicit CLiP language:
- An audit, multi-AI review, council, or live-evidence check caught a miss and the session produced a structural correction in response.
- One session produced several accepted evidence units, added or advanced a concept bridge, and strengthened a shared doctrine, method, or routing surface.
- A validate step materially changed the output rather than merely approving it; that is often an observe -> capture -> validate -> recover arc.
- A repeated failure mode moved from "remember to do this" into a structural prevention layer or reusable procedure.

**Interrupt now if all of these are true:**
- a durable artifact was produced (document, skill, finding, methodology)
- it was reviewed or validated in some form, especially by audit, multi-AI review, council, or live-evidence verification
- resurfacing surfaces (Learning System, CHANGES_LOG, concept bridges, routing) were updated
- the next move is logging or adoption follow-up, not more creation

Do not wait for the words "CLiP cycle" to appear. Infer completion from the evidence chain.

This is not a promotion skill. It does not decide Canon status, does not silently log cycles, and does not mutate bridge state unless Ted explicitly asks for that next step.

## Inputs That Matter

- The concrete artifact, output, or session outcome
- The evidence chain showing what actually happened
- Whether the arc is Canon-level, domain-level, bridge adoption, adversarial review, or still partial
- Whether a dedicated CLiP ledger or destination surface already exists
- What remains incomplete, if anything

## Cycle Types

- `Canon-level cycle` — observation through Canon update
- `Domain-level cycle` — observation through domain artifact or operational change
- `Partial cycle` — enough evidence to say synthesis or closure is now due, but not finished
- `Bridge adoption event` — a concept bridge has clearly moved from bridge to active use
- `Adversarial review run` — a second reviewer materially challenged and improved a synthesis output
- `Methodology capture event` — a session produced a reusable process pattern, playbook entry, or know-how artifact that wasn't in the system before. Observe arc = the session work itself; capture arc = the methodology document; validate arc = document reviewed and surfaces updated.

Use the most accurate bounded label. Do not inflate a good session into a full cycle if the evidence only supports a partial one.

## Workflow

1. Confirm there is a real cycle candidate.
Look for an actual observe -> capture/accumulate -> synthesize/output arc, not just a productive conversation.

2. Name the evidence chain.
State what counts as observation, what counts as the intermediate work, and what counts as the output or close step. If one link is missing, say so.

3. Classify the cycle status.
Choose one:
- `completed`
- `near-complete`
- `partial`
- `adoption event`
- `adversarial-review complete`

4. Choose the destination.
Name where the closure record belongs:
- CLiP cycle ledger
- concept bridge adoption pass
- CHANGES_LOG tag or note
- domain artifact note
- synthesis-ready queue

If the destination surface does not exist yet, say so plainly and draft the record anyway.

5. Draft the concise durable record.
Include:
- cycle type
- one-sentence arc
- concrete evidence
- destination
- next action, if any

6. Stop before execution.
Do not log, promote, mark adopted, or route anything unless Ted explicitly asks for that next step.

## Output Shape

- `Cycle status`
- `Cycle type`
- `Why it counts`
- `Evidence`
- `Draft closure record`
- `Suggested destination`
- `Open gap` (only if something is still missing)

Keep the response compact. The value is recognition and closure drafting, not another long synthesis memo.

## Boundary With Nearby Skills

- Use `signal-review` when the main job is deciding whether an observation should enter the evidence base.
- Use `proposal-candidate-surfacing` when the main question is whether a discussion has crossed into proposal territory.
- Use `proposal-packet` when the user wants a durable proposal or handoff packet.
- Use `surface-routing` when the main question is where an already-formed artifact should live.
- Use this skill when the main question is whether a CLiP cycle has completed enough to be named and logged.

## Never Assume

- Do not call every useful session a CLiP cycle.
- Do not declare completion without naming evidence.
- Do not confuse synthesis output with promotion.
- Do not mark bridge adoption just because a concept was mentioned once.
- Do not silently create a ledger convention if the surface does not exist yet.
- Do not turn closure recognition into a Canon decision.
- Do not wait for explicit CLiP language — infer arc completion from the evidence chain.

## Scripts vs. Skill

Use this skill for closure judgment and compact cycle drafting.

If repeated use stabilizes a fixed ledger format later, add a validator or renderer script then. Do not build that machinery into the skill before the closure pattern is proven.

## Watch Status

Monitor since 2026-04-28 for boundary drift with `synthesis-review`. Both skills produce closure-shaped output. The intended boundary: **clip-cycle-closer** fires when a coherent CLiP arc has completed (observe → name → record → structurally prevent), drafting a closure record. **synthesis-review** fires on accumulated cross-pass material maturing into higher-signal memo. Boundary is real but subtle.

Revise trigger language if: live use shows the same situation invoking both skills, or a closure record from one skill duplicates a memo from the other. Keep both as-is if drift doesn't appear after 5+ instances of either skill firing.

## Update-Surfacing Backstop

This skill assumes the current CLiP cycle labels, closure statuses, and destination surfaces are still the right ones to name a completed arc. If live use exposes a cycle outcome that the current status labels, cycle types, or destination list cannot classify cleanly:

- check the current CLiP logging surface and recent closure examples first
- check `Operations/CHANGES_LOG.md` for CLiP or routing changes that may have shifted the vocabulary in practice
- do not force the old label set onto a new closure shape; surface the mismatch and propose the SKILL.md correction in the same turn

`skills-review` is the periodic backstop. Per-use surfacing is the main one.
