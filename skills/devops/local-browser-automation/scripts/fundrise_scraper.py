#!/usr/bin/env python3
"""
Fundrise Balance Scraper — CDP via browser-scanner Chrome (port 9222).

Auto-launches the browser if not running, scrapes portfolio value from
the Fundrise account page, and writes to system.db for YNAB writeback.
Includes explicit URL verification after tab connect — navigates to Fundrise
if the launched tab landed elsewhere (common when Chrome restores a prior session tab).

Cron: fundrise-balance-scraper (daily 7am, no-agent)
"""
import asyncio, json, os, re, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
import websockets

CDP_HTTP = "http://127.0.0.1:9222"
DASHBOARD_URL = "https://fundrise.com/account"
BALANCE_FILE = Path("/tmp/fundrise_balance.json")
CHROME_PATH = "/Volumes/Extra/Apps/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE_DIR = "/Users/ted/Library/Application Support/Browser_Profiles/hermes-browser"


def ensure_browser():
    """Ensure CDP browser is running. Launch if not."""
    try:
        urlopen(f"{CDP_HTTP}/json/version", timeout=3)
        return
    except Exception:
        pass

    print("[fundrise] Launching browser...")
    subprocess.Popen(
        [CHROME_PATH,
         f"--remote-debugging-port=9222",
         f"--user-data-dir={PROFILE_DIR}",
         "--no-first-run",
         "--new-window", DASHBOARD_URL],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    for _ in range(40):
        time.sleep(0.5)
        try:
            urlopen(f"{CDP_HTTP}/json/version", timeout=2)
            print("[fundrise] Browser ready")
            return
        except Exception:
            continue
    raise RuntimeError("Browser did not start")


def find_tab_ws():
    """Find a Fundrise tab or create one."""
    tabs = json.loads(urlopen(f"{CDP_HTTP}/json", timeout=10).read())
    for t in tabs:
        if t.get("type") == "page" and "fundrise.com/account" in t.get("url", ""):
            return t["webSocketDebuggerUrl"], t["id"]
    # Fallback: create new tab
    req = urlopen(Request(f"{CDP_HTTP}/json/new?{DASHBOARD_URL}", method="PUT"), timeout=10)
    tab = json.loads(req.read())
    return tab["webSocketDebuggerUrl"], tab["id"]


async def main():
    try:
        ensure_browser()
    except RuntimeError as e:
        print(f"[fundrise] {e}")
        return 1

    ws_url, target_id = find_tab_ws()
    if not ws_url:
        print("[fundrise] No page tab available")
        return 1

    print(f"[fundrise] Tab: {target_id[:16]}")

    msg_id = 0

    async def cdp(method, params=None):
        nonlocal msg_id
        msg_id += 1
        payload = json.dumps({"id": msg_id, "method": method, "params": params or {}})
        await ws.send(payload)
        while True:
            raw = await ws.recv()
            data = json.loads(raw)
            if data.get("id") == msg_id:
                return data

    async def evaluate(js):
        r = await cdp("Runtime.evaluate", {
            "expression": js, "returnByValue": True
        })
        return r.get("result", {}).get("result", {}).get("value")

    async with websockets.connect(ws_url) as ws:
        await cdp("Page.enable")

        # Verify the tab actually landed on Fundrise — Chrome may restore
        # a previous session tab instead of the --new-window URL.
        # Explicitly navigate if needed.
        current_url = await evaluate("window.location.href")
        if current_url and "fundrise.com" not in current_url:
            print(f"[fundrise] Tab is on {current_url.split('/')[2] if current_url else 'unknown'} — navigating to Fundrise...")
            await cdp("Page.navigate", {"url": DASHBOARD_URL})
            await asyncio.sleep(8)
            body = await evaluate("document.body?.innerText || ''")
            if body and ("human" in body.lower() or "verify" in body.lower()):
                print("[fundrise] Bot challenge after navigation, waiting...")
                await asyncio.sleep(15)

        await asyncio.sleep(3)

        body = await evaluate("document.body?.innerText || ''")
        if not body:
            print("[fundrise] Could not read page content")
            return 1

        if "Log in" in body and "Email address" in body:
            print("[fundrise] Login required — open the browser window and log into Fundrise once")
            return 1

        if "human" in body.lower():
            print("[fundrise] Bot challenge detected, waiting...")
            await asyncio.sleep(15)
            body = await evaluate("document.body?.innerText || ''")

        m = re.search(r'Account value\s+\$?([\d,.]+)', body)
        if not m:
            print("[fundrise] Could not find account value on page")
            title = await evaluate("document.title")
            print(f"  Title: {title}")
            print("  Preview:", body[:500])
            return 1

        value_str = m.group(1).replace(",", "")
        value_cents = int(round(float(value_str) * 100))

    # Write to system.db
    sys.path.insert(0, os.path.expanduser("~/Control/backend"))
    try:
        import system_db
        system_db.init_db()
        conn = system_db.get_db()
        conn.execute(
            "CREATE TABLE IF NOT EXISTS scrape_balances "
            "(source TEXT PRIMARY KEY, balance_cents INTEGER, updated_at TEXT)"
        )
        conn.execute(
            "INSERT OR REPLACE INTO scrape_balances (source, balance_cents, updated_at) VALUES (?, ?, ?)",
            ("fundrise", value_cents, datetime.now(timezone.utc).isoformat())
        )
        conn.commit()
        print(f"[fundrise] ${float(value_str):.2f} ({value_cents}c) — saved to system.db ✅")
    except Exception as e:
        print(f"[fundrise] DB write failed ({e}), saving to file instead")
        with open(BALANCE_FILE, "w") as f:
            json.dump({
                "source": "fundrise", "balance_cents": value_cents,
                "balance_dollars": float(value_str),
                "fetched_at": datetime.now(timezone.utc).isoformat()
            }, f, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
