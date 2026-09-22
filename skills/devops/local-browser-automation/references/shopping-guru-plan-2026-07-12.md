# Shopping Guru — Data Sources & Plan Reference

> Created 2026-07-12 during collaborative HT scraping session.
> Full plan: `/Volumes/Extra/Substrate/Substrate_v14/Chapters/16_Shopping_Guru/PLAN.md`

## Data Sources Found

### Harris Teeter Purchase History (item-level)
**Location:** `/Volumes/Extra/Substrate/Commons/Substrate_Finance_Planning/Evidence/Grocery_Receipt_Staging/ht_receipts_*.json`

Best file: `ht_receipts_20260629_233303.json` — 3 detailed orders (Jun 11, Jun 14, Jun 21) with item names, prices, quantities, deal info. Later fetches only got order-level summaries.

Items found in Ted's history: Chicken wings (bought twice, Jun 11 + Jun 21), Drumsticks, Birds Eye Steamfresh (Cheesy Pasta & Broccoli, Chive Butter Roasted Red Potatoes), Sweet Corn (every trip), Bananas, Brie, Olives, Pasta, Apples (Envy, Pink Lady), Pears (Bartlett, D'anjou), Tofu, Coffee (Classic Medium Roast Ground), Heavy Cream, Bacon, Breakfast Burritos (El Monterey), Pineapple Slices, Mandarin Oranges, Grapes, Poblano Peppers, Onions, Potatoes, and more.

### Weekly Deals
- **My Specials** (`/specials/my-specials`) — personalized deals based on Ted's purchase history
- **Weekly Ad** (`/specials/weeklyad`) — all current sales
- **e-VIC Coupons** (`/savings/cl/coupons/`) — digital coupons

### Price Thresholds Learned (2026-07-12)
- Chicken wings: good price ≤$2.99/lb at HT, ≤$2.89/lb at Sam's Club
- Chicken drumsticks: $1.49/lb was a deal (bought, in freezer)
- Sweet Corn: 4/$1 ($0.25/ear) at HT, corn season

## Shopping Guru Concept

Cross-reference weekly sales against purchase history to generate:
- Items you buy that are on sale
- Reorder timing (when was the last time?)
- Price history (is this actually a good deal?)
- Healthier suggestions based on patterns
- Inventory awareness (food in freezer, pantry stock)

## Plan Location

Full plan at `/Volumes/Extra/Substrate/Substrate_v14/Chapters/16_Shopping_Guru/PLAN.md` with 3 phases:
- Phase 1: Full purchase history scraper + weekly sales scraper + cross-reference report
- Phase 2: Reorder cadence, price history, gap detection
- Phase 3: Healthier swaps, new-to-try suggestions, meal ideas

## Model Selection

- **Flash (deepseek-v4-flash):** All scraping — CDP scripts run on terminal, not through model
- **Pro (deepseek-v4-pro):** Cross-referencing/analysis layer (meal suggestions, price trends)
