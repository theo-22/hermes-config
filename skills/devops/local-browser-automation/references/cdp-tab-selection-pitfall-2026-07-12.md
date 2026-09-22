# CDP Tab-Selection Pitfall — Chrome Session Restore (2026-07-12)

## Symptom

When launching Chrome with `--new-window <URL>`, the browser may restore the **previous session's last active tab** instead of loading `<URL>`. The `find_tab_ws()` function then connects to that wrong tab and reads unintended page content.

Example: Fundrise scraper connected to a Samsclub purchase history tab because Chrome restored the prior session.

## Root Cause

Chrome's `--new-window` flag creates a new window but doesn't force that window to load the provided URL in the active tab — especially when the user-data-dir has a saved session with open tabs. Chrome restores the old session first, and the launch URL may end up in a background tab or never load.

## Fix

After connecting to a tab and enabling Page, verify the URL before reading page content:

```python
current_url = await evaluate("window.location.href")
if current_url and "targetdomain.com" not in current_url:
    domain = "unknown"
    try:
        parts = current_url.split('/')
        if len(parts) > 2 and parts[2]:
            domain = parts[2]
    except Exception:
        domain = "unknown"
    print(f"[scraper] Tab is on {domain} — navigating to target...")
    await cdp("Page.navigate", {"url": TARGET_URL})
    await asyncio.sleep(8)
    # Check for bot challenge
    body = await evaluate("document.body?.innerText || ''")
    if body and ("human" in body.lower() or "verify" in body.lower()):
        print("[scraper] Bot challenge detected, waiting...")
        await asyncio.sleep(15)
    await asyncio.sleep(3)
```

## Related

- HT store-selector wall: direct navigation to `/specials/my-specials` triggers a store modal that blocks deal modals. Navigate via nav bar links instead of direct URL to avoid it.
- Bot detection from `Page.navigate` via CDP: some sites (Fundrise) trigger Cloudflare challenges on CDP-initiated navigation. The 15-second wait usually resolves them.
