---
name: mimoud-episode-review
description: Publish or update a MiMOUD/podcast-notes episode (audio/video from NotebookLM/Gemini, script drafted by ChatGPT) on artisticlogistics.com with a Sources page and — only when the material is substantive or new — an independent Claude adversarial source-fidelity review. Use when Ted adds a new episode, updates a source doc, or asks for "sources" / "review" / "due diligence" on MiMOUD or /notes/ content. Do not use for cosmetic page edits, and do not add an adversarial review pass just because one is possible — it's earned by real stakes, not run by default.
metadata:
  category: web-publish
  domain: artisticlogistics.com
  one_line_use: publish a checked podcast episode
---

# MiMOUD / Notes episode review

Working contract set by Ted, 2026-09-15 (source: `_sources/mimoud/MiMOUD_Evidence_and_Multi_Intelligence_Review_Standard.md`). Reviews are complementary, not duplicate approvals — each actor checks something the others can't.

## Working contract

**ChatGPT — research synthesis and episode construction.** Researches and assembles the source brief; tags 🟢 source-backed claims vs. 🟠 interpretation/clinical reasoning; explains mechanisms, competing explanations, limitations, the "why"; traces consequential statistics to inspectable sources; avoids stronger causal/clinical claims than the evidence supports; surfaces uncertainty and counterevidence rather than smoothing it away. This is synthesis, not independent verification of itself.

**Claude — adversarial source-fidelity review and publication check.** For substantive or materially changed clinical content, independently review before final publication: reopen the cited sources directly rather than trusting ChatGPT's summary; verify claims/statistics are actually supported; check evidence type and strength; look specifically for causal overreach, denominator/base-rate problems, missing qualifications, omitted safety-relevant findings, superseded guidance, commentary presented as evidence; distinguish factual/citation corrections (fix directly) from genuine clinical/interpretive judgment calls (flag for Ted, don't invent). One solid review is normally sufficient — a second pass only when the first found material problems or the source changed materially. **No recursive review loops for reassurance.**

**Ted — clinical applicability and final judgment.** Determines whether technically-supported material reflects real clinical practice, preserves appropriate distinctions/role boundaries, adequately considers engagement/harm-reduction/patient experience/workflow/resource realities, and is framed in a way he's willing to stand behind. Source fidelity and clinical adequacy are separate questions — accurately sourced material can still be clinically misleading. Don't treat a Claude review as sufficient sign-off on its own; this step isn't skippable.

**Gemini/NotebookLM — presentation, not verification.** Generates audio/video from the reviewed source packet. Generation alone never counts as an evidence review and should never be represented as one.

## Transient-file intake rule

**Downloads is an ingress buffer, not a source of record.** Gemini/NotebookLM and other systems that can't write to the project filesystem deliver source docs, audio, video, or other artifacts through Downloads.

**The first actor that makes substantive use of a downloaded artifact owns importing it into the durable project location before continuing the workflow.** After import:
- verify the durable copy landed correctly (size/content check against the Downloads original) before removing anything;
- use the durable path for all subsequent review, editing, publication, and provenance — never build continuing workflow references around a Downloads path;
- clear the transient Downloads copy once import is verified.

If a correction is needed and the only working copy is still in Downloads, import first, then edit the canonical durable artifact — never edit the transient copy as if it were the source of record.

**Lifecycle:** external generator → Downloads → first-use import → durable MiMOUD episode package → review / generation / publication.

**Durable locations (established 2026-09-15):**
- Source docs (ChatGPT drafts, not published): `/Volumes/Extra/Substrate/ArtisticLogistics/_sources/mimoud/<slug>.md` — this path is excluded from the live FTP sync (`sync_artisticlogistics.sh`, `--exclude='_sources/'`), so it never reaches the public site.
- Published episode media + pages: `/Volumes/Extra/Substrate/ArtisticLogistics/mimoud/podcasts/<slug>.{mp4,m4a}` and `.../mimoud/podcasts/index.html`; the standalone-topic equivalent is `.../notes/`.

## Publishing an episode

Site root: `/Volumes/Extra/Substrate/ArtisticLogistics/`. Deploy with `bash /Users/ted/Control/scripts/sync_artisticlogistics.sh` (live FTP push — real production site, confirm before first push of a new episode if it's not obviously routine).

1. Import: move (not copy-and-leave) new Downloads artifacts into the durable locations above; verify before clearing Downloads.
2. Per episode, on its page: title, one-line tagline, video + audio players (dark theme, existing `.episode` card CSS — copy an existing card rather than reinventing).
3. **Sources** link → a `sources-<slug>.html` page: numbered list, each entry labeled by source type where it matters (guideline, RCT, cohort, preprint, commentary — don't let a weaker source read as strong), with a real URL found via WebSearch, never guessed.
4. **Adversarial review** link → only add this page when a review was actually run (see below). Don't stub a review link with nothing behind it.

## When to run the adversarial review

Run it once, for real, when the episode makes clinical/statistical claims a reader might act on, and the source doc is new or changed materially.

Don't run it for a page-layout/copy edit, a second time on unchanged content "just in case," or as an escalating series of passes. Ted has flagged stacking review passes as excessive before — check with him before a third pass on the same doc.

Review method: a fresh, blind subagent (hasn't seen how the doc was built) reads the durable source doc in full and checks its claims against the cited sources directly via WebSearch/WebFetch — not against the doc's own framing.

If Ted wants true cross-vendor independence (not same-model-family review), prepare a paste-ready prompt for him to run in ChatGPT himself — don't claim cross-vendor review happened when it didn't.

## After a review

- Fix factual/citation errors directly in the durable `_sources/mimoud/<slug>.md` file (so the next NotebookLM regenerate picks it up) — already-published audio can't be retroactively edited.
- Add or update a `review-<slug>.html` page with findings, dated, tagged by severity, noting what was fixed vs. flagged for Ted.
- Keep the review record honest: same-model review should say so; don't imply cross-vendor scrutiny that didn't happen.

## Proportion check

Before adding a second/third review layer or a new formal page, ask: does this serve "Ted can show due diligence / more than one point of view," or is it accumulating process for its own sake? If unsure, ask rather than default to more.
