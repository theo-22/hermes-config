---
name: surface-routing
description: Route an observation, finding, proposal, or artifact onto the correct authoritative local file and the right AI-visible resurfacing surfaces. Use when there are multiple candidate surfaces and the right one is non-obvious, when AI-visible resurfacing (Coordinator, manifests, Seeds) needs updating alongside file placement, or when the local-vs-mirror distinction must be explicitly maintained. Do not use when routing is obvious and only one surface is in play — just do it inline.
category: database-integrated
write_mode: file
one_line_use: place it where the system will see it
fast_pick: "yes"
---

# Surface Routing

Place emerging work where the system will actually catch it later.

This skill is for the collection-and-placement step that sits between a good observation and a durable system-visible artifact.

For proposal packets specifically, assume inbox-first intake unless Ted says otherwise.
Choose the inbox by intended owner.

Use it when the question is not just `where should this file live?` but:

- what is the authoritative local source?
- what AI-visible surfaces should also reflect this?
- what tracking or resurfacing surfaces need to advance?
- what copies are mirrors only and must not be treated as live sources?
- what source surface should be cleared now that material has moved?

After creating or refining a durable artifact, check whether routing is now due before moving on. Do not wait to be asked.

## Inputs That Matter

- The observation, finding, proposal, or artifact being preserved
- The likely domain or concept home
- Which AI or workflow should be able to see it later
- Whether it should resurface through Seeds, accumulation, manifests, Coordinator, or another surface
- Whether any copies are mirrors, exports, or backups rather than live sources

## Database-First Routing

The system database is now the primary operational layer for structured state. Route to the database when the item has structure:

- **Signal evidence** (observation with tags): `POST /api/signal-evidence` — use `signal-review` skill for the full workflow
- **Concept bridge** (local term → standard concept): `POST /api/concept-bridges` — use `concept-bridge-surfacing` skill
- **Work item** (task, proposal, note with owner/state): `POST /api/work-items` — tracks across all surfaces
- **State change** (item acted/deferred/blocked): `POST /api/work-items/state` — with poka-yoke on deferred items

Files still serve as the human-readable surface and deep content store. The database tracks state, routing, and queryable metadata.

## Core Workflow

1. Identify the authoritative home — database or file.
If the item has structured state (tags, owner, phase, destination): database first, file second.
If the item is deep content (analysis, proposal text, findings): file first, database tracks it.

For proposal packets, the authoritative intake home is often an inbox surface because those are reviewed at session start.

Default owner rule:
- Codex-owned or Codex-implemented packet -> `/Users/ted/Codex_Inbox/` + `addWorkItem` with source_surface
- Claude Code-owned, Canon-affecting, shared-infrastructure, or cross-system packet -> `/Users/ted/_AI_Inbox/` + `addWorkItem`
- GA-owned GPT-layer architecture or reconciliation packet -> `/Users/ted/GPT_Architect/Reconciliations/` (GA writes its own; CC or Codex deliver companion-change packets to `_AI_Inbox/` or `Codex_Inbox/` for out-of-scope work per Plan §3.G)
- Mid-stream briefing to GA -> `/Users/ted/GPT_Architect/Briefings/` (CC or Ted writes; GA reads at session start)
- If ownership is already settled on the active surface and Ted wants direct implementation, inbox intake may be skipped

2. Identify the resurfacing surfaces.
Ask what should see this later:
- System database (queryable via API — always reachable)
- `Planning/Seeds.md`
- Coordinator manifest files
- Learning System concept files
- planning packets or indexes
- other established local surfaces

3. Route locally before mirroring.
Update the authoritative local file first. Only after local placement is correct should mirrors or export copies refresh.

4. Preserve source-vs-mirror distinction.
Call out when a copy is:
- live local source
- AI-visible manifest mirror
- iCloud export / backup mirror
- reference copy only

5. Verify visibility.
Check whether the relevant resurfacing surfaces now include the update. If accumulation should advance, verify that too.

6. Stop before promotion.
Do not silently promote observations into Canon or doctrine. Routing into visible surfaces is not the same as approval.

7. Clean the source surface.
After successful placement, check whether the source surface should be cleared:
- Seed absorbed into a Planning doc → remove from Seeds.md
- _AI_Inbox item evaluated and decided → clear the file
- Coordinator/Inbox/ signal integrated into continuity → remove when fully consumed
- TODO completed or superseded → remove per TODO lifecycle process
- GA briefing consumed by GA (evidenced by ACTIVE_INDEX update or reconciliation packet emission referencing it) → clear or move briefing out of `GPT_Architect/Briefings/`

Routing is not just placement — it includes clearing what material came from. A surface that only accumulates and never clears becomes noise. Stale items on active surfaces are a poka-yoke failure: AIs may act on information that was current when captured but has since been superseded. Cleanup keeps surfaces honest.

Not every routing action triggers cleanup. Cleanup applies when material has definitively moved — not when it was copied, mirrored, or is still under evaluation.

## Common Surfaces

**Database (structured state — primary):**
- `signal_evidence` table — accepted evidence units with tags and destination
- `concept_bridges` table — local term → standard concept mappings
- `work_items` table — proposals, tasks, notes with state tracking across all inboxes

**File surfaces (deep content):**
- `/Users/ted/Codex_Inbox/` for Codex-owned proposal-packet intake and session-start pickup
- `/Users/ted/_AI_Inbox/` for Claude Code-owned, Canon-affecting, or cross-system proposal-packet intake
- `Learning_System/concepts/` for preserved method observations
- `Planning/Seeds.md` for resurfacing emerging ideas
- `Planning/PLANNING_INDEX.md` when a new planning artifact should become visible
- `Manifests/Coordinator/` and related manifest mirrors for Coordinator-visible copies

**Deprecated as primary query surface (still human-readable archive):**
- `Operations/ACCUMULATION_STATUS.md` — use `getLaneStats` and `getSignalClusters` instead
- `Planning/Signal_Evidence_Log.md` — use `getSignalEvidence` instead

Use existing surfaces whenever possible. Prefer fitting the observation into the current system over inventing a new tracker.

## Output Shape

- `Authoritative local home`
- `Resurfacing surfaces`
- `Mirror status`
- `What was updated`
- `What now becomes visible`
- `What was cleared` (if source surface cleanup applies)

Keep the response short and operational.

## Never Assume

- Do not treat iCloud or other mirrors as the live source of truth.
- Do not invent a new storage location if an existing surface already works.
- Do not confuse preservation with Canon readiness.
- Do not update mirrors first.
- Do not assume every observation deserves Seeds, accumulation, and planning placement all at once.
- Do not leave the update half-routed if the user asked for durable placement.
- Do not skip inbox intake for proposal packets when inbox is the established pickup surface.
- Do not route by packet type alone when intended owner is already clear.

## Scripts vs. Skill

Use this skill for judgment-heavy routing and visibility placement.

Use scripts only when:
- a stable mirror or sync already exists
- deterministic refresh is needed after local placement
- repeated validation of visibility surfaces becomes mechanical

Keep the skill narrow. Its value is routing judgment, not building another governance layer.

## Watch Status

Monitor since 2026-04-25. The artifact-creation checkpoint may trigger routing too early on small or local outputs that aren't ready for broader placement.

Revise if: the skill encourages routing immature or purely local artifacts onto resurfacing surfaces before they've proven durable. Keep if: it catches genuinely under-routed artifacts that would otherwise have been missed.

## Update-Surfacing Backstop

This skill references live API endpoints and names specific surfaces as deprecated or primary. If any of the following drift:

- Endpoint routes (`/api/signal-evidence`, `/api/concept-bridges`, `/api/work-items`, `/api/work-items/state`) are renamed, their payload shapes change, or new structured-state endpoints are added
- A surface listed as "Deprecated as primary query surface" is reinstated, or a current primary surface is deprecated
- A new owner is added to the active-team role map (Canon Section 12 additions, new GPT role registration)

Do not silently route to the old destination or skip the structured-state write. Instead:

- Check `Control/backend/app.py` for current routes and payload fields
- Check `Operations/CHANGES_LOG.md` for recent routing-related changes
- Check `Canon/AI_Coordination/Active_Team_Agreements.md` for new owner registrations
- Surface the mismatch to Ted and propose a SKILL.md correction in the same turn
