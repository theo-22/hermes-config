#!/usr/bin/env python3
"""
Harris Teeter Receipt Fetcher — CDP-based scraper.

Connects to the existing CDP browser (port 9223), navigates to
Harris Teeter purchase history, and extracts receipt data with
item-level detail. Uses CDP Runtime.evaluate for DOM queries and
Input.dispatchMouseEvent for clicks (React SPA compatible).

Writes structured JSON to staging directory.

Usage:
  python3 grocery_receipt_fetcher.py
  python3 grocery_receipt_fetcher.py --login
"""

import asyncio
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
import websockets


STAGING_DIR = Path("/Volumes/Extra/Substrate/Commons/Substrate_Finance_Planning/Evidence/Grocery_Receipt_Staging")
COOKIE_FILE = Path("/tmp/ht_cookies.json")
BASE_URL = "https://www.harristeeter.com"
PURCHASES_URL = f"{BASE_URL}/mypurchases"
CDP_URL = "http://127.0.0.1:9223"

HERMES_PYTHON = "/Users/ted/.hermes/hermes-agent/venv/bin/python3"
if sys.executable != HERMES_PYTHON and os.path.exists(HERMES_PYTHON):
    os.execv(HERMES_PYTHON, [HERMES_PYTHON] + sys.argv)


# ---------------------------------------------------------------------------
# CDP connection helpers
# ---------------------------------------------------------------------------

async def get_cdp_ws_url():
    """Get the WebSocket debugger URL from CDP, preferring an HT tab."""
    try:
        tabs = json.loads(urlopen(f"{CDP_URL}/json", timeout=10).read())
        ht_tab = [t for t in tabs if t.get("type") == "page" and "harristeeter.com" in t.get("url", "")]
        if ht_tab:
            print(f"  Using existing HT tab: {ht_tab[0].get('title', '')[:60]}")
            return ht_tab[0]["webSocketDebuggerUrl"]
        pages = [t for t in tabs if t.get("type") == "page"]
        if pages:
            return pages[0]["webSocketDebuggerUrl"]
        return None
    except Exception as e:
        print(f"  CDP connection failed: {e}")
        return None


async def cdp_call(ws, method, params=None):
    """Send a CDP command and wait for the matching response."""
    msg_id = int(time.time() * 1000) % 100000
    payload = json.dumps({"id": msg_id, "method": method, "params": params or {}})
    await ws.send(payload)
    while True:
        raw = await ws.recv()
        data = json.loads(raw)
        if data.get("id") == msg_id:
            return data
        if "method" in data:
            continue


async def cdp_eval(ws, js):
    """Evaluate JavaScript in the page context and return the result value."""
    result = await cdp_call(ws, "Runtime.evaluate", {
        "expression": js,
        "returnByValue": True,
        "timeout": 15000
    })
    return result.get("result", {}).get("result", {}).get("value")


async def cdp_get_url(ws):
    """Get current page URL."""
    return await cdp_eval(ws, "document.location.href") or ""


# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------

async def prime_ht_session_via_cdp():
    """Reload the Harris Teeter tab in the CDP browser and give it a chance to
    self-auth before we copy cookies out.

    Returns True if logged in, False if on sign-in page, None if CDP unavailable.
    """
    try:
        urlopen(f"{CDP_URL}/json/version", timeout=3)
    except Exception:
        return None
    try:
        ws_url = await get_cdp_ws_url()
        if not ws_url:
            return None
        async with websockets.connect(ws_url) as ws:
            await cdp_call(ws, "Page.navigate", {"url": PURCHASES_URL})
            await asyncio.sleep(7)
            url = await cdp_get_url(ws)
            return not any(k in url for k in ("signin", "login", "connect-auth"))
    except Exception as e:
        print(f"[ht] session prime skipped ({e})")
        return None


async def refresh_cookies_from_cdp():
    """Extract cookies from the CDP browser if cookies are missing or stale."""
    if COOKIE_FILE.exists():
        age = time.time() - COOKIE_FILE.stat().st_mtime
        if age < 21600:  # 6 hours
            return True
    try:
        urlopen(f"{CDP_URL}/json/version", timeout=3)
    except Exception:
        print("Starting browser for cookie refresh...")
        import subprocess
        subprocess.Popen(
            ["/Volumes/Extra/Apps/Google Chrome.app/Contents/MacOS/Google Chrome",
             "--remote-debugging-port=9223",
             "--user-data-dir=/Users/ted/Library/Application Support/Google/Chrome/Cost Tabs",
             "--profile-directory=Default",  # 615 agent identity (Ted, 2026-09-22)
             "--no-first-run"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        await asyncio.sleep(5)

    try:
        ws_url = await get_cdp_ws_url()
        if not ws_url:
            return False
        async with websockets.connect(ws_url) as ws:
            r = await cdp_call(ws, "Network.getAllCookies")
            cookies = r.get("result", {}).get("cookies", [])
            pw_cookies = []
            for c in cookies:
                pw = {"name": c["name"], "value": c["value"],
                       "domain": c.get("domain", ""), "path": c.get("path", "/"),
                       "httpOnly": c.get("httpOnly", False), "secure": c.get("secure", False),
                       "sameSite": c.get("sameSite", "Lax")}
                pk = c.get("partitionKey")
                if isinstance(pk, dict):
                    pk = pk.get("topLevelSite") or next(iter(pk.values()), None)
                if pk and not isinstance(pk, str):
                    pk = str(pk)
                if pk:
                    pw["partitionKey"] = pk
                if c.get("expires") and c["expires"] > 0:
                    pw["expires"] = c["expires"]
                pw_cookies.append(pw)
            with open(COOKIE_FILE, "w") as f:
                json.dump(pw_cookies, f, indent=2)
            print(f"Refreshed {len(pw_cookies)} cookies from CDP browser")
        return True
    except Exception as e:
        print(f"Cookie refresh failed ({e})")
        return False


# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------

async def extract_order_list(ws):
    """Extract order summaries from the purchase history list page."""
    js = """
    (function() {
        const rows = document.querySelectorAll('[class*="PurchaseListRow"]');
        const orders = [];
        for (const row of rows) {
            const text = row.innerText;
            const lines = text.split('\\n').map(function(l) { return l.trim(); }).filter(function(l) { return l; });
            var order_type = null;
            var date = null;
            var total = null;
            for (var li = 0; li < lines.length; li++) {
                var line = lines[li];
                if (['Pickup', 'In-store', 'Delivery', 'Fuel'].indexOf(line) !== -1) {
                    order_type = line;
                } else if (/^[A-Z][a-z]+\.? \d{1,2}, \d{4}$/.test(line)) {
                    date = line;
                } else if (/^\$[\d.]+$/.test(line)) {
                    total = line;
                }
            }
            if (date && total) {
                orders.push({
                    type: order_type,
                    date: date,
                    total: total,
                    total_float: parseFloat(total.replace('$', ''))
                });
            }
        }
        return orders;
    })()
    """
    return await cdp_eval(ws, js) or []


async def get_element_center(ws, css_selector, index=0):
    """Get the center coordinates of an element matching a CSS selector,
    using the :nth-of-type-like approach for indexed elements."""
    js = """
    (function() {
        var rows = document.querySelectorAll('%s');
        if (rows.length <= %d) return null;
        var el = rows[%d];
        var rect = el.getBoundingClientRect();
        return {
            x: rect.left + rect.width / 2,
            y: rect.top + rect.height / 2,
            width: rect.width,
            height: rect.height
        };
    })()
    """ % (css_selector.replace("'", "\\'"), index, index)
    return await cdp_eval(ws, js)


async def cdp_mouse_click(ws, x, y):
    """Dispatch a trusted mouse click at (x, y) using CDP Input.dispatchMouseEvent.
    This produces a genuine browser-level click that React SPAs can detect."""
    await cdp_call(ws, "Input.dispatchMouseEvent", {
        "type": "mousePressed",
        "x": x,
        "y": y,
        "button": "left",
        "clickCount": 1
    })
    await cdp_call(ws, "Input.dispatchMouseEvent", {
        "type": "mouseReleased",
        "x": x,
        "y": y,
        "button": "left",
        "clickCount": 1
    })


async def click_order_row(ws, order_index):
    """Click on an order row by index using a DOM .click().

    Verified 2026-08-09: CDP Input.dispatchMouseEvent at the row center was
    NOT triggering the React row onClick for most orders (6 of 8 in a live
    run), leaving the scraper on the list page with 0 items. A native DOM
    .click() on the row reliably opens the detail view (verified live against
    harristeeter.com/mypurchases)."""
    result = await cdp_eval(ws, """
    (function() {
        var rows = document.querySelectorAll('[class*="PurchaseListRow"]');
        if (rows.length === 0) return false;
        var idx = %d;
        if (idx >= rows.length) return false;
        rows[idx].click();
        return true;
    })()
    """ % order_index)
    return bool(result)


async def extract_order_detail_via_eval(ws):
    """Extract item-level details from the currently visible order detail panel.

    Verified 2026-08-09 against harristeeter.com/mypurchases/detail/*: the site
    no longer renders product names in `[class*="ProductDescription"]` elements.
    Names now live in the `alt` attribute of product images inside
    `[class*="ListStyleProductCard--image"]`, with size/weight/paid/original
    prices in the card's parent text (e.g. "Received: 2.54 lbs Paid: $7.59
    Discounted From $15.21")."""
    js = """
    (function() {
        var items = [];
        var imgs = document.querySelectorAll('[class*="ListStyleProductCard--image"] img');
        for (var ei = 0; ei < imgs.length; ei++) {
            var name = (imgs[ei].getAttribute('alt') || '').trim();
            // HT renders a fallback alt ("No Description Found") for some
            // products and occasionally prefixes names with stray chars.
            var needFallback = (!name || name === 'No Description Found');
            var container = imgs[ei].parentElement;
            var cardText = '';
            for (var j = 0; j < 5; j++) {
                if (!container) break;
                var text = container.innerText;
                if (text.indexOf('Paid:') !== -1) {
                    cardText = text;
                    break;
                }
                container = container.parentElement;
            }
            if (!cardText) continue;
            if (needFallback) {
                var firstLine = cardText.split('\\n')[0].trim();
                if (firstLine && firstLine.indexOf('$') === -1) name = firstLine;
            }
            name = name.replace(/^[)\s]+/, '').trim();
            if (!name) continue;
            var allPrices = cardText.match(/\\$[\\d.]+/g) || [];
            var promoMatch = cardText.match(/(\\d+ For \\$[\\d.]+)/);
            var sizeMatch = cardText.match(/(\\d+\\s*(oz|OZ|ct|CT|lb|fl oz))/i);
            var weightMatch = cardText.match(/Received:\\s*([\\d.]+)\\s*lbs?/);
            items.push({
                name: name,
                price_display: allPrices[0] || null,
                original_price: allPrices.length > 1 ? allPrices[allPrices.length - 1] : null,
                promo: promoMatch ? promoMatch[1] : null,
                size: sizeMatch ? sizeMatch[1] : null,
                weight_lb: weightMatch ? parseFloat(weightMatch[1]) : null
            });
        }
        var bodyText = document.body.innerText;
        var totalMatch = bodyText.match(/Total:\\s*\\$([\\d.]+)/);
        var savingsMatch = bodyText.match(/\\$([\\d.]+)\\s*Total Savings/);
        var taxMatch = bodyText.match(/Tax\\s*\\$([\\d.]+)/);
        var itemTotalMatch = bodyText.match(/Item Total\\s*\\$([\\d.]+)/);
        return {
            items: items,
            item_count: items.length,
            totals: {
                total: totalMatch ? '$' + totalMatch[1] : null,
                item_total: itemTotalMatch ? '$' + itemTotalMatch[1] : null,
                tax: taxMatch ? '$' + taxMatch[1] : null,
                savings: savingsMatch ? '$' + savingsMatch[1] : null
            }
        };
    })()
    """
    return await cdp_eval(ws, js)


async def wait_for_detail_stable(ws, timeout=25):
    """Wait until the order-detail product-card count settles.

    The detail page lazy-renders product cards; a fixed sleep either grabs a
    partial list (missed items) or wastes time. Poll the card count every 1s,
    return when it is stable (>0 and unchanged for 2 consecutive samples) or
    the timeout expires. Returns the settled count (0 if never populated)."""
    prev = None
    stable_streak = 0
    for _ in range(timeout):
        n = await cdp_eval(ws, """
        (function() {
            return document.querySelectorAll('[class*="ListStyleProductCard--image"] img').length;
        })()
        """)
        n = int(n or 0)
        if n > 0 and n == prev:
            stable_streak += 1
            if stable_streak >= 2:
                return n
        else:
            stable_streak = 0
        prev = n
        await asyncio.sleep(1)
    return prev or 0


async def wait_for_detail_url(ws, timeout=10):
    """Wait until the page URL contains /detail/ (SPA navigation happened)."""
    for _ in range(timeout):
        url = await cdp_get_url(ws)
        if "/detail/" in url:
            return True
        await asyncio.sleep(1)
    return False


async def open_order_detail(ws, order_index, click_retries=2):
    """Click an order row and verify the SPA navigated to the detail page.

    The DOM .click() can land before the list finishes rendering, leaving the
    page on /mypurchases with no product cards. Return the URL once /detail/ is
    confirmed; retry the click if navigation didn't happen."""
    for attempt in range(click_retries + 1):
        clicked = await click_order_row(ws, order_index)
        if clicked and await wait_for_detail_url(ws):
            return True
        # navigation didn't happen — navigate back to the list and retry
        await cdp_call(ws, "Page.navigate", {"url": PURCHASES_URL})
        await asyncio.sleep(4)
    return False


# ---------------------------------------------------------------------------
# Main fetch flow
# ---------------------------------------------------------------------------

async def fetch_receipts():
    """Fetch all receipt data from Harris Teeter purchase history via CDP."""
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    # Give the CDP browser's HT session a chance to self-auth
    primed = await prime_ht_session_via_cdp()
    if primed is False:
        print("⚠️ Harris Teeter is parked on a sign-in page in the browser — "
              "open the HT tab and log in once; skipping this run.")
        return None

    # Refresh cookies from CDP browser if needed
    await refresh_cookies_from_cdp()

    ws_url = await get_cdp_ws_url()
    if not ws_url:
        print("❌ No CDP browser available. Start Chrome with:")
        print("   /Volumes/Extra/Apps/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome \\")
        print("     --remote-debugging-port=9223 \\")
        print('     --user-data-dir="/Users/ted/Library/Application Support/Google/Chrome/Cost Tabs" \\')
        print('     --profile-directory="Default" \\')
        print("     --no-first-run")
        return None

    async with websockets.connect(ws_url) as ws:
        # Navigate to purchase history
        print(f"Navigating to: {PURCHASES_URL}")
        await cdp_call(ws, "Page.navigate", {"url": PURCHASES_URL})
        await asyncio.sleep(7)

        # Check login status
        url = await cdp_get_url(ws)
        if "signin" in url or "login" in url:
            print("🔓 Session expired — need to log in.")
            print("   Log in manually at https://www.harristeeter.com/signin")
            # Retry navigation after a fresh login attempt
            await cdp_call(ws, "Page.navigate", {"url": PURCHASES_URL})
            await asyncio.sleep(7)
            url = await cdp_get_url(ws)
            if "signin" in url or "login" in url:
                print("❌ Still not logged in after refresh.")
                return None

        print("✅ Authenticated")

        # Extract order summaries from the list page
        orders = await extract_order_list(ws)
        if not orders:
            print("Found 0 orders — the page structure may have changed or no purchase history.")
        else:
            print(f"Found {len(orders)} orders")

        # For each order, click and extract detail
        detailed_orders = []
        for i, order in enumerate(orders):
            print(f"  Order {i+1}/{len(orders)}: {order['date']} ${order['total']} ({order['type']})...")

            # Navigate back to the list first to ensure fresh state
            # (the detail panel can overlay the list, so reload between orders)
            if i > 0:
                await cdp_call(ws, "Page.navigate", {"url": PURCHASES_URL})
                await asyncio.sleep(5)

            # Open the order detail with navigation verification + retry
            # (DOM click + URL check + stable card wait: fixes missed-item races)
            opened = await open_order_detail(ws, i)
            if not opened:
                print(f"    ⚠️ Could not open order row {i} (navigation failed)")
                detailed_orders.append(order)
                continue

            # Wait for the detail page's product cards to finish lazy-rendering
            card_count = await wait_for_detail_stable(ws)
            if card_count == 0:
                print(f"    ⚠️ Detail page never populated product cards")

            # Extract detail from the now-open panel
            detail = await extract_order_detail_via_eval(ws)
            if detail:
                order.update(detail)
                detailed_orders.append(order)
                print(f"    ✅ {detail.get('item_count', 0)} items, "
                      f"savings={detail.get('totals', {}).get('savings', '?')}")
            else:
                print(f"    ⚠️ Failed to extract detail")
                detailed_orders.append(order)

        # Save results
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output = {
            "store": "Harris Teeter",
            "fetch_time": datetime.now(timezone.utc).isoformat(),
            "order_count": len(detailed_orders),
            "total_spend": sum(o.get('total_float', 0) for o in detailed_orders),
            "orders": detailed_orders
        }

        output_file = STAGING_DIR / f"ht_receipts_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        summary_file = STAGING_DIR / "ht_receipts_latest.json"
        with open(summary_file, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\n✅ Saved {len(detailed_orders)} orders (${output['total_spend']:.2f} total) to {output_file}")

    return output


# ---------------------------------------------------------------------------
# Login flow
# ---------------------------------------------------------------------------

async def login_flow():
    """Open CDP browser tab for manual login, then save cookies."""
    try:
        urlopen(f"{CDP_URL}/json/version", timeout=3)
    except Exception:
        print("Starting browser for login...")
        import subprocess
        subprocess.Popen(
            ["/Volumes/Extra/Apps/Google Chrome.app/Contents/MacOS/Google Chrome",
             "--remote-debugging-port=9223",
             "--user-data-dir=/Users/ted/Library/Application Support/Google/Chrome/Cost Tabs",
             "--profile-directory=Default",  # 615 agent identity (Ted, 2026-09-22)
             "--no-first-run"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        await asyncio.sleep(5)

    ws_url = await get_cdp_ws_url()
    if not ws_url:
        print("❌ Could not connect to CDP browser")
        return

    async with websockets.connect(ws_url) as ws:
        # Open sign-in page
        login_url = f"{BASE_URL}/signin?redirectUrl=/mypurchases"
        print(f"Navigating to login page: {login_url}")
        await cdp_call(ws, "Page.navigate", {"url": login_url})
        await asyncio.sleep(4)

        print("🔓 Browser tab is OPEN. Please log in manually.")
        print("⏳ Waiting up to 5 minutes...")

        for _ in range(150):
            await asyncio.sleep(2)
            url = await cdp_get_url(ws)
            if "harristeeter.com" in url and not any(k in url for k in ("signin", "login", "connect-auth")):
                print("✅ Login successful!")
                # Save cookies
                r = await cdp_call(ws, "Network.getAllCookies")
                cookies = r.get("result", {}).get("cookies", [])
                pw_cookies = []
                for c in cookies:
                    pw = {"name": c["name"], "value": c["value"],
                           "domain": c.get("domain", ""), "path": c.get("path", "/"),
                           "httpOnly": c.get("httpOnly", False), "secure": c.get("secure", False),
                           "sameSite": c.get("sameSite", "Lax")}
                    pk = c.get("partitionKey")
                    if isinstance(pk, dict):
                        pk = pk.get("topLevelSite") or next(iter(pk.values()), None)
                    if pk and not isinstance(pk, str):
                        pk = str(pk)
                    if pk:
                        pw["partitionKey"] = pk
                    if c.get("expires") and c["expires"] > 0:
                        pw["expires"] = c["expires"]
                    pw_cookies.append(pw)
                with open(COOKIE_FILE, 'w') as f:
                    json.dump(pw_cookies, f, indent=2)
                print(f"✅ Saved {len(pw_cookies)} cookies")
                break
        else:
            print("⏰ Timeout waiting for manual login")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if '--login' in sys.argv:
        print("=== Harris Teeter Login ===")
        asyncio.run(login_flow())
    else:
        print("=== Harris Teeter Receipt Fetcher === ")
        result = asyncio.run(fetch_receipts())
        if result is None:
            exit(0)  # CDP unavailable (Chrome down/not debug-enabled) — clean skip
