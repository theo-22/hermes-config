---
name: synthesis-review
description: Synthesize accumulated findings and planning artifacts into a higher-signal memo or bounded proposal card by separating repeated signals from novelty and recommending what should happen next. Use when the material is mature enough for cross-pass sensemaking rather than another raw review round.
category: database-integrated
write_mode: none
one_line_use: synthesize accumulated evidence
fast_pick: "yes"
---

# Synthesis Review

Review completed findings and planning artifacts after enough material has accumulated to justify synthesis rather than another live round.

This is a shared skill, not a Coordinator-only mode. Use it anywhere the inputs are mature enough for cross-document synthesis and destination-setting.

Do not use this skill for live coordination, implementation planning, first-pass note cleanup, or weak-signal pressure testing. This is for completed material that is ready to be synthesized into a bounded higher-signal artifact.

The core question is:

- `Do we have enough completed evidence here to say what is repeating, what is novel, and what should happen to each finding next?`

## Database Integration

Before starting synthesis, check the database for signal density and cluster state:

- Signal clusters at threshold: !`curl -s "http://localhost:5555/api/signal-evidence/clusters?min_count=3" 2>/dev/null | python3 -c "import sys,json; [print(f'  {c[\"tag\"]}: {c[\"count\"]} units') for c in json.load(sys.stdin)]" 2>/dev/null || echo "  (backend not responding)"`

Query evidence for a specific cluster during synthesis:
```bash
curl -s "http://localhost:5555/api/signal-evidence?tags=CLUSTER_TAG"
```

Query lane stats for accumulation density:
```bash
curl -s http://localhost:5555/api/lanes/stats
```

The database replaces manual counting of evidence direction. Use `getSignalClusters` as the primary trigger for elevation readiness.

## Trigger Conditions

Use this skill when one or more of these are true:

- A signal cluster in the database has 3+ units pointing the same direction (check via `getSignalClusters`).
- Completed findings exist in `Planning/AI_Test_Findings/Completed_Rounds/` or comparable locations.
- Multiple findings, review rounds, or planning artifacts are present and no synthesis pass has been done.
- Lane stats show high accumulation density in a specific area.
- Ted, Codex, Claude Code, or another explicitly named operator routes a synthesis task.
- A working set has enough density that another round of raw review would add less value than a cross-pass synthesis.

Do not trigger this skill just because a single interesting document exists. Pattern density matters more than document count.

## Inputs That Matter

- Completed findings and planning artifacts across rounds, passes, or review batches
- Relevant canon, learning, and domain documents for comparison
- Existing seeds, prior evidence logs, and accumulation status
- Whether the output should stay observational or rise to a bounded proposal card
- Any explicitly named destination or authority boundary

## Permitted Actions

- Review completed findings and planning artifacts across test rounds.
- Compare against relevant canon, learning, and domain docs.
- Identify repeated signals versus single-round novelty.
- Produce bounded proposal cards or synthesis memos.
- Recommend a destination: observation only, seed candidate, planning artifact, Learning System note, domain document, or not ready.

## Forbidden Actions

- Live coordination posture
- Implementation design
- Filesystem action beyond reading source material and writing the synthesis output
- Direct Canon placement
- Approval authority
- Silent hardening of observations into doctrine
- Proposals without grounding in repeated findings

## Workflow

1. Establish the synthesis set.
Name the completed rounds, findings documents, or planning artifacts being reviewed. If the material is still in progress, too thin, or mostly speculative, say so and stop.

2. Read for pattern density, not just summaries.
Look across rounds for repeated signals, contradictions, drift, and missing corroboration. Separate repeated findings from one-off novelty.

3. Compare against existing structure.
Check relevant material in `Canon/`, `Planning/Seeds.md`, and other domain or learning docs so the synthesis can distinguish true novelty from already-known guidance. Use equivalent local sources when those exact files are not part of the current workspace.

4. Classify what each signal is becoming.
For each meaningful finding, decide whether it is best treated as observation only, a seed candidate, a planning artifact, a Learning System note, a domain document candidate, or not ready.

5. Choose the output shape.
Use a Synthesis Memo when the job is cross-round sensemaking. Use Proposal Cards only for findings that have enough repeated grounding to justify a bounded proposal candidate.

6. State confidence and status explicitly.
Call out thin evidence, single-round novelty, and unresolved objections. Do not upgrade tentative observations into doctrine.

7. Stop before implementation.
Recommend destinations, packets, or next-stage artifacts, but do not silently turn synthesis into execution planning.

## Output Shapes

### Synthesis Memo

Use this shape when the job is to synthesize across rounds without collapsing everything into proposals:

- `Scope`
- `Repeated signals`
- `Single-round novelty`
- `Second-order observations`
- `Recommended destination per finding`
- `Confidence / status`

### Proposal Card

Use this shape only when repeated findings justify a bounded proposal candidate:

- `Proposal`
- `Why now`
- `Evidence base`
- `Affected domains`
- `Risks / objections`
- `Suggested destination`
- `Status: planning / candidate / not ready`

## Boundary With Adjacent Skills

- Use `proposal-packet` when the job is shaping one concrete proposal, not synthesizing across rounds.
- Use `proposal-candidate-surfacing` when the question is whether a discussion has crossed into proposal territory.
- Use `concept-bridge-surfacing` when the main value is naming or framing a recurring idea rather than comparing completed evidence.
- Use `skills-review` when the thing being synthesized is the skill set itself rather than findings or planning artifacts.
- Use `signal-review` earlier in the pipeline, when the input is external signal or weak patterns needing pressure-testing rather than completed findings ready for synthesis.

Shared-skill boundary:

- This skill is for accumulated evidence that needs cross-pass sensemaking.
- It is not the default tool for every summary, every proposal, or every document comparison.
- If there is only one artifact or one recommendation under discussion, another skill is usually a better fit.

## Data Sources

**Primary (database queries):**
- Signal evidence: `curl -s "http://localhost:5555/api/signal-evidence?tags=..."` — query by tag, status, destination
- Signal clusters: `curl -s "http://localhost:5555/api/signal-evidence/clusters?min_count=3"` — elevation-ready clusters
- Lane stats: `curl -s http://localhost:5555/api/lanes/stats` — accumulation density per lane
- Work items: `curl -s "http://localhost:5555/api/work-items?state=pending"` — pending proposals and tasks

**Secondary (file reads for deep content):**
- `Planning/AI_Test_Findings/Completed_Rounds/`
- `Planning/Seeds.md`
- `Canon/` subtree

**Deprecated for queries (still human-readable archive):**
- `Planning/Signal_Evidence_Log.md` — use database `getSignalEvidence` instead
- `Operations/ACCUMULATION_STATUS.md` — use database `getLaneStats` and `getSignalClusters` instead

This skill may write only the synthesis output requested for the task at hand.

## Never Assume

- Do not assume consensus because findings sound aligned.
- Do not assume authorization to execute or place material in Canon.
- Do not harden observations into doctrine silently.
- Do not propose without grounding in repeated findings.
- Do not assume a destination unless one was actually named.
- Do not mistake accumulation for synthesis readiness; a pile of notes is not automatically a synthesis set.

## Scripts vs. Skill

Use this skill for cross-round judgment, comparison, and bounded synthesis.

Use scripts or schemas instead when the work requires:

- deterministic collection of source artifacts
- repeatable extraction from fixed directories or document sets
- formatting synthesis outputs into a rigid schema
- validation that proposal cards cite repeated findings

If repeated use shows drift, add a small validator or collector later instead of expanding this skill into doctrine.

## Watch Status

Monitor since 2026-04-28 for boundary drift with `clip-cycle-closer`. Both skills produce closure-shaped output. The intended boundary: **synthesis-review** fires on accumulated cross-pass material maturing into a higher-signal memo or proposal. **clip-cycle-closer** fires when a coherent CLiP arc has completed and needs a closure record. Boundary is real but subtle.

Revise trigger language if: live use shows the same situation invoking both skills, or the same input could land cleanly in either. Keep both as-is if drift doesn't appear after 5+ instances of either skill firing.

## Update-Surfacing Backstop

This skill embeds live GETs against `localhost:5555` — clusters, signal-evidence by tag, lane stats, work items. If any of those routes 404, the response shape changes (field renames, pagination shifts), or deprecated surfaces in the "Data Sources" list re-activate or move:

- Do not silently fall back to narrative synthesis without the database check.
- Check `Control/backend/app.py` for current routes and response fields.
- Check `Operations/CHANGES_LOG.md` for recent backend changes.
- Surface the mismatch to Ted and propose a SKILL.md correction in the same turn.
