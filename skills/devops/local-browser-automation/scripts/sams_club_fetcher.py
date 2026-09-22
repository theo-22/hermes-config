#!/usr/bin/env python3
"""
Sam's Club Receipt Fetcher — CDP-based (shared browser at port 9223).

Connects to the existing CDP browser (port 9223), navigates to
Sam's Club orders page, and extracts all order/receipt data into
structured JSON.

Usage:
  python3 sams_club_fetcher.py                    # Fetch receipts (requires session in CDP browser)
  python3 sams_club_fetcher.py --login             # Interactive login (opens CDP browser)

Output: /Volumes/Extra/Substrate/Commons/Substrate_Finance_Planning/Evidence/Grocery_Receipt_Staging/
"""
import asyncio
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from substrate_root import resolve_substrate_path, substrate_root
from urllib.request import urlopen
import websockets

HERMES_PYTHON = "/Users/ted/.hermes/hermes-agent/venv/bin/python3"
if sys.executable != HERMES_PYTHON and os.path.exists(HERMES_PYTHON):
    os.execv(HERMES_PYTHON, [HERMES_PYTHON] + sys.argv)

STAGING_DIR = resolve_substrate_path('Commons/Substrate_Finance_Planning/Evidence/Grocery_Receipt_Staging')  # <!-- alias-ok: relative arg to the SUBSTRATE_ROOT resolver (#324/#723), not a hardcoded path -->
COOKIE_FILE = Path("/tmp/sc_cookies.json")
BASE_URL = "https://www.samsclub.com"
ORDERS_URL = f"{BASE_URL}/orders"
LOGIN_URL = f"{BASE_URL}/account/auth/login"
CDP_URL = "http://127.0.0.1:9223"


async def get_cdp_ws_url():
    """Get the WebSocket debugger URL from CDP, preferring an existing SC tab."""
    try:
        tabs = json.loads(urlopen(f"{CDP_URL}/json", timeout=10).read())
        # Prefer an existing Sam's Club tab to re-use session
        sc_tab = [t for t in tabs if t.get("type") == "page" and "samsclub.com" in t.get("url", "")]
        if sc_tab:
            print(f"  Using existing SC tab: {sc_tab[0].get('title', '')[:60]}")
            return sc_tab[0]["webSocketDebuggerUrl"]
        # Fall back to any page tab
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
        # Swallow events (non-matching responses)
        if "method" in data:
            continue


async def js_eval(ws, expression):
    """Evaluate JS in the page and return the result value (or None)."""
    result = await cdp_call(ws, "Runtime.evaluate", {
        "expression": expression,
        "returnByValue": True,
        "timeout": 15000
    })
    return result.get("result", {}).get("result", {}).get("value")


async def fetch_receipts():
    """Fetch all receipt data from Sam's Club purchase history via CDP."""
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

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
        # Navigate to orders page
        print("  Navigating to purchase history...")
        nav_result = await cdp_call(ws, "Page.navigate", {"url": ORDERS_URL})
        loader_id = nav_result.get("result", {}).get("loaderId")
        if not loader_id:
            print("  ⚠️ Navigation may not have completed")
        await asyncio.sleep(5)

        # Check login redirect
        current_url = await js_eval(ws, "document.location.href")
        if not current_url:
            current_url = ""
        print(f"  Current URL: {current_url}")

        if 'signin' in current_url or 'login' in current_url or 'auth' in current_url:
            print("🔓 Session expired — please log in at samsclub.com in the CDP browser")
            print("   Then re-run this script.")
            return None

        # Wait for orders content to load (SPA loads dynamically). Poll for the
        # "See details" buttons rather than a fixed sleep + generic 'h2' check —
        # the account-nav sidebar (Order/Membership/Services/...) renders its own
        # h2 tags immediately, before the actual order list has loaded, so a bare
        # h2 count is not a reliable readiness signal and produced a false
        # PAGE_STRUCTURE_ERROR under normal (just slower-than-3s) page loads.
        # This selector is also what extract_order_detail() clicks later, so
        # passing here guarantees the thing the rest of the script needs exists.
        orders_found = False
        for _ in range(10):
            count = await js_eval(
                ws,
                "document.querySelectorAll("
                "'button[aria-label*=\"View details for order number\"]').length"
            )
            if count:
                orders_found = True
                break
            await asyncio.sleep(2)

        if not orders_found:
            print("PAGE_STRUCTURE_ERROR: orders page loaded (logged in) but expected content "
                  "never appeared — site layout may have changed")
            return None

        print("✅ Authenticated")

        # Extract ALL order data from body text (Sam's Club SPA renders in flat text)
        body_text = await js_eval(ws, "document.body.innerText")
        if not body_text:
            print("❌ Could not extract page text")
            return None

        order_list = parse_orders_from_text(body_text)
        print(f"Found {len(order_list)} orders")

        # Item-level detail — click into each order
        for i, order in enumerate(order_list):
            print(f"  Order {i+1}/{len(order_list)}: {order.get('order_id','?')} ({order.get('date_raw','?')})...")
            detail = await extract_order_detail(ws, i)
            if detail:
                order.update(detail)
                print(f"    ✅ {detail.get('item_count', 0)} items, total={detail.get('total')}")
            else:
                print(f"    ⚠️ Failed to extract detail (list-level data kept)")

        # Save results
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output = {
            "store": "Sam's Club",
            "fetch_time": datetime.now(timezone.utc).isoformat(),
            "order_count": len(order_list),
            "total_spend": sum(o.get('total_float', 0) for o in order_list if o.get('total_float')),
            "orders": order_list
        }

        output_file = STAGING_DIR / f"sc_receipts_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        summary_file = STAGING_DIR / "sc_receipts_latest.json"
        with open(summary_file, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\n✅ Saved {len(order_list)} orders to {output_file}")
        if output['total_spend']:
            print(f"   Total: ${output['total_spend']:.2f}")
        for o in order_list:
            date = o.get('date_raw', 'no date') or 'no date'
            items = str(o.get('items', '?')) if o.get('items') is not None else '?'
            total = str(o.get('total', '?')) or '?'
            print(f"   {o.get('order_id','?'):25s} | {date:15s} | {items:3s} items | {total}")

        return output


def parse_orders_from_text(text):
    """Parse order data from Sam's Club body text.

    Format:
        Order NNNN-NNNN-NNNN-NNN
        Picked up on May 16
        Asheville Sam's Club at 645 PATTON AVE
        20 items
    """
    orders = []
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    current = None

    for line in lines:
        order_match = re.match(r'^Order\s+([\d-]+)', line)
        if order_match:
            if current:
                orders.append(current)
            current = {'order_id': order_match.group(1), 'items': None, 'total': None,
                       'total_float': None, 'date': None, 'location': None}
            continue
        if not current:
            continue

        # "Picked up on May 16" or "Picked up on Jun 27" (abbreviated months)
        date_match = re.match(
            r'(?:Picked up|Delivered|Ordered|Placed)\s+on\s+'
            r'(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
            r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|'
            r'Dec(?:ember)?)\s+(\d{1,2})', line, re.I)
        if date_match:
            current['date_raw'] = date_match.group(0)
            current['date_month'] = date_match.group(1)
            current['date_day'] = int(date_match.group(2))
            continue

        # "N items"
        item_match = re.match(r'^(\d+)\s*items?$', line, re.I)
        if item_match:
            current['items'] = int(item_match.group(1))
            continue

        # Location (e.g. "Asheville Sam's Club at 645 PATTON AVE")
        if 'sams club' in line.lower() or 'club at' in line.lower():
            current['location'] = line
            continue

    if current:
        orders.append(current)
    return orders


async def extract_order_detail(ws, order_index):
    """Click into an order's detail page and extract item-level rows + fees
    using CDP Runtime.evaluate.

    DOM structure per order item:
        .print-item-title  (visible) — product name, size, unit price
        .print-items-list  (hidden)  — status, qty, price per item

    Both are indexed in order on the page; they pair up by index.
    """
    try:
        # Click the "See details" button for this order via JS
        click_js = f"""
        (function() {{
            const buttons = document.querySelectorAll(
                'button[aria-label*="View details for order number"]'
            );
            if (buttons[{order_index}]) {{
                buttons[{order_index}].click();
                return true;
            }}
            return false;
        }})()
        """
        clicked = await js_eval(ws, click_js)
        if not clicked:
            print(f"    Could not find 'See details' button #{order_index}")
            return None

        # Wait for detail page to load (SPA navigation)
        await asyncio.sleep(6)

        # Extract item details via JS
        extract_js = """(function() {
            const titles = document.querySelectorAll('.print-item-title');
            const detailRows = document.querySelectorAll('.print-items-list');
            const items = [];
            const count = Math.min(titles.length, detailRows.length);
            for (let i = 0; i < count; i++) {
                const nameLine = titles[i].textContent.trim();
                const typeEl = detailRows[i].querySelector('.print-bill-type');
                const qtyEl = detailRows[i].querySelector('.print-bill-qty');
                const priceEl = detailRows[i].querySelector('.print-bill-price');
                const priceText = priceEl ? priceEl.textContent.trim() : '';
                // weight-based items (lamb chops, chicken wings) have
                // concatenated prices: "$12.52$21.95$21.95" = unit$weight$total
                const priceMatches = priceText.match(/\\$(\\d+\\.\\d{2})/g);
                const totalPrice = priceMatches ? priceMatches[priceMatches.length - 1] : null;
                const qtyText = qtyEl ? qtyEl.textContent.trim() : '';
                const qtyMatch = qtyText.match(/Qty\\s+(\\d+)/);
                items.push({
                    name: nameLine,
                    status: typeEl ? typeEl.textContent.trim() : '?',
                    qty: qtyMatch ? parseInt(qtyMatch[1], 10) : null,
                    price: totalPrice ? parseFloat(totalPrice.replace('$', '')) : null,
                    price_raw: priceText
                });
            }
            const feeEls = document.querySelectorAll('.print-fees-item');
            const fees = [];
            feeEls.forEach(f => {
                const text = f.textContent.trim();
                const m = text.match(/\\$(\\d+\\.\\d{2})/);
                fees.push({label: text.replace(/\\$\\d+\\.\\d{2}/g, '').trim(), amount: m ? parseFloat(m[1]) : 0.0});
            });
            // Subtotal and total from the payment section
            const allText = document.body.innerText;
            const subtotalMatch = allText.match(/Subtotal\\$(\\d+\\.\\d{2})/);
            const totalMatch = allText.match(/Total\\$(\\d+\\.\\d{2})/);
            return {
                items: items,
                item_count: items.length,
                fees: fees,
                subtotal: subtotalMatch ? parseFloat(subtotalMatch[1]) : null,
                total: totalMatch ? parseFloat(totalMatch[1]) : null
            };
        })()"""

        result_raw = await cdp_call(ws, "Runtime.evaluate", {
            "expression": extract_js,
            "returnByValue": True,
            "timeout": 15000
        })
        result = result_raw.get("result", {}).get("result", {}).get("value")

        if not result:
            print("    Extract returned null — detail page may have different layout")
            # Still navigate back to orders list
            await cdp_call(ws, "Page.navigate", {"url": ORDERS_URL})
            await asyncio.sleep(5)
            return None

        item_subtotal = sum(it['price'] for it in result['items'] if it.get('price') is not None)
        fee_total = sum(f['amount'] for f in result['fees'] if f['amount'])
        calc_total = round(item_subtotal + fee_total, 2) if result['items'] else None

        result['item_subtotal'] = round(item_subtotal, 2)
        result['fee_total'] = round(fee_total, 2)
        # Prefer DOM's authoritative total; fall back to calculated
        if result['total'] is None:
            result['total'] = calc_total
        result['total_float'] = result['total']
        result['calc_total'] = calc_total

        # Navigate back to orders list for next detail click
        await cdp_call(ws, "Page.navigate", {"url": ORDERS_URL})

        # Wait for orders page to render
        await asyncio.sleep(3)
        for attempt in range(5):
            h2_found = await js_eval(ws, "document.querySelector('h2') !== null")
            if h2_found:
                break
            await asyncio.sleep(2)
        await asyncio.sleep(3)

        return result

    except Exception as exc:
        print(f"    Error extracting detail: {exc}")
        try:
            await cdp_call(ws, "Page.navigate", {"url": ORDERS_URL})
            await asyncio.sleep(5)
        except Exception:
            pass
        return None


async def login_flow():
    """Open CDP browser tab for manual login, then save cookies."""
    ws_url = await get_cdp_ws_url()
    if not ws_url:
        print("❌ No CDP browser available. Start Chrome with:")
        print("   /Volumes/Extra/Apps/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome \\")
        print("     --remote-debugging-port=9223 \\")
        print('     --user-data-dir="/Users/ted/Library/Application Support/Google/Chrome/Cost Tabs" \\')
        print('     --profile-directory="Default" \\')
        print("     --no-first-run")
        return

    async with websockets.connect(ws_url) as ws:
        nav_result = await cdp_call(ws, "Page.navigate", {"url": LOGIN_URL})
        loader_id = nav_result.get("result", {}).get("loaderId")
        if not loader_id:
            print("  ⚠️ Navigation may not have completed")
        await asyncio.sleep(4)

        print("✅ Login form loaded")
        print("🔓 Browser is OPEN. Please log in manually.")
        print("⏳ Waiting up to 5 minutes...")

        for i in range(150):
            await asyncio.sleep(2)
            current_url = await js_eval(ws, "document.location.href")
            if not current_url:
                current_url = ""
            if 'samsclub.com' in current_url and 'login' not in current_url and 'auth' not in current_url:
                print("✅ Login successful! Saving cookies...")
                # Extract cookies via CDP
                cookie_result = await cdp_call(ws, "Network.getAllCookies", {})
                cookies = cookie_result.get("result", {}).get("cookies", [])
                with open(COOKIE_FILE, 'w') as f:
                    json.dump(cookies, f)
                print(f"✅ Saved {len(cookies)} cookies")
                break
        else:
            print("⏰ Timeout")

        await asyncio.sleep(3)


async def main():
    if '--login' in sys.argv:
        print("=== Sam's Club Login (CDP) ===")
        await login_flow()
    else:
        print("=== Sam's Club Receipt Fetcher (CDP) ===")
        result = await fetch_receipts()
        if result is None:
            exit(0)  # CDP unavailable (Chrome down/not debug-enabled) — clean skip


if __name__ == "__main__":
    result = asyncio.run(main())
