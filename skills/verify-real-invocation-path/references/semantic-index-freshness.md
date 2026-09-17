# Verify semantic-index freshness

Use when a semantic index, embedding store, or derived search projection claims
to be current after its source changed. This extends the parent verification
skill; it does not authorize rebuilding production data or restarting services.

## Trace the two consumers

Identify the authoritative source, chunk producer, embedding producer, freshness
publisher, refresh trigger, and actual semantic consumer. Trace exact-ID lookup
separately: it may read the live source while semantic discovery reads an old
snapshot. A working exact lookup cannot prove semantic coverage, and a visual
map regeneration cannot prove an unrelated index was rebuilt.

Recent embedding timestamps may only mean old chunks were embedded again. Read
the source and index directly before accepting a timestamp or stored label.

## Required agreement

Use a coherent source snapshot and deterministic ordering. Check:

- Exact live and indexed ID sets, including missing, extra, duplicate and
  malformed identities; equal counts alone are insufficient.
- Matching counts and maximum IDs where the source uses ordered numeric IDs.
- Indexed content matches the source-derived content, not merely its IDs.
- Each active chunk has the active embedding expected by the real consumer's
  provider/model/version contract. A different model's vector is not coverage.
- Recomputed source/content hash matches the registered hash.
- Stored freshness agrees with those facts; a stale or unknown source cannot
  pass just because its chunks happen to match.

Bound mismatch output to counts and small samples. Do not dump private source
text or vectors to demonstrate coverage.

## Transaction and concurrency checks

When repair is separately authorized, inspect the publication sequence:

1. Successful graph/source mutations invalidate freshness atomically with their
   commit. Failed, rolled-back, no-op and idempotent operations must not invent
   a freshness transition. Preserve existing audit and stale-write guards.
2. Keep freshness stale while chunks or embeddings are incomplete. Re-embedding
   old chunks alone must not restore current.
3. Revalidate source identity and coverage before publishing current. Validation
   and publication need an atomic boundary so a concurrent source edit cannot
   have its stale flag overwritten. Keep slow inference outside write locks.
4. Bind a success receipt to the snapshot that attempt processed. If refresh A
   is superseded by refresh B, A must not report its old counts/hash alongside
   successful verification of B's newer index. Report supersession/failure or
   explicitly distinguish attempted and published snapshots.
5. A parent regeneration transaction needs the semantic producer's own result.
   Semantic failure must prevent overall PASS without concealing already
   completed visual/source steps. Ensure claim leases cover the added work.

## Bounded fixture and consumer probes

Use a disposable database and the actual mutation/producer helpers. Mock only
the expensive provider when useful, then add a real provider fixture if it is
authorized and practical. Required negative cases:

- equal counts with wrong IDs; missing or duplicate IDs;
- missing/inactive/wrong-consumer embeddings;
- mismatched source hash or indexed content;
- provider failure after chunk publication;
- graph/source edit during inference;
- overlapping producers where the later attempt completes first;
- failed audit commit, caller rollback, no-op and idempotent replay.

Prove current → committed change → stale → rebuilt and verified current. Test
structured results and exit codes, not just printed success text.

For live acceptance, run the authorized producer, repeat the full consistency
check, and query distinctive language from a previously missing source item
through the real semantic consumer. Verify source identity and returned item,
not just a plausible answer. Also rerun the healthy exact-ID path unchanged.

Keep layers explicit: source/fixture lifecycle proof, real-provider fixture,
live index production, installed daemon, actual client retrieval, and independent
verification. Do not mutate meaningful production records just to manufacture a
live lifecycle specimen. If no live source mutation was performed, say so.

## Verified example and limits

The 2026-08-30 Concept Graph repair found 342 live nodes through #344 but only
236 semantic chunks/embeddings through #238, labeled current. Later embedding
timestamps had hidden the stale chunk snapshot. The repair connected graph
mutation invalidation and verified Map Curator regeneration to the semantic
producer. Independent review caught and helped falsify an overlapping-refresh
receipt inconsistency before acceptance.

Final live proof was 342/342/342 coverage, exact ID/content/hash agreement,
rank-1 semantic retrieval of #344, and unchanged exact-frame delivery. Lifecycle
mutation proof used disposable fixtures; no live graph meaning was changed for
acceptance. These counts and IDs are historical specimens, not future expected
values: recompute against the current source.

Evidence:
- `/Volumes/Extra/Substrate/Operations/reports/CONCEPT_SEMANTIC_FRESHNESS_REPAIR_2026-08-30.md`
- `/Volumes/Extra/Substrate/Operations/reports/CONCEPT_SEMANTIC_FRESHNESS_VERIFY_2026-08-30.md`

Regression owners: `/Users/ted/Control/backend/test_concept_memory_freshness.py`
and `/Users/ted/Control/mcp/test_map_semantic_refresh.py`. Reinspect their current
contracts before copying commands, provider names, database fields or paths.
