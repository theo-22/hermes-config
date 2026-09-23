# Harris Teeter Playwright Login — Verified 2026-06-29

## Approach: Local Playwright (NOT browser_use, NOT cloud browser)

After the cloud browser (Browserbase) proved unstable for OAuth redirect chains, and the
`browser_use` approach required 515 lines of fragile selector-guessing, we tested local
async Playwright. The login form renders correctly and is straightforward.

## Verified Login Flow

```python
from playwright.async_api import async_playwright

async def harris_teeter_login(email, password):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # visible for debugging
        page = await browser.new_page()

        # Step 1: Go to Harris Teeter signin (triggers Kroger B2C redirect)
        await page.goto('https://www.harristeeter.com/signin?redirectUrl=/',
                        wait_until='domcontentloaded', timeout=30000)

        # Step 2: Wait for the B2C form to render
        # The email field has a stable ID: #signInName (type=text, NOT type=email)
        await page.wait_for_selector('#signInName', timeout=20000)

        # Step 3: Fill credentials
        await page.fill('#signInName', email)           # Kroger B2C quirk: type=text
        await page.fill('input[type="password"]', password)
        await page.click('button[type="submit"]')

        # Step 4: Wait for redirect back to harristeeter.com
        # (OAuth flow goes through login.kroger.com → onmicrosoft.com → /connect-auth)
        # Simple approach: wait for any navigatio to harristeeter.com
        for _ in range(30):
            await asyncio.sleep(2)
            if 'harristeeter.com' in page.url and 'login' not in page.url:
                break

        return browser, page  # pass to extraction logic

async def extract_purchases(page):
    await page.goto('https://www.harristeeter.com/mypurchases',
                    wait_until='domcontentloaded', timeout=30000)
    await asyncio.sleep(3)  # let dynamic content load

    # Save raw HTML for debugging
    content = await page.content()

    # Order selectors (from 2026-06-28 session):
    # [data-testid='PO-NonPendingPurchase'] for order rows
    # Each row shows: date, store type, total, item count
```

## Key Facts

| Fact | Source |
|------|--------|
| `login.kroger.com` root URL returns 404 | Live test 2026-06-29 |
| Must go through `harristeeter.com/signin` redirect to get B2C form | Live test |
| Email field `#signInName` — type=text with email validation pattern | Verified via page inspection |
| Form has "Keep me signed in" checkbox (pre-checked) | Screenshot verification |
| No modal dismissal needed — direct form load | Simpler than old script assumed |
| After login → redirect through `/connect-auth` → `/mypurchases` | OAuth fragment flow |

## Why cloud browser failed

Browserbase CDP WebSocket connection dropped during the multi-domain redirect chain
(harristeeter.com → login.kroger.com → onmicrosoft.com → back). Local Playwright
handles redirects natively without WebSocket tunneling — no connection stability issue.

## Credential Source

```python
# From Keychain module at ~/.hermes/scripts/grocery_keychain_credentials.py
from grocery_keychain_credentials import get_harris_teeter_credentials
email, password = get_harris_teeter_credentials()
```

## Output Target

Stage raw captures to: `/Volumes/Extra/Substrate/Commons/Substrate_Finance_Planning/Evidence/Grocery_Receipt_Staging/`
Format: `grocery_receipt_fetcher_playwright_capture.md` (raw) + JSON (structured)
