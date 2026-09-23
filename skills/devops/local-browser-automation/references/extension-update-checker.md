# Extension Update Checker Pattern

Cron job to monitor the Hermes Browser Extension repo for updates.

## Setup

```bash
# Check manually
cd /Volumes/Extra/Substrate/Hermes/hermes-browser-extension && git fetch origin main && git log HEAD..origin/main --oneline
```

## Cron Configuration

- **Schedule:** Weekly Monday 10am
- **Job ID:** `199110651907`
- **Script:** Prompt-only (no script)
- **Action:** Compare local HEAD with origin/main
- **Output:** Report new commits or "No updates available"
- **Auto-update:** NO — manual only (Ted prefers to decide when to update)

```bash
# Create cron
cronjob action=create \
  name="browser-extension-update-check" \
  schedule="0 10 * * 1" \
  prompt="Check for updates to Hermes Browser Extension at /Volumes/Extra/Substrate/Hermes/hermes-browser-extension/. Run: cd /Volumes/Extra/Substrate/Hermes/hermes-browser-extension && git fetch origin main. Compare local HEAD with origin/main. Report if there are new commits (with commit messages) or 'No updates available'. Do NOT auto-update or rebuild."
```

## Why Manual Updates

- Rebuilding the extension resets its Chrome extension ID (see Rebuild Warning in hermes-browser-extension.md)
- All settings (API key, permissions, CORS) are lost on rebuild
- Ted prefers to decide when to reconfigure vs. getting new features
