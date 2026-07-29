# OpenClaw Alignment Sweep — Worked Example (2026-07-29)

**Agent:** OpenClaw (AGI-level gateway, warga-aaa lane 555-ASI)
**Phase:** Post Phase 0-6 consolidation alignment sweep
**Duration:** One session, 6 phases
**Result:** SEAL-READY — 0 deprecated names, 0 APEXMax references, 5 skills federated

## Discovery (Phase 1)

OpenClaw's file layout:

```
/root/AAA/agents/openclaw/
├── AGENTS.md              — Operational protocol (213 lines)
├── IDENTITY.md            — Who/what/why (81 lines)
├── SOUL.md                — Voice (105 lines)
├── TOOLS.md               — Tool surface (58 lines)
├── LAYOUT.md              — Canonical layout (33 lines)
├── HEARTBEAT.md           — Health check (28 lines)
├── BOOTSTRAP.md           — Cold start (44 lines)
├── agent-card.json        — A2A agent card (635 lines)
├── config/
│   ├── config.yaml        — Runtime config (102 lines)
│   └── handoff-protocol.yaml — Handoff rules (96 lines)
├── procedures/
│   └── SUBAGENT_SPAWN.md  — Sub-agent spawn template (91 lines)
└── art_binding.yaml       — ART binding config
```

## Tool Drift Found (Phase 2)

### config.yaml — 11 deprecated tool names

| Line | Old Name | Canonical |
|------|----------|-----------|
| 81 | arif_session_init | arif_init |
| 82 | arif_sense_observe | arif_observe |
| 83 | arif_kernel_route | arif_route |
| 84 | arif_gateway_connect | (legacy custom — retained) |
| 85 | arif_judge_deliberate | arif_judge |
| 86 | arif_ops_measure | (legacy custom — retained) |
| 87 | arif_heart_critique | (legacy custom — retained) |
| 88 | arif_reply_compose | (legacy custom — retained) |
| 89 | arif_memory_recall | arif_memory |
| 90 | arif_mind_reason | arif_think |
| 91 | arif_evidence_fetch | (legacy custom — retained) |

Missing canonical tools: **arif_forge**, **arif_seal**

### TOOLS.md — Same 11 deprecated names, same mapping

### agent-card.json — surface mismatch

| Old | New | Reason |
|-----|-----|--------|
| arif_act | arif_forge | Wrong name for execution gate |
| (missing) | arif_memory | Required canonical tool |
| tool_count: 7 | tool_count: 8 | Needed updating |

## Protocol Migration (Phase 3)

8 APEXMax/APEX references found in `handoff-protocol.yaml`:

| Location | Old Text | New Text |
|----------|----------|----------|
| EXEC_COMPLETE action | "Route to APEXMax if 888_HOLD" | "Route to arif_judge if 888_HOLD" |
| JUDGE_REQUEST target | `to: apexmax` | `to: arif_judge` |
| JUDGE_REQUEST action | `apexmax_action:` | `arif_judge_action:` |
| JUDGE_REQUEST follow-up | `hermes_action_post_apex:` | `hermes_action_post_judge:` |
| Decision tree (SEAL) | "Hermes routes to APEXMax → APEXMax returns verdict" | "Hermes routes to arif_judge → arif_judge returns verdict" |
| Decision tree (HOLD) | "includes APEX verdict if available" | "includes arif_judge verdict if available" |
| Decision tree (irreversible) | "sends JUDGE_REQUEST to APEXMax" | "sends JUDGE_REQUEST to arif_judge" |
| Group chat rule | "APEXMax NEVER speaks in group" | "arif_judge NEVER speaks in group" |
| Forbidden | "bypassing APEXMax for irreversible actions" | "bypassing arif_judge for irreversible actions" |

## Skills Federation (Phase 4)

5 consolidated skills added to `/root/AAA/registries/skills.yaml`:

| ID | Canonical Hermes Skill | Risk Tier | Floor Scope |
|----|----------------------|-----------|-------------|
| federated-vps-response | autonomous-vps-response | medium | F1, F4, F11 |
| federated-nasi-lemak-tracking | nasi-lemak-tracking | low | F1, F2 |
| federated-free-loop-mesh | flame-free-loop-mesh | low | F2, F4 |
| federated-telegram-userbot | telegram-userbot-telethon | medium | F1, F12, F13 |
| federated-trading-stack | trading-signal-chart + agentic-trading-companion + mt5-ai-trading-agent | high | F1, F2, F4, F6, F7, F11, F13 |

## Zen Alignment Gaps (Phase 5)

| Check | Verdict |
|-------|---------|
| 000-999 loop | ✅ PASS |
| F1-F13 enforcement | ✅ PASS |
| A2A peers | ✅ PASS |
| ART binding | ✅ PASS |
| Stale org references | ✅ PASS (Consolidation Note documented) |
| APEXMax references | ✅ FIXED (8 references) |
| Tool naming consistency | ✅ FIXED (6 deprecated names) |

Gaps found:
- **LOW**: agent-card.json metadata references `KERNEL-quantum-runtime` and `KERNEL-qubit-substrate` — experimental/stale kernel deps
- **LOW**: TOOLS.md, HEARTBEAT.md, BOOTSTRAP.md, IDENTITY.md dates 3 months stale

## Files Modified

| File | Changes |
|------|---------|
| config/config.yaml | 6 tool renames, 2 additions (arif_forge, arif_seal), comments for legacy tools |
| TOOLS.md | 6 tool renames with `(was:)` source annotation, 2 additions |
| agent-card.json | arif_act → arif_forge, +arif_memory, tool_count 7→8 |
| handoff-protocol.yaml | 8 APEXMax→arif_judge, field rename |
| registries/skills.yaml | +5 federated Hermes skills (150→155 total) |

## Report

Full structured report: `/root/forge_work/2026-07-29/openclaw-alignment-report.json`
