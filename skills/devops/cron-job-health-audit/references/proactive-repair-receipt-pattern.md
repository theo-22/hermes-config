# Hermes Proactive Repair Receipt Pattern

## What It Is

A receipt-style check that scans specific surfaces for degradation and records findings with actionable classification. Runs periodically (weekly or after triggers).

## Shape

```
# Hermes Proactive Repair — YYYY-MM-DD HH:MM TZ

**Status:** ok | attention
**Fixed:** N
**Flagged:** N

## Needs Attention
- [Surface type]: [specific path or job name] — [what's wrong, quantified]

## Verified Clean
- [surfaces that passed check]

## Not Changed
- [scope guard: what was explicitly NOT modified]
```

## Rules for Writing the Receipt

1. **Cite specific paths** — not generic names like "Outbound.md". Which file, in which directory.
2. **Verify against live state before flagging** — check the actual current state, not a cached impression. A cron job flagged "error" must have a current error, not a stale last-run impression.
3. **Apply documented thresholds** — stale thresholds are defined in NEXT_ACTION.md or equivalent. Don't flag without checking against the threshold.
4. **Age claims must match real stat times** — compute from `stat -f %Sm` or equivalent, not from memory.
5. **"Intentionally Not Changed" section required** — document scope boundaries so future readers know the receipt was observation-only.

## Pitfalls

- **Don't flag generic categories without specific targets.** "Outbound.md" with no path leaves the reader guessing which handoff is stale. Each flag must resolve to one file path.
- **Don't flag cron errors without checking current status first.** The cron health receipt (`cron_health_receipt`) runs frequently and records `last=ok`. If the receipt shows ok, the flag is stale — correct it in the same receipt rather than letting the false flag persist.
- **False positives compound.** A 67% false-positive rate (2/3 wrong) undermines trust in the entire receipt. When false positives are found, document what went wrong so the next run improves.

## Related

See `cron_health_receipt` pattern in `cron-job-health-audit` skill for the companion cron-health receipt format. Both share the observation-only, receipt-first philosophy.
