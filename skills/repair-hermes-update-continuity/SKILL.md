---
name: repair-hermes-update-continuity
description: Preserve and recover Hermes session visibility across updates. Use when Ted asks whether a Hermes update is safe or available, sessions or profiles appear empty after an update/restart, Hermes Desktop cannot start after the backend updates, the desktop and CLI disagree about versions or sessions, or a repair risks modifying state.db. Distinguish real data loss from client cache/filter, profile attribution, runtime-home, and desktop/backend version-skew failures before changing session data.
metadata:
  category: meta
  write_mode: file
  one_line_use: preserve and prove Hermes sessions before and after updates
  fast_pick: "no"
---

# Repair Hermes Update Continuity

Protect the session record first, then repair the consumer that stopped showing it.

## Boundary

- Treat the live Hermes home and `state.db` as authority; prove the running process path before choosing a home.
- Do not retag, merge, delete, restore, or rewrite sessions until read-only database evidence proves the data itself is wrong.
- Do not copy a live SQLite database as a backup. Use SQLite online backup.
- Do not expose session titles, message bodies, credentials, or provider keys in receipts.
- Preserve unrelated local modifications in the Hermes checkout.

## Before an update

1. Prove the live home from running Hermes process paths. Use `/Users/ted/.hermes` only when live evidence confirms it.
2. Run the bundled read-only snapshot:

   ```bash
   python3 scripts/hermes_update_continuity.py --snapshot /tmp/hermes-before.json
   ```

3. Require `quick_check=ok`; record total sessions, archived count, null-profile count, and per-profile counts.
4. If the update is about to mutate the runtime, create an online backup:

   ```bash
   sqlite3 /Users/ted/.hermes/state.db ".backup '/explicit/backup/path/state.db'"
   ```

5. Record the CLI version, desktop build stamp, installed app version, live home, and currently running app/backend commands.
6. Run the update only when authorized. An inquiry about whether an update exists is not authorization to install it.

## After an update or apparent session loss

1. Re-run the snapshot and compare it with the pre-update file:

   ```bash
   python3 scripts/hermes_update_continuity.py \
     --compare /tmp/hermes-before.json \
     --snapshot /tmp/hermes-after.json
   ```

2. Classify before repairing:

   - **Database intact, UI sparse/empty:** restart the desktop; inspect profile/filter/cache state. Do not rewrite sessions.
   - **Profiles missing but total rows intact:** check `profile_name` distribution and live-home selection before any retagging.
   - **Desktop startup 404 mentioning headless `hermes serve`:** suspect desktop/backend version skew. Rebuild with Hermes's supported desktop command, client-test the build, preserve the old app bundle, then replace it.
   - **Different live home or multiple gateways:** follow `_shared/Hermes_Runtime_Map.md`; reconcile launchers only after proving which home owns the current data.
   - **Physical row count dropped or `quick_check` failed:** stop. Preserve current files and WAL, compare the online backup, and escalate as a data-recovery incident.

3. For desktop/backend skew, use the supported build path:

   ```bash
   hermes desktop --build-only --force-build
   ```

   Launch the built bundle before replacing `/Applications/Hermes.app`. Verify existing sessions, profile list, and `Gateway ready`. Keep a dated rollback bundle.

4. Verify both surfaces independently:

   - Desktop app: existing sessions visible, expected profile counts, gateway ready, no fatal renderer/API error.
   - Browser dashboard: exact intended port returns HTML/HTTP 200.
   - CLI/database: version and read-only snapshot still match the post-update state.

## Done standard

Report:

- live Hermes home and versions;
- pre/post total and per-profile session counts without titles;
- whether the incident was data loss, visibility/cache drift, home drift, or version skew;
- backup and rollback paths;
- desktop and browser-visible proof;
- any remaining non-fatal warnings.

An HTTP 200 alone is insufficient. A restart alone is insufficient. The session corpus and the client that Ted uses must both be proven.

## Runtime notes

- Codex/Claude Code: run the bundled script and inspect local process/app paths.
- Hermes: run the same read-only script through terminal access; do not self-modify `state.db` based only on sidebar appearance.
- ChatGPT roles without filesystem access: route a bounded repair request naming this skill and require the returned pre/post evidence.
