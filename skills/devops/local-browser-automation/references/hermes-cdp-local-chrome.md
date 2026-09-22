# Hermes CDP Local Chrome Configuration

## Discovery Date
2026-06-29 — during Harris Teeter receipt automation session

## Problem
Hermes's built-in browser tools (`browser_navigate`, `browser_click`, `browser_type`, etc.) use **Browserbase** (cloud browser) by default. This fails for sites with anti-bot OAuth flows (Kroger B2C, banks, etc.) because:
- Cloud browsers get `ERR_HTTP2_PROTOCOL_ERROR` on Harris Teeter
- OAuth redirect chains (harristeeter.com → login.kroger.com → onmicrosoft.com → back) break cloud browser sessions
- Window closes unexpectedly during multi-domain auth flows

## Solution: Hermes CDP Config

Hermes can route browser tools to your **local Chrome** via CDP (Chrome DevTools Protocol):

```yaml
# ~/.hermes/config.yaml (or profile-specific config)
browser:
  cdp_url: "http://127.0.0.1:9222"
```

Then `browser_*` tools use YOUR Chrome with your logged-in sessions.

## Prerequisites

1. Chrome must be running with `--remote-debugging-port=9222`
2. Ted's config already has `cdp_url: ''` (empty) — just needs the value set
3. Chrome path: `/Volumes/Extra/Apps/Google Chrome.app`

## Launch Command

```bash
/Volumes/Extra/Apps/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/hermes_chrome_profile" \
  --no-first-run
```

**CRITICAL: Use a separate `--user-data-dir`** — trying to attach to your main Chrome (already running without the debug flag) fails because the new instance forwards to the existing process and the flag is ignored. A separate profile:
- Opens a NEW Chrome window (your main Chrome stays untouched)
- Cookies persist in `/tmp/hermes_chrome_profile` between runs
- You log in once to any site, Hermes reuses the session
- Works for general web exploration, not just groceries

**Important**: Chrome must be started fresh with this flag. If Chrome is already running without the flag, the new instance forwards to the existing process and the flag is ignored.

## CLI Alternative

Hermes also has a `/browser connect` slash command (CLI only, not available in chat):
```
/browser connect                 # Auto-launch/connect at http://127.0.0.1:9222
/browser connect ws://host:port  # Specific CDP endpoint
/browser status                  # Check connection
/browser disconnect              # Detach
```

## When to Use CDP vs Playwright Script

| Approach | Best For |
|----------|----------|
| Hermes CDP config | Interactive tasks where you want Hermes to drive your visible browser |
| Playwright script (persistent context) | Scheduled cron scraping, complex extraction, item-level parsing |

For Ted's grocery receipts: **Playwright script is better** because:
- Runs as `no_agent` cron (no LLM tokens)
- Handles complex DOM extraction (aria-label, split-span prices)
- Persistent context survives between runs
- Doesn't require Chrome to be always running with debug flag

## Config Location

- Global: `~/.hermes/config.yaml`
- Profile-specific: `~/.hermes/profiles/<profile>/config.yaml`
- Ted's substrate-hermes profile already has the `cdp_url` field at empty string
