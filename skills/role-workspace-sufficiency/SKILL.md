---
name: role-workspace-sufficiency
description: Use when creating, converting, reviewing, or repairing a role-runtime role and the question is whether it has enough workspace: continuity, scratch, staged output, receipts, telemetry, persistence, sandbox folders, or anti-curtailment room to function well without broad write access.
category: gpt
write_mode: file
one_line_use: check and add enough owned workspace for a role-runtime role
fast_pick: "yes"
---

# Role Workspace Sufficiency

Use this skill to prevent role-runtime conversions from becoming packet-only or over-contained. A role needs enough owned workspace to work well, but formal outputs still belong on their owning surfaces.

Read `/Users/ted/_shared/Role_Runtime_Workspace_Sufficiency.md` when applying this skill.

## When to use

Use when:

- Ted asks whether roles have continuity, scratch, persistence, telemetry, sandbox, receipts, or enough workspace.
- A role-runtime role can start or read but cannot leave its own continuity.
- A role has formal write tools but no safe draft or receipt surface.
- A role conversion feels like curtailment, "smallest useful," or over-containment.
- You are adding a new `ROLE_TOOL_SCOPES` entry or start tool for a role.

## Canonical workflow

1. Start from the role's job.
   Name what the role actually needs to carry between sessions or stage before routing outward.

2. Inventory current surfaces.
   Check the role packet, launch registry, `ROLE_TOOL_SCOPES`, existing workspace folders, start tool, stage-write tools, formal output surfaces, and closeout/telemetry surfaces.

3. Decide whether the role needs a sandbox.
   If the role has cross-session thought, draft work, staged handoffs, generated artifacts, or tool receipts, give it an owned workspace. If it is truly stateless, record that explicitly.

4. Use the default folder shape unless a role-specific root already exists:

   ```text
   /Users/ted/<Role_Name>/ChatGPT/
     continuity/
     scratch/
     staged/
     receipts/
   ```

5. Add one fenced stage-write path.
   Prefer a role-specific tool such as `<role>_stage_write`. It should write only under the owned workspace, reject path traversal, reject hidden filenames, append `.md` when helpful, and avoid overwrite by default.

6. Load the workspace at start.
   The role's start tool should include latest continuity, workspace index, relevant receipts, and the role-layer surfaces needed to orient.

7. Keep formal outputs separate.
   Final domain records, Brain writes, Canon edits, Project Room updates, saved digest runs, audit cases, and generated exhibit promotion remain on their formal owner surfaces.

8. Verify.
   Prove that the role can write/read back inside its workspace and cannot access unrelated write tools.

9. Route the decision.
   Update the role packet, launch registry, fleet tracker or room state, drift note, CHANGES_LOG, and any affected Project instructions. If the pattern was newly sharpened, update `_shared`.

## Digest default

For AI Monitoring Digest, recommend a generic sandbox as a desk:

```text
/Users/ted/AI_Monitoring_Digest/ChatGPT/{continuity,scratch,staged,receipts}
```

Use it for session continuity, scratch synthesis, staged topic candidates, handoff drafts, live-proof notes, and tool receipts.

Do not use it for final digest runs, checkpoints, provisional observations, failure reports, feed operations, or canonical pattern records. Those stay on existing Digest surfaces.

## Success criteria

- The role has enough workspace to continue, draft, stage, and prove its own work.
- Writes are fenced to the role-owned workspace unless routed through an existing formal operation.
- Start loads continuity and workspace state.
- Formal system surfaces remain authoritative.
- Verification includes one positive workspace write/readback and one negative scope check.

## Failure modes

- Treating "read-only" as "no working body."
- Creating a second archive that competes with the formal output surface.
- Giving broad filesystem write access because a role needs scratch space.
- Calling a folder a workspace when the start tool never reads it.
- Adding a sandbox to a truly stateless role as ceremony.
