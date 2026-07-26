# Agent Card Inventory — 2026-07-25 Full A2A Compliance Sweep

> **Session:** Hermes agent audit — "map all agent config files and make AAA A2A protocol ready"
> **Provenance:** Verified against live files at `/root/AAA/agent-cards/` and `/root/HERMES/.well-known/agent-card.json`
> **Status:** All 22 cards A2A-ready with principal_agent + warga_binding

## Summary

| Category | Count | Status |
|----------|-------|--------|
| Harness cards (FI-001–011) | 11 | ✅ All pa+wb+proto 1.0 |
| Organ cards | 4 | ✅ All pa+wb+proto 1.2 (patched 2026-07-25) |
| Identity cards | 3 | ✅ pa=architect, proto 1.0 |
| Function cards | 1 | ✅ OpenClaw pa+proto 1.0 |
| Gateway cards | 2 | ✅ agent-card.json + agent.json serving 200 |
| Hermes ASI | 1 | ✅ pa+wb → 555-ASI, proto 1.0 |
| **Total** | **22** | **✅ All ready** |

## Harness Cards (Coding Toolbench Agents)

| FI | Agent | Version | Model | Binary | 
|:--:|-------|---------|-------|--------|
| 001 | OpenCode | 1.18.3 | deepseek/deepseek-v4-pro | /usr/local/bin/opencode |
| 002 | Claude Code | 2.1.218 | deepseek/deepseek-v4-pro | /root/.local/bin/claude |
| 003 | Kimi Code | 0.29.1 | kimi/k3 | /root/.kimi-code/bin/kimi |
| 004 | Codex CLI | 0.145.0 | GPT-5.5 | /usr/local/bin/codex |
| 005 | Copilot CLI | 1.0.71 | GitHub models | /usr/bin/copilot |
| 006 | Aider | -- | -- | Not installed |
| 007 | Gemini CLI | 2.0.0 | google/gemini-2.5-flash | /root/.local/bin/gemini |
| 008 | Grok Build | 0.2.111 | xai/grok-4.5 | /root/.kimi-code/bin/grok |
| 009 | AGY | 1.1.7 | deepseek/deepseek-v4-pro | /root/.local/bin/agy |
| 010 | Continue CLI | 2.0.0 | deepseek/deepseek-v4-pro | /root/.local/bin/cn |
| 011 | Qwen Code | 0.17.1 | qwen/qwen3.7-max | /usr/bin/qwen |

## Gaps Found and Fixed

| Gap | Resolution |  
|-----|------------|
| Kimi Code had `"id": "FI-008"` instead of FI-003 | **Fixed** — patched to FI-003 to resolve collision with Grok Build |
| FI-009 AGY card did not exist | **Created** — full A2A card with pa, wb, proto, security, sig |
| A-FORGE organ card missing pa + wb | **Patched** — added principal_agent + warga_binding (FORGE-777 lane) |
| GEOX organ card missing pa + wb | **Patched** — added principal_agent + warga_binding (EVIDENCE-111 lane) |
| WEALTH organ card missing pa + wb | **Patched** — added principal_agent + warga_binding (ADVISORY-222 lane) |
| WELL organ card missing pa + wb | **Patched** — added principal_agent + warga_binding (REFLECT-666 lane) |

## Warga Lane Assignments

| Lane | authority_level | Cards |
|------|-----------------|-------|
| 333-AGI | engineer | FI-001 through FI-011, arifOS kernel, GEOX |
| 555-ASI | sovereign-delegate | Hermes ASI |
| FORGE-777 | executor | A-FORGE (aforge-mcp) |
| EVIDENCE-111 | EVIDENCE_ONLY | GEOX (geox-mcp) |
| ADVISORY-222 | ADVISORY_ONLY | WEALTH (wealth-mcp) |
| REFLECT-666 | REFLECT_ONLY | WELL (well-mcp) |

## Identity Cards (No warga_binding — they ARE the lanes)

| ID | pa.type | proto |
|:--:|:-------:|:-----:|
| 333-AGI | architect | 1.0 |
| 555-ASI | architect | 1.0 |
| 888-APEX | architect | 1.0 |

## Live Endpoints Verified

```
https://aaa.arif-fazil.com/.well-known/agent-card.json → 200 ✅
https://aaa.arif-fazil.com/.well-known/agent.json      → 200 ✅
https://arifos.arif-fazil.com/.well-known/agent-card.json → 200 ✅
```

## Skill Update

The `a2a-agent-card-registration` skill was updated with:
1. **principal_agent + warga_binding** — documented as mandatory constitutional identity blocks with field reference and lane assignment table
2. **Full A2A Compliance Audit** — 6-field sweep workflow with one-liner audit script, organ card patching pattern, and live endpoint verification
