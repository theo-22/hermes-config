# Installed UI Action Feedback Proof

Use this reference when an installed interface action claims to show meaningful
pending, success, and error feedback, but one or more branches cannot be
reached safely against the current live target.

## What This Proves

A controlled response through the installed browser consumer can prove:

- the real served bundle issues the expected request;
- the pending state appears while that request is unresolved;
- success and structured failure bodies reach the client handler;
- the visible result, accessibility announcement, and retry control render;
- the handler does not throw an unintended client-side exception.

It does **not** prove that the backend, launcher, service manager, or external
system performed the action. Pair it with live read-only state or a safe real
action before claiming those layers.

Call the result **controlled-response rendered-client proof**. Do not call it
end-to-end proof.

## Preconditions

1. Resolve the installed consumer URL and served artifact. A development server
   or component harness is lower-layer evidence unless it is the real consumer.
2. Read the action's real request shape and success/failure contract.
3. Check live target state first. Do not stop, degrade, or restart a healthy
   production dependency merely to make a button or error branch appear.
4. Preserve unrelated browser state. Use an isolated browser session when
   interception would affect other tabs or requests.

## Proof Matrix

Exercise the same visible action through the same installed UI for each row.

| Branch | Controlled response | Required observation |
|---|---|---|
| Pending | Delay resolution long enough to inspect | Action is disabled or guarded; specific progress text appears |
| Success | Return the action's real success status/body shape | Specific success state appears and no client exception occurs |
| Structured error | Return the real non-success status/body shape | Backend detail appears; retry or safe recovery control is available |
| Network error | Abort or disconnect, when relevant | Network failure is distinguishable from a backend rejection |

Pending and success should be one continuous probe when practical: observe the
pending state before releasing the delayed success response, then observe the
success state after resolution.

## Canonical Workflow

1. **State the visible contract.** Name the action, installed page, request,
   pending text, success text, failure detail, and recovery control.
2. **Load the installed UI normally.** Confirm the current bundle or asset hash
   when the server uses compiled artifacts.
3. **Expose the action without mutating production.** When the button appears
   only for a stopped, missing, or degraded target, control the read-only status
   response in the browser so only that target appears eligible.
4. **Control only the action response.** Keep unrelated API calls live. Match
   the exact action URL and method narrowly.
5. **Run the proof matrix.** Snapshot or query the rendered text and controls at
   each state boundary.
6. **Inspect the browser console.** A visible label can render briefly even when
   the handler throws afterward. Treat any new action-path exception as a
   failure and trace it before accepting the UI.
7. **Check request behavior.** Confirm one click issues one request, repeated
   clicks are guarded while pending, and Retry creates a new attempt.
8. **Test stale-state safety when the implementation uses timers.** A cleanup
   from an older request must not erase a newer request's state. Request IDs or
   equivalent current-attempt checks should win over timer order.
9. **Remove interception and reload.** Confirm the real live target and page
   return to their unmodified state. Clean up disposable browser artifacts.
10. **Report layers separately.** Record build/static proof, served-artifact
    proof, controlled-response rendered-client proof, real backend/service
    proof, and any still-pending fresh-client or human acceptance.

## Playwright Runtime Note

Playwright network routing is one suitable mechanic. Install routes before
reloading the page, narrow them to the status/action endpoints under test, and
use a delayed fulfillment for the pending branch. Interact from a fresh page
snapshot or stable accessibility locator, then inspect rendered text and the
console.

Illustrative shape only:

```js
await page.route('**/api/status', statusWithOneEligibleTarget);
await page.route('**/api/action/target', async route => {
  await page.waitForTimeout(800);
  await route.fulfill({ status: 200, json: successBody });
});
await page.reload();
```

Use the runtime's supported browser tooling when Playwright is unavailable;
preserve the same proof contract and boundary labels.

## Evidence Receipt

Record:

- installed URL and served artifact or bundle identifier;
- action endpoint and method;
- live target state before and after;
- exact pending, success, and error observations;
- console errors introduced by each probe;
- which responses were controlled;
- which backend/service layers were actually live-proven;
- cleanup result and any remaining acceptance gate.

## Failure Modes

- stopping a healthy dependency solely to expose the action;
- mocking the entire application so the installed consumer is never exercised;
- intercepting broad URL patterns that make unrelated data synthetic;
- asserting success from a toast while the inline action state remains stale;
- ignoring a console exception because the expected text appeared first;
- reporting controlled browser fulfillment as a real service restart or write;
- leaving routes, browser artifacts, or synthetic state active after proof.

## Proven Origin

This method was extracted from work item #615. The installed Wall dashboard's
Gallery action was tested without stopping the healthy Gallery service. A
delayed controlled success proved `Starting…` then `Started ✓`; a controlled
HTTP 500 proved detailed failure plus Retry. Console inspection exposed a
separate missing callback return that caused both result branches to throw—an
error a successful build alone did not reveal.
