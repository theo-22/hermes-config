---
name: share-learning
description: Save a reusable pattern, technique, repeated correction, or operational finding to _shared/ so all substrate actors can benefit from it. Use when a pattern has been established through repeated use, when Ted has had to re-explain or re-correct the same behavior, when CC output contains "pattern is established for future", "the pattern for X", "worth saving to _shared", or when Ted says "save to _shared", "make this a pattern", "should this be in _shared", "add to shared". Writes to _shared/ and updates _shared/README.md; updates SKILL_INDEX.md only when a real shared skill is added or its index wording changes.
category: knowledge-capture
write_mode: shared
one_line_use: capture a reusable pattern or technique to _shared/
fast_pick: "yes"
---

# Share Learning

Save a reusable pattern to `_shared/` so it's available to all substrate actors — CC, Codex, GA, and any GPT with bridge read access to `_shared/`.

## When to fire

**Proactively** — without waiting to be invoked — when:
- CC's output contains pattern-establishment language: "pattern is established for future", "pattern is now X", "the pattern for", "worth saving to _shared", "reusable pattern"
- A session produced a technique that was used successfully and is clearly applicable elsewhere
- Ted has had to make the same correction more than once, especially around scope, terminology, proof, authority, routing, closeout, or over-cautious "safe" behavior
- Ted says any variant of: "save this to _shared", "make this a pattern", "should this be a skill", "all should know this"

**On demand** via `/share-learning` anytime Ted wants to capture something.

## Inputs that matter

Before writing, identify:
1. **Pattern name** — slug form for the filename, human-readable for the heading
2. **What it solves** — the problem or situation it addresses
3. **The technique** — the concrete steps or decision logic
4. **Confirmed instances** — how many times has this been used? Even one is enough to start.
5. **Promotion target** — what evidence would make this Canon-ready?

For repeated-correction captures, also identify:
- **Correction sentence** — the behavior Ted had to correct, stated in one sentence
- **Reusable trigger** — the future condition that should make an agent apply the correction without Ted repeating it
- **Best owner surface** — existing skill, `_shared` doc, Project Room, MRS slice, Reference note, or explicit rejection with upkeep rationale

## Workflow

1. **Check for duplicates** — scan `_shared/` filenames and README for similar patterns. If a close match exists, propose updating it instead of creating a new file.

   If the input is a repeated correction, first check whether an existing skill can absorb the correction as a trigger, boundary, evidence standard, or failure mode. Prefer patching the existing owner over creating a parallel skill.

2. **Write the pattern file** to `_shared/<PatternName>.md`:
   - Frontmatter: name, created date, status (Pre-Canon), instance count
   - Sections: What this is / When to apply / The pattern (concrete steps) / What it does not cover
   - Keep it practical — a reader should be able to apply it on the next decision

3. **Add to `_shared/README.md`** — one row in the Current Contents table: file, status, confirmed instances, promotion target.

4. **Update `SKILL_INDEX.md` only for actual shared-skill index changes.** Ordinary `_shared/` pattern capture does not update the shared skills index. Touch the index only when the capture also creates an accepted shared skill, changes an existing shared skill's name/metadata/quick-picker wording, or otherwise changes what `skills-card-check` should expose.

5. **Log to CHANGES_LOG** — one line noting what was captured and why.

6. **Fleet broadcast** — after writing, call `POST /api/broadcast` to notify applicable actor inboxes:
   - `destinations`: `["GA", "Coordinator_Inbox", "Codex_Inbox"]` by default (doctrine-level broadcast)
   - `title`: `"New _shared/ pattern: <PatternName>"`
   - `kind`: `"handoff"`
   - `tags`: `["fleet-broadcast", "share-learning"]`
   - `content`: 3–5 line brief — pattern name, one-sentence summary, link to `_shared/<PatternName>.md`, action line
   - `author`: your actor name (e.g. "Claude Code")
   - `filename`: `Fleet_Broadcast_<PatternName>.md`
   - If Ted said "I want all to know" or similar: use `destinations: "all"`

## Guardrails

- Do not create a _shared doc for something project-specific (CoCM, Image Factory, etc.) — those belong in the project directory.
- Do not create a _shared doc for something already in Canon — link to Canon instead.
- Do not create a _shared doc from a single session that hasn't been applied — note it as a seed unless Ted explicitly asks to write it now.
- One pattern per file. Do not bundle unrelated techniques.
- Do not preserve whole correction transcripts as the reusable artifact. Extract the behavior, trigger, and procedure; route the source transcript separately as Reference if it still needs to be kept.

## Fleet visibility

`_shared/` is readable by:
- **CC**: direct filesystem read
- **Codex**: direct filesystem read
- **GA and other GPTs with bridge access**: via `ga_read_file` or equivalent read action pointed at `_shared/`

When writing a new _shared doc, consider whether the pattern is immediately actionable for Codex or another AI — if so, note it in the file or drop a message to the relevant inbox.
