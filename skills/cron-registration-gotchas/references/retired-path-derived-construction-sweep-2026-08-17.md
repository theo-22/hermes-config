# Retired path keeps recreating? Search derived construction, not just the literal

Session: 2026-08-17. A home-resident symlink (`/Users/ted/Operations`) was removed
to force-discovery latent stale-path writers. The dir kept reappearing despite a
literal-string sweep.

## The failure

A naive `grep`/`sed` for the literal `/Users/ted/Operations` only caught consumers
that spelled the path out. A whole class of scripts **build** the path from a base
and escaped the sweep, silently recreating the dir on every run:

```python
HOME = Path("/Users/ted")
OPERATIONS_DIR = HOME / "Operations"              # derived — MISSED by literal grep
REPORT = HOME / "Operations" / "reports/..."      # derived — MISSED
STATE = Path.home() / "Operations" / "state/..."  # derived — MISSED
SRC   = pathlib.Path.home() / "Operations/scripts/foo.py"  # derived — MISSED
ROOT  = Path(os.path.expanduser("~/Operations/reports/GPT_Self_Checks"))  # derived — MISSED
OUT   = os.path.expanduser("~/Operations/bridge_health_state.json")       # derived — MISSED
```

## The complete search pattern (grep ALL of these)

```bash
# 1. literal retired string
grep -rn "/Users/ted/Operations" <dir>

# 2. base-var derivation
grep -rnE 'HOME\s*/\s*"Operations"|Path\.home\(\)\s*/\s*"Operations"|pathlib\.Path\.home\(\)\s*/\s*"Operations"' <dir>

# 3. expanduser / ~-prefixed / absolute hardcodes
grep -rnE 'expanduser\("~/Operations|"/Users/ted/Operations' <dir>
```

## Classify operative code vs docstring

Only **operative code** (an assignment/expression used for the write or read)
needs repointing. Docstring/history mentions (e.g. `# writes to ~/Operations/...`,
a comment listing an old path) are harmless as long as no code builds a write from
them — but flag them so a later re-sweep doesn't confuse them with real writers.

## Scope the authoritative set FIRST

The cron scheduler executes the **profile-local copy**
(`~/.hermes/profiles/<profile>/scripts/`), NOT the root copy (`~/.hermes/scripts/`).
Only the profile-local copy is the authoritative consumer for cron work. When Ted
wants a contained fix, fix the enabled cron-executed script set first, verify it,
then fan out — this matches Ted's documented pacing preference.

## After the fix

- Purge stale `.pyc` (`find ... -path '*/__pycache__/*' -name '<name>*.pyc' -delete`)
  so old compiled bytecode doesn't carry the old path.
- Run one write-in-the-script to prove the canonical output lands.
- Confirm `/Users/ted/Operations` stays ABSENT after the run. Its reappearance does
  NOT mean "restore it" — it means an untraced writer surfaced; trace it, don't
  re-add the symlink.
- Ted's own technique: removing the symlink is the forcing function that exposes
  hidden writers. Treat each reappearance as the detection net working.

## Straightforward 2-line fixes that catch lint traps

When const-correcting these derived paths, the canonical base is a single constant:
`OPS = Path("/Volumes/Extra/Substrate/Operations")`. Replacing `HOME / "Operations"`
with `OPS` is safe when the file also uses `HOME` for OTHER legit things
(`HERMES_HOME = HOME / ".hermes"`, `HOME / "Project"` etc.) — only change the
Operations-built constants. For `expanduser("~/...")` rewrites, add the `Path`
import if not already present (Pyright flags undefined `Path`).
