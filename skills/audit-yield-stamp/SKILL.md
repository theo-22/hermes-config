---
name: audit-yield-stamp
description: Read, verify, and stamp completed audit case files with a yield verdict. Use when case files lack a ## CC yield rating section or have a Pending rating that needs recheck. Do not stamp without citing a verifiable evidence surface. Do not use for new audit runs — that's Audit GPT's job.
category: judgment-only
write_mode: file
one_line_use: verify and stamp audit case files
fast_pick: "yes"
---

# Audit Yield Stamp

Rate completed Audit Triage case files by verifying their findings against live system state, then writing a `## CC yield rating` section that cites the evidence surface used.

False closure is the main failure mode: stamping a verdict based on timestamp pattern-matching or session memory instead of observed system state. The stamp must cite a verifiable evidence surface — file path, DB query, command output, CHANGES_LOG entry — or fall back to `Pending — not verified this session`.

The output section keeps the historical `## CC yield rating` name because existing case files and readers expect it. The skill itself is portable: any runtime that can read the case file and verify the named evidence surface can apply the same procedure.

## When To Use

- A completed audit case file lacks a `## CC yield rating` section.
- A case file has `**Rating:** Pending` and Ted or a session-start pass asks for recheck.
- The task is to rate audit usefulness against evidence, not to perform the audit again.

## When Not To Use

- Do not use for new audit runs; that remains Audit GPT's job.
- Do not use to implement audit findings while stamping. Route implementation separately.
- Do not stamp when the evidence surface is unavailable or unclear; write `Pending — not verified this session`.

## Before You Start

Identify the target set.

**Specific file:** verify the path exists and the `## CC yield rating` section is absent or empty.

**Pending batch:** use the runtime's normal filesystem search to find:

- Explicitly Pending-rated files.
- Unstamped files modified in the last 14 days.

For Codex or Claude Code, this deterministic search is acceptable:
```bash
# Explicitly Pending-rated — always surface regardless of age
grep -l "^\*\*Rating:\*\* Pending" /Users/ted/Projects_GPT/Audit/Runs/*.md 2>/dev/null

# Unstamped case files in last 14 days (older unstamped files are accumulated backlog, not session-fresh)
find /Users/ted/Projects_GPT/Audit/Runs -maxdepth 1 -type f -name "20??-??-??_*.md" -mtime -14 \
  -exec grep -L "^## CC yield rating" {} \; 2>/dev/null
```

Cap a single pass at **5 files** unless Ted explicitly authorizes a larger batch. Verification requires reading live surfaces; moving faster than you can verify produces false closure.

## Canonical Workflow

**1. Read the case file — these sections only:**
- `## Recommended next move` — what action the auditor said should happen
- `## Findings` — what the auditor found; each finding is a claim about system state

**2. Identify the verification surface.**
Ask: what observable surface — file path, DB query, CHANGES_LOG entry, command output — would confirm or refute whether the recommended action was taken and whether the findings were accurate? Name this surface before checking it.

**3. Check that surface.** Read the file, run the query, run the command. Do not reconstruct from memory or timestamp inference ("this was probably done because date X is after date Y" is not verification).

**4. Write the stamp.** Append this section at the end of the case file:

```markdown
## CC yield rating

**Rating:** HELPFUL | NEUTRAL | LOW_YIELD | FALSE_POSITIVE | MIXED
**Evidence:** [exact path/query/command checked, and what it showed]
**Rationale:** [1-3 sentences: was the finding accurate, was the recommended action taken, what value was produced]
```

Use `Pending` when you cannot verify in this session:

```markdown
## CC yield rating

**Rating:** Pending — not verified this session
**Evidence needed:** [surface that would need to be checked]
**Reason not verified:** [explicit reason — session scope, surface unavailable, requires Ted action, etc.]
```

## Rating Vocabulary

- **HELPFUL** — finding was accurate; recommended action was taken (by CC, Codex, or Ted); produced measurable improvement
- **NEUTRAL** — finding was accurate but already-known or low-impact; action not clearly blocked by the audit
- **LOW_YIELD** — technically valid finding; cost to address exceeded value; or a real gap that isn't worth closing
- **FALSE_POSITIVE** — finding named something as a problem that wasn't, or cited wrong evidence
- **MIXED** — use when a file has 4+ findings with clearly divergent verdicts; name the split explicitly

## Exit Checklist

Before leaving each stamped file:
- Evidence surface named explicitly in the `**Evidence:**` field
- Verdict matches what the evidence shows — not what seems likely or what memory suggests
- No timestamp-inference used
- If `Pending`: explicit reason stated and evidence surface named for the next session that checks it

## Boundaries

- **Do not act on findings while stamping.** Stamping is read + verify + record, not implementation. Route actionable findings to Ted or the appropriate inbox.
- **Do not stamp findings beyond the auditor's stated scope** — auditor scope defines what CC rates.
- **Unstamped files older than 14 days are accumulated backlog.** Do not session-start-triage them without Ted's direction; the 14-day cap in `SESSION_START.md` step 3b is intentional.
- **If a required DB query is unclear**, write Pending rather than guessing. A `Pending — not verified` stamp is structurally stronger than a fabricated verdict.

## Update-Surfacing Backstop

If the `Projects_GPT/Audit/Runs/` path changes or if the `## CC yield rating` section convention is updated (e.g., new required fields), this skill needs a corresponding update. Check `Operations/CHANGES_LOG.md` and the `Projects_GPT/Audit/` README before assuming the format is current.
