# Verify shared skill discovery in Codex

Use when a shared skill exists on disk but is absent from Codex, or when repairing metadata and exposure drift. A valid file and a working link are necessary evidence; fresh runtime discovery establishes that Codex accepts the skill.

## Bound the repair

1. Identify the named canonical skill folders under `/Volumes/Extra/Substrate/Skills/`. Resolve actual paths and repo roots; do not assume a home-directory alias is a separate source.
2. Run `/Volumes/Extra/Substrate/Skills/skills-card-check` before editing. It checks index membership, required shared metadata, and Codex exposure. Read its current accepted values rather than inventing category names from the index's display headings.
3. Check git status and active claims; claim the exact shared files and links before writing. Preserve unrelated edits.
4. Repair only the demonstrated defects. For the 2026-08-30 Icon case, the established operational classification was `category: meta` plus `write_mode: file`; `file-write` was a display concept, not an accepted category. Choose categories from the current schema and comparable skills, not from this example alone.
5. Expose canonical folders with symlinks under the active Codex skills directory. In the verified installation, `/Users/ted/.codex/skills` resolves to `/Volumes/Extra/Substrate/.codex/skills`. Check existing paths before creating links; do not overwrite an unexpected file or fork the skill body into a copy.

## Verify three separate things

- **Catalog:** rerun `skills-card-check`. Record any remaining unrelated failures separately; do not call the full catalog clean if only targeted checks pass.
- **Files and links:** compare before/after contents, prove workflow bodies unchanged for metadata-only repairs, and resolve each exposure link strictly to its expected canonical folder.
- **Codex discovery:** initialize a fresh installed Codex app-server process and request a forced skill reload for the affected working directory. Require every named skill to appear at its canonical path with `enabled: true`; inspect returned errors.

## Fresh app-server probe

Resolve the installed executable with `command -v codex`; inspect `codex app-server --help` if the interface has changed. The proven invocation was `codex app-server --stdio`. Use a temporary subprocess with JSON-lines stdin/stdout and a bounded timeout, not an interactive model turn. No model generation or skill execution is needed.

Send initialization, wait for response id 1, then send the notification and list request:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientInfo":{"name":"skill-discovery-check","version":"1.0"}}}
{"jsonrpc":"2.0","method":"initialized","params":{}}
{"jsonrpc":"2.0","id":2,"method":"skills/list","params":{"cwds":["/absolute/affected/working/directory"],"forceReload":true}}
```

Replace the working-directory placeholder. Match responses by id, allowing intervening notifications. Inspect the result for the requested names, canonical `path`, `enabled`, `scope`, and errors. Keep the saved proof limited to those fields; do not dump configuration, environment, or unrelated catalog contents. Always terminate and reap the subprocess, including on timeout or parse failure. Do not restart the desktop app or shared services to run this check.

If this interface is unavailable, report catalog/link proof as passing and fresh runtime proof as unverified. Do not substitute a successful process start or a grep match for discovery. A fresh app-server result proves its discovery path, not that an already-open conversation refreshed its cached catalog or that the skill's workflow works.

## Validator compatibility and closeout

The two validators enforce complementary requirements. Keep `name` and `description` at the top level and the required `category`, `fast_pick`, `one_line_use`, and `write_mode` under `metadata`; see `/Volumes/Extra/Substrate/Skills/README.md`. On 2026-08-30 the library migrated its legacy top-level extensions into that supported mapping and replaced the shared checker's line-flattening parser with strict YAML parsing. Run both checks on changed skills. Do not delete required metadata or patch the bundled generic validator merely to obtain a green result.

Review the diff, record the proof, commit scoped changes in their owning repos, and release claims. Verify push separately: the Icon repair's Skills commit pushed, while the Codex links were committed locally because that repo had no remote. Never invent a remote or claim local commits are pushed.

## Verified instance

2026-08-30: `icon-image-processor` and `icon-apply-sort` produced exactly two invalid-category and two missing-link failures. Two category replacements and two canonical symlinks cleared the full shared checker. Fresh Codex `skills/list` returned both enabled at canonical paths with zero errors. Workflow bodies remained unchanged; no image processing or Finder apply ran. Skills commit `383d74c`, local Codex exposure commit `1c9324d`, Operations closeout commit `0d32e4eb0`.
