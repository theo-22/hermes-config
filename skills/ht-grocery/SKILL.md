---
name: ht-grocery
description: Harris Teeter grocery shopping patterns — site navigation, Shop Deal modals, cart management, checkout flow. For any Hermes profile or Claude Code actor that needs to interact with HT.
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

## Prerequisites

- CDP browser running: `--remote-debugging-port=9222 --user-data-dir=/Users/ted/Substrate/Profiles/hermes-browser`
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

## Timing Notes
- Wednesday mornings: prices reset
- Friday: 4x fuel points available (clip coupon)
- Current shop: Pickup at Village at Chestnut Street (136 Merrimon Ave, Asheville NC)

## Shopping Guru Integration
Cross-reference workflow:
1. Scrape My Specials → extract personalized deals
2. Scrape Start My Cart / Past Purchases → known items
3. Check cart → what's already there
4. Generate cross-reference: "you buy X, it's on sale, you're low"
5. Present for Ted's approval
6. Navigate to checkout, let Ted complete the order
