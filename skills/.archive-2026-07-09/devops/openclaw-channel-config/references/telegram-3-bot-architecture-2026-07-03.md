# Telegram 3-Bot Architecture — Verified 2026-07-03

## Bot Map

| Bot | Username | Token Env Var | Token Prefix | Process | Delivery |
|-----|----------|---------------|-------------|---------|----------|
| ASI💃 | @ASI_arifos_bot | ASI_BOT_TOKEN = HERMES_TELEGRAM_BOT_TOKEN | 84101... | hermes-asi-gateway.service | Hermes internal |
| AGI🦞 | @AGI_ASI_bot | TELEGRAM_BOT_TOKEN | 81495... | openclaw-gateway.service | Webhook → :8787 |
| 777 FORGE🔥 | @arifOS_bot | FORGE_BOT_TOKEN = TELEGRAM_OPENCODE_BOT_TOKEN | 87275... | opencode-bot.service | Polling |

**All tokens unique.** Verified via SHA256 hash comparison (2026-07-03).

## Token Aliases

- `ASI_BOT_TOKEN` = `HERMES_TELEGRAM_BOT_TOKEN` (same token, two env var names)
- `FORGE_BOT_TOKEN` = `TELEGRAM_OPENCODE_BOT_TOKEN` (same token, two env var names)
- `ASI_BOT_TOKEN_LEGACY` = deprecated, unused

## Service → Token Mapping

All services source `/root/.secrets/vault.flat.env` (which has ALL tokens), but each service uses a DIFFERENT token:

- **hermes-asi-gateway**: reads `HERMES_TELEGRAM_BOT_TOKEN` → @ASI_arifos_bot
- **openclaw-gateway**: reads `TELEGRAM_BOT_TOKEN` → @AGI_ASI_bot (via webhook)
- **opencode-bot**: reads from file `/root/.secrets/tokens/telegram-opencode-bot` → @arifOS_bot (NOT from env)

## opencode-bot Token Loading

The `bot.py` uses `TOKEN_PATH=Path("/root/.secrets/tokens/telegram-opencode-bot")` — reads from file, NOT from env. If the file is missing, it `sys.exit(1)` with no fallback. This means:
- `TELEGRAM_BOT_TOKEN` in the process env (from vault.flat.env) is NOT used
- `TELEGRAM_OPENCODE_BOT_TOKEN` in the process env is NOT used
- Only the file content matters

## AAA Group

- Group ID: `-1003753855708`
- All 3 bots are members
- Each bot responds independently on its own token
- No token competition (different tokens, different processes)

## Webhook Architecture

```
Telegram → openclaw.arif-fazil.com/telegram-webhook
  → Caddy (reverse_proxy) → 127.0.0.1:8787/telegram-webhook
  → OpenClaw gateway webhook listener (Node, PID 1617702)
```

**Critical:** Webhook listener is on port 8787, NOT 18789. Caddy must proxy to 8787.

## Mention Rules (2026-07-03)

- **Arif (267378578):** No @mention needed. All 3 bots respond to his messages in AAA.
- **Agent-to-agent:** Must @mention each other. @AGI_ASI_bot only responds to messages matching `mentionPatterns` regex.
- **Implementation:**
  - OpenClaw: `groupAllowFrom: ["267378578"]` + `mentionPatterns: ["@AGI_ASI_bot"]`
  - Hermes: `require_mention: true` + `free_response_chats: ["267378578"]`
  - 777-FORGE: `should_respond_in_group()` checks `ALLOWED_USER_ID` bypass
