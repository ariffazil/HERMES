---
name: agent-init-architecture
description: "Design platform-agnostic agent init prompts for multi-agent federations. Covers SALAM ceremony, F1-F13 boot, thin per-agent wrappers, instruction file size management, and the 'one constitution, many platforms' pattern. Use when adding a new agent to the federation, creating or updating init prompts, or trimming agent instruction files that exceed client token budgets."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents, init, salam, federation, multi-agent, config, boot, aaa]
    related_skills: [arifos-auto-init, federated-skill-architecture, hermes-agent-skill-authoring]
---

# Agent Init Architecture

## Overview

The arifOS federation runs multiple AI agents (Kimi Code, Claude Code, OpenCode, Copilot CLI, Gemini CLI, Cursor, Hermes) on the same VPS. Each agent has its own CLI tool, config format, and entry point — but they all serve the same Sovereign under the same constitution.

The **SALAM pattern** solves this: one universal init prompt (`SALAM_AAA_INIT.md`) contains the constitution, boot ceremony, organ map, autonomy tiers, and refusal surface. Each agent's entry point is a thin wrapper (~20-30 lines) that points to the universal init and adds only platform-specific config (model, MCP servers, key paths).

## When to Use

- Adding a new agent to the AAA federation
- Creating or updating the SALAM init prompt
- Agent instruction file exceeds client token budget (e.g., Kimi warns at 32 KB)
- Consolidating multiple agent-specific init files into one canonical source
- User says "make init prompt for X" or "make this platform-agnostic"

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
- CLAUDE.md pointer table: SALAM = canonical boot, v3.0 = extended ref

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
- `templates/agent-wrapper-template.md` — copy-paste template for new agent wrappers

## Common Pitfalls

1. **Duplicating constitution in every wrapper.** F1-F13 floors, organ map, refusal surface belong in SALAM once. Wrappers reference, not repeat.

2. **Wrapper too heavy.** If a wrapper exceeds 2 KB, you're probably duplicating SALAM content. Check what can be moved up.

3. **Not trimming with headroom.** Trimming to exactly 32 KB means the warning fires again next time you add a section. Target 25-26 KB.

4. **Trimming core sections.** Sections 1-7 (doctrine, floors, organs, autonomy) are sacred. Only trim sections 8+ that duplicate other files.

5. **Patching without verifying.** Always `wc -c` after patching instruction files. The patch tool can create duplicates when context hints overlap.

6. **Forgetting CLAUDE.md pointer.** `/root/CLAUDE.md` is 22 KB deep reference. It should have a SALAM pointer at the top so agents know to load SALAM first, CLAUDE.md on demand.

7. **Platform-specific MCP config in SALAM.** MCP server lists vary per agent (Kimi has10, Hermes has different). Keep MCP config in wrappers, not SALAM.
