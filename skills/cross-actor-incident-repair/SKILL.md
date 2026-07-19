---
name: cross-actor-incident-repair
status: proposed
description: Diagnose and repair a live system fault across siloed AI actors without crossing streams. Use when a role/GPT or service hits real friction (hangs, timeouts, "unhealthy", stale state, wrong results) and the fix needs a different actor than the one that surfaced it — e.g. a ChatGPT role reports a symptom, the filesystem-access actor must diagnose root cause, and the code-owning actor must repair inside its fence. Ted conducts across the walled-off lanes (no direct AI-to-AI comms), carrying the symptom, the corrected diagnosis, and the fix confirmation between actors. Do not use for single-actor bugs one actor can fully own end-to-end, for design/build work with no live fault, or as a substitute for the owner simply fixing its own code when no cross-actor seam exists.
category: meta
write_mode: file
one_line_use: run a symptom→diagnose→handoff→repair→verify loop across siloed actors, Ted conducting
fast_pick: "no"
---

# Cross-Actor Incident Repair

Repair a live fault that spans siloed AI actors — surfacer, diagnoser, and fixer are different actors, and the human conducts between them.

**Proposed 2026-07-18** from a clean live instance (below). This is a shared-layer *draft*: the diagnoser and human-conductor lanes are Claude/Ted-authored and proven; the **fixer** and **surfacer** lanes (Codex, ChatGPT role-runtime) describe those actors' behavior and need their confirmation via `CROSS_ACTOR_SKILL_REVIEW` before promotion to active.

## Why it exists

The substrate walls actors off from each other by design — no direct AI-to-AI comms. That siloing is a feature (it prevents runaway loops and confused provenance — it evolved from watching open peer coordination fail: "Zulip open-floor coordination produced silence" per `AGENTS.md`), but it means no single AI can see across the lanes when a fault spans them. The human is the only actor holding all the parallel sessions at once. This skill names that: the loop only closes because a human carries information across seams no AI can see, and because each actor stays in the one lane its position makes it best at.

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

## Connected doctrine
- `_shared/CC_Handoff_Protocol.md` — packaging work for CC (the inverse direction).
- `_shared/SKILL_Authority_And_Local_Adapters.md` — shared doctrine vs local mechanics.
- `Skills/live-surface-verification`, `Skills/repair-capability-truth` — adjacent single-lane pieces this composes.
