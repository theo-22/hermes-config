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

### Knowledge-Capture (writes to _shared/)

- `share-learning`
  Use when a reusable pattern, technique, or operational finding should be saved to `_shared/` for fleet-wide visibility. Checks for duplicates, writes the pattern doc, updates `_shared/README.md`, and logs to CHANGES_LOG. Update this index only when a shared skill is added or existing shared-skill index wording/metadata changes.

### File-Write / Operational (reads system files, executes action sequences)

- `quick-save`
  Use when a bounded one-task session needs durable save/checkpoint treatment without full `/session-end`. Updates earned continuity surfaces, verifies touched repo state, names uncommitted work, and escalates to full session-end when the session is too broad.

- `workflow-orchestration`
  Use when Ted says "Let's get some work done" or asks to advance Operations session-chain work from the conductor board. Runs one routed chain through completion report, validation, QuickSave receipt, and stop.

- `project-room-review`
  Use when Ted asks to review, resume, orient, discuss, advance, save, or decide the next move for a Project Room. Reads room-local state first, checks v1-readiness, and prepares bounded save or QuickSave-chain handoffs without broadening into implementation.

- `codex-usage-audit`
  Use when Codex itself needs an efficiency/reliability pass. Audits AGENTS, config, hooks, MCP/plugins, slash/status surfaces, repeated workflows, paste-heavy workflows, subagent fit, and review wiring before proposing small patches.

- `repair-capability-truth`
  Use when a role's fresh-session callable surface, static scope, current documentation, and typed operational queries disagree. Separates evidence layers, preserves specialist-role inhabitation, repairs full live-schema mappings without migration, and requires direct plus aggregate proof.

- `audit-yield-stamp`
  Use when completed audit case files lack a yield rating or have a Pending rating that needs recheck. Reads Findings + Recommended Next Move, verifies against a live evidence surface, writes the historical `## CC yield rating` stamp with citation. Falls back to `Pending — not verified this session` when verification isn't possible this session.

- `builder-batch`
  Use when GPT Builder changes have accumulated and Ted is ready for a fleet pass. Reads `/api/gpt-status` work queue + `Builder_Update_Batch.md`, executes the four-step checklist per pending GPT, requires proof receipts before marking complete. Composes `gpt-instructions-discipline` and `gpt-environment-build`.

- `workspace-orchestration-coordination`
  Use when multiple AI actors (Hermes, ga-hermes, CC, Codex) need to edit the same shared GPT source files without lost-update overwrites. Extends `SURFACE_RESERVATIONS.md` + `CONDUCTOR.md` check-in/check-out to GPT source files.

- `role-workspace-sufficiency`
  Use when creating, converting, reviewing, or repairing a role-runtime role and the question is whether it has enough continuity, scratch, staged output, receipts, telemetry, persistence, sandbox folders, or anti-curtailment room to function well without broad write access.

- `role-hermes-worker-access`
  Use when a ChatGPT role-runtime role needs direct Hermes worker dispatch or a review of worker authority. Designs role-specific wrappers, path fences, proof receipts, and narrow per-role access instead of exposing broad `dispatch_worker` by default.

- `coordinator-hermes-work-loop`
  Use when Ted and Coordinator produce something that should become a durable handoff — a file placement, scan, report, or cleanup task. Coordinator shapes intent into a bounded Hermes handoff; Hermes evaluates for flow/friction before executing.

- `image-factory-16x9-replacement-workflow`
  Use when Ted asks Image Factory to generate and place a 16:9 replacement candidate — "let's generate a replacement," "do a 16:9 replacement run," "continue the replacement program." Runs generate → stage → inspect → label → move (dry-run then live) → sidecar → record-change as one accountable loop; flags an incomplete run (esp. missing sidecar) instead of reporting false success.

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

- `ht-grocery`
  Use for Harris Teeter grocery site automation — My Specials, Weekly Ad, cart, checkout. CDP browser patterns for the site's React SPA, including the click-doesn't-fire workaround. Human in the loop on checkout; never auto-submits orders.

- `live-session-to-skill`
  Use when a live collaborative browsing/automation session (Ted + Hermes navigating a site together) has just proven a working pattern and it should be captured as a reusable skill before the session ends. 5-phase loop: do → learn → capture skill → improve plans → hand off buildout.

### Judgment-Only (no database writes)

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

- `gpt-instructions-discipline`
  Use when GPT Custom Instructions are near the 8000-char limit or OpenAPI action descriptions are near the 300-char limit and need principled trimming that preserves behavior. Not for ordinary prompt polish.

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
- `synthesis-review` = synthesize accumulated evidence
- `skills-review` = review the skill set itself
- `surface-routing` = place it where the system will see it
- `clip-cycle-closer` = name the cycle as closed and draft the record
- `gpt-instructions-discipline` = trim GPT instructions under hard platform limits
- `gpt-environment-build` = build or repair the whole Custom GPT environment
- `affected-gpt-hearing` = hear the GPT whose operating surface would change
- `digest-topic-refresh` = compare digest deltas against a living topic
- `live-surface-verification` = prove the live surface before trusting docs
- `quick-save` = save a bounded task without full session-end
- `workflow-orchestration` = run one conductor-routed work lane
- `project-room-review` = review a Project Room from live room-local state
- `codex-usage-audit` = audit Codex overhead before patching
- `repair-capability-truth` = reconcile live capability, current docs, and typed operational queries
- `audit-yield-stamp` = verify and stamp audit case files
- `builder-batch` = run the Builder update queue across the fleet
- `manager-handoff-contract` = shape worker output into a manager-ready handoff

- `profile-birthday-proof` = birth or promote a profile with live-path proof, correction handling, and CHANGES_LOG

- `coordinator-hermes-work-loop` = Coordinator shapes handoff, Hermes evaluates and executes
- `role-workspace-sufficiency` = check and add enough owned workspace for a role-runtime role
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
| `synthesis-review` | Cross-pass sensemaking: synthesize accumulated findings or artifacts |
| `clip-cycle-closer` | Closure: name a completed or near-complete CLiP arc and draft the record |
| `surface-routing` | Routing/placement: land accepted material where the system will see it |
| `poka-yoke` | Structural prevention layer: replace memory-dependent prevention with durable design |
| `skills-review` | Maintenance loop: keep the skill set aligned with live practice |
| `project-room-review` | Room review loop: recover live room state, choose the next bounded move, and gate v1 orchestration |
| `live-surface-verification` | Verification: route proof to the actual runtime surface before changing docs or code |
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

If the main need is trimming GPT instructions under platform character limits:
- use `gpt-instructions-discipline`

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
- If there is only one document or one recommendation, `synthesis-review` is probably not the right skill.
- If the issue is not naming or proposal shape but `where should this now live so the right AI sees it later?` use `surface-routing`.
- If the issue is not just prompt trimming but the whole Custom GPT environment is failing across multiple layers, use `gpt-environment-build`.
- If the GPT environment change is proposed but the question is whether the affected GPT must be heard before settlement, use `affected-gpt-hearing`, not `gpt-environment-build`.
- If the issue is not summary but whether new digest material materially changes a living topic, use `digest-topic-refresh`.
- If the issue is disputed live state, do not infer from intended-state files; use `live-surface-verification`.
- If disputed live state has already proved stale capability docs or typed-query mappings and the authorized job is to repair and verify them, use `repair-capability-truth`; use `live-surface-verification` when the job is still proof-only.
- If the issue is one Project Room's current standing, next action, v1-readiness, or chain handoff, use `project-room-review`, not broad workspace discovery.
- If the issue is not yet proposal or implementation work but a worker output needs to be handed to Ted/Codex/Claude in a usable shape, use `manager-handoff-contract`.

## Exact Skill Names

- `affected-gpt-hearing`
- `audit-yield-stamp`
- `builder-batch`
- `check-system`
- `claude-validator`
- `clip-cycle-closer`
- `codex-usage-audit`
- `concept-bridge-surfacing`
- `context-extension-surfacing`
- `coordinator-consolidation-synthesis`
- `coordinator-hermes-work-loop`
- `create-worker`
- `dashboard-api`
- `digest-topic-refresh`
- `gpt-environment-build`
- `gpt-instructions-discipline`
- `ht-grocery`
- `icon-relocation-audit`
- `image-factory-16x9-replacement-workflow`
- `live-session-to-skill`
- `live-surface-verification`
- `manager-handoff-contract`
- `model-switch-surfacing`
- `pieces-ambient-lead-evaluation`
- `poka-yoke`
- `profile-birthday-proof`
- `project-room-review`
- `proposal-candidate-surfacing`
- `proposal-packet`
- `quick-save`
- `repair-capability-truth`
- `relocate-role-from-projects-gpt`
- `role-hermes-worker-access`
- `role-workspace-sufficiency`
- `scope-comparison`
- `share-learning`
- `signal-review`
- `skills-review`
- `structure-distinction-surfacing`
- `surface-routing`
- `synthesis-review`
- `system-14-update`
- `workflow-orchestration`
- `workspace-orchestration-coordination`
