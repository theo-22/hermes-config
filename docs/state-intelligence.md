# State Intelligence: Files, Semantic Memory, and Temporal Continuity

A role-runtime system needs more than prompts. Actors need enough state to begin work without reconstructing months of history.

In this installation, the state-intelligence pattern has three main layers:

- **Live files / Project Homes** hold readable authority: current state, next actions, boundaries, receipts, and durable docs.
- **Brain** provides semantic recall: durable ideas, decisions, and retrieval hooks that let actors find the right shelf quickly.
- **Pieces** provides temporal continuity: recent cross-actor context, workstream traces, and broader conversation history when the current files are not enough.

These are not interchangeable. Brain and Pieces do not replace live files; they help actors find and understand the right live state. Git and receipts provide proof of what actually changed. The human operator remains the final authority.

## What problem this solves

Every AI actor in the system starts cold — no chat history, no shared memory of what happened last session. Without state intelligence, an actor would need to re-read everything or ask the human to recap. With it, an actor can:

1. Read current state from files (authoritative, human-visible)
2. Search Brain for durable decisions and concepts (semantic recall)
3. Use Pieces for broader recent continuity when needed (temporal trail)
4. Verify claims against live files, receipts, and git (proof)
5. Act within role boundaries (clean handoff)

This is different from simple chat memory. It is state intelligence — designed so that cold actors can start useful work quickly.

## How the layers relate

| Layer | What it provides | When it's primary |
|-------|-----------------|-------------------|
| Files / Home docs | Readable authority, current state, next actions | Every session start — this is always the first read |
| Brain / semantic memory | Targeted recall, durable ideas, retrieval hooks | When an actor needs to find relevant context by meaning |
| Pieces / temporal continuity | Broader cross-actor context, workstream trail | When files and Brain aren't enough — recent activity across all actors |
| Receipts / git | Proof of what changed, audit trail | After any write — verify the change landed correctly |
| Dashboards | Visibility and navigation | When the human needs to see the system state at a glance |
| Human operator | Final authority, decisions, direction | When any layer is ambiguous or a boundary is crossed |

## Why this accelerates AI work

A state-intelligence system means:

- **No warm-up cost.** A role can start producing useful work on its first turn because the state it needs is findable, not latent in someone's chat history.
- **Cross-actor continuity.** An insight produced by one actor (e.g., a finance finding from ChatGPT) can be retrieved by a different actor (e.g., Hermes implementing the change) without the human relaying it by hand.
- **Verifiable claims.** Every assertion about what changed or what was decided can be checked against a live file, a Brain thought, a Pieces event, a git commit, or a receipt.
- **Clean boundaries.** Each layer has a defined job. Files don't try to be memory. Brain doesn't try to be temporal history. Dashboards don't try to be authoritative. This prevents the "everything pile" problem where a single surface becomes too broad to trust.

## How someone else could adapt this pattern

Brain and Pieces are the tools used in this installation. The reusable pattern is broader:

- **Authoritative current-state files** — Project Homes, any structured doc surface with CURRENT_STATE + NEXT_ACTION
- **Semantic memory** — Brain (Open Brain / OB1), any embedding-based retrieval system
- **Temporal continuity** — Pieces, any workstream capture tool that records cross-application activity

Another installation could substitute different tools for each layer. The pattern survives the tool swap.

## Privacy and security boundaries

- Brain stores only curated, durable thoughts — not raw conversation history
- Pieces captures workstream activity locally; no data leaves the machine
- Live files are plain markdown — human-readable, no special tooling required
- Secrets, credentials, and PHI are excluded from all state-intelligence surfaces by domain boundary
- The human operator is always the final authority — no layer acts autonomously on its own declared state without verification

## Plain version

State is apparent, so work can begin.
