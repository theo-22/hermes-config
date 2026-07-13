---
name: live-surface-verification
description: Verify disputed live state by asking the actual runtime surface before trusting local docs. Use when schemas, env files, Builder inventory, backend code, logs, or memory disagree about what is true for a GPT Action, browser/Builder configuration, proxy route, bearer scope, uploaded Knowledge, or other live integration. Prefer a harmless live probe from the real GPT, Chrome/Builder inspection, or backend audit evidence over inference from intended-state files. If direct verification is unavailable, ask Ted for a bounded exact live test instead of guessing.
category: judgment-only
write_mode: none
one_line_use: prove the live surface
fast_pick: "yes"
---

# Live Surface Verification

Prove the thing where it actually runs.

Use this skill when the question is not "what do the files say should happen?" but "what is the live system actually doing?"

Common triggers:
- a GPT Action exists locally but fails in the GPT
- docs, schemas, env vars, Builder inventory, or backend code disagree
- the disputed fact is a bearer key, resolved scope, route, uploaded schema, uploaded Knowledge, action count, auth mode, proxy path, or permission boundary
- the tempting fix is based on a plausible document rather than live proof

## Core Rule

When live wiring is disputed, direct runtime evidence outranks local intended-state files.

Do not patch auth, scope, permissions, route shape, or Builder state based only on documents when a harmless live probe can settle the question.

## Evidence Ladder

Use the closest available proof source:

1. The actual GPT runs a harmless read/list action and reports raw tool output.
2. Chrome/Builder inspection confirms the actual pasted configuration.
3. Backend logs or audit rows show what reached the server and how it resolved.
4. Local files, schemas, env files, and docs show intended state only.

If you must rely on level 4, say it is not live proof.

## Workflow

1. Name the disputed fact.
Examples: "Which bearer is pasted in Builder?", "Which scope does the backend resolve?", "Does the clean route reach the proxy?", "Is this Knowledge file uploaded?"

2. Choose a bounded harmless live probe.
Prefer `list`, `read`, `status`, `health`, or metadata calls. Avoid writes, moves, deletes, imports, sends, or purchases unless Ted explicitly authorizes them.

3. Ask the live surface first.
If you can call the GPT/tool/browser directly, do that. If not, ask Ted for a bounded exact test.

4. Require raw output.
Ask for backend-resolved fields such as `scope`, `root`, `status`, `operationId`, action count, route status, or error text. A summary is useful after the raw result, not instead of it.

5. Patch only after proof.
Update backend/docs/scripts to match the verified live result. Record the proof phrase, not just the conclusion.

## Asking Ted Is Allowed

Do not avoid asking Ted for a tiny live test merely because it gives him something to do.

When Ted can ask the actual GPT faster than an assistant can infer the answer, asking Ted is the lower-stress path. Make the ask small, exact, and copy-pasteable.

Use this shape:

```text
Please run this in [exact GPT name]:

[copy-paste prompt]

Paste back the raw action response, especially [specific field].
```

Then explain how to interpret each likely result.

## GPT Action Test Prompt Pattern

```text
Please test only [action name].

Call `[operationId]` with:
{
  "op": "list",
  "root": "[safeRoot]",
  "path": ""
}

Do not use other actions for this test. Report the raw JSON response, especially `[field]`.
```

Interpretation example:
- `scope: digest` proves the pasted bearer resolves to `digest`
- `scope: image_factory` proves it resolves to `image_factory`
- `404` proves route or rewrite failure
- `401` on an unauthenticated request proves the route is reachable and auth-gated
- `no such action` means Builder does not have the action available in that GPT/chat

## Chrome/Builder Inspection

Use Chrome/Builder when the disputed fact is the Builder surface itself:
- action count
- pasted schema/domain
- authentication mode
- which Action is present
- uploaded Knowledge list or freshness
- conversation starters or instructions

Chrome inspection is stronger than local inventory, but still verify with a live GPT action when the question is runtime behavior.

## Never Assume

- Do not treat `.env`, schema YAML, Builder inventory, or memory as proof of what is pasted in Builder.
- Do not convert "I cannot test" into "therefore the docs are true."
- Do not make Ted approve a conceptual fix when a tiny live probe would settle it.
- Do not hide uncertainty. Say "local intended state only" when live proof is missing.
- Do not ask Ted for broad debugging. Ask for one exact, harmless test.

## Output Shape

- `Disputed fact`
- `Best proof source`
- `Live test used or requested`
- `Raw result`
- `Conclusion`
- `What to patch`
- `Confidence`

Keep it short. The point is to shorten the path to reality, not create another audit layer.
