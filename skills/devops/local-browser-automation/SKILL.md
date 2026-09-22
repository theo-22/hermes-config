---
name: local-browser-automation
description: Drive local Chrome via CDP or Playwright for authenticated scraping — HT, Fundrise, Sam's Club, provider dashboards.
category: devops
write_mode: active
one_line_use: "When you need to scrape a site that requires login, uses CDP-connected Chrome or Playwright persistent context."
fast_pick: CDP browser launch · Authenticated scraping · Login-wall handling · Exit-code discipline
---

# Local Browser Automation

**Purpose:** Drive Ted's always-open CDP Chrome browser (port 9222) to scrape authenticated sites — Harris Teeter receipts, Fundrise balance, Sam's Club orders, AI provider dashboards. **CDP is the default. Playwright is deprecated** — only kept where CDP can't bypass bot detection.

**When to use:**
- Site requires login (Ted keeps the CDP browser logged in)
- Site uses JavaScript rendering (SPA) that raw HTTP can't handle
- Ted is actively on the site and wants to show/verify something
- You need to extract data from an authenticated session using an existing tab

---

## Single Approach: CDP Browser (Ted's always-open Chrome)

Ted keeps a Chrome instance running on port 9222 with all his accounts logged in. All scrapers connect to it directly via WebSocket CDP commands. No separate browser profiles, no cookie files to juggle.

**Launch the browser (if needed):**
```python
CDP_HTTP = "http://127.0.0.1:9222"
CHROME_PATH = "/Volumes/Extra/Apps/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE_DIR = "/Users/ted/Library/Application Support/Browser_Profiles/hermes-browser"

def ensure_browser():
    try:
        urlopen(f"{CDP_HTTP}/json/version", timeout=3)
        return  # already running
    except:
        subprocess.Popen([CHROME_PATH, f"--remote-debugging-port=9222",
                         f"--user-data-dir={PROFILE_DIR}",
                         "--profile-directory=Profile 1",  # '615' agent identity — ALWAYS pin (Pitfall 8)
                         "--no-first-run",
                         "--new-window", TARGET_URL], ...)
```

**Key pattern — connect and evaluate:**
```python
tabs = json.loads(urlopen(f"{CDP_HTTP}/json").read())
ht_tab = [t for t in tabs if t["type"]=="page" and "harristeeter.com" in t["url"]]
ws_url = ht_tab[0]["webSocketDebuggerUrl"]

async with websockets.connect(ws_url) as ws:
    async def cdp_call(ws, method, params=None):
        msg_id = int(time.time() * 1000) % 100000
        await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        while True:
            raw = await ws.recv()
            data = json.loads(raw)
            if data.get("id") == msg_id:
                return data
            if "method" in data:
                continue  # swallow events
    
    async def evaluate(js):
        r = await cdp_call(ws, "Runtime.evaluate", {"expression": js, "returnByValue": True})
        return r.get("result",{}).get("result",{}).get("value")
    
    await cdp_call(ws, "Page.navigate", {"url": target_url})
    await asyncio.sleep(5)
    title = await evaluate("document.title")
    body = await evaluate("document.body?.innerText || ''")
```

**Key pattern — trusted CDP click (HT React SPA clicks + Chrome autofill trigger):**
```python
async def trusted_click(ws, selector):
    box = await evaluate(
        "(()=>{const el=document.querySelector(%s);if(!el)return null;"
        "const r=el.getBoundingClientRect();"
        "return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2});})()" % json.dumps(selector))
    if not box:
        return False
    c = json.loads(box)
    await cdp_call(ws, "Input.dispatchMouseEvent",
              {"type": "mousePressed", "x": c["x"], "y": c["y"],
               "button": "left", "clickCount": 1})
    await cdp_call(ws, "Input.dispatchMouseEvent",
              {"type": "mouseReleased", "x": c["x"], "y": c["y"],
               "button": "left", "clickCount": 1})
    return True
```

---

## Login-Wall Handling Strategy

**Priority order:**
1. **Cookies still valid** → fastest, no login needed
2. **Chrome saved passwords** → CDP trusted click on password field triggers autofill, then click Log in
3. **Auto-launch login flow** (preferred) → script detects session expired, opens visible browser with credentials auto-filled, waits up to 5 min for Ted to click Sign In, saves cookies, retries fetch
4. **`--login` flag** (fallback) → run manually once to save cookies

**Auto-launch login flow (the right way, 2026-07-18):**
When a Playwright scraper detects a login redirect, don't just print a message and exit. Auto-launch the login flow (`login_flow()`) which opens a VISIBLE browser, navigates to the login page, and waits up to 5 minutes with credentials already filled. After Ted clicks Sign In, the flow saves cookies and retries the fetch:

```python
if 'signin' in page.url or 'login' in page.url:
    await context.close()
    print("🔓 Session expired — launching login window (credentials auto-filled, just click Sign In)")
    await login_flow()
    # Retry with fresh cookies
    async with async_playwright() as p2:
        ctx2 = await p2.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR, headless=True, ...)
        page = ctx2.pages[0] if ctx2.pages else await ctx2.new_page()
        # load fresh cookies, navigate, check again
        if 'signin' in page.url:
            print("❌ Still not logged in — login may not have completed")
            return None  # real error
        context = ctx2  # use new context for the rest of the fetch
```

**Why auto-launch instead of just printing:** Ted reported seeing popup windows appear and then disappear while he was trying to log in. Auto-launching the login flow keeps the window open (5 min timeout) and saves cookies on success. If nobody's at the computer, the window sits until timeout, then exits.

**Exit-code discipline (CRITICAL — updated 2026-07-18):**
Scripts should auto-launch login first. The script's main section should treat `result is None` as a real error (login was attempted but failed) and exit 1:

```python
# In __main__:
result = asyncio.run(fetch_receipts())
if result is None:
    exit(1)  # Login flow was attempted but failed — real error
```

This is the inverse of the earlier pattern. Now `result is None` means the auto-login was attempted AND failed, which IS a cron error worth reporting. The login wall itself is handled inside `fetch_receipts()`, not by exiting at the top level.

**Rationale:** Ted set up these scrapers knowing some require periodic manual login. The scripts already populate username/email. The remaining step is one mouse click. The script should OPEN a window for that click, not print a message and disappear.

---

## Browser Identity Policy (Ted, 2026-09-22)

**One AI browser profile for all actors.** Chrome profile "Profile 1" ("615", `615l5guest@gmail.com`) in the fleet `hermes-browser` dir is THE agent identity — every actor (Hermes profiles, other models, any AI runtime) uses it for all browser work. Never create per-actor Chrome profiles; never use Ted's personal Default profile or Jackie's profile for agent work.

Rationale: browser profiles are cookie jars, not identities — ownership/attribution lives in the account layer (executions.db, actor labels), not the browser. One profile = one login surface, one blast radius, sessions shared across actors via the always-open tabs.

Separation lives at the site-account level *inside* the profile when needed (e.g., guest vs real account on the same site = different logins within 615, not a new Chrome profile). New AI registrations default to `615l5guest@gmail.com`.

**Identity resource inventory (reserve):** Ted holds ~4-5 registered domains with websites + can create more; disposable/guest mailboxes on the AI-facing Gmail family are available. These are a standing reserve for future AI identity needs (sacrificial accounts, site-specific identities) — expected to stay unused; if a future site demands identity separation that money/risk justifies, a second agent profile or a new domain/alias is a five-minute addition, not an architecture change.

---

## CDP Tab Selection

When attaching to a running Chrome with multiple tabs, find the right one by URL:
```python
tabs = json.loads(urlopen(f"{CDP_HTTP}/json", timeout=10).read())
for t in tabs:
    if t.get("type") == "page" and "target-site.com" in t.get("url", ""):
        return t["webSocketDebuggerUrl"], t["id"]
```

If no matching tab exists, open a new one:
```python
tab = json.loads(urlopen(
    Request(f"{CDP_HTTP}/json/new?{TARGET_URL}", method="PUT"), timeout=10
).read())
```

**Pitfall:** Chrome may open a generic "New Tab" page (`chrome://newtab/`) instead of the target URL. After `Page.navigate`, wait and check `window.location.href` — the tab may need 3-5 seconds to resolve past redirects or bot challenges.

---

## Bot Challenge Handling

Sites using Akamai, Cloudflare, or similar bot detection:
1. Look for "human", "verify", or "click and hold" in page body text
2. Wait 10-15 seconds and retry
3. If persistent, the script needs a live browser session (headless mode triggers bot detection more aggressively)

---

## Pitfalls

**Pitfall 1. Script content doesn't match `.sh` extension.** Cron runs `.sh` files via bash. If your scraper is Python, either name it `.py` and set `no_agent: true` (cron runs via python3 for .py), or wrap it in a `.sh` shell script.

**Pitfall 2. Credential autofill doesn't always work.** Chrome's autofill is heuristic. Sometimes the password field selector `input[type=password]` doesn't match custom form fields. Fallback: check how many inputs are filled (>=1 means credentials are there).

**Pitfall 3. CDP session state doesn't persist.** Each `Runtime.evaluate` call is independent — event subscriptions don't survive between calls. Use the dedicated browser tools for stateful workflows, or pass `frame_id` for cross-origin iframes.

**Pitfall 4. Script must be in the profile scripts dir.** Cron resolves scripts relative to `~/.hermes/profiles/<profile>/scripts/`, not the shared `~/.hermes/scripts/`. After editing, sync: `cp ~/.hermes/scripts/X.py ~/.hermes/profiles/<profile>/scripts/X.py`

**Pitfall 5. HT bot detection.** Akamai detection at `www.harristeeter.com` is less aggressive when the CDP browser is already logged in via a real user session (as Ted keeps it). If extraction fails, the page may need a longer wait or a navigation refresh. The HT receipt fetcher falls back to extracting via innerText from the purchase history page — simpler than navigating SPA deal cards.

**Pitfall 6. Hermes browser tools may open new tabs that tools don't track.** When using the Playwright-backed tools (`browser_navigate`, `browser_click`, etc.), clicking a link may open content in a **new browser tab** that the toolset doesn't know about. After the click, `browser_snapshot`, `browser_console`, and `window.location.href` return stale content from the original tab. Common triggers:
- Retail purchase-history links (Harris Teeter, Sam's Club)
- SPA apps that deep-link via `window.open()` or `<a target="_blank">`

**Detection:** After a click that should navigate, run `browser_cdp(method='Target.getTargets')` and scan for a tab matching the expected URL or title.

**Escape hatch:** Use `Runtime.evaluate` with the new tab's `target_id` to extract content:
```
browser_cdp(method='Runtime.evaluate',
  params={'expression': "document.querySelector('main').innerText", 'returnByValue': True},
  target_id='<targetId-from-getTargets>')
```

**Prevention:** Before clicking, check if the element has `target="_blank"` or a click handler that opens a new window. If so, use CDP `Page.navigate` or the dedicated scraper script instead.

**Pitfall 7. Sam's Club Next.js SPA resists direct URL order-detail access.** Sam's Club `/orders` uses client-side routing. The "See details" button (`<button>`) fires an SPA route change without changing the URL. Direct CDP navigation (`Window.location.href=...` or `Page.navigate`) to `/orders/ORDER-ID` renders a blank page — the route only works through the client-side router.

**Workarounds for Sam's Club item extraction:**
- **Item names from listing page**: Product thumbnail `alt` attributes contain full item names. Extract via: `document.querySelectorAll('img[alt]').forEach(i => console.log(i.alt))`
- **Prices**: Not available on the listing page. Use the dedicated `sams_club_fetcher.py` script (Playwright-based) or `computer_use` to drive the visible browser window.
- **13-item discrepancy note**: The listing shows 12 images for a 13-item order — the last item may not have a product image.

**Pitfall 8. ALWAYS pin the Chrome profile on fleet relaunches; never rely on last-used.** Every fleet launcher (signal scan, gemini digest, grocery/fundrise fetchers) passes `--profile-directory="Profile 1"` — the "615" agent identity where the always-open sessions live. An un-pinned relaunch lands on whatever profile Chrome last used, so agent tabs and personal tabs silently mix identities and saved sessions appear to vanish. Cookie sessions live in the profile on disk: a graceful quit + pinned relaunch preserves all logins and restores the standing tabs — restart is safe and is the correct fix when the listener is gone.

**Pitfall 9. A running Chrome is not a CDP Chrome.** A manual plain launch (or Ted's own browsing instance) takes the profile lock without the debug port, so the fleet launcher's relaunch becomes a no-op flag drop and 9222 refuses connections. Symptom: "Chrome is running but connection refused." Fix: quit Chrome gracefully, relaunch the fleet instance with the pinned profile (Pitfall 8) — never force-kill the personal browsing instance.

**Pitfall 10. Verify login state by in-page probe, not tab titles.** Titles flip to logged-in-looking strings on both states. Ground truth per site, via the site's own tab: same-origin `fetch('/path', {redirect:'manual', credentials:'include'})` → `type:'opaqueredirect'` = signed out, `status:200` = signed in; for APIs, call the real endpoint (HT purchase-history-search returning orders beats any title check).

---

## Built-in Scripts

| Script | Site | Approach | Schedule | Notes |
|--------|------|----------|----------|-------|
| `grocery_receipt_fetcher.py` | Harris Teeter | **CDP** (always-open browser) | Sundays 10am | Uses existing HT tab, extracts orders + items |
| `sams_club_fetcher.py` | Sam's Club | **CDP** (always-open browser) | Sundays | Uses existing Sam's tab, extracts orders |
| `fundrise_scraper.py` | Fundrise | CDP + saved passwords | 1st, 15th | Credentials auto-populate, just click Log in |

---

## References

- `references/cdp-websocket-scraping-pattern-2026-07-11.md` — Full fundrise scraper session detail
- `references/ht-cdp-patterns-2026-07-12.md` — HT CDP scraping patterns
- `references/cdp-tab-selection-pitfall-2026-07-12.md` — Tab selection gotcha
- `references/ynab-writeback-scrape-pattern.md` — YNAB writeback integration
- `references/ht-bot-detection-cdp-challenge-2026-07-13.md` — HT bot detection details
- `references/grocery-midweek-pull-2026-07-29.md` — Multi-tab CDP escape hatch + Sam's Club SPA extraction limitation
