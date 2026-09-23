# Grocery Receipt Cron Setup

How to set up automated grocery receipt collection from Harris Teeter and Sam's Club.

## Discovered 2026-06-29

## Cron Architecture

Two cron jobs run on schedule:
1. **Sunday 10pm** — Full pull from both stores
2. **Wednesday 10pm** — Mid-week check for new receipts

Both crons:
1. **Notify Ted first** — send a message asking him to verify browser is logged in
2. **Navigate to store purchase history** — Harris Teeter at harristeeter.com/mypurchases, Sam's Club at samsclub.com/orders
3. **Extract new items** — compare against existing ledger, only add new orders
4. **Append to ledger** — `/Volumes/Extra/Substrate/Commons/Substrate_Finance_Planning/27_Grocery_Item_Ledger.md`
5. **Update reconciliation table** — receipt count, item total, receipt total, difference
6. **Send summary** — what was added or "No new receipts this week"

## Cron Prompt Template

```
Grocery Receipt Pull — [Day] [Time]

You need to pull grocery receipt data from Harris Teeter and Sam's Club for the past week.

IMPORTANT: Send Ted a message first asking him to make sure the browser is active and
logged in to both stores.

Steps for Harris Teeter:
1. Navigate to https://www.harristeeter.com/mypurchases
2. Check for orders since the last entry in the ledger
3. For each new order, click into the detail page and extract all items

Steps for Sam's Club (PRINT VIEW method — preferred):
1. Navigate to https://www.samsclub.com/orders
2. Check for new orders since last pull
3. For each new order:
   a. Click "View details" button
   b. Click "Print receipt" button (triggers print-optimized view with all items visible)
   c. Extract items: querySelectorAll('.print-items-list .flex.justify-between')
   d. Parse: name before "Qty", qty from "Qty N", price is last $XX.XX
4. Fees in .print-fees-item elements (Pickup FREE, Tax $X.XX)

Append all new items to the ledger using existing format.
Update reconciliation table.

If no new orders exist, send Ted a message saying "No new receipts this week."
```

## Ted's Stores

- **Harris Teeter**: Village at Chestnut Street, 136 Merrimon Ave, Asheville NC 28801
- **Sam's Club**: Asheville Sam's Club at 645 PATTON AVE, Asheville NC 28806
- **Loyalty ID**: •••• 1168 (Harris Teeter)
- **Sam's Club membership**: since 2024

## Ledger Format

```
|| Date | Store | Receipt | Item raw | Item normalized | Group | Qty | Unit | Paid | Confidence | Notes ||
```

Groups: protein, produce/fruit, produce/vegetable, dairy/ingredient, dairy/snack, pantry/antipasto, pantry/meal-base, pantry/dip, pantry/condiment, frozen/staple, frozen/protein, snack, dessert/snack, beverage/pantry, household/non-food, prepared/convenience

## Reconciliation Table

```
| Receipt | Item rows | Item total | Receipt subtotal | Difference |
|---|---:|---:|---:|---:|
| `29_Harris_Teeter_Receipt_2026-06-14` | 17 | $76.52 | $78.05 | $1.53 |
| `38_Sams_Club_Order_2026-06-27` | 17 | $204.39 | $208.40 | $4.01 |
| `HT_Pickup_2026-06-27` | 12 | $41.89 | $41.89 | $0.00 |
```

## Cron Job IDs

- **Sunday**: `8696f134a086` — `0 22 * * 0` (every Sunday at 10pm)
- **Wednesday**: `2a4d5f3a7d18` — `0 22 * * 3` (every Wednesday at 10pm)

## Notification Pattern

Crons send messages to Ted via the `deliver: "origin"` setting, which routes to the current chat (Telegram). The first message asks Ted to verify login. If Ted doesn't respond, the cron proceeds anyway (the Hermes Chrome profile is usually still logged in).
