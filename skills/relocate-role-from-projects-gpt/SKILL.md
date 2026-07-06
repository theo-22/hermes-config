---
name: relocate-role-from-projects-gpt
description: "Move a converted role's doctrine/reference files out of a legacy Projects_GPT/<role>/ directory into the role's own Home directory, and repoint every live reader. Use for the two remaining roles (AI_Monitoring_Digest/Digest, Audit) still reading role-layer files out of Projects_GPT/. Do not use for roles already migrated (Coordinator, Image Factory, System Icons) or for moving production data (case files, inboxes, ledgers) — Audit's move is doctrine-files-only, its live workspace (Runs/, Inbox/, disposition ledger) stays put."
category: temporary
write_mode: file
one_line_use: relocate a role's doctrine files out of Projects_GPT/ and repoint readers
fast_pick: "no"
---

# Relocate a Role Out of `Projects_GPT/`

**Status: temporary, task-scoped.** Written 2026-07-05 after landing 3 of these moves (Coordinator, Image Factory, System Icons) in one session, with 2 left (Digest, Audit — see `Operations/TODO.md` "Move Audit's runtime-authority files out of `Projects_GPT/`"). Retire this skill once both remaining moves land and are verified live — it exists to carry forward what worked and what almost went wrong across those two remaining executions, not as permanent doctrine. If a fourth need to relocate a role ever comes up after Digest+Audit close, re-derive rather than reviving this file from memory — check whether the pattern still matches first.

## Why this exists

`Projects_GPT/<role>/` is a legacy name from when these roles were Custom GPTs. Every already-converted role that still reads its doctrine files from there re-introduces the exact "this is still a GPT" confusion the role-runtime migration is trying to kill. The fix is mechanical once you've done it once: move the doctrine files to the role's own Home directory (the pattern every migrated role already uses for continuity/inbox/workspace), repoint the two or three places in code that hardcode the old path, restart the bridge, verify live.

## When to use

- The role is the target: `AI_Monitoring_Digest` (Digest role, `DIGEST_ROLE_LAYER_FILES` reads 8 files from `Projects_GPT/AI_Monitoring_Digest/`) or `Audit` (`AUDIT_ROOT = HOME / "Projects_GPT" / "Audit"`).
- Not for roles already done: Coordinator, Image Factory, System Icons — moved 2026-07-05, do not re-touch.

## When not to use

- Don't fold Audit's production data (case files under `Runs/`, the cross-actor `Inbox/`, `Working/`, `RUN_LOG.md`, the disposition ledger) into this move. Audit's scope is **doctrine files only** — mirror the other 3's pattern: move `Audit_Role_Runtime_Packet.md`, `Audit_Instructions.md`, `Audit_Doctrine_Kernel.md`, `Audit_Behavior_Overlay.md`, `Audit_Case_File_Template.md`, `Inbox_Convention.md`, plus any mode files under `_guidance/` — leave everything else in `Projects_GPT/Audit/` exactly where it is.
- Don't use this for a role that hasn't been converted to role-runtime yet, or for any move Ted hasn't explicitly routed (this is Canon/`_shared`-adjacent-but-not; it touches live server code other actors depend on).

## Canonical workflow

1. **Enumerate exactly what reads the old path.** Grep `Control/mcp/server.py` and `Control/backend/app.py` for the role's `*_ROLE_LAYER_FILES` list (or equivalent constant) and any `GPT_CONTEXT_FILES[...]` entries pointing at `Projects_GPT/<role>/`. Don't assume the list you're told is complete — the 2026-07-05 session found the prior TODO's claim ("Digest already proves the target pattern") was flat wrong on live inspection; always verify against the actual constant, not a prior summary.
2. **Decide the destination.** The role's existing Home directory, matching whatever subfolder shape its other role-runtime files already use (e.g. `~/Coordinator/`, `~/Image_Factory/`; System Icons got a new `~/IconSystem/Reference/` since no reference subfolder existed yet). If the role's Home lacks an obvious doctrine home, create one narrow subfolder — don't scatter files at the Home root.
3. **Copy, don't move-then-fix.** Copy files to the new location first, leave the old ones in place until the code repoint is verified working, then remove the old copies. Never edit-in-place across two locations simultaneously.
4. **Repoint every reader in the same pass.** Update the `*_ROLE_LAYER_FILES` list, matching `GPT_CONTEXT_FILES[...]` entries, and any hardcoded path constants (e.g. `ICON_SYSTEM_STATE_PATH`) or docstrings referencing the old location. Grep again after editing to confirm zero remaining references to the old path for files you moved (some historical one-off scripts referencing the old path are fine to leave — confirm they're not cron/launchd-scheduled first).
5. **Restart the bridge, verify in-process before declaring done.** `launchctl kickstart -k gui/$UID/com.ted.control.mcp`, confirm new PID, health check, then actually call the role's `_start`/read function in-process (or via a real role session if available) and confirm it resolves the new path with zero errors. In-process verification is real evidence; "the restart succeeded" is not — the 2026-07-05 Homes Manager incident was exactly this gap (fix reproduced/tested in-process, never confirmed from a real ChatGPT session — flag that residual gap explicitly rather than rounding up to "proven").
6. **Log the state_before/state_after/watch shape in CHANGES_LOG** (see the 2026-07-05 entry for Coordinator/Image Factory/System Icons as the template) — files_changed, what moved where, what was deliberately left untouched and why, what's still unverified.
7. **Update `FLEET_TRACKER.md` / `Operations/TODO.md`** to reflect the narrowed remaining scope — don't leave a stale "4 roles pending" line after 3 close.

## Evidence / success criteria

- Grep for the old `Projects_GPT/<role>/` path in `Control/mcp/server.py` and `Control/backend/app.py` returns zero hits for files you moved.
- The role's read function, called in-process against the running (post-restart) server, resolves the new path and returns the expected content with zero errors.
- CHANGES_LOG entry exists naming files_changed, state_before, state_after, and watch items.
- For Audit specifically: `Runs/`, `Inbox/`, `Working/`, `RUN_LOG.md`, and the disposition ledger are confirmed untouched (same paths, same file count) — the move only touched the named doctrine files.

## Failure modes (from the 3 already done)

- **Trusting a prior summary instead of checking the live constant.** The original TODO claimed Digest already had zero `Projects_GPT` dependency; live inspection showed 8 files still read from there. Always re-verify against the actual code before scoping the next move.
- **Leaving stale references half-updated.** Historical one-off scripts (not cron-scheduled) referencing the old path were found and deliberately left as-is rather than churned — that's fine, but it has to be a deliberate, logged decision, not an oversight.
- **Declaring done from an in-process test alone.** In-process verification against the running server is good evidence but is not the same as a real live role session confirming the read-back. Name the gap in the CHANGES_LOG `watch` field rather than rounding up.
- **Conflating doctrine-file relocation with production-data relocation.** Audit's case is the live example: don't let "relocate the role" scope-creep into "relocate the production workspace" — those are different-risk moves requiring a separate explicit decision.

## Update-surfacing backstop

This skill names live file paths (`Control/mcp/server.py`, `Control/backend/app.py`, specific constant names) and a specific remaining-scope list (Digest, Audit). If either remaining move lands, update or retire this skill in the same session — don't let it go stale as a phantom "still 2 to do" pointer after the work is done.
