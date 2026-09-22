# YNAB Writeback: Scraped Balance Sync Pattern

Extends the Control dashboard's `ynab_writeback.py` to automatically sync
off-budget tracking accounts (Fundrise, Webull Cash, etc.) by storing
scraped balances in a `scrape_balances` table in `system.db`.

## Architecture

```
CDP browser login → scraper script → system.db scrape_balances → ynab_writeback.py → YNAB API
         └─ 7am cron ────┘                  └─ 8am cron ────────────┘
```

## Adding a new scrape-based account

### 1. Create a scraper script

Pattern: `scripts/<name>_scraper.py` in the profile's scripts dir:

```python
# CDP cookie bridge: extract cookies from running CDP browser → save
# Then in the scraper: load cookies, navigate, extract balance
async def scrape():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(...)
        if COOKIE_FILE.exists():
            with open(COOKIE_FILE) as f:
                await context.add_cookies(json.load(f))
        await page.goto(DASHBOARD_URL, ...)
        # extract balance via page.evaluate("document.body.innerText")
        # parse with regex for the balance pattern
```

### 2. Save to scrape_balances table

```python
conn.execute(
    "CREATE TABLE IF NOT EXISTS scrape_balances "
    "(source TEXT PRIMARY KEY, balance_cents INTEGER, updated_at TEXT)"
)
conn.execute(
    "INSERT OR REPLACE INTO scrape_balances (source, balance_cents, updated_at) "
    "VALUES (?, ?, ?)",
    ("fundrise", value_cents, datetime.now(timezone.utc).isoformat())
)
```

The `source` key should match the YNAB account name in lowercase with spaces → underscores
(e.g. "Webull Cash" → "webull_cash").

### 3. Add mapping to ynab_writeback.py

```python
ACCOUNT_MAPPINGS = [
    ...
    ("scrape:fundrise", "Fundrise"),
]
```

The `_live_total` function already handles `scrape:` sources by reading from `scrape_balances`.
It falls back to the current YNAB balance (no-op) if no scrape data exists.

### 4. Create crons

```bash
# Scraper: daily before writeback (e.g. 7am)
cronjob action=create name=<name>-balance-scraper script=<name>_scraper.py \
    schedule="0 7 * * *" no_agent=true deliver=local

# Writeback: daily (e.g. 8am) — picks up scrape_balances + holdings + coinbase
cronjob action=create name=ynab-writeback script=ynab_writeback_cron.sh \
    schedule="0 8 * * *" no_agent=true deliver=local
```

## Current accounts

| Source | YNAB Account | Data method |
|--------|-------------|-------------|
| `holdings:Webull Invested` | Webull Invested | holdings table (price * shares) |
| `holdings:SoFi Invest` | SoFi Invest | holdings table (price * shares) |
| `coinbase` | Coinbase | coinbase_accounts table (sum) |
| `scrape:fundrise` | Fundrise | fundrise_scraper → scrape_balances ✅ ($130.12) |
| `scrape:webull_cash` | Webull Cash | CDP harvest → scrape_balances ✅ ($1,304) — Manual unlock required, no cron automation |
| `coinbase_wallet` | Coinbase Wallet | (needs coinbase_wallet_accounts table — separate self-custody wallet app. $9.99, under writeback threshold) |
| `scrape:sofi_checking` | (not in YNAB) | Checking $0.10, Savings $0.00 — not worth syncing. Cookies saved at `/tmp/sofi_cookies.json` |

## Key files

- `/Users/ted/Control/backend/scripts/ynab_writeback.py` — the writeback engine
- `/Users/ted/Control/backend/scripts/ynab_pull.py` — pulls YNAB data INTO system.db
- `/Users/ted/Control/backend/.env` — YNAB_TOKEN
- `scripts/fundrise_scraper.py` — Fundrise scraper (7am daily cron)
- `scripts/ynab_writeback_cron.sh` — cron wrapper for writeback (8am daily)
