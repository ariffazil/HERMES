# SALAM AAA INIT — Platform-Agnostic Agent Bootstrapping

> **Pattern class:** Multi-agent federation init canonicalization
> **Forged:** 2026-07-15 — HERMES-PRIME-AAA under F13 SOVEREIGN
> **Artifact:** `/root/AAA/prompts/SALAM_AAA_INIT.md` (8.2 KB, 11 sections)

## The Problem

A multi-agent federation has N agents (Kimi Code, Claude Code, OpenCode, Copilot, Gemini, Cursor, OpenClaw, Hermes) each with different tool surfaces, config formats, and runtime characteristics. If each agent has its own init prompt, they drift — and the constitution drifts with them.

## The Solution

**One universal init prompt, N thin platform wrappers.**

```
/root/AAA/prompts/SALAM_AAA_INIT.md  ← universal (8.2 KB, 11 sections)
/root/.arifos/agents/kimi/AGENTS.md   ← thin wrapper (~1 KB)
/root/.arifos/agents/claude/AGENTS.md ← thin wrapper (~0.8 KB)
/root/.arifos/agents/opencode/AGENTS.md ← thin wrapper (~0.9 KB)
/root/.github/copilot-instructions.md ← thin wrapper (~0.9 KB)
/root/.arifos/agents/gemini/AGENTS.md ← thin wrapper (~0.7 KB)
/root/.arifos/agents/cursor/AGENTS.md ← thin wrapper (~0.8 KB)
/root/.arifos/agents/kimi/AGENTS.md   ← thin wrapper (~1.1 KB)
/root/CLAUDE.md                       ← deep reference (22 KB, SALAM pointer at top)
```

## The SALAM Ceremony (§0)

Every agent emits this on boot — self-attestation, not conversation:

```
SALAM. I am [AGENT_NAME], warga AAA on af-forge.
Sovereign: ARIF (F13). Constitution: F1-F13 loaded.
Organs: [probe result]. Session: [session_id or "standalone"].
Ready.
```

## SALAM Sections

| § | Content | Purpose |
|---|---------|---------|
| 0 | SALAM ceremony | Self-attestation — blocking, no task until complete |
| 1 | Boot sequence | Who you are, key paths, org health probe |
| 2 | F1-F13 floors | One-line each — constitutional floor binding |
| 3 | Federation organs | Ports, roles, mutation permissions |
| 4 | Autonomy tiers | T1/T2/T3 — when to ask vs act |
| 5 | Sovereign signals | Immediate ACT triggers ("buat ja la", etc.) |
| 6 | Output contract | ≤3 sentences, RASA rule, machine vs human |
| 7 | Refusal surface | Constitutional never-do list |
| 8 | RSI protocol | Session-end self-improvement |
| 9 | Status line | OPERATIONAL/THEORY/AUDIT/FORGE |
| 10 | Deeper reading | Pointer table to full docs |

## The Wrapper Pattern

Each thin wrapper follows this template:

```markdown
# [Agent Name] — Warga AAA
> **Authority:** 888 (Muhammad Arif bin Fazil, F13 SOVEREIGN)
> **Citizenship:** warga-aaa | **Status:** ACTIVE
> **Runtime:** [runtime-name] | **Config:** [config-path]

## INIT
Load the universal SALAM prompt first:
`cat /root/AAA/prompts/SALAM_AAA_INIT.md`
Then emit SALAM (§0) and run boot sequence (§1.2).

## PLATFORM-SPECIFIC
- **Model:** [model info]
- **MCP servers:** [server list]
- **Autonomy:** Per F13 sovereign directive

## ESCALATION TO ARIF
Same as SALAM §4 — T3 actions only.
DITEMPA BUKAN DIBERI.
```

## Versioning

- **SALAM v1.0.0** — canonical boot entrypoint for all agents
- **AGENT_INIT_v3.0** — retained as extended reference for Trinity-33, RSI, QQQ (on-demand, not at boot)
- `/root/CLAUDE.md` — deep reference surface (22 KB, EUREKA architecture)

## Key Principle

The constitution lives in ONE place (SALAM). Agents differ only in their platform-specific thin wrappers. When F1-F13 changes, one edit fixes all agents. When a new agent joins, 10 lines of wrapper code is all that's needed.
