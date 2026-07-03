---
name: skills-review
description: Review the shared skills in ~/Skills/ for fit, overlap, gaps, adoption, and CLiP connection, then propose specific changes instead of just observations. Use when a new skill is proposed, when the set feels stale or crowded, or during a periodic cleanup pass. Always read live files — never evaluate from memory. Do not use for app-specific skills unless explicitly asked.
category: meta
write_mode: none
one_line_use: review the skill set itself
fast_pick: "yes"
---

# Skills Review

Evaluate the shared skill set from live files and produce specific proposals, not just observations.

`~/Skills/` is the canonical source. `~/.claude/skills/` and `~/.codex/skills/` are aliases to the same files — read `~/Skills/` only.

## When to Trigger

- A new skill is proposed (by Ted, Codex, or Coordinator)
- The set has grown and hasn't been reviewed recently
- Something in the set feels off, redundant, or unused
- A CLiP cycle surfaces a recurring judgment move that has no skill yet
- Periodic review (quarterly or when explicitly requested)

## What to Read

1. `~/Skills/` — all SKILL.md files, live from disk
2. Note which skills are app-specific and intentionally excluded from the shared set
3. `~/Skills/<skill>/PROPOSED_DELTAS.md` per skill if present — holding location for deltas queued for batch review (see urgency criteria in each file). The default home for non-urgent skill changes; reading this is part of every review pass.

Read the description frontmatter and enough of the body to understand trigger conditions, output shape, and boundaries with adjacent skills.

## What to Evaluate

**Fit:** Does each skill do what its description says? Are the trigger conditions accurate? Would I know when to apply it?

**Overlap:** Are two or more skills firing in the same conditions? Can one absorb the other without losing anything real? Consolidation is better than coexistence when the underlying operation is the same.

**Gaps:** Is there a recurring judgment move that appears in real work but has no skill? Name it as a candidate — do not build it yet.

**CLiP connection:** Do the skills map onto CLiP steps? Skills are the session-level interface to the CLiP cycle:
- `concept-bridge-surfacing` (document review) → Observation/Capture step applied to digest material
- `proposal-candidate-surfacing` → CLiP mid-cycle trigger
- `proposal-packet` → CLiP Synthesis output format

Note where the mapping is clean and where it isn't.

**Adoption:** Are skills being applied proactively, or only when invoked? If proactive application isn't happening, ask whether the trigger conditions are clear enough or whether the skill is too similar to another.

**Update-surfacing mechanism:** Does the skill specify how it stays current when its domain shifts? Look for a self-extending check, a periodic review hook, or another explicit resurfacing path. A skill with no update mechanism can become memory-dependent maintenance. Flag it and propose a fitting backstop.

**Pending deltas:** For each skill with a `PROPOSED_DELTAS.md`, evaluate whether the queued entries are still relevant, whether they interact with other pending deltas (within the same skill or across skills with adjacent domains), and which should be applied this pass. Decide: apply, defer with reason, or close as superseded. Do not leave entries unaddressed across multiple reviews without naming why.

## How to Coordinate

If authoring or implementation changes are needed, route them through the current implementation-authorized actor for shared skills. In this workspace, Codex is the default implementer for shared skill files and related git work.

Route to Codex when:
- A new skill needs to be written
- An existing skill needs structural changes
- A consolidation proposal requires a new SKILL.md

Shared-skill reviews may propose changes, but proposals are not implementation authority. Do not author changes unilaterally unless Ted explicitly delegates that implementation slice to the current actor.

## Output Shape

- **Assessment:** one-line status for each skill (fit / overlap / gap / CLiP connection)
- **Proposals:** specific, named changes — consolidate X and Y, retire Z, add candidate for W
- **Coordination note:** what needs Codex involvement and why
- **CLiP advancement note:** if the review produces evidence relevant to CLiP or KA/CLiP/Taxonomy advancement, say so and offer to log it

Keep the output compact. Proposals over observations.

## Never Assume

- Do not evaluate from memory — always read live files first
- Do not propose changes without naming the specific overlap or gap that justifies them
- Do not author new skills without Codex involvement unless explicitly delegated
- Do not treat app-specific skills (session-start, session-end, pdf) as part of the shared set unless asked
- Do not consolidate skills that have genuinely different trigger conditions, even if their bodies look similar

## Scripts vs. Skill

Use this skill for judgment-heavy evaluation of the skill set.

A script could automate listing skills and checking for structural issues (missing frontmatter, broken symlinks). If that becomes a recurring need, add a small validator script alongside this skill rather than growing this file into a checklist.

## Update-Surfacing Backstop

This skill stays current when shared-skill conventions, authorship rules, or CLiP-step mapping change. If live use shows this skill applying outdated coordination directives, missing a new audit dimension, or pointing at the wrong canonical skills location:

- check `Canon/AI_Coordination/Active_Team_Agreements.md` for changes to Codex/CC authorship rules
- check the actual `~/Skills/` directory layout in case the canonical source has moved
- check whether new skill conventions (heading patterns, frontmatter fields, evaluation dimensions) have emerged in recently-edited skills and aren't yet reflected in this skill's audit list
- update this skill in the same pass as the convention shift, not later

Per-use convention drift during real review work is the main backstop. The skill checks itself when run; the audit it performs on others should also be applied to its own coverage.
