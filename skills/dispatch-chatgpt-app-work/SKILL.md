---
name: dispatch-chatgpt-app-work
description: Start real work in a ChatGPT or Codex app session, have it drop a written report when done, and check back later instead of watching it live. Use when dispatching a bounded task to ChatGPT/Codex and moving on to other work — including running several dispatches in parallel. Do not use for a quick question that needs an immediate answer in the same turn, or for work that must be watched live for safety reasons.
metadata:
  category: dispatch
  write_mode: file
  one_line_use: fire-and-check-back dispatch to a ChatGPT app session
  fast_pick: "yes"
---

# Dispatch ChatGPT App Work

The point of this skill: start a task, have it write its own report to a file when finished, and come back for the report later. Never sit and watch a session work turn by turn — that defeats the purpose of running several at once.

## 0. Check token/usage availability FIRST

Before dispatching anything, confirm the target account actually has usage room:

- In the ChatGPT app or chatgpt.com, check Settings → Usage (or the "You're out of Codex/Work usage" banner if one is already showing).
- If usage is exhausted (a banner reading "You're out of Codex and Work usage, resets at [time]" appears on ANY thread), do not dispatch on that account — either wait for the reset, or switch to a different account that has room and confirm it actually has the connector/plugin you need installed (check its Plugins list — do not assume).
- This check applies per account, not per thread. One account being out of usage blocks every thread on it.

Skip this step and you will burn a whole dispatch cycle discovering the block only after wasting a turn.

## 1. Pick the right surface

Everything in this skill applies equally to ChatGPT and Codex sessions — same check-tokens-first, same report-and-check-back pattern. Pick whichever surface actually has room and the right access for the task (see [[feedback_prefer_chatgpt_app_sessions_parallel_dont_over_route_to_codex]] for when to prefer one over the other).

- **`chatgpt.com` as a website** → use the Chrome browser tool. Fine for anything that only needs the MCP connector (network access to Substrate's backend), not local files.
- **Native ChatGPT/Codex desktop app** → use computer-use tools. Required when the task needs direct local filesystem access (editing real files on disk) — the desktop app has this, the website does not.
- Check the desktop app's top-left mode dropdown (ChatGPT vs Codex) — it is a real functional switch, not a label. Pick the one actually intended.
- A separate real Codex cloud environment also exists (`chatgpt.com/codex/cloud`, GitHub-repo-based) with its own usage pool and its own Environments/Connectors settings — check which surface you're actually dispatching to, they are not interchangeable.

## 2. Start the session

1. New chat.
2. Attach the relevant plugin/connector (click `+` → Plugins → the connector name). Screenshot to confirm the tag actually shows in the composer before typing — a misplaced click can navigate to the connector's detail page instead of attaching it.
3. Write the task prompt. Long prompts (roughly 1000+ characters) can get interrupted mid-type if something steals window focus — send in 2-3 shorter chunks rather than one giant block if the task is long.

## 3. The task prompt MUST include a report instruction

Every dispatch prompt ends with something like:

> When done (or if blocked), write a short report to `<a real path you will check later>` covering: what was done, real evidence (commit hashes, file diffs, command output — not just a claim), and whether it's fully done, partially done, or blocked and why. Do not wait for me to ask — write the report as your last step.

Pick a real, findable path — e.g. `Operations/reports/Orchestration_Receipts/` for anything touching the shared system, or wherever fits the task's existing convention. Don't invent a new location per task.

## 4. Move on — don't watch

Once the prompt is sent and you've confirmed it started (one screenshot showing "Thinking" or a real first tool call), stop watching that thread. Either:
- Start the next dispatch (repeat from step 0 for a different account/task), or
- Schedule a check-back (10+ minutes for real multi-step work) instead of polling every few seconds.

**Concurrency:** one or two dispatches at a time is the safe default. Ted sometimes runs 5-8, but that's an experienced-operator pattern — a cheaper/simpler agent following this skill should stick to one or two until it has a track record of reading reports correctly.

## 5. Checking back

- Read the report file directly rather than reopening the chat thread and re-reading its conversation — the whole point of step 3 was to make this a file read, not a conversation replay.
- **If the report file is not present when you check, go back to the actual chat thread and check conditions** — don't assume it's still working, don't assume it's fine, don't re-dispatch a duplicate task blind. Look at what state the thread is actually in: still genuinely working (real recent tool activity), stalled waiting for a "proceed" nudge, or hit a real blocker (usage limit — red error indicator in the sidebar; a crashed tool call; something else). Act on what you actually find, not on an assumption.
- **Never trust a self-reported "done" without independent verification** — check the actual evidence the report cites (a git commit really exists, a process is really running, a live call really succeeds). A session can be sincerely wrong about its own success.
- A session does not resume on its own just because a blocking condition (like a usage limit) clears — it needs an explicit "proceed" / continue message sent to it.

## The same pattern applies to Claude Code itself

When Claude Code hits its own usage/token limit mid-task, it does not need to be manually re-prompted from scratch once capacity returns — a scheduled check-back (the same mechanism recommended in step 4) picks the work back up on its own. Ted: "Claude will auto finish when tokens come back." This is the same fire-and-check-back principle as the rest of this skill, just applied to Claude Code's own session rather than a dispatched ChatGPT/Codex one.

## Real operational lessons (2026-09-01 live run)

A full generate → process → place → escalate run (10 images, multiple sessions, real handoffs) surfaced these — see `project_image_factory_capability_recovery_specimen_2026_09_01.md` (memory) for the full worked example:

- **Avoid the words "batch" and "group" when dispatching generation-style work.** Plain numbers work better — "let's do 8" or "four worked, twice." Not fully understood why, but repeatedly observed.
- **8-10 items as an opening instruction reliably works** for a single generation session ("let's do 8 one after another").
- **Recovery is reconciliation, not restart.** When a run fails partway, check what's actually there (list the actual output, match by exact byte count/hash against what was intended) and complete only the real gap. Don't re-derive or redo from scratch.
- **Multi-stage work spanning several sessions is normal.** Generate/process/place can legitimately be different authority boundaries, not one continuous task — expect real handoff files between stages, not one clean end-to-end report.
- **The escalation ladder, explicitly:** try the bounded work yourself → if genuinely blocked by an authority boundary (not a skill gap), finish and verify everything within your own bounds first → then write a precise, evidence-backed proposal naming the exact capability needed and a real acceptance test. A vague "I got stuck" is not an acceptable stopping point if there's more you could verify or finish first.

## Common mistakes this skill prevents

- Dispatching without checking usage first, then discovering the block after the fact.
- Staying attached to one thread's live output instead of parallelizing.
- Trusting a task's own "it's done" claim without checking the cited evidence.
- Assuming a stalled thread will resume itself once whatever blocked it clears.
