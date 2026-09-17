# Duplicate registration → concurrent double-append (2026-08-08)

Full repair recipe for the two-agent-copies-of-same-job variant of Gotcha 9.

## Incident

`pieces-digest-router` was registered in TWO profile registries, both enabled,
both scheduled `30 7 * * *`:

| Registry | Job ID | Enabled |
|---|---|---|
| `/Users/ted/.hermes/cron/jobs.json` (default) | `9730ec605cf2` | True |
| `/Users/ted/.hermes/profiles/substrate-hermes/cron/jobs.json` | `5f6579fdedf4` | True |

Both fired at 07:30 and both ran the same prompt against the same digest
(`pieces_continuity_2026-08-08.md`), appending the same window to:

- `/Volumes/Extra/Substrate/Hermes/Working/pieces_copilot_summaries.md`
- `/Volumes/Extra/Substrate/Hermes/Working/pieces_decisions_log.md`

Net effect: each file ended up with TWO `## 2026-08-08` sections, one from each
run. The second writer's section was MORE accurate (it had read the 08-08 Codex
return in `_AI_Inbox` and routed the stop-hook to `work_items #322`; the first
writer had routed it to an older 08-07 item). Keeping the more accurate pass
mattered — the dedup was not symmetric.

## Detection (in the moment)

When appending to an append-only routing log, ALWAYS check for prior processing
of the same window FIRST. The tell was subtle: `tail` after my append showed
content I didn't write, with a second `## 2026-08-08` header below mine.

```bash
grep -n "^## 2026-08-08" <routing-log>.md          # two headers = double-fire
grep -n "^## 2026-08-08" pieces_copilot_summaries.md
grep -n "^## 2026-08-08" pieces_decisions_log.md
```

Then confirm the registration cause:

```bash
python3 -c "
import json
for p in ['/Users/ted/.hermes/cron/jobs.json',
          '/Users/ted/.hermes/profiles/substrate-hermes/cron/jobs.json']:
    d = json.load(open(p))
    jobs = d if isinstance(d, list) else d.get('jobs', d)
    if isinstance(jobs, dict): jobs = list(jobs.values())
    for j in jobs:
        if 'pieces-digest-router' in j.get('name',''):
            print(p, '->', j.get('id'), 'enabled:', j.get('enabled'))
"
```

## Dedup procedure (when keeping the MORE accurate pass)

1. Compare the two sections. The second-writer pass is usually more accurate
   because it ran later and had seen newer inbox items (Codex returns, alerts).
2. Remove the less accurate section wholesale (patch tool, replace the whole
   block including its trailing `---` separator).
3. Preserve ANY unique items from the removed section by merging them into the
   surviving section — do not lose content in the name of dedup:
   - summaries: add missing bullets to the surviving bullet list
   - decisions log: add missing table rows to the surviving table
4. If the merge leaves a duplicated table header (my first merge created a
   second `### Decisions captured…` + header row), collapse it back into ONE
   table: patch the separator so the merged row sits directly above the
   surviving first row.
5. Verify: `grep -c "^## 2026-08-08"` == 1 per file; `tail -3` reads clean.

## Append workaround (terminal guard)

The terminal tool rejects heredoc appends whose content contains `&` (it parses
`&` as shell backgrounding):

```
Foreground command uses '&' backgrounding.
```

Fix: append via `python3 -c` with a triple-quoted string instead of `cat >>`:

```bash
python3 -c "
entry = '''...content with & and markdown...'''
with open('/path/to/file.md', 'a') as f:
    f.write(entry)
"
```

## Routing discipline lesson (re-filing risk)

This double-fire is the same failure mode that got `pieces-digest-router`
flagged on 2026-07-21 for re-filing resolved items: each independent run routes
the same findings with zero check against what the other run already filed.
When a routing log shows a duplicate section, treat the WHOLE window as already
processed — do NOT file inbox items for it again. The correct behavior when a
duplicate is found: keep the best section, ensure no inbox item was created
twice, and surface the two job ids to Ted.

## Status after this incident

- Files deduped to single accurate sections (2026-08-08).
- 0 inbox items created (all candidates already had prior surfaces).
- Fix (disable one registration) left as TED'S CALL because both profiles
  legitimately own the job name; surfaced ids `9730ec605cf2` vs `5f6579fdedf4`.
