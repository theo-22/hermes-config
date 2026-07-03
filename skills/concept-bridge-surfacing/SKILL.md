---
name: concept-bridge-surfacing
description: Map Ted's local term, recurring idea, or document passage to the closest useful established concept so the right standard name can be adopted without losing the original meaning. Use in live conversation or document review when naming would improve orientation, search, retrieval, or the next decision. Do not use when the main question is layer classification, when the concept match is weak, or when Ted already wants a full taxonomy or formal write-up.
category: database-integrated
write_mode: db
one_line_use: name the idea
fast_pick: "yes"
---

# Concept Bridge Surfacing

Bridge Ted's observation, local term, or document passage to the closest useful existing concept.

Use this skill as a terminology-check reflex when Ted uses a term that seems important but ambiguous, locally coined, metaphorical, or structurally loaded. First preserve the meaning and, when needed, ask what he means. Do not silently accept the first term and build structure from it. The operating stance is: defer to Ted's intent, not automatically to Ted's first wording.

**Adoption of the standard term is one outcome, not the goal.** Bridge first, then classify and **ask Ted per term** which way it resolves:

- **Adopt** — his term is *just* the standard concept → move to the standard name, especially early before the name sets.
- **Keep as umbrella** — his term is a *superset*: the standard concept *plus* more. Keep his term and name the real concept(s) *inside* it with standard terms used alongside. Flattening a non-flat term loses meaning.
- **Stand-alone keep** — genuinely unique (rare); his term is usable because nothing else covers it.

Prior: a real concept usually exists, so make "keep" *earn it.* Don't over-validate Ted's coinage — failing to help him adopt a clean standard term when one fits is its own failure (reads as support, functions as resistance). Decide *with* Ted, per term; volume is low, so this is a discussion as terms arise, not a process. (`Set` terms — already established — add cost-to-change on top of the type judgment.)

Two phases (the adopt path):

- `bridge`: introduce the standard concept alongside Ted's wording; explain why the match holds; confirm understanding
- `adoption`: once Ted grasps the concept, use the standard term going forward; gently use it when Ted uses his old term

**Adoption tracking (added 2026-05-08 per R1 research):** bridge use is now telemetered. When a bridge is used in working output (named in a plan, applied to a decision, referenced in an audit case file), log via `~/Commands/Workspace/BridgeUsed.command <bridge_id> [u|p] [shaped|noted|corrected] [note]`. Auto-promote script `Control/backend/scripts/bridge_adoption_promote.py` reads bridge-use events and promotes bridges meeting criteria: ≥3 distinct sessions OR ≥2 distinct AIs; ≥1 use shaped a plan/review/decision; ≥50% of uses are unprompted (no fresh bridge read in immediately preceding window). The "unprompted" requirement is the load-bearing distinction between echo and durable internalization. Ted can log uses he notices; future-CC discipline: log uses in working output when invoking a bridge.

Use this skill in two contexts:

- `live discussion`: when a recurring idea, structure, or operating move is taking shape in conversation
- `document review`: when digest, note, or synthesis material would become easier to search, learn from, or revisit with a light concept bridge

## Database Integration

Before proposing a bridge, check whether the concept has already been bridged:

```bash
curl -s "http://localhost:5555/api/concept-bridges/check?concept=TERM_HERE"
```

When a bridge is accepted by Ted, write it to the database:

```bash
curl -X POST http://localhost:5555/api/concept-bridges \
  -H "Content-Type: application/json" \
  -d '{"local_term": "...", "standard_concept": "...", "why_match": "...", "difference": "...", "actor": "<current_actor>"}'
```

Set `<current_actor>` to the runtime using the skill, such as `codex`, `claude_code`, `coordinator_gpt`, or another explicit actor value used by the live telemetry path.

When Ted confirms adoption (standard term replaces local term in practice), mark it:

```bash
curl -X POST http://localhost:5555/api/concept-bridges/adopt \
  -H "Content-Type: application/json" \
  -d '{"bridge_id": N}'
```

Current bridges in the database:
!`curl -s http://localhost:5555/api/concept-bridges 2>/dev/null | python3 -c "import sys,json; [print(f'  {b[\"local_term\"]} -> {b[\"standard_concept\"]} [{b[\"phase\"]}]') for b in json.load(sys.stdin)]" 2>/dev/null || echo "  (backend not responding)"`

## Inputs That Matter

- Ted's original observation, passage, or local term
- Whether the idea feels recurring or structurally meaningful rather than one-off
- Whether there is a reasonably strong concept match
- Whether naming it would improve orientation, search, retrieval, or the next implementation decision
- Whether the concept match changes how the thing is usually handled
- Whether the match is strong, partial, or weak

## Core Workflow

1. Preserve the original idea first.
Do not start by replacing Ted's phrasing with official terminology.

If the term is unclear, ask a terminology-check question before proposing structure:

- "When you say `<term>`, do you mean `<interpretation A>` or `<interpretation B>`?"
- "I may be mapping that word wrong. What job is this thing doing in the system?"

2. Test for a real concept match.
Choose the closest useful concept only when it genuinely clarifies the idea. If confidence is low, say so plainly.

3. Add the right-sized bridge.
Prefer:
- `Closest concept`
- `Why`
- `Difference` when useful

4. Add context-specific value only when it helps.
Use `Usually handled as` when the concept match changes implementation or classification.
Use `Why this matters` when the bridge improves retrieval, search, learning, or connection to Ted's current method.

5. Check for understanding before adoption.
Do not shift to the standard term until it's clear Ted has internalized the concept. A confirmation ("yes, that's exactly what I meant") or sustained use is enough signal. If uncertain, ask.

6. After adoption, use the standard term.
Once understanding is confirmed, use the standard term in conversation. If Ted uses the old term, briefly reflect the standard one back without correcting — let the swap happen naturally.

7. Stop early.
Do not turn a naming move into a lecture, migration plan, taxonomy, or redesign unless Ted asks.

## Context Notes

### Live Discussion

Use when a live discussion starts to sound like an existing named concept and a short naming move would help Ted orient.

Focus on:

- what feature of the live idea triggered the match
- whether the match changes the next question or implementation move
- keeping the bridge brief enough not to derail the discussion

### Document Review

Use when reviewing digests, notes, or synthesis material and a concept label would make the material easier to learn from, search, or revisit later.

Focus on:

- preserving the original wording and intent of the passage
- adding a concept bridge only when it improves future retrieval or understanding
- connecting the match to Ted's current method or recurring local pattern when that adds real value

## Output Shape

When the match is strong:

- `Closest concept: <name>`
- `Why: <one short explanation>`
- `Difference: <optional short note>`
- `Usually handled as: <optional layer / form>`
- `Why this matters: <optional short note>`

When the match is partial:

- `Closest concept so far: <name>`
- `Why: <one short explanation>`
- `Difference: <optional short note>`
- `Usually handled as: <optional layer / form>`
- `Confidence: partial`

When no strong match exists:

- `No clean standard concept yet`
- `Why: <one short explanation>`

Keep the response to 1-3 short paragraphs or 2-5 short sentences unless Ted asks for more.

## Never Assume

- Do not force terminology onto every good observation or document passage.
- Do not treat Ted's first term as settled when the meaning is unclear.
- Do not build, route, or save structure from an unclear term before checking the intended meaning.
- Do not force a weak match just to sound helpful.
- Do not push adoption before understanding is confirmed — the bridge phase exists to prevent premature switching.
- Do not preserve Ted's wording indefinitely once the concept has landed — adoption is the goal.
- Do not politely reinforce a likely misclassification.
- Do not imply that a named concept is automatically best practice.
- Do not imply that naming something means it is finished or settled.
- Do not build structure before checking whether the concept match changes handling.
- Do not recommend building a skill, script, or process from the pattern unless Ted asks for that next step.
- Do not turn a naming move into a taxonomy, theory lesson, or formal framework unless Ted asks.

## Boundary With Nearby Skills

- Use `structure-distinction-surfacing` when the main question is which layer something belongs to.
- Use `proposal-candidate-surfacing` when the main question is whether the discussion has crossed into a real proposal candidate.
- Use `proposal-packet` when Ted already wants a durable proposal packet rather than a light naming move.
- Use this skill when the main value is bridging Ted's wording or source material to the closest useful concept.

## Scripts vs. Skill

Use this skill for judgment-heavy naming and concept bridging in live discussion or document review.

Do not add scripts for this. The value is interpretive, not deterministic.

## Update-Surfacing Backstop

This skill embeds live GETs and POSTs against `localhost:5555/api/concept-bridges`. If the check endpoint errors, the adoption POST shape changes (e.g., `bridge_id` becomes `id`), or the listing response stops parsing:

- Do not silently skip the DB check and write a markdown bridge instead.
- Check `Control/backend/app.py` for current routes and payload fields.
- Check `Operations/CHANGES_LOG.md` for recent concept-bridges API changes.
- Surface the mismatch to Ted and propose a SKILL.md correction in the same turn.
