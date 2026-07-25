---
name: contradiction-sweep
description: Hand a session's own artifacts to a different, uncommitted model and ask it to find contradictions between them — the ones the author resolved without noticing. Use before a session close, a handoff, or any packet built from several documents written in one sitting, and whenever a run of doctrine/plan/code artifacts share assumptions. Do not use to review a single file, to get quality feedback on ideas, or as a substitute for testing code.
category: judgment-only
write_mode: none
one_line_use: cold model finds the contradictions you smoothed over
fast_pick: "yes"
---

# Contradiction Sweep

Give your session's output to a model that has no stake in it, and ask what conflicts.

**The one claim:** you cannot find contradictions in material you authored, because a contradiction you resolved is not experienced as *smoothed* — it is experienced as *settled*. There is no felt difference between "I considered this and it's fine" and "I never noticed." So the miss is structural, not a matter of care or effort, and no amount of re-reading your own work fixes it. A reader with no commitment to your resolutions has the one advantage that matters.

This is the practical instrument for the excessive-agreement problem: not a second opinion on whether the ideas are good, but a check on whether they can all be true at once.

## When to run it

- **Before a session close** that produced more than two or three durable artifacts.
- **Before any handoff or packet** assembled from documents written in one sitting — those share assumptions that were never stated, so they conflict in ways neither file reveals alone.
- **After a doctrine or planning run**, especially one where rules were written *and* applied in the same session. That combination reliably produces self-application failures: the author writes a rule, then violates it three files later without noticing.
- **When a decision-bearing artifact** will be built on by downstream work.

**Skip it** when the output is a single file, when the work is code whose correctness a test can settle, or when the session was one continuous edit to one thing. The sweep earns its keep on *spread* — several artifacts, one author, one sitting.

## Choosing the reviewer

- **A different model than the author.** This is the whole mechanism. Same model, fresh context is weaker but still useful; same model continuing the same conversation is worthless.
- **Cheapest competent tier.** This is detection work, and detection is the class where cheap and premium models find the same things. Do not spend a premium lane here.
- **One reviewer is usually enough.** For a high-stakes packet, use two from different vendors and read for agreement — vendor diversity beats headcount.

### The Ted-relayed lane, and its real cost

Ted has near-free access to a strong non-Anthropic model at reasoning levels up to very high (noted 2026-07-25). No actor can dispatch it directly; Ted pastes the briefing and pastes the result back.

**That is the strongest available reviewer for this job on the merits** — different vendor entirely, so it shares none of the author's training-shaped habits, and vendor diversity is worth more than headcount. For a dense packet it beats a same-vendor cheap pass.

**But it is not free, and the price is the thing the system is short of.** It spends Ted's attention and puts him back in the wire between actors — precisely the role years of work went into removing (`concept_bridges` #126, #136, #178, #182). Cheap-in-dollars is not cheap-in-Ted.

So: **use the relayed lane when the artifact is decision-bearing enough to justify his involvement, not merely because the tokens cost nothing.** Routine sweeps go to a dispatchable model. If the relayed lane starts getting used for convenience, the free capacity has quietly reintroduced the human relay — and that is a worse trade than paying for a worker.

## Pre-register the prediction

**Before dispatching, write down how many real contradictions you expect.** This is what converts the sweep from a satisfying exercise into a measurement.

Without a number written first, any result gets rationalized: a big list feels like the sweep worked, a small list feels like the work was clean. With a number, the *gap* is the finding. On the first run (2026-07-25) the author predicted 3–4 and the sweep returned about 7 novel items — and the direction of that error, underestimating his own smoothing, was worth more than any single item on the list.

## The briefing

```md
Task: Find contradictions and unacknowledged tensions among these artifacts, all written in a single session.

Files:
- [absolute path]  (all of them, in full)

Do:
1. Read all of them completely.
2. Find places where two assert things that cannot both be acted on, or where following one's rule would violate another's.
3. Find claims stated with more confidence than their own stated evidence supports.
4. Quote both sides with file path and line number.

Do not:
- Propose fixes or resolutions. Naming the tension IS the deliverable.
- Judge whether the underlying ideas are good.
- Edit any file. Strictly read-only.
- Pad the list. A short list of real tensions beats a long list of near-misses.

Return:
Numbered list, hardest first, max 12. Each item: one sentence stating the tension, then quote A with file:line, quote B with file:line.

Success criteria:
Every item traceable to two real quotes. At least one item a reader of only one file could not notice.

Context the reviewer cannot infer: these were authored by one session in conversation with the system's owner. The purpose is to catch what that author smoothed over without noticing — the author cannot do this on his own material, because a contradiction he resolved is experienced as settled. Bias toward reporting a tension you are unsure about over staying silent.
```

**"Do not propose fixes" is load-bearing.** A reviewer that offers resolutions produces a to-do list, and a to-do list invites you to dispose of each item quickly — which is how a real tension gets closed by the same reflex that created it.

## Sorting the returns — the distinction that matters

Two different things come back and they need opposite handling:

- **A defect** — stale text, a factual error, a comment contradicting current behavior, a dead reference. **Fix it.** Leaving a known-wrong line in place because it is "evidence" is precious.
- **A tension** — two live commitments that genuinely conflict, where choosing between them is a real decision. **Preserve it unresolved.** Record it, do not close it.

Getting this backwards ruins the output in both directions: fixing tensions destroys the material a deeper review exists to work on, and preserving defects leaves wrong text in the system.

**When the returns feed a packet for a deeper review, record no preferred resolution.** A visible preference makes the next reviewer anchor on it and hand your own answer back with a second signature — corroboration-shaped and empty.

## What a null result means

Zero novel contradictions is a real outcome, not a failed run. It means either the artifacts genuinely cohere, or the sweep was pointed at too little spread. Say which you think it is. Do not quietly re-run with a bigger file list until something turns up.

## Watch status

- Whether it degrades into ceremony — run on every session regardless of spread, returning near-misses nobody acts on.
- Whether the returns get *resolved* rather than recorded when they were meant to feed a packet — the author's smoothing reflex reasserting itself one layer up.
- Whether pre-registration actually happens, or gets skipped as overhead. Without it there is no measurement, only a feeling.
- Whether a same-model-fresh-context reviewer performs materially worse than a different model — currently assumed, not tested.
