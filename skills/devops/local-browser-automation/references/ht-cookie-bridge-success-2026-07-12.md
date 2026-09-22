# Harris Teeter CDP Cookie Bridge — 2026-07-12

## Situation

The `grocery-receipt-staged-fetcher` cron (Playwright with `/tmp/ht_session_persist` context)
kept erroring "Not logged in" even though the CDP browser (port 9222, `hermes-browser` profile)
had a valid Harris Teeter session from a prior manual login.

The two browsers don't share cookies — Playwright's `/tmp/ht_session_persist` is separate from
Chrome's current profile at `/Users/ted/Library/Application Support/Browser_Profiles/hermes-browser` (moved from the original retired path after this specimen).

## Fix: Bridge CDP Cookies → Playwright

1. Navigate the CDP browser to Harris Teeter (auto-authenticates from saved session)
2. Extract cookies via CDP `Storage.getCookies` call
3. Filter for `harristeeter.com` / `kroger.com` domains
4. Fix `sameSite` casing (CDP returns `"LAX"`, Playwright expects `"Lax"`)
5. Save to `/tmp/ht_cookies.json`
6. The Playwright fetcher already reads from that path

## Results

- **57 cookies** extracted including `loggedIn: yes` and `kroger-si-customer-data-token` JWT
- Tester successfully authenticated, fetched 1 order ($11.05, Jul 8)
- No manual login needed — cookies were still valid from a login weeks ago

## Extraction Script Pattern

```python
import asyncio, json, websockets
from urllib.request import urlopen

async def extract_cookies(domain_filter="harristeeter"):
    tabs = json.loads(urlopen("http://127.0.0.1:9222/json").read())
    t = [x for x in tabs if x["type"] == "page"][0]
    ws_url = t["webSocketDebuggerUrl"]

    msg_id = 0
    async def cdp(method, params=None):
        nonlocal msg_id
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        while True:
            raw = await ws.recv()
            d = json.loads(raw)
            if d.get("id") == msg_id:
                return d

    async with websockets.connect(ws_url) as ws:
        result = await cdp("Storage.getCookies")
        return result.get("result", {}).get("cookies", [])

# Filter + fix sameSite casing
cookies = await extract_cookies()
playwright_cookies = []
for c in cookies:
    if "harristeeter" in c["domain"] or "kroger" in c["domain"]:
        playwright_cookies.append({
            "name": c["name"],
            "value": c["value"],
            "domain": c["domain"],
            "path": c.get("path", "/"),
            "secure": c.get("secure", True),
            "httpOnly": c.get("httpOnly", False),
            "sameSite": {"LAX": "Lax", "STRICT": "Strict", "NONE": "None"}.get(
                c.get("sameSite", "").upper(), "Lax"
            ),
        })
```
