# Telegram Chat Mapping — Template for User Approval

Use this template when mapping Telegram bots to their groups/channels/DMs.
Collect config from: `~/.hermes/config.yaml`, profile configs, startup scripts,
systemd units, and `channel_directory.json`.

## Architecture Overview

```
3 Bots x 8 Groups x 15 DMs

@ASI_arifos_bot --+-- AAA (war room)          -- Hermes Agent
                   +-- SADO, AL AMIN, etc.      (conversation, governance)
                   +-- ARIF DM ---+------ OpenClaw @AGI_ASI_bot
                   +-- Syed DM    +-- ARIF DM only (allowlist)

@arifOS_bot -------+-- OpenCode bot.py          -- FORGE / HANDS layer
                    +-- FORGE gateway            (code, infra, execution)
```

## Bot A: @ASI_arifos_bot -- Hermes Agent

**Bot ID:** 8410138119
**Token var:** `ASI_ARIFOS_BOT_TOKEN`
**Service:** `hermes-asi-gateway.service`
**Script:** `/usr/local/bin/hermes-gateway-secure.sh` -> sources `runtime/.env`
**Config:** `~/.hermes/config.yaml` + `profiles/hermes_asi|apex|forge/config.yaml`

| Chat | ID | Type | Role | Status |
|------|----|------|------|--------|
| AAA | `-1003753855708` | Group+topics | Federation war room | active |
| SADO | `-1003815535761` | Group | Trading | active |
| Dear NABILAH | `-1003792478194` | Group | | active |
| Kanak-kanak | `-1003768847825` | Group | | active |
| AA | `-1003521544074` | Group | | active |
| Al AMIN | `-1003721331017` | Group | | active |
| arifOS channel | `-1004446358629` | Channel | Broadcast | active (MISSING from channel_directory) |
| BODYBUILDER | `-5561731065` | Group | | active |
| ARIF | `267378578` | DM | Sovereign | free_response |
| Syed/Abang Sado | `1042200555` | DM | SADO trading | free_response |
| Wawa (Azwa) | `8324190535` | DM | Adik | |
| *(others)* | `*` | DM | | |

- **allowed_chats:** 8 groups
- **free_response_chats:** 8 groups + 4 DMs + sovereign

## Bot B: @AGI_ASI_bot -- OpenClaw Gateway

**Bot ID:** 8149595687
**Token var:** `TELEGRAM_BOT_TOKEN`
**Service:** `openclaw-gateway.service`
**Script:** `/usr/local/bin/openclaw-gateway-secure.sh` -> sources `vault.env`
**Port:** 18789

| Chat | ID | Type | Role | Status |
|------|----|------|------|--------|
| ARIF | `267378578` | DM | Sovereign (allowFrom) | |
| All groups | `*` | Group | mention-required | `groupMentionRequired: true` |

- **dmPolicy:** `allowlist` (only ARIF)
- **groupPolicy:** `open` with `groupMentionRequired: true`

## Bot C: @arifOS_bot -- FORGE / OpenCode

**Bot ID:** 8727562763
**Token var:** `FORGE_BOT_TOKEN`
**Service 1:** `forge-gateway.service` -> Hermes gateway (FORGE profile)
**Script:** `/usr/local/bin/forge-gateway.sh` -> sources `~/.forge/.env`
**Service 2:** `opencode-bot.service` -> `EnvironmentFile=vault.flat.env`

Toolbench bot -- no group chat binding. Pure tool interface.

## Known Unknowns (needs user approval)

| ID | Found in | Missing | Action |
|----|----------|---------|--------|
| `-1004446358629` | allowed_chats | channel_directory.json | ADD entry |
| `5316953867` | free_response | name/context | VERIFY or REMOVE |
| `5250473787` | free_response | name/context | VERIFY or REMOVE |

## Token Source Governance Gap

| Service | Sources From | In vault? |
|---------|-------------|-----------|
| Hermes ASI | `runtime/.env` | NO |
| FORGE | `~/.forge/.env` | NO |
| OpenClaw | `vault.env` | YES |

## Provenance

- **Template created:** 2026-07-26
- **Source session:** Token rotation + multi-bot infra audit
- **Verified against:** config YAML, systemd units, startup scripts, all 3 Telegram APIs
