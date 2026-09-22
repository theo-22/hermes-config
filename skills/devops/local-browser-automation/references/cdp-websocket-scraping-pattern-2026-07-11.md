# CDP WebSocket Scraping Pattern — 2026-07-11

**What changed:** Cron-based authenticated scraping moved from Playwright-only to native CDP WebSocket for simple value extraction. Fundrise scraper rewritten from Playwright (broken dep + expired cookies) to CDP WebSocket. Harris Teeter grocery fetcher updated with CDP cookie refresh.

**Motivation:** Playwright requires a separate browser context + cookie management + Python dependency. The browser-scanner Chrome (port 9222) already runs with persistent cookies — connecting directly via CDP WebSocket eliminates the middle layer.

## The Three Approaches

| Approach | Dependencies | Best For | Examples |
|----------|-------------|----------|----------|
| Native CDP WebSocket | `websockets`, `urllib` | Single-value extraction (balance, total, count) | Fundrise scraper |
| CDP Cookie Bridge + Playwright | `websocket-client`, `playwright` | Complex multi-click extraction (order list → detail → parse) | HT grocery fetcher |
| Playwright standalone | `playwright` + manual login | Sites without CDP browser session | Greenfield scrapers |

## CDP WebSocket Fundamentals

### Connecting

```python
from urllib.request import urlopen
import websockets

# Get tab info
tabs = json.loads(urlopen("http://127.0.0.1:9222/json", timeout=10).read())
# Find first page tab
tab = [t for t in tabs if t.get("type") == "page"][0]
ws_url = tab["webSocketDebuggerUrl"]  # e.g. ws://127.0.0.1:9222/devtools/page/<id>
target_id = tab["id"]

async with websockets.connect(ws_url) as ws:
    # ... send CDP commands
```

### Sending Commands & Filtering Events

CDP WebSocket multiplexes two message types:
- **Command responses:** Have an `"id"` field matching your request
- **Event notifications:** Have a `"method"` field (e.g., `Page.frameStartedLoading`)

**You MUST filter:** Without the `while True` loop, you get events instead of responses.

```python
msg_id = 0

async def cdp(method, params=None):
    nonlocal msg_id
    msg_id += 1
    payload = json.dumps({"id": msg_id, "method": method, "params": params or {}})
    await ws.send(payload)
    while True:
        raw = await ws.recv()
        data = json.loads(raw)
        if data.get("id") == msg_id:
            return data  # This is our response
        # Events are silently skipped
```

### Reading Page Content

```python
async def evaluate(js):
    r = await cdp("Runtime.evaluate", {
        "expression": js, "returnByValue": True
    })
    # ⚠️ THREE levels of nesting:
    return r.get("result", {}).get("result", {}).get("value")
    #  ^--- CDP envelope  ^--- JS result  ^--- actual value
```

The outer `result` is the CDP command response envelope (`{"id": N, "result": {...}}`).
The inner `result` is the JavaScript execution result (`{"type": "string", "value": "..."}`).

### Avoiding Bot Detection

`Page.navigate` via CDP triggers Cloudflare challenges (Fundrise: "Let's confirm you are human"). **Don't use it.** Instead:

- Launch Chrome with `--new-window <URL>` so the page loads naturally
- The tab opens and loads without CDP automation fingerprints
- Find the tab and read it — don't navigate it

```python
subprocess.Popen(
    [CHROME_PATH, "--remote-debugging-port=9222",
     f"--user-data-dir={PROFILE_DIR}", "--no-first-run",
     "--new-window", DASHBOARD_URL],  # This is key
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)
```

## Auto-Launch Pattern (cron-safe)

```python
def ensure_browser():
    """Auto-launch the CDP browser if not running."""
    try:
        urlopen("http://127.0.0.1:9222/json/version", timeout=3)
        return  # Already running
    except Exception:
        pass

    subprocess.Popen(
        [CHROME_PATH,
         "--remote-debugging-port=9222",
         f"--user-data-dir={PROFILE_DIR}",
         "--no-first-run",
         "--new-window", TARGET_URL],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    for _ in range(40):
        time.sleep(0.5)
        try:
            urlopen("http://127.0.0.1:9222/json/version", timeout=2)
            return
        except Exception:
            continue
    raise RuntimeError("Browser did not start within 20 seconds")
```

## Cookie Extraction for Playwright

When a site requires complex interaction (click each order, extract details), use the CDP browser's cookies to feed Playwright:

```python
# Extract cookies from CDP browser
r = await cdp("Network.getAllCookies")
cookies = r.get("result", {}).get("cookies", [])

# Convert to Playwright format (sameSite must be title case)
pw_cookies = []
for c in cookies:
    pw = {
        "name": c["name"], "value": c["value"],
        "domain": c.get("domain", ""), "path": c.get("path", "/"),
        "httpOnly": c.get("httpOnly", False), "secure": c.get("secure", False),
        "sameSite": {"LAX": "Lax", "STRICT": "Strict", "NONE": "None"}
            .get(c.get("sameSite", "").upper(), "Lax"),
    }
    # ⚠️ partitionKey: CDP returns as dict, Playwright expects string
    pk = c.get("partitionKey")
    if isinstance(pk, dict):
        pk = pk.get("topLevelSite") or next(iter(pk.values()), "")
    if pk and not isinstance(pk, str):
        pk = str(pk)
    if pk:
        pw["partitionKey"] = pk

    pw_cookies.append(pw)

with open("/tmp/cookies.json", "w") as f:
    json.dump(pw_cookies, f, indent=2)
```

**Key gotchas:**
- `sameSite` casing: CDP returns `"LAX"`, Playwright expects `"Lax"`. Use the dict lookup.
- `partitionKey` type: CDP returns an object, Playwright expects a string. Extract `topLevelSite`.
- `expires`: Some CDP cookies have `expires: -1` (session-only). These die when the browser closes.
- `httpOnly`: CDP returns this as a boolean; keep it. Playwright accepts it.

## Worked Example: Fundrise Scraper

**Before (Playwright, broken):**
```python
# Required: playwright installed, cookie file at /tmp/fundrise_cookies.json
# Problems: playwright dep not installed in cron python, cookies expired
from playwright.async_api import async_playwright
```

**After (CDP WebSocket, working):**
```python
# Required: only websockets (stdlib-available), browser-scanner Chrome
# Auto-launches browser with profile cookies → reads balance directly
import websockets
from urllib.request import urlopen
# ... full CDP session pattern above
```

File: `~/.hermes/profiles/substrate-hermes/scripts/fundrise_scraper.py`

## Cron Dependencies

Scripts using this pattern need `websockets` available in the running Python. The system Python (`/usr/local/bin/python3`) has it installed (`websockets v15.0.1`).

No other dependencies needed (not even Playwright, unless the script uses Option D's cookie bridge).

## Browser Profile

The browser-scanner Chrome profile at `/Users/ted/Library/Application Support/Browser_Profiles/hermes-browser/` persists cookies for:
- Fundrise (logged in once, session persists)
- Harris Teeter (logged in once)
- Sam's Club (logged in once)
- Provider dashboards (DeepSeek, Claude, OpenRouter, etc.)

Logging into a new site on this profile once enables any cron script to use it.
