---
name: opus-review-surfacing
description: Recognize when a real chunk of structural work has landed in a session, then proactively package it and dispatch an uncommitted Opus reviewer to find what the working session may have settled without real scrutiny — blind spots, premature actions, unverified claims presented as confirmed, tensions narrated as resolved rather than actually resolved. Use after a substantial, structurally real chunk of work (not busywork) and before continuing further or closing out. Do not use for a single contradiction check between a few documents — that's `contradiction-sweep`. Do not use for shaping an unclear proposal before it's built — that's `proposal-candidate-surfacing`. Do not use on trivial or purely mechanical work.
category: judgment-only
write_mode: none
one_line_use: uncommitted Opus pass finds what the session settled without scrutiny
fast_pick: "yes"
---

# Opus Review Surfacing

**The one claim:** a session that has been "inside" its own work for hours cannot reliably tell the difference between a tension it genuinely resolved and one it narrated as resolved. Both feel settled from inside. The miss is structural, same shape as `contradiction-sweep`'s — but this skill's scope is broader than contradictions between documents: it covers premature actions, claims taken on faith, and architecture conclusions the session may be defending rather than testing.

Named and requested by Ted, 2026-07-27, after watching the pattern work live: "This is good. This is how I need to do a lot of this. Assembling my never ending string of ideas. Packaging now and then and get our bearings." See `~/.claude/projects/-Users-ted/memory/user_assemble_then_package_and_get_bearings_rhythm.md` — this skill is the mechanical form of that named rhythm.

## When to use

- A real, structurally significant chunk of work has landed — new durable state (database writes, edited canonical nodes, a committed plan), not just conversation.
- The session has been running long enough that Sonnet may be defending earlier calls rather than re-examining them.
- Before continuing to build further on top of what just landed, or before closing a session out.
- Ted names the moment directly ("are we good, or should we get a second look"), or the shape matches without him naming it.

## When NOT to use

- The work is trivial, mechanical, or fully verified already (tests passed, live-checked against ground truth) — an Opus pass on already-proven work is theater, not scrutiny.
- A single contradiction check across a handful of documents — use `contradiction-sweep`, it's narrower and cheaper.
- Shaping an idea that isn't built yet — use `proposal-candidate-surfacing`.
- Every small step. This is for a real bearings-check, not a tic. Don't force it onto work that doesn't need it — matches the anti-over-routing principle in `Surface_Routing_Discipline.md`.

---

## Workflow

### 1. Detect the threshold

Look for the shape, don't wait to be told:
- A durable write happened (DB rows, a committed file, an edited canonical node) that other work will build on.
- The session is long and idea-dense — several distinct threads landed, not one clean task.
- Ted expresses uncertainty about the whole arc ("am I doing this well," "I don't know what works") — that's the live trigger moment, not a sign to just reassure him.

### 2. Package a bounded bundle — not the raw transcript

Name the specific files, database queries, and claims the reviewer needs to check. Point at exact paths and give exact SQL/lookup commands so the reviewer verifies live state itself rather than trusting a description of it. A raw session transcript dump is not a package — it's a burden. The bundling is the hard part; do it carefully.

### 3. Instruct the reviewer to find problems, not summarize

Explicit in the prompt: not praise, not a recap — specific claims to interrogate. Ask direct yes/no questions about the things most likely to have been smoothed over (a contradiction presented as resolved, an action taken on unverified secondhand information, an architecture conclusion that might have a real failure mode). Tell it explicitly: if something genuinely holds up, say so plainly — don't manufacture problems to look rigorous.

### 4. Surface the findings honestly to Ted

Report what came back without softening it. If the reviewer confirms everything holds, say that plainly too — this skill is a real check, not a ritual that always has to produce a finding.

---

## Relationship to sibling skills

- **`contradiction-sweep`** — narrower: one specific check (do these documents contradict each other), any uncommitted model, use before a close/handoff. This skill is broader (blind spots, premature actions, unverified claims, architecture conclusions) and specifically models a fuller session-arc review, typically Opus given the depth of judgment needed.
- **`proposal-candidate-surfacing`** — earlier in the pipeline (shape an idea before building), this skill is later (scrutinize what got built).
- **`lens-assembly-pass`** — assembles/wires/persists a topic into durable structure. This skill is what checks that structure afterward, once enough of it has accumulated to be worth a bearings-check.
