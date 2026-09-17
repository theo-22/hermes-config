# Work Packet: [fill concise title]

**Packet schema:** work_packet.v1
**Packet ID:** [fill stable identifier]
**Packet status:** externally_authorized
**Requested actor:** [fill receiving actor]
**Authority reference:** `[fill absolute path to external durable authority receipt]`
**Compiler version:** compile-work-packet.v1
**Priority:** [fill or state not specified]
**Requested completion:** [fill or state not specified]

## Provenance

[Fill origin, shaping inputs, consulted doctrine, and authorization event.]

## Scope comparison

- **Asked:** [fill]
- **Proposing:** [fill]
- **Gap:** [fill or none]
- **Gap reason:** [fill or not applicable]

## Why now

[Fill the concrete reason this stage should run now.]

## Objective

[Fill one observable outcome.]

## Source surfaces

- `/absolute/path/to/source`

## Execution lane

[Fill actor, harness, access fence, and expected mechanism.]

## In scope

- [fill]

## Out of scope and boundaries

- [fill]

## Implementer-owned choices

- [Fill bounded choices the implementer may make and document.]

## Stop-worthy meaning forks

- [Fill decisions that require return rather than inference, or state none with rationale.]

## Acceptance criteria

- [Fill observable pass/fail condition.]

## Verification and acceptance gates

- **Implementation/local proof:** [fill]
- **Independent verification:** [fill or state why not required]
- **Fresh receiving-role acceptance:** [fill or state why not required]

## Return contract

Write the durable return to `/absolute/path/to/receipt.md` and include files
changed, checks run, actual result, what was intentionally not changed,
deviations, unresolved items, remaining design questions, packet hash, and
relevant claim/work-item/commit identifiers.

## Stop condition

[Fill the exact point where the receiver must stop and return.]

## Self-critique

[Fill assumptions, weak spots, and likely disagreement.]

## Legacy compatibility

Not applicable; this packet is compiled as `work_packet.v1`.

## Cold-probe receipt

Pending before dispatch at `/absolute/path/to/cold_probe_receipt.md`. The receipt
must record packet SHA-256, requested profile/model, actually served
profile/model, verdict, and unresolved ambiguity.
