---
name: review-canon-membership
description: Independently classify current Canon files as Keep, Keep-trim, Move, or Extract by applying the live Canon Membership Criterion with file-backed evidence. Use for Canon admission, relocation, subtraction, consolidation, dual-review gates, anti-pattern specimens, mixed doctrine/current-state files, or when a previously edited Canon batch needs a second-vendor verdict before Ted decides execution.
category: judgment-only
write_mode: file
one_line_use: independently classify Canon membership without mutating Canon
fast_pick: "no"
---

# Review Canon Membership

Produce decisive, comparison-ready membership verdicts without editing Canon. Judge the current file bodies against the live criterion; do not reward usefulness, history, or preservation value with Canon status unless the content also governs stable system-wide structure.

## Authority and boundaries

1. Start from the routed packet or named file list.
2. Read the live `/Users/ted/Canon/Reference/Canon_Membership_Criterion.md` completely. Its current wording outranks this skill.
3. Read `_shared/WHEN_TO_READ.md`, then the directly routed Canon-living and multi-AI review docs.
4. Treat every Canon file as read-only. A verdict is classification, not execution authority.
5. Stop before creating, moving, trimming, extracting, or deleting Canon content. Ted decides after reviewer comparison.

If the packet contains another reviewer's verdicts, avoid using them as the answer key. Read the raw files and record provisional verdicts first; compare only afterward. A summary of what changed is context, not membership evidence.

## Review workflow

### 1. Establish the exact batch

- Resolve every named path against the live filesystem.
- Include new companion files, specimens, or extracted residues explicitly named by the packet.
- Do not reconstruct prior versions unless the task specifically asks for historical comparison.
- Record missing files as a scope problem; do not infer their current content from diffs, summaries, or memory.

### 2. Read current bodies

Read each file completely enough to distinguish:

- governing rule from explanation;
- stable structure from current runtime state;
- system-wide doctrine from domain material;
- accepted practice from candidate or trial;
- authority from origin history, evidence, or preserved specimen.

Use direct file reads as primary evidence. Search matches, line counts, dates, and prior verdicts are orientation only.

### 3. Apply all four tests independently

For every file, answer:

1. **Stable structure:** Does it govern or define a load-bearing rule, protocol, schema, or structure rather than document current state?
2. **System-wide:** Does it apply across Ted's work, or across all work for a governed platform/actor?
3. **Doctrine, not trial:** Has it been proven and explicitly accepted as stable?
4. **Best expression:** Is Canon the right authority surface rather than Operations, Planning, top-level Reference, or a domain folder?

A file fails membership if any test fails. Evaluate mixed files by passage; a stable core does not make operational residue canonical.

### 4. Apply the special checks

- **Navigation exception:** Use only for Canon-internal navigation whose relocation would degrade Canon usability.
- **Scaffolding Test:** Ask whether an origin/companion file retains any non-trivial Canon-eligible rule not captured in the extracted authority. Unique governing distinctions defeat a scaffolding diagnosis; history and trivial residue do not.
- **Extract guard:** Recommend Extract only when a governing principle is mixed with non-Canon material and is already load-bearing in at least two independent domains or projects. Transferability in theory is insufficient.
- **Preservation distinction:** A specimen may deserve preservation while failing membership. Route evidence/background to top-level Reference rather than keeping it in Canon by sentiment.

### 5. Choose one verdict

- **Keep:** passes all four tests or the narrow navigation exception.
- **Keep-trim:** Canon-eligible core remains, but named passages fail one or more tests and can be removed without creating new doctrine.
- **Move:** the file fails membership; name every failed test and a concrete destination.
- **Extract:** mixed content contains an earned cross-context governing principle; name the principle, proposed Canon destination, and origin destination.

Do not return a concern list without verdicts. For every non-Keep verdict, name the failed test numbers and the content boundary that caused failure.

### 6. Write a comparison-ready return

Use this compact shape:

```markdown
### `<path>`

**Verdict:** Keep | Keep-trim | Move | Extract

**Passes/Fails:** Tests ...
**Evidence:** Current passages or structural function that determine the result.
**Keep:** ...          <!-- Keep-trim only -->
**Trim/relocate:** ... <!-- Keep-trim only -->
**Destination:** ...   <!-- Move/Extract -->
```

End with:

- a one-row-per-file verdict table;
- direct answers to any questions named in the packet;
- the no-mutation boundary;
- explicit disagreements that Ted must resolve.

Agreement is valid when earned. Independence does not require manufacturing disagreement; it requires showing which tests were applied and what current evidence controlled the verdict.

### 7. Route and close the queue

- Write the return to the destination named by the packet, defaulting to `/Volumes/Extra/Substrate/_AI_Inbox/` addressed to Ted and the requesting reviewer.
- Claim the shared return path before writing.
- Verify the file by readback.
- If the packet requires consumption, run the live `Operations/scripts/inbox_consumption.py --consume ...` command with a concise verdict summary.
- Record the durable review in the normal closeout surfaces. Do not record a pending classification as settled Canon doctrine.

## Watch status

Review this skill after 5 invocations or 30 days. Watch for:

- usefulness or preservation value being mistaken for Canon membership;
- current-state incident history piggybacking on a stable doctrine core;
- another reviewer's verdict anchoring the independent pass;
- vague concern lists replacing decisive verdicts;
- Extract proposed without two-context evidence;
- classification silently turning into Canon mutation before Ted decides;
- queue consumption omitted after the return lands.
