# Cross-Actor Skill Review Queue

Last reviewed: 2026-06-13 by Codex

Purpose: keep a small, repeatable queue for skills that may benefit the whole group. This is not a request to import every actor-local skill. The target is reusable behavior that should be shared across actors, while runtime-specific mechanics stay local.

## Review Rule

- Promote or adapt only skills that capture a recurring group-level judgment move.
- Keep actor/runtime recovery mechanics local unless the same behavior is useful across actors.
- Prefer one bounded promotion at a time, with verification that the shared skill is visible where needed.
- Revisit this queue during `skills-review` passes or after a real work case exposes a repeated gap.

## Current Candidates

### 1. Scheduled output quality review

- Source: `/Users/ted/.hermes/skills/quality-assurance/cron-job-output-quality-assessment/SKILL.md`
- Proposed shared shape: `scheduled-output-quality-review`
- Why it helps the group: scheduled outputs, digests, monitor results, dispatcher reports, and cron-style summaries all need the same practical question answered: did this output satisfy the job it was supposed to perform?
- Recommendation: promote/adapt first.
- Notes: generalize beyond Hermes cron jobs; keep the grading/review behavior, but make the trigger about any scheduled or recurring output.

### 2. Bounded experiment / spike

- Source: `/Users/ted/.hermes/skills/software-development/spike/SKILL.md`
- Proposed shared shape: likely `bounded-experiment` or an addition to an existing planning/proposal skill.
- Why it helps the group: sometimes a small live experiment is the right next action before committing to a build or durable system change.
- Recommendation: adapt later, not copy as-is.
- Notes: remove language that implies underbuilding by default; frame experiments as enough-to-answer-the-risk, not as a thin product substitute.

### 3. Agent-driven implementation and review pattern

- Source: `/Users/ted/.hermes/hermes-agent/optional-skills/software-development/subagent-driven-development/SKILL.md`
- Proposed shared shape: reference material for `context-extension-surfacing` or a future agent-task review skill.
- Why it helps the group: it has a useful pattern of delegating bounded work and then reviewing both spec fit and implementation quality.
- Recommendation: study after the first scheduled-output skill promotion.
- Notes: too heavy to promote wholesale right now; extract the review discipline rather than the whole workflow.

### 4. Pieces MCP tool guide

- Source: `/Users/ted/.agents/skills/pieces-mcp/SKILL.md`
- Proposed shared shape: shared tool-choice/adaptor note only if multiple actors actually have the Pieces tools exposed.
- Why it helps the group: Pieces may provide useful memory, workstream, browser, calendar, and filesystem retrieval across actors.
- Recommendation: defer until tool availability is checked per actor.
- Notes: do not promote a guide that would cause actors to reach for tools they cannot call.

### 5. Hermes gateway recovery

- Source: `/Users/ted/.hermes/skills/software-development/hermes-macos-gateway-recovery/SKILL.md`
- Proposed shared shape: keep Hermes-local; optionally reference from Hermes shared runtime documentation.
- Why it helps the group: it prevents wrong recovery behavior around the Hermes runtime.
- Recommendation: do not make a general shared skill.
- Notes: this is valuable precisely because it is runtime-specific.

### 6. Legacy session-end router cleanup

- Source: `/Users/ted/.agents/skills/actor-session-end-router/SKILL.md`
- Proposed shared shape: none.
- Why it helps the group: cleanup may reduce confusion now that actor-specific session-end surfaces exist.
- Recommendation: revisit during a maintenance pass; retire only if no actor still needs it.

## Next Pass Order

1. Promote/adapt `scheduled-output-quality-review`.
2. Re-read the Hermes `spike` and optional `subagent-driven-development` skills together and extract only the reusable group behavior.
3. Check Pieces tool exposure across actors before any shared guide.
4. Review Hermes-local recovery and legacy session-end routing only as cleanup, not as group promotion candidates.

## Already Checked

- `/Users/ted/Skills/poka-yoke/PROPOSED_DELTAS.md` has no current unapplied pending deltas as of this review.
- Hermes has many app/library skills; this queue intentionally lists only the candidates that appeared plausibly useful to the group.
