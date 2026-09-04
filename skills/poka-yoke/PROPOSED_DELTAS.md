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

## 2026-09-03 — applied via targeted skills-review: evidence-contamination and side-effect isolation

Added `evidence-contamination` to the failure-mode vocabulary and `side-effect isolation` to the mechanism taxonomy. The two-sided verification requirement preserves production observability while preventing fixture activity from entering real rankings; cleanup is routed through the evidence surface's recoverable lifecycle.

**Rationale:** Image Factory `create_exhibit` tests isolated their filesystem paths but still wrote load-bearing temporary exhibits into production `surface_touches`, where Coordinator ranked them as real attention. Control commit `422ebc55` added explicit test-mode suppression, proved live-mode emission remained intact, and recoverably retired the six confirmed fixture rows.

## 2026-08-16 — new mechanism: redundant-cadence recovery

**Proposed addition to Mechanism Taxonomy:** `redundant-cadence recovery` - a job survives an isolated failure without anyone noticing because it has two properties together: (1) idempotent — it checks durable state (a ledger, a dedup key) before acting, so re-running after a failure never duplicates or corrupts anything; (2) high-frequency — it runs often enough relative to the cost of a missed cycle that a single failure's damage window is small. Neither property alone is sufficient: idempotent-but-rare leaves a long silent gap; frequent-but-not-idempotent risks damage on the retry itself. Distinct from `self-extinguishing schedule` (that's about a check turning itself off when its job is done, not about surviving its own failure).

**Rationale:** live case, Hermes `ai-inbox-claude-triage` cron job (2026-08-16). A 429 rate-limit error killed one scheduled run outright (no retry, no fallback, confirmed from the run's own output log). The very next scheduled run 3 hours later picked up everything the failed run would have caught, with zero loss, because the job checks an append-only ledger of already-judged files before acting. Ted's framing, verbatim: "self-healing sounds like poka-yoke, how do we have more of it?" — the answer is these two specific properties, not a general vibe. Worth naming so other single-point-of-failure jobs can be checked against a concrete bar instead of an intuition.

## 2026-05-03 — applied via skills-review

The 2026-05-01 `articulation-lag` and `articulation-as-capture-trigger` deltas were applied to `SKILL.md` after the listener-side hook implementation validated the mechanism in live use.
