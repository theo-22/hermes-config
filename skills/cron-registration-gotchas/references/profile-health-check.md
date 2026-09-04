# Profile Health Check

Periodic verification that all Hermes profiles are healthy. Run this after runtime relocations, profile changes, or when cron jobs start failing silently.

Current fleet: **7 gateway profiles** + **1 mold/decommissioned** + **9 worker profiles** (spawned on-demand).

## What to check

### 1. Gateway status (all profiles)

```bash
hermes gateway status
```

Expected output: All 7 gateways with ✓ and a PID.

| Profile | Model | Role |
|---------|-------|------|
| default | deepseek-v4-flash | Primary gateway, ~44 cron jobs |
| advisor | deepseek-v4-flash | Morning advisory loop, Telegram-facing |
| brain-hermes | deepseek-v4-flash | Brain/Pieces operations |
| claude-hermes | deepseek-v4-pro | Heavy-lifting dispatch, Telegram |
| coordinator-hermes | deepseek-v4-flash | Coordinator support |
| lab-hermes | deepseek-v4-flash | Experiments, fleet probes |
| substrate-hermes | deepseek-v4-flash | Substrate maintenance |

Worker profiles (no gateways — spawned on-demand): brain-ingest-tracer, console-usage-collector, doc-reconciler, legacy-room-triager, museum-root-migrator, path-migration-auditor, reconciler, refiner, verifier

### 2. Config + model per profile

```bash
for p in advisor brain-hermes claude-hermes coordinator-hermes lab-hermes substrate-hermes; do
  echo "=== $p ==="
  hermes -p "$p" config show 2>&1 | head -12
  echo
done
# Default profile:
hermes config show 2>&1 | head -12
```

Verify:
- Each profile's `Config:` path starts with `/Users/ted/.hermes/` (internal, not Extra)
- `Secrets:` points to the profile's own `.env`
- `OpenRouter` key present for all profiles except claude-hermes (uses DeepSeek + GLM fallback)

### 3. DeepSeek API key per profile .env

```bash
for p in advisor brain-hermes claude-hermes coordinator-hermes lab-hermes substrate-hermes; do
  key=$(grep DEEPSEEK_API_KEY ~/.hermes/profiles/$p/.env 2>/dev/null | head -1)
  echo "$p: ${key:+present}${key:-MISSING}"
done
# Default profile:
key=$(grep DEEPSEEK_API_KEY ~/.hermes/.env | head -1)
echo "default: ${key:+present}${key:-MISSING}"
```

All profiles should show `present`.

### 4. Cron error scan — all profiles

The health pulse checks every profile's cron independently. Run it directly:

```bash
python3 /Volumes/Extra/Substrate/Skills/_shared/scripts/cron_health_pulse.py
echo "Exit: $?"
```

- Exit 0 with no output = all clean
- Exit 0 with error lines = stored error states that need attention

For per-profile inspection:

```bash
# Default profile
python3 -c "import json; data=json.load(open('/Users/ted/.hermes/cron/jobs.json')); [print(f\"{j['name']:30s} | {j.get('last_status'):10s} | {str(j.get('last_error',''))[:80]}\") for j in data.get('jobs',[]) if j.get('last_status') in ('error','unknown')]"

# Named profiles
for p in advisor brain-hermes coordinator-hermes lab-hermes substrate-hermes; do
  jp="/Users/ted/.hermes/profiles/$p/cron/jobs.json"
  [ -f "$jp" ] || continue
  errs=$(python3 -c "import json; data=json.load(open('$jp')); print(len([j for j in data.get('jobs',[]) if j.get('last_status')=='error']))")
  [ "$errs" != "0" ] && echo "$p: $errs error(s)"
done
```

### 5. Cron error fix patterns

**Stale error states** — script works but stored error persists (common after migration):

```bash
hermes -p <profile> cron run <job-name>
```

**Config drift guard** — LLM-driven job skipped because provider/model changed:

```bash
cronjob action=update job_id=<id> model='{"model":"deepseek-v4-flash","provider":"deepseek"}'
```

For per-profile LLM jobs (cronjob tool only fixes default), edit the profile's `cron/jobs.json` directly:

```python
import json
path = '/Users/ted/.hermes/profiles/<profile>/cron/jobs.json'
data = json.load(open(path))
for j in data['jobs']:
    if j.get('name') == '<job-name>':
        j['provider'] = 'deepseek'
        j['model'] = 'deepseek-v4-flash'
        j['last_status'] = 'ok'
        j.pop('last_error', None)
json.dump(data, open(path, 'w'), indent=2)
```

For permanent fixture: the `cron_health_pulse.py` re-reads from disk, so any direct json edit is reflected immediately in the pulse.

### 6. Symlinked loss-tolerant data

After a runtime relocation, these directories are symlinked back to Extra:

```bash
ls -la ~/.hermes/state-snapshots
ls -la ~/.hermes/decommissioned_profiles
```

Both should resolve to `/Volumes/Extra/Substrate/.hermes/...`.

### 7. Internal vs Extra profile parity

After migration, internal and Extra profile dirs should match:

```bash
diff <(ls /Volumes/Extra/Substrate/.hermes/profiles/ | sort) <(ls ~/.hermes/profiles/ | sort)
```

No output = clean. Any output lists profiles missing from one side.

## When to run

- After any `hermes update` or runtime relocation
- After profile creation or cloning
- When a profile's Telegram bot goes silent
- When Ted reports "something feels off" with the system
- Weekly hygiene — the profile fleet is stable and small enough for a quick scan

---
*Consolidated 2026-09-04 (#1574). A second, older copy of this file existed at
`~/.hermes/profiles/advisor/skills/cron-registration-gotchas/references/`, dated
2026-06-28. It was strictly narrower — no fleet table, and it still listed the
retired `ga-hermes` profile — so this 2026-07-16 version supersedes it and the
older one was not merged.*
