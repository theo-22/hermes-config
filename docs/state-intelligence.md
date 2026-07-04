# State Intelligence: Files, Semantic Memory, and Temporal Continuity

A role-runtime system needs more than prompts. Actors entering a session need enough state to begin work without reconstructing months of history from scratch. This document describes the state-intelligence pattern used in this installation — a layered approach that separates readable authority, searchable memory, temporal continuity, and proof.

## The Problem

Without an intentional state layer, every AI session either:

- Starts with a blank context and asks the operator to re-explain the system
- Dumps a massive prompt with years of stale history
- Relies on chat memory that is not searchable, not verifiable, and not shared across actors

None of these scale to multi-actor, multi-session work.

## The Pattern: Three Layers, One Operator

```
┌─────────────────────────────────────────────┐
│             Human Operator                  │
│        (final authority, judgment)          │
├─────────────────────────────────────────────┤
│       Live Files / Project Homes            │
│  (readable authority, current state,        │
│   next actions, boundaries, receipts)       │
├─────────────────────────────────────────────┤
│        Semantic Memory Layer                │
│  (durable decisions, concepts,              │
│   retrieval hooks, landing notes)           │
├─────────────────────────────────────────────┤
│     Temporal Continuity Layer               │
│  (recent cross-actor context,               │
│   workstream traces, conversation trail)    │
├─────────────────────────────────────────────┤
│         Proof / Receipts                    │
│  (git commits, change logs, receipts)       │
└─────────────────────────────────────────────┘
```

These layers are **not interchangeable**. Each serves a different purpose.

### 1. Live Files / Project Homes (Authoritative Current State)

This is the source of truth for what is true *right now*.

- `CURRENT_STATE.md` — what is true, what is not yet true
- `NEXT_ACTION.md` — the next bounded thing to do
- `README.md` — purpose, ownership, boundaries
- `CHANGES_LOG.md` — cross-actor history of what changed and why

Actors read these surfaces at session start to orient. They do not replace chat history; they make chat history unnecessary for basic orientation.

### 2. Semantic Memory Layer (Findable Durability)

Not all useful knowledge fits in files. Decisions, reasoning, concepts, and recurring patterns need to be findable across sessions without digging through every file.

A semantic memory layer provides:

- **Targeted recall** — search by meaning, not filename
- **Durable ideas** — landing notes that survive session boundaries
- **Retrieval hooks** — pointers to the right file or surface
- **Cross-actor visibility** — any actor can find what another learned

This is not a replacement for live files. Files hold authority; memory holds findability.

### 3. Temporal Continuity Layer (Broder Context)

Some work requires understanding not just the current state, but the recent flow of work across actors and sessions. A temporal continuity layer captures:

- Recent cross-actor activity traces
- Broader conversation history when current files are not enough
- Ambient context that did not warrant a file but matters for coherence

This layer is the widest and least authoritative — it provides clues, not decisions.

### 4. Proof / Receipts

Git commits, receipts, and change logs provide verifiable evidence that work was actually done. Claims in chat are not proof. A commit hash or receipt timestamp is.

- `git log` for file history
- Receipts for session closeouts
- Change logs for cross-actor visibility

### 5. Human Operator

The human remains the final authority on judgment calls, boundary decisions, and anything involving taste, relationships, or protected surfaces.

## How It Works in Practice

A new actor entering the system does this:

```
1. Read current state from live files (Project Homes)
2. Search semantic memory for relevant decisions and concepts
3. Check temporal continuity for recent relevant context
4. Verify claims against live files, receipts, and git
5. Act within role boundaries
6. Record outcomes back to the appropriate layer
```

This is different from simple chat memory. It is **state intelligence** — the system surfaces enough context that work can begin without re-explanation.

## Plain Version

State is apparent, so work can begin.

## Adapting This Pattern

The implementation can vary. In this installation:

- **Live files** are organized into Project Homes with standard entry surfaces
- **Semantic memory** is provided through a searchable thought/knowledge store
- **Temporal continuity** uses a cross-actor activity index
- **Proof** comes from git history and structured receipts

Another installation could use different tools — a vector database for memory, a message log for continuity, a different VCS for proof — but the **pattern** stays the same:

> Combine authoritative current-state files with searchable memory and temporal continuity so cold actors can start useful work quickly.

## Privacy and Security Boundaries

- Live authority files are readable by all actors but writeable only within role bounds
- Semantic memory stores curated thought content, not raw data dumps
- Temporal continuity does not replicate protected content
- Git receipts are public by design; sensitive content stays out of public repos
- The human operator gates access to protected surfaces (financial, clinical, security)

## Why This Accelerates AI Work

Without state intelligence, every session costs re-orientation time. The operator explains the same context, the same decisions, the same boundaries — repeatedly. With it:

- Cold sessions start productive in minutes, not rounds of Q&A
- Decisions persist beyond the session that made them
- Multiple actors can work on related surfaces without stepping on each other
- The system gets more useful over time instead of starting over each session

This is the core architectural insight: **state intelligence is the difference between a chatbot that remembers nothing and a system that compounds knowledge.**
