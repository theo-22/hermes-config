#!/usr/bin/env python3
"""
Harris Teeter Weekly Sales / Weekly Ad Deals Fetcher.

Connects to the existing CDP browser (port 9223), navigates to
the HT Weekly Ad page, and extracts all deal listings into structured JSON.

Output: /Volumes/Extra/Substrate/Commons/Substrate_Finance_Planning/Evidence/Grocery_Receipt_Staging/

Usage:
  python3 ht_weekly_sales_fetcher.py
  python3 ht_weekly_sales_fetcher.py --weekly-ad   # same as default
  python3 ht_weekly_sales_fetcher.py --my-specials  # try personalized deals
"""
import asyncio
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen
import websockets


STAGING_DIR = Path("/Volumes/Extra/Substrate/Commons/Substrate_Finance_Planning/Evidence/Grocery_Receipt_Staging")
BASE_URL = "https://www.harristeeter.com"
WEEKLY_AD_URL = f"{BASE_URL}/specials/weeklyad"
MY_SPECIALS_URL = f"{BASE_URL}/specials/my-specials"
CDP_URL = "http://127.0.0.1:9223"

HERMES_PYTHON = "/Volumes/Extra/Substrate/.hermes/hermes-agent/venv/bin/python3"
if sys.executable != HERMES_PYTHON and os.path.exists(HERMES_PYTHON):
    os.execv(HERMES_PYTHON, [HERMES_PYTHON] + sys.argv)


async def get_cdp_ws_url():
    """Get the WebSocket debugger URL from CDP."""
    try:
        tabs = json.loads(urlopen(f"{CDP_URL}/json", timeout=10).read())
        # Prefer an existing HT page to keep session
        ht_tab = [t for t in tabs if t.get("type") == "page" and "harristeeter.com" in t.get("url", "")]
        if ht_tab:
            print(f"  Using existing HT tab: {ht_tab[0].get('title', '')[:60]}")
            return ht_tab[0]["webSocketDebuggerUrl"]
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


async def extract_specials(page_url=WEEKLY_AD_URL):
    """Navigate to the HT specials page and extract all deal cards."""
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
        # Navigate to the specials page
        print(f"  Navigating to: {page_url}")
        nav_result = await cdp_call(ws, "Page.navigate", {"url": page_url})
        loader_id = nav_result.get("result", {}).get("loaderId")
        if not loader_id:
            print("  ⚠️ Navigation may not have completed")

        # Wait for page to load
        await asyncio.sleep(6)

        # Check the current URL to see if we got redirected (login, store selector)
        result = await cdp_call(ws, "Runtime.evaluate", {
            "expression": "document.location.href",
            "returnByValue": True
        })
        current_url = result.get("result", {}).get("result", {}).get("value", "")
        print(f"  Current URL: {current_url}")

        if "signin" in current_url or "login" in current_url:
            print("❌ Not logged in. The CDP browser needs an HT login session.")
            print("   Log in manually at https://www.harristeeter.com/signin")
            return None

        if "specials" not in current_url and "choose-store" in current_url.lower():
            print("⚠️ Store selection page detected. The HTML extraction may be limited.")
            # Try to continue — the page may still load specials content behind the wall

        # Check for "My Specials Unavailable" on the my-specials page
        result = await cdp_call(ws, "Runtime.evaluate", {
            "expression": "document.body.innerText.includes('My Specials Unavailable') || document.body.innerText.includes('To view')",
            "returnByValue": True
        })
        page_blocked = result.get("result", {}).get("result", {}).get("value", False)
        if page_blocked and "my-specials" in current_url:
            print("⚠️ My Specials says 'Unavailable' — store not selected or no personal deals.")
            print("   Falling back to Weekly Ad page.")
            if "my-specials" in current_url:
                # Try the weekly ad instead
                await cdp_call(ws, "Page.navigate", {"url": WEEKLY_AD_URL})
                await asyncio.sleep(6)

        # Extract all deal cards via JavaScript
        print("  Extracting deal cards...")
        extract_js = """
        (function() {
            const cards = document.querySelectorAll('.AutoGrid-cell, [class*=\"AutoGrid\"] > li, [class*=\"SpecialsCard\"]');
            const results = [];

            for (const card of cards) {
                // Find the outermost SpecialsCard wrapper
                const specialsCard = card.querySelector('[class*=\"SpecialsCard\"]') || card;
                if (!specialsCard || !specialsCard.querySelector) continue;

                // Deal type badge (top-left/right tag)
                let dealType = '';
                let dealTag = specialsCard.querySelector('[data-citrus-component=\"Tag\"] span');
                if (dealTag) dealType = dealTag.innerText.trim();

                // Product name
                let productName = '';
                let titleEl = specialsCard.querySelector('[class*=\"SpecialsCardTitle\"]');
                if (titleEl) productName = titleEl.innerText.trim();

                if (!productName) continue;  // skip empty cards

                // Price display — several possible structures:
                let priceDisplay = '';
                let priceValue = null;

                // Structure A: dollar.cents via TWPAP (e.g. $9.99)
                const twpap = specialsCard.querySelector('.TWPAP-Price');
                const prefixSup = specialsCard.querySelector('.TWPAP-Prefix-Sup');
                const postfixSup = specialsCard.querySelector('.TWPAP-Postfix-Sup');
                if (twpap) {
                    const dollars = twpap.innerText.trim();
                    const cents = postfixSup ? postfixSup.innerText.trim() : '';
                    priceDisplay = '$' + dollars + '.' + cents;
                    priceValue = parseFloat(dollars + '.' + cents);
                }

                // Structure B: multi-buy text (e.g. "4/$1", "2/$7")
                let multiBuyText = '';
                const twfp = specialsCard.querySelector('.TWFP-Prefix-Text');
                if (twfp) multiBuyText = twfp.innerText.trim();

                // Structure C: BOGO text (Buy 1 Get 1 Free, etc.)
                let bogoText = '';
                const headline = specialsCard.querySelector('[class*=\"CouponCard-heading\"]');
                if (headline) {
                    const ariaLabel = headline.getAttribute('aria-label');
                    if (ariaLabel && (ariaLabel.includes('Buy') || ariaLabel.includes('Free'))) {
                        bogoText = ariaLabel;
                    }
                }

                // If price not found via TWPAP, try headline aria-label for dollar amounts
                if (!priceValue) {
                    if (headline) {
                        const ariaLabel = headline.getAttribute('aria-label') || '';
                        const priceMatch = ariaLabel.match(/\\$?([\\d.]+)/);
                        if (priceMatch && !ariaLabel.includes('Buy') && !ariaLabel.includes('Free')) {
                            priceDisplay = '$' + priceMatch[1];
                            priceValue = parseFloat(priceMatch[1]);
                        }
                    }
                }

                // Limit text
                let limitText = '';
                let limitEl = specialsCard.querySelector('[class*=\"color-text-neutral-primary\"]');
                if (limitEl) limitText = limitEl.innerText.trim();

                // Alternative limit/description — check full card text
                const cardText = specialsCard.innerText || '';

                // Image alt text (sometimes has cleaner name)
                let imgAlt = '';
                const img = specialsCard.querySelector('img');
                if (img) imgAlt = img.getAttribute('alt') || '';

                // Determine primary deal category
                let dealCategory = 'sale';
                if (dealType.includes('BOGO') || dealType.includes('Free') || dealType.includes('Half Price')) {
                    dealCategory = 'bogo';
                } else if (dealType.includes('Save at Least') || dealType.includes('Save Big')) {
                    dealCategory = 'multi-buy';
                } else if (dealType.includes('e-VIC')) {
                    dealCategory = 'e-vic';
                }

                // Extract savings amount from deal type
                let savingsText = '';
                const savingsMatch = dealType.match(/Save at Least \\$?([\\d.]+)/);
                if (savingsMatch) savingsText = '$' + savingsMatch[1];

                results.push({
                    name: productName,
                    price: priceDisplay,
                    price_value: priceValue,
                    deal_type: dealType,
                    deal_category: dealCategory,
                    multi_buy: multiBuyText,
                    bogo_text: bogoText,
                    savings: savingsText,
                    limit: limitText,
                    image_alt: imgAlt,
                    raw_card_text: cardText.substring(0, 500)
                });
            }
            return results;
        })()
        """

        result = await cdp_call(ws, "Runtime.evaluate", {
            "expression": extract_js,
            "returnByValue": True,
            "timeout": 15000
        })

        deals = result.get("result", {}).get("result", {}).get("value", [])
        if deals is None:
            deals = []

        print(f"  Extracted {len(deals)} deal cards")

        # Get page timestamp info
        result = await cdp_call(ws, "Runtime.evaluate", {
            "expression": "document.body.innerText.match(/Valid\\s+[\\w\\s,]+\\d{4}|Sale\\s+[\\w\\s,]+\\d{4}|[A-Z][a-z]+\\s+\\d{1,2}\\s*-\\s*[A-Z][a-z]+\\s+\\d{1,2}|Now\\s+thru/i)",
            "returnByValue": True
        })
        date_info = result.get("result", {}).get("result", {}).get("value", None)

        return {
            "store": "Harris Teeter",
            "page": "Weekly Ad" if "weeklyad" in page_url else "My Specials",
            "fetch_time": datetime.now(timezone.utc).isoformat(),
            "date_info": date_info,
            "deal_count": len(deals),
            "deals": deals
        }


async def main():
    import sys
    target = "weekly-ad"
    if "--my-specials" in sys.argv:
        target = "my-specials"

    print(f"=== HT Weekly Sales Fetcher [{target}] ===")

    page_url = MY_SPECIALS_URL if target == "my-specials" else WEEKLY_AD_URL
    result = await extract_specials(page_url=page_url)

    if result is None:
        print("🔓 HT login needed — log in at harristeeter.com in the CDP browser")
        exit(0)

    # Save to staging
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    tag = "weeklyad" if "weeklyad" in page_url else "myspecials"
    output_file = STAGING_DIR / f"ht_deals_{tag}_{timestamp}.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    # Latest symlink alias
    latest_file = STAGING_DIR / f"ht_deals_{tag}_latest.json"
    with open(latest_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\n✅ Saved {result['deal_count']} deals to {output_file}")

    # Print summary
    categories = {}
    for d in result['deals']:
        cat = d.get('deal_category', 'other')
        categories[cat] = categories.get(cat, 0) + 1
    print(f"   Breakdown: {categories}")

    # Highlight items matching Ted's known preferences
    pref_keywords = ['corn', 'chicken wing', 'bacon', 'broccoli', 'poblano',
                     'brie', 'coffee', 'cream', 'rice', 'beans', 'olive',
                     'pineapple', 'mandarin', 'yogurt', 'cottage cheese',
                     'steamfresh', 'birds eye']
    matches = []
    for d in result['deals']:
        name_lower = d.get('name', '').lower()
        for kw in pref_keywords:
            if kw in name_lower:
                matches.append(d)
                break
    if matches:
        print(f"   🔔 {len(matches)} items matching Ted's preferences on sale:")
        for m in matches[:8]:
            print(f"      {m['name']} — {m['price'] or m['deal_type']}")

    return result


if __name__ == "__main__":
    result = asyncio.run(main())
