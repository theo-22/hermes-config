---
name: improve-system
description: Audit a Claude Code environment (CLAUDE.md, memory, settings, hooks, installed plugins, shared-skill adoption) against Substrate's own doctrine — not generic best practice — and hand back specific fixes. Use periodically (weekly, or after a new-machine setup), whenever a plugin or config change lands, or when Ted asks "how's my Claude Code setup" / "what should I improve." Do not use for the shared skill set's own health (skills-review) or a database pulse (check-system).
metadata:
  category: judgment-only
  write_mode: none
  one_line_use: audit this machine's Claude Code setup against Substrate doctrine
  fast_pick: "yes"
---

# Improve System

Audit one Claude Code environment against Substrate's own stated rules, and hand back a short list of specific fixes — not a generic "best practices" checklist.

This exists because BuildPartner.ai's `/buildpartner:improve-system` did the generic version (reviews CLAUDE.md/plugins/workflow patterns against best practice in the abstract) and was paywalled beyond 5 free runs. The Substrate-native version checks the same surfaces against doctrine Ted has actually written down, for free, and knows where that doctrine lives.

## When to Trigger

- Periodic health check (weekly, or whenever it's been a while)
- Right after a new-machine setup or a Substrate-internalization path change
- Right after installing, removing, or upgrading a plugin
- Ted asks directly: "review my Claude Code setup," "what am I missing," "how do I get better outputs"

## What to Read

1. `~/.claude/CLAUDE.md` (global) and any project-level `CLAUDE.md` in the current working directory
2. `~/.claude/settings.json` and `.claude/settings.local.json` (project) — hooks, permissions, allowed-tools
3. `claude plugin list` — installed plugins, and whether each still earns its place
4. `~/.claude/projects/-Users-ted/memory/MEMORY.md` — index size, floor intact, staleness of pinned entries
5. Shared-skill adoption: is `~/Skills/` (canonical, at `/Volumes/Extra/Substrate/Skills/`) actually reachable from this machine (`~/.claude/skills/` symlink or alias), or has a path drifted since the last relocation
6. `/Users/ted/Canon/` doctrine this session's config claims to follow — check the claim against the live file, don't take the config's word for it

Read live files. Do not evaluate from memory of a prior audit.

## What to Evaluate

**CLAUDE.md fidelity.** Does it still say only what Ted has stated directly and repeatedly (per its own 2026-08-31 rewrite note), or has it re-accreted a session-start ritual, a lecture, or doctrine that belongs in `Canon/` instead? Compare against `Canon/Names_and_Identifiers_Policy.md` and the file-naming rule — are both still correctly summarized, not drifted?

**Memory hygiene.** Is `MEMORY.md` still a thin index (per its own 2026-09-03 cut rationale) or has it started re-growing into a flat enumeration? Are any "Placed by Scribe" entries stale — superseded by a later decision, a closed work item, or a project that's since wrapped?

**Settings and hooks.** Do configured hooks still guard something genuinely irreversible or protected (per `Canon/Reference/Active_Team_Agreements.md`'s Act-and-Report default and anti-ratchet gate discipline), or has a blocking gate crept in for reversible work? Are permissions/allowed-tools rules stale — naming a tool or path that no longer exists?

**Plugin footprint.** For each installed plugin: what does it actually do, is it still used, does it duplicate a shared skill Ted already has, and does it carry a paid tier or credential surface worth knowing about. Flag anything that looks like a one-time trial nobody revisited (see `feedback_never_propose_symlinks_home_to_extra.md`-style "quietly stuck around" pattern).

**Shared-skill reachability.** Confirm this machine's Claude Code can actually see `~/Skills/` — a broken symlink or a stale hardcoded path after a relocation (see `project_substrate_internalization_2026_09_20.md`) silently starves every shared skill without erroring loudly.

**Doctrine drift.** Anywhere the local config *asserts* a fact about Canon or Substrate paths, check it against the live file. A stale assertion here is exactly the failure mode `Active_Team_Agreements.md`'s own 2026-09-07 review caught in itself.

## What Not to Duplicate

- Shared-skill set quality (overlap, gaps, CLiP mapping) — that's `skills-review`
- System database pulse (work items, signal clusters) — that's `check-system`
- Full new-machine migration planning — that's the dedicated migration project thread

This skill is scoped to: is *this machine's Claude Code environment* internally consistent with what Ted has actually written down. Route findings that belong to those other surfaces there instead of absorbing them here.

## Output Shape

- **Findings:** each one names the specific file/line and the specific doctrine or prior decision it's out of step with — not a generic style note
- **Fixes:** concrete edit per finding, ready to apply if authorized
- **No findings:** say so plainly, don't manufacture busywork to justify the run

Keep it short. A clean environment gets a two-line report, not a padded one.

## Never Assume

- Do not evaluate CLAUDE.md or memory against generic best-practice — evaluate against what Ted's own files say the rule is
- Do not flag a hook as excessive without checking whether it guards a protected surface first (Canon, credentials, bridge, spend)
- Do not propose reinstalling a plugin just uninstalled without a stated reason it's needed again
- Do not treat this skill's own checklist as exhaustive — if live use surfaces a new class of drift, add it here in the same pass

## Update-Surfacing Backstop

This skill's checklist is only as good as its map of where Substrate doctrine lives. If a referenced path (`Canon/...`, `Active_Team_Agreements.md`, a memory file) has moved or been retired, fix the reference in the same pass that finds it stale — don't leave this skill pointing at a dead path while flagging other configs for doing exactly that.
