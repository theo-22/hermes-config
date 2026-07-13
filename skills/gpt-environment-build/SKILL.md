---
name: gpt-environment-build
description: Build or repair the full environment around a ChatGPT Custom GPT when the work spans instructions, knowledge files, action schema, backend or proxy alignment, Builder updates, and live verification. Use when the work starts sounding like "the GPT is close but still fighting us," "the action exists but fails in live use," "should we re-import the schema or update Builder?," or "this works locally but not through the proxy," and the capability must be carried through from runtime to Builder and proven end to end. Do not use for isolated instruction trimming, pure proposal writing, or routine routing.
category: gpt
write_mode: file
one_line_use: build or repair the whole Custom GPT environment
fast_pick: "yes"
---

# GPT Environment Build

Make the GPT actually work, not just look configured.

Use this skill when the problem is multi-layered:
- instructions
- knowledge files
- action schema
- backend routes
- MCP/proxy registration
- Builder state
- live verification

Read these shared references first:
- [/Users/ted/_shared/GPT_Build_Patterns.md](/Users/ted/_shared/GPT_Build_Patterns.md)
- [/Users/ted/_shared/GPT_Session_Playbooks.md](/Users/ted/_shared/GPT_Session_Playbooks.md)

Treat those files as the running doctrine for known Builder limits, route/proxy failure modes, and repeatable session methods.

Concrete trigger phrases to notice:
- "The GPT is close but still fighting us."
- "The action exists but fails in live use."
- "Should we re-import the schema or update Builder?"
- "This works locally but not through the proxy."
- "We fixed the code, but the GPT still cannot actually do the task."

## When to Use

- A GPT is mostly built, but real use keeps exposing friction
- A new capability exists in code or schema, but the GPT still cannot use it reliably
- A workflow spans more than one layer and "just update the instructions" is not enough
- An action is visible in Builder but fails in live GPT use
- A GPT needs a real environment loop: desired workflow -> capability gap -> bridge change -> live retest

Do not use when:
- the job is only to shorten instructions under hard limits — use `gpt-instructions-discipline`
- the job is only to write a proposal packet — use `proposal-packet`
- the main question is where a finished artifact should live — use `surface-routing`

## Core Workflow

1. Define the desired workflow.
Do not start from the current limitation. Name the workflow Ted actually wants.

2. Inspect the current environment.
Check the active surfaces:
- instructions
- knowledge files
- schema
- backend routes
- proxy/MCP routes
- continuity/state surfaces

3. Let the GPT try the real task.
Prefer live use over hypothetical reasoning. Real friction is better evidence than imagined gaps.

4. Ask the GPT what it needs, when useful.
Use direct self-assessment prompts when the GPT is already in the workflow and can name its own missing affordances.

5. Patch the actual blocker with contained scope.
Fix the live path before debating abstractions. Prioritize active blockers over cleanup philosophy.

6. Verify in layers.
For new or repaired actions, verify separately:
- local backend
- remote/proxy path
- fresh GPT chat with raw tool results

7. Refresh Builder only where needed.
If the schema changed, re-import the schema.
If instructions changed, re-paste instructions.
If knowledge files changed, refresh the Builder knowledge set from the authoritative local source.

8. Save continuity and carry forward the lesson.
When a new pattern proves durable, add it to the shared build/process docs so the next GPT starts from the better standard.

## Verification Rules

### One question at a time

If auditing GPT coherence, use a one-question ladder:
- ask one question
- inspect the answer against live sources
- ask only the next missing or highest-risk follow-up

Do not overload Builder chat with long checklists unless there is a specific reason.

### Raw-results prompt for stale chats

If a GPT keeps repeating old diagnoses after fixes, use a fresh chat and say:

`Do not summarize prior continuity. Execute these tools now and report only raw results.`

This distinguishes stale chat memory from real live failure.

### Read-only capability probe

For new action surfaces, use a read-only probe before trusting them in normal work:
- read continuity first
- test the exact actions in order
- forbid rename/move/archive/overwrite/import/generation unless explicitly allowed
- summarize what worked, what failed, and what remains blocked

## Builder and Bridge Patterns

- Keep a full schema and a Builder-safe schema when Builder limits force trimming
- Treat "schema visible" and "route mounted" as different questions
- New backend routes must also be registered in the proxy/MCP surface
- GPT-facing preview/image actions should prefer structured JSON over raw binary responses when transport reliability matters
- `saved: true` is not enough for overwrite/import validation; prefer before/after evidence and hashes when available

## Output Shape

- `Desired workflow`
- `Current blocker`
- `Layer`
- `Smallest fix`
- `Verification`
- `Builder updates needed`
- `Carry-forward lesson`

Keep the response operational. This skill is for getting the environment into working shape, not for producing a long architecture memo unless Ted asks.

## Never Assume

- Do not assume the current manual workflow is acceptable just because it has existed for a long time
- Do not assume Builder visibility means the action is actually usable
- Do not assume localhost success proves the GPT path is fixed
- Do not assume a contaminated chat is a trustworthy verifier
- Do not assume `saved: true` means the content changed
- Do not jump to cleanup philosophy before the active path works
- Do not treat the GPT's self-report as truth without checking the live surfaces

## Boundary With Nearby Skills

- `gpt-instructions-discipline` — use when the main job is instruction or action-description trimming under hard limits
- `proposal-candidate-surfacing` — use when the question is whether today’s learning has crossed into proposal territory
- `proposal-packet` — use when the environment recommendation needs a durable handoff packet
- `surface-routing` — use when the main problem is where the resulting artifact, note, or packet should live
- `skills-review` — use when the question is whether this pattern belongs as a shared skill at all
- `poka-yoke` — use when the main question is how to structurally prevent recurring human cleanup or memory-dependent failure loops

## Scripts vs. Skill

Use this skill for judgment-heavy GPT environment work.

Do not add scripts unless a stable mechanical step emerges that is worth automating. The value here is cross-layer diagnosis, sequencing, and verification judgment.

## Update-Surfacing Backstop

This skill stays current when ChatGPT Builder, OpenAI Builder, or any other GPT-platform environment changes its configuration surface (Instructions field, Knowledge files, Actions schema, Conversation Starters, Capabilities toggles).

If live build or repair work exposes a platform component not named here, or shows that an existing component behaves differently than this skill assumes (for example Builder limits, knowledge-file behavior, or schema refresh behavior):

- check `/Users/ted/_shared/GPT_Build_Patterns.md`
- check `/Users/ted/_shared/GPT_Session_Playbooks.md`
- update this skill when the new behavior is durable enough to recur across more than one GPT session

`skills-review` is the periodic backstop. Per-use drift during real GPT build work is the main one.
