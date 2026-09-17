# Hermes Operator Integration — Room Verification Pattern

## Context

The Hermes_Operator Integration room is a Project Room that the meta-agent sweep may flag as "stale." This pattern proves whether a flagged room is genuinely stale or actively maintained with evidence outside the standard mtime check.

## When to Use

- The meta-agent sweep flags a room as "stale" or "worth a quick look"
- The room contains many document types with different update cadences
- The room's `CURRENT_STATE.md` dates may be old but content is still meaningful
- Need to distinguish "neglected" from "actively maintained with varied cadence"

## Verification Checklist

Check ALL of these before declaring a room stale:

| # | Check | What it proves |
|---|-------|----------------|
| 1 | **Documents modified in last 30d** — `find . -name "*.md" -mtime -30` | Active editing, not just old files |
| 2 | **Records directory health** — count records, check date range | The room's evidence base is current |
| 3 | **Daily receipt freshness** — for each daily receipt type, check the most recent one | The room's automated monitoring is running |
| 4 | **Thread status** — check if open threads need human input vs are neglected | Distinguish "waiting on Ted" from "abandoned" |
| 5 | **Proactive repair accuracy** — run a dry-run against last receipt's flags | The room's self-check mechanism is working |
| 6 | **CURRENT_STATE.md `Card checked:` date** — compare to today | The last human-verified date |

## Scoring

- **5-6 checks pass:** Room is actively maintained. "Stale" flag is a FALSE POSITIVE. Clear it or note why the flag is wrong.
- **3-4 checks pass:** Room has gaps but isn't neglected. Flag specific items for Ted, don't lifecycle-change.
- **0-2 checks pass:** Room is genuinely stale. Escalate with evidence.

## Pitfalls

- **Don't equate "12 days old" with "stale."** Rooms with daily automated receipts (cron health, proactive repair) and periodic manual reviews (Ted's thread input) have a maintenance cadence that isn't captured by a single date field.
- **Don't ignore thread state.** A thread that's "unanswered" because it needs Ted's specific judgment is not a neglect signal — it's a routing signal.
- **Don't skip the dry-run.** Running a dry-run against the last proactive repair's flags proves (or disproves) the room's self-monitoring accuracy. This is the strongest single check.

## Output

Produce a REVERIFY_YYYY-MM-DD.md in `Hermes_Records/` with:
- Each check, its result, and the evidence source
- Overall verdict: false positive / confirmed stale / partial
- Recommended action per finding
