---
name: digest-topic-refresh
description: Read the newest digest material, compare it against an existing living topic and index state, then decide whether to leave unchanged, update the topic, or create a new topic. Use when fresh digest items may materially affect an existing research artifact in a research-memory workflow. Do not use for first-pass source ingestion with no existing topic context, or when the task is only to summarize a digest without comparison.
category: judgment-only
write_mode: file
one_line_use: compare digest deltas against a living topic
fast_pick: "yes"
---

# Digest Topic Refresh

Compare fresh digest material against living topic state and write only when the digest adds real signal.

This skill is for the judgment-heavy pass between "new digest exists" and "artifact should change." Its job is to compare, classify the material delta, and decide one of three outcomes:

- `no change`
- `update existing topic`
- `create new topic`

Use it when the main question is whether new digest material changes an already-living artifact. Do not use it for routing, evidence logging, or first-pass topic creation from scratch.

## Inputs That Matter

- Latest digest checkpoint or equivalent summary surface
- Newest full digest file or files
- Existing index entry or entries
- Existing living artifact or artifacts
- Domain filter for relevance
- User-scoped question, if one was given

## Required Read Order

1. Read the current index to locate candidate existing topics.
2. Read the matching living artifact or artifacts.
3. Read the latest checkpoint or `LAST_DIGEST` surface.
4. Read the newest full digest file or files that post-date or materially sharpen the checkpoint.
5. Only then decide whether a true delta exists.

## Relevance Filter

Keep only digest items that affect the topic through one or more of these:

- new federal or state policy actions
- regulatory pathway changes
- guidance, implementation detail, funding, or access changes
- new trial results, approvals, denials, CRLs, safety findings, or guideline shifts
- operational details that change how the topic should be interpreted in practice

Discard or down-rank:

- commentary with no new factual content
- repetitions of already-captured items
- weakly related background news
- rhetorical or political signaling that does not change topic state

## Material-Delta Test

Update only if the digest adds at least one of the following:

- a new fact not present in the artifact
- a more concrete implementation detail that changes operational meaning
- a meaningful change in evidence level, safety picture, regulatory posture, or treatment availability
- a conceptually important sharpening of uncertainty, limits, or watchpoints

If the digest only repeats the existing artifact in fresher wording, do not update.

## Decision Rule

Choose exactly one:

- `no change` when there is no material delta
- `update existing topic` when there is a material delta that belongs inside the current topic boundary
- `create new topic` when the new material has its own distinct claim set, evidence base, or operational implications and would distort the existing artifact if folded into it

Prefer updating the existing topic over creating a near-duplicate artifact.

## Comparison Method

For each relevant digest item:

1. State what the artifact already says.
2. State what the digest adds, sharpens, or contradicts.
3. Name whether the change is about evidence, policy, safety, regulation, implementation, or interpretation.
4. Decide whether that change is material enough to revise the living topic.

## Guardrails

- Never confuse policy acceleration with proof of efficacy.
- Never confuse funding or executive attention with approval, coverage, or standard-of-care status.
- Preserve uncertainty explicitly when digest material is politically salient but clinically immature.
- Do not overwrite a broader topic with a narrow digest item; fold it in proportionally.
- If multiple topics are plausible, name the ambiguity and choose the best fit rather than duplicating content.

## Persistence Rule

If the topic changes:

1. write the revised artifact
2. update the index entry

If the topic does not change:

- answer with the comparison result
- do not force a write merely to show activity

## Output Shape

Use this compact structure unless Ted asks for another format:

- `existing topic found`
- `relevant digest items`
- `material delta`
- `update decision`
- `what changed in the topic`
- `revised living artifact` or `no artifact change`
- `index updated` or `index unchanged`

## Boundary With Nearby Skills

- Use `signal-review` when an accepted material delta should also become `signal_evidence`. This skill stops at topic comparison and topic update.
- Use `surface-routing` when the main question is where the revised artifact or follow-on proposal should live.
- Use `concept-bridge-surfacing` when the main value is naming a concept that the digest material surfaced.
- Do not stretch this skill into general digest summarization or research synthesis with no living artifact in play.

## Never Assume

- Do not assume the newest digest item is more correct than the existing artifact; compare, do not defer blindly.
- Do not assume recency equals materiality.
- Do not assume a named compound deserves its own artifact if it clearly belongs inside a broader living topic.
- Do not assume every digest run should produce an update.

## Update-Surfacing Backstop

This skill assumes a checkpoint surface plus full digest files, with a living index and artifact layer to compare against. If any of these drift:

- the digest checkpoint format changes
- the `LAST_DIGEST` or equivalent checkpoint surface moves
- the archive location for full digests changes
- the target domain stops using an index + living-artifact pattern

Do not silently improvise from stale assumptions. Instead:

- check the current digest surfaces and file locations directly
- check `Operations/CHANGES_LOG.md` for recent digest or routing changes
- if the write target is unclear, stop at the comparison result and route the placement question through `surface-routing`
- surface the mismatch to Ted and propose the SKILL.md correction in the same turn
