---
name: signal-review
description: Pressure-test an input for signal worth preserving, then write accepted evidence units to the system database with tags and destination. Use when external signal, digest material, or weak internal patterns need vetting before they enter the evidence base. Do not use for completed findings ready for synthesis (use synthesis-review) or for live coordination (use coordinate mode directly).
category: database-integrated
write_mode: db
one_line_use: pressure-test and save evidence
fast_pick: "yes"
---

# Signal Review

Pressure-test whether an input carries enough signal to be worth finding again. If it does, write it to the system database as an accepted evidence unit.

This skill replaces the markdown-append workflow. Accepted units go to the database via the backend API — not to Signal_Evidence_Log.md.

## Before You Start

Check current system state so you don't duplicate or miss context:

- Existing clusters: !`curl -s http://localhost:5555/api/signal-evidence/clusters?min_count=3 2>/dev/null | python3 -c "import sys,json; [print(f'  {c[\"tag\"]}: {c[\"count\"]} units') for c in json.load(sys.stdin)]" 2>/dev/null || echo "  (backend not responding — use python3 directly against system.db)"`
- Recent evidence: !`curl -s "http://localhost:5555/api/signal-evidence?limit=5" 2>/dev/null | python3 -c "import sys,json; [print(f'  [{e[\"tags\"]}] {e[\"signal\"][:80]}') for e in json.load(sys.stdin)]" 2>/dev/null || echo "  (backend not responding)"`

## Save Gate

The default answer is **no save**. The question at the gate:

> Does this unit carry enough signal to be worth finding again?

If the answer is not clearly yes, do not save. Volume is a sign the gate is weak, not that the session was productive.

## Inputs That Matter

- The raw input: digest article, conversation excerpt, observation, pattern
- Whether the idea is recurring or structurally meaningful (not one-off)
- Whether it connects to an existing cluster (check clusters above)
- Whether it changes how something is usually handled

## Core Workflow

1. **Read the input.** Understand what is being claimed or observed.

2. **Pressure-test it.** Is this signal or noise? Would you look for this again? Does it connect to something already accumulating?

3. **If accepted:** Write an evidence unit (1-5 sentences) with:
   - `signal` — what was observed
   - `why_it_matters` — why this is worth preserving
   - `tags` — light comma-separated tags; check existing clusters before inventing new ones
   - `destination` — where this should resurface (e.g., "KA advancement", "Learning System", "Canon candidate")

4. **Write to database.** Set `actor` to the current runtime applying the skill (for example, `codex`, `claude_code`, or another explicit actor), rather than copying a hard-coded example value:
   ```bash
   curl -X POST http://localhost:5555/api/signal-evidence \
     -H "Content-Type: application/json" \
     -d '{"signal": "...", "why_it_matters": "...", "tags": "...", "destination": "...", "actor": "<current_actor>"}'
   ```

5. **Check for elevation.** After writing, check clusters again. If any cluster now has 3+ units pointing the same direction, note it as an elevation candidate for Ted.

6. **If KA, CLiP, or Taxonomy tagged:** Explicitly note which advancement surface it should reach — KA_CLiP_Taxonomy_Advancement_Checklist.md or Learning System development surfaces — not only the database.

## Session Constraints

- **Cap: 3 accepted units per session for organic/conversational signal.** More than 3 in a normal session = save gate is drifting.
- **No cap for pre-screened harvest lists.** When input comes from a Triage audit harvest case file, the Triage Auditor already did the filtering. Apply the save gate per unit but do not impose a session count limit — volume from a harvest is expected, not a drift signal.
- **Tags: keep light.** 2-4 tags per unit. Check existing clusters before creating new tags.
- **Comparability:** Accepted units should be at the same level of abstraction — finding, implication, or design question. Do not mix levels unless explicitly named.

## Exit Checklist

Before leaving signal review, state:
- Save gate: held / did not hold
- Accepted units: count
- Drift signs: none / tag creep / volume creep / comparability issue
- Elevation candidates: any clusters that crossed threshold

## Boundary With Adjacent Skills

- Use `synthesis-review` when the material is completed findings ready for cross-pass synthesis.
- Use `concept-bridge-surfacing` when the main value is naming, not evidence collection.
- Use `surface-routing` when the question is where to place an already-accepted artifact.
- Use `proposal-candidate-surfacing` when the question is whether a discussion has become a proposal.

## Never Assume

- Do not save just because the input is interesting.
- Do not create new tags when existing cluster tags fit.
- Do not treat surfacing as readiness for Canon.
- Do not skip the save gate for digest material — articles carry external authority, not local authority.
- Do not exceed the session cap for organic signal without naming why. Harvest input from a Triage audit is exempt from the count cap.

## Update-Surfacing Backstop

This skill embeds live POSTs and GETs against `localhost:5555`. If endpoints 404, shapes change (e.g., `tags` field renamed, `actor` required/removed), or clusters/evidence responses stop parsing:

- Do not work around the drift by constructing a markdown fallback.
- Check `Control/backend/app.py` for the current route contract.
- Check `Operations/CHANGES_LOG.md` for recent signal-evidence or API changes.
- Surface the mismatch to Ted and propose a SKILL.md correction in the same turn.
