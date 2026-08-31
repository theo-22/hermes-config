---
name: create-worker
description: "Mint a new bounded, dispatchable Hermes worker on the proven migrator/verifier mold — correct by construction (config floor + five disciplines baked in). Use when a SHAPE of bounded, externally-checkable work recurs and no existing worker owns it, and you want callable capacity a hub can dispatch and verify. Works for any actor: Claude Code and Codex run the factory via shell; Coordinator (and other GPT roles with scope) call the create_worker MCP tool. Do not use for one-off work (just dispatch the closest worker with a precise packet) or for anything needing live judgment (that stays with a hub)."
metadata:
  category: meta
  write_mode: file
  one_line_use: mint a bounded CC/Codex/Coordinator-dispatchable worker on the migrator mold
  fast_pick: "yes"
---

# Create Worker

Mint a bounded worker — the migrator/verifier pattern, generalized. This is Layer 3
of the Fleet Operating Model (`Planning/Fleet_Operating_Model_Proposal.md`):
callable bounded capacity, never self-directing, reached through
dispatch-with-receipt. A hub (Claude Code or Coordinator) shapes the task and
verifies the receipt; the worker executes; Ted approves at gates.

## When to mint (vs. dispatch an existing worker)

- **Mint** when a *shape* of bounded work recurs and no worker owns it — e.g.
  reference-integrity, doc-drift reconciliation, bounded cleanup, single-question
  evidence audits. One worker = one coherent task-shape with its own discipline.
- **Don't mint** for a one-off — dispatch the closest existing worker
  (`dispatch_worker` / `orchestrate.py dispatch`) with a precise packet.
- **Don't mint** for anything needing live Ted judgment — that stays with a hub.
- Check the live registry first: `_shared/Worker_Dispatch.md`.

## What every worker gets (correct by construction)

The factory guarantees, for every caller, the same poka-yoke:
- a fixed unit classification of `worker`, with a functional task-shape name;
  the model remains separate runtime configuration and never defines identity;
- a **model lane** resolved at mint time and written into the profile's
  `config.yaml` (`model.default` + `model.provider`) — lanes come from the Lab
  model replacement scan (2026-08-15): `cheap` (ling-2.6-flash / openrouter for
  machine-parsed, mechanical, contract-clean output), `mid` (OR
  `~deepseek/deepseek-v4-flash-latest` / openrouter for judgment/contradiction/
  verification/config-touching), `specialized` (caller-supplied model; provider
  may be explicit or inherited from a deterministically classified mold, e.g.
  finance GLM 5.2 / zai — only when the model IS the evaluation subject). A
  specialized model never silently defaults to OpenRouter.
  **Ask the five lane questions before minting:** (1) machine-parsed or
  human-read output? (2) mechanical or judgment work? (3) needs 1M context?
  (4) touches config/runtime surfaces? (5) frequent cron or rare dispatch?
  cheap earned, mid default, specialized explicit.
- cloned from a mold profile (default `migrator`), config floor applied
  (`verify_on_stop`, memory, `max_turns` — the settings that were wrong on 9/10
  hand-built profiles), refuses to clobber an existing profile. The mold must
  have an explicit `profile.yaml` `worker_factory.mold_safety_class` declaration
  or an exact established SOUL marker; genuinely ambiguous molds fail closed;
- inherits the mold's provider, compatible base URL, fallback posture, and
  whitelisted non-secret provider routing settings when the provider is not
  explicitly changed. Credential values are never read into plans or receipts;
- a SOUL carrying the **five non-negotiable disciplines**: HALT-don't-improvise ·
  reversible-only (never hard-delete) · evidence-not-assertion (grep + file:line) ·
  stay-in-scope (read-only assessments) · leads-not-authority (the hub verifies);
- a **kind**: `read-only` (examines/reports, never mutates — the safe default) or
  `mutating` (bounded reversible changes, preserves originals). The SOUL's
  disciplines flex to match.
- the shared human-attention contract at
  `/Volumes/Extra/Substrate/_shared/Human_Attention_Routing.md`; workers submit a validated
  Planner request instead of creating Calendar, Reminders, or duplicate inbox
  projections themselves.

## How each actor invokes it

**Claude Code / Codex (shell):**
```
# dry run first (prints the plan, touches nothing):
python3 /Volumes/Extra/Substrate/Operations/scripts/create_worker.py <name> \
    --role "<one-line role>" --kind read-only --lane cheap \
    --tasks "shape one;shape two"
# then mint:
python3 /Volumes/Extra/Substrate/Operations/scripts/create_worker.py <name> --role "..." \
    --lane cheap --apply
# specialized (the model IS the subject, e.g. a model being evaluated):
python3 /Volumes/Extra/Substrate/Operations/scripts/create_worker.py <name> --role "..." \
    --lane specialized --model glm-5.2 --provider zai --apply
# or inherit Z.AI routing identity from a deterministically classified Z.AI mold:
python3 /Volumes/Extra/Substrate/Operations/scripts/create_worker.py <name> --role "..." \
    --from glm53-zai-evaluator --lane specialized --model glm-5.3-flash --apply
```

**Coordinator / GPT role (MCP tool, no shell):**
Call the `create_worker` MCP tool with `name` and `role` (required), optional
`kind`/`tasks`/`mold`/`lane`/`model`/`provider`. It runs the same factory
in-process and returns the result. Then dispatch the new worker with the
`dispatch_worker` tool.

## Then: dispatch and verify (the loop)

1. Dispatch a bounded packet: `dispatch_worker(...)` or
   `python3 Control/backend/orchestrate.py dispatch <worker> "<task>"` —
   claim → dispatch → receipt → release.
2. The worker writes a signed receipt to its receipt lane
   (`Operations/reports/Orchestration_Receipts/`).
3. **The hub verifies** — re-run the receipt's cited file:line / commands. A
   worker's summary is a lead, not proof. Cross-check worker judgment against a
   deterministic scan where one exists; neither is trusted alone. (A live worker
   false-negative was caught exactly this way on 2026-07-11.)
4. Update `_shared/Worker_Dispatch.md`'s registry when a worker is minted.
5. If the worker exposes a future need for Ted's attention, submit it with
   `Operations/scripts/planner_request.py`; the hub does not let the worker
   choose the projection.

## Guardrails

- Long worker runs must be detached (background) — a caller-side timeout otherwise
  leaves the claim locked until its lease expires.
- The MCP path defaults to `read-only`; minting a `mutating` worker is a
  deliberate choice — mutating workers still carry the reversible-only discipline
  and the hub still verifies every receipt.
- Mechanical exact transforms (e.g. string repoints across files) belong in a
  deterministic script, not worker freehand; the worker does the *judgment*
  (live vs. historical, safe vs. unsafe), the script does the transform.
- Do not name a worker for a provider, model tier, personality, or current
  assignee. Name the recurring task shape it performs.
