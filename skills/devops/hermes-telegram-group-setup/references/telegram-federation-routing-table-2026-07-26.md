# Telegram Federation Routing Table — Settled 2026-07-26

> Canonical mapping for the 3-bot × 9-group × 5-DM arifOS Telegram architecture.
> Sealed operational config — not a design doc. Update only on Arif's explicit F13 directive.

## Bot Inventory

| Bot | Username | Token Env | Service | Identity |
|-----|----------|-----------|---------|----------|
| **ASI💃** | `@ASI_arifos_bot` | `ASI_ARIFOS_BOT_TOKEN` (8410138119) | `hermes-asi-gateway.service` | Hermes Agent (aku) |
| **🦞AGI** | `@AGI_ASI_bot` | `TELEGRAM_BOT_TOKEN` (8149595687) | OpenClaw Node.js gateway | OpenClaw (dia) |
| **🔥FORGE** | `@arifOS_bot` | `FORGE_BOT_TOKEN` (8727562763) | `opencode-bot.service` | OpenCode tool interface |

## Routing Policy

| Bot | Coverage | require_mention | Surface Type |
|-----|----------|-----------------|--------------|
| **ASI💃** | **9 groups + 5 DMs** | ❌ No (auto-respond) | Conversational + broadcast |
| **🦞AGI** | **AAA only** | N/A (allowlist) | AAA conversational |
| **🔥FORGE** | **Arif DM only** | N/A | Tool notifications |

## Group Chat Coverage

| Chat ID | Nama | ASI💃 | 🦞AGI | 🔥FORGE | Type |
|---------|------|-------|-------|---------|------|
| `-1003753855708` | AAA | ✅ | ✅ | ❌ | Group + topics |
| `-1003792478194` | Dear NABILAH | ✅ | ❌ | ❌ | Group |
| `-1003768847825` | Kanak-kanak | ✅ | ❌ | ❌ | Group |
| `-1003521544074` | 🅰❗️🅰 | ✅ | ❌ | ❌ | Group |
| `-1003815535761` | SADO | ✅ | ❌ | ❌ | Group + topics |
| `-1003721331017` | Al AMIN | ✅ | ❌ | ❌ | Group |
| `-1004446358629` | arifOS | ✅ | ❌ | ❌ | Channel (@arifos999) |
| `-5561731065` | BODYBUILDER | ✅ | ❌ | ❌ | Group |
| `-1003890512851` | makcikGPT | ✅ | ❌ | ❌ | Group |

## Personal DM Coverage

| User ID | Nama | Bot |
|---------|------|-----|
| `267378578` | ARIF (Sovereign) | ASI💃 + 🦞AGI |
| `1042200555` | Syed / Abang Sado | ASI💃 |
| `5316953867` | Aminol? | ASI💃 |
| `5250473787` | Aminol friend? | ASI💃 |
| `8798431893` | Amin Al | ASI💃 |

## EUREKA Plane Mapping

| Surface | EUREKA Plane | Who Talks | Who Listens |
|---------|-------------|-----------|-------------|
| **AAA group** | P3 Intelligence + P4 Execution | ASI💃 + 🦞AGI | 🔥FORGE passive |
| **Other groups (8)** | P3 Intelligence | ASI💃 sahaja | — |
| **arifOS channel** | P6 Truth (broadcast) | ASI💃 post only | Humans read |
| **Arif DM** | P1 Sovereign | ASI💃 + 🦞AGI + 🔥FORGE | Arif |

## Conflict Prevention Rules

1. **Identity hard boundary** — every bot has unique token + unique process. No token sharing. Verified via `ps aux` + `grep vault.env` + Telegram `getMe`.
2. **Surface boundary** — channel ≠ group. Channel is broadcast only (post, don't respond).
3. **Message loop prevention** — Telegram API blocks bot-to-bot message visibility by default. No additional filtering needed.
4. **AAA is the convergence point** — only place where ASI + AGI coexist. ASI handles routing; AGI handles deep reasoning; FORGE handles tool notifications (Arif DM only for now).

## Config Locations

- Hermes allowed_chats + free_response: `/root/.hermes/config.yaml` lines 895-928
- Vault tokens: `/root/.secrets/vault.env` (3 token vars)
- OpenClaw group allowlist: `/root/.openclaw/openclaw.json`
- Channel registry: `/root/HERMES/channel_directory.json`

## History

- 2026-07-25: Identity verified via triple cross-check after 409 Conflict history
- 2026-07-26: All groups identified and labeled. makcikGPT added. Final routing settled.
