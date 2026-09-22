# CDP Tab Selection & Wrong-Tab Recovery — 2026-07-12

## Problem
When launching Chrome with `--new-window <URL>`, Chrome may restore the previous session tab instead of navigating to the target URL. The CDP script then connects to the wrong tab (e.g. Samsclub instead of Fundrise) and reads the wrong page content.

## Discovery
The Fundrise scraper was connecting to a Samsclub tab because Chrome restored the old session. The scraper's `find_tab_ws()` searched for `fundrise.com/account` in the URL, but the launched tab wasn't on Fundrise. The fallback `GET /json/new?URL` CDP endpoint has URL encoding issues with `://` in query params.

## Fix: explicit Page.navigate after connection
After connecting to any page tab via WebSocket:
1. Read `window.location.href`
2. If it doesn't contain the target domain, call `Page.navigate({"url": TARGET_URL})`
3. Wait 8s for navigation
4. Check for bot challenges ("human" or "verify" in body text) — wait 15s if detected
5. Proceed with scraping

This makes the scraper robust against whatever tab it connects to — it always navigates to the right page.

## Pattern code
```python
# After connecting to tab via websocket
current_url = await evaluate("window.location.href")
if "fundrise.com" not in current_url:
    await cdp("Page.navigate", {"url": DASHBOARD_URL})
    await asyncio.sleep(8)
    body = await evaluate("document.body?.innerText || ''")
    if body and ("human" in body.lower() or "verify" in body.lower()):
        await asyncio.sleep(15)  # Bot challenge auto-resolve
```

## Tradeoff
Page.navigate via CDP can trigger bot detection on aggressive sites (Cloudflare). For Fundrise it works fine. For HT it made things worse. Test per site.
