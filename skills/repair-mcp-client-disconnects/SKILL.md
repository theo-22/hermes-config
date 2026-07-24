---
name: repair-mcp-client-disconnects
description: Diagnose, implement, and live-verify narrow MCP server handling for normal SSE or streamable-HTTP client disconnects. Use when an MCP bridge logs AnyIO ClosedResourceError, EndOfStream, BrokenPipeError, ConnectionResetError, ExceptionGroup failures, unhandled ASGI disconnect errors, intermittent bridge restarts, or post-disconnect hangs.
category: meta
write_mode: file
one_line_use: narrowly repair and live-prove normal MCP client disconnect handling
fast_pick: "no"
---

# Repair MCP Client Disconnects

Repair expected client-disconnect handling without hiding server faults, cancellation, or dependency failures.

## Establish authority and live state

1. Start from the routed diagnosis or handoff.
2. Resolve the active service's real script path from `launchctl print` and `ps`; do not trust a stale repository path.
3. Record the initial PID, health response, relevant log line counts, installed Python/MCP/AnyIO/Starlette versions, and dirty-worktree state.
4. Claim shared target files before writing. Preserve unrelated work and use partial staging if the target file contains interleaved changes.
5. Stop if the live fault originates outside the authorized handlers or requires dependency changes.

## Implement narrow handling

Define only the expected disconnect leaves supported by the installed stack:

```python
_DISCONNECT_EXCEPTIONS = (
    BrokenPipeError,
    ConnectionResetError,
    anyio.ClosedResourceError,
    anyio.EndOfStream,
)
```

For a direct exception, suppress only this tuple. For `BaseExceptionGroup`, split by the tuple:

```python
_, remaining = group.split(
    lambda exc: isinstance(exc, _DISCONNECT_EXCEPTIONS)
)
if remaining is not None:
    raise remaining
```

Apply the same policy at both transport boundaries:

- the `mcp.run(...)` call inside the SSE connection lifecycle;
- the streamable-HTTP manager's `handle_request(...)` call.

Keep role or request ContextVar reset logic in `finally`.

Never:

- catch `BaseExceptionGroup` unconditionally;
- include cancellation in the disconnect tuple;
- suppress unrelated leaves from a mixed group;
- broaden into MCP library internals or dependency upgrades without new authority.

## Add focused regression tests

Prove all applicable cases:

1. Direct expected disconnect is handled.
2. All-disconnect exception group is handled.
3. Mixed exception group re-raises only the unexpected remainder.
4. Unrelated direct exception propagates.
5. Cancellation propagates.
6. ContextVar resets after handled disconnect, unrelated failure, and cancellation.
7. Both SSE and streamable-HTTP endpoints use the same policy.
8. Existing route ownership, authentication classification, and response lifecycle remain unchanged.

Run the focused suite, syntax compilation, and the repository's diff/static checks.

## Restart and prove live behavior

1. Restart only through the documented service command.
2. Wait for a new PID and a successful health response.
3. Use real authenticated MCP clients:
   - open SSE, confirm the stream is established, then terminate the client abruptly;
   - initialize a streamable-HTTP client, then terminate it abruptly.
4. After each disconnect, prove:
   - the service PID remains stable;
   - health responds;
   - a fresh client initializes;
   - a harmless read-only MCP call completes.
5. Inspect only the log delta captured after the baseline for new DOWN alerts, ASGI exceptions, or disconnect errors.

Do not use an incomplete oversized HTTP body as the acceptance test. That tests malformed request-body handling, not a normal initialized-client disconnect, and MCP dependencies may log their own `ClientDisconnect` or background-session error while the bridge remains alive. Record that separately and stop rather than disguising it with broader suppression.

## Return the receipt

Report:

- root cause as confirmed, revised, or not reproduced;
- exact files and functions changed;
- direct and exception-group policy;
- tests and checks;
- PID before and after restart;
- SSE and streamable-HTTP disconnect results;
- post-disconnect health and fresh-client call;
- log-delta result;
- remaining dependency-level or malformed-request risk;
- commit/push state and any preserved unrelated work.
