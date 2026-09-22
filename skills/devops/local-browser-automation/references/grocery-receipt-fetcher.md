# Grocery Receipt Fetcher — Harris Teeter + Sam's Club

Production implementation for Stage 2 semi-automated grocery receipt imports.
Follows the gate in `09_Grocery_Receipt_Automation_Gate_2026-05-28.md`.

## Stores

| Store | Base URL | Login Path | Orders Path |
|-------|----------|------------|-------------|
| Harris Teeter | `https://www.harristeeter.com` | `/account/login` (redirects to `https://login.kroger.com`) | `/mypurchases` (shows Orders tab with year/month accordion) |
| Sam's Club | `https://www.samsclub.com` | `/account/login` (or `https://titan.samsclub.com`) | `/account/orders` |

## Selectors (Heuristic)

Both sites use dynamic class names. Use multiple fallback selectors:

```python
selectors_to_try = [
    "[data-testid*='order']",
    "[class*='order-history']",
    "[class*='order-card']",
    "[class*='receipt']",
    "[class*='purchase-history']",
    ".order-item",
    ".purchase-item",
    "article[class*='order']",
    "div[class*='OrderHistory']",
    "table tbody tr",
    "[role='listitem']",
    "li[class*='order']",
]
```

## Extraction Logic

1. Navigate to login → wait for signal file
2. Navigate to orders page
3. Try selectors in order until multiple elements found
4. For each element: extract text content
5. Fallback: full page text → regex for `$X.XX` + date patterns

## Signal File Pattern

```python
SIGNAL_FILE = Path("/tmp/grocery_auth_ready")

# In wait loop:
while not SIGNAL_FILE.exists():
    await asyncio.sleep(1)
SIGNAL_FILE.unlink()
```

## Stage 2 Gate Compliance

- ✅ Ted manually authenticates (visible browser)
- ✅ No credential storage
- ✅ No unattended scraping
- ✅ Item-level extraction to `27_Grocery_Item_Ledger.md`
- ✅ 4+ runs across 4 weeks before Stage 3 consideration

## Known Issues

- Harris Teeter: Login redirects to Kroger B2C at `login.kroger.com`; orders path is `/mypurchases` (not `/account/orders` or `/account/update/`)
- Sam's Club: Blocked at 2FA/OTP choice page (`identity.samsclub.com/withotpchoice`) — not a script problem, requires Ted to choose password option or disable 2FA
- Both: Dynamic rendering may need scroll/wait before extraction
- Cloud browser (Browserbase) connection unstable for OAuth redirect chains — 502 Bad Gateway errors. **Use local Playwright for login flows.**
- The old 515-line `grocery_receipt_fetcher.py` used selector guessing + modal dismissal + 8s sleeps — too fragile. Replace with focused Playwright script using known selectors (`#signInName`, `input[type="password"]`, `button[type="submit"]`).
- `login.kroger.com` root URL returns 404 — must go through `harristeeter.com/signin` redirect to get the B2C form

## Cloud Browser Tools (Fallback)

When local browser_use fails, use Hermes built-in cloud browser tools:

```python
# Navigate
await browser_navigate(url="https://login.kroger.com")

# Click by ref from snapshot
await browser_click(ref="e10")

# Type into field
await browser_type(ref="e10", text="tedhughes@me.com")

# Get full page snapshot
snapshot = await browser_snapshot(full=True)
```

These tools work reliably for manual authentication flows.

## Usage

```bash
/Users/ted/.hermes/hermes-agent/venv/bin/python3 \
  /Users/ted/.hermes/scripts/grocery_receipt_fetcher.py
```