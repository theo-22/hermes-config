# HT Bot Detection & API Alternative — 2026-07-12

## Discovery
During the live HT shopping session (Jul 12), HT presented a "click and hold to prove you're human" challenge. CDP's `--remote-debugging-port=9222` is a detectable automation signal. HT is actively fighting CDP automation.

## Observable symptoms of bot detection
- "Click and hold" or "press and hold" challenges appearing during page interactions
- Clicks not registering on React SPA buttons (may be site fighting automation, not just React quirks)
- Search returning "no results" for valid queries (HT search was unreliable in general, but bot detection amplifies this)
- Modal content failing to load when it previously worked on a fresh session
- Elements found by text scanning but button events not firing

## Recommended approach: HT backend API
The web app calls internal APIs via AJAX. Sniffing these during a manual session provides a faster, cheaper, undetectable alternative:

1. Open Chrome DevTools → Network tab during a manual HT session
2. Filter by XHR/Fetch
3. Identify API calls for:
   - Purchase history: `/mypurchases` → order list → order detail
   - Weekly ad / My Specials deal data
   - Search results
   - Add to cart
4. Authenticate via session cookies (already in the hermes-browser profile)
5. Call APIs directly with `curl` or Python `requests` — no browser needed

## Alternative: Computer Use
Vision-based mouse control bypasses detection but is slower and costs more (vision tokens per step). Only worth considering if API approach fails.

## What this means for CDP
- **CDP is not dead** — it works fine for sites without bot detection (Fundrise, provider consoles)
- **For HT specifically**, API calls are the better path
- Keep the CDP browser running for authenticated sessions that do need browser rendering
