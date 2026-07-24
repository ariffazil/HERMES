---
name: uncertainty-routing-protocol
description: "When uncertain, route to the correct evidence organ — never spawn recursive self-auditors."
triggers:
  - agent encounters uncertainty or low confidence
  - agent is tempted to spawn another copy of itself for "verification"
  - any claim needs grounding before emission
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

## Escalation to F13

Only escalate to Arif when:
- The question is about **human intent** (what does the user actually want?)
- The action is **irreversible** (F1 gate)
- Two organs **disagree** on a verdict
- Evidence is **insufficient** and no organ can resolve it
