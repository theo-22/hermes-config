---
name: external-artifact-intake
description: Use when an external generator, app, or AI runtime (ChatGPT, NotebookLM/Gemini, a web tool, etc.) delivers an artifact into Downloads or another transient ingress and real work will use it. The first actor that substantively uses the artifact owns importing it into the durable project/Home location, verifying the landed copy, then clearing the transient copy — and editing the durable copy, never the transient original. Not for canonical/symlinked intake lanes, user-designated working areas, one-shot ephemeral reads, or internal system outputs.
metadata:
  category: file-ops
  one_line_use: import externally delivered artifacts from transient ingress to their durable home
---

# External artifact intake

External artifacts delivered through Downloads or another transient ingress are **not source-of-record artifacts**. The ingress point is a holding buffer only.

## The rule

1. **First substantive use = ownership.** The first actor that substantively uses an external artifact (any purpose beyond immediate display or one-shot inspection) owns importing it into the appropriate durable project/Home location before continuing the workflow.
2. **Verify before clearing.** After import, verify the landed copy (size/content/hash check against the ingress original) before removing anything from the transient location.
3. **Use the durable path thereafter.** Build all subsequent review, editing, processing, provenance, and references on the durable path — never around the ingress path.
4. **Clear the transient copy** only after verification passes.
5. **Edit durable, not transient.** If a correction is needed and the only working copy is still in the ingress point, import first, then edit the durable copy — never treat the transient copy as the source of record.

Lifecycle: external generator → transient ingress → first-use import → durable project/Home location → all subsequent work.

## Exceptions (ingress copy may stand as-is)

- **Canonical or symlinked intake lanes.** If the ingress path is a symlink into the project (e.g. the `IconDownloads` pattern in `gpt-build-patterns` §File Intake from ChatGPT), the artifact already lives at its canonical path — the symlink is the import.
- **Explicit user-designated working areas.** When Ted or a domain convention names a transient path as the working area for a bounded task, that designation wins for the task's lifetime.
- **True one-shot ephemeral reads.** Read once for display or an immediate decision, no durable reference built → leave in the ingress point; no import owed.
- **Internal actor/system outputs.** `_AI_Inbox` handoffs, dispatch receipts, reports the system writes to its own directories, and similar are governed by their own routing/placement rules — not this skill.
- **Domain-specific placement skills.** Where a domain skill owns placement mechanics (e.g. `accepted-image-finishing`, `governed-artifact-placement` for Museum/Image Factory objects, the MiMOUD durable locations in `mimoud-episode-review`), that skill owns the destination; this skill supplies only the general import-first contract.

## Related skills (read, don't duplicate)

- `mimoud-episode-review` — origin of this rule; its Transient-file intake rule is the domain-specific instance.
- `accepted-image-finishing` — "preserve first; transform later" pattern for accepted images.
- `gpt-build-patterns` — Downloads-symlinked staging technique for ChatGPT artifacts.
- `probe-chatgpt-host-artifact-binding` — establishes Downloads as non-authoritative for host artifact binding.
