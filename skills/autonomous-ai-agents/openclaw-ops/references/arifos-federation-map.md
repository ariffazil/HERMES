# arifOS Federation — OpenClaw topology (observed 2026-08-05)

## Three-layer Telegram architecture (Arif's stack)

| Layer | Bot | Role | Runtime |
|---|---|---|---|
| SOUL | Hermes `@ASI_arifos_bot` | cognitive / human language | HERMES gateway |
| GUTS | OpenClaw `@AGI_ASI_bot` | metabolizer / process / route | `openclaw-gateway.service` (:18789) |
| HANDS | 777-FORGE `@arifOS_bot` | code / infra / machine ops | `openclaw-bot.service` (Python bot, NOT OpenClaw itself) |

Note: `openclaw-bot.service` is a custom Python Telegram bot (workspace/bots/opencode-bot/bot.py, token `telegram-opencode-bot`) that wraps `opencode run`. Don't confuse it with the OpenClaw gateway's own channel.

## Key paths & units

- Binary: `/root/.npm-global/bin/openclaw` (version 2026.7.1-2)
- Config: `/root/.openclaw/openclaw.json` (mode 600) — top-level keys include `channels`, `gateway`, `agents`, `models`, `plugins`, `mcp`
- Workspace: `/root/.openclaw/workspace` (has its own AGENTS.md pointer to /root/AGENTS.md)
- Env: `/root/.openclaw/.env` (2 lines only) + systemd `EnvironmentFile=/root/.secrets/vault.flat.env`
- Token drop-in: `/etc/systemd/system/openclaw-gateway.service.d/agi-bot-token.conf` → `Environment="TELEGRAM_BOT_TOKEN=8149595687:***"`
- Token files: `/root/.secrets/tokens/telegram-agi-asi-bot` (OpenClaw GUTS), `/root/.secrets/tokens/telegram-opencode-bot` (777-FORGE)
- Units: `openclaw-gateway.service`, `openclaw-bot.service`, `openclaw-restart.path` + `openclaw-restart.service`

## Gateway config shape (telegram channel)

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "${TELEGRAM_BOT_TOKEN}",
      "tokenFile": "/root/.secrets/tokens/telegram-agi-asi-bot",
      "webhookUrl": "https://openclaw.arif-fazil.com/telegram-webhook",
      "webhookSecret": "${TELEGRAM_WEBHOOK_SECRET}",
      "dmPolicy": "allowlist",
      "allowFrom": ["267378578", "1042200555"],
      "groupPolicy": "allowlist",
      "groups": {"-1003753855708": {"groupPolicy": "open", "requireMention": false}},
      "groupAllowFrom": ["267378578", "8410138119"],
      "name": "AGI_ASI_bot",
      "streaming": {"mode": "progress"}
    }
  },
  "gateway": {"port": 18789, "mode": "local", "auth": {"mode": "password", "password": "${OPENCLAW_GATEWAY_PASSWORD}"}}
}
```

Key IDs: Arif = `267378578`. Shared group `-1003753855708` (AAA Home) is where BOTH Hermes and OpenClaw respond — the natural "both agents here" surface.

## Journal signatures (what "working" looks like)

```
[telegram] webhook local listener on http://127.0.0.1:8787/telegram-webhook
[telegram] webhook advertised to telegram on https://openclaw.arif-fazil.com/telegram-webhook
[telegram] Inbound message telegram:267378578 -> @AGI_ASI_bot (direct, 27 chars)
[telegram] outbound send ok accountId=default chatId=267378578 messageId=107380 operation=sendMessage deliveryKind=text threadId=124647 chunkCount=1
```

`openclaw channels status --probe` verdict when healthy:
`Telegram default (AGI_ASI_bot): enabled, configured, running, connected, mode:webhook, bot:@AGI_ASI_bot, token:tokenFile, groups:unmentioned, works, audit ok`

## Known non-blocking warnings (observed)

- `web_search` provider unavailable — brave plugin not installed (`openclaw plugins install @openclaw/brave-plugin` to fix)
- Plugins not installed (harmless unless the feature is needed): acpx, discord, exa, firecrawl, perplexity
- Memory sync fails: `ECONNREFUSED 127.0.0.1:11434` (Ollama down) → L5 memory offline, channel unaffected
- Command menu: 217 commands exceeds Telegram limit → OpenClaw trims to 71; `/status /model /think /mcp` conflict with native commands (expected noise)

## Bridge option (if user wants OpenClaw in a Hermes thread)

Gateway is WebSocket-based on :18789 with password auth; HTTP REST probes 404. Outbound sends via `openclaw message send --channel telegram --message "…" --reply-to <id>`. Full bidirectional bridge = relay Hermes ↔ gateway — build only on explicit request (it's a build decision, not a default).
