---
name: workspace-orchestration-coordination
description: RETIRED 2026-07-12. Multi-actor file check-in/check-out is now the DB-backed claim/lease in claims.py (System 14 Ch15). This skill was a build spec for an Operations/gpt_coord/ system that was never built, targeting the retired GPT-Builder-file domain. Use claims.py surface-grain claims instead.
category: gpt
write_mode: none
one_line_use: retired — use claims.py surface-grain claims to check out a file
fast_pick: "no"
---

# Workspace Orchestration — GPT File Coordination — RETIRED 2026-07-12

**This skill is retired.** Do not follow its former procedure.

## Why retired

- Its Phase 1–5 was a **build spec for `Operations/gpt_coord/`** (with `changes.jsonl` / `queue.jsonl` / `reservations.jsonl` and a `gpt_coordination.py` module) that **was never built** — the directory does not exist.
- Its domain — shared **GPT Builder source files** and the Builder-repaste queue — is being retired as roles convert to role-runtime (Builder pastes are no longer the write path).
- Its proposed `reservations.jsonl` checkout is **superseded by `claims.py`**, the DB-backed claim/lease that already unifies surface / task / domain grains (System 14 Chapter 15).

## What to use instead

**Check out a file before writing it via `claims.py` surface-grain claims** — the live, unified checkout:

- Claim: `/api/claims/claim` with `grain=surface`, `target=<absolute file path>`, an `actor`, and a `purpose`. The DB refuses a second active claim on the same `(grain, target)` — the lost-update guard this skill wanted, now structural.
- Release: `/api/claims/release` at closeout (or let the lease TTL expire).
- `SURFACE_RESERVATIONS.md` is an auto-generated *view* of live surface-grain claims — read it, don't hand-edit it.

The still-good ideas from the old design (hash-verify before write, atomic write-temp-then-rename) remain good practice and can ride on top of a claim; they did not require this skill's parallel JSONL store.

## References

- `Control/backend/claims.py` — the live checkout (grain/target claim + lease + audit).
- `Operations/session_chains/SURFACE_RESERVATIONS.md` — the generated view.
- `Skills/workflow-orchestration/SKILL.md` — the chain-runner that takes claims at chain start.
