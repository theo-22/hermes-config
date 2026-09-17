---
name: reconcile-inbox-work-items
description: Classify `_AI_Inbox` packets, link them to authoritative Control `work_items`, close linked intake through terminal work-item transitions, and reconcile lifecycle mismatches. Use when an inbox packet represents actionable work, evidence for existing work, a duplicate/reference/declined item, a stale packet whose real status must be proven, or when completing a work item that has an originating `_AI_Inbox` packet.
metadata:
  category: database-integrated
  write_mode: shared
  one_line_use: classify inbox intake, link authoritative work, close both sides, and prove reconciliation
  fast_pick: "yes"
---

# Reconcile Inbox Work Items

Use the installed lifecycle rather than editing packet status and work-item state separately.

## Authority and boundaries

- Treat `/Users/ted/Control/backend/system.db#work_items` as the one work-status authority.
- Treat `_AI_Inbox` as intake and inspectable source evidence.
- Preserve packets and receipts. Archive reversibly; never delete.
- Do not auto-create a work item for every arrival.
- Do not bulk-classify the legacy backlog. An unclassified packet is migration input, not proof of live work.
- Before terminal closure, map live evidence to every material acceptance clause. Adjacent machinery is not acceptance.

## Classify one packet

Read the complete packet and the candidate work-item rows first. Choose exactly one classification:

- `actionable` — source work; requires at least one work-item link.
- `response` — evidence attached to existing work; requires at least one link and archives immediately.
- `reference` — no work obligation; archives immediately.
- `duplicate` — duplicate/superseded intake; optionally link provenance; archives immediately.
- `declined` — no action will be taken; archives immediately.

Run:

```bash
python3 /Volumes/Extra/Substrate/Operations/scripts/inbox_consumption.py \
  --classify <packet.md> \
  --classification <classification> \
  --work-item <id> \
  --actor <actor> \
  --note "evidence-based disposition"
```

Repeat `--work-item` for N:M provenance. Several packets may link to one item, and one packet may link to several items. An actionable packet linked to several items remains active until all linked items are terminal.

Do not reclassify an already classified packet by hand. The installed API rejects conflicting reclassification; reconcile the prior record explicitly.

## Complete linked work

Use the canonical state endpoint rather than stamping or moving the packet manually:

```bash
curl -s -X POST http://127.0.0.1:5555/api/work-items/state \
  -H 'Content-Type: application/json' \
  -d '{"item_id":<id>,"state":"acted","actor":"<actor>"}'
```

Terminal states are `acted`, `declined`, and `superseded`. `evaluated` and `deferred` do not close intake.

The terminal operation must:

1. Refuse the work-state change if a linked active packet is missing.
2. Wait if another linked work item remains nonterminal.
3. Stamp classification, work-item ids, consumer, timestamp, and close note.
4. Move the complete packet to a dated `_AI_Inbox/Archived/*_work_items/` folder.
5. Commit the work-item state and packet lifecycle together, rolling ordinary failures back.

## Reconcile and verify

Run:

```bash
python3 /Volumes/Extra/Substrate/Operations/scripts/inbox_consumption.py --reconcile
```

Read `/Volumes/Extra/Substrate/Operations/reports/Inbox_Work_Item_Reconciliation_LATEST.md`. It reports:

- unclassified active packets;
- actionable packets without links;
- terminal work with an unconsumed packet;
- consumed actionable packets with open work;
- missing packet files.

For one completed item, prove all of these before reporting closure:

```bash
curl -s 'http://127.0.0.1:5555/api/work-items' | jq '.[] | select(.id == <id>)'
sqlite3 -json /Users/ted/Control/backend/system.db \
  'select p.*, l.work_item_id, l.relationship from inbox_packets p join inbox_work_item_links l using(packet_id) where l.work_item_id=<id>;'
curl -s 'http://127.0.0.1:5555/api/inbox-work-items/exceptions' | \
  jq '[.exceptions[] | select(.work_item_ids | index(<id>))]'
```

Require: terminal DB state, archived source path present, frontmatter receipt preserved, original packet body preserved, and zero exceptions for the item.

## Closeout

- Record the exact source-packet disposition and acceptance proof on the owning receipt/continuity surface.
- Keep unrelated legacy reconciliation findings separate from the completed item.
- Release all task and file claims.
- Report `Source item: completed and removed` only when it left the active inbox and remains recoverable in archive.
