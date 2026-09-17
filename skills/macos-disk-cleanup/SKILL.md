---
name: macos-disk-cleanup
description: Audit and reclaim disk space on a local Mac while distinguishing safe disposable data from active, personal, snapshot-retained, or system-protected material. Use for low-space investigations, cleanup requests, stale installer removal, or verification that a deletion produced real headroom.
metadata:
  category: judgment-only
  write_mode: file
  one_line_use: safely audit and reclaim local macOS disk space with snapshot-aware proof
  fast_pick: "no"
  version: 1.0.0
  platforms: [macos]
  tags: [disk, storage, cleanup, apfs, time-machine]
---

# macOS Disk Cleanup

Safely turn a low-space report into an evidence-backed cleanup whose live effect and remaining uncertainty are explicit.

## When to Use

Use this skill when the user wants to:

- understand what is consuming a Mac's internal disk;
- identify easy or low-risk cleanup candidates;
- remove selected caches, logs, duplicate installers, or obsolete update material;
- distinguish live files from APFS or Time Machine snapshot retention;
- verify whether prior cleanup created physical headroom.

## When Not to Use

Do not use this skill to:

- clean Windows, Linux, network storage, or cloud accounts;
- delete personal documents, archives, application state, or backups without specific evidence and authorization;
- thin Time Machine snapshots merely to make a free-space number rise;
- disable System Integrity Protection, clear immutable flags, or weaken another macOS protection for negligible recovery;
- treat a cache as disposable while its application or runtime is actively using it.

## Authority and Scope

Start from the exact disk, folder, handoff, or concern the user named. A read-only audit authorizes inspection, not deletion. Approval for an "easy" batch covers only the candidates presented as that batch; system-owned installer data, snapshots, active application caches, and archive candidates remain separate decisions unless explicitly included.

Before mutation, make the selection concrete: exact paths, allocated size, why each is disposable, active-consumer result, expected recovery, and recovery route. Recheck those facts immediately before deletion.

## Canonical Workflow

### 1. Establish current physical state

Record the internal APFS container size and free space, volume consumption, swap use, and local snapshots. On macOS, useful read-only sources include:

```sh
diskutil info /
diskutil apfs list
sysctl vm.swapusage
tmutil status
tmutil listlocalsnapshots /
diskutil apfs listSnapshots <data-volume-device>
```

Confirm whether a current external Time Machine backup exists when recoverability matters. Do not equate a local snapshot with an independent backup.

### 2. Measure without double-counting

Use targeted paths rather than a broad filesystem crawl when possible. Compare allocated and apparent sizes for suspicious trees; sparse files, clones, firmlinks, and APFS sharing can make ordinary totals misleading.

```sh
du -sk <path>       # allocated blocks
du -Ak <path>       # apparent bytes expressed in KiB
```

Treat `du` totals on Preboot, Data firmlinks, clones, and sparse files as leads until reconciled with `diskutil`'s physical-container view. Do not add overlapping directory totals together.

### 3. Classify candidates by risk

Use these behavioral classes rather than assuming everything large is removable:

- **Low-risk disposable:** closed rotated logs, exact duplicate cached installers, old application download caches with no active consumer, package-manager cleanup, and already-discarded cache/runtime material in Trash.
- **Archive or cold-launch candidate:** inactive application support, old profiles, state backups, and user history whose continuing value is uncertain. Prefer relocation to a spacious volume plus a cold-launch check.
- **System-aware candidate:** obsolete `macOS Install Data`, update bundles, and local snapshots. Verify host version, bundle version, active update services, open handles, and protection flags before recommending action.
- **Poor target:** swap, live runtime data, active browser/model caches, current application state, system temporary files, and anything that will immediately regenerate without fixing the underlying pressure.
- **Personal or ambiguous:** documents, images, handoffs, calendar files, project archives, and unfamiliar Trash contents. Preserve unless the user selects them.

For each meaningful candidate, report allocated size, not just apparent size.

### 4. Prove the candidate is inactive

Check both process state and open files. A quit application is useful evidence, but it is not enough when helpers or update services may persist.

```sh
pgrep -ifl '<application-or-service>'
lsof -nP | rg '<exact escaped path>'
```

Avoid expensive recursive open-file scans over the whole disk. If a generic macOS service is running but has no handle on the target, say both facts rather than calling the service absent.

### 5. Handle stale macOS installers correctly

Do not infer the host machine from one model string inside an update bundle. Apple update assets can support many models.

Before removing obsolete installer data:

1. Read the live model with `system_profiler SPHardwareDataType` and the live OS with `sw_vers`.
2. Read the bundle's `Info.plist` or equivalent metadata for its OS version, build, supported devices, and update behavior.
3. Compare the live OS to the bundle; prove the bundle is obsolete for the current system.
4. Confirm no process holds the exact payload path open.
5. Record allocated size and current free space.
6. Obtain explicit authorization for the system-owned target.

Delete only the obsolete payload the evidence supports. If macOS leaves a tiny `restricted`, `rootless`, immutable, or boot-label wrapper, verify its size and leave it. Do not disable system protection to erase a negligible placeholder.

### 6. Execute the authorized batch narrowly

- Resolve every exact target again and refuse unexpected symlinks.
- Avoid unresolved variables, broad globs, home-directory recursion, filesystem-root recursion, and combined targets that are hard to audit.
- Prefer recoverable relocation for ambiguous/archive candidates — but check the destination: a payload archived *inside* a git repo can be auto-committed by its drift watcher and then block every future push, because GitHub rejects files over 100 MB. Confirm the archive tree is gitignored before relocating into it.
- If that already happened, unwinding is safe only while the offending commit is unpushed: `git log origin/main..main` to confirm, `git reset --soft HEAD~1`, unstage and gitignore the payload subtrees, re-commit the receipt alone, push. Never rewrite pushed history for this.
- Permanent deletion is appropriate only for the exact pre-audited disposable material the user authorized.
- Keep personal Trash items outside the selected set.
- For a root-owned target, request administrator authorization for one exact operation. If the operation fails before mutation, prove the target is unchanged before retrying.
- Never convert a failed safe command into a broader destructive command.

### 7. Verify live outcome

Verification is part of the cleanup:

1. Prove each exact selected target is absent or reduced to the explicitly retained protected wrapper.
2. Prove nearby active application and user-data paths still exist.
3. Recheck relevant processes and open handles.
4. Re-read APFS physical free space and snapshot count.
5. If free space does not rise—or moves in the opposite direction—report the observation without claiming the cleanup failed or succeeded physically. Check snapshot retention, swap, current downloads, backups, and concurrent writes.
6. Distinguish:
   - **logical removal:** the live directory entry and current-file reference are gone;
   - **physical recovery:** the APFS container reports more free blocks;
   - **reclaimable retention:** older snapshots still own deleted blocks and macOS may prune them under pressure.

Take more than one free-space reading when the value is volatile. Do not manufacture a clean before/after number by thinning snapshots unless the user separately authorizes that action.

## Done Standard

A cleanup is complete only when the record states:

- exact paths selected and what was preserved;
- allocated size logically removed;
- active-consumer and symlink checks;
- exact post-delete readback;
- current physical free space and snapshot count;
- whether recovery is live, snapshot-retained, or still unexplained;
- any separate candidates deliberately deferred;
- whether deletion is recoverable from Trash, local snapshots, or an external backup.

## Common Failure Modes

- Calling a universal updater "for an old Mac" because one supported-model string names that Mac.
- Reporting `du` apparent totals as physical recovery.
- Emptying all of Trash when only selected cache/runtime trees were authorized.
- Deleting a browser or model cache while the owning application is open.
- Treating swap as ordinary disposable storage.
- Manually thinning snapshots to force the expected number instead of reporting snapshot retention.
- Removing a system-protected 12 KiB wrapper after the multi-gigabyte payload is already gone.
- Claiming reclaimed space from one volatile free-space reading while the system is writing concurrently.
- Archiving multi-gigabyte payload material into a directory inside a git repo with an auto-commit watcher, silently breaking that repo's auto-push on the 100 MB file limit.

## Runtime Notes

### Local filesystem runtimes

Use native macOS commands and exact-path reads. Prefer a visible administrator prompt for the one authorized root-owned operation rather than embedding or soliciting credentials.

### Runtimes without local filesystem access

Provide the canonical audit and verification sequence, but do not claim live proof or deletion. Route execution to a local authorized runtime.

## Update Backstop

Command output, APFS behavior, protection flags, updater layouts, and skill paths can change across macOS releases. Inspect the live command interface and bundle structure rather than assuming the examples above still match. Update this shared skill when a repeated new behavior changes candidate classification, authorization boundaries, or the done standard.
