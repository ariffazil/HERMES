# Multi-Bot Telegram Architecture — arifOS Federation

> Verified: 2026-07-26 (post-token-rotation)
> Source: full sweep across configs, systemd, scripts, and vault.env

## Three Bot Tokens (all rotated)

| Bot | ID | Env Var | Agent | Purpose |
|-----|-----|---------|-------|---------|
| @ASI_arifos_bot | 8410138119 | `ASI_ARIFOS_BOT_TOKEN` | Hermes Agent | Conversation, governance, AAA |
| @AGI_ASI_bot | 8149595687 | `TELEGRAM_BOT_TOKEN` | OpenClaw AGI | Machine ops, reasoning, search |
| @arifOS_bot | 8727562763 | `FORGE_BOT_TOKEN` | FORGE/OpenCode | Code, infra, HANDS layer |

## Service → Bot Mapping

| Systemd Unit | Bot Token | Script | Sources From | Port |
|---|---|---|---|---|
| `hermes-asi-gateway.service` | `ASI_ARIFOS_BOT_TOKEN` | `/usr/local/bin/hermes-gateway-secure.sh` | `runtime/.env` | 18001/8644 |
| `openclaw-gateway.service` | `TELEGRAM_BOT_TOKEN` | `/usr/local/bin/openclaw-gateway-secure.sh` | `vault.env` ✅ | 18789 |
| `forge-gateway.service` | `FORGE_BOT_TOKEN` | `/usr/local/bin/forge-gateway.sh` | `~/.forge/.env` | — |
| `opencode-bot.service` | `FORGE_BOT_TOKEN` | `/usr/bin/python3 bot.py` | `vault.flat.env` | — |

## Groups (8 total, all in allowed_chats + free_response)

| ID | Name | Type | Topics |
|---|---|---|---|
| `-1003753855708` | AAA | Group + topics | 36572, 1, 36988, 37092, 36606, 41564, 37069 |
| `-1003815535761` | SADO | Group | — |
| `-1003792478194` | Dear NABILAH | Group | — |
| `-1003768847825` | Kanak-kanak | Group | — |
| `-1003521544074` | 🅰❗️🅰 | Group | — |
| `-1003721331017` | Al AMIN | Group | — |
| `-1004446358629` | arifOS (@arifos999) | Channel | Broadcast only |
| `-5561731065` | BODYBUILDER | Group | — |

## DMs (15 known)

| ID | Name | free_response | Notes |
|---|---|---|---|
| `267378578` | ARIF | ✅ | Sovereign |
| `1042200555` | Syed/Abang Sado | ✅ | SADO trading bot |
| `8003148821` | Koho Pharma | ❌ | |
| `8324190535` | Wawa (Azwa) | ❌ | Adik |
| `6191189810` | Fahmi Amni | ❌ | |
| `8247664885` | Ismax | ❌ | |
| `2049604363` | The Reformation | ❌ | |
| `1117475785` | Summer Bae | ❌ | |
| `8798431893` | Amin Al | ✅ | |
| `8900829116` | AGENT MERDEKA | ❌ | |
| `93372553` | BotFather | ❌ | BotFather |
| `5316953867` | (unknown) | ✅ | Stale? |
| `5250473787` | (unknown) | ✅ | Stale? |
| `6907930063` | ID BOT | ❌ | |
| `52504489` | User Info IDbot | ❌ | |

## Token Source Governance Gap

Only OpenClaw sources its token from `vault.env`. Hermes ASI and FORGE both
source from standalone `.env` files OUTSIDE the vault governance chain:

| Service | Sources From | In vault Governance? | Risk |
|---------|-------------|----------------------|------|
| Hermes ASI | `runtime/.env` | ❌ — independent of vault.env | Token may be stale; backup not centralized |
| FORGE | `~/.forge/.env` | ❌ — outside vault chain | Token may be stale; manual update required |
| OpenClaw | `vault.env` | ✅ | Auto-synced via vault.flat.env |
| OpenCode | `vault.flat.env` | ✅ (derived from vault.env) | Auto-synced |

## Known Gaps (as of 2026-07-26)

1. `-1004446358629` (arifOS channel) — in all allowed_chats but MISSING from `channel_directory.json`
2. `5316953867` — in free_response but no name/context
3. `5250473787` — in free_response but no name/context
4. `runtime/.env` and `~/.forge/.env` — outside vault.env governance chain
5. 107+ old ARIF DM topic entries in channel_directory (historical artifacts)
