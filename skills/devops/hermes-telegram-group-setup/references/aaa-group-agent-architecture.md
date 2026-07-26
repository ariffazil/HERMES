# AAA Group — Agent Architecture & Interaction Model

> Updated: 2026-07-26
> Covers: Hermes Agent, OpenClaw, and all coding forge agents (OpenCode, Claude Code, Kimi Code, AGY, Codex, Grok Build, Copilot CLI)

## What AAA Is

AAA group (`-1003753855708`) is the **federation control plane** — not a general chat room, but the command bridge between Arif (F13), Hermes, OpenClaw, and the coding forge agents. It's where governance discussion, architectural decisions, and operational coordination happen.

## Agents in the Ecosystem

| Agent | Role | In AAA Group? | Interaction Mode |
|---|---|---|---|
| **🦞 AGI** (OpenClaw) | Federation overseer — monitors FQ, drift, governance integrity | ✅ Yes | Responds in-group, governance oversight |
| **ASI💃** (Hermes — me) | Intelligence relay — observe, think, route to organs | ✅ Yes | Responds in-group, auto-respond (no @mention) |
| **OpenCode** | Primary coding actuator — edit, build, test code | ❌ No | **CLI only** — triggered via `arif_forge` MCP → terminal |
| **Claude Code** | Coding fallback — Codex/Anthropic | ❌ No | CLI only |
| **Kimi Code** | Coding alternative — Moonshot K3, 1M ctx | ❌ No | CLI only |
| **AGY** | Coding agent | ❌ No | CLI only |
| **Codex** | Autonomous coding agent | ❌ No | CLI only |
| **Grok Build** | xAI builder | ❌ No | CLI only |
| **Copilot CLI** | GitHub coding assistant | ❌ No | CLI only |

## Interaction Flow

```
Arif types in AAA group
         │
    ┌────┴────┐
    │         │
  🦞 AGI    ASI💃
(OpenClaw) (Hermes)
    │         │
    │    ┌────┴────┬──────────┬──────────┐
    │    │         │          │          │
    │   Direct    Route to  Route to   Route to
    │   answer    GEOX MCP  WEALTH     WELL
    │             (earth)   (capital)  (vitality)
    │
    ├── Governance / Federation check → OpenClaw monitors
    └── Coding task?
          │
          ├── Hermes: assess scope, plan, confirm approach (in AAA)
          ├── Hermes: call arif_forge (kernel 777) → A-FORGE allocate
          ├── OpenCode/Claude Code: execute in terminal (NOT in group)
          └── Result: summarized back into AAA
```

## Why Coding Agents Are CLI-Only

| Reason | Detail |
|---|---|
| **Noise** | Build output, test logs, error traces would flood the group chat |
| **Context** | Coding agents work in terminal/workspace, not conversation threads |
| **Tool access** | OpenCode has `"*": "allow"` tool permissions — unsafe to trigger from group |
| **FORGE bot security** | @arifOS_bot is a tool interface bot restricted to Arif DM only |
| **Separation of concerns** | AAA = governance/reasoning surface; Terminal = execution surface |

## The Coding Loop

| Langkah | Where | Dalam AAA? |
|---------|-------|-----------|
| 1. Arif says "forge feature X" | AAA group | ✅ |
| 2. Hermes assesses scope, plans approach | AAA group | ✅ |
| 3. Hermes calls arif_forge → A-FORGE allocates | Kernel :8088 | ✅ (MCP) |
| 4. OpenCode/Claude Code executes in terminal | VPS terminal | ❌ |
| 5. Build/tests compete | VPS terminal | ❌ |
| 6. Result returns to chat | AAA group | ✅ |

## FORGE Bot (@arifOS_bot) Restriction

@arifOS_bot is **not in any group** (only Arif DM). This is by design:
- FORGE has tool execution capability
- Group presence could allow accidental trigger via @mention
- Deploy/coding notifications stay in Arif's private DM
- Adding FORGE to AAA group for deploy status requires Telethon handler setup in OpenCode's bot.py

**Decision (2026-07-26): HOLD on adding FORGE to AAA group.** Not enough use case to justify noise and risk.

## OpenClaw's Role (AAA-Specific)

OpenClaw's AGI bot (@AGI_ASI_bot) is restriced to AAA group only. Its roles:
1. **Flow Quality (FQ) monitoring** — federation health biomarker
2. **Drift detection** — config vs runtime divergence alerts
3. **Governance oversight** — ensures all agents follow Zen Alignment
4. **State tracking** — writes to `/root/AAA/state/flow_state.json`
5. **FQ thresholds**: >1.0 BALANCED, 0.5-1.0 DRIFT, <0.5 HOLD (all agents hold)

## Key Boundaries

| Rule | Reason |
|---|---|
| Coding agents never enter Telegram groups | Security + noise + context mismatch |
| FORGE bot is Arif DM only | Tool interface must be private |
| OpenClaw is AAA-only | Governance surface, not general chat |
| ASI💃 covers all 9 groups | Single conversational bot for federation reach |
| arifOS channel is ASI💃 only | Passive broadcast surface |
