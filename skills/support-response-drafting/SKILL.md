---
name: support-response-drafting
description: Draft concise, case-linked replies and escalations to vendor support when a requested outcome remains unresolved. Use after reading the latest thread, especially when support offers troubleshooting, documentation, or an internal tool limitation instead of completing the requested action. Works across providers such as OpenAI and Anthropic. Draft only unless the user explicitly asks to send.
metadata:
  category: judgment-only
  write_mode: none
  one_line_use: turn the latest vendor-support reply into a precise outcome-bound escalation
  fast_pick: "yes"
  version: 1.0.0
  platforms: [all]
  tags: [support, escalation, correspondence, vendor-neutral]
---

# Support Response Drafting

Turn the latest support exchange into a short, ready-to-send reply that advances the requested outcome without widening its scope.

## When to Use

- The user asks to read an existing support case and draft a reply.
- Support has explained a limitation, repeated troubleshooting, linked documentation, or described why it cannot act, but the requested outcome is still incomplete.
- A deletion, correction, access, billing, or account action needs an exact boundary and written confirmation.
- The same method is needed with any provider, including OpenAI, Anthropic, Apple, Google, or another service.

## When Not to Use

- The user wants a company-facing response written from the support agent's perspective; use a customer-service response skill instead.
- The task is primarily legal analysis, a privacy-rights demand, or a charge dispute; use the relevant specialist workflow and treat this skill only as writing support.
- The user has not supplied the thread and no authorized source can retrieve it. Ask for the latest message rather than reconstructing it.

## Canonical Workflow

1. Read the latest message in the existing case before drafting. Use older messages only to preserve settled facts, identifiers, exclusions, and prior commitments.
2. Separate the requested outcome from what support actually provided:
   - **Outcome:** the concrete action the user asked the provider to complete.
   - **Response:** troubleshooting, documentation, explanation, workaround, limitation, partial action, or completed action.
   - **Remaining gate:** the exact provider-side action or confirmation still missing.
3. Preserve exact identifiers from the authoritative thread. Never invent an object ID, case number, team name, policy, or completion state.
4. Draft in this compact order:
   - acknowledge the useful fact in the latest reply;
   - state plainly that the requested outcome remains unresolved;
   - if support lacks the necessary control, identify that as an internal capability or routing constraint, not resolution;
   - request escalation to the team with authority to complete the action, without guessing that team's name;
   - restate the exact target and explicitly protect adjacent objects, services, accounts, or data;
   - name the closure condition and request written confirmation.
5. Keep the reply in the existing case-linked email or support conversation unless that channel is unavailable. Preserve the subject when replying by email.
6. Return ready-to-send wording. Do not send, create a draft, modify an account, or perform the requested provider-side action unless the user explicitly authorizes that separate step.

## Strong Escalation Language

Prefer precise sentences over heat:

- “That tool limitation is an internal routing constraint, not resolution of this case.”
- “Please escalate this case to the team with authority to complete the requested action.”
- “Please do not close the case as resolved until the action is completed and verified.”
- “Confirm in writing that only the named object was affected.”

Use the substance, not necessarily the exact wording. Match the firmness to the provider's response and the user's requested tone.

## Evidence and Success Criteria

A successful draft:

- responds to the actual latest message;
- distinguishes explanation or inability from completion;
- names the requested action and exact target accurately;
- preserves every explicit exclusion and protected neighboring object;
- gives support one concrete next action;
- defines what counts as resolution;
- remains concise enough to send without editing;
- makes no unsupported legal, technical, or organizational claim.

## Failure Modes

- Treating “our tool cannot do that” as the final resolution instead of requesting internal escalation.
- Repeating customer-side troubleshooting after support has already agreed it is exhausted.
- Broadening a single-object request into account deletion, privacy deletion, or removal of related working integrations.
- Omitting identifiers or protected neighbors when the action is irreversible.
- Guessing which internal team owns the capability.
- Adding threats, legal claims, or deadlines the user did not request and the evidence does not support.
- Opening a new case when the existing thread can preserve history and accountability.
- Sending because the user asked for a draft.

## Runtime Notes

### Codex

When an authorized mail connector is available, search by exact case number or subject, then read the full latest thread. Treat mail actions as separate authority: reading and drafting do not authorize creating or sending a draft.

### Claude Code

Use an available mail or browser surface to read the latest case when authorized. If direct access is unavailable, ask for the latest support message. Apply the same canonical procedure; do not maintain a separate Anthropic-specific doctrine fork.

### Other Runtimes

Use any authorized read surface that preserves sender, timestamp, subject, and full message body. If only a pasted message is available, identify it as user-provided rather than live-verified.

## Update-Surfacing Backstop

Provider interfaces and support channels may change, but the outcome-versus-response distinction is stable. If a runtime repeatedly needs a new retrieval or reply mechanic, add a short runtime note or deterministic helper here rather than changing the canonical escalation standard or creating a provider-specific fork.
