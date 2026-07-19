---
name: governed-execution-prompt
description: "Build execution prompts for coding agents that produce runtime impact, not documentation theater. Pre-prompt codebase review, phase bundling, anti-theater principle."
triggers:
  - "prompt for opencode"
  - "prompt for claude code"
  - "prompt for codex"
  - "give to opencode"
  - "execute governedly"
  - "do it governedly"
  - "opencode prompt"
  - "execution prompt"
  - "governed prompt"
  - "ada beza ka"
  - "so what"
  - "buat apa"
  - "documentation theater"
  - "phase 1 phase 2"
---

# Governed Execution Prompt Pattern

Build execution prompts for coding agents (OpenCode, Claude Code, Codex)
that produce real runtime impact — not documentation theater.

## The Anti-Theater Principle

Documentation without wiring = hiasan dinding (wall decoration).
Phase 1 (docs) without Phase 2 (data flow) = theater.

**Always ask:** does this change runtime behavior? If not, either:
1. Bundle it with Phase 2 work that DOES change behavior
2. Be honest that it's foundational and name what Phase 2 looks like
3. Let the user decide

## Pre-Prompt Codebase Review (MANDATORY)

Before writing ANY execution prompt, gather with search_files/read_file:

| What to check | Why |
|---|---|
| Existing numbering (GENESIS 049 exists?) | Prevent overwrites |
| Public vs internal tool surface | Don't expose what shouldn't be exposed |
| Canonical file paths | Specs, manifests, schemas — where do they live |
| Test commands | What does the organ's test suite look like |
| Backward compatibility | Will this break existing callers |
| Already-taken names/numbers | Prevent collision |

## Anatomy of a Governed Execution Prompt

```
# Title — Organ Execution Prompt

> Sovereign / Tier / Organ / Date / Verdict status

## CONTEXT
What exists. What the gap is. Why now.
Reference actual file paths, line counts, tool names from codebase.

## TASK N: Short Name
### File: /path/to/file
Exact content or precise description of changes.
For docs: include ACTUAL content (GENESIS docs, decision docs).
For code: specify function signatures, field names, types.

## CONSTRAINTS
1. No new tools / no schema changes / etc.
2. Backward compatibility requirements
3. What NOT to do (explicit)
4. Test requirements
5. Commit message format
6. Deploy vs commit-only

## VERIFICATION
- [ ] File exists at expected path
- [ ] Tests pass
- [ ] Git commit with conventional message
- [ ] Specific behavioral checks
```

## Phase Bundling Rule

| Phase | What | Runtime impact |
|-------|------|---------------|
| Phase 1 | Documentation, GENESIS docs, decision docs | Zero (foundational) |
| Phase 2 | Wiring, surface changes, data flow | Real (behavioral) |
| Phase 3 | Deployment, testing, verification | Confirmation |

**Default: bundle Phase 1+2.** Let user opt for Phase 1-only.

When user challenges impact ("ada beza ka?" / "so what???"):
Don't defend documentation. Show the Phase 2 path or admit it's theater.

## User Challenge Protocol

When user asks "what will this actually change?":
1. Be honest about runtime impact per deliverable
2. Distinguish "foundational" from "behavioral"
3. Offer to expand into Phase 2 if they want real impact
4. Never oversell documentation as "change"

## Pitfalls

1. **Writing the prompt without reading the codebase first.** Always probe.
2. **Using taken numbering.** Check before assigning.
3. **Bundling too much.** 5 tasks max per prompt. Split if more.
4. **Specifying code changes too vaguely.** "Update readiness_envelope" → specify exact field names, types, default values.
5. **Forgetting backward compatibility.** Additive fields with None defaults.
6. **Not specifying commit message.** Conventional commits, specific message.
7. **Confusing "document exists" with "system changed."** GENESIS docs don't change runtime.
8. **Config collision with OpenCode.** See `references/opencode-execution-logistics.md` for the workaround when OpenCode fails with "Unrecognized keys" due to A2A agent-card files.
9. **TUI submit race.** `process(action="submit")` may leave text in buffer unsent. For multi-phase work, `opencode run` with a 600s timeout is more reliable than interactive TUI.
10. **Undershooting the timeout.** Multi-phase execution across multiple repos needs 600s. Setting 180s will kill the agent mid-phase.

## Example Session: WELL Thermodynamic-APEX Wiring (2026-07-18)

User built Jung × thermodynamics × APEX synthesis, then asked for OpenCode prompt.

Codebase review found:
- GENESIS 013/014/015 already taken → used 049/050/051
- 8 public tools out of 111 internal
- readiness_envelope.py had no thermodynamic fields
- Internal tools not mapped to conceptual framework

Bundled 5 tasks:
1. 3 GENESIS docs (energy, shadow, individuation-as-aim)
2. 1 surface decision doc (proposal, needs arif_judge)
3. readiness_envelope additive fields (backward-compat)
4. 3 new prompt definitions
5. tool_authority_manifest mapping section

User challenged: "ada beza ka lalu x buat?" — demanded runtime impact justification.
Honest answer: Phase 1 alone ≈ zero impact. Phase 2 (actual data wiring) is the real work.
Offered to bundle Phase 1+2 into single prompt.

Lesson: always lead with impact, not deliverables.
