---
name: agent-init-architecture
description: "Design platform-agnostic agent init prompts for multi-agent federations. Covers SALAM ceremony, F1-F13 boot, and one-constitution-many-platforms pattern."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents, init, salam, federation, multi-agent, config, boot, aaa, zen, instruction-shrink]
    related_skills: [arifos-auto-init, federated-skill-architecture, hermes-agent-skill-authoring, governance-friction-rightsizing]
---

# Agent Init Architecture

## Overview

The arifOS federation runs multiple AI agents (Kimi Code, Claude Code, OpenCode, Copilot CLI, Gemini CLI, Cursor, Hermes) on the same VPS. Each agent has its own CLI tool, config format, and entry point — but they all serve the same Sovereign under the same constitution.

The **SALAM pattern** solves this: one universal init prompt (`SALAM_AAA_INIT.md`) contains the constitution, boot ceremony, organ map, autonomy tiers, and refusal surface. Each agent's entry point is a thin wrapper (~20-30 lines) that points to the universal init and adds only platform-specific config (model, MCP servers, key paths).

## Core Principle: Instructions Are a Tax on Model Stupidity

> **Smarter models need fewer instructions.** This is not speculation — it's measured from live Claude Code captures (2026-04-20 → 2026-07-21, Pawel Huryn's `phuryn/experiments`).

Anthropic proved this empirically: Opus 4.8 runs on **383 words** of system prompt while Sonnet 5 still needs **2,094 words** for the same task. The gap is not cosmetic — the two tiers are architecturally separate code paths in Claude Code's prompt engine.

**The rule of thumb:** If an agent's instruction file keeps growing, you're compensating for a model weaker than the one you should be running. Raise the model, not the instruction count. Instruction proliferation is a diagnostic signal, not a design practice.

### The Zen Pattern (proven by Anthropic's edit)

The real edit applied everywhere was not a single big cut — the **same edit applied everywhere**:

| Old style | Zen style |
|-----------|-----------|
| "Don't add abstractions, don't add error handling, don't write comments, don't explain WHAT the code does" (11 bullets) | "Write code that reads like the surrounding code: match its comment density, naming, and idiom." (1 line) |
| Example lists, parenthetical code snippets, edge-case enumerations | Deleted entirely |
| "What NOT to save" / "before recommending from memory" subsections (long) | Single positive sentence |
| **Say what NOT to do, with examples** | **Say what TO do, once, positively, no examples** |

**Measured result:** 2,686 → 830 words (~70% cut) with the memory block loaded on both sides. The behavioural core (no memory) shrank 73%. The memory block alone shrank 59%.

### The QQQQ FFFF AAAA Framework

Classifies every prompt component into three enforceable layers for systematic audit:

| Code | Layer | Maps to | Zen strategy |
|---|---|---|---|
| **QQQQ** | Observation/Query | What the model sees: skills index, memory, user profile, file context | Compress skills to 1-liners; tier descriptions by model capability; prune stale memory entries |
| **FFFF** | Constitutional Floor | Governance rules: F13 standing ruling, F1 identity bind, F2 epistemic integrity ban | Kernel enforces at runtime via `arif_judge` — the prompt doesn't repeat the floor book. If the kernel already blocks it, delete it from the prompt. |
| **AAAA** | Action/Execution | Tool schemas, forge/act verbs, agent behaviour rules, allowed/forbidden action lists | Tier by model frontier: stronger models get full toolset with compact descriptions; weaker models get explicit usage constraints and fewer tools |

**Rule:** When zening a prompt, check every line against QQQQ FFFF AAAA. If it's an F (floor) line that the kernel enforces, delete it. If it's a Q (observation) line that's verbose, compress it. If it's an A (action) line with examples, replace with a positive principle.

### Measuring the Prompt Stack

Every agent can be audited the same way Anthropic's was — count the actual words in the live prompt, not the source file.

For Hermes: `hermes prompt-size --json` builds an offline agent and reports exact prompt sizes tier by tier.

**Key insight from a real Hermes audit (2026-07-24, DeepSeek V4 Flash session):**

| Component | Size | % of prompt |
|---|---|---|
| Skills index (49 skills) | 20.3 KB | **52%** |
| Stable tier (identity + guidance) | 11.4 KB | 29% |
| Memory + user profile | 7.1 KB | 18% |
| Context (AGENTS.md) | 0.2 KB | 1% |
| **Total system prompt** | **40.4 KB** | 100% |
| **Tool schemas** (35 MCP tools) | **65.3 KB** | +161% overhead |

**The real elephant:** the skills index is 52% of the system prompt. Tool schemas (65 KB) are bigger than the system prompt itself. Per-turn fixed cost: ~105 KB before the user says anything.

**Protocol for auditing any agent's prompt stack:**

1. **Capture** — Get the live prompt (for Hermes: `hermes prompt-size --json`; others: self-report or proxy-capture)
2. **Separate** — Isolate shipped instruction prose from session-specific content (CLAUDE.md, tool schemas, timestamp)
3. **Classify** — Tag every component as Q (observation), F (floor), or A (action) per the QQQQ FFFF AAAA framework
4. **Zen** — Apply the Zen edit per layer: say it once, positively, no examples. F-layers delete when kernel enforces. Q-layers compress. A-layers replace examples with principles.
5. **Verify** — Confirm the kernel actually enforces what was deleted. Run the agent on the zenned prompt and test edge cases.

### Application to Federation Agent Files

The same principle applies to every AGENTS.md, CLAUDE.md, and INIT.md in the federation:

1. **Kernel enforces, prompt doesn't repeat.** arifOS kernel enforces F1-F13 at runtime via `arif_judge`. The agent prompt doesn't need the full floor table inline — it gets loaded into judgment context only when `arif_judge` is called.

2. **Sections 1-7 (core doctrine) can be compressed, not just trimmed.** The mechanical trim strategy (cutting sections 8+) is necessary but not sufficient. The real gain is rewriting core sections from negative rule-lists to positive principles.

3. **Model tier determines prompt depth.** Opus/Fable agents get the zen prompt (≤500 words). Sonnet/Haiku agents keep the full rulebook (2,000+ words). When an agent's model upgrades, the prompt *shrinks* — this is the diagnostic signal that the upgrade was real.

4. **Conditional knowledge is load-on-demand, not inline.** Memory rules, floor details, organ-specific build commands, deep doctrine — loaded via skill or file pointer only when the agent enters that domain, not at session start.

### Trim vs Zen: The Difference

| **Trim** (mechanical) | **Zen** (principled) |
|---|---|
| Cut sections 8+ that duplicate other files | Rewrite sections 1-7 from negative rules to positive principles |
| Target 25-26 KB to avoid client warnings | Target lineage: Opus → 383 words, not 25 KB |
| Content moved, not deleted | Content deleted — the kernel already enforces it |
| No semantic loss | Principle replaces enumeration |
| Works for any model tier | Model tier determines how far you go |

**When you zen, you must verify:** the kernel actually enforces what the deleted instructions described. If F1-F13 rules are deleted from the prompt but not enforced by `arif_judge`, the agent is ungoverned. Zen only after kernel verification.

### Key references

- `references/claude-code-prompt-zen-2026-07.md` — full data: word counts, cross-model tier split, the three things the headline skips (70% not 80%, frontier-only, smarter model needs fewer instructions), and the mapping to federation files.
- `references/hermes-prompt-audit-2026-07-24.md` — live Hermes prompt stack measurement, QQQQ FFFF AAAA classification with real session data, per-turn cost breakdown, and specific zening targets.

## When to Use

- Adding a new agent to the AAA federation
- Creating or updating the SALAM init prompt
- Agent instruction file exceeds client token budget (e.g., Kimi warns at 32 KB)
- Consolidating multiple agent-specific init files into one canonical source
- User says "make init prompt for X" or "make this platform-agnostic"
- **Model upgrade** — after upgrading an agent's model, zen its prompt (frontier tier → ≤500 words)
- **Instruction audit** — evaluating whether existing AGENTS.md/CLAUDE.md files need zening

## Architecture

```
/root/AAA/prompts/SALAM_AAA_INIT.md          ← universal constitution (8 KB)
    ↑ referenced by:
/root/.arifos/agents/kimi/AGENTS.md           ← Kimi wrapper (~1 KB)
/root/.arifos/agents/claude/AGENTS.md         ← Claude wrapper (~1 KB)
/root/.arifos/agents/opencode/AGENTS.md       ← OpenCode wrapper (~1 KB)
/root/.arifos/agents/gemini/AGENTS.md         ← Gemini wrapper (~1 KB)
/root/.arifos/agents/cursor/AGENTS.md         ← Cursor wrapper (~1 KB)
/root/.github/copilot-instructions.md         ← Copilot wrapper (~1 KB)
/root/CLAUDE.md                               ← deep reference (22 KB, SALAM pointer at top)
/root/AGENTS.md                               ← federation rules (28 KB, trimmed)
```

### The Layer Cake

| Layer | Content | Size | Load when |
|-------|---------|------|-----------|
| **SALAM init** | Constitution, boot, organs, autonomy, refusal, sovereign signals | ~8 KB | Every session start |
| **Platform wrapper** | Agent identity, model, MCP servers, platform-specific config | ~1 KB | Auto-loaded by CLI tool |
| **Deep reference** (CLAUDE.md, AGENTS.md) | Full doctrine, Trinity-33, QQQ, invariants, build/test rules | 20-30 KB | On demand, not at boot |

## SALAM Ceremony (§0 of SALAM_AAA_INIT.md)

Every agent emits this self-attestation on wake:

```
SALAM. I am [AGENT_NAME], warga AAA on af-forge.
Sovereign: ARIF (F13). Constitution: F1-F13 loaded.
Organs: [probe result]. Session: [session_id or "standalone"].
Ready.
```

This is NOT a conversation — it's self-attestation. If any field can't be filled, boot first.

## Platform Wrapper Template

Each wrapper MUST contain:

1. **Header** — agent name, authority chain, citizenship, runtime identity
2. **INIT block** — `cat /root/AAA/prompts/SALAM_AAA_INIT.md` command
3. **Platform-specific** — model, MCP servers, autonomy mode, key paths unique to this CLI
4. **Escalation** — what requires Arif (same as SALAM §4, just referenced)
5. **Doctrine footer** — DITEMPA BUKAN DIBERI

Each wrapper MUST NOT contain:
- F1-F13 floors (lives in SALAM)
- Organ map (lives in SALAM)
- Boot sequence (lives in SALAM)
- Refusal surface (lives in SALAM)
- Sovereign signals (lives in SALAM)

**Rule of thumb:** if you'd copy-paste the same text into every wrapper, it belongs in SALAM.

## Instruction File Size Management

Client tools warn when instruction files exceed token budgets:
- Kimi Code: warns at 32 KB
- Claude Code: no hard limit but context cost increases
- Copilot CLI: reads `.github/copilot-instructions.md` (soft limit)
- OpenCode: reads `AGENTS.md` from project root

### Trim Strategy (when a client warns)

1. **Identify duplicate sections** — content that exists verbatim in other canonical files (RUNBOOK.md, LANDING.md, CONTEXT.md)
2. **Compress to pointers** — replace 20-line sections with 1-line references: `→ See RUNBOOK.md §X for full details.`
3. **Target 25-26 KB** — leave ~6-8 KB headroom so the warning doesn't fire again when you add a section
4. **Sections 1-7 are sacred** — core doctrine, floors, organs, autonomy. Don't trim these.
5. **Sections 8+ are compressible** — session checklists, pointer indexes, anomaly lists, final notes. These duplicate content in other files.

### Trim Map (proven 2026-07-15)

| Section type | Action | Typical savings |
|---|---|---|
| Session start checklist | Compress to 4-5 lines (source secrets, health probe) | ~1.5 KB |
| "Day's chaos" / memory conventions | Delete (already in daily memory convention) | ~0.4 KB |
| "When something breaks" | 1-line pointer to RUNBOOK.md | ~0.8 KB |
| Memory & fact check | Merge into "when something breaks" or §1 | ~0.5 KB |
| Pointer index table | Move to LANDING.md, keep 1-line reference | ~2.5 KB |
| Known anomalies | Move to RUNBOOK.md, keep 1-line summary | ~0.8 KB |
| Final notes for agents | Compress to single paragraph | ~0.7 KB |

**Result:** ~7-8 KB trimmed, no semantic loss (content moved, not deleted).

### Pitfall: patch tool creates duplicate sections

When the patch context hint overlaps with the replacement content, the tool may insert the new content without fully removing the old. **Always verify after patching** with `wc -c` and `tail -n +<start_line>` to check for duplicates.

## Adding a New Agent

1. Create `/root/.arifos/agents/<name>/AGENTS.md` using the wrapper template above
2. If the agent uses a non-standard entry point (like Copilot's `.github/copilot-instructions.md`), create it there instead
3. Verify: the wrapper should be <2 KB, and `cat /root/AAA/prompts/SALAM_AAA_INIT.md` should work from the agent's shell
4. Test: launch the agent, confirm SALAM ceremony emits correctly

## Key Paths

| What | Path |
|------|------|
| Universal SALAM init | `/root/AAA/prompts/SALAM_AAA_INIT.md` |
| Federation rules (trimmed) | `/root/AGENTS.md` |
| Zero-context landing | `/root/LANDING.md` |
| Deep reference | `/root/CLAUDE.md` (22 KB) |
| Agent INIT (full) | `/root/AAA/prompts/INIT.md` |
| Ops runbook | `/root/RUNBOOK.md` |
| Agent homes | `/root/.arifos/agents/{kimi,claude,opencode,gemini,cursor,forge}/` |

## Init Versioning Pattern

When upgrading the init prompt (e.g., v3.0 → SALAM), keep both with clear roles:

| File | Role | Loaded when |
|------|------|-------------|
| **SALAM_AAA_INIT.md** | Canonical boot entrypoint | Every session start |
| **INIT.md** | Extended reference (Trinity-33, RSI, QQQ) | On demand for deep work |

**Cross-reference rules (sovereign decision 2026-07-15):**
- SALAM header: `Boot entrypoint: Canonical. v3.0 retained as extended reference.`
- v3.0 header: `Boot: Via SALAM (canonical). Load this file on demand.`
- CLAUDE.md checklist: `Booted via SALAM` replaces `Loaded active INIT v3.0`
- CLAUDE.md pointer table: SALAM = canonical boot, v3.0 = depth reference

**Never:** two competing SOTs. One is active init, one is depth reference. The distinction must be explicit in both files' headers.

## Platform Entry Point Inventory

| Agent | Entry Point | Notes |
|-------|-------------|-------|
| **Kimi Code** | `/root/.arifos/agents/kimi/AGENTS.md` | Auto-loaded by kimi CLI |
| **Claude Code** | `/root/.arifos/agents/claude/AGENTS.md` | Plus `/root/CLAUDE.md` (22 KB deep ref) |
| **OpenCode** | `/root/.arifos/agents/opencode/AGENTS.md` | Reads from agent home |
| **Copilot CLI** | `/root/.github/copilot-instructions.md` | GitHub convention path |
| **Gemini CLI** | `/root/.arifos/agents/gemini/AGENTS.md` | Auto-loaded by gemini CLI |
| **Cursor** | `/root/.arifos/agents/cursor/AGENTS.md` | Plus `.cursorrules` if present |
| **Hermes** | SOUL.md + system prompt | Separate identity artifact |
| **Forge (internal)** | `/root/.arifos/agents/forge/AGENTS.md` | Internal executor agent |

## Linked Files

- `references/agents-md-trim-2026-07-15.md` — real-world trim: 31.4→28 KB, sections 8-11 compressed, duplicate-header pitfall
- `references/claude-code-prompt-zen-2026-07.md` — full data: word counts, cross-model tier split, the three things the headline skips (70% not 80%, frontier-only, smarter model needs fewer instructions), and the mapping to federation files
- `templates/agent-wrapper-template.md` — copy-paste template for new agent wrappers

## Common Pitfalls

1. **Duplicating constitution in every wrapper.** F1-F13 floors, organ map, refusal surface belong in SALAM once. Wrappers reference, not repeat.

2. **Wrapper too heavy.** If a wrapper exceeds 2 KB, you're probably duplicating SALAM content. Check what can be moved up.

3. **Not trimming with headroom.** Trimming to exactly 32 KB means the warning fires again next time you add a section. Target 25-26 KB.

4. **Trimming core sections.** Sections 1-7 (doctrine, floors, organs, autonomy) are sacred. Only trim sections 8+ that duplicate other files.

5. **Patching without verifying.** Always `wc -c` after patching instruction files. The patch tool can create duplicates when context hints overlap.

6. **Forgetting CLAUDE.md pointer.** `/root/CLAUDE.md` is 22 KB deep reference. It should have a SALAM pointer at the top so agents know to load SALAM first, CLAUDE.md on demand.

7. **Platform-specific MCP config in SALAM.** MCP server lists vary per agent (Kimi has 10, Hermes has different). Keep MCP config in wrappers, not SALAM.

8. **Zening without verifying kernel enforcement.** If you delete inline F1-F13 rules from the agent prompt because "the kernel enforces it," verify that `arif_judge` actually blocks the behaviour at runtime first. Zen = principled deletion, not blind deletion.
