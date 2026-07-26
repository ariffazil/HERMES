# Three-Bot Routing Topology (2026-07-26)

Approved Telegram bot routing configuration for the arifOS federation.

## Topology

```
                    ┌─────────────────┐
Arif/Group DM ────→│  @ASI_arifos_bot │──→ Hermes Agent (ALL groups)
                    │  (ASI💃)         │──→ arifOS MCP :8088 (judge)
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     OpenClaw @AGI_ASI      A-FORGE :7071   OpenCode @arifOS_bot
     (🦞AGI, AAA only)     (build/deploy)  (🔥FORGE, tool only)
```

## Bot Assignment

| Bot | Token | Groups | DM | No Mention? |
|-----|-------|--------|----|-------------|
| **ASI💃** @ASI_arifos_bot | `ASI_ARIFOS_BOT_TOKEN` | ALL 9 groups | Arif + Syed + 3 users | ✅ |
| **🦞AGI** @AGI_ASI_bot | `TELEGRAM_BOT_TOKEN` | AAA only | Arif only | N/A |
| **🔥FORGE** @arifOS_bot | `FORGE_BOT_TOKEN` | None | Arif only (tool calls) | N/A |

## ASI Bot Groups (all require_mention=false)

| Chat ID | Name | Type |
|---------|------|------|
| -1003753855708 | AAA | Group + topics |
| -1003792478194 | Dear NABILAH | Group |
| -1003768847825 | Kanak-kanak | Group |
| -1003521544074 | 🅰❗️🅰 | Group |
| -1003815535761 | SADO | Group + topics |
| -1003721331017 | Al AMIN | Group |
| -1004446358629 | arifOS channel | Channel |
| -5561731065 | BODYBUILDER | Group |
| -1003890512851 | makcikGPT | Group ✅ NEW |

## AGI Bot Groups (allowlist)

| Chat ID | Name | Notes |
|---------|------|-------|
| -1003753855708 | AAA | Only group |

## DM Service

| User ID | Name | ASI | AGI | Notes |
|---------|------|-----|-----|-------|
| 267378578 | Arif | ✅ | ✅ | Sovereign |
| 1042200555 | Syed | ✅ | ❌ | Abang Sado |
| 5316953867 | ? | ✅ | ❌ | Free response |
| 5250473787 | ? | ✅ | ❌ | Free response |
| 8798431893 | ? | ✅ | ❌ | Free response |

This topology was established and approved by Arif on 2026-07-26.
