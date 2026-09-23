#!/usr/bin/env python3
"""put_on_tv.py — push any URL onto a named display via the shared CDP Chrome (port 9223).

Instrumentation, promoted fleet-shared 2026-09-22 (Model Management room, Ted: "everybody
shares, no reservation"). Origin: CC's 2026-08-01 demo on the 55" (deliberately CC-only
then; lineage recorded on Concept Graph node 24).

Design (Ted's spaces principle): the TV is a SHARED display surface, never reserved.
Default push = a normal, movable window placed on the TV — arrangement, not hijack.
Fullscreen is an explicit opt-in (--fullscreen) for genuine take-the-screen moments.

Multi-window contention rules (built in before first cron consumer):
  - Scheduled pushes open as movable windows alongside existing output.
  - --reuse updates an existing TV window in place instead of stacking a new one.
  - --slot N minutes = temporary slot: on expiry (checked lazily by the next push)
    the previous content is restored automatically.

Usage:
  python3 put_on_tv.py <url> [--screen 55P605] [--windowed] [--fullscreen]
                       [--reuse] [--slot MINUTES] [--list] [--restore ID]
  python3 put_on_tv.py --list        # NSScreen geometry (y-up, as macOS reports)
  python3 put_on_tv.py --restore <windowId>   # window -> normal state

Proven recipe (2026-09-22, advisor, live-verified on the TCL 55P605):
  1. Display geometry: NSScreen reports y-UP from bottom-left; CDP Browser.setWindowBounds
     wants y-DOWN from top-left of the main display. Convert: cdp_top = main_height -
     (screen_y + screen_height).
  2. Chrome insets every window 31px (menu bar) and macOS may auto-hide Dock/menu on the
     target display — expect reported bounds slightly inside the screen. Correct; don't "fix".
  3. Sequence matters: set windowState normal -> THEN position-only (no windowState key in
     same call, or Chrome clamps to main display) -> THEN windowState fullscreen (only if
     --fullscreen). Fullscreen follows the display the window currently sits on.
  4. websocket-client must connect with suppress_origin=True (Chrome 403s Origin-bearing
     handshakes); the `websockets` library works unmodified.
"""
import argparse, json, os, subprocess, sys, time, urllib.request

CDP_HTTP = "http://127.0.0.1:9223"
STATE_FILE = os.path.expanduser("~/.hermes/cache/tv_push_state.json")
DEFAULT_SCREEN = "55P605"


def screens():
    """JXA/NSScreen probe: [{name,x,y,w,h}] with y-up coords."""
    script = (
        'ObjC.import("AppKit");const s=$.NSScreen.screens;let o=[];'
        "for(let i=0;i<s.count;i++){const c=s.objectAtIndex(i),f=c.frame;"
        "o.push({name:String(c.localizedName.js||c.localizedName),x:f.origin.x,y:f.origin.y,"
        "w:f.size.width,h:f.size.height});}JSON.stringify(o);"
    )
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", script],
                         capture_output=True, text=True).stdout.strip()
    return json.loads(out)


def cdp_ws():
    ver = json.loads(urllib.request.urlopen(f"{CDP_HTTP}/json/version", timeout=5).read())
    import websocket
    return websocket.create_connection(ver["webSocketDebuggerUrl"], timeout=15, suppress_origin=True)


class Cdp:
    def __init__(self):
        self.ws, self.mid = cdp_ws(), 0

    def call(self, method, params=None):
        self.mid += 1
        self.ws.send(json.dumps({"id": self.mid, "method": method, "params": params or {}}))
        while True:
            d = json.loads(self.ws.recv())
            if d.get("id") == self.mid:
                return d


def tab_ws(target_id):
    """Per-tab websocket (for Page.navigate without a browser-level session)."""
    tabs = json.loads(urllib.request.urlopen(f"{CDP_HTTP}/json", timeout=5).read())
    for t in tabs:
        if t.get("id") == target_id and t.get("webSocketDebuggerUrl"):
            import websocket
            return websocket.create_connection(t["webSocketDebuggerUrl"], timeout=15,
                                               suppress_origin=True)
    return None


def tab_navigate(target_id, url):
    ws = tab_ws(target_id)
    if not ws:
        return False
    ws.send(json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": url}}))
    try:
        ws.settimeout(5)
        ws.recv()
    except Exception:
        pass
    ws.close()
    return True


def tv_bounds(name):
    scr = screens()
    main = scr[0]  # first entry is main (0,0)
    tv = next((s for s in scr if s["name"] == name), None)
    if not tv:
        names = ", ".join(s["name"] for s in scr)
        sys.exit(f"screen {name!r} not found. Screens: {names}")
    return {"left": tv["x"], "top": main["h"] - (tv["y"] + tv["h"]),
            "width": tv["w"], "height": tv["h"]}


def on_screen(bounds, screen_bounds):
    """Window bounds sit (mostly) on the named screen?"""
    return (bounds.get("left", 99999) <= screen_bounds["left"] + 150
            and bounds.get("left", -99999) >= screen_bounds["left"] - 150
            and bounds.get("top", 99999) <= screen_bounds["top"] + 150)


def find_tv_windows(c, b):
    """All page windows currently living on the TV screen: [(targetId, windowId, url)]."""
    out = []
    tabs = json.loads(urllib.request.urlopen(f"{CDP_HTTP}/json", timeout=5).read())
    for t in tabs:
        if t.get("type") != "page":
            continue
        r = c.call("Browser.getWindowForTarget", {"targetId": t["id"]})
        wid = r.get("result", {}).get("windowId")
        if not wid:
            continue
        wb = c.call("Browser.getWindowBounds", {"windowId": wid})["result"]["bounds"]
        if on_screen(wb, b):
            out.append((t["id"], wid, t.get("url", "")))
    return out


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(st):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(st, f)


def expire_due_slots(c, b):
    """Lazy slot expiry: restore any slot whose window is gone or whose time is up."""
    st = load_state()
    slots = st.get("slots", [])
    live = []
    changed = False
    now = time.time()
    tv_wins = find_tv_windows(c, b)
    for s in slots:
        expired = s.get("expires_at", 0) and now >= s["expires_at"]
        # window must still exist AND still hold our pushed content — a live user may
        # have reused the window for their own page; never clobber it (yield-to-live).
        win = next((w for w in tv_wins if w[1] == s["windowId"]), None)
        import urllib.parse as _up
        ours = bool(win) and _up.unquote(win[2]) == _up.unquote(s.get("pushed_url") or "")
        if expired or not win:
            changed = True
            if expired and ours and s.get("prev_url"):
                tab_navigate(s["targetId"], s["prev_url"])  # restore previous content
            # reused window (content changed) -> drop slot silently; gone window -> nothing
        else:
            live.append(s)
    if changed:
        st["slots"] = live
        save_state(st)
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", nargs="?", help="URL or data: page to display")
    ap.add_argument("--screen", default=DEFAULT_SCREEN)
    ap.add_argument("--windowed", action="store_true", default=True,
                    help="(default) place a normal movable window on the TV — no hijack")
    ap.add_argument("--fullscreen", action="store_true",
                    help="explicit fullscreen takeover of the TV (old behavior)")
    ap.add_argument("--reuse", action="store_true",
                    help="update an existing TV window in place instead of stacking")
    ap.add_argument("--slot", type=float, metavar="MINUTES",
                    help="temporary slot: auto-restore previous content after N minutes")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--restore", type=int, metavar="WINDOW_ID")
    args = ap.parse_args()

    if args.list:
        print(json.dumps(screens(), indent=1))
        return
    if args.restore:
        c = Cdp()
        c.call("Browser.setWindowBounds", {"windowId": args.restore, "bounds": {"windowState": "normal"}})
        print(f"window {args.restore} restored to normal")
        return
    if not args.url:
        ap.error("need a url (or --list / --restore)")

    b = tv_bounds(args.screen)
    c = Cdp()
    expire_due_slots(c, b)  # lazy sweep before every push

    tid = wid = prev_url = None
    tv_wins = find_tv_windows(c, b)

    if args.reuse and tv_wins:
        tid, wid, prev_url = tv_wins[0]
        tab_navigate(tid, args.url)
    else:
        prev_url = tv_wins[0][2] if tv_wins else None
        r = c.call("Target.createTarget", {"url": args.url, "newWindow": True})
        tid = r["result"]["targetId"]
        wid = c.call("Browser.getWindowForTarget", {"targetId": tid})["result"]["windowId"]

    time.sleep(1.2)
    c.call("Browser.setWindowBounds", {"windowId": wid, "bounds": {"windowState": "normal"}})
    time.sleep(0.4)
    c.call("Browser.setWindowBounds", {"windowId": wid, "bounds": b})  # position onto TV
    time.sleep(0.4)
    if args.fullscreen:
        c.call("Browser.setWindowBounds", {"windowId": wid, "bounds": {"windowState": "fullscreen"}})
    time.sleep(0.8)
    got = c.call("Browser.getWindowBounds", {"windowId": wid})["result"]["bounds"]
    on_tv = on_screen(got, b)

    if args.slot:
        st = load_state()
        st.setdefault("slots", [])
        st["slots"] = [s for s in st["slots"] if s["windowId"] != wid]
        st["slots"].append({"windowId": wid, "targetId": tid, "screen": args.screen,
                            "prev_url": prev_url, "pushed_url": args.url,
                            "expires_at": time.time() + args.slot * 60})
        save_state(st)

    print(json.dumps({"windowId": wid, "targetId": tid, "mode": "fullscreen" if args.fullscreen
                      else "windowed", "slot_min": args.slot, "bounds": got, "on_tv": on_tv}))
    sys.exit(0 if on_tv else 1)


if __name__ == "__main__":
    main()
