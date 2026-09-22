# Sam's Club Order Extraction via Browser

## Two Extraction Methods

### Method 1: Quick-Fetch (Order Summaries Only) — New 2026-07-09

For cron-based staging: extract order IDs, dates, and item counts from the **order list page** body text. **No SPA clicks needed.** Sam's Club renders order data in flat readable text.

**URL:** `https://www.samsclub.com/orders`
**Output:** Order ID, date (format `Picked up on Jun 27`), item count, location.
**No dollar totals** on the list page — totals only in order detail / print view.
**Script:** `scripts/sams_club_fetcher.py`

#### Flat-text format
```
Order 8000-0004-7991-553
Picked up on Jun 27          ← abbreviated month!
Asheville Sam's Club at 645 PATTON AVE
20 items
```

#### Extraction code (Python/Playwright)
```python
body = await page.evaluate('() => document.body.innerText')
# Then parse with regex — see scripts/sams_club_fetcher.py parse_orders()
```

#### Abbreviated month names
Sam's Club uses abbreviated month names in "Picked up on" lines. The regex must handle both forms:
```python
months_pat = r'(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
```

#### CDP Cookie Bridge
The quick-fetch script gets cookies from the CDP browser (port 9222) instead of requiring a separate Playwright login. Same technique as Harris Teeter — extract `Storage.getCookies` from CDP, filter for samsclub.com domains, write as Playwright-compatible cookies to `/tmp/sc_cookies.json`.

**⚠️ sameSite casing gotcha:** CDP returns `"LAX"`, Playwright expects `"Lax"`. Use dict lookup:
```python
{"LAX": "Lax", "STRICT": "Strict", "NONE": "None"}.get(ss.upper(), "Lax")
```

**Cron:** substrate-hermes, Sundays 10:30am, no-agent, `sams_club_fetcher.py`

---

### Method 2: Item-Level Detail (Print View) — Preferred for Deep Extraction

For full item-level data (product names, prices, quantities, fees), use the **Print View** method. This avoids the React SPA collapsed-item problem.

**Steps:**
1. Navigate to `https://www.samsclub.com/orders`
2. Click "View details" button for the target order
3. **Click "Print receipt" button** — renders a print-optimized view with all items visible
4. Extract from DOM: `.print-items-list .flex.justify-between`

**Why Print View is better than clicking "Show items":**
- No React SPA issues — print view is plain HTML
- All items visible at once (no collapsed sections)
- Consistent DOM structure across orders
- Fees (Pickup, Tax) also visible via `.print-fees-item`

#### Print View DOM Extraction Code
```javascript
(() => {
  const rows = document.querySelectorAll('.print-items-list .flex.justify-between');
  const items = [];
  rows.forEach(row => {
    const text = row.textContent.trim();
    const qtyMatch = text.match(/Qty\s+(\d+)/);
    const priceMatches = text.match(/\$(\d+\.\d{2})/g);
    const totalPrice = priceMatches ? priceMatches[priceMatches.length - 1] : '';
    const nameEnd = text.indexOf('Qty');
    const name = nameEnd > -1 ? text.substring(0, nameEnd).trim() : text.substring(0, 80);
    items.push({name: name.substring(0, 80), qty: qtyMatch ? qtyMatch[1] : '?', price: totalPrice});
  });
  const fees = document.querySelectorAll('.print-fees-item');
  return JSON.stringify({items, fees: Array.from(fees).map(f => f.textContent.trim()), count: items.length});
})()
```

### Method 3: Legacy DOM (Show Items Click) — Fallback Only

Alternative approach using `document.querySelectorAll('.dn')` after clicking "Show items". Less reliable than Print View — React SPA may flicker or navigate away. See earlier session notes for JS click sequence.

---

## Login

- **URL**: `https://www.samsclub.com/account/auth/login`
- Ted's account is pre-authenticated in the Hermes Chrome (CDP) profile
- If not logged in: email field is standard text input, verification code sent to phone

## Key Gotchas

1. **React SPA rendering**: Items are NOT in `document.body.innerText` until expanded. Use Method 2 (Print View) or 3 (Legacy DOM > .dn click).
2. **"View details" vs "Show items"**: "View details" is on the order list card. "Show items" is on the order detail page — it's a `<button>` with aria-expanded="false". JS `click()` works.
3. **Page navigation**: Opening developer tools or certain clicks can cause the page to navigate away from the order detail. If this happens, re-navigate.
4. **Item count discrepancy**: UI says "20 items" but extraction may yield 17 unique rows. Difference is quantity units (Qty 2 = 2 items in UI count). Subtotal always matches.
5. **Price format**: Unit prices are in cents/oz (e.g., "45.0¢/oz"). Total prices are in dollars (e.g., "$14.98").
6. **Order detail page errors**: Direct navigation to `/orders/<order_id>` using the CDP browser shows "We hit a snag. Please try again." — use the list page click sequence instead.

## 2026-07-12 update — button text changed, print-receipt step unresolved

The "View details" button's **visible text is now "See details"** (aria-label still says "View details for order number ..." — match on that instead, it's more stable):
```python
view_buttons = await page.locator('button[aria-label*="View details for order number"]').all()
```
Fixed in `scripts/sams_club_fetcher.py`. Order-list level scraping (order id, date, item count, no dollar totals) is confirmed working unattended as of tonight.

**Priority note (2026-07-12, Ted):** low-frequency store — he can grab a receipt when he actually shops there. Don't treat this gap as urgent; fix opportunistically, not as a standing priority.

**Still broken, not yet diagnosed:** after clicking "See details" then "Print receipt", the extraction that follows (`.print-items-list .flex.justify-between`) comes back empty and the subsequent `page.goto(ORDERS_URL)` + `wait_for_selector('h2')` times out. Suspect Print Receipt opens a new tab/window rather than navigating in place — the script only watches the original `page` object. Next session: check `context.pages` for a new tab right after the Print Receipt click, or listen for a `page` event on `context`, before assuming the print view rendered in place.

**Also tonight:** rapid repeated automated `/orders` page loads (several diagnostic script runs in a row) tripped Sam's Club's "prove you're human" bot-detection wall. Recovered by having Ted log in via a real (non-Playwright-testing-build) Chrome window and transplanting the cookies into `/tmp/sc_cookies.json`. Lesson: pace live-site diagnostic probes — don't fire off more than one or two quick automated navigations in a row against this site, and prefer reading the DOM/network in a single combined script rather than several small sequential ones.

## Reconciliation

Sam's Club: `Subtotal + Tax = Total`
- Tax shown separately in payment summary
- Item rows sum to subtotal

## Example Data (Jun 27, 2026)

Order 8000-0004-7991-553, Curbside pickup, $208.40 total ($204.39 subtotal + $4.01 tax)

17 unique items, 20 quantity units, $204.39 subtotal (matches receipt exactly).

## Verification environment note (CC correction, 2026-07-14)

The refiner round that rewrote Method 2 (direct-DOM, no click) reported it "couldn't validate end-to-end because Playwright isn't installed on this machine." **That's wrong — Playwright IS installed** at `/Volumes/Extra/Substrate/.hermes/hermes-agent/venv/bin/python3` (confirmed by CC after the run). So the DOM-extraction logic was verified via CDP against one live order (real: 13 items, $169.73+$4.39=$174.12 reconciles), but the *full script running start-to-finish through the refined path is still unproven* — not because it couldn't be, but because the worker wrongly believed the tool was missing.

**For the next refiner round (updated knowledge to carry in):** Playwright is available at that venv path; you CAN run the whole script end-to-end. The only real reason not to is the bot-detection wall — pace it, single run, reuse the already-authenticated CDP session (port 9222) rather than navigating fresh if possible. Don't re-report "not installed."
