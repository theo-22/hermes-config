# CDP → Playwright Cookie Bridge (2026-07-09)

**Context:** Substrate-Hermes migrated the `grocery-receipt-staged-fetcher` cron from default profile to substrate-hermes. The cron errored with "Not logged in" — the Playwright script uses an isolated browser profile (`/tmp/ht_session_persist`) and cookie file (`/tmp/ht_cookies.json`), while Ted logged into Harris Teeter on the CDP browser (cost-dashboard Chrome at port 9222).

**Resolution:** Extracted cookies from the CDP browser via `Storage.getCookies` and saved them in Playwright format to `/tmp/ht_cookies.json`.

## Technique

1. Connect to CDP WebSocket endpoint (port 9222)
2. Call `Storage.getCookies` — returns ALL browser cookies across all sites
3. Filter for `harristeeter.com` and `kroger.com` domains
4. Map to Playwright cookie format with sameSite title-case fix
5. Save to `/tmp/ht_cookies.json` — the grocery fetcher reads this on startup

## sameSite casing

CDP returns `sameSite: "LAX"` (uppercase). Playwright's `add_cookies()` requires `sameSite: "Lax"` (title case). The error message:
```
BrowserContext.add_cookies: cookies[0].sameSite: expected one of (Strict|Lax|None)
```
Fix via lookup dict: `{"LAX": "Lax", "STRICT": "Strict", "NONE": "None"}.get(ss.upper(), "Lax")`

## Results

- Extracted 54 cookies (Harris Teeter + Kroger)
- Fetcher loaded all 54 and authenticated successfully
- Pulled 1 order: July 8, 2026 — $11.05 (in-store, 2 items)
- Saved to `Substrate_Finance_Planning/Evidence/Grocery_Receipt_Staging/`

## Limitations

- Session-only cookies (`expires: -1`) die when CDP browser closes
- Need re-extraction after CDP browser restart or cookie expiry (~30 days)
- Script used `websocket` Python library — requires `pip install websocket-client`
- CDP port 9222 must be reachable at extraction time
