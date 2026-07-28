# arifOS Federation — Bot Routing Configuration (2026-07-25)

> Live config snapshot. **Probe before trust** — verify with `ps aux | grep -E 'gateway|bot\.py'` before acting.

## Bot Mapping

| Agent | Bot | Token | Service |
|---|---|---|---|
| **Hermes Agent** | **ASI💃** @ASI_arifos_bot | `8410138119` | `/usr/local/bin/hermes gateway run --replace` (`hermes-asi-gateway.service`) |
| **OpenClaw** | **🦞AGI** @AGI_ASI_bot | `8149595687` | `/usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway` |
| **FORGE/OpenCode** | **🔥FORCE** @arifOS_bot | `8727562763` | `/usr/bin/python3 /root/.openclaw/workspace/bots/opencode-bot/bot.py` |

## Group Coverage

### ASI💃 (Hermes) — 9 Groups + 5 DMs

`require_mention: false` (auto-respond)

| Group ID | Name | Bot |
|---|---|---|
| `-1003753855708` | AAA | ASI💃 + 🦞AGI (guest) + 🔥FORGE (no, DM only) |
| `-1003792478194` | Dear NABILAH | ASI💃 |
| `-1003768847825` | Kanak-kanak | ASI💃 |
| `-1003521544074` | 🅰❗️🅰 | ASI💃 |
| `-1003815535761` | SADO | ASI💃 |
| `-1003721331017` | Al AMIN | ASI💃 |
| `-1004446358629` | arifOS channel | ASI💃 |
| `-5561731065` | BODYBUILDER | ASI💃 |
| `-1003890512851` | makcikGPT | ASI💃 |

| DM ID | Name | Bot |
|---|---|---|
| `267378578` | ARIF (Sovereign) | ASI💃 + 🔥FORGE (tool notifications) |
| `1042200555` | Syed | ASI💃 |
| `5316953867` | Aminol? | ASI💃 |
| `5250473787` | Aminol friend? | ASI💃 |
| `8798431893` | Amin Al | ASI💃 |

### 🦞AGI (OpenClaw) — Guest in AAA only

`allowFrom: ["267378578"]` — only responds to Arif
System prompt: SILENT default, speak on governance/FQ/drift/seal/HOLD signals

### 🔥FORGE (OpenCode) — Arif DM only

Tool notification interface. Not in any group.

## OpenClaw Gateway Config Key Section

```json
{
  "telegram": {
    "enabled": true,
    "dmPolicy": "allowlist",
    "allowFrom": ["267378578"],
    "groupPolicy": "allowlist",
    "groups": {
      "-1003753855708": {}
    },
    "tokenFile": "/root/.secrets/tokens/telegram-agi-asi-bot"
  }
}
```

## Hermes Config Key Section

```yaml
telegram:
  bot_token_env: ASI_ARIFOS_BOT_TOKEN
  bot_username: '@ASI_arifos_bot'
  require_mention: false
  free_response_chats:
    # All 9 groups + 5 DMs listed
```

## 409 Conflict History

**Date:** 2026-07-08
**Cause:** OpenClaw gateway was using ASI💃 token (`8410138119`) alongside Hermes
**Symptom:** Intermittent silence — one gateway would get deauthed by Telegram
**Fix:** Assigned OpenClaw its own token (`8149595687`), updated tokenFile, restarted both gateways
**Tool:** `journalctl -u openclaw | grep Conflict`
