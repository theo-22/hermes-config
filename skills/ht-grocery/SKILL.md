---
name: ht-grocery
description: Harris Teeter grocery shopping patterns — site navigation, Shop Deal modals, cart management, checkout flow. For any Hermes profile or Claude Code actor that needs to interact with HT.
metadata:
  category: meta
  write_mode: file
  one_line_use: navigate/scrape Harris Teeter site for grocery deals and purchase data
  fast_pick: "no"
  version: 1.0.0
  platforms: [macos]
  tags: [grocery, harris-teeter, shopping, scraping]
---

# Harris Teeter Grocery Patterns

Site patterns learned from live session (2026-07-12). For any actor that needs to browse, scrape, or shop at Harris Teeter.

## If you're stuck

If a selector, click pattern, or extraction method in this skill stops working and 2-3 reasonable variations don't fix it, stop and report back rather than continuing to retry variations — don't burn an unattended run looping on a broken pattern. Report: what you tried, what actually happened (exact error/output, not a summary), and what page/URL/element you were working against. A site redesign or a genuinely new pattern needs a live human or a fresh live-session-to-skill pass to capture correctly, not more guessing against a stale assumption.

## Prerequisites

- CDP browser running: `--remote-debugging-port=9222 --user-data-dir="/Users/ted/Library/Application Support/Browser_Profiles/hermes-browser"`
- Chrome path: `/Volumes/Extra/Apps/Google Chrome.app`
- Login once per site — cookies persist in the hermes-browser profile
- Python deps: `websockets` (stdlib available)

## Site Navigation

### The correct way to navigate (not URL direct)
Use the nav bar — clicking "Shop" or "Save" in the top nav works. Direct URL navigation to `/specials/my-specials` triggers a store-selection wall that's hard to dismiss. **Nav bar > URL navigation.**

### Search
- Use `?query=` parameter, NOT `?keyword=` — the latter returns "no results" even when products exist
- Search sometimes returns nothing — HT search is unreliable. Fall back to the homepage Start My Order section or My Specials page

### Key page URLs
| Page | URL | Notes |
|------|-----|-------|
| Homepage | `https://www.harristeeter.com/` | Has "Start My Order" with Favorites/Sale/Past Purchases |
| My Specials | `/specials/my-specials` | Personalized deals — what Ted buys, on sale (nav via Save) |
| Weekly Ad | `/specials/weeklyad` | Full weekly ad (nav via Save) |
| e-VIC Coupons | `/savings/cl/coupons/` | Digital coupons to clip |
| Fuel Points | `/d/fuel-points-program` | Fuel point balance and multipliers |
| Cart | `/cart` | Shopping cart |
| Checkout | `/scheduling?fulfillmentType=CurbSide` | Pickup scheduling |
| Start My Cart | `/products/start-my-cart` | Ted's frequent items |

## Product Interaction

### Shop Deal Modal (multi-variety items)
Items like "Birds Eye Steamfresh Vegetables — Select Varieties" use a Shop Deal modal:
1. Find the product card by scanning innerText for the product name
2. Walk up the parent tree (up to 15 levels) looking for a `<button>` with `innerText.trim() === 'Shop Deal'`
3. Click with: `btn.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}))` followed by `btn.click()`
4. Wait 4-5s for the modal to appear
5. The modal is a `<dialog>` element with `display: flex` (visible)
6. Read varieties from the dialog's `innerText`

### Adding items to cart from modal
- Find the button by `aria-label` containing "Add to Cart" + product keywords
- Click same as above (MouseEvent + .click())
- After first add, the button becomes a quantity stepper — look for "Increment" or "increment" in aria-label
- Each product has its own button within the modal

### Adding items via search page
- Use `https://www.harristeeter.com/search?query={term}&searchType=default_search`
- Look for "Add to Cart" buttons with aria-labels containing product keywords
- Same double-click pattern (MouseEvent + .click())

### Cart page
- Cart URL: `/cart`
- Items may be collapsed — click "Show All Items" link to expand
- "Check Out Pickup" button at bottom
- Store already set to Village at Chestnut Street (136 Merrimon Ave)

### Checkout flow
1. Click "Check Out Pickup" on cart page → goes to "Your Sale Items" (recommendations)
2. Click "Continue to Checkout" → opens scheduling page
3. Select day (Today / Mon / Tue etc.) then time slot
4. Click "Continue" → payment page
5. Review → "Place Pickup Order" to confirm

**Known CDP limitations:**
- React SPA `click()` often doesn't register — use `dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}))` as well
- For critical interactions (checkout, payment), let the user click
- Store selector wall appears on first visit — requires clicking the pickup nav dropdown, selecting "Village at Chestnut Street", and "Start Shopping"

## Sam's Club Order Detail Extraction (printToPDF method — bypasses React collapsible items)

Sam's Club order detail pages use a React collapsible "N items" section that CDP `click()` cannot reliably expand (React synthetic events don't fire). **Solution:** use `Page.printToPDF` via CDP to render the page as PDF (includes ALL items expanded), then extract text with `pdftotext`.

**URL format:**
```
https://www.samsclub.com/en/orders/{orderIdNoDashes}?groupId={groupId}
```
- Order ID from the existing data: `8000-0004-7991-553`
- URL format removes dashes: `800000047991553`
- `groupId` comes from the URL when you first navigate there (seems persistent per session)

**Working extraction pattern (Python):**
```python
async with websockets.connect(ws_url) as ws:
    # Navigate (also dismisses any open print dialog)
    await cdp("Page.navigate", {"url": order_url})
    await asyncio.sleep(8)

    # Print to PDF — bypasses the collapsed items section entirely
    result = await cdp("Page.printToPDF", {
        'printBackground': True, 'preferCSSPageSize': True,
        'marginTop': 0.3, 'marginBottom': 0.3,
        'marginLeft': 0.3, 'marginRight': 0.3
    })
    pdf_data = result['result']['data']
    pdf_bytes = base64.b64decode(pdf_data)

    # Extract text with pdftotext (brew install poppler)
    import subprocess
    with open('/tmp/sc_temp.pdf', 'wb') as f: f.write(pdf_bytes)
    text = subprocess.run(['pdftotext', '/tmp/sc_temp.pdf', '-'],
                          capture_output=True, text=True, timeout=15).stdout
    os.remove('/tmp/sc_temp.pdf')

    # Parse items from the clean text
    # Format: Item name, then Qty N, then $X.XX
```

**Known orders (from existing data):**
| Order ID | Date | Items | Total |
|----------|------|:-----:|:-----:|
| 8000-0004-7991-553 | Jun 27 | 17 | $208.40 |
| 8000-0003-5927-335 | May 16 | 13 | $116.32 |
| 8000-0003-5996-955 | May 03 | 12 | — |
| 8000-0003-1295-560 | Apr 14 | 13 | — |
| 8000-0002-8400-883 | Apr 04 | 9 | — |
| 8000-0002-5459-413 | Mar 29 | 10 | — |
| 8000-0002-2566-432 | Mar 15 | 3 | — |
| 8000-0002-1815-461 | Mar 01 | 13 | — |
| 8000-0001-1129-672 | Jan 11 | 6 | — |
| 8000-0000-9313-412 | Jan 05 | 13 | — |

**Note:** This pattern (stuck on a React SPA collapsible section → ask Ted → use `Page.printToPDF` instead) is a general technique that works for any site where React prevents programmatic expansion of hidden content. The print preview renders everything expanded.
## Timing Notes
- Wednesday mornings: prices reset
- Friday: 4x fuel points available (clip coupon)
- Current shop: Pickup at Village at Chestnut Street (136 Merrimon Ave, Asheville NC)

## Unused lead — first-party JSON API (found 2026-07-12, never wired in)

The currently-running purchase-history scraper (`grocery_receipt_fetcher.py`) works by clicking into each order and reading rendered page text — the same class of approach that broke on Sam's Club when its site changed. HT actually has a clean, undocumented-but-real first-party JSON API that could replace that DOM-scraping entirely. Found via CDP network inspection, called directly from the page's own JS context (same-origin `fetch()`, cookies already attached — no extra auth needed for this one):

**Order list** — works, fully proven:
```
GET /atlas/v1/post-order/v1/purchase-history-search?pageNo=1&pageSize=10
```
Returns clean JSON: `createdDateTime`, `handoffStoreId`, `total` (e.g. `"USD 38.97"`), `purchaseType` (`PICKUP`/`IN_STORE`), `receiptKey` (format `097~00348~2026-07-12~1460~941917`), `lineItems` (UPC codes only, no names/prices at this level), `status`, plus `pageNo`/`pageSize`/`pageTotal`/`isLastPage` for pagination.

**Item-level detail — found the endpoint, never got it working:**
```
POST /atlas/v1/purchase-history/v2/details
```
- `GET` with `?receiptKey=...` → 405 Method Not Allowed (confirms POST-only).
- `POST` with `{"receiptKey": "..."}` body → 400, `{"reason": "Channel Missing", "code": "MISSING_CHANNEL"}`.
- Tried adding `channel`/`purchaseType` fields to the JSON body (`WEB`, `web`, `ONLINE`, `DESKTOP`) — all still hit the same `MISSING_CHANNEL` error. Never captured what the site's own JS actually sends for this call (would need to intercept the real request when the site itself opens an order detail view — reload didn't re-trigger it, needs a real click-through while `Network.requestWillBeSent` is being watched).

**Why this is still worth it:** if solved, this replaces DOM-scraping (fragile to site redesigns, exactly what broke Sam's Club) with a stable JSON contract for both order list AND item detail. **Next step for whoever picks this up:** click into a real order detail view while capturing the live request's headers/body (not guessing), find whatever `channel` value or header the site's own frontend sends, then this can fully replace the current DOM-based scraper.

**Update 2026-07-13 (Substrate-Hermes):** The API `MISSING_CHANNEL` issue was partially resolved — `x-kroger-channel: WEB` as a header gets past the channel error but hits `body must be an array` / `body[0] does not match any of the allowed types`. Multiple body shapes tried, none fully solved. **However, this API endpoint is not actually needed** — the order detail page (`/mypurchases/detail/<receiptKey>`) renders all item names, prices, quantities, and discounts directly in the page DOM. The existing DOM-based scraper can read it trivially. The API was a nice-to-have for cleanliness, but the data is already available through the rendered page.

## Weekly Ad / Deal Card Extraction (2026-07-13)

HT's site runs on Kroger's Citrus React framework. Weekly Ad page (`/specials/weeklyad`) renders each deal as an `<li class="AutoGrid-cell">` containing a `SpecialsCard` div. Extractable fields and their selectors:

| Field | Selector | Notes |
|---|---|---|
| Deal type badge | `[data-citrus-component="Tag"] span` | Values like "e-VIC Member Price $7.97", "Item Rings at Half Price", "Save at Least $5.00 On 4", "Must Buy 2 to Get 1 Free" |
| Price | `.TWPAP-Price` + superscript cents | BOGO items have no numeric price — `aria-label` says "Buy 1, Get 1 Free" instead |
| Multi-buy prefix | `.TWFP-Prefix-Text` | Gives "4/", "2/", "Buy 2, Get 3 Free" |
| Product name | `[class*="SpecialsCardTitle"]` | |
| Image alt | product `<img>` `alt` attribute | Cleaner, shorter product name than the title element |

**Deal category classification** (derived from badge text): `multi-buy` (Save at Least $X, per-lb deals), `bogo` (BOGO / half-price), `e-vic` (e-VIC member pricing), `generic` (plain sale price).

**Edge cases:**
- My Specials page (`/specials/my-specials`) is gated behind UI-based store selection — direct URL shows "Unavailable." Falls back to Weekly Ad, which doesn't have this gate.
- Multi-buy vs. per-unit price is ambiguous from the badge text alone — capture the raw card text alongside the parsed fields so ambiguous cases can be manually resolved later.
- BOGO items have a null numeric price — don't treat that as a parse failure.
- "lb" sometimes appears in the multi-buy prefix field as a false positive from per-lb deal cards (not an actual multi-buy).

**CLI usage:**
```bash
python3 ht_weekly_sales_fetcher.py           # Weekly Ad
python3 ht_weekly_sales_fetcher.py --my-specials  # falls back to weekly ad
```

**Output format:** JSON with `store`, `page`, `fetch_time`, `deal_count`, and a `deals` array — each deal has `name`, `price`, `price_value`, `deal_type`, `deal_category`, `multi_buy`, `bogo_text`, `savings`, `limit`, `image_alt`. Lands at `Commons/Substrate_Finance_Planning/Evidence/Grocery_Receipt_Staging/ht_deals_weeklyad_latest.json`.

## Shopping Guru Integration — REVISED 2026-09-12

**Current design (Ted-approved):** the deal pipeline lives in the AGENTS, not in scripts.
- **RETIRED:** `shopping_guru_weekly.sh` + `shopping_guru_crossref.py` (cron `shopping-guru-weekly-crossref`, paused 2026-09-12). The standalone weeklyad scraper silently produced `deal_count: 0` stubs most weeks (Kroger Citrus DOM churn), and the token-overlap crossref produced false-positive matches. Four consecutive weeks the check-in agents compensated with live CDP pulls — the agent method IS the proven tool.
- **NOW:** the Wednesday `shopping-guru-wednesday-checkin` agent (substrate-hermes cron `399120b5127f`) does the deal pull itself as STEP 1 (live CDP, ht-grocery patterns, writes `ht_deals_weeklyad_latest.json` + dated copy, verifies `deal_count > 0`, never fabricates on failure), selects deals by Ted's priority: BOGO/B2G2 first, then half-price/multi-buy, then 30%+ markdowns, matched in-context against his purchase ledger.
- **UNCHANGED:** receipt pulls (Sun/Wed 8pm), Saturday order finalizer (live price verification), Sunday preflight. Checkout stays human-only.

**If the agent pull fails 2 weeks running:** escalate to a Codex build of the first-party JSON API path below (order-list endpoint already proven; item-detail needs the `channel` header captured from real site traffic).
