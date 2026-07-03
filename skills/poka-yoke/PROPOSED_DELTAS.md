# Proposed Deltas — poka-yoke

Pending taxonomy additions or skill changes held for the next `skills-review` pass. Batch review lets related deltas be evaluated in context with each other — entries that touch the same boundary get implemented coherently rather than in isolation.

## Urgency criteria — implement immediately rather than hold

Apply a delta directly to `SKILL.md` (skipping this holding file) only when:

- **Critical bug** — skill is misleading, dangerous, or actively wrong as currently written
- **Purely additive zero-risk fix** — typo, broken link, dead reference, missing word
- **Live-use block** — current absence of the delta is blocking session work right now

Otherwise: hold here. `skills-review` reads this file on each pass and decides what to apply, defer, or close as superseded.

## Format

Each entry has: date, name, proposed text/change, and a one-line rationale tying it to the live case that exposed the gap.

---

## 2026-05-03 — applied via skills-review

The 2026-05-01 `articulation-lag` and `articulation-as-capture-trigger` deltas were applied to `SKILL.md` after the listener-side hook implementation validated the mechanism in live use.
