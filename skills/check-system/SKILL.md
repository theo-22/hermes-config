---
name: check-system
description: Quick database pulse check — system stats, signal clusters, pending work items, and concept bridge status. Use on demand before coordination decisions, after database-affecting work, or any time you need a fast read of operational state. Replaces reading scattered markdown status files.
category: database-integrated
write_mode: none
one_line_use: read the system pulse
fast_pick: "yes"
---

# Check System

Get a fast, structured read of system operational state from the database.

## System Pulse

!`curl -s http://localhost:5555/api/system/stats 2>/dev/null | python3 -c "
import sys,json
d = json.load(sys.stdin)
print(f'Signal evidence: {d.get(\"signal_evidence_units\", \"?\")}')
print(f'Concept bridges: {d.get(\"concept_bridges\", \"?\")} ({d.get(\"bridges_in_learning\", \"?\")} in learning)')
print(f'Pending work items: {d.get(\"pending_work_items\", \"?\")}')
print(f'Total events: {d.get(\"total_events\", \"?\")}')
" 2>/dev/null || echo "(backend not responding — check if app.py is running on :5555)"`

## Signal Clusters (elevation threshold: 3+)

!`curl -s "http://localhost:5555/api/signal-evidence/clusters?min_count=3" 2>/dev/null | python3 -c "
import sys,json
clusters = json.load(sys.stdin)
if not clusters: print('  No clusters above threshold')
for c in clusters: print(f'  {c[\"tag\"]}: {c[\"count\"]} units')
" 2>/dev/null || echo "(backend not responding)"`

## Pending Work Items by Surface

!`curl -s "http://localhost:5555/api/work-items?state=pending" 2>/dev/null | python3 -c "
import sys,json
from collections import Counter
items = json.load(sys.stdin)
by_source = Counter(i.get('source_surface','unknown') for i in items)
for src, n in by_source.most_common(): print(f'  {src}: {n} pending')
print(f'  Total: {len(items)} pending')
" 2>/dev/null || echo "(backend not responding)"`

## Memory Watcher Cases

!`curl -s "http://localhost:5555/api/memory/recurrence?limit=10" 2>/dev/null | python3 -c "
import sys,json
d = json.load(sys.stdin)
cases = d.get('cases', [])
open_status = {'active', 'monitoring', 'repair', 'escalated'}
open_cases = [c for c in cases if c.get('status') in open_status]
if not open_cases:
    print('  No unresolved watcher cases')
for c in open_cases:
    key = c.get('case_key', '?')
    outcome = c.get('conversion_outcome') or 'none-yet'
    status = c.get('status') or 'active'
    count = c.get('event_count', '?')
    action = c.get('default_next_action') or c.get('recommended_action') or ''
    print(f'  {key}: {count} events, status={status}, outcome={outcome}')
    if action:
        print(f'    next: {action}')
" 2>/dev/null || echo "(backend not responding)"`

## What to Do With This

After reading the pulse:

1. **Clusters at threshold** — any cluster with 3+ units is an elevation candidate. Propose a synthesis artifact to Ted if one hasn't been created yet.

2. **Pending work items** — check if any are stale, blocked, or need routing. Use `setWorkItemState` to update.

3. **Memory watcher cases** — cases in `active`, `monitoring`, `repair`, or `escalated` status are not closure. Route them toward repair, tune, retire, reject, or explicit escalation, then record the outcome.

4. **Concept bridges** — if all are still in `bridge` phase, check whether any have been adopted in practice and should be marked.

5. **Event velocity** — high event count relative to last session means significant system activity occurred.

## When to Use

- Before coordination decisions (to ground recommendations in current state)
- After a batch of writes (to verify the database reflects what was done)
- When Ted asks "where are we?" or "what's pending?"

This is a read-only orientation skill. It does not modify state.

## Update-Surfacing Backstop

This skill embeds live endpoints against `localhost:5555`. If any of them return errors, 404s, or shapes different from what this skill parses (fields renamed, endpoints moved, schema drift):

- Do not silently fall back to narrative or to stale markdown files.
- Check `Control/backend/app.py` for current route names and response fields.
- Check `Operations/CHANGES_LOG.md` for recent backend changes.
- Surface the drift to Ted plainly: which endpoint, what changed, what this skill expects.
- Propose a SKILL.md update in the same turn rather than working around the drift.

Memory-dependent update checking will drift. The check runs on every invocation; structural mismatch is the trigger.
