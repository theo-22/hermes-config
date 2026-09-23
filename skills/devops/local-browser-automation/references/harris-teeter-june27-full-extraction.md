# Harris Teeter — Full Order Extraction Example (June 27, 2026)

## Order Summary

- **Order ID**: `097~00348~2026-06-27~1460~231413`
- **Type**: Pickup
- **Date**: June 27, 2026
- **Items**: 12
- **Item Total**: $67.94
- **Discounts**: -$27.09
- **Tax**: $1.04
- **Total**: $41.89
- **Savings**: $32.04 (47% savings rate)

## Full Item List (from aria-label + h3 extraction)

| # | Item | Size | Tags |
|---|------|------|------|
| 1 | Birds Eye Steamfresh Super Sweet Corn, Frozen Vegetables | 10 OZ | frozen, produce |
| 2 | Birds Eye Steamfresh Whole Grain Rice with Vegetables Steamer Bag | 10 oz | frozen, staple |
| 3 | Birds Eye® Long Grain White Rice | 10 oz | frozen, staple |
| 4 | Birds Eye® Steamfresh Selects Frozen Long Grain White Rice & Vegetables | 10 oz | frozen, staple |
| 5 | Pork Boston Butt Country Style Ribs Value Pack | $1.99/lb | protein |
| 6 | Daily's Naturally Hickory Smoked Bacon | 16 oz | protein |
| 7 | Fresh Bunch of Bananas – 5-7 Bananas | $0.59/lb | produce |
| 8 | Fresh Sweet Corn on the Cob-Each | 1 ct | produce |
| 9 | Harris Teeter® Canned Fancy Pineapple Slices in 100% Pineapple Juice | 20 oz | produce, pantry |
| 10 | Harris Teeter™ 85% Cocoa Extra Dark Belgian Chocolate | 3.5 oz | snack |
| 11 | Harris Teeter™ Mandarin Orange Segments in Pear Juice | 11 oz | pantry |
| 12 | Fresh Blueberries - 1 PT Clamshell | 1 pt | produce |

## Extraction Code (Python regex on saved HTML)

```python
import re

with open('order_detail.html') as f:
    html = f.read()

# Method 1: aria-label (name + size together)
items_aria = re.findall(r'aria-label="([^"]+?)\s*title"', html)

# Method 2: h3 (clean name only)
h3_names = re.findall(r'data-testid="cart-page-item-description"[^>]*>([^<]+)</h3>', html)

# Totals from page text
item_total = re.search(r'Item Total.*?\$([\d.]+)', html)
discounts = re.search(r'Item Coupons/Sales.*?\$([\d.]+)', html)
tax = re.search(r'Tax.*?\$([\d.]+)', html)
total = re.search(r'Total.*?\$([\d.]+)', html)
savings = re.search(r'\$([\d.]+)\s*Total Savings', html)
```

## Finance Room Reconciliation Format

Existing files in `/Volumes/Extra/Substrate/Commons/Substrate_Finance_Planning/` use this table format:

```
| Store | Receipt / order date | Receipt / order id | Visible line count | Item/subtotal | Discount/promo | Tax | Calculated total | Visible total | Delta | First-pass tags | Sample visible items |
```

New capture files should be numbered sequentially (e.g. `20_Grocery_Receipt_Capture_2026-06-27.md`) and follow the same format.

## Key Lesson: Don't Close the Browser Early

The #1 mistake in this session: the script had a timeout that closed the Playwright browser window before Ted could finish typing his credentials. The correct pattern:

```python
# WRONG — closes before user finishes
await asyncio.sleep(30)
await context.close()

# RIGHT — wait for URL change, not fixed timeout
for i in range(150):  # 5 minutes max
    await asyncio.sleep(2)
    url = page.url
    if 'harristeeter.com' in url and 'signin' not in url and 'login' not in url:
        # Login succeeded!
        break
```

## Key Lesson: Don't Kill/Restart Chrome Repeatedly

Attempting to attach to Ted's running Chrome via CDP (`--remote-debugging-port=9222`) failed because:
1. Chrome was already running (new instance just forwards to existing)
2. Profile lock prevents two processes using same profile
3. The flag gets ignored when Chrome acts as secondary process

**Solution**: Use a SEPARATE persistent context profile (`/tmp/ht_session_persist`) that doesn't conflict with Ted's running Chrome.
