# General-Purpose CDP Browser Setup

Created: 2026-06-29

## What It Is

A second Chrome instance that Hermes controls via CDP (Chrome Deviation Protocol). Launched with `--remote-debugging-port=9222`, separate profile from main Chrome.

## Launch Command

```bash
/Volumes/Extra/Apps/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/hermes_chrome_profile" \
  --no-first-run
```

## Hermes Config

```yaml
# ~/.hermes/profiles/<profile>/config.yaml
browser:
  cdp_url: "http://127.0.0.1:9222"
```

## Key Properties

- **Separate profile** — `/tmp/hermes_chrome_profile`, won't conflict with main Chrome's profile
- **Persistent cookies** — log in once, cookies survive across sessions (until `/tmp` is cleared)
- **Visible window** — user can watch Hermes drive it
- **Not your main Chrome** — no extensions, no bookmarks, no existing logins

## Limitations Discussedd

- Ted: "This is not really ready for use yet" — new profile every time, lose settings, can't share with main Chrome
- Codex/Claude have better computer-use UX, Hermes's integration isn't seamless yet
- The browser extension is the preferred approach for interactive browsing
- CDP debug Chrome is better for automation/scraping (grocery receipts via Playwright)

## Use Cases

1. **Authenticated scraping** — Playwright attaches to this Chrome's debug port for sites that block headless/cloud browsers
2. **Automated testing** — script-driven browser interaction
3. **Future: extension + CDP combo** — extension drives the connected browser (not yet seamless)

## User Frustration Rules (from this session)

- **Don't open/close Chrome repeatedly** — Ted got frustrated watching windows appear and disappear
- **"Yes" once = authorization** — don't re-confirm or try multiple approaches
- **"Stop" means stop** — don't keep iterating
- **Report success, not limitations** — if it works, just say it works
- **2-try rule** — if something fails twice, stop and explain
