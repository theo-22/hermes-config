---
name: cold-probe-refine
description: Test whether an assembled concept or projected environment is reconstructable by sending a question to a cheap cold reader first, then using a stronger reviewer to classify semantic recovery and projection failures before any refinement. Use when a surface is load-bearing, newly refined, intended for delegation to cheap models, or explicitly being measured for reconstructability. Do not use for trivial assemblies, private chain-of-thought requests, automatic graph mutation, or one-run worker-selection conclusions.
metadata:
  category: database-integrated
  write_mode: file
  one_line_use: cold-probe a projected inference surface, diagnose failures, and preserve comparable Lab evidence
  fast_pick: "yes"
---

# Cold Probe Refine

Use a weaker cold reader as a sensor of what the environment teaches, then use a stronger reader to diagnose the result. Improve the external representation only after classifying the failure.

This skill composes with `lens-assembly-pass`. It does not replace `topic-assembly`, judge concept-map meaning, or perform `persist`.

## Trigger

Run when at least one condition is true:

- the assembled claim is load-bearing for later decisions;
- the surface was newly refined and its reconstructability is unproved;
- the surface is meant to support delegation to a cheap or fast model;
- Ted, Map Curator, Lab, or the operator explicitly requests a reconstructability measurement.

Skip when the assembly is trivial, already has current comparable proof, or no question-conditioned semantic test can be stated.

## Workflow

### 1. Pre-register the test

Record before dispatch:

- test question;
- source node, cluster, or context pointer plus a deterministic fingerprint;
- why the trigger applies;
- required ideas to recover;
- likely roads or evidence bearings, as hints for evaluation rather than a mandatory route;
- unacceptable distortions;
- what would distinguish projection failure, instruction/traversal failure, infrastructure failure, and reader limitation.

Do not teach the expected answer to the cold reader. Provide only the question, the authorized source surface, and the output contract.

### 2. Run the cheap cold reader first

Prefer an existing Hermes worker/profile suited to the work shape. Record both requested and actually served profile/model; never infer the served model from the profile name. Do not build a new worker, provider route, account, or credential for a probe when an existing lane can run it.

Require:

1. concise answer;
2. node/road or source-evidence path in traversal order;
3. one line on what each item contributed;
4. ambiguity, missing connection, or misleading connection report;
5. confidence;
6. worker profile, requested model, and actually served model;
7. durable Lab result pointer.

Never request private chain of thought. An inspectable evidence path is the proof surface.

### 3. Review second

Give the cold result, pre-registered rubric, and same source surface to a stronger independent reviewer. Compare semantic recovery, not exact wording or route identity.

Return one verdict:

- `pass` — required meaning recovered without an unacceptable distortion;
- `projection_failure` — the environment did not carry required meaning clearly enough;
- `instruction_or_traversal_failure` — task shaping or retrieval prevented a fair read;
- `reader_limitation` — the surface carried the meaning but this reader did not recover it;
- `infrastructure_failure` — execution failed before semantic evidence was produced;
- `inconclusive` — evidence does not separate the causes.

For any non-pass semantic verdict, classify the primary failure as one of:

- node wording;
- missing road;
- misleading road or type;
- edge-note dependency;
- traversal or retrieval;
- worker instructions;
- model limitation.

Keep infrastructure failures separate from model-quality evidence.

### 4. Refine within authority

Use the reviewer as diagnostician, not as an automatic editor.

- Route concept-node wording, relation meaning, and State-layer membership to Ted or Map Curator.
- Apply mechanical instruction or representation changes only when the current task authorizes that surface.
- If a substantive authorized refinement lands, rerun the same cold test against a new fingerprint.
- If no projection change lands, record rerun as `not_run_no_projection_change` rather than manufacturing a pass.

Default bound: one cold run, one stronger review, and at most one same-pass rerun. Start a new evidence cycle if more refinement is warranted; do not overfit indefinitely to one weak model.

### 5. Land comparable Lab evidence

Follow `/Volumes/Extra/Substrate/Lab/Model_Tests/Map_Node_Probes/COLD_PROBE_LEARNING_LOOP_CONTRACT.md`. Preserve raw receipt pointers and the normalized semantic record. A result is not complete until its durable Lab path is named.

Do not update worker-selection or model-routing conclusions from one pass. Accumulate comparable results first.

## Success criteria

- Cheap/fast reader ran first when the trigger applied.
- Stronger judgment happened only after the cold result.
- Evidence path and actually served model are inspectable.
- Semantic failure is classified before any environmental change.
- Any refinement stayed inside owner authority and earned a same-question rerun.
- Lab record distinguishes model, projection, traversal, and infrastructure evidence.

## Failure modes

- Pre-teaching the answer to make the cold model succeed.
- Scoring exact wording or one preferred road instead of semantic recovery.
- Calling a timeout or provider error a model failure.
- Letting the stronger reviewer silently rewrite graph meaning.
- Treating one successful or failed probe as a settled worker-selection verdict.
- Repeating refinements until one weak reader is overfit.

## Runtime notes

- Existing Hermes profiles are the preferred execution lane. `graph-nav-bench` is a proven cold graph reader; a stronger existing profile can review second.
- Preserve worker terminal receipts rather than copying private reasoning.
- If this skill runs inside `lens-assembly-pass`, return control to FORTIFY and PERSIST after the probe/refine cycle.
