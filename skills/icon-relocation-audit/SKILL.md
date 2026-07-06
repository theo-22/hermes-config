---
name: icon-relocation-audit
description: >
  When a root has been relocated from /Users/ted to /Volumes/Extra/Substrate,
  audit all icon family apply scripts for stale single-path entries and update
  them to target both the ~/ symlink/alias surface and the Extra real path.
trigger: >
  Ted says "icons need relocation audit," a new root has been relocated to
  Extra, or Icon System hands off a relocation-aware request.
category: meta
write_mode: file
one_line_use: audit icon families for relocated roots, update apply scripts for dual-path
fast_pick: "no"
---

# Icon Relocation Audit

When a root directory is relocated from `/Users/ted/` to `/Volumes/Extra/Substrate/`, any icon family that maps that root still points only at the `~/` path. This skill audits all families and updates scripts to apply icons to BOTH the `~/` symlink/alias surface and the Extra real target.

## When to use

- Ted says "icons need updating for the relocation"
- A specific root was moved (e.g. `Learning_System`, `Commands`) and icon scripts were not updated
- Icon System routes a relocation audit request to you

## When not to use

- Just adding a new icon to an existing family — use the family's normal apply script
- Bulk icon redesign or family creation — that's Icon System's domain

## Core doctrine

- **Check, don't assume.** A path at `/Volumes/Extra/Substrate/` is not automatically a relocation of the `~/` version. Verify with `file /Users/ted/<Root>` — if it's a symlink to Extra, it's relocated. If both are real directories with different contents, they are NOT the same root and don't get dual-path.
- **Project Rooms stay.** `/Users/ted/Projects/` remains authoritative until explicit cutover per migration docs. Do not remap.
- **Runtime/authority roots stay.** Operations, Control, Canon are not relocated — they're separate copies at Extra for backup/Substrate use.
- **Backup before edit.** Every apply script you modify gets a `.bak.YYYY-MM-DD` copy.
- **Dry-run before apply.** Run the family script in dry-run mode first to verify no unexpected missing sources/targets.
- **Write a receipt.** Return an audit receipt to `_AI_Inbox` addressed to Icon System / Ted.

## Audit workflow

### 1. Inventory relocated roots

Find which `~/` paths are symlinks to Extra:

```bash
find /Users/ted -maxdepth 1 -type l | while read f; do
  target=$(readlink "$f")
  echo "$f -> $target"
done | grep "/Volumes/Extra"
```

Also check Extra to find roots that might have both surfaces without being symlinks:

```bash
ls -d /Volumes/Extra/Substrate/*/ | while read d; do
  name=$(basename "$d")
  tedpath="/Users/ted/$name"
  if [ -L "$tedpath" ]; then
    echo "SYMLINK  ~/$name -> $(readlink "$tedpath")"
  elif [ -d "$tedpath" ] && [ ! -L "$tedpath" ]; then
    echo "REAL DIR ~/$name (separate from Extra) — NOT a relocation"
  fi
done
```

### 2. Check all icon families for stale paths

```bash
for f in /Users/ted/IconSystem/Icon_Families/*/apply_family_icons.zsh; do
  family=$(basename "$(dirname "$f")")
  echo "=== $family ==="
  grep -n '/Users/ted/Commands\|/Users/ted/Homes_Manager\|/Users/ted/Learning_System\|/Users/ted/Transition' "$f" 2>/dev/null || echo "  (no stale paths)"
done
```

Search for the actual relocated roots (Commands, Homes_Manager, Learning_System, Transition, or whatever was just moved).

### 3. Check Dock_Family command script (already dual-path)

`Dock_Family/apply_command_icons.zsh` was already updated with `$REAL_CMD_ROOT`/`$ALIAS_CMD_ROOT` variables. It auto-discovers icons and targets both paths. No manual update needed for new command file icons. Verify the variables point correctly:

```
REAL_CMD_ROOT="/Volumes/Extra/Substrate/Commands"
ALIAS_CMD_ROOT="/Users/ted/Commands"
```

### 4. Update Metallic_Glow or other families

Each family script maps icon PNGs to targets via `add()` calls. For relocated roots, replace `add` with `dual_add`:

```bash
# Add EXTRA_TARGET_BY_KEY to the typeset line at the top of the script:
#   typeset -A TARGET_BY_KEY ICON_BY_KEY EXTRA_TARGET_BY_KEY

# Add the dual_add helper function after the add() definition:
# dual_add() {
#   local key="$1" icon="$2" alias_path="$3" real_path="$4"
#   ICON_BY_KEY[$key]="$SCRIPT_DIR/$icon"
#   TARGET_BY_KEY[$key]="$alias_path"
#   EXTRA_TARGET_BY_KEY[$key]="$real_path"
# }

# Update the apply loop to handle extra_target:
#   extra_target="${EXTRA_TARGET_BY_KEY[$key]:-}"
#   ... then check and apply to both targets
```

### 5. Backup

```bash
cp /Users/ted/IconSystem/Icon_Families/<Family>/apply_family_icons.zsh \
   /Users/ted/IconSystem/Icon_Families/<Family>/apply_family_icons.zsh.bak.$(date +%Y-%m-%d)
```

### 6. Dry-run

```bash
zsh /Users/ted/IconSystem/Icon_Families/<Family>/apply_family_icons.zsh
```

(Default mode is dry-run. Use `--dry-run` explicitly if supported, otherwise no-args is dry-run.)

### 7. Apply

```bash
zsh /Users/ted/IconSystem/Icon_Families/<Family>/apply_family_icons.zsh --apply
```

### 8. Write receipt to _AI_Inbox

Include: files inspected, files changed, backups, dry-run results, apply results, roots intentionally left unchanged with reasons.

## Families reference

| Family | Targets | Has relocated roots? | Notes |
|--------|---------|---------------------|-------|
| Dock_Family | `.command` files in Commands/Workspace | ✅ Already dual-path (Icon System) | Auto-discovers icons, targets both real and alias |
| Metallic_Glow_Family | Top-level `~/` folders + some nested | ⚠️ Update `add()` → `dual_add()` for each relocated root | Handles Commands, Homes_Manager, Learning_System |
| Project_Rooms_Industrial_Family | `/Users/ted/Projects/<Room>/` | ❌ Not relocated — leave as-is per migration docs | Project Rooms stay ~/ authority |
| Gold_Family | Single .command file | Check manually | Rarely touched |
| IconSystem_Family | Icon system directories | Check manually | Rarely touched |
| Chromatic_Core_Family | Canon icons | No apply script | Icon files only |

## Verified relocated roots (as of 2026-07-05)

| Root | ~/ path | Extra path | Status |
|------|---------|------------|--------|
| Commands | Symlink → Extra | Real dir | Dual-path set |
| Homes_Manager | Symlink → Extra | Real dir | Dual-path set |
| Learning_System | Symlink → Extra | Real dir | Dual-path set |
| Transition | Symlink → Extra | Real dir | No icon mapping exists |

## Pitfalls

- **Do NOT treat every Extra path as a relocation.** Operations, Control, Canon, and Projects exist as SEPARATE directories at both paths with different contents. They are NOT relocations — they are the runtime/authority roots that stay at `~/` per migration docs.
- **Do NOT remap Project Rooms.** The migration docs explicitly say "/Users/ted/Projects remain current authority until explicit cutover."
- **Do NOT assume the apply script supports `--dry-run`.** Read the script's help/usage section. Some default to dry-run (no-flag = dry), others default to apply and need `--dry-run`.
- **Symlinked targets resolve through the symlink.** Applying an icon to `/Users/ted/Commands` (a symlink) puts the icon on the symlink itself, not on the real directory at Extra. That's fine for Finder navigation through `~/`. The dual-path approach ensures the Extra real path also gets the icon for when Ted browses there directly.
- **Alias files (macOS .alias) don't work the same as symlinks.** `file /Users/ted/WORKSPACE_MAP` shows "MacOS Alias file" — these may not resolve through the same mechanism. Treat aliases differently from symlinks (check per case).
