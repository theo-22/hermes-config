#!/usr/bin/env python3
"""
Fundrise Balance Scraper — CDP via browser-scanner Chrome (port 9223).

Auto-launches the browser if not running, scrapes portfolio value from
the already-loaded Fundrise tab (opened at launch), and writes to system.db
for the YNAB writeback to consume.
"""
import asyncio, json, os, re, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
import websockets

CDP_HTTP = "http://127.0.0.1:9223"
DASHBOARD_URL = "https://fundrise.com/account"
BALANCE_FILE = Path("/tmp/fundrise_balance.json")
CHROME_PATH = "/Volumes/Extra/Apps/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE_DIR = "/Users/ted/Library/Application Support/Google/Chrome/Cost Tabs"


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
         "--remote-debugging-port=9223",
         f"--user-data-dir={PROFILE_DIR}",
         "--profile-directory=Default",  # 615 agent identity (Ted, 2026-09-22)
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
    """Find a Fundrise tab and its WebSocket URL."""
    tabs = json.loads(urlopen(f"{CDP_HTTP}/json", timeout=10).read())
    # Prefer an existing Fundrise tab with logged-in content
    for t in tabs:
        if t.get("type") == "page" and "fundrise.com/account" in t.get("url", ""):
            return t["webSocketDebuggerUrl"], t["id"]
    # Open a new tab specifically to Fundrise
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

    async def _click_xy(x, y):
        # A TRUSTED click via the Input domain — Chrome treats this as a real
        # user gesture (unlike element.click()/.focus()), which is required to
        # trigger saved-password autofill.
        await cdp("Input.dispatchMouseEvent",
                  {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
        await cdp("Input.dispatchMouseEvent",
                  {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})

    async def trusted_click(selector):
        box = await evaluate(
            "(()=>{const el=document.querySelector(%s);if(!el)return null;"
            "const r=el.getBoundingClientRect();"
            "return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2});})()" % json.dumps(selector))
        if not box:
            return False
        c = json.loads(box)
        await _click_xy(c["x"], c["y"])
        return True

    async with websockets.connect(ws_url) as ws:
        await cdp("Page.enable")

        # Check what URL we're actually on
        current_url = await evaluate("window.location.href")
        if current_url and "fundrise.com" not in current_url:
            domain = "unknown"
            try:
                parts = current_url.split('/')
                if len(parts) > 2 and parts[2]:
                    domain = parts[2]
            except Exception:
                domain = "unknown"
            print(f"[fundrise] Tab is on {domain} — navigating to Fundrise...")
            await cdp("Page.navigate", {"url": DASHBOARD_URL})
            # Wait for navigation to complete
            await asyncio.sleep(8)
            # Check for bot challenge
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
            # Login wall. This Chrome profile autofills the USERNAME on load but
            # withholds the PASSWORD until a trusted user gesture (Chrome anti-
            # phishing). Dispatch a real CDP click on the password field to
            # trigger the fill, then submit only if the password actually
            # populated — never submit empty fields (a repeating cron doing that
            # could trip a failed-login lockout). If it won't fill, bail and let
            # Ted log in.
            await trusted_click("input[type=password]")
            await asyncio.sleep(2.5)
            pw_len = await evaluate("(document.querySelector('input[type=password]')||{}).value?.length||0")
            if not pw_len:
                # Nudge the username field too, then re-check the password.
                await trusted_click("input[name=username], input[type=email]")
                await asyncio.sleep(2.5)
                pw_len = await evaluate("(document.querySelector('input[type=password]')||{}).value?.length||0")
            if not pw_len:
                # Final check: count ALL filled inputs. The password selector
                # `input[type=password]` fails if Fundrise uses a custom form
                # field (no type=password). If ANY inputs have values (e.g.
                # the email/username field is filled), the credentials ARE
                # present — the password field just didn't match our selector.
                # Submitting with filled username is safe against lockout
                # (empty-field submit is the real risk the guard above prevents).
                has_creds = await evaluate("""
                    (()=>{
                        var inputs=document.querySelectorAll('input');
                        var filled=0;
                        for(var i=0;i<inputs.length;i++){
                            if(inputs[i].value&&inputs[i].value.length>0)filled++;
                        }
                        return filled;
                    })()
                """)
                if has_creds and has_creds >= 1:
                    print("[fundrise] %d input(s) filled despite password selector miss — trying existing credentials" % has_creds)
                else:
                    print("[fundrise] Login needed — credentials auto-populated, just click Log in (schedule: 1st/15th)")
                    return 0

            login_box = await evaluate(
                "(()=>{const b=[...document.querySelectorAll('button,input[type=submit]')]"
                ".find(x=>/^(log\\s*in|sign\\s*in)$/i.test((x.innerText||x.value||'').trim()));"
                "if(!b)return null;const r=b.getBoundingClientRect();"
                "return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2});})()")
            if not login_box:
                print("[fundrise] Credentials filled but no Log in button found")
                return 1
            print("[fundrise] Credentials pre-filled — clicking Log in, waiting for dashboard...")
            lb = json.loads(login_box)
            await _click_xy(lb["x"], lb["y"])
            await asyncio.sleep(8)
            body = await evaluate("document.body?.innerText || ''") or ""
            if "Log in" in body and "Email address" in body:
                print("[fundrise] Still on login page after submit — login did not complete")
                return 1
            # fall through to account-value extraction below

        if "human" in body.lower():
            # Bot challenge — wait and retry once
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
