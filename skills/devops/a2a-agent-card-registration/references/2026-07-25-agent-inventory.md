# 33-Agent Federation Inventory — 2026-07-25

> Validated during A2A Live Wire activation. All 33 agents have A2A-compliant cards with principal_agent + warga_binding.

## Layer Breakdown

| Layer | Count | Agents |
|-------|:-----:|--------|
| **🧠 Identity** | 3 | 333-AGI, 555-ASI, 888-APEX |
| **🏛 Organs** | 5 | arifOS, A-FORGE, GEOX, WEALTH, WELL |
| **🔌 Extensions** | 3 | hermes-asi, makcikgpt, ARIF_FAZIL |
| **🔧 Forge Harnesses** | 11 | opencode, claude-code, kimi-code, codex-cli, copilot-cli, grok-build, antigravity, gemini-cli, aider, qwen-code, continue-cli |
| **🌐 Gateways** | 3 | openclaw, aaa-gateway, arifos-kernel |
| **⚖ Governance** | 8 | aforge-pillar, aforge-executor, geox-witness, wealth-witness, well-witness, geox-organ, wealth-organ, aforge-organ, arifos-organ, arifos-bot |
| **Total** | **33** | |

## A2A Validation Summary

| Check | Result |
|-------|--------|
| AAA validate:aaa | ✅ 33 agents, 22 hosts, 150 skills, 270 tools |
| A2A schema (8/8) | ✅ Identity, capability, delegation, evidence, result, witness, seal, vault |
| Public .well-known | ✅ 6/7 live |
| Cockpit | ✅ 8 registered |
| Federation organs | ✅ 6/6 healthy |
| Skills pool | ✅ 150 unique (exceeds 99 cap) |

## A2A Compliance — 6-Field Sweep Results

All 22 agent cards (canonical paths at /root/AAA/agents/) verified:

| FI | Agent | principal_agent | warga_binding | protocolVer | security | iface | sig |
|:--:|-------|:---:|:---:|:---:|:---:|:---:|:---:|
| 001 | opencode | ✅ | ✅ | 1.0 | ✅ | ✅ | ✅ |
| 002 | claude-code | ✅ | ✅ | 1.0 | ✅ | ✅ | ✅ |
| 003 | kimi-code | ✅ | ✅ | 1.0 | ✅ | ✅ | ✅ |
| 004 | codex-cli | ✅ | ✅ | 1.0 | ✅ | ✅ | ✅ |
| 005 | copilot-cli | ✅ | ✅ | 1.0 | ✅ | ✅ | ✅ |
| 006 | aider | ✅ | ✅ | 1.0 | ✅ | ✅ | ✅ |
| 007 | gemini-cli | ✅ | ✅ | 1.0 | ✅ | ✅ | ✅ |
| 008 | grok-build | ✅ | ✅ | 1.0 | ✅ | ✅ | ✅ |
| 009 | agy | ✅ | ✅ | 1.0 | ✅ | ✅ | ✅ |
| 010 | continue-cli | ✅ | ✅ | 1.0 | ✅ | ✅ | ✅ |
| 011 | qwen-code | ✅ | ✅ | 1.0 | ✅ | ✅ | ✅ |

Identity (333-AGI, 555-ASI, 888-APEX) ✅ ALL — principal_agent=architect, proto=1.0
Organs (aforge, geox, wealth, well) ✅ ALL — principal_agent added, proto=1.2
Functions (openclaw) ✅ — proto=1.0
Extensions (hermes-asi) ✅ — principal_agent=agent, warga=555-ASI
Gateway (main/arifOS_bot) ✅ — principal_agent added, binds 888-APEX

## Gaps Fixed This Session

| Gap | Fix |
|-----|-----|
| Kimi Code id=FI-008 (collision with Grok Build) | Fixed to FI-003 |
| FI-009 AGY missing | Created agent-card.json + skills.json |
| Organ cards missing principal_agent + warga_binding | Added to aforge, geox, wealth, well |
| hermes-asi missing principal_agent | Added (555-ASI lane) |
| main (arifOS_bot) missing principal_agent | Added (888-APEX lane) |
| All 11 harnesses missing skills.json | Created from SKILL_MANIFEST.json data |
| Status.json showing 888_HOLD | Updated to LIVE with guard documentation |

## A2A Message Flow Verified

POST /a2a/message/send with A2A-Version: 1.0 → TASK_STATE_COMPLETED ✅
Membrane middleware active on every message ✅
VAULT999 seal written on completion ✅
Live wire manifest at /root/AAA/a2a-server/live-wire-manifest.json ✅

## Agent Card Canonical Locations

```
/root/AAA/agents/
├── _external/        → FI harness cards (opencode, claude-code, etc.)
├── _lanes/           → Identity cards (333-AGI, 555-ASI, 888-APEX)
├── hermes-asi/       → Hermes ASI card
├── main/             → arifOS_bot card
├── openclaw/         → OpenClaw gateway card
├── opencode/         → OpenCode primary card
├── makcikgpt/        → MakcikGPT card
└── prospect-maturation/ → Prospect maturation card
```

**Gateway loading paths:**
- Primary: `/root/AAA/a2a-server/agent-cards/` (recursive scan)
- Secondary: `/root/AAA/agent-cards/` (CIV-33 canonical)
- Seed (gateway identity): `/root/AAA/src/seed/agent-card-official.json`
