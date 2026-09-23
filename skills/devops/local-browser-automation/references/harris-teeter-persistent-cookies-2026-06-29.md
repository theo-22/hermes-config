# Harris Teeter Receipt Fetching — Persistent Cookie Approach (2026-06-29)

## What Works

**Logged-in once → cookies saved → automated weekly fetch**

1. Open Playwright persistent context (`user_data_dir=/tmp/ht_session_persist`)
2. Navigate to `harristeeter.com/signin?redirectUrl=/mypurchases`
3. Wait for `#signInName` field (Kroger B2C form loaded)
4. **User types credentials manually** into visible browser window
5. Script waits for URL to change away from login pages (up to 5 min)
6. Save cookies: `cookies = await context.cookies()` → JSON file
7. Navigate to mypurchases, extract data via JS evaluate
8. On subsequent runs, `context.add_cookies(cookies)` skips login entirely

## First Login Script

```python
async def login_flow():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir='/tmp/ht_session_persist',
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        page = context.pages[0]
        await page.goto('https://www.harristeeter.com/signin?redirectUrl=/mypurchases')
        await page.wait_for_selector('#signInName', timeout=15000)
        print("🔓 Log in manually. Waiting 5 min...")
        
        for i in range(150):
            await asyncio.sleep(2)
            url = page.url
            if 'harristeeter.com' in url and 'signin' not in url and 'login' not in url and 'connect-auth' not in url:
                cookies = await context.cookies()
                with open(COOKIE_FILE, 'w') as f:
                    json.dump(cookies, f)
                print(f"✅ Saved {len(cookies)} cookies")
                break
        await context.close()
```

## Extraction Pattern (DOM via JS evaluate)

### Method 1: aria-label (PREFERRED — most reliable)

Product names AND sizes are in the `aria-label` attribute of `<a>` tags with `ProductDescription` class:

```python
import re
names_with_sizes = re.findall(r'aria-label="([^"]+?)\s*title"', html)
# Returns: ["Birds Eye Steamfresh Super Sweet Corn, Frozen Vegetables 10 OZ", ...]

# Clean names are in <h3 data-testid="cart-page-item-description">
names = re.findall(r'data-testid="cart-page-item-description"[^>]*>([^<]+)</h3>', html)
```

This is more reliable than innerText parsing because:
- aria-label includes both name AND size in one attribute
- h3 text is the clean product name without size/price noise
- No DOM container walking needed

### Method 2: Container walking (fallback)

Product names are in `[class*="ProductDescription"]` anchors. Walk up to a `$`-containing container:

```javascript
const nameEls = document.querySelectorAll('[class*="ProductDescription"]');
for (const el of nameEls) {
    let container = el.parentElement;
    for (let j = 0; j < 6; j++) {
        if (container.innerText.includes('$') && container.innerText.length > 30) break;
        container = container.parentElement;
    }
    const allPrices = container.innerText.match(/\$[\d.]+/g);
    const promoMatch = container.innerText.match(/(\d+ For \$[\d.]+)/);
    const sizeMatch = container.innerText.match(/(\d+\s*(oz|OZ|ct|CT|lb|fl oz))/i);
}
```

## Price Parsing Caveat

Dollars and cents are split across separate `<span>` elements (e.g. `$1` + `.` + `25` = `$1.25`).
Regex `/\$[\d.]+/g` catches `$1` not `$1.25`. The last price in `allPrices` is usually the
original/list price. For finance tracking, the **order total** (from list page) is reliable;
item-level prices need DOM refinement.

## Order Totals (Reliable)

```javascript
const bodyText = document.body.innerText;
const totalMatch = bodyText.match(/Total:\s*\$([\d.]+)/);
const savingsMatch = bodyText.match(/\$([\d.]+)\s*Total Savings/);
const taxMatch = bodyText.match(/Tax\s*\$([\d.]+)/);
```

## Verified Data (2026-06-29)

Ted's account (THEODORE, tedhughes@me.com) had 4 orders visible:
- June 27, 2026 — Pickup — $41.89 (12 items, $32.04 savings)
- June 21, 2026 — In-store — $66.66 (15 items, $37.02 savings)
- June 14, 2026 — In-store — $78.05 (17 items, $15.60 savings)
- June 11, 2026 — In-store — $27.95 (2 items, $5.03 savings)

**The account is NOT empty.** The "no purchase history" was from a fresh/unauthenticated Playwright session.

## Why Other Approaches Failed

| Approach | Problem |
|----------|---------|
| Cloud browser (Browserbase) | `ERR_HTTP2_PROTOCOL_ERROR`, 502s, window closes |
| Headless Playwright fresh profile | Kroger B2C detects automation, blocks requests |
| CDP attach to running Chrome | `--remote-debugging-port` ignored if Chrome already running |
| Using Chrome profile directly | Profile lock conflict when Chrome is running |
| Script closing window before user types | Fixed: wait for URL change, not fixed timeout |

## Data Location

- Staging: `/Volumes/Extra/Substrate/Commons/Substrate_Finance_Planning/Evidence/Grocery_Receipt_Staging/ht_receipts_latest.json`
- Script: `grocery_receipt_fetcher.py` (in `~/.hermes/scripts/` and `~/.hermes/profiles/substrate-hermes/scripts/`)
- Cookies: `/tmp/ht_cookies.json` (regenerate with `--login` if expired)
