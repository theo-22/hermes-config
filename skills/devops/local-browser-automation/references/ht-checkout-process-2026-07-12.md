# HT Checkout Process — Real-time CDP Interaction (2026-07-12)

## Flow Summary

Cart → "Check Out Pickup" → "Your Sale Items" recommendation page → "Continue to Checkout" → Scheduling page (`/scheduling?fulfillmentType=CurbSide`) → Select day + time → "Continue" → Payment page → "Place Pickup Order" → Confirmation

## React SPA Click Limitations

HT's checkout uses React synthetic events. CDP `element.click()` and `dispatchEvent(new MouseEvent('click'))` do NOT reliably trigger navigation steps:

| Step | CDP click works? | Fallback |
|------|:-:|----------|
| "Check Out Pickup" | ✅ | Direct Page.navigate to cart |
| "Continue to Checkout" | ✅ | Works with MouseEvent dispatch |
| Day carousel (Today/Mon/etc.) | ❌ | Must ask Ted to click |
| Time slot selection (7:00-7:30) | ❌ | React custom component — clicks don't register |
| "Continue" after time selected | ❌ | Button appears active but doesn't navigate |
| "Place Pickup Order" | ❌ | Same issue — ask Ted to click |

**Pattern for checkout:** Do all the prep (navigate pages, extract info), present the summary to Ted, and ask him to handle the last 2-3 clicks. The human-in-loop pattern emerged naturally here.

## Schedule Types

- Pickup at Village at Chestnut Street (136 Merrimon Ave, Asheville NC 28801)
- Available same-day if within store hours (until 11 PM)
- Also offers Delivery option

## Items in Cart (2026-07-12 example)

18 items, $46.20 subtotal, $7.45 savings, $38.75 estimated total.
Payment: Rewards World Credit card ending 2164.
Store: Village at Chestnut Street (Pickup).
Plus 78 fuel points earned on order.

## Order Confirmation Page

URL pattern: `/checkout/clicklist/<orderId>/complete`
Shows: order number, pickup time, items count, total savings, fuel points earned, confirmation text.

## Key Pattern

The CDP browser works well for READING data and ADDING items, but the CHECKOUT flow (especially time selection and final placement) consistently resists synthetic events. Always hand off the final steps to Ted.
