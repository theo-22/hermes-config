---
name: live-multi-actor-negotiation
status: active
description: Run a live, synchronous conversation where two or more standing AI actors (a ChatGPT role-runtime, Claude Code, Orchestrator, etc.) read and respond to each other's actual messages in a shared thread — with Ted present and participating but not relaying — to negotiate a boundary or working agreement between the actors who will be bound by it, verify a claim across tool surfaces, or jointly review a shared artifact (e.g. a concept-map node). Use when the parties to a constraint should be the ones stating it, and the actors have complementary, non-overlapping access (one has DB/filesystem reach, one has graph-tool reach, one has a different verification boundary). Do not use for parallel task execution, for anything one actor can fully own end-to-end, or as a way to avoid Ted's sign-off on meaning/authority changes — the actors negotiate the terms; Ted settles them.
category: meta
write_mode: file
one_line_use: three-plus actors, one live thread, real-time cross-verification
fast_pick: "no"
---

# Live Multi-Actor Negotiation

Hold a real-time conversation between Ted and two or more standing AI actors in a shared thread, where every actor reads and answers what the others actually said — not a summary carried by Ted — and each independently verifies the others' claims against whatever it can actually check.

**Active 2026-07-26**, from a live instance: Ted, Map Curator (ChatGPT role), Claude/CC, and Orchestrator (ChatGPT role) negotiated a durable cross-actor working agreement, found and fixed two live production bugs, and converged on the same concept-map node from three independent angles, in one continuous session. Full account: `/Volumes/Extra/Substrate/Roles/Role_Runtime_Architecture/Map_Curator_Working_Agreement_and_Auto_Inject_Session_Report.md`.

## What this is in tension with (read before using)

**Not the "walled-off" premise — that's retired.** `cross-actor-incident-repair` (drafted 2026-07-18, still `proposed`) says the substrate walls actors off by design, no direct AI-to-AI comms. That wording was explicitly relaxed on 2026-07-23: `Canon/Reference/Decision_Principles.md` now reads *"it never meant don't ask each other, only that the exchange must be recorded."* Actors handing off directly through shared surfaces is the live default; Ted is the decision point, not the required relay. The Zulip evidence also says less than it's been made to say — `AGENTS.md` attributes the June 28 open floor's zero replies to **no owner and no return contract**, a dispatch-design failure, and Ted's own account is that Zulip was never really adopted at all. Non-adoption is not a topology failing under load.

**The live objection is `_shared/Cross_Actor_Communication.md`, and it is a real one.** Two of its four guardrails aim straight at this skill:

- *"Callable bounded worker, not peer chat"* — an exchange should carry a scope and a return contract and land as an artifact, not run as an open-ended conversation that evaporates.
- *"Centralized routing beats peer-heavy swarms"* — backed by research (`Operations/Resolved/Deep_Research_Multi_AI_API_Patterns_Report.md`): centralized orchestration beat peer-heavy patterns on reliability, and independent parallel agents amplified errors on sequential work. Panel/debate patterns survive in that literature only as a *specialized* tool, gated on problem difficulty and built on genuinely heterogeneous participants — with conformity cascade as the named failure mode.

**But those guardrails are about task execution, and this is not task execution.** The research warns about parallel agents *producing work* — error amplification on sequential tasks, debate as an expensive way to get a better answer. This skill does something else: the actors who will be bound by a constraint state that constraint themselves, in front of each other. That's not "more minds produce a better answer." It's the evidence-mode rule the spine already runs on — **name your source before you trust a return.** For "what can Map Curator actually reach, and where does that stop," the authoritative source is Map Curator. A third party relaying reconstructs each side's limits secondhand and lossily, in both directions.

**Ted's read, and it is the operative one (2026-07-26):** *"The power of what we did IS the actors talking directly. Them negotiating boundaries and a contract about how things will work is far more thorough than I could create, and what we could create with me passing info back and forth."* Two things follow. The contract is **more accurate** — each actor corrects the other's guess about its own surface in real time, which is what produced the three tightenings in the worked instance that CC's solo draft had wrong. And it is **cheaper**, not more expensive: relaying costs a full restatement of each position in each direction, plus Ted's reconstruction of both. Direct exchange pays once.

**So what actually earns the exception is scope.** This is for negotiating, verifying, and jointly reviewing — the genres where the participants hold the ground truth. It is not for parallel execution, which is exactly where the research's warning lands. The entry conditions below hold that line.

**Status: active, signed off by Ted 2026-07-26** after Opus adversarial review the same day.

## Entry conditions — all four, or don't run it

1. **Heterogeneous access (hard requirement, not a nice-to-have).** Each actor must be able to check something the others structurally cannot. In the worked instance: Map Curator could not touch a file, CC could not write a graph edge, Orchestrator could not read `role_lib.py`. Homogeneous actors talking is the swarm shape the research says degrades reliability — the non-overlap *is* the mechanism. If two actors could each do the whole job, this is peer chat with no panel underneath it.
2. **The genre is negotiate / verify / jointly review — not execute.** A contested boundary, a working agreement between actors, a claim that crosses tool surfaces, a shared artifact several roles read differently. The test: would a single actor working alone plausibly get this wrong *because it can't see the other side's ground truth*? If the answer is no — if it's work one actor can just do — this is overhead. Parallel task execution is the case the research says degrades; keep it out of here.
3. **Demonstrated verify-before-trust in every participant.** This skill assumes that discipline; it does not create it. An actor that accepts a plausible peer claim without re-deriving it turns the session into a conformity cascade with extra steps.
4. **Ted present for the duration.** Not delegating and stepping away. He settles meaning and authority in the thread; that's the gate, and it can't be async here.

## Do not use when

- One actor can own the work end-to-end — this skill adds real overhead (multiple tabs, cross-verification) that isn't worth paying without a real cross-actor need.
- **The work is bounded and has a clean return contract.** Then it's a worker dispatch or an inbox handoff, not a live thread. Live dialogue is the expensive option; reach for it only when the back-and-forth itself is doing work that a scoped ask-and-return can't.
- The actor count would be more than 2-3 AI actors at once, or any actor involved doesn't have a demonstrated verify-before-trust practice — more actors is not better, and past that point this is the swarm shape the research says amplifies errors.
- Ted can't be live and present — this is not a way to run unattended multi-actor coordination; that's a different (and currently unbuilt) problem.
- The outcome would change meaning, authority, or a role's operating contract without Ted explicitly settling it in the thread — this skill produces proposals, never autonomous agreement.

## Canonical workflow

1. **Ted opens the live conversation(s)** — typically one browser tab per ChatGPT-role actor, with Ted present in at least one and CC (or the filesystem-capable actor) joining via browser automation, announcing itself explicitly (e.g. `[Claude / CC]`) so every message's author is unambiguous.
2. **Each actor speaks from its own access.** The graph/role-meaning actor proposes changes to meaning; the filesystem/DB actor verifies claims against live state and executes file/DB changes the other can't reach; each says plainly what it did and did not check.
3. **Every claim gets independently re-verified before being acted on**, not trusted because a peer stated it — this is the load-bearing discipline, not the live-chat mechanism itself. A survey, a count, a code claim: re-derive it from the primary source before treating it as settled.
4. **Meaning and authority changes are proposed, never auto-applied.** Ted reads the proposal in the thread and gives an explicit yes before any write happens.
5. **When stakes warrant, escalate to an outside, uncommitted reader** (a fresh Opus review, a Hermes worker dispatch) rather than trusting the in-thread consensus — invested parties agreeing with each other is not the same as being right (this is what caught the material survey error in the worked instance).
6. **Consolidate into one durable record** at close — **this is the return contract, and it is what June 28 was missing.** Not optional polish — not left scattered across chat transcripts. A single report file, updated as the session progresses, naming what was decided, what was found, what's still open, and who is meant to act on each open item next.

## Evidence / success criteria

- Every non-trivial claim exchanged between actors has a verification step attached to it (not just an assertion accepted at face value).
- At least one genuinely independent catch happened (an actor found something the others missed or got wrong) — if the actors only ever agree with each other, the cross-verification isn't doing real work.
- Ted explicitly settled every meaning/authority change in the thread itself, not inferred from silence.
- A single consolidated file exists at close, not just the raw transcripts.

## Failure modes

- **Courier drift:** the filesystem-capable actor becomes the only path information travels between the ChatGPT-role actors, quietly becoming a required relay rather than a peer. Route findings through a durable inbox/staged surface when possible instead of live-chat-only handoff; watch for this explicitly (see the "Master Orchestrator framing" discussion in the worked instance's report).
- **Agreement theater (the research literature's *conformity cascade*, and the named failure mode of every panel/debate pattern):** actors defer to each other's plausible-sounding claims instead of re-deriving them, and the live-chat format makes that feel like productive collaboration when it's actually skipped verification. The countermeasure is entry condition 1 — actors with genuinely different reach can't quietly agree about things neither can see.
- **Ted becomes the bottleneck anyway:** if every single message needs Ted's live attention, this isn't saving anything over the walled-off pattern — the point is Ted settling real judgment calls, not approving each mechanical step.
- **Silent scope creep on "the ship":** using this skill's live-collaboration feel to justify writes that should have gone through the meaning/authority gate — the workflow's step 4 exists specifically to prevent this.

## Runtime notes

### Claude Code (the filesystem/DB-capable actor)

Use `mcp__claude-in-chrome__*` tools to join the actual browser tab(s) where the ChatGPT-role actors are running — this requires Ted's real logged-in session, not the sandboxed in-app browser. Announce as `[Claude / CC]` on every message so authorship is unambiguous in the transcript. Verify every claim against live files/DB before acting on it or relaying it to another actor.

### ChatGPT role-runtime actors (Map Curator, Orchestrator, etc.)

Read and respond to messages in the shared thread as they would any other input; use existing tool surfaces for verification (e.g. `map_neighborhood` for graph claims); state plainly when a claim is outside what the role's own tools can check, rather than treating filesystem/code claims routed through CC as independently verified.

## Cross-references

`_shared/Cross_Actor_Communication.md` (**the live doctrine this skill must satisfy** — the four ways to reach another actor and the four guardrails) · `Operations/Resolved/Deep_Research_Multi_AI_API_Patterns_Report.md` (the evidence behind those guardrails: hub-and-spoke over peer chat, gating and heterogeneity for panels, conformity cascade) · `Canon/Reference/Decision_Principles.md` (the 2026-07-23 relaxation of "no AI-to-AI direct comms") · `/Volumes/Extra/Substrate/Substrate_v14/Chapters/15_Parallel_Agent_Coordination/PROJECTION.md` (the instance and open question, recorded 2026-07-26) · `Skills/cross-actor-incident-repair/SKILL.md` (carries the retired walled-off framing — needs its own update) · `/Volumes/Extra/Substrate/Roles/Role_Runtime_Architecture/MAP_CURATOR_CC_WORKING_AGREEMENT.md` (the durable output of the worked instance) · `/Volumes/Extra/Substrate/Roles/Role_Runtime_Architecture/Map_Curator_Working_Agreement_and_Auto_Inject_Session_Report.md` (full session account)
