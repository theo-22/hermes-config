# CDP Attach: Authenticated Scraping via Running Chrome

**Pattern:** Connect Playwright to the user's already-running Chrome via remote debugging.
**Use when:** Sites block headless/automated browsers but work fine in the user's normal Chrome.

## When to Use

- Site shows `ERR_HTTP2_PROTOCOL_ERROR` or similar in headless Playwright
- Microsoft Azure B2C / OAuth flows detect automation
- You need the user's existing cookies/sessions (already logged in)
- Cloud browser (Browserbase) is timing out on redirect chains

## Prerequisites

1. Chrome must be running with `--remote-debugging-port=9222`
2. If Chrome is already running WITHOUT the flag, you must kill and restart it
3. Use a separate `--user-data-dir` to avoid profile lock conflicts

## Recipe

```bash
# Step 1: Kill existing Chrome (it won't have the debug port)
pkill -9 -f "Google Chrome"
sleep 3

# Step 2: Launch Chrome with debugging
# macOS (Ted's setup — Chrome on external volume):
/Volumes/Extra/Apps/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome_debug_profile \
  --no-first-run &

# Step 3: Wait for port to bind
sleep 8
curl -s http://localhost:9222/json/version
# Should return: {"Browser": "Chrome/...", "webSocketDebuggerUrl": "ws://..."}
```

```python
# Step 4: Connect and scrape
import asyncio
from playwright.async_api import async_playwright

async def scrape():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()
        
        # Now you have access to all cookies, sessions, logged-in state
        await page.goto('https://www.harristeeter.com/mypurchases')
        await asyncio.sleep(3)
        
        content = await page.content()
        # ... extract data ...
        
        await browser.close()  # Disconnects but does NOT kill Chrome

asyncio.run(scrape())
```

## Cleanup

```bash
# When done, kill the debug-port Chrome if you used a separate profile
pkill -9 -f "Google Chrome"
# Then restart normally (without the debug flag) if desired
```

## Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| `ECONNREFUSED localhost:9222` | Chrome not launched with flag, or not fully started | Kill Chrome, restart with `--remote-debugging-port=9222`, wait 8s |
| Chrome launches but port not bound | Another Chrome instance already running (flag ignored) | `pkill -9 -f "Google Chrome"` first, then restart |
| `ERR_HTTP2_PROTOCOL_ERROR` | Site blocks headless/Playwright-default browser | Use CDP attach to real Chrome instead |
| Profile lock error | Same `--user-data-dir` used by two instances | Use `/tmp/chrome_debug_profile` for the debug instance |
| `connect_over_cdp` not found | Wrong Playwright API | Use `p.chromium.connect_over_cdp()` not `launch_over_cdp()` |

## Verified Working (2026-06-29)

- ✅ Connected to Chrome/149.0.7827.197 via CDP
- ✅ Navigated to harristeeter.com (no HTTP/2 error)
- ✅ Loaded mypurchases page (confirmed logged in via existing session)
- ✅ Page showed "no recorded purchase history" — data availability issue, not auth issue
