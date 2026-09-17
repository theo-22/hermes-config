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

### 3a. Prove the telemetry observes the effective request client

When a provider-shaped error and the usage receipt disagree about whether the wire ran, trace the evidence object through the complete request lifetime. Do not assume the client visible to an outer hook is the client that sent the request.

Check all active call modes, including streaming paths used by quiet or one-shot invocations:

1. identify the exact SDK client created for the attempt;
2. follow its owned HTTP client and effective transport;
3. record provenance before the per-request client or stream is closed, cleared, cached, or replaced by an abort handle; and
4. prove the lifecycle/usage collector serializes that same request-local record.

If cleanup runs before the outer error hook, carry a credential-free provenance record on the exception or another request-local object. Snapshot the transport's pre-request provenance and attach only a newly produced record; otherwise a reused client's older HTTP receipt can falsely prove that a later synthetic/local error reached the provider.

Search both Hermes and installed dependencies for the exact error text plus every relevant exception constructor/translator. An SDK `RateLimitError` class alone is not proof: it may be constructed locally, while an SDK path that constructs it from an actual response status is evidence only when the effective transport and request-local receipt agree.

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
- Exercise every installed request mode that owns a distinct client lifetime. A one-shot or quiet command may still use the streaming implementation even when no token consumer is visible.
- Assert request-body equality, intended path, permitted header shape, redirect policy, and removal or preservation of SDK metadata as required by the known-good replay.
- Pair a genuine loopback HTTP error with a synthetic/local exception. The HTTP case must retain the response boundary after client cleanup; the synthetic case must remain null even if the client contains an older provenance record.
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
- `provider=<name>`, an HTTP-shaped exception, and `api_calls=1` do not prove provider receipt. Require a request-local transport boundary such as `HTTP_RESPONSE_RECEIVED`.
- `provider_received=false` or null provenance means local/pre-response failure unless the exact effective-client attachment and cleanup path has itself been tested and shown defective.
- Console activity is corroborating account-side evidence, not a substitute for wire proof. A genuine HTTP response can coexist with no billable usage record, for example when account or plan eligibility rejects the request before inference.
- A live qualification verdict requires the provider response plus Hermes lifecycle/usage evidence from the authorized invocation.

## Failure modes

- Reconstructing rather than replaying the exact body.
- Letting the replay library silently redirect or retry.
- Triggering an endpoint detector during an allegedly offline credential probe.
- Logging keys, Authorization headers, or provider error bodies into durable receipts.
- Adding a fleet-wide header/TLS change because one isolated profile failed.
- Allowing selector failure to revert silently to the failing path.
- Reading provenance from a shared cache or outer client after the per-request streaming client has already been cleared.
- Reusing a prior request's transport receipt to label a synthetic/local exception as provider-received.
- Treating current provider unavailability as model-quality evidence.
- Spending the final request during repair verification rather than stopping for authorization.

## Reference implementation

The 2026-08-27 through 2026-08-28 `glm53-zai-evaluator` repair is the worked instance:

- receipt: `/Volumes/Extra/Substrate/Operations/reports/Orchestration_Receipts/cycle_glm53-zai-evaluator-urllib-transport-offline-pass-20260827.md`;
- final provenance/qualification receipt: `/Volumes/Extra/Substrate/Operations/reports/Orchestration_Receipts/GLM53_ZAI_Coding_Plan_Qualification_Final_2026-08-28.md`;
- transport adapter commit: `52bb602960`;
- request-lifetime provenance commit: `e22ab9ec53`;
- adapter: `/Users/ted/.hermes/hermes-agent/agent/zai_urllib_transport.py`.

The final specimen proved a real Z.AI Coding Plan HTTP 429 with request-local `HTTP_RESPONSE_RECEIVED` provenance while the authenticated console showed no active Coding Plan subscription. That combination established correct routing plus account-plan rejection, not model failure and not a locally synthesized 429.

These paths identify evidence, not permanent API. Re-resolve the installed Hermes source, active profile, and current constructor names on every use.
