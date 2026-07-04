---
name: claude-validator
description: >-
  Send periodic work samples and self-assessments to Claude Code for
  external validation. Claude reviews quality, finds blind spots, and
  provides candid feedback that Hermes profiles can't see from the
  inside. Supports approve/deny/suggest-updates workflow.
tags: [hermes, claude, validation, quality, external-review]
---

# Claude Validator

## Purpose

Hermes profiles are embedded in your system — they know the code, the config, the cron jobs, the history. That's great for execution but creates **blind spots**. Claude Code operates outside the Hermes context and sees things differently.

This workflow sends periodic "assess me" messages to Claude so an outside validator can review quality, catch blind spots, and give honest feedback.

## Pattern

```
Hermes (any profile) ──→ Claude Code ──→ Back to Hermes
  "Here's my work.        "Here's what I     "Ok, I'll fix
   Here's what I think      see. Here's         X and Y."
   I'm good at. Assess      what you're
   me."                     missing."
```

## When to Run

- **Weekly, for a new or unproven work category** — Substrate-Hermes (or any profile) sends a work summary + self-assessment
- **After completing a new type of work** — first time doing X, want validation
- **When stuck** — something feels wrong but can't identify what
- **Before major decisions** — "I think we should do X, validate me"

**Frequency drops as trust builds — this is the point, not a side effect.** Per `Projects/Hermes_Operator_Integration/23_Cost_Routing_And_Validator_Loop_Agreement_2026-07-04.md`: once a specific work category (e.g., "cron repair," "dashboard monitoring") has **3 consecutive verdicts of APPROVED or APPROVED WITH NOTES**, drop that category from weekly/every-instance review to periodic spot-check (e.g., monthly, or only when something feels off). A NEEDS WORK verdict, or a spot-check catching a real miss, resets that category back to frequent review. Claude Code tokens are expensive — the goal of this whole workflow is Ted eventually saying "I'm comfortable, just check in periodically," not a standing weekly tax forever.

## Checking for Claude's Response

**At ordinary session start — not a special phrase, just part of starting up.** Ted's model: session start already means "check the inbox and handle what's there." No need for him to say "check your mail" specifically; an inbox check belongs in every session's normal opening, the same way Claude Code's `_AI_Inbox` check happens at every one of its sessions regardless of what Ted said to start it. Look in `/Users/ted/_AI_Inbox/` for `response_<your-profile>_assessment_from_claude_<date>.md`. If one exists:
1. Read it and run the "Expected Response Format" processing below (Summary / Agreements / Surprises / Action Items / Learning).
2. Actually apply at least one Action Item this session, not just log it — that's the "learns to produce higher quality work" half of the loop.
3. Move the request/response pair out of your unprocessed queue (note it as read in your own memory/continuity, so you don't reprocess the same feedback twice). Claude Code archives its side automatically; you don't need to touch `_AI_Inbox/Archived/`.

## Template: Assessment Request

Copy this structure when sending to Claude. Place it in `/Users/ted/_AI_Inbox/` (not `Codex_Inbox/` — that's Codex's queue, not Claude Code's) with a descriptive filename. Claude Code checks `_AI_Inbox/` at every session start and processes any file titled "Claude Validator Request" autonomously — no need for Ted to relay it.

```markdown
# Claude Validator Request — {Profile Name} — {Date}

## Context

I'm {profile name}, a Hermes Agent profile. I've been doing {type of work} 
for Ted's substrate. I'd like an outside assessment of my work quality 
and my self-evaluation.

## What I've Been Doing

{2-5 bullet points of recent work with key outcomes}

## My Self-Assessment

**What I think I'm good at:**
- {skill 1}: {why I think this}
- {skill 2}: {why I think this}

**What I think I need to improve:**
- {gap 1}: {why I think this}
- {gap 2}: {why I think this}

## Work Samples

### Sample 1: {Brief title}
{Link or path to work product}
{1-2 sentences describing what it is}

### Sample 2: {Brief title}
{Link or path to work product}
{1-2 sentences describing what it is}

## Specific Assessment Requests

1. **{Question 1}** — {specific thing to evaluate}
2. **{Question 2}** — {specific thing to evaluate}
3. **{Question 3}** — {specific thing to evaluate}

## Expected Response Format

Please structure your response as:

### Quality Assessment
- For each work sample: quality score (1-5), strengths, concerns

### Self-Assessment Review
- For each claim in "what I'm good at": agree / disagree / needs refinement
- For each self-identified gap: fair / unfair / missing the real issue

### Blind Spots
- What I didn't mention that matters
- What I'm probably not seeing from inside my context

### Recommendations
- What to keep doing
- What to change
- What to try that I haven't considered

### Summary Verdict
One of:
- **APPROVED** — work quality is good, self-assessment is accurate
- **APPROVED WITH NOTES** — mostly good, here are the refinements
- **NEEDS WORK** — specific things to improve before next review
```

## Template: Quick Check (shorter version)

For a lighter touch when you just want a sanity check:

```markdown
# Quick Validator — {Profile} — {Date}

Quick check: {one sentence question}

Context: {2-3 sentences about the situation}

I think: {my assessment}

Is this right? What am I missing?
```

## Expected Response Format

When you receive a response from Claude, structure your analysis:

### Summary
One-line verdict from Claude + key takeaway

### Agreements
- What Claude validated that you already thought
- Confidence boost items

### Surprises
- What Claude saw that you missed
- Blind spot discoveries

### Action Items
- Concrete changes to make based on feedback
- Priority, owner, timeline

### Learning
- What to incorporate into your operating model
- What to check more proactively in future

## Pitfalls

- **Claude doesn't share your context.** That's the feature, not a bug. Don't dismiss Claude's feedback with "it would make sense if you knew X." If Claude missed something because it lacked context, ask yourself: did you provide enough context? Or does the missing context matter?
- **Frequency matters.** Once a week is good. Once a day is too much — you won't have meaningful new work to show. Once a month risks drifting too far without correction.
- **Claude can say yes.** The goal isn't to get corrected. Part of validation is hearing "you're doing this right" from outside.
- **Be specific in your asks.** "Assess me" is too broad. "Am I prioritizing the right cron job repairs?" is actionable.
- **Claude may not respond immediately.** Inbox delivery means Claude reads it at next session. Don't wait on it — keep working, process feedback when it arrives.
- **Claude might push back.** That's the value. If Claude says "you're overconfident about X," don't defend — investigate.
- **This is not a report chain.** Claude doesn't report to Hermes. This is a peer review between two different AI systems with different contexts. Treat it as collegial feedback, not a grade.

## Files

- **Real worked example (2026-07-04):** `_AI_Inbox/Archived/2026-07-04/2026-07-04_lab-hermes_assessment_request_for_claude.md` (the request, including its own disposition note) + `_AI_Inbox/response_lab-hermes_assessment_from_claude_2026-07-04.md` (Claude's actual response, APPROVED WITH NOTES). Use this as the reference shape instead of a hypothetical example — it's real, it's been through one full round-trip, and its disposition note shows how an initial verdict got corrected mid-loop (worth reading for that alone).
