# meta_agent_sweep.py Bug Fix — 2026-06-29

## Bug

`AttributeError: 'NoneType' object has no attribute 'lower'` at lines 268 and 337.

## Root Cause

`extract_field()` returns `None` when a field is not found in the room state content. The code assumed the value was always a string:

```python
# Line 268 (in analyze_project_room)
result["blocked"] = extract_field(state_content, "Blocked")
if result.get("blocked", "").lower().startswith("yes"):  # BUG: None.lower() crashes

# Line 337 (in attention_bucket)
if analysis.get("blocked", "").lower().startswith("yes"):  # BUG: None.lower() crashes
```

The `.get("blocked", "")` default only fires if the key is **missing entirely** — not if the value is `None`.

## Fix

Replace with explicit None-coalescing:

```python
# Line 268
if (result.get("blocked") or "").lower().startswith("yes"):

# Line 337
if (analysis.get("blocked") or "").lower().startswith("yes"):
```

## Files Modified

- `/Volumes/Extra/Substrate/Operations/scripts/meta_agent_sweep.py` (symlink → actual file)
- `/Users/ted/.hermes/profiles/substrate-hermes/scripts/meta_agent_sweep.py` (cron copy)

## Verification

After fix, ran successfully: 36 rooms scanned, 0 needing action, exit 0.
