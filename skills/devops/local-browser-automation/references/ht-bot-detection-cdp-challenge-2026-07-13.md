# HT Bot Detection — CDP "Click and Hold" Challenge (2026-07-13)

During a live HT shopping session, the site threw a "click and hold to prove you're human" CAPTCHA challenge. After investigation:

## Root Cause
The CDP browser's `--remote-debugging-port=9222` flag is a detectable automation signal. Harris Teeter (via Akamai bot protection) flags it and serves challenges.

## Symptoms
- Intermittent CAPTCHA challenges ("click and hold")
- Clicks not registering on React SPA components
- Search returning "no results" even for valid queries (may also be CDP fingerprinting, not just the SPA quirk)
- Erratic element targeting in DOM queries

## What Was Attempted
1. **CDP WebSocket native approach** — worked for basic page reads and cookie extraction, but triggered bot challenges during active shopping (adding to cart, checkout).
2. **Header-based API calls** — `x-kroger-channel: WEB` was discovered as the correct header for HT's first-party API. The order-list endpoint (`GET /atlas/v1/post-order/v1/purchase-history-search`) works. The item-detail endpoint (`POST /atlas/v1/purchase-history/v2/details`) could not be fully resolved (schema validation error, not the MISSING_CHANNEL issue).
3. **Page-based API call from JS context** — same `MISSING_CHANNEL` error resolved with the header, but `body must be an array` / `body[0] does not match any of the allowed types` persisted.

## Current State
The DOM-based scraper (navigate to order detail page, read rendered HTML) works for getting item-level data. The API is not needed for the data we need — the page already renders everything. Documented in case the DOM approach breaks from a site redesign.

## Recommendation for Future
If DOM scraping breaks: capture the actual API request the site's own JS makes when clicking into an order detail view. The `x-kroger-channel: WEB` header is confirmed correct. The body schema is the remaining unknown.
