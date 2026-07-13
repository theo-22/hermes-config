---
name: codex-usage-audit
description: Audit Codex usage efficiency and reliability on Ted's machine or a local repo. Use when Ted asks to reduce Codex context, token, tool, MCP, subagent, slash-command, review, or correction-loop waste; inspect AGENTS files, config, hooks, MCP/plugins, statusline, repeated workflows, paste-heavy workflows, and review wiring before proposing small patches.
category: meta
write_mode: none
one_line_use: audit Codex context/tool/reliability overhead before patching
fast_pick: "yes"
---

# Codex Usage Audit

Audit first. Do not rewrite core files until the audit findings and patch set are clear, unless Ted explicitly asks to implement.

## Scope

Use this for Codex-native efficiency and reliability work across:

- `~/.codex/AGENTS.md`
- repo or subdirectory `AGENTS.md` / `AGENTS.override.md`
- `~/.codex/config.toml` and repo `.codex/config.toml`
- skills, hooks, MCP servers, apps, plugins, slash commands, status line, subagents, `/goal`, and `/review`

## Audit Workflow

1. **Find loaded guidance.**
List AGENTS files that apply to the current repo or workspace. Note empty, oversized, duplicated, vague, stale, or misplaced guidance.

2. **Inspect config.**
Read Codex config for model, reasoning, sandbox, approval, MCP, plugin, profile, feature, memory, hook, telemetry, and project trust settings.

3. **Classify tools.**
List active MCP servers, apps, and plugins as:

- `keep`
- `keep/on demand`
- `disable by default`
- `investigate`

Base the call on whether the tool removes a real manual loop.

4. **Check command surfaces.**
Identify availability or durable guidance for `/status`, `/statusline`, `/compact`, `/clear`, `/review`, `/model`, `/permissions`, `/diff`, `/goal`, and `/agent`.

5. **Check status visibility.**
Look for status line or equivalent visibility into model, reasoning, context, rate limits, token counters, git branch, project root, and Codex version. Do not invent unsupported config keys.

6. **Find repeated workflows.**
Name workflows that should become skills or scripts. Prefer skills for procedural judgment; prefer scripts for fragile repeated mechanics.

7. **Find paste-heavy workflows.**
Identify places where large logs, transcripts, planning files, or reports should be handled by path-based reads, targeted search, parsing, or source inventories instead of chat paste.

8. **Assess subagents.**
Recommend subagents only for bounded independent review, parallel audits, large-log extraction, or patch review that would pollute the main context. Flag cases where subagents would waste tokens.

9. **Wire review.**
Identify where `/review`, `codex review`, repo review guidance, or local `AGENTS.md` review rules should be used.

## Deliverable

Return:

- current-state findings
- recommended small patch set
- exact files to edit
- exact proposed content or diffs
- savings target for each change: startup context, repeated context, MCP/tool overhead, model/reasoning cost, correction-loop waste, or review rework
- risks and tradeoffs
- verification steps

Stop before applying changes unless Ted explicitly approves implementation.

## Verification

Use read-only checks first. Useful commands include:

```sh
codex doctor
codex mcp list
codex plugin list
codex debug prompt-input "surface check"
find . -name AGENTS.md -o -name AGENTS.override.md
find . -path '*/.codex/config.toml'
```

After approved edits, rerun only the checks needed to prove the changed surfaces are visible and valid.
