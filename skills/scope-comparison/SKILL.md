---
name: scope-comparison
description: Before committing to scope on any non-trivial response or build, write the explicit comparison surface (Asked / Proposing / Gap / Gap-reason) and shape-check the gap-reason against known curtailment shapes. Use when Ted's prompt contains scope-implying language (action verbs, scope-totality framings, named-work references) or when sizing a response/build at decision points. Do not use for purely conversational answers, single-line bug fixes, or tasks where scope is unambiguous from the ask. The full protocol lives at `_shared/Scope_Comparison_Protocol.md`; this skill is the entry point.
category: judgment-only
write_mode: none
one_line_use: write the comparison surface before committing scope
fast_pick: "yes"
---

# Scope Comparison

Catch curtailment at the moment of scope selection by making the selection explicit.

This skill exists because CC repeatedly defaults to smaller-than-asked scope at the moment of selection, and the selection happens inside CC's reasoning where no hook can intercept. Writing the comparison surface forces the selection to be inspectable before commit — turns an invisible decision into a visible one.

Full doctrine: **`_shared/Scope_Comparison_Protocol.md`**. Read that for the shape catalog, the dial, the failure-mode examples, and the connection notes. This skill is the trigger card.

## When to Fire

Fire when:

- The userprompt_scope_size_recognition hook injects the protocol reminder (catalog at `~/.claude/hooks/scope_recognition_phrases.txt`)
- Ted's prompt contains scope-implying language: action verbs ("let's build," "wire up," "implement"), scope-totality framings ("full sweep," "across the fleet," "all 8 GPTs"), named-work references ("Hermes," "Builder pass," "curtailment-detection"), ask-strength signals ("I need it," "enough")
- You are sizing a non-trivial response or build at a decision point
- You notice yourself reaching for a "small," "minimal," "viable," "POC," or "first version" framing — that reach IS the trigger

Do not fire for:

- Purely conversational answers (yes/no questions, clarifications, factual lookups)
- Single-line bug fixes where the scope is the bug itself
- Tasks where the ask is one specific deliverable with no ambiguity about how much to build

## The Protocol

Write the comparison surface explicitly:

```
Asked:        <restate Ted's ask in his terms>
Proposing:    <my scope, concretely>
Gap:          <difference, or "none">
Gap-reason:   <why, if there is a gap>
```

Then shape-check the gap-reason against known shapes (see `_shared/Scope_Comparison_Protocol.md` for the full list with examples):

| Gap-reason matches | Shape | Action |
|---|---|---|
| "keep it simple," minimal-viable framing, "MVP," "viable version," "iterate from thin" | Shape 1 (size-framing) | Revise upward to enough |
| "X isn't verified yet," "no URL exists," "we don't have Y" | Shape 2 (unverified-prereq) | Build the missing piece, don't defer |
| "to fit the limit," "trim to make it work" | Shape 3 (trim-in-place) | Refactor to a more appropriate surface |
| "writing a plan for the rest," "Planning doc for the other items" | Shape 4 (planning-doc-substitution) | Execute the asked-for full sweep |
| "Ted should decide," "let me know which option" | Shape 5 (defer-to-Ted) | Determine from context; recommend directly |
| "I'll come back to that," "I'll flag that" | Shape 6 (empty-flag) | Do it now or commit it to a tracked todo |
| "first A, then B later" without exit condition for B | Shape 7 (sequencing-as-deferral) | Either name B's exit condition explicitly or do B inline |
| "let me prove the small case first," "validate before extending" | Shape 8 (test-the-piece-before-the-whole) | Build enough; test the relevant whole path |
| "want me to do all 6 or just the 3 highest signal" | Shape 9 (permission-fishing for smaller version) | Don't re-offer smaller when the ask was specific |
| "we can generalize later," "hardcode for now" | Shape 10 (architecture-bound to single-instance) | Parameterize when same cost as hardcoding; avoid preventable rework |

If gap-reason matches a known shape, revise scope upward to enough before responding.

If gap-reason produces under-scope but doesn't match a known shape, you have found a new shape — name it and add to `_shared/Scope_Comparison_Protocol.md` § "Known shapes" same-turn.

## Satisfying the artifact-side hook (durable writes)

`check_scope_comparison_surface.py` blocks durable writes (Planning/, _shared/, Canon/, proposals, calibration, briefings, reports) until a valid surface exists. As of 2026-05-30 it reads a **turn-scoped window** (current + previous turn) **or** a **session sentinel** — so stating the surface once in a turn clears every later write that turn. **No "go"-dance:** do not insert filler replies between markers and writes. For a same-message first write with no prior surface that turn, either do the write as your next step (a later message — no user reply needed), or write the surface to `Operations/state/scope_surface_declared.md` first (clears it synchronously, even in one message). Mechanism detail: `_shared/Scope_Comparison_Protocol.md` § "Satisfying the artifact-side check".

## The Dial

| Sizing | Meaning |
|---|---|
| Minimal | Absolute least; literal answer; leaves Ted with partial work |
| **Enough** | Fully serves the named need end-to-end; enough is not minimal and does not trap the system in its first version |
| Comprehensive | Pre-built scaffolding Ted didn't ask for |

Enough means the work can emerge at step one: usable for the current need, with the obvious connecting pieces handled, and enough breathing room that the next cycle is use/growth rather than escape from a too-tight first form. Do not shrink to minimal, and do not add speculative scaffolding just to prove ambition.

Reference: `~/.claude/projects/-Users-ted/memory/feedback_default_to_enough_and_room_to_grow.md`

## False-Positive Handling

If the hook fired on incidental usage (quoting prior discussion, describing past events, hypothetical reasoning, narrating someone else's decision) and there's no scope decision in this turn:

- Acknowledge the FP briefly in your response
- Note it in `Operations/Calibration_Scope_Size_Recognition.md` so the catalog can be tuned
- Proceed with the substantive answer

## Catalog Growth Discipline

When Ted names a new scope-implying shape (in chat, temp.md, post-mortem):

- Add the shape to `_shared/Scope_Comparison_Protocol.md` § "Known shapes"
- Add the literal trigger phrase(s) to `~/.claude/hooks/scope_recognition_phrases.txt` under the `[TI <date>]` section
- Do this same-turn — `feedback_default_to_enough_and_room_to_grow.md` makes the standing rule explicit

## Anti-Patterns

- **Minimal-viable first-pass framing** — Shape 1, common surface vocabulary. Revise to enough.
- **"I'll do A and B now, and write a Planning doc for C, D, E"** — Shape 4. Execute the full sweep.
- **"To fit the 8000-char Instructions cap, I'll trim some doctrine"** — Shape 3. Refactor doctrine to Knowledge files. See `_shared/Kernel_Instructions_Pattern.md`.
- **"I'll flag that for next session"** — Shape 6. Either do it or write the TODO with explicit exit condition.
- **"Would you prefer A or B?"** when the right answer is determinable from loaded context — Shape 5. Recommend directly.
- **"Let me start with a POC and we can iterate"** — Shape 1 (engineering-discipline variant). Build to enough.
- **"Let me get A landed, then we can add B in a follow-up"** without B's exit condition — Shape 7 (sequencing-as-deferral). Either name what triggers B's resumption, or do B inline.
- **"Prove the path before generalizing,"** "smoke test before extending" — Shape 8 (test-the-piece-before-the-whole). The small case becomes a permanent micro-instance; build enough from the start.
- **"Or want me to just do the highest-signal ones?"** when the ask was specific — Shape 9 (permission-fishing). Don't re-offer the smaller version.
- **"We can parameterize later"** when parameterizing is same cost as hardcoding — Shape 10 (architecture-bound to single-instance). Build the parameter.

## Connection Notes

- `_shared/Scope_Comparison_Protocol.md` — foundational doctrine (the body this skill points at)
- `~/.claude/hooks/userprompt_scope_size_recognition.py` — UserPromptSubmit hook that surfaces this skill via catalog match
- `~/.claude/hooks/scope_recognition_phrases.txt` — trigger catalog
- `Operations/Calibration_Scope_Size_Recognition.md` — calibration ledger (promotion gate ≥3 TP + ≤1 FP / 30d)
- `~/.claude/projects/-Users-ted/memory/feedback_default_to_enough_and_room_to_grow.md` — the dial discipline
- `~/.claude/projects/-Users-ted/memory/user_engage_at_capacity_not_protective.md` — objective-level recalibration framing
- `~/.claude/hooks/stop_detect_curtailment_output.py` — downstream backstop (chat-output boundary)
- `~/.claude/hooks/output_pattern_intercept.py` — downstream backstop (file-write boundary)
- `CLAUDE.md` Anti-Curtailment Notice — binding doctrine
