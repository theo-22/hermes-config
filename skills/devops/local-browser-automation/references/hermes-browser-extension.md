# Hermes Browser Extension — Setup & Security

**Repo:** https://github.com/abundantbeing/hermes-browser-extension
**Version:** v0.1.6 (alpha, not on Chrome Web Store — load unpacked only)
**License:** MIT
**Author:** Jon Komet (@abundantbeing)

## What It Is

Chrome/Edge/Chromium MV3 side panel that connects active browser tab context to a Hermes Gateway/API server. NOT a browser chatbot — talks to the real Hermes runtime to use configured models, tools, skills, sessions, memory, and MCP servers.

## Local Install

```bash
cd /Users/ted/Hermes
git clone https://github.com/abundantbeing/hermes-browser-extension.git
cd hermes-browser-extension
npm install
npm run build
# Output: dist/
```

## API Server Config

Add to `~/.hermes/profiles/<profile>/.env`:
```
API_SERVER_ENABLED=true
API_SERVER_HOST=127.0.0.1
API_SERVER_PORT=8642
API_SERVER_KEY=<random-64-char-hex>
API_SERVER_CORS_ORIGINS=*
```

**Note:** `chrome-extension://*` wildcard does NOT work for CORS in practice — the extension gets 403. Use `*` (the API is localhost-only anyway).

**Restart gateway from a SEPARATE terminal** (cannot restart from inside a Hermes session):
```bash
hermes gateway restart -p <profile>
```

Verify:
```bash
curl http://127.0.0.1:8642/health
curl -H "Authorization: Bearer <key>" http://127.0.0.1:8642/v1/models
```

### Troubleshooting 403 Errors

If the extension shows "Could not create session (403)":

1. **CORS issue** (most likely): `API_SERVER_CORS_ORIGINS=chrome-extension://*` doesn't match. Change to `*` in `.env`, restart gateway.
2. **Gateway not restarted**: The running gateway has the OLD config. Must restart from a separate terminal.
3. **Wrong key**: Verify with `curl -H "Authorization: Bearer <key>" http://127.0.0.1:8642/v1/models` — should return model list, not "Invalid API key".
4. **API server not running**: `curl http://127.0.0.1:8642/health` should return `{"status": "ok"}`.

## Load Extension

1. `chrome://extensions` → enable Developer mode
2. "Load unpacked" → select `/Users/ted/Hermes/hermes-browser-extension/dist`
3. Pin extension icon → click to open side panel
4. Enter `http://127.0.0.1:8642` + API key → Test connection

## What It Sends to Hermes

- Active tab URL + title
- Selected text
- Readable page text (wrapped as UNTRUSTED context)
- Page headings, forms, links, buttons
- Open tab titles/URLs (if enabled)
- YouTube transcripts (if available)
- Voice dictation (Hermes STT or browser speech fallback)

## Security Model

- **Read-only**: no click/type/form-submit/checkout
- No cookies, history, bookmarks, downloads, debugger, nativeMessaging
- Page content wrapped as `UNTRUSTED_BROWSER_CONTEXT_START/END`
- Redacts secrets: bearer tokens, API keys, private keys, GitHub/Slack tokens, JWTs
- Blocks sensitive pages: banking, crypto wallets, password managers, checkout/payment, health, government-tax
- API key stored in `chrome.storage.local` (masked after save)

## Quick Commands

`/summarize`, `/explain`, `/rewrite`, `/tabs`, `/action-items`

## Themes

Light/Dark/System + Nous, Midnight, Ember, Mono, Cyberpunk, Slate

## Known Issues & Fixes

### Font Size Too Small

Chrome side panels render at a small default font size. `Cmd+` zoom does NOT work in side panels. `Ctrl+scroll` works as a temporary workaround.

**Permanent fix:** Edit `extension/sidepanel.css`, change `body { font-size: ... }` to `20px` (4K monitors) or `16px` (standard). Run `npm run build`, reload at `chrome://extensions`.

### Rebuild Warning ⚠️

**Rebuilding resets the extension ID.** Chrome treats the rebuilt `dist/` as a new extension → ALL settings lost (API key, permissions, CORS, theme). ALWAYS warn Ted before rebuilding — let him decide if the change is worth reconfiguring.

### Fixing Font Size Properly

The `body` font-size change alone is NOT enough — `.message-content` has a hardcoded `font-size: 12px` that overrides everything. You must change BOTH:

1. In `extension/sidepanel.css`, find `body {` rule → set `font-size: 20px;` (4K) or `16px` (standard)
2. In the same file, find `.message-content {` rule → set `font-size: 18px;` (was 12px — this is what causes headaches during long sessions)
3. Optionally bump `.composer-help`, `.status-copy`, `.settings-button`, `.connect-actions button`, `.context-chip`, `.context-preview` from 9-11px to 14-15px

Then rebuild:
```bash
npm run build
```
Then reload at `chrome://extensions`.

**Ted's preference:** The default chat font (12px) was too small to read comfortably. 18px chat + 20px body is good for 4K monitors.
