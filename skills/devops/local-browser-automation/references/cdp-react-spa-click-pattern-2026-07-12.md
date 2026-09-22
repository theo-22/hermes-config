# CDP React SPA Click Handling — 2026-07-12

## Problem
React SPAs (like Harris Teeter's website) don't reliably register `element.click()` from CDP Runtime.evaluate. The synthetic events that React listens for aren't triggered by programmatic `.click()` calls.

## Reliable pattern
Use `dispatchEvent` with a native `MouseEvent` alongside `.click()`:

```javascript
btn.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
btn.click();
```

Both calls together maximize the chance the SPA registers the interaction:
- `dispatchEvent(new MouseEvent(...))` fires the native DOM event
- `.click()` triggers any inline onclick handlers

## Button finding strategies
Ranked by reliability:

1. **aria-label match** — HT product cards use `aria-label` on Add to Cart buttons: `btn.getAttribute('aria-label')` contains "Add to Cart: Birds Eye ..."
2. **Text content** — `btn.innerText.trim() === 'Shop Deal'` — works for modal buttons with stable text
3. **Parent tree walk** — walk up parent elements (up to 15 levels) looking for a child button with target text

## Modal interaction (Shop Deal pattern)
Items with multiple varieties (e.g. "Birds Eye Steamfresh Vegetables — Select Varieties") open a modal via "Shop Deal" button. The modal is a `<dialog>` element with `display: flex`. Read varieties from `dialog.innerText`. Each variety has its own "Add to Cart" button within the modal.

## Cart page
After adding items, clicking "Show All Items" expands the cart list. "Check Out Pickup" proceeds to scheduling. The React SPA sometimes needs a fresh page load to show updated cart state.
