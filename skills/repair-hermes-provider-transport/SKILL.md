---
name: repair-hermes-provider-transport
description: Diagnose and repair an isolated Hermes OpenAI-compatible provider failure when the exact final request body succeeds through a simpler transport but fails through Hermes/OpenAI SDK/httpx. Use to trace the installed client-construction path, preserve strict request budgets, implement the narrowest profile- or process-local wire adapter, prove isolation offline, and stop before a separately authorized live qualification request.
metadata:
  category: meta
  write_mode: file
  one_line_use: isolate and repair a Hermes provider wire-path differential without widening profiles or request authority
  fast_pick: "no"
---

# Repair Hermes Provider Transport

Repair the smallest demonstrated transport boundary while preserving Hermes behavior above it and the user's live-request budget.

## When to use

Use this skill when:

- an installed Hermes profile repeatedly reaches the intended provider but fails;
- the exact serialized final request body has been captured value-safely;
- replaying that body unchanged through a simpler HTTP path succeeds; and
- provider, credential, model, endpoint, and request-body causes are therefore substantially ruled down.

The differential must be real. A hand-reconstructed body, a different endpoint, or a replay with different semantic fields does not establish a transport-only lane.

## When not to use

- Do not use this skill to repair authentication, provider routing, model selection, or prompt content before those layers are independently resolved.
- Do not treat it as authorization for a provider call, retry, fallback, S1/S2 run, production-default change, or fleet-wide transport change.
- Do not use a broad shared-client modification when a profile-local or process-local selector can contain the repair.
- Do not conflate HTTP transport with MCP filesystem fences, host path namespaces, or connector reachability; diagnose those as separate boundaries unless evidence links them.

## Canonical workflow

### 1. Freeze scope and request authority

Write down:

- the exact target profile;
- model, provider, effective base URL, and fallback policy;
- allowed outer attempts and SDK retries;
- whether any live request remains authorized; and
- explicit exclusions such as S1/S2 or other profiles.

If no live request is authorized, all verification must be static, network-disabled, or loopback-only.

### 2. Establish the same-body differential

Capture the final request body at the last safe boundary before transmission without persisting credentials. Replay the exact bytes through the smallest alternative transport that can preserve endpoint and TLS intent.

Compare only below-body variables:

- TLS trust source and SSL context;
- HTTP library and connection pooling;
- proxy/environment handling;
- redirects;
- Host, framing, compression, and protocol negotiation;
- User-Agent and SDK-added metadata headers;
- timeout and retry behavior.

A successful exact replay narrows the fault; it does not yet prove which individual transport variable caused it.

### 3. Trace the installed construction path

Inspect the actual installed invocation using its owning working directory, interpreter, selected profile home, and loader. Identify:

1. profile/config resolution;
2. provider and endpoint resolution;
3. model/default-header application;
4. OpenAI client construction;
5. `httpx.Client` or current keepalive/bootstrap construction;
6. outer retry loop and SDK retry setting; and
7. rebuild, restore, or model-switch paths that reuse the constructor.

Name current equivalents rather than assuming historical function names still own the live path.

### 4. Choose the narrowest reversible adapter

Prefer, in order:

1. process-local bootstrap injection;
2. active-profile transport selector;
3. provider-local client override;
4. shared Hermes behavior only when isolation is impossible and separately authorized.

Keep the OpenAI SDK above the adapter whenever possible so response parsing, streaming, tool calls, usage handling, and Hermes lifecycle remain normal. Replace only the final wire implementation. Make selector failures fail closed rather than silently falling back to the known-bad transport.

### 5. Prove offline isolation and invariants

Before any provider request, require all of the following:

- Parse the root and every profile config; exactly the named profile selects the adapter.
- Read back the intended model, provider, effective General/Coding API route as applicable, and empty fallback list.
- Prove the configured outer-attempt count and the OpenAI SDK retry count separately.
- Inspect credential-file existence and permissions only; do not print values or persist Authorization headers.
- Exercise the actual SDK over a loopback capture server through the adapter.
- Assert request-body equality, intended path, permitted header shape, redirect policy, and removal or preservation of SDK metadata as required by the known-good replay.
- Prove a non-target provider/profile still uses the original client builder.
- Compile/lint changed code and run focused neighboring retry/TLS tests.
- State why no provider call could occur during verification; use a network guard when static inspection and loopback containment are insufficient.

Mock-only selection tests are not enough. Pair them with an actual SDK client crossing the adapter into a local server.

### 6. Stop at the live gate

Write an offline receipt that separates:

- implementation;
- profile isolation;
- invariant readback;
- local SDK/transport proof;
- credential hygiene;
- provider-call count; and
- the remaining human authorization or acceptance gate.

Do not roll offline PASS into qualification PASS. If the user later authorizes one final specimen, run only the exact installed wrapper and prove the outer lifecycle trace, retry number, fallback count, provider response, and served-model evidence. Stop on the first terminal boundary.

## Evidence standard

- Configuration proves intent, not served behavior.
- Unit tests prove seams, not provider acceptance.
- An exact replay proves a transport differential, not the precise causal header or TLS feature.
- Wrapper exit, sentinel text, or `api_calls=1` do not alone prove one outbound attempt.
- A live qualification verdict requires the provider response plus Hermes lifecycle/usage evidence from the authorized invocation.

## Failure modes

- Reconstructing rather than replaying the exact body.
- Letting the replay library silently redirect or retry.
- Triggering an endpoint detector during an allegedly offline credential probe.
- Logging keys, Authorization headers, or provider error bodies into durable receipts.
- Adding a fleet-wide header/TLS change because one isolated profile failed.
- Allowing selector failure to revert silently to the failing path.
- Treating current provider unavailability as model-quality evidence.
- Spending the final request during repair verification rather than stopping for authorization.

## Reference implementation

The 2026-08-27 `glm53-zai-evaluator` repair is the worked instance:

- receipt: `/Volumes/Extra/Substrate/Operations/reports/Orchestration_Receipts/cycle_glm53-zai-evaluator-urllib-transport-offline-pass-20260827.md`;
- installed Hermes commit: `52bb602960`;
- adapter: `/Users/ted/.hermes/hermes-agent/agent/zai_urllib_transport.py`.

These paths identify evidence, not permanent API. Re-resolve the installed Hermes source, active profile, and current constructor names on every use.
