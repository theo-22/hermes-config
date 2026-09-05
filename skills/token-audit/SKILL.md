---
name: token-audit
description: Measure what a session costs before Ted types a word — preload tokens, the editable surface largest-first, and the turn multiplier — and compare against the saved baseline. Use when sessions feel expensive, after adding skills or MCP servers, or on the weekly re-check. Not for deciding what to cut; that's a judgment call after the numbers land.
---

# Token audit

The measurement is a script. Do not re-derive it in prose — that is the exact
habit this skill exists to remove.

## Run it

```bash
python3 /Volumes/Extra/Substrate/Operations/scripts/token_audit.py --days 7
```

- `--days N` widens the window (default 7)
- `--save-baseline` writes current numbers to `~/.claude/token_audit_baseline.json`
- `--json` for machine-readable output

Every subsequent run prints the delta against that baseline automatically.

## Measure it over time

```bash
python3 /Volumes/Extra/Substrate/Operations/scripts/token_audit.py --trend --days 30
```

Two series, and they are not the same kind of thing:

**Usage is backfilled.** Turns, output, cache read and cold-start preload all
live in the transcripts already on disk, so `--trend` shows real history from
day one, including days before this script existed.

**Config composition is not recoverable.** How big the skill listing was, how
many MCP tools loaded - none of that leaves a trace in a transcript. It only
accrues from snapshots taken forward:

```bash
python3 .../token_audit.py --record        # append a config snapshot
```

A launchd agent `ai.ted.token-audit` runs `--record` daily at 23:50
(`~/Library/LaunchAgents/ai.ted.token-audit.plist`, logs in
`~/Library/Logs/TokenAudit/`). It is deliberately NOT a Hermes job: Hermes
resolves scripts under the profile directory, which is what produced the
82-script fork in work item #1574. This one runs the Operations copy directly,
so there is only ever one implementation.

Check it is alive: `launchctl list | grep token-audit`

### Reading the trend

- **Cold-start preload climbing** is context creep - a skill, an MCP server, or
  a CLAUDE.md line got added. Compare the recorded config snapshots to see which.
- **out/turn climbing** means responses are getting longer; check whether the
  be-concise rule in `~/.claude/CLAUDE.md` is still there.
- **cache read** is the real bill. It is preload x turns plus accumulated
  context, so it moves when either does.
- Days bucket by transcript **mtime**, not session start. A day when many old
  transcripts were touched reads high. Trust the trend, not one row.

## Reading the output

**Preload** is the only number that is not an estimate — it comes from the API's
own usage accounting on the session's first request (input + cache creation +
cache read). Everything under "editable surface" is a chars/4 estimate: ~5% off
in absolute terms, but consistent run to run, so the deltas are real.

**The multiplier is the finding, not the preload.** Preload is not paid once per
session; it is re-read on every turn. At current volume, 1,000 tokens of preload
costs ~15M tokens a week. That is why a skill description matters more than it
sounds, and why a 30-line CLAUDE.md is already fine while an 87-skill listing is
not.

## What to do with the numbers

Only after the audit runs, and only as a proposal to Ted:

- **Skill listing** is usually the largest editable item. Trim descriptions to a
  tight trigger sentence; keep the fire / don't-fire semantics or skills stop
  firing when they should.
- **MCP tool names** — a server used in <5% of sessions costs its full preload in
  100% of them. Enable on demand rather than deleting; deleting removes reach.
- **CLAUDE.md / MEMORY.md** are usually already small. Check before assuming.

## Gotchas

- A server removed from config still appears in the audit until Claude Code
  restarts — the running process holds the old tool list.
- Desktop-app connectors (UUID-named servers) are not in any config file. They
  are toggled in the app, so the script can measure them but not change them.
- The script reads `~/.claude/projects/-Users-ted/`. Other workspaces need the
  `PROJ` path changed.

## Related

Baseline narrative and the first run's findings:
`Operations/reports/Token_Preload_Baseline.md`,
`Operations/reports/Token_Habit_Card.md`,
`Operations/reports/Token_Preload_Connector_Steps.md`.
