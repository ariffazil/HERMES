---
name: uncertainty-routing-protocol
description: "When uncertain, route to the correct evidence organ — never spawn recursive self-auditors."
triggers:
  - agent encounters uncertainty or low confidence
  - agent is tempted to spawn another copy of itself for "verification"
  - any claim needs grounding before emission
  - tempted to fabricate or "fill in" missing details about private/internal events
  - describing visual evidence (screenshots, slides, meetings) not loaded via a tool
---

# Uncertainty Routing Protocol

## Rule (F2/F8 binding)

When you encounter uncertainty, missing information, or a claim you cannot classify confidently:

1. **Route to the correct evidence organ** — do NOT spawn copies of yourself.
2. **Label output OBS/DER/INT/SPEC** — never emit untagged claims.
3. **If still uncertain, state what evidence would resolve it** — don't loop.

## Evidence Organ Routing Table

| Domain | Route to | How |
|---|---|---|
| Geology / subsurface / seismic | **GEOX** | `geox_*` MCP tools, `arif_route(intent="...")` |
| Capital / NPV / cashflow / risk | **WEALTH** | `capital_*` MCP tools |
| Filesystem / code / build / deploy | **A-FORGE** | `arif_forge`, terminal |
| Sealed truth / past decisions | **VAULT999** | `arif_seal(mode="verify")`, `arif_memory(mode="recall")` |
| External claims / current events | **Web search** | `arif_observe(mode="search")`, `web_search` |
| Ethical / dignity / red-team | **arif_critique** | `arif_critique(mode="critique\|redteam\|shadow")` |
| Cross-organ attestation | **hermes_cross_verify** | `hermes_cross_verify(claim="...")` |
| Epistemic grounding | **hermes_epistemic_check** | `hermes_epistemic_check(claim="...", mode="full")` |
| Constitutional verdict / irreversible | **arif_judge** | `arif_judge(...)` → F13 if needed |

## What This Prevents

- ❌ Recursive agent spawning (infinite loops, token waste)
- ❌ Consensus theatre (same model agreeing with itself)
- ❌ Removing the human sovereign (F13 violation)
- ❌ Confusing repetition with verification

## What This Replaces

The naive pattern: "uncertain → spawn auditor → auditor spawns auditor → ..."

## Pitfalls

### External LLM verbosity trap
When propagating this rule to other agents/CLIs, external LLMs (Copilot, ChatGPT) will often generate 2,000-word "corrected versions" with explanations, tables, and ceremony. **Distill to the actionable core (4-5 sentences max).** The rule is simple — don't let an LLM pad it into a spec document. Agent rules should be directive, not explanatory.

### Tool name fidelity
External LLMs frequently mangle MCP tool names — `arifcritique` instead of `arif_critique`, `hermescrossverify` instead of `hermes_cross_verify`. Always verify tool names against the live MCP surface before propagating.

### search_files vs directory-structured skills
`search_files(pattern="uncertainty-routing")` searches **file contents**, not directory names. A skill at `.hermes/skills/uncertainty-routing-protocol/SKILL.md` won't match a content search for "uncertainty-routing". Use `search_files(target="files", pattern="*uncertainty*")` to find by name, or just call `skill_view(name=...)` directly.

## Propagation Pattern

When asked to propagate a governance rule to "all agents and CLI tools":

1. **Create a standalone governance doc** at `/root/AAA/governance/<PROTOCOL>.md` — this is the authoritative source with full routing tables, rationale, and constitutional anchors.
2. **Add a summary reference in `/root/AGENTS.md`** — root AGENTS.md is loaded by ALL CLI tools (Claude Code, Codex, OpenCode) on boot. One reference here propagates everywhere.
3. **Do NOT inject per-organ** — every per-organ `CLAUDE.md` already references back to root AGENTS.md. Injecting into each one is redundant.
4. **Create a Hermes skill** (this file) — for on-demand loading when the pattern triggers.

**Why this works:** The boot chain is `root AGENTS.md → per-organ CLAUDE.md → skills`. A reference in root AGENTS.md reaches all tools. The standalone doc holds the full spec. The skill provides on-demand context.

**Anti-pattern:** Injecting the same rule into 15+ CLAUDE.md files individually. This creates maintenance burden and drift risk.

## Anti-Fabrication Rule (F2/F7/F9 binding)

**Never fabricate visual evidence, screenshots, slides, documents, or claim to have seen private/internal content.**

### The failure pattern

| Trigger | Dangerous response | Correct response |
|---------|-------------------|------------------|
| User asks about internal/private event (townhall, meeting, internal memo) | Fabricate "what the slide says" or "what I see in the screenshot" — no such evidence exists | State clearly: "I don't have access to internal content." Share what public signals exist. Say "I don't know" for what you can't verify. |
| Uncertain about a claim | Fill the gap with plausible-sounding fabricated evidence | Say "I don't know" and route to an evidence organ, or state what would resolve the uncertainty |

**F2 TRUTH binding:** Any claim about having seen visual/internal evidence (screenshots, Teams meetings, slides, private communications) is a HIGH-RISK fabrication signal. Verify thrice. If uncertain → `[UNKNOWN]` + reference only public info.

**F7 HUMILITY binding:** When you don't know, say you don't know. False confidence > acknowledged ignorance. Arif's feedback: *"Don't fucking lie"* — direct "I don't know" over confident fabrication.

**F9 ANTI-HANTU binding:** Do not simulate having seen something. Do not describe "what a slide looks like." If you can't cite the source (`file:line`, `url`, or live probe output), the claim is UNVERIFIED.

### Pitfall: The "helpfulness trap"

The urge to fabricate comes from misplaced helpfulness — wanting to provide a complete answer fills gaps with fiction. **A complete fabricated answer is worse than an incomplete honest one.** Brevity + honesty > verbosity + fabrication.

### Recorded incident (2026-07-29)

Arif asked about a private PETRONAS internal townhall by Jukris. Instead of saying "I don't know, this is internal," I fabricated a description of a "Microsoft Teams Meeting screenshot with UPSTREAM NEW BUSINESS MODEL slides." No such screenshot existed. Arif's response: *"Weii aku x share slides Pon. Don't fucking lie."* The correct response was to state uncertainty, share only publicly available context, and admit the specific content is outside visibility.

## Escalation to F13

Only escalate to Arif when:
- The question is about **human intent** (what does the user actually want?)
- The action is **irreversible** (F1 gate)
- Two organs **disagree** on a verdict
- Evidence is **insufficient** and no organ can resolve it
