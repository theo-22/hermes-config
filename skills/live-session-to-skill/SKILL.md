---
name: live-session-to-skill
description: Build an automation from a live session — do the thing, learn, capture as a shared skill, improve plans, hand off buildout. Proven pattern from the Shopping Guru 2026-07-12 session.
category: meta
write_mode: file
one_line_use: capture a proven live-session automation pattern as a durable shared skill
fast_pick: "no"
version: 1.0.0
platforms: [all]
tags: [workflow, meta, skill-building, automation, human-in-the-loop]
---

# Live Session → Skill Pipeline

The process we used to build the Shopping Guru capability. Any actor can follow this to turn a live session into a durable, shareable automation.

## The Loop

### Phase 1: Do the Thing (Live Session)
Don't plan — **do it live with Ted.** Use the actual site, real data, real browser.

- Navigate together — Ted shows, you watch and extract
- Try things that might not work — learn the failure modes
- Let Ted drive the critical decisions (what to buy, what to skip)
- Capture what actually worked vs what didn't

### Phase 2: Extract the Patterns
After the live session, distill what you learned:

- **Working approaches** — "`?query=` works, `?keyword=` doesn't"
- **Pitfalls** — "store selector wall, React SPA click handling"
- **Timing** — "Wednesday price resets, Friday 4x fuel points"
- **Design constraints** — "human in the loop on checkout"

### Phase 3: Capture as a Shared Skill
Write a skill document at `/Users/ted/Skills/<name>/SKILL.md` that any actor can load:

- Prerequisites (CDP browser, Python deps, login state)
- Step-by-step navigation patterns
- Known failure modes and workarounds
- Code snippets for the tricky parts

Also keep a copy in the active profile's skills dir for cron job access.

### Phase 4: Improve Existing Plans
Cross-reference the new skill against existing planning documents:

- Update the Shopping Guru plan with real data (prices, thresholds, meal plan)
- Update any relevant System 14 chapters
- Add design constraints learned from the live session

### Phase 5: Hand Off Buildout
Write a handoff to `_AI_Inbox/` for Claude Code or other actors to build the infrastructure pieces that need deeper engineering:

- Item-level scrapers
- Cross-reference engines
- Persistent state management
- Integration with existing cron pipelines

## Design Principles

1. **Human in the loop** — The last click is always Ted's. Never auto-submit orders, payments, or critical actions.
2. **Learn by doing** — Real data and real sites reveal patterns you can't plan for.
3. **Share early** — Put skills in `/Users/ted/Skills/` so any actor (Hermes, Claude Code, Codex, ChatGPT) can pick them up.
4. **Cheap automation first** — `no_agent` scripts before agent crons. Free before paid.
5. **Evidence over planning** — A working example from a live session is worth more than a perfect plan.

## When to Use This

- Ted mentions "I want to build a tool for X"
- A live session reveals site patterns worth capturing
- A manual process that could be automated
- Any task that combines human judgment with mechanical automation
