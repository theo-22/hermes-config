# Shared Skill Index

Use this as the quick picker for the shared skills Ted created.

If the `/` menu is crowded, scan this card first, then search for the exact skill name.

## Fast Picks

### Database-Integrated (read/write system database)

- `check-system`
  Use on demand when you need a fast read of operational state. Database pulse: stats, clusters, pending items.

- `signal-review`
  Use when external signal or weak patterns need pressure-testing before entering the evidence base. Writes accepted units to database.

- `concept-bridge-surfacing`
  Use when a local idea or phrase wants the closest standard concept name. Checks database for existing bridges, writes new ones.

- `synthesis-review`
  Use when multiple findings, notes, or planning artifacts have accumulated and need a cross-pass synthesis. Reads clusters from database.

- `surface-routing`
  Use when a good observation or proposal needs to land on the right surface. Routes to database for structured state, files for deep content.

- `proposal-packet`
  Use when the proposal already exists and you want a compact durable packet for evaluation or handoff. Tracks in database.

- `compile-work-packet`
  Use after external authorization when consequential asynchronous or cross-actor work needs a versioned execution contract. Lints schema-defined critical fields, fingerprints the packet, and requires a bounded cold executability probe without treating readability as approval or correctness.

- `graph-edge-finding`
  Use when a graph node is thin, orphaned, or "feels" disconnected. Finds its real missing edges and writes them to database.

- `topic-assembly`
  Use when a live discussion topic deepens and should be assembled into its connected node-neighborhood, not just discussed. Writes nodes/edges to database. Stage 1 of `lens-assembly-pass`.

- `cold-probe-refine`
  Use when a load-bearing, newly refined, or cheap-model-facing inference surface needs a reconstructability test. Runs cheap/fast cold first, stronger semantic review second, classifies projection versus traversal/model/infrastructure failure, and lands comparable Lab evidence without mutating graph meaning automatically.

- `lens-assembly-pass`
  **The engine — start here for concept-map work.** Use when a topic is worth laying down rather than just discussed, or when a session produced understanding that will otherwise evaporate. Runs assemble (`topic-assembly`) → optional probe/refine (`cold-probe-refine`) → fortify (spine verdict: realized / gap / drift) → persist.

- `persist`
  Use as the never-skipped closing step of any concept work — writes the idea to all three durable surfaces (Brain, memory file + `MEMORY.md` pointer, buoyancy touch). Callable alone. Not a substitute for `quick-save`/`session-end`: those close a session, this closes an idea.

### Knowledge-Capture (writes to _shared/)

- `share-learning`
  Use when a reusable pattern, technique, or operational finding should be saved to `_shared/` for fleet-wide visibility. Checks for duplicates, writes the pattern doc, updates `_shared/README.md`, and logs to CHANGES_LOG. Update this index only when a shared skill is added or existing shared-skill index wording/metadata changes.

### File-Write / Operational (reads system files, executes action sequences)

- `quick-save`
  Use when a bounded one-task session needs durable save/checkpoint treatment without full `/session-end`. Updates earned continuity surfaces, verifies touched repo state, names uncommitted work, and escalates to full session-end when the session is too broad.

- `shape-work-item-sessions`
  Use when Ted reviews or reroutes live work items and wants them set up as future sessions. Classifies each row as runnable, discussion-gated, waiting, routed, multi-session, closeable, or unresolved; appends cold-readable session contracts; verifies any closure; and recommends one next session without executing the shaped backlog.

- `route-work-item-ownership`
  Use after Coordinator or Ted has already settled a queue-routing decision and the canonical work-item owner must change, or obsolete framing must be superseded with a linked successor. Preserves history and draft authority, stale-checks the live row, proves receiving-role visibility, and closes with audited readback and released claims.

- `reconcile-stale-decision-work-item`
  Use when a live decision row or consumer says a question is open but primary authority and audit history may show it was already settled. Proves the authority chain, guards owner-attributed relay, reconciles only stale canonical or projected surfaces, and requires persisted terminal readback plus released claims.

- `repair-claim-effect-truth`
  Use when a claim or retry unexpectedly changes canonical work-item ownership, a composite coordination label is parsed as one item, or a blocked response hides effects already produced by the held claim. Separates coordination identity from routing authority, restores state through audited control-plane paths, preserves legitimate single-item behavior, and requires installed-path audit proof.

- `workflow-orchestration`
  Use when Ted says "Let's get some work done" or asks to advance Operations session-chain work from the conductor board. Runs one routed chain through completion report, validation, QuickSave receipt, and stop.

- `reconcile-inbox-work-items`
  Use when an `_AI_Inbox` packet represents actionable work or evidence, a stale packet must be proven open/closed, or a work item with an originating packet is completing. Classifies intake, preserves N:M provenance, closes the packet through terminal work state, and verifies reconciliation.

- `reconcile-promoted-findings-work-items`
  Use when an audit/findings sweep has inflated the live queue by treating undispositioned findings as authorized current work. Identifies the exact promotion cohort, preserves unresolved findings as `known_backlog`, closes only evidence-proven exceptions, applies through a guarded transaction with rollback, retires stale projections, and proves the survivor queue.

- `project-room-review`
  Use when Ted asks to review, resume, orient, discuss, advance, save, or decide the next move for a Project Room. Reads room-local state first, checks v1-readiness, and prepares bounded save or QuickSave-chain handoffs without broadening into implementation.

- `contradiction-sweep`
  Use before a session close or handoff when several durable artifacts were written in one sitting. Hands them to a different, cheaper, uncommitted model and asks only for contradictions between them — because an author cannot find the ones he resolved without noticing, a resolved contradiction being experienced as settled rather than smoothed. Pre-register a predicted count; the gap is the finding. Sort returns into defects (fix) and tensions (preserve unresolved).

- `opus-review-surfacing`
  Use proactively after a real, structurally significant chunk of work has landed in a long session — not just a contradiction check, a full bearings pass. Packages the specific files/DB state (not the raw transcript), dispatches an uncommitted Opus reviewer told explicitly to find problems (blind spots, premature actions, unverified claims presented as confirmed) rather than summarize, and surfaces the result honestly either way. Ted's named general rhythm: "assembling my never ending string of ideas, packaging now and then to get our bearings."

- `codex-usage-audit`
  Use when Codex itself needs an efficiency/reliability pass. Audits AGENTS, config, hooks, MCP/plugins, slash/status surfaces, repeated workflows, paste-heavy workflows, subagent fit, and review wiring before proposing small patches.

- `repair-capability-truth`
  Use when a role's fresh-session callable surface, static scope, current documentation, and typed operational queries disagree. Separates evidence layers, preserves specialist-role inhabitation, repairs full live-schema mappings without migration, and requires direct plus aggregate proof.

- `reconcile-runtime-authority`
  Use when startup, continuity, configuration, generated reports, or documentation disagree about which surface is authoritative. Classifies active, state, generated, tombstone, and historical surfaces; reconciles readers and writers; and requires deterministic plus genuinely fresh-runtime proof.

- `repair-retired-path-recreation`
  Use when a moved or retired filesystem path reappears. Correlates timestamps with live schedulers and processes, reconciles tracked/installed/published copies, preserves recreated state, adds a no-recreation guard, and proves the exact installed consumer writes only to the canonical destination.

- `update-protected-generated-artifacts`
  Use when a source generator or builder rewrites shared primary artifacts plus frontend, published, installed, or build mirrors. Acquires typed checkouts for the source and every target, verifies expected pre-write state, runs the sanctioned generator, proves byte parity and preserved meaning/data, verifies the exact consumer path, then receipts and releases the lane.

- `register-concept-map-viewer-layer`
  Use when an already-curated Concept Graph domain needs its human-visible filter button. Adds one registry row only, claims every builder output, regenerates through the installed path, proves exact isolated and Merged behavior in a real browser, and receipts zero node/road mutation.

- `calibrate-advisory-hook`
  Use for one recurring advisory work item: classify genuine catches, false positives, and uncertain evidence; tune only the supported class; distinguish fixture from real runtime proof; preserve recurrence visibility and verify closeout.

- `verify-real-invocation-path`
  Use when a fix, hook, script, service, launcher, or integration is called verified but the evidence may have exercised a proxy, stale path, interpreter shortcut, wrong cwd/environment, health-only surface, or warmed client instead of the exact installed consumer path—or when an independent real-client probe contradicts green local tests. Requires paired real-path probes, observable consequences, an evidence-led contradiction-repair loop, and independent/fresh-client/human gates when applicable.

- `repair-model-visible-token-transport`
  Use when a model, client, or safety layer blocks credential-shaped tool arguments before they reach the server. Replaces raw token transport with short server-resolved handles while preserving scope, expiry, restart invalidation, fail-closed checks, and layered live proof.

- `repair-mcp-client-disconnects`
  Use when an MCP bridge logs expected SSE or streamable-HTTP client disconnect errors, unhandled AnyIO exception groups, intermittent restarts, or post-disconnect hangs. Suppresses only proven disconnect leaves, preserves cancellation and unrelated faults, and requires authenticated abrupt-disconnect plus fresh-client proof.

- `migrate-mcp-secret-to-keychain`
  Use when a macOS MCP access key is duplicated in local code, keyed URLs, or client configs and Ted has authorized credential changes. Moves one secret to a Keychain-backed shared stdio proxy, removes active plaintext copies, and proves a real workload plus fail-closed behavior without printing the value.

- `repair-hermes-update-continuity`
  Use before a Hermes update or when sessions/profiles disappear, Desktop fails after an update, or CLI/Desktop state disagrees. Takes read-only pre/post session snapshots, distinguishes real row loss from cache/profile/home/version drift, requires SQLite-safe backup, and proves both the session corpus and Ted-facing client before completion.

- `repair-pieces-runtime`
  Use when PiecesOS, an LTM query, scheduled ingestion, continuity digests, or downstream reporting appears broken. Separates the runtime, producer jobs, and report consumers; distinguishes active jobs from paused duplicates and historical model-drift evidence; catches retired digest paths; and requires a real LTM query plus affected-layer proof before repair is complete.

- `cross-actor-incident-repair`
  Use when a live fault spans siloed actors — one role/GPT surfaces a specific symptom, the filesystem-access actor diagnoses root cause (self-correcting wrong first guesses before handoff), and a different code-owning actor repairs inside its fence, with Ted conducting between the walled-off lanes. STATUS: proposed — Codex/ChatGPT surfacer/fixer lanes pending `CROSS_ACTOR_SKILL_REVIEW`.

- `live-multi-actor-negotiation`
  Use when a decision needs live, synchronous input from 2-3 standing AI actors with non-overlapping access (e.g. a ChatGPT role owning graph/role meaning, Claude Code owning filesystem/DB execution) — actors read and answer each other directly in a shared thread, Ted present throughout, every claim independently re-verified before acting. STATUS: proposed — flags a real, unresolved tension with `cross-actor-incident-repair`'s walled-off-by-design premise; pending Opus adversarial review and Ted sign-off before treated as settled.

- `verify-curator-return`
  Use immediately after a live verifying actor (Map Curator or similar) reports back on CC-authored work — read the raw rows it touched, apply verdicts including ones that reject CC's own edges, append attribution corrections without rewriting the verifier's events, separate what it fixed from what only CC can reach, and catch claims it corrected in prose, not just relation/edge types. The receiving-side counterpart to `live-multi-actor-negotiation` and `live-surface-verification` — neither covers what happens with the report once it lands.

- `audit-yield-stamp`
  Use when completed audit case files lack a yield rating or have a Pending rating that needs recheck. Reads Findings + Recommended Next Move, verifies against a live evidence surface, writes the historical `## CC yield rating` stamp with citation. Falls back to `Pending — not verified this session` when verification isn't possible this session.

- `review-canon-membership`
  Use when Canon files, batches, specimens, or mixed doctrine/current-state documents need an independent Keep / Keep-trim / Move / Extract verdict. Reads the live criterion and current file bodies, preserves reviewer independence, requires failed-test evidence for non-Keep verdicts, routes a comparison-ready return, and stops before Ted-authorized mutation.

- `builder-batch`
  Use when GPT Builder changes have accumulated and Ted is ready for a fleet pass. Reads `/api/gpt-status` work queue + `Builder_Update_Batch.md`, executes the four-step checklist per pending GPT, requires proof receipts before marking complete. Composes `gpt-environment-build`.

- `workspace-orchestration-coordination`
  Use when multiple AI actors (Hermes, ga-hermes, CC, Codex) need to edit the same shared GPT source files without lost-update overwrites. Extends `SURFACE_RESERVATIONS.md` + `CONDUCTOR.md` check-in/check-out to GPT source files.

- `role-workspace-sufficiency`
  Use when creating, converting, reviewing, or repairing a role-runtime role and the question is whether it has enough continuity, scratch, staged output, receipts, telemetry, persistence, sandbox folders, or anti-curtailment room to function well without broad write access.

- `build-inhabitable-role`
  Use when a role emerges from conversation, specifies its own workspace, must be portable across ChatGPT/Codex/Claude/Hermes, or needs separate inhabitability, operability, runtime-integration, and clean-exit proofs.

- `role-contract-boundary-reconciliation`
  Use when a durable role runtime's job, neighboring-role boundaries, Home ownership, continuity authority, static access, live doctrine, or orchestration identity disagree. Reconciles the complete contract and existing authority, requires exact positive/negative proof plus independent verification, and stops before fresh-session acceptance, map mutation, new capability, or fleet rollout.

- `role-hermes-worker-access`
  Use when a ChatGPT role-runtime role needs direct Hermes worker dispatch or a review of worker authority. Designs role-specific wrappers, path fences, proof receipts, and narrow per-role access instead of exposing broad `dispatch_worker` by default.

- `coordinator-hermes-work-loop`
  Use when Ted and Coordinator produce something that should become a durable handoff — a file placement, scan, report, or cleanup task. Coordinator shapes intent into a bounded Hermes handoff; Hermes evaluates for flow/friction before executing.

- `image-factory-16x9-replacement-workflow`
  Use when Ted asks Image Factory to generate, capture, place, recover, or export native-16:9 replacement keepers. Preserves exact-byte identity, dry-run/no-overwrite placement, sidecar titles, durable partial-state recovery, globally collision-safe `All_Burn` output names, and evidence stronger than counts or worker text.

- `image-factory-mixed-replacement-batch-generation`
  Use when Image Factory needs mixed-subject native-16:9 generation briefs. Describe each image independently without image counts or exhibit/replacement/workflow language; use `image-factory-16x9-replacement-workflow` for capture, placement, recovery, and export.

- `profile-birthday-proof`
  Use when a new AI profile, Hermes profile, role runtime, agent, or major operating surface needs first-wake/birthday proof. Requires live path verification, session-start artifact, proof note, correction handling, honest BORN status, and CHANGES_LOG when durable state changes.

- `dashboard-api`
  Use when Substrate-Hermes or any profile needs live Hermes Dashboard data — cron health, log anomalies, gateway status, session activity, or config verification. 5 reusable API functions, shared across all profiles.

- `model-switch-surfacing`
  Use when the active model is wrong for the task — Flash on a deep reasoning chain, or Pro on simple edits. Surfaces a quick upgrade/downgrade decision to Ted. Does not switch automatically. Judgment-only, no file writes.

- `system-14-update`
  Use when Ted says "update System 14" or work has landed in a chapter room. Update the chapter first, then thread upward into the spine and Home files. No parallel plans, no chat-only summaries.

- `icon-relocation-audit`
  Use when a root has been relocated from ~/ to Extra and icon scripts need dual-path updates. Audit families, update scripts, backup, dry-run, apply, write receipt.

- `icon-image-processor`
  Icon System capability — generates/processes candidate icon images. Never applies them to Finder; that stays with `icon-apply-sort` under the Icon System ROLE_CONTRACT split.

- `icon-apply-sort`
  Icon System capability — sorts and applies processed icon images to their Finder targets. Paired with `icon-image-processor`, which only produces the images.

- `ht-grocery`
  Use for Harris Teeter grocery site automation — My Specials, Weekly Ad, cart, checkout. CDP browser patterns for the site's React SPA, including the click-doesn't-fire workaround. Human in the loop on checkout; never auto-submits orders.

- `live-session-to-skill`
  Use when a live collaborative browsing/automation session (Ted + Hermes navigating a site together) has just proven a working pattern and it should be captured as a reusable skill before the session ends. 5-phase loop: do → learn → capture skill → improve plans → hand off buildout.

### Judgment-Only (no database writes)

- `support-response-drafting`
  Use when a vendor-support case remains unresolved and the latest reply needs a concise, case-linked escalation. Distinguishes troubleshooting, documentation, or an internal tool limitation from resolution; preserves exact targets and protected neighboring objects; drafts only unless sending is explicitly authorized.

- `trace-claim-evidence`
  Use when a concrete AI assertion must be checked against the exact tool evidence available before it was stated, when replaying known wrong claims, or when deciding whether a watch-only detector has earned promotion. Preserves intermediate text and event order, separates relevance from support, allows `not_established`, and keeps machine status distinct from human calibration.

- `manager-handoff-contract`
  Use when Hermes, a cheaper model, an overnight monitor, a Home report, or a conversation has produced shaped material that may need Ted/Codex/Claude manager review. Defines required outcomes for the handoff without approving, implementing, or preserving every thought.

- `structure-distinction-surfacing`
  Use when the question is what kind of thing something is: skill, script, environment, procedure, guardrail, source of truth.

- `poka-yoke`
  Use when the question is how to stop a recurring failure from depending on memory, reminders, or convention.

- `proposal-candidate-surfacing`
  Use when a conversation feels like it is becoming proposal-shaped and the candidate needs to be brought into focus through discussion before `/proposal-packet` writes it. Names the threshold, surfaces what's clear vs. fuzzy, and calls ready-or-not. Stops before writing.

- `context-extension-surfacing`
  Use when work in the primary conversation is ready to leave as a bounded agent briefing. Names the threshold, shapes the cold briefing, and keeps agent execution decision-free, bounded, and checkable.

- `skills-review`
  Use when the shared skill set itself needs cleanup, gap review, overlap review, or sharper trigger conditions.

- `clip-cycle-closer`
  Use when a session appears to have completed a CLiP arc (Canon-level, domain-level, bridge adoption, adversarial review) and you need a concise evidence-backed closure record. Does not promote, log silently, or mutate state.

- `gpt-environment-build`
  Use when a Custom GPT needs full environment work across instructions, knowledge files, action schema, backend or proxy alignment, Builder updates, and live verification. Not just prompt trimming.

- `affected-gpt-hearing`
  Use when a proposed GPT/system change may affect another GPT's startup behavior, runtime path, handoff, continuity, authority boundary, or action/tool shape and the affected GPT needs to be heard before settlement.

- `digest-topic-refresh`
  Use when a new digest may materially change an existing living topic and you need a disciplined `no change` / `update` / `create` call rather than a summary.

- `pieces-ambient-lead-evaluation`
  Use when Ted asks how Pieces (or another ambient-memory tool) can serve the system, or when a Pieces lead should be turned into verified local work. Treats Pieces as overview, not authority — classify threads, then verify against live owner files before acting.

- `live-surface-verification`
  Use when docs, schemas, env vars, Builder inventory, backend code, or memory disagree about live GPT/Builder/proxy state. Prove the real surface first: ask the GPT for a harmless raw action result, inspect Builder with Chrome, or use backend logs before patching.

- `claude-validator`
  Use when a Hermes profile wants outside assessment of work quality and blind spots. Sends self-assessment + work samples to Claude Code, Claude returns Quality Assessment, Self-Assessment Review, Blind Spots, Recommendations, and Summary Verdict. 3 clean assessments → spot-check.

## One-Line Distinctions

- `share-learning` = capture a reusable pattern to _shared/ for all actors
- `check-system` = read the system pulse
- `signal-review` = pressure-test and save evidence
- `concept-bridge-surfacing` = name the idea
- `structure-distinction-surfacing` = classify the layer
- `poka-yoke` = choose structural prevention
- `proposal-candidate-surfacing` = surface and shape the candidate until packet-ready
- `context-extension-surfacing` = surface and shape agent-ready work before dispatch
- `proposal-packet` = write the actual proposal packet
- `compile-work-packet` = compile externally authorized intent for bounded dispatch
- `synthesis-review` = synthesize accumulated evidence
- `skills-review` = review the skill set itself
- `support-response-drafting` = turn the latest vendor-support reply into a bounded, outcome-driven escalation
- `surface-routing` = place it where the system will see it
- `clip-cycle-closer` = name the cycle as closed and draft the record
- `gpt-environment-build` = build or repair the whole Custom GPT environment
- `affected-gpt-hearing` = hear the GPT whose operating surface would change
- `digest-topic-refresh` = compare digest deltas against a living topic
- `live-surface-verification` = prove the live surface before trusting docs
- `trace-claim-evidence` = match each assertion to prior evidence before judging or promoting a detector
- `quick-save` = save a bounded task without full session-end
- `shape-work-item-sessions` = turn live queue rows and current decisions into bounded future-session contracts
- `reconcile-promoted-findings-work-items` = withdraw an invalid findings-to-work bulk promotion without losing unresolved findings
- `route-work-item-ownership` = land an authorized canonical retarget or linked supersession without widening execution authority
- `reconcile-stale-decision-work-item` = prove whether a decision is truly open and reconcile stale surfaces to settled authority without re-deciding it
- `repair-claim-effect-truth` = stop coordination claims from becoming silent owner changes and make held-claim effects visible
- `workflow-orchestration` = run one conductor-routed work lane
- `project-room-review` = review a Project Room from live room-local state
- `contradiction-sweep` = a cold model finds the contradictions you smoothed over
- `opus-review-surfacing` = proactive full bearings-check on a real chunk of landed work, uncommitted Opus reviewer
- `codex-usage-audit` = audit Codex overhead before patching
- `repair-capability-truth` = reconcile live capability, current docs, and typed operational queries
- `repair-retired-path-recreation` = trace every live recreator, preserve state, repoint the full chain, and prove the retired root stays absent
- `update-protected-generated-artifacts` = protect the generator and every output, regenerate once, prove parity and real consumer behavior
- `repair-mcp-client-disconnects` = narrowly handle and live-prove normal MCP transport disconnects
- `repair-hermes-update-continuity` = preserve and prove sessions across Hermes updates before repairing visibility or version skew
- `repair-hermes-provider-transport` = isolate an exact-body SDK/httpx differential, contain the adapter to one profile, and stop before unauthorized provider spend
- `repair-pieces-runtime` = prove Pieces runtime, producer jobs, and report consumers separately; repair only the failed layer
- `cross-actor-incident-repair` = diagnose→handoff→repair→verify a fault across siloed actors, Ted conducting (proposed)
- `live-multi-actor-negotiation` = live shared-thread dialogue between 2-3 standing actors, Ted present, every claim independently re-verified (proposed, tension with cross-actor-incident-repair unresolved)
- `verify-curator-return` = read the verifier's raw state, don't just file the verdict
- `audit-yield-stamp` = verify and stamp audit case files
- `review-canon-membership` = independently classify Canon membership without mutating Canon
- `builder-batch` = run the Builder update queue across the fleet
- `manager-handoff-contract` = shape worker output into a manager-ready handoff

- `profile-birthday-proof` = birth or promote a profile with live-path proof, correction handling, and CHANGES_LOG

- `coordinator-hermes-work-loop` = Coordinator shapes handoff, Hermes evaluates and executes
- `role-workspace-sufficiency` = check and add enough owned workspace for a role-runtime role
- `build-inhabitable-role` = build a portable role through self-specification, inhabitability, real-work operability, runtime adapters, and clean exit
- `role-contract-boundary-reconciliation` = reconcile a role's job, ownership, continuity, access, and lifecycle identity without adding capability
- `role-hermes-worker-access` = design/review role-scoped Hermes worker dispatch without broad generic worker access
- `dashboard-api` = monitor Hermes Dashboard for cron health, logs, and gateway status
- `system-14-update` = update the System 14 plan — chapter-first, then thread upward
- `icon-relocation-audit` = update icon scripts for relocated ~/→Extra roots
- `claude-validator` = send work samples to Claude for external validation and blind-spot detection

## CLiP Role Map

Use this as orientation only; the individual skill trigger still decides whether a skill actually fires.

| Skill | CLiP role |
|---|---|
| `signal-review` | Capture: pressure-test observations before evidence entry |
| `concept-bridge-surfacing` | Observation/Capture: map local terms to established concepts |
| `proposal-candidate-surfacing` | Discovery: shape a forming proposal through conversation until ready for the packet skill |
| `context-extension-surfacing` | Context preservation: shape determinate work into bounded agent briefings so the primary conversation stays available for judgment and learning |
| `proposal-packet` | Synthesis output: shape an already-real proposal for evaluation or handoff |
| `compile-work-packet` | Execution intake: compile externally authorized intent into a linted and cold-readable contract |
| `shape-work-item-sessions` | Work intake: reconcile live queue rows with current decisions and make future sessions cold-readable before stronger orchestration or dispatch |
| `reconcile-promoted-findings-work-items` | Queue repair: withdraw an invalid findings promotion, preserve unresolved evidence, and prove the corrected live survivor set |
| `route-work-item-ownership` | Queue transition: atomically land a settled owner retarget or linked supersession while preserving authority and history |
| `reconcile-stale-decision-work-item` | Decision reconciliation: prove the authority chain, preserve genuine gates, and close stale open-decision rows without manufacturing judgment |
| `synthesis-review` | Cross-pass sensemaking: synthesize accumulated findings or artifacts |
| `clip-cycle-closer` | Closure: name a completed or near-complete CLiP arc and draft the record |
| `surface-routing` | Routing/placement: land accepted material where the system will see it |
| `poka-yoke` | Structural prevention layer: replace memory-dependent prevention with durable design |
| `skills-review` | Maintenance loop: keep the skill set aligned with live practice |
| `project-room-review` | Room review loop: recover live room state, choose the next bounded move, and gate v1 orchestration |
| `live-surface-verification` | Verification: route proof to the actual runtime surface before changing docs or code |
| `trace-claim-evidence` | Evidence calibration: preserve chronology, attribute assertions to prior results, and keep support separate from human verdicts |
| `scope-comparison` | Selection-time discipline: write the asked/proposing/gap surface before committing to a scope |
| `affected-gpt-hearing` | Settlement evidence: get affected-GPT operational input before changing another GPT's operating surface |
| `manager-handoff-contract` | Manager intake: shape lower-cost worker or Hermes output so Ted/Codex/Claude can accept, reject, discard, fold in, or route forward |
| `role-workspace-sufficiency` | Capability design: make sure a role has owned continuity/scratch/staged/receipt surfaces without broad write access |
| `role-hermes-worker-access` | Capability/access design: add or review bounded Hermes worker dispatch through role-specific wrappers and fences |

## Short Routing Guide

If the main need is "where are we?":
- use `check-system`

If the main need is vetting new signal:
- use `signal-review`

If the main need is naming:
- use `concept-bridge-surfacing`

If the main need is classification:
- use `structure-distinction-surfacing`

If the main need is structural prevention:
- use `poka-yoke`

If the main need is recognizing a forming proposal and shaping it through conversation:
- use `proposal-candidate-surfacing`

If the main need is moving determinate side work out of the primary chat as a bounded agent briefing:
- use `context-extension-surfacing`

If the main need is durable proposal shaping:
- use `proposal-packet`

If the main need is cross-round or cross-document synthesis:
- use `synthesis-review`

If the main need is maintaining the shared skills:
- use `skills-review`

If the main need is getting an observation onto the right live and resurfacing surfaces:
- use `surface-routing`

If the main need is closing out a CLiP arc with a small durable record:
- use `clip-cycle-closer`

If the main need is making the whole Custom GPT environment work across Builder, schema, backend, proxy, and live verification:
- use `gpt-environment-build`

If the main need is deciding whether another GPT must be heard before its operating surface changes:
- use `affected-gpt-hearing`

If the main need is deciding whether new digest material changes an existing living topic:
- use `digest-topic-refresh`

If the main need is verifying what a GPT/Builder/proxy/action is actually doing:
- use `live-surface-verification`

If the main need is saving one bounded task without full session-end:
- use `quick-save`

If the main need is turning a live backlog review into runnable, discussion, waiting, routed, or closeable future sessions:
- use `shape-work-item-sessions`

If the main need is reviewing or resuming a Project Room from live state:
- use `project-room-review`

If the main need is reducing Codex context, tool, MCP, reasoning, subagent, or review-loop waste:
- use `codex-usage-audit`

If fresh-session role capability, current documentation, and typed operational queries disagree:
- use `repair-capability-truth`

If the main need is rating and closing out accumulated audit case files:
- use `audit-yield-stamp`

If the main need is running the accumulated GPT Builder queue:
- use `builder-batch`

If the main need is shaping Hermes, cheap-model, overnight, or conversational output for Ted/Codex/Claude manager review:
- use `manager-handoff-contract`

If the main need is deciding whether a role has enough workspace or sandbox to function well:
- use `role-workspace-sufficiency`

If a role is emerging, specifying its own environment, crossing runtimes, or needs an entry/operate/exit lifecycle:
- use `build-inhabitable-role`

If the role's job, neighboring-role boundary, Home ownership, continuity authority, existing access, or lifecycle identity disagree:
- use `role-contract-boundary-reconciliation`

If the main need is deciding whether a role may safely dispatch Hermes workers:
- use `role-hermes-worker-access`

## Common Confusions

- If you want a snapshot of system state, use `check-system`, not `signal-review`.
- If you want to pressure-test new input, use `signal-review`, not `synthesis-review`.
- If you are asking "what do we call this?" use `concept-bridge-surfacing`, not `structure-distinction-surfacing`.
- If you are asking "what kind of thing is this?" use `structure-distinction-surfacing`, not `concept-bridge-surfacing`.
- If you are asking "how do we stop this from depending on memory or convention?" use `poka-yoke`.
- If a proposal is forming and the enough-for-use version, boundaries, or open questions are still ambiguous, use `proposal-candidate-surfacing` first to shape it. `proposal-packet` writes; it doesn't discover.
- If the proposal is already real and needs a durable shape, use `proposal-packet`.
- If the proposal is externally authorized and another actor needs a bounded execution contract, use `compile-work-packet` before consequential dispatch.
- If the authoritative queue rows already exist but need current routing, gates, scope, proof, and stop conditions for future sessions, use `shape-work-item-sessions`; use `workflow-orchestration` only when a conductor chain is actually being staged or run.
- If the routing decision is already settled and the live queue address itself must change, use `route-work-item-ownership`; do not use session shaping or a direct owner update as a substitute.
- If there is only one document or one recommendation, `synthesis-review` is probably not the right skill.
- If the issue is not naming or proposal shape but `where should this now live so the right AI sees it later?` use `surface-routing`.
- If the issue is not just prompt trimming but the whole Custom GPT environment is failing across multiple layers, use `gpt-environment-build`.
- If the GPT environment change is proposed but the question is whether the affected GPT must be heard before settlement, use `affected-gpt-hearing`, not `gpt-environment-build`.
- If the issue is not summary but whether new digest material materially changes a living topic, use `digest-topic-refresh`.
- If a local macOS MCP key is hardcoded or duplicated across clients, use `migrate-mcp-secret-to-keychain`; use `repair-model-visible-token-transport` when the failure is a model/client refusing to transmit a credential-shaped tool argument.
- If the issue is disputed live state, do not infer from intended-state files; use `live-surface-verification`.
- If disputed live state has already proved stale capability docs or typed-query mappings and the authorized job is to repair and verify them, use `repair-capability-truth`; use `live-surface-verification` when the job is still proof-only.
- If the issue is one Project Room's current standing, next action, v1-readiness, or chain handoff, use `project-room-review`, not broad workspace discovery.
- If the issue is not yet proposal or implementation work but a worker output needs to be handed to Ted/Codex/Claude in a usable shape, use `manager-handoff-contract`.
- If vendor support has explained a limitation or repeated troubleshooting without completing the requested outcome, use `support-response-drafting`; keep the existing case linkage and exact scope boundary.

## Exact Skill Names

- `build-inhabitable-role`
- `affected-gpt-hearing`
- `audit-yield-stamp`
- `calibrate-advisory-hook`
- `builder-batch`
- `check-system`
- `claude-validator`
- `clip-cycle-closer`
- `codex-usage-audit`
- `concept-bridge-surfacing`
- `cold-probe-refine`
- `compile-work-packet`
- `contradiction-sweep`
- `context-extension-surfacing`
- `coordinator-consolidation-synthesis`
- `coordinator-hermes-work-loop`
- `create-worker`
- `dashboard-api`
- `digest-topic-refresh`
- `gpt-environment-build`
- `graph-edge-finding`
- `ht-grocery`
- `icon-relocation-audit`
- `icon-image-processor`
- `icon-apply-sort`
- `image-factory-16x9-replacement-workflow`
- `image-factory-mixed-replacement-batch-generation`
- `lens-assembly-pass`
- `live-session-to-skill`
- `live-surface-verification`
- `manager-handoff-contract`
- `migrate-mcp-secret-to-keychain`
- `model-switch-surfacing`
- `opus-review-surfacing`
- `persist`
- `pieces-ambient-lead-evaluation`
- `poka-yoke`
- `profile-birthday-proof`
- `project-room-review`
- `proposal-candidate-surfacing`
- `proposal-packet`
- `quick-save`
- `register-concept-map-viewer-layer`
- `repair-capability-truth`
- `repair-claim-effect-truth`
- `reconcile-inbox-work-items`
- `reconcile-promoted-findings-work-items`
- `reconcile-runtime-authority`
- `reconcile-stale-decision-work-item`
- `repair-retired-path-recreation`
- `repair-mcp-client-disconnects`
- `repair-model-visible-token-transport`
- `repair-hermes-provider-transport`
- `repair-hermes-update-continuity`
- `repair-pieces-runtime`
- `verify-real-invocation-path`
- `review-canon-membership`
- `cross-actor-incident-repair`
- `live-multi-actor-negotiation`
- `verify-curator-return`
- `relocate-role-from-projects-gpt`
- `role-contract-boundary-reconciliation`
- `role-hermes-worker-access`
- `role-workspace-sufficiency`
- `route-work-item-ownership`
- `scope-comparison`
- `shape-work-item-sessions`
- `share-learning`
- `signal-review`
- `skills-review`
- `structure-distinction-surfacing`
- `support-response-drafting`
- `surface-routing`
- `synthesis-review`
- `system-14-update`
- `topic-assembly`
- `trace-claim-evidence`
- `update-protected-generated-artifacts`
- `workflow-orchestration`
- `workspace-orchestration-coordination`
