---
name: gpt-instructions-discipline
description: Route GPT Builder content to the right home (Instructions vs Knowledge/overlay) and keep each within hard platform limits (8000 chars for Custom GPT Instructions, 300 chars for OpenAPI action descriptions). Use when adding any new behavior or section to a GPT, when content is near or over a limit, when claiming "preserved elsewhere" during a trim (the skill requires grep verification), or when OpenAPI action descriptions exceed the per-op cap. Routing comes first; trimming is the last resort. Do not use for schema architecture or ordinary prompt writing comfortably within budget.
category: gpt
write_mode: none
one_line_use: trim GPT instructions under hard platform limits
fast_pick: "yes"
---

# GPT Instructions Discipline

Keep GPT Builder content in the right home, then within hard platform limits.

This skill governs **two coupled decisions**:

1. *Where* should this content live — Instructions vs Knowledge/overlay vs local live-read vs MDPS package plane vs `_shared`?
2. *Does it fit* the hard limit of the home it belongs in?

Routing comes first. Trimming is the second-line response only when Instructions is the right home AND it's over budget. Most of the failures this skill addresses come from putting doctrine in Instructions and then having to trim it under pressure — fixing the routing eliminates the trim crisis.

## The homes

GPT artifacts split across several surfaces with very different constraints:

- **Builder Instructions** (`/Users/ted/Projects_GPT/<GPT>/<GPT>_Instructions.md`) — pasted into the GPT Builder's Instructions field. Hard cap: **8000 characters** for the full pasted file, including any manifest-stamped HTML frontmatter comment if that comment is pasted. Read on every turn. Holds: required reflexes, triggers, action-call sequences. The *what* — operational spine.

- **Knowledge files** (`<GPT>_Behavior_Overlay.md` plus Layer files, all bundled into `/Users/ted/Manifests/<GPT>/` by Sync_All and uploaded to the Knowledge panel) — effectively uncapped (~2 MB per file, 20 files per GPT). Read on demand or via session-start reflexes. Holds: doctrine, taxonomies, examples, rationale, citation discipline. The *how* — doctrinal context.

- **Local live-read files** (`_guidance/`, role context, domain files, workbench references, or other Action-readable local sources) — for material that should stay current and does not need to be copied into Builder Knowledge.

- **MDPS package planes** (`artisticlogistics.com` Baseline, `dawgdomains.com` Domain Worker, reserved `hughesenterprises.com` Builder/Maintainer, or another named domain plane) — for reusable capability that should not consume the GPT's primary 30-operation action budget.

- **`_shared/`** — for reusable doctrine and build lessons that apply beyond one GPT. Check it before restating a pattern; contribute back when a session surfaces a reusable lesson.

OpenAPI action descriptions have their own hard cap: **300 characters** per operation `description`.

## Workflow — routing first, trimming last

### Step 1 — Routing decision (always first, before any edit)

Before adding ANY content to a `*_Instructions.md` file, classify what you're about to write:

**Belongs in Instructions:**
- Trigger condition (when to do something)
- Action-call sequence (which Action, in what order)
- Required reflex (must always happen on X)
- Session-start trigger/reporting reflex (short; details elsewhere)
- Operational menu (the visible action surface)
- Safety boundary
- Scope rule (what this GPT does/doesn't do)

**Belongs in overlay/Knowledge:**
- Doctrine (why we do something this way)
- Taxonomy (categorization scheme — source classes, value tiers, evidence levels)
- Worked example / format demo
- Rationale / motivation / background
- Verification workflow (multi-step check process with prose)
- Detailed citation discipline
- Mode behavior or longer runtime method that must be available to the GPT
- Detailed session-start checklist or reporting template

If the content being added is taxonomy/doctrine/example/rationale, **do not put it in Instructions**. Put it in the GPT's overlay file (e.g. `Clinical_Behavior_Overlay.md`) and have Instructions reference the overlay section by name in one short line.

The signal that something is overlay-bound: it explains WHY or HOW, gives EXAMPLES, or enumerates CATEGORIES. Instructions handles WHEN and WHAT.

**Belongs in local live-read or package surfaces:**
- Dynamic or frequently updated material
- Capability operations that recur across GPTs
- Domain-scoped filesystem work
- Shared civic operations: continuity, shared docs, work items, inbox, change log

Route reusable operations through MDPS package planes before cramming them into a GPT's primary schema. Domains are not scarce; semantic clarity is the gate.

**Belongs in `_shared/`:**
- A pattern, failure mode, diagnostic, or method that will help more than one GPT or assistant
- A repeated Ted reminder that can become reusable doctrine
- A generalized lesson from a GPT repair, audit, or Builder update

### Step 2 — Verification of preservation claims (before any cut)

If you are about to remove content from Instructions while claiming it's preserved elsewhere ("this is in the overlay" / "covered by X"), you must **grep to verify** before the cut lands. Paste the matching grep output as evidence in your reasoning.

This rule exists because unverified preservation claims have caused real losses. On 2026-04-30 the source-class taxonomy ("primary evidence / guideline / policy / implementation report / expert commentary / general web") was claimed-as-in-overlay during a trim, the overlay didn't actually have it, the cut shipped, and Ted had to call out the loss before walk-back. Multiple re-pastes followed. **Grep is cheap; walk-backs are expensive.**

### Step 3 — Budget check

Compute the current full pasted-file length and the post-edit projected length. Ted's current paste convention includes the HTML `<!-- ... -->` frontmatter stamped at the top, so count it.

The Claude PreToolUse hook (`/Users/ted/.claude/hooks/check_gpt_instructions_routing.py`) enforces this automatically for Claude edits. The shell/Codex-side guardrail (`/Users/ted/Operations/scripts/check_gpt_instruction_budgets.py`, included in `/Users/ted/Operations/scripts/check_gpt_builder_guardrails.py`) checks active instruction files outside Claude. Any edit path that would push the file over 8000 chars and increase length should be blocked or corrected before Builder paste. Edits that reduce length are always allowed (so trim work is never blocked even when the file is over).

The hook also surfaces the routing reminder on every Instructions edit. This is structural enforcement of Step 1 — the question can't be skipped.

### Step 4 — Trim only if Instructions is the right home

Trimming is the LAST resort, only invoked when:
- Step 1 confirmed the content genuinely belongs in Instructions
- The file is over the 8000-char limit
- Step 2 verification has been done for any preservation claims

When trimming Instructions:

- **Protect:** REQUIRED REFLEXES, action-call sequences, operationIds, trigger conditions, Safety sections, scope rules, the operational menu.
- **Cut first:** duplicate sections, redundant headers, historical notes (renames, deferred phases, legacy aliases), explanatory padding, repeated "before saying X, do Y" phrasing.
- **Cut next:** elaborated rationale and prose explanations — these almost always belong in the overlay (route them, don't drop them).
- **Cut last:** edge cases or examples (and only if Step 1 confirms they belong in overlay; route, don't drop).

For OpenAPI 300-char descriptions:

- **Preserve front:** what the operation does + when to call it.
- **Trim from end:** examples, soft qualifiers, taxonomies (these go in the GPT's Instructions or overlay where appropriate, not in the schema description).
- **Validate with character count BEFORE declaring done.** Common error: drafting a "trimmed" version, eyeballing it, and assuming it fits. Always measure.

## Output Shape

When this skill drives an edit, the response should include:

- **Routing decision** — for each piece of content being added or moved, one line stating where it belongs and why.
- **Verification** — for any cut claiming preservation, paste the grep output proving it.
- **Revised content** — with character count.
- **Cuts made** — one short line per cut and why it was safe.
- **Operator update** — per the GPT update format: Instructions path (if changed), Schema path (if changed), then "run Sync_All and upload the manifest." No verbose explanation.

Keep the output compact and operational.

## Never Assume

- Do not write doctrine, taxonomy, examples, or rationale into Instructions. Route to overlay first; that decision precedes any concern about character limits.
- Do not forget spillover. If a detail matters but does not fit Instructions, use Knowledge, local live-read, hosted/package surfaces, or `_shared`; do not reduce capability to fit the field.
- Do not skip `_shared` when the lesson is reusable. Read before duplicating and contribute after learning.
- Do not drop the session-start/reporting reflex to save characters. Keep the trigger in Instructions and move detail elsewhere.
- Do not claim content is preserved elsewhere without grepping to confirm.
- Do not declare a trim done without measuring the result against the limit.
- Do not paraphrase operationIds.
- Do not cut REQUIRED REFLEXES, Safety sections, or scope rules.
- Do not trim the front of an OpenAPI description before trimming the tail.
- Do not treat ordinary prompt polish as a reason to invoke this skill — only invoke when the routing decision or a hard limit is in play.

## Boundary With Nearby Skills

- `openapi-schema-build` — when designing new actions, validation flow, or overall schema structure. This skill handles description-text discipline and Instructions/Knowledge routing only.
- `gpt-environment-build` — when assembling a full GPT environment from scratch. This skill handles the routing/budget side of an existing GPT.
- `surface-routing` — when content isn't GPT-specific.

## Update-Surfacing Backstop

If platform limits change (currently: 8000 chars for ChatGPT Custom GPT Instructions; 300 chars for OpenAPI action descriptions), verify against live platform behavior and update this skill in the same pass. The Claude PreToolUse hook (`/Users/ted/.claude/hooks/check_gpt_instructions_routing.py`) and the shell/Codex budget checker (`/Users/ted/Operations/scripts/check_gpt_instruction_budgets.py`) hard-code the 8000 limit — update all three together so they don't drift.

If a new GPT-related instruction-bearing surface appears (e.g., a new system-context layer file), add it to "The two homes" section.

Per-use limit mismatch is the main backstop. `skills-review` periodic pass is the secondary.
