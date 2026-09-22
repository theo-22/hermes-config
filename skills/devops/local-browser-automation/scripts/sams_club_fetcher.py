#!/usr/bin/env python3
"""
Sam's Club Receipt Fetcher — Playwright with CDP browser cookies.
https://www.samsclub.com/orders

Quick-fetch: extracts order summaries from the order list page (body text, no SPA clicks).
For item-level detail, use the Print View method (see references/sams-club-order-extraction.md).

Usage:
  python3 sams_club_fetcher.py                    # Fetch order summaries
  python3 sams_club_fetcher.py --login             # Interactive login (rarely needed)

Cron: substrate-hermes profile, Sundays 10:30am, no-agent
Cookies: /tmp/sc_cookies.json (extracted from CDP browser port 9222)
"""
import asyncio, json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path

HERMES_PYTHON = "/Users/ted/.hermes/hermes-agent/venv/bin/python3"
if sys.executable != HERMES_PYTHON and os.path.exists(HERMES_PYTHON):
    os.execv(HERMES_PYTHON, [HERMES_PYTHON] + sys.argv)

from playwright.async_api import async_playwright

STAGING_DIR = Path("/Volumes/Extra/Substrate/Commons/Substrate_Finance_Planning/Evidence/Grocery_Receipt_Staging")
COOKIE_FILE = Path("/tmp/sc_cookies.json")
PROFILE_DIR = "/tmp/sc_session_persist"
ORDERS_URL = "https://www.samsclub.com/orders"


async def fetch_receipts():
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR, headless=False,
            args=['--disable-blink-features=AutomationControlled'],
            viewport={'width': 1280, 'height': 3000})
        page = context.pages[0] if context.pages else await context.new_page()

        if COOKIE_FILE.exists():
            with open(COOKIE_FILE) as f:
                await context.add_cookies(json.load(f))
            print(f"Loaded {len(json.load(open(COOKIE_FILE)))} saved cookies")

        await page.goto(ORDERS_URL, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_selector('h2', timeout=20000)
        await asyncio.sleep(5)

        if any(k in page.url for k in ('signin', 'login', 'auth')):
            print("❌ Not logged in. Run with --login flag.")
            await context.close()
            return None

        print("✅ Authenticated")

        # Extract from body text — Sam's Club SPA renders order data in flat text
        body = await page.evaluate('() => document.body.innerText')
        orders = parse_orders(body)

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output = {"store": "Sam's Club", "fetch_time": datetime.now(timezone.utc).isoformat(),
                  "order_count": len(orders), "orders": orders}
        out = STAGING_DIR / f"sc_receipts_{timestamp}.json"
        with open(out, 'w') as f:
            json.dump(output, f, indent=2)
        with open(STAGING_DIR / "sc_receipts_latest.json", 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\n✅ Saved {len(orders)} orders to {out}")
        for o in orders:
            print(f"   {o.get('order_id','?'):25s} | {o.get('date_raw','no date'):20s} | {str(o.get('items','?')):3s} items")
        await context.close()
        return output


def parse_orders(text):
    """Parse Sam's Club order list from flat body text.
    
    Format per order:
        Order NNNN-NNNN-NNNN-NNN
        Picked up on Jun 27          ← abbreviated month!
        Asheville Sam's Club at ...
        20 items
    No dollar totals on the list page — totals only in order detail / print view.
    """
    orders = []
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    current = None
    months_pat = r'(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'

    for line in lines:
        m = re.match(r'^Order\s+([\d-]+)', line)
        if m:
            if current: orders.append(current)
            current = {'order_id': m.group(1), 'items': None, 'date_raw': None, 'location': None}
            continue
        if not current: continue

        m = re.match(rf'(?:Picked up|Delivered|Ordered|Placed)\s+on\s+{months_pat}\s+(\d{{1,2}})', line, re.I)
        if m:
            current['date_raw'] = m.group(0)
            continue

        m = re.match(r'^(\d+)\s*items?$', line, re.I)
        if m: current['items'] = int(m.group(1)); continue

        if 'sams club' in line.lower() or 'club at' in line.lower():
            current['location'] = line

    if current: orders.append(current)
    return orders


async def login_flow():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR, headless=False,
            args=['--disable-blink-features=AutomationControlled'],
            viewport={'width': 1280, 'height': 900})
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto(f"https://www.samsclub.com/account/auth/login", wait_until="domcontentloaded", timeout=30000)
        print("✅ Login form loaded\n🔓 Browser is OPEN. Please log in manually.\n⏳ Waiting up to 5 minutes...")
        for _ in range(150):
            await asyncio.sleep(2)
            if 'samsclub.com' in page.url and 'login' not in page.url and 'auth' not in page.url:
                cookies = await context.cookies()
                with open(COOKIE_FILE, 'w') as f: json.dump(cookies, f)
                print(f"✅ Saved {len(cookies)} cookies"); break
        else: print("⏰ Timeout")
        await asyncio.sleep(3); await context.close()


if __name__ == "__main__":
    if '--login' in sys.argv:
        print("=== Sam's Club Login ==="); asyncio.run(login_flow())
    else:
        print("=== Sam's Club Receipt Fetcher ===")
        r = asyncio.run(fetch_receipts())
        if r is None: exit(1)
