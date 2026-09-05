---
name: repair-model-visible-token-transport
description: "Repair tool calls blocked before server receipt because JWTs, API keys, or signed capsules appear in model-authored arguments. Use when a client or safety layer rejects a call before the connector logs it, or raw bearer values should move behind server-resolved handles."
metadata:
  category: meta
  write_mode: file
  one_line_use: move blocked token arguments behind server-resolved opaque handles
  fast_pick: "yes"
---

# Repair Model-Visible Token Transport

## Overview

Repair the transport boundary, not the authorization design. Replace a credential-shaped value in model-visible tool arguments with a short opaque handle that the server resolves back to the original protected token before running the existing validation path.

Use `$verify-real-invocation-path` for installed-consumer and fresh-client proof.

## Boundaries

- First prove where the call stops. A client or platform block leaves no matching server receipt; a schema or server rejection does.
- Preserve the original token's role, scope, tool, expiry, restart, replay, and refresh semantics unless the user explicitly authorizes a policy change.
- Do not treat the handle as identity or authority. It is only a lookup key for the server-side token.
- Keep signed tokens and credentials out of tool responses, schemas, receipts, and logs. Redact exact handles from durable evidence too.
- Reject legacy raw tokens after migration unless compatibility is explicitly required and separately risk-reviewed.
- Do not misdiagnose token-free calls. If a read call with no credential-shaped argument is blocked, investigate dispatcher name, schema, or content separately.

## Workflow

### 1. Establish the failure boundary

Reproduce the exact call and inspect the connector's request, audit, and error surfaces for the same time window.

Classify the result as one of:

- client or safety layer blocked before server receipt;
- tool schema or argument serialization failure;
- server-side authentication or authorization rejection;
- downstream handler failure after authorization.

Do not change transport until this distinction is evidenced.

### 2. Record the invariants

Before editing, write down the behavior that must survive:

- role and scope binding;
- allowed-tool or mutation-class checks;
- ordinary expiry;
- process, boot, or restart invalidation;
- one-time use or replay behavior, if any;
- refresh endpoint, grace period, and renewal rules;
- omission, malformed value, and wrong-role failure behavior.

These invariants are the acceptance criteria.

### 3. Choose the narrowest transport

For a stateless request transport, prefer a short opaque server-resolved handle. Use implicit session binding only when the live client supplies a stable, authenticated session identity and that architecture is explicitly in scope.

For multi-process or load-balanced servers, an in-memory per-process registry is unsafe unless requests are sticky. Use a shared TTL store or an equivalent routing guarantee.

### 4. Implement the registry

Generate a cryptographically random, non-credential-shaped handle such as `cap_...`. Map it server-side to the signed token and a retention deadline.

Conceptually:

```text
handle = "cap_" + secure_random()
registry[handle] = (signed_token, retention_deadline)
token = registry.resolve(handle)
verify_existing_token(token, requested_tool, now)
```

Required properties:

- collision checking and concurrency safety;
- bounded retention and pruning;
- process-local invalidation on restart when restart invalidation is an invariant;
- no signed token in the model-visible response;
- no raw-token fallback in the resolver;
- sufficient retention to preserve an authorized refresh grace path without making ordinary expired-token use valid.

Keeping the existing argument field name can be appropriate when it avoids a fleet-wide schema migration, but its description must state that the value is an opaque handle, not a token.

### 5. Resolve before existing validation

Resolve the handle at the authorization boundary, then send the recovered token through the existing verifier unchanged.

Ensure:

- omitted or empty handle returns the established required-activation error;
- unknown, stale, or pre-restart handle fails closed;
- raw signed tokens are rejected;
- wrong role, scope, or tool still fails in the existing verifier;
- the authorization-only argument is removed before handler invocation;
- every protected mutator inherits the same schema and enforcement path.

### 6. Reconcile capability truth

Update tool descriptions, discovery output, operator documentation, probes, and receipts so they consistently describe an opaque handle backed by server-side state. Never publish an exact bearer value as proof.

### 7. Verify in layers

Run focused tests for:

- prefix and dot-free handle shape;
- raw internal token absent from responses;
- valid, invalid, missing, expired, tampered, wrong-role, and wrong-scope cases;
- stale handle after restart;
- refresh and grace behavior;
- schema coverage across all protected tools.

Then perform paired live probes against the same write-shaped tool:

1. An invalid handle must reach the connector and fail authorization.
2. A freshly issued handle must pass authorization and reach a deliberately chosen downstream validation failure that makes no mutation.

Finally verify the installed launcher or service, public discovery surface, an actual model-authored tool call, and—when required—a genuinely fresh client. Keep implementation proof, independent review, and fresh-client acceptance as separate verdicts.

### 8. Use an alternate transport when the model client preflights the proof away

If the ordinary model client declares the authorization field required, omitting it may fail locally before dispatch. That proves client containment, but not the live server boundary. Close that evidence gap with a genuinely fresh raw-protocol client:

1. Start a new process and connection against the exact installed/public role-scoped endpoint.
2. Confirm the server identity and expected protected tool through live discovery.
3. Mint a fresh opaque handle; redact it from output and durable evidence.
4. Call one protected mutator with safe, ordinary-looking nonexistent or non-allowlisted arguments and omit the handle.
5. Repeat the identical call with the valid handle.
6. Prove from the client implementation, an outbound trace, or a server receipt that the first call was actually sent. Do not assume a “raw” SDK skips input validation.

Accept the pair only when:

- the missing-handle call returns from the live protocol/server boundary with the established schema or authorization rejection;
- the valid-handle control crosses activation and reaches a deterministic downstream validation failure;
- neither call can write, execute, or otherwise mutate production state.

This is a boundary probe, not a replacement for the model-authored fresh-client leg. Record which client produced each verdict and combine evidence layers explicitly.

## Decision Guide

| Observed condition | Appropriate move |
|---|---|
| Raw token is blocked and transport is stateless | Use an opaque server-side handle |
| Stable authenticated session identity exists | Consider session binding only with explicit architecture approval |
| Token-free call is also blocked | Investigate dispatcher, schema, or content; this skill is not sufficient |
| Server has multiple workers | Use a shared TTL registry or guaranteed sticky routing |

## Failure Modes

- Re-encoding or obfuscating the raw token while still exposing it to the model.
- Letting the handle bypass expiry, role, scope, tool, or restart checks.
- Logging the exact handle or its mapped token.
- Quietly accepting both handles and legacy raw tokens.
- Claiming session binding on a transport with no trustworthy session identity.
- Treating a health check, unit test, or warm client as complete invocation-path proof.
- Calling through a raw SDK without verifying whether that SDK validates arguments locally before sending.
- Collapsing local implementation success and fresh-client acceptance into one verdict.

## Proven Pattern

This pattern was established during the 2026-08-09 role-activation repair: credential-shaped signed capsules were replaced by `cap_...` handles while the original server-side validation remained authoritative. The repair covered 75 protected mutating tools across 15 roles and passed a live Analyst start/write-shaped probe.

The alternate-transport acceptance extension was proven on 2026-08-13 for Codex Builder. A fresh Python MCP client was verified to send `tools/call` without local input-schema validation: omission was rejected at the live MCP server boundary, while the identical call with a fresh handle crossed activation and stopped at the execution allowlist, with no write or execution.

For that concrete implementation and its doctrine, consult:

- `/Volumes/Extra/Substrate/_shared/Role_Activation_Capsule.md`
- `/Volumes/Extra/Substrate/_AI_Inbox/2026-08-09_codex_return_role_activation_opaque_handle_transport_repair.md` (retired in the 2026-08-19 archive rotation; no longer on disk)
- `/Volumes/Extra/Substrate/_AI_Inbox/response_codex_builder_missing_handle_alternate_transport_acceptance_2026-08-13.md` (retired in the 2026-08-19 archive rotation; no longer on disk)

Treat these as an example, not as permission to copy role-specific names or architecture into another runtime.

## Related Skills

- `$verify-real-invocation-path`: prove the installed consumer, restart path, and fresh client.
- `$repair-capability-truth`: use when the main defect is disagreement among live schema, documentation, and callable capability.
- `$repair-mcp-client-disconnects`: use for transport disconnect handling, not pre-server safety blocking.
