---
name: probe-chatgpt-host-artifact-binding
description: Run a fresh-client, no-side-effect probe to determine whether a native ChatGPT-generated artifact can reach a connector as a bound file or bytes, or exposes only a stable ID with an official exact-content retrieval path. Use before building any host-to-local artifact receiver.
metadata:
  category: verification
  write_mode: file
  one_line_use: classify native ChatGPT artifact binding as PASS, PARTIAL, or FAIL before receiver work
  fast_pick: "yes"
  version: "1.0.0"
  tags: [chatgpt, artifacts, fresh-client, mcp, verification]
---

# Probe ChatGPT Host Artifact Binding

Prove the current host boundary in a genuinely fresh ChatGPT client before designing or building a receiver. Prior receipts, local schemas, documentation, and model memory are orientation only.

## Gate

- **PASS:** the exact generated artifact reaches the intended connector as a host-bound file object, stream, or original bytes.
- **PARTIAL:** the fresh host exposes a stable artifact/file ID and an official authenticated operation for retrieving the exact original content, but the intended connector receives neither the binding nor bytes.
- **FAIL:** the output has no stable retrievable identity, the purported retrieval path is unofficial or cannot be tied to the exact artifact, or only chat prose, `/mnt/data`, screen inspection, Downloads, or filename reconstruction is available.

Do not build a receiver unless the user's implementation authority is explicit and the required proof gate passes. A PARTIAL result may justify a separate retrieval-feasibility review; it is not receiver acceptance.

## Procedure

1. Read the current work item or architecture packet and preserve its exact scope, forbidden actions, and acceptance definitions.
2. Start a new authenticated ChatGPT conversation. Do not reuse a warmed role session as fresh-client evidence.
3. Generate one disposable native artifact with an unmistakably simple prompt. Record the conversation URL and generation identifier exposed by the host.
4. Inspect the fresh client's current host file/artifact inventory and relevant tool schemas. Do not assume prior tool names still exist.
5. Establish whether the exact output has a stable host identity. Require raw evidence tying the identifier to the generated artifact, such as current file inventory plus `source_kind: generated` or the current equivalent.
6. Inspect whether the host exposes an authenticated exact-original-content retrieval operation for that identifier. Schema evidence must show the identifier input and raw/original representation; documentation alone is not enough.
7. Inspect the intended connector's live schema. Determine whether it accepts a host-bound file/attachment, stream, original bytes, or the exact host identifier. A generic string/path parameter does not count.
8. Unless explicitly authorized otherwise, do not invoke materialization, download, upload, capture, stage-write, request-recording, processing, placement, retirement, apply, or receiver code.
9. Classify exactly once using the gate above. Record observed identifiers, raw schema facts, actions not invoked, local/DB non-mutation checks, and the precise return condition.

## Evidence boundary

Host capability and connector capability are separate:

- Host inventory proves the artifact exists and may prove stable identity.
- A host retrieval schema may prove an official exact-content path in that ChatGPT context.
- Connector input schema proves whether the artifact can cross the boundary.
- A model statement that transfer is possible does not prove transfer.
- A local request table, manually recorded metadata, or Downloads match does not prove host binding.

For a no-side-effect probe, verify relevant local request tables remain unchanged and no matching Downloads/local capture artifact appeared. Preserve unrelated worktree changes.

## Receipt

Record:

- verdict: `PASS`, `PARTIAL`, or `FAIL`;
- fresh-client conversation reference;
- native generation/artifact identifiers;
- host inventory classification;
- exact host retrieval operation and relevant input/representation schema, if any;
- connector tool and accepted binary-source fields;
- whether a file object or bytes actually crossed;
- prohibited actions confirmed absent;
- next permitted action and stop condition.

If the result is PARTIAL or FAIL, leave the receiver unbuilt and retain the existing manual/local fallback without presenting it as host binding.
