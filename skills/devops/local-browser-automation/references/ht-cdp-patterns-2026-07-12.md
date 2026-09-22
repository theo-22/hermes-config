# Harris Teeter CDP Patterns — 2026-07-12 Live Session

Key lessons from the first collaborative HT shopping session using the CDP browser.

## Search: Use `?query=`, NOT `?keyword=`

HT search is unreliable. Two different URL patterns produce different results:
- `https://www.harristeeter.com/search?query=birds%20eye&searchType=default_search` → WORKS
- `https://www.harristeeter.com/search?keyword=birds%20eye` → Returns "no results" even when products exist

When search fails entirely, fall back to the homepage "Start My Order" section or My Specials page.

## Navigation: Use the Nav Bar, Not Direct URLs

Navigating directly to `/specials/my-specials` triggers a store-selection wall (an inline message "To view this week's specials, make sure your preferred store is currently selected") that is hard to dismiss via CDP. Instead:
- Click "Shop" or "Save" in the top navigation bar
- Then click the sub-link from the dropdown
- This avoids the store selector overlay entirely

## React SPA Click Handling

HT uses React (citrus-components). `element.click()` alone often doesn't trigger synthetic events. Reliable pattern:

```javascript
// MouseEvent dispatch + native click — both needed for React
btn.scrollIntoView({behavior: 'instant', block: 'center'});
btn.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
btn.click();
```

Known issues:
- **Quantity stepper buttons** in modals: after first click, aria-label changes from "Add to Cart:..." to "Increment ..." or "Decrement ..." — search for "Increment" in aria-label for subsequent clicks
- **Time slot selectors** on the scheduling page still failed even with this pattern — let the user click those

## Shop Deal Modal Pattern

Items with multiple varieties (e.g. "Birds Eye Steamfresh Vegetables — Select Varieties") use a Shop Deal overlay:

1. Find the product by scanning `innerText` for the product name
2. Walk up the parent tree (up to 15 levels) looking for a `<button>` with `innerText.trim() === 'Shop Deal'`
3. Click with the MouseEvent + click pattern above
4. Wait 4-5s for the modal — it's a `<dialog>` element with `display: flex`
5. Read varieties from the dialog's `innerText`
6. Each variety has its own "Add to Cart" button identified by aria-label

## Store Selector Wall

When the store selector modal appears (triggered by some page loads):
1. Click "Pickup" in the nav bar (opens a modality selector)
2. Click "Village at Chestnut Street" from the recent stores list
3. Click "Start Shopping" button to confirm
4. Then the Shop Deal modal opens on the next click

**Better approach: Don't trigger it.** Navigate via nav bar, not direct URL.

## Checkout Flow

1. Cart page → "Check Out Pickup" → goes to "Your Sale Items" (recommendations page)
2. Click "Continue to Checkout" → scheduling page
3. Select day (Today / Mon / Tue etc.), then time slot
4. Click "Continue" → payment page
5. "Place Pickup Order" to confirm

**Critical: The last 2-3 steps (time slot selection, payment, place order) often fail with CDP clicks.** Let the user handle these in the browser.

## Items Already in Cart

When navigating to a page where items are already in the cart:
- "Add to Cart" buttons become quantity steppers ("Decrement / Increment")
- The aria-label changes to reflect the new state
- Search for "incremented successfully" in aria-labels to confirm an add worked

## Known Limitations (2026-07-12)

- **React SPA clicks don't always register** — even with MouseEvent dispatch, some buttons (time slots, Continue on scheduling page) failed repeatedly
- **Playwright may handle React better** for critical interactions
- **Store selector persistance** — CDP page navigations lose the store context even though the visual browser keeps it
- **Search returns empty** — inconsistent; retry with `?query=` parameter, fall back to nav bar browsing
