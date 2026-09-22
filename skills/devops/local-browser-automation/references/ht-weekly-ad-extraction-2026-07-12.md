# HT Weekly Ad & My Specials — CDP Real-time Extraction

**Date:** 2026-07-12
**Source:** Collaborative scraping session, Ted + Substrate-Hermes

## URLs

| Page | URL |
|------|-----|
| Weekly Ad | `https://www.harristeeter.com/specials/weeklyad` |
| My Specials | `https://www.harristeeter.com/specials/my-specials` |
| Start My Cart | `https://www.harristeeter.com/products/start-my-cart` |
| Search | `https://www.harristeeter.com/search?keyword=<term>` |
| Purchase History | `https://www.harristeeter.com/mypurchases` |
| Cart | `https://www.harristeeter.com/cart` |

## Extraction Pattern

1. Navigate via CDP `Page.navigate` (HT has minimal bot detection)
2. Wait 5-8s for the React SPA to fully render
3. Extract `document.body.innerText` — all deal text is in flat text, not images
4. Parse by scanning for deal header lines followed by product names

## Deal Type Patterns (from innerText)

| Pattern | Meaning | Example |
|---------|---------|---------|
| `Item Rings at Half Price` | BOGO — second item half price | Raspberries, Bacon |
| `Buy 1, Get 1 Free` | BOGO | Oscar Mayer Bacon |
| `Buy 2, Get 3 Free` | Buy 2 get 3 free | Kraft Shredded Cheese |
| `Buy 2, Get 1 Free` | Buy 2 get 1 free | Coca-Cola, Powerade |
| `Save at Least $X` | Discount shown | Save $5.00 On 4 |
| `Save Big!` | Flat sale price | $2.79 Birds Eye |
| `e-VIC Member Price $X` | Loyalty card price | $7.97 Rao's Pizza |
| `Must Buy X to Get Y Free` | Conditional multi-buy | Must Buy 1 to Get 1 50% off |
| `4/$X`, `2/$X`, `3/$X` | Multi-unit pricing | 4/$10 Sweet Corn |

## Item Card Structure

Each deal card on the page has this approximate layout:
```
[DEAL TYPE HEADER]
[PRICE/BOGO DETAIL]
[PRODUCT NAME - SIZE]
[Select Varieties / Limit / Product of]
[Add to List] [Shop Deal]
```

## Page Structure

The page is an SPA using HT's citrus design system. All deals render in flat `innerText` without iframes or shadow DOM. Department tabs use CSS class `citrus-Tabs-tab`.

## Shop Deal Modal — Variant Selection & Add to Cart

Clicking "Shop Deal" on a product card opens a modal dialog containing all variants of that product. Critical for bulk items (like Birds Eye Steamfresh) with multiple varieties.

### Modal Detection

```javascript
// Check for an open modal
document.querySelectorAll('[role="dialog"]')
// Modal is display:flex; visibility:visible when open
// Look for "Shop Deal" in modal title
```

### Variant Structure

Each variant in the modal:
- **Product name** (text node, exact match)
- **Size/weight** (e.g. "10.800 OZ")
- **Sale price** (e.g. "$2.79")
- **Regular price** (e.g. "Discounted From $3.39")
- **Add to Cart button** — `<button>` with `innerText === "Add to Cart"`
- **Availability** — "Delivery Only" instead of "Add to Cart" (skip for Pickup)

### Finding Variants via TreeWalker

```python
result = await evaluate(f"""
    (() => {{
        let walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
        let node;
        while (node = walker.nextNode()) {{
            if (node.textContent.trim().startsWith({json.dumps(search_text[:25])})) {{
                let el = node.parentElement;
                for (let i = 0; i < 15; i++) {{
                    if (!el) break;
                    let btns = el.querySelectorAll('button');
                    for (let btn of btns) {{
                        if (btn.innerText.trim() === 'Add to Cart') {{
                            btn.scrollIntoView({{behavior: 'instant', block: 'center'}});
                            btn.click();
                            return 'added';
                        }}
                    }}
                    el = el.parentElement;
                }}
            }}
        }}
        return 'not found';
    }})()
""")
```

### Verifying Cart Additions

After clicking "Add to Cart", the button's aria-label changes:

```
Before:  "Add to Cart: <product name> - <size>"
After:   "<Add/Decrement/Increment> <product name> - <size>, incremented successfully"
```

Check for "incremented successfully":
```python
incremented = await evaluate("""
    (() => {
        let btns = document.querySelectorAll('button');
        let added = [];
        for (let btn of btns) {
            let label = btn.getAttribute('aria-label') || '';
            if (label.includes('incremented successfully')) {
                added.push(label.substring(0, 80));
            }
        }
        return JSON.stringify(added);
    })()
""")
```

## ⚠️ Critical Gotchas

1. **Cart must be initialized** — Click "Start My Cart" before any Add to Cart action. Without this, clicks appear to succeed (aria-labels change) but cart stays empty. Found 2026-07-12 after several attempts to add items that showed as "incremented successfully" but never appeared in the cart.
2. **Store selection doesn't persist** — CDP browser session loses store context between page navigations. The "Choose Store" prompt blocks Shop Deal modals. Workaround: click pickup nav → select Village at Chestnut Street → click "Start Shopping". Sometimes still doesn't stick — user may need to set store manually.
3. **Search broken via CDP** — `search?keyword=X` AND `search?query=X` both return "no results". This is a known HT site flakiness, not a URL format issue. Use My Specials or Weekly Ad pages instead of search. The search overlay (accessed via nav bar search icon) may work when the URL doesn't, but is not reliable either.
4. **SPA button clicks** — HT's citrus design system uses React synthetic events. `element.click()` alone often doesn't register. Use `btn.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}))` followed by `btn.click()`.
5. **Text matching collisions** — "Sugar Snap Peas" appears in both standalone product and "Broccoli, Carrots, Sugar Snap Peas, Water Chestnuts". Use longer prefixes or exact match.
6. **"Delivery Only" variants** — Some variants can't be added for Pickup. Check for "Delivery Only" text before clicking. From 2026-07-12: Diced Sweet Potatoes, Tri-Colored Pepper & Onion Medley, Broccoli Stir-Fry were Delivery Only.
7. **Modal auto-closes** — Each CDP connection is independent. If modal disappears between script runs, re-click Shop Deal.
8. **Cart count not reliably in DOM text** — HT stores cart count in React state. The cart icon badge may show old counts. Verify additions via button aria-labels ("incremented successfully") instead.
9. **All actions stay on same URL** — No navigation occurs on any SPA interaction. Verify state via `window.location.href`.
10. **"Start My Cart" auto-adds all My Specials items** — when you click Start My Cart from the My Specials page, it pre-loads every item with quantity 1. Every item in the list gets a "Decrement" button. This can cause confusion if you wanted to pick items selectively. Verify cart state before adding more.
11. **HT search via nav bar overlay** — The search icon in the top nav opens an overlay, not a new page. Typing in it shows suggestions ("birds eye", "birds eye frozen vegetable") but clicking a suggestion may navigate to a search results page that shows "no results" even for valid products. This appears to be a site reliability issue, not a script problem.

## Successful Add-to-Cart Sequence (proven 2026-07-12)

```
1. Navigate to My Specials
2. Click "Start My Cart" (sets cart context)
3. Dismiss store selector (pickup → Village → Start Shopping)
4. Click Shop Deal on target item
5. Wait 4-5s for modal
6. Extract modal innerText to list varieties
7. For each desired variant: find text → walk up → click Add to Cart
8. For qty > 1: find Increment button → click (n-1) times
9. Verify via aria-labels containing "incremented successfully"
```

## Example — Birds Eye Variant List (2026-07-12, all $2.79)

| Variety | Size | Available |
|---------|------|-----------|
| Baby Broccoli Florets | 12.6 oz | ✅ Add to Cart |
| White Pearl Onions | 14.4 oz | ✅ Add to Cart |
| Diced Sweet Potatoes | 10 oz | ❌ Delivery Only |
| Sugar Snap Peas | 10 oz | ✅ Add to Cart |
| Edamame in the Pod | 10 oz | ✅ Add to Cart |
| Broccoli, Carrots, Sugar Snap Peas... | 10.8 oz | ✅ Add to Cart |
| Broccoli and Cauliflower | 10.8 oz | ✅ Add to Cart |
| Corn, Carrots & Asparagus | 10.8 oz | ✅ Add to Cart |
| Whole Green Beans | 10.8 oz | ✅ Add to Cart (Low Stock) |
| Brussels Sprouts | 10.8 oz | ✅ Add to Cart |
| Broccoli Florets | 10.8 oz | ✅ Add to Cart |
| Baby Sweet Peas | 13 oz | ✅ Add to Cart |
| Baby Gold & White Corn | 14.4 oz | ✅ Add to Cart (Low Stock) |
| Garlic Butter Broccoli | 9 oz | ✅ Add to Cart |
| Tri-Colored Pepper & Onion | 14.4 oz | ❌ Delivery Only |
| Broccoli Stir-Fry | 14.4 oz | ❌ Delivery Only |
