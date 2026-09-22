#!/usr/bin/env python3
"""
Harris Teeter Receipt Fetcher — Local Playwright with saved cookies.

Uses a persistent browser session to log in once, then fetches receipt data
on schedule. Saves raw JSON to staging directory.

Run: /Users/ted/.hermes/hermes-agent/venv/bin/python3 /Users/ted/.hermes/scripts/grocery_receipt_fetcher.py
Login: python3 grocery_receipt_fetcher.py --login

Changelog:
  2026-06-29 — Fixed browser-close-while-typing bug (rule 7 in skill).
                 Added aria-label extraction method. Updated price handling.
"""
import asyncio
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERMES_PYTHON = "/Users/ted/.hermes/hermes-agent/venv/bin/python3"
if sys.executable != HERMES_PYTHON and os.path.exists(HERMES_PYTHON):
    os.execv(HERMES_PYTHON, [HERMES_PYTHON] + sys.argv)

from playwright.async_api import async_playwright

STAGING_DIR = Path("/Volumes/Extra/Substrate/Commons/Substrate_Finance_Planning/Evidence/Grocery_Receipt_Staging")
COOKIE_FILE = Path("/tmp/ht_cookies.json")
PROFILE_DIR = "/tmp/ht_session_persist"
BASE_URL = "https://www.harristeeter.com"
PURCHASES_URL = f"{BASE_URL}/mypurchases"


async def fetch_receipts():
    """Fetch all receipt data from Harris Teeter purchase history."""
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
            args=['--disable-blink-features=AutomationControlled'],
            viewport={'width': 1280, 'height': 900}
        )
        page = context.pages[0] if context.pages else await context.new_page()
        
        if COOKIE_FILE.exists():
            with open(COOKIE_FILE) as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)
            print(f"Loaded {len(cookies)} saved cookies")
        
        print("Navigating to purchase history...")
        await page.goto(PURCHASES_URL, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(5)
        
        if 'signin' in page.url or 'login' in page.url:
            print("Cookies expired. Run: python3 grocery_receipt_fetcher.py --login")
            await context.close()
            return None
        
        print("Authenticated")
        
        # Extract orders with item-level detail
        orders = await extract_all_orders(page)
        
        # Save results
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output = {
            "store": "Harris Teeter",
            "fetch_time": datetime.now(timezone.utc).isoformat(),
            "order_count": len(orders),
            "total_spend": sum(o.get('total_float', 0) for o in orders),
            "orders": orders
        }
        
        output_file = STAGING_DIR / f"ht_receipts_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        summary_file = STAGING_DIR / "ht_receipts_latest.json"
        with open(summary_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"Saved {len(orders)} orders (${output['total_spend']:.2f}) to {output_file}")
        await context.close()
        return output


async def extract_all_orders(page):
    """Extract all orders with item-level detail."""
    rows = await page.query_selector_all('[class*="PurchaseListRow"]')
    orders = []
    
    for i, row in enumerate(rows):
        text = await row.inner_text()
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        order_type = None
        date = None
        total = None
        
        for line in lines:
            if line in ('Pickup', 'In-store', 'Delivery', 'Fuel'):
                order_type = line
            elif re.match(r'(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}', line):
                date = line
            elif re.match(r'^\$[\d.]+$', line):
                total = line
        
        if not (date and total):
            continue
        
        print(f"  Order {i+1}: {date} ${total} ({order_type})...")
        
        # Click into order for detail
        await row.click()
        await asyncio.sleep(4)
        
        detail = await extract_order_detail(page)
        
        orders.append({
            "type": order_type,
            "date": date,
            "total": total,
            "total_float": float(total.replace('$', '')),
            **(detail or {})
        })
        
        # Go back to list
        await page.goto(PURCHASES_URL, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(3)
    
    return orders


async def extract_order_detail(page):
    """Extract item-level detail from an order detail page using JS evaluate."""
    try:
        result = await page.evaluate('''() => {
            const items = [];
            const nameEls = document.querySelectorAll('[class*="ProductDescription"]');
            
            for (const el of nameEls) {
                const ariaLabel = el.getAttribute('aria-label') || '';
                const name = ariaLabel.replace(/\\s*title$/, '').trim();
                
                // Walk up to find the card container with prices
                let container = el.parentElement;
                let cardText = '';
                for (let j = 0; j < 6; j++) {
                    if (!container) break;
                    const text = container.innerText;
                    if (text.includes('$') && text.length > 30) {
                        cardText = text;
                        break;
                    }
                    container = container.parentElement;
                }
                
                if (!cardText) continue;
                
                const allPrices = cardText.match(/\\$[\\d.]+/g) || [];
                const promoMatch = cardText.match(/(\\d+ For \\$[\\d.]+)/);
                const sizeMatch = cardText.match(/(\\d+\\s*(oz|OZ|ct|CT|lb|fl oz|pt))/i);
                const weightMatch = cardText.match(/Received:\\s*([\\d.]+)\\s*lbs?/);
                const paidMatch = cardText.match(/Paid:\\s*\\$([\\d.]+)/);
                
                items.push({
                    name,
                    price_display: allPrices[0] || null,
                    original_price: allPrices.length > 1 ? allPrices[allPrices.length - 1] : null,
                    promo: promoMatch ? promoMatch[1] : null,
                    size: sizeMatch ? sizeMatch[1] : null,
                    weight_lb: weightMatch ? parseFloat(weightMatch[1]) : null,
                    paid: paidMatch ? '$' + paidMatch[1] : null
                });
            }
            
            // Extract totals
            const bodyText = document.body.innerText;
            const totalMatch = bodyText.match(/Total:\\s*\\$([\\d.]+)/);
            const savingsMatch = bodyText.match(/\\$([\\d.]+)\\s*Total Savings/);
            const taxMatch = bodyText.match(/Tax\\s*\\$([\\d.]+)/);
            const itemTotalMatch = bodyText.match(/Item Total\\s*\\$([\\d.]+)/);
            const discountMatch = bodyText.match(/Item Coupons/Sales\\s*-\\$([\\d.]+)/);
            
            return {
                items,
                item_count: items.length,
                totals: {
                    total: totalMatch ? '$' + totalMatch[1] : null,
                    item_total: itemTotalMatch ? '$' + itemTotalMatch[1] : null,
                    tax: taxMatch ? '$' + taxMatch[1] : null,
                    savings: savingsMatch ? '$' + savingsMatch[1] : null,
                    discounts: discountMatch ? '-$' + discountMatch[1] : null
                }
            };
        }''')
        
        return result
        
    except Exception as e:
        print(f"    Error: {e}")
        return None


async def login_flow():
    """Open browser for manual login, then save cookies."""
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
            args=['--disable-blink-features=AutomationControlled'],
            viewport={'width': 1280, 'height': 900}
        )
        page = context.pages[0] if context.pages else await context.new_page()
        
        await page.goto(f"{BASE_URL}/signin?redirectUrl=/mypurchases", wait_until="domcontentloaded", timeout=30000)
        
        try:
            await page.wait_for_selector('#signInName', timeout=15000)
            print("Login form loaded")
        except:
            print("Login form not found")
            await context.close()
            return
        
        print("Browser is OPEN. Please log in manually.")
        print("Waiting up to 5 minutes...")
        
        for i in range(150):  # 150 * 2s = 5 min
            await asyncio.sleep(2)
            url = page.url
            if 'harristeeter.com' in url and 'signin' not in url and 'login' not in url and 'connect-auth' not in url:
                print("Login successful!")
                cookies = await context.cookies()
                with open(COOKIE_FILE, 'w') as f:
                    json.dump(cookies, f)
                print(f"Saved {len(cookies)} cookies")
                break
        else:
            print("Login timeout")
        
        await asyncio.sleep(3)
        await context.close()


if __name__ == "__main__":
    if '--login' in sys.argv:
        print("=== Harris Teeter Login ===")
        asyncio.run(login_flow())
    else:
        print("=== Harris Teeter Receipt Fetcher ===")
        result = asyncio.run(fetch_receipts())
        if result is None:
            exit(1)
