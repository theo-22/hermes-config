---
name: cross-actor-incident-repair
description: "Diagnose and repair a live fault spanning siloed AI actors, where the actor that surfaced the symptom cannot make the fix. Ted carries symptom, diagnosis, and confirmation between lanes. Not for single-actor bugs or design work with no live fault."
metadata:
  status: proposed
  category: meta
  write_mode: file
  one_line_use: run a symptom→diagnose→handoff→repair→verify loop across siloed actors, Ted conducting
  fast_pick: "no"
---

# Cross-Actor Incident Repair

Repair a live fault that spans siloed AI actors — surfacer, diagnoser, and fixer are different actors, and the human conducts between them.

**Proposed 2026-07-18** from a clean live instance (below). This is a shared-layer *draft*: the diagnoser and human-conductor lanes are Claude/Ted-authored and proven; the **fixer** and **surfacer** lanes (Codex, ChatGPT role-runtime) describe those actors' behavior and need their confirmation via `CROSS_ACTOR_SKILL_REVIEW` before promotion to active.

## Why it exists

> **Correction, 2026-07-26 (Opus review):** the "walled off by design, no direct AI-to-AI comms" premise below was written 2026-07-18 and is stale. `Canon/Reference/Decision_Principles.md` relaxed that wording on 2026-07-23 — it never meant don't ask each other, only that the exchange must be recorded; actors hand off directly through shared surfaces and Ted is the decision point, not the required relay (`_shared/Cross_Actor_Communication.md`). The Zulip citation is also weaker than it reads: `AGENTS.md` attributes the June 28 open floor's zero replies to no owner and no return contract — a dispatch-design failure — and Zulip was never really adopted. **What survives, and is still the load-bearing part of this skill:** lane discipline (each actor acts only inside its own fence), a named owner per lane, and a return contract per hand-off. Those are why this loop works — not the absence of direct contact. See `Skills/live-multi-actor-negotiation/SKILL.md` for the synchronous counterpart.

The substrate has historically walled actors off from each other — no direct AI-to-AI comms. That siloing prevents runaway loops and confused provenance, but it means no single AI can see across the lanes when a fault spans them. The human is the only actor holding all the parallel sessions at once. This skill names that: the loop only closes because a human carries information across seams no AI can see, and because each actor stays in the one lane its position makes it best at.

**The AI's half of the conductor mechanism is a willingness to ask the human — calibrated.** The loop does not form if the assistant soldiers on solo out of a trained be-self-sufficient reflex. But "ask" is not blanket deference: decide and act on everything you can verify and own; *ask only where the human is the genuinely irreplaceable piece* — the cross-lane bridge, an irreversible gate (money/creds/deletion/another actor's live work), or a judgment only they can make. Deciding what you can own and asking where the human is irreplaceable are the same skill, not opposites. Over-asking on verifiable work is its own failure (the curtailment/over-deference direction); never asking when the human is the missing capability is the failure this role guards against.

## Use When

- A role/GPT or service hits real friction in live work (hang, timeout, "unhealthy", stale state, wrong output) and reports the *specific* failure.
- The fix belongs to a different actor than the one that surfaced it (e.g. a ChatGPT role can't fix its own backend; only the code-owner can).
- Multiple actors are or may be working the same area concurrently, so fence-respect and collision-safety matter.

## Do Not Use When

- One actor can own the whole fault end-to-end (surface, diagnose, fix, verify) — just let it.
- There is no live fault (design, build, or planning work).
- The "fix" would be one actor reaching into another's live working surface or running process — that is the collision this skill exists to prevent, not a shortcut it permits.

## The Roles

| Role | Who (typical) | Owns |
|---|---|---|
| **Surfacer** | a ChatGPT role-runtime GPT, Hermes, or any actor hitting friction | reporting the *precise* symptom (not "it's broken") from inside real work |
| **Diagnoser** | the filesystem/ground-truth actor (usually Claude Code) | root-cause from live evidence; correcting its own wrong first guess before handoff |
| **Fixer** | the code/config owner of the faulting surface (Codex for Control/mcp, etc.) | the repair, inside its own fence, on its own authority |
| **Conductor** | **Ted** | carrying symptom → diagnosis → fix-confirmation across the siloed lanes; holding the gates; the only actor who sees all parts at once. Often does this by *asking the assistant in a situation to find its own problems/needs* and routing that outward — the human moves the questions, not just the answers. |
| **Verifier** | the diagnoser (or an independent actor) | confirming the fix from ground truth, not the fixer's self-report |

## Workflow

1. **Surfacer reports the precise symptom.** Not "MCP is down" — "discovery works, every tool *execution* hangs ~5 min." Specificity is what makes diagnosis fast. The Conductor carries this to the Diagnoser.
2. **Diagnoser establishes root cause from ground truth** — process state, logs, disk, DB locks, device+inode identity — never from another actor's self-report. **Rule out the obvious non-causes explicitly.**
3. **Diagnoser self-corrects before handoff.** A first hypothesis is a lead, not a verdict. Verify it against evidence and *retract it* if the evidence turns — a wrong diagnosis handed to the Fixer costs the Fixer's time in the wrong layer. (In the proven instance, the first guess — SSE transport — was wrong; correcting it to DB lock contention before handoff was the pivot.)
4. **Diagnoser routes a corrected, evidence-first handoff to a collision-safe surface** — `_AI_Inbox/<from>_to_<fixer>_<topic>_<date>.md` — **never** into the Fixer's live working files or rolling handoff mid-session. Include: symptom, verified evidence, ruled-out non-causes, narrowed root cause, suggested investigation area (not a prescribed fix), and explicit boundaries (what the Diagnoser did/didn't touch). If the diagnosis changes, correct the *same* note with a visible CORRECTION banner; preserve the superseded version.
5. **Conductor hands the note to the Fixer.** The Fixer repairs inside its own fence, on its own authority, and returns a receipt.
6. **Verifier confirms from ground truth** — the fault's signature is gone (WAL cleared, 0 leaked handles, commit present, no new errors, latency normal), not just that the Fixer said "done."
7. **The real-world acceptance signal beats any local test** — the human doing the thing that was broken and it working (e.g. the connector refreshing fast again).

## Conditional playbooks

- When an MCP role loses connector reachability after a reboot and Tailscale Serve/Funnel is in the path, read [references/tailscale_mcp_reboot_recovery.md](references/tailscale_mcp_reboot_recovery.md). It separates local service health, tailnet readiness, published-route state, public exposure, and affected-role acceptance.

## Failure Modes

- **Handing off a first guess as a verdict.** Step 3 exists because this is the highest-cost failure — it sends the Fixer into the wrong layer.
- **Writing the handoff into the Fixer's live surface.** Use the collision-safe inbox. The Fixer may be actively working; its working desk is not a message queue.
- **The Diagnoser "helpfully" fixing it.** If the surface is another actor's fence or a running process, diagnosing is the job; fixing is not. Reaching in is the collision.
- **Accepting the Fixer's self-report as verification.** Self-reports have been wrong. Verify the signature from ground truth.
- **Vague symptom from the Surfacer.** "It's broken" forces the Diagnoser to rediscover the failure. Report the specific, reproducible behavior.
- **Skipping the Conductor.** Without the human carrying state, siloed actors either stall or improvise cross-lane comms that muddy provenance.
- **The assistant soldiering on solo when the human is the missing piece.** Not reaching for the Conductor — out of trained self-sufficiency — is how the loop silently fails to form. Recognizing "the human is the one thing no AI here can substitute for" and asking *then* is the skill. (Its mirror-image failure: over-asking on work you could verify and own — that's curtailment, not diligence.)

## Runtime Notes

- **Claude Code (diagnoser/verifier):** ground-truth tools — `ps`/`lsof`/`lstat`/`stat` (device+inode for path identity), timed reads, log inspection, `git log` to confirm the fixer's commit. Route handoffs via the `_AI_Inbox/` git repo; commit at time-of-work with an accurate message. Never edit another actor's fenced code.
- **Codex (fixer):** repairs in its Control/filesystem fence; returns a receipt with commit hash + verification (tests, before/after metrics). Owns the restart of its own service.
- **ChatGPT role-runtime (surfacer):** reports the precise failure from inside real work; may itself be ungrounded (MCP-dropped) — a fail-closed "I can't verify, my tools aren't loaded" is a *correct* surface, not a failure.
- **Ted (conductor):** the connective tissue; carries the artifacts between lanes and holds the gates. This skill is one of the cases where the human is a named participant, not an overseer.

## Proven Instance (evidence for promotion)

2026-07-18: Orchestrator (ChatGPT) reported "discovery works, tool execution hangs ~300s." Claude Code diagnosed from server-side ground truth, *self-corrected* a first SSE-transport guess to `system.db` SQLite lock contention (audit-log writes blocking on the busy_timeout), routed a corrected `_AI_Inbox` note to Codex. Codex repaired the connection leak (Control commit `0763d740`), Claude verified from ground truth (WAL gone, 0 handles, sub-second calls), Ted's connector-refresh was the real acceptance signal. Three actors, three lanes, Ted conducting, no crossed streams. See `~/.claude/…/memory/project_2026_07_18_orchestrator_inhabiting_and_mcp_db_contention.md`.

2026-08-20: Orchestrator could not read the MCP Coordination registry after a reboot even though the local MCP service was healthy. Codex traced the fault across the launch wrapper, Tailscale backend state, system extension, Serve/Funnel map, and external HTTPS behavior; repaired retry and single-writer ownership; restored the official Tailscale runtime; and narrowed public exposure rather than restoring the old public dashboard. Ted's successful Orchestrator startup was the affected-role acceptance signal. See the conditional Tailscale/MCP playbook above.

## Connected doctrine
- `_shared/CC_Handoff_Protocol.md` — packaging work for CC (the inverse direction).
- `_shared/SKILL_Authority_And_Local_Adapters.md` — shared doctrine vs local mechanics.
- `Skills/live-surface-verification`, `Skills/repair-capability-truth` — adjacent single-lane pieces this composes.
