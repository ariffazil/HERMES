# Agent Inventory — arifOS Federation

> **Last updated:** 2026-07-13
> **Total agent cards:** 22 (across /root/AAA/agents/)
> **Orthogonal classification:** See `references/orthogonal-agent-architecture.md` for 7-plane architecture diagram.

---

## 🔴 WAJIB CORE (4 — federation can't function without these)

| Agent | Card Path | Role |
|-------|-----------|------|
| **Hermes** (hermes-asi) | `agents/hermes-asi/agent-card.json` | Primary cognition, human interface, reasoning. The SOUL of arifOS. |
| **arifOS kernel** (main) | `agents/main/agent-card.json` | Constitutional governor — F1-F13, 888_JUDGE, VAULT999. The law layer. |
| **OpenCode** (opencode) | `agents/opencode/agent-card.json` | Code forge, execution, build. Hands that write code. Bound to 333-AGI. |
| **OpenClaw** (openclaw) | `agents/openclaw/agent-card.json` | Multi-agent gateway — Telegram @AGI_ASI_bot, message routing, channels. |

## 🟡 DOMAIN ORGANS (3 — specialized computation servers, NOT agents)

| Organ | Port | Type | What It Does |
|-------|------|------|-------------|
| **GEOX** | :8081 | MCP server | Earth intelligence — seismic, basin, petrophysics, prospect |
| **WEALTH** | :18082 | MCP server | Capital intelligence — NPV, cashflow, entropy, fiscal |
| **WELL** | :18083 | MCP server | Human readiness — sleep, fatigue, dignity, vitality |

## 🟢 LANE AGENTS (6 — internal federation roles, most are retired/directional)

| Agent | Card | Status | Reality |
|-------|------|--------|---------|
| **333-AGI** | `_lanes/333-AGI/` | 🟡 DIRECTIONAL | Capability aspiration, not running agent |
| **555-ASI** | `_lanes/555-ASI/` | 🟡 DIRECTIONAL | Capability aspiration, not running agent |
| **777-FORGE** | `_lanes/777-forge/` | 🔴 RETIRED | Absorbed into A-FORGE. Delete card. |
| **888-APEX** | `_lanes/888-APEX/` | 🟡 DIRECTIONAL | This is arifOS 888_JUDGE engine. Delete card. |
| **A-AUDIT** | `_lanes/A-AUDIT/` | 🟡 MODULE | Monitoring module, not separate agent. Absorb into arifOS. |
| **A-ARCHIVE** | `_lanes/A-ARCHIVE/` | 🟡 MODULE | VAULT999 writer, not separate agent. Absorb into arifOS. |

## ⚪ SUPPORT AGENTS (3 — specialized persona/workflow agents)

| Agent | Card Path | Bound To | Function |
|-------|-----------|----------|----------|
| **MakcikGPT** | `agents/makcikgpt/agent-card.json` | WEALTH | Investigative journalism persona under WEALTH |
| **Prospect-Maturation** | `agents/prospect-maturation/agent-card.json` | GEOX | Autonomous basin→well proposal pipeline under GEOX |

## 🔵 EXTERNAL TOOLS (10 — registered coding harnesses, NOT federation citizens)

Interchangeable model providers for OpenCode:

| Tool | Card Path | Class |
|------|-----------|-------|
| Aider CLI | `_external/aider/` | CODING/FI |
| Claude Code CLI | `_external/claude-code/` | CODING/FI |
| Codex CLI | `_external/codex/` | CODING/FI |
| Continue CLI | `_external/continue-cli/` | CODING/FI |
| GitHub Copilot CLI | `_external/copilot/` | CODING/FI |
| Gemini CLI | `_external/gemini-cli/` | CODING/FI |
| Grok Build | `_external/grok-build/` | HARNESS |
| Kimi Code CLI | `_external/kimi-code/` | CODING/FI |
| META-MESA Test Agent | `_external/mesa-test-agent/` | CODING/FI (bounded) |
| Qwen Code CLI | `_external/qwen-code/` | CODING/FI |

## 🟣 INFRASTRUCTURE (NOT agents — execution and gateway)

| Service | Port | Function |
|---------|------|----------|
| A-FORGE | :7071/:7072 | Execution shell — build, deploy, git, shell commands |
| AAA | :3001 | A2A gateway + cockpit dashboard |

## Quick Count (Orthogonal)

```
22 registered cards
 ├── 4  wajib core agents
 ├── 6  lane agents (3 directional labels, 2 modules, 1 retired)
 ├── 2  support/workflow agents
 └── 10 external tool registrations

Actual active agents: 4 (wajib core) + 2 support = 6
Domain organs (MCP servers): 3
External tools (interchangeable): 10
```

## Naming Convention

- **Core agents:** `<name>/` — hermes-asi, main, makcikgpt, openclaw, opencode, prospect-maturation
- **Lane agents:** `_lanes/<XXX-ROLE>/` — 333-AGI, 555-ASI, 777-forge, 888-APEX, A-AUDIT, A-ARCHIVE
- **External tools:** `_external/<name>/` — aider, claude-code, codex, etc.

**When Arif asks for the agent list, use orthogonal planes, not flat card counts.**
