---
name: persist
description: Write concept work to the three durable surfaces — Brain, memory file, and a buoyancy touch — so an idea developed in conversation survives the session that produced it. Use as the never-skipped closing step of any concept-map assembly, node minting, edge wiring, or synthesis pass, and any time a session produced understanding that is not yet on disk. Do not use for routine file edits already saved, or as a substitute for quick-save/session-end (those close a session; this closes an idea).
category: database-integrated
write_mode: db
one_line_use: write concept work to Brain, memory, and a touch
fast_pick: "yes"
---

# Persist

Write the idea down, in all three places, before the session ends.

**The one claim:** work that exists only in a conversation is not externalized. It feels finished — the understanding is live, the reasoning is fresh, the AI can still restate it — and that feeling is exactly why it gets skipped. The next session inherits nothing. Persist is the step that converts *having understood* into *the system knowing*.

This is the closing andon of [lens-assembly-pass]. It is also callable on its own.

## The three surfaces — all three, not a choice

Each one answers a different question later. Skipping one leaves a real hole.

1. **Brain** (`capture_thought`, open-brain) — *semantic recall.* Answers "have we thought about this before?" when a future session searches by meaning rather than by filename. Without it, the idea is unfindable unless someone already knows it exists.
2. **Memory file** (`~/.claude/projects/-Users-ted/memory/<slug>.md` + a one-line pointer in `MEMORY.md`) — *automatic re-entry.* `MEMORY.md` auto-loads every session, so this is the only surface that reaches a cold session without anyone querying for it. Without it, the idea waits to be asked for.
3. **Buoyancy touch** (`/Users/ted/Control/backend/scripts/add_touch.py`) — *the trend signal.* Records that the concept was worked, so recurrence becomes visible over time. Without it, the fact that a topic keeps coming back stays invisible.

Node and edge writes in the concept map do **not** count as persist. They are the *artifact*; this is the *record that it happened and why*.

## Canonical workflow

1. **Name the one claim.** One sentence: what is now true that was not true before this pass. If it can't be written in a sentence, the work isn't finished — go back, don't persist a fog.
2. **Brain.** `capture_thought` with the claim, the reasoning that earned it, and the node ids / file paths it touches. Write for a reader who has none of this conversation.
3. **Memory file.** One fact per file, standard frontmatter (`name`, `description`, `metadata.type`). Link related memories with `[[slug]]` liberally. **Then add the one-line pointer to `MEMORY.md`** — a memory file with no index line is invisible to a cold session, which defeats the surface's whole purpose.
4. **Touch.** `add_touch.py <surface_path> <surface_class> <touch_type> --actor claude_code --concept-key <key> --why "..."`. Use a stable `concept-key` so repeat work on the same concept accumulates rather than scattering.
5. **State what you wrote.** Name the three surfaces and what landed on each. An unverified "persisted" claim is the failure this skill exists to prevent.

## Evidence / success criteria

- All three surfaces written, each named explicitly in the response.
- The memory file has its `MEMORY.md` pointer line — verified, not assumed.
- A cold reader could reconstruct the claim and its reasoning from the Brain capture alone, with no access to this conversation.
- The touch carries a `concept-key` that matches prior work on the same concept.

## Failure modes

- **The "it's already in the map" skip.** Nodes and edges are the artifact, not the record. The map shows *what* connects; it does not carry why this pass happened or what was decided. Both are needed.
- **Memory file with no index line.** The most common silent failure. The file exists, nothing loads it, and the next session re-derives from scratch — the exact cost this whole practice exists to eliminate.
- **Persisting a fog.** Writing three surfaces about work that never resolved to a claim. Produces the appearance of continuity with none of the substance. If step 1 won't write, stop.
- **End-of-session token pressure.** This step is the one that gets dropped when budget runs short, precisely because the understanding still feels present. Treat it as the andon: it does not yield to remaining tokens. **If budget is genuinely short, persist first and cut depth elsewhere.**
- **Duplicating instead of updating.** Check for an existing memory file covering the same fact; update it rather than forking a second version that will drift.

## Runtime Notes

### Claude Code
- Brain: `mcp__open-brain__capture_thought`. Local read path per Ted's 2026-07-18 call.
- Memory: write the file, then edit `MEMORY.md`. Both are plain files.
- Touch: `python3 /Users/ted/Control/backend/scripts/add_touch.py …` (exit 0 = success, 2 = validation error). Speaks to `system_db` directly, no HTTP.

### GPT bridge
No direct write. Route the three payloads (Brain capture, memory file content, touch parameters) to `_AI_Inbox/` for an actor with write access to land.

## Update-surfacing backstop
Names live paths (`add_touch.py`, the memory directory, `MEMORY.md`) and the open-brain tool name. If any drift, fix here or leave a review note.
