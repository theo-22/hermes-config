---
name: compile-work-packet
description: Compile externally authorized intent into a versioned, linted, cold-readable execution packet before consequential asynchronous or cross-actor dispatch. Use after a proposal or decision has explicit authority and the receiving worker needs a bounded objective, scope, choices, stopping forks, acceptance, return contract, and separated proof gates. Do not use this skill to create authority, settle an unresolved proposal, approve work, or treat cold readability as correctness.
category: meta
write_mode: file
one_line_use: compile externally authorized intent into a linted and cold-probed work packet
fast_pick: "yes"
---

# Compile Work Packet

Convert authorized intent into an execution contract that a cold receiving
worker can inspect without the originating conversation. This skill is the
boundary between authorization and dispatch; it creates neither.

## Trigger

Use for consequential work that is asynchronous, cross-actor, context-poor, or
likely to outlive the current conversation. For an unsettled idea, use
`proposal-candidate-surfacing`; for an already-shaped recommendation, use
`proposal-packet`. Compile only after an external authority has approved a
bounded execution slice.

Small synchronous work that Ted directly authorizes and the current actor can
finish and prove in one context does not need packet ceremony.

## Invariants

- Compilation and probing do not create authority, approve scope, or prove
  implementation success.
- `Handoff_Contract.md` or the receiving role's equivalent remains policy
  authority. This skill is a reusable mechanism.
- Critical and quality fields come from
  `references/work_packet.v1.schema.json`, not model judgment.
- A worker stops on unresolved critical fields. It never fills a meaning fork
  with a plausible guess.
- Cold-probe failure returns to proposal or packet shaping. The cold reader may
  diagnose ambiguity but must not repair scope or invent a decision.
- Implementation verification and fresh receiving-role acceptance are separate
  later gates.

## Workflow

### 1. Establish external authority

Record the exact decision, approved proposal, work-item row, issue, or other
external authority surface. The packet cannot cite itself as authority. If the
authority is conversational, first preserve a durable receipt that identifies
who authorized what and when.

### 2. Compile from the v1 template

Copy `assets/work_packet.v1.md`. Fill every critical field while preserving the
metadata keys and `##` headings. Keep the packet compact; link exact source
surfaces instead of copying broad context.

Distinguish:

- **implementer-owned choices** — decisions the worker may make and document;
- **stop-worthy meaning forks** — decisions that would change authority,
  meaning, scope, architecture, protected state, irreversibility, or cost and
  therefore require return rather than inference.

Acceptance criteria must be observable. The return contract must name a durable
absolute destination, not merely “report back.”

### 3. Validate deterministically

Run:

```bash
python3 scripts/validate_work_packet.py /absolute/path/to/packet.md \
  --mode activation --check-source-paths --json
```

Activation mode blocks missing or placeholder critical fields. Quality-field
omissions warn but do not block. Preserve the JSON report or its essential
fields—schema version, linter version, content SHA-256, status, errors, and
warnings—in the packet receipt.

Activation mode also requires an existing backticked absolute authority-receipt
path. Unversioned legacy packets remain inspectable with a warning.
Consequential activation requires recompilation to the current schema or
`--legacy-authority-override /absolute/path/to/authority_override_receipt.md`;
the linter checks that receipt exists and records it. It never silently
invalidates or silently upgrades legacy packets. The override permits bounded
activation/preflight only; consequential dispatch still requires recompilation
to the current schema so probe/hash binding is enforceable.

### 4. Run a cheap cold executability probe

Before consequential dispatch, give an existing cheap, uncommitted Hermes
reader only the packet and this output contract:

1. objective;
2. external authority and what it authorizes;
3. in-scope and out-of-scope work;
4. implementer-owned choices;
5. stop-worthy meaning forks;
6. acceptance criteria;
7. verification and fresh-acceptance gates;
8. durable return destination and stop condition;
9. unresolved ambiguity or missing critical information;
10. requested and actually served profile/model.

The reader performs no writes, dispatch, implementation, approval, or packet
repair. A pass means the execution contract is reconstructable without hidden
context. It does not mean the plan is correct or the work succeeded.

Record the packet hash and durable probe receipt. If the reader finds a
critical ambiguity, revise through the authority-preserving shaping path,
re-lint, and rerun against the new hash.

Before dispatch, run the deterministic post-probe gate:

```bash
python3 scripts/validate_work_packet.py /absolute/path/to/packet.md \
  --mode dispatch --check-source-paths --json
```

Dispatch mode verifies that the packet's cold-probe section names an existing
durable receipt containing `Result: PASS` and the current packet SHA-256.
It also requires requested and actually served profile/model metadata.

### 5. Dispatch, verify, and accept separately

Dispatch only after validation and the required cold probe pass. On return:

1. inspect implementation/local proof;
2. obtain an independent verifier where the work changed consequential state;
3. obtain genuinely fresh receiving-role acceptance when the role or live
   consumer must accept the result;
4. close the work item only after every material acceptance clause is met.

## Outputs

- versioned work packet;
- linter report with content hash;
- cold executability probe receipt;
- later implementation verification and fresh-acceptance receipts when
  required.

## Resources

- `references/work_packet.v1.schema.json` — authoritative field classification
- `assets/work_packet.v1.md` — compact packet template
- `scripts/validate_work_packet.py` — deterministic validator/fingerprinter
- `scripts/test_validate_work_packet.py` — regression tests

## Never Assume

- Authorization because a proposal is persuasive or a packet is complete.
- Permission to broaden scope because the receiver can see adjacent work.
- Correctness because a cold reader reconstructed the contract.
- Completion because dispatch or delivery occurred.
- Compatibility because a legacy packet looks similar to v1.
