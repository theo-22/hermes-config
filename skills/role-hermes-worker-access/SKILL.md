---
name: role-hermes-worker-access
description: Use when designing, implementing, or reviewing Hermes worker dispatch access for ChatGPT role runtimes. Covers ROLE_TOOL_SCOPES exposure, role-specific dispatch wrappers, Home/Room/path fences, mutating vs read-only worker authority, start-card/role-packet/registry updates, proof receipts, and narrow per-role access variants. Use for roles that need to dispatch Hermes workers directly or safely inherit Coordinator-style worker orchestration.
---

# Role Hermes Worker Access

Use this skill when a role should gain Hermes worker dispatch capability, or when reviewing whether a role's worker access is properly fenced.

This is not just "add `dispatch_worker` to the role." The correct pattern is role-specific authority first, then a tool wrapper that enforces that authority before calling the generic claim -> dispatch -> receipt -> release cycle.

## Core Decision

Classify the role before editing code:

- **Broad operator**: can touch a whole class of surfaces. Homes Manager is the exception case: it can manage ordinary Home/Room docs across existing Homes/Rooms.
- **Narrow domain operator**: can touch only one Home, one project root, one artifact class, or one explicit path set.
- **Read-only/verifier**: can dispatch read-only workers only; no mutating worker wrapper.
- **Proposal-only**: no worker dispatch; use proposals/inbox.

Do not expose generic `dispatch_worker` to a role unless the role is intentionally allowed to dispatch across arbitrary targets. Prefer a role-specific wrapper such as `homes_manager_dispatch_worker`.

## Implementation Pattern

1. **Read authority surfaces first**
   - Role packet under `/Volumes/Extra/Substrate/<Role>/...` or `/Volumes/Extra/Substrate/Roles/...`
   - `/Users/ted/Projects/Role_Runtime_Architecture/ROLE_LAUNCH_REGISTRY.md`
   - `/Users/ted/Projects/Role_Runtime_Architecture/CHATGPT_PROJECT_INSTRUCTIONS.md`
   - `/Users/ted/Control/mcp/server.py`
   - Any `_shared` doc triggered by the role domain, especially access, Project Room/Home governance, or worker orchestration.

2. **Name the access envelope**
   - Allowed roots or exact target paths.
   - Allowed file types and operations.
   - Whether writes may create missing standard files/directories.
   - Whether the role can call mutating workers or read-only workers only.
   - Protected surfaces that always require proposal or explicit Ted authorization.

3. **Add a role-specific wrapper**
   - Validate every target path before dispatch.
   - Reject protected roots, registries, hidden paths, cross-actor/system surfaces, and path escapes.
   - Prepend the worker prompt with the role boundary.
   - Use the existing dispatch cycle underneath, usually `_dispatch_worker(...)`.
   - Record worker receipt path and release status in the returned payload.

4. **Expose only the wrapper**
   - Add the wrapper to `ROLE_TOOL_SCOPES[role]`.
   - Do not add raw `dispatch_worker` unless the role's contract truly permits broad target dispatch.
   - If the role needs worker creation too, decide separately whether `create_worker` is appropriate. Most roles should dispatch existing workers, not mint new ones.

5. **Update role-facing surfaces**
   - Tool descriptions in `server.py`.
   - Role packet: what the role may do, what remains protected, worker authority, and failure modes.
   - Launch registry row.
   - ChatGPT project instructions.
   - Fleet tracker or current-state surface when the role-runtime contract changes.
   - `SYSTEM_ARCHITECTURE_DRIFT.md` if local proof passed but fresh ChatGPT proof remains open.

6. **Verify with live-shaped proof**
   - `python3 -m py_compile /Users/ted/Control/mcp/server.py`
   - Local role start function shows the new rung/tools/start-card boundary.
   - Allowed path write/read/revert or read-only dispatch proof, depending on authority.
   - Protected path block.
   - Outside-root path block.
   - Worker wrapper blocks out-of-scope target.
   - If mutating worker authority exists: one tiny in-scope worker dispatch against a temporary proof file, then remove/revert the file.
   - Restart the MCP bridge and confirm `http://127.0.0.1:5600/sse` returns the expected OAuth/401 boundary.

7. **Route proof**
   - Write a receipt under `/Users/ted/Operations/reports/<Role_or_Domain>/`.
   - If another actor needs to verify, write a targeted `_AI_Inbox` handoff.
   - Archive or update the source inbox packet.
   - Update CHANGES_LOG/session event only for durable runtime changes.

## Fence Recipes

For broad Home/Room roles:

- Resolve with `os.path.realpath`.
- Require path inside an existing root; do not silently create top-level Home/Room roots.
- Block protected top-level surfaces: `.git`, `.codex`, `.hermes`, `_AI_Inbox`, `_shared`, `Codex_Inbox`, `Control`, `Operations`, `Canon`.
- Block protected filenames such as `HOME_REGISTRY.md`, `ROOM_HOME_OWNERSHIP.md`, `ROLE_LAUNCH_REGISTRY.md`, `CHANGES_LOG.md`, startup/end files, and root instruction files.
- Allow only ordinary docs unless the role contract says otherwise: `.md`, `.txt`, and tightly named `.json` such as `resources/source_map.json`.

For narrow roles:

- Hard-code the exact Home/root(s) rather than reusing Homes Manager's broad fence.
- Prefer allowlists of specific subdirectories and filenames.
- If target paths are supplied by the model, validate each path before dispatch.
- If target paths come from a dashboard/API, still validate them in the wrapper.

## Worker Prompt Boundary

Every mutating wrapper should prepend a boundary like:

```text
You may mutate only the exact target_paths listed below, and only for ordinary reversible work inside <role scope>. Do not delete, move, rename, archive, create roots, edit registries, edit Canon/Control/Operations/_shared/inbox surfaces, or broaden scope. Preserve originals where you overwrite content. Stop after the requested change and report files changed, verification performed, and any blocked/protected request.
```

Then list exact paths and the task.

## Homes Manager Reference Instance

The first implementation of this pattern is the Homes Manager bounded operating authority, completed 2026-07-14.

Key files:

- `/Users/ted/Control/mcp/server.py`
- `/Volumes/Extra/Substrate/Homes_Manager/Homes_Manager_Packet.md`
- `/Users/ted/Projects/Role_Runtime_Architecture/ROLE_LAUNCH_REGISTRY.md`
- `/Users/ted/Projects/Role_Runtime_Architecture/CHATGPT_PROJECT_INSTRUCTIONS.md`
- `/Users/ted/Operations/reports/Homes_Manager/2026-07-14_HOMES_MANAGER_BOUNDED_OPERATING_AUTHORITY_RECEIPT.md`

Homes Manager is an exception case because it needs broad Home/Room management authority. Most future roles should get narrower fences.

## Connector Note

As of Ted's 2026-07-14 report, the ChatGPT MCP Coordination app was refreshed:

- URL: `https://theos-mini.tail19cc07.ts.net/sse`
- Connected on: 2026-07-09
- Version notes: `dev-72`
- Version id: `asdk_app_v_6a0f350554788191b969def2ba061283`
- App id: `connector_69d70c198d048191a294db30fb059fcd`
- Auth: OAuth

When new tools do not appear in ChatGPT, first suspect connector refresh/version visibility before re-debugging the backend.
