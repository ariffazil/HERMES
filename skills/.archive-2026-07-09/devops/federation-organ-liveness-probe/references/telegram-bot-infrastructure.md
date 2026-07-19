# Telegram Bot Infrastructure — arifOS Federation

> **Verified 2026-07-04** via `/proc/<PID>/environ` + `getMe` API against running processes. **Refreshed 2026-07-05** — corrected token-to-process mapping (bot.py reads from file not env var, OpenClaw uses webhook not polling), added webhook diagnostic and SHA256 comparison technique. **Updated 2026-07-03** — added webhook port fix (8787), AAA mention rules, 000-999 command alignment, terminal redaction trap.

## The Three Bots

| # | Env Var(s) | Bot Handle | Bot ID | Display Name | Gateway Process | Delivery |
|---|---|---|---|---|---|---|
| 1 | `TELEGRAM_BOT_TOKEN` | `@AGI_ASI_bot` | 8149595687 | AGI🦞 | OpenClaw gateway (Node.js, :18789) | **Webhook** → `:8787` |
| 2 | `ASI_BOT_TOKEN` = `HERMES_TELEGRAM_BOT_TOKEN` | `@ASI_arifos_bot` | 8410138119 | ASI💃 | Hermes gateway (Python) | Hermes internal |
| 3 | `TELEGRAM_OPENCODE_BOT_TOKEN` = `FORGE_BOT_TOKEN` | `@arifOS_bot` | 8727562763 | 777 FORGE 🔥🧠⚒️🌎💎 | OpenCode bot.py (Python) | **Polling** |

**Key fact:** `ASI_BOT_TOKEN` and `HERMES_TELEGRAM_BOT_TOKEN` are the SAME token (identical SHA256). `FORGE_BOT_TOKEN` and `TELEGRAM_OPENCODE_BOT_TOKEN` are also the same.

## Webhook Listener Port (Critical)

The OpenClaw gateway webhook listener runs on port **8787**, NOT the main gateway port 18789.

```
Telegram POST → openclaw.arif-fazil.com/telegram-webhook
  → Caddy reverse_proxy → 127.0.0.1:8787/telegram-webhook (webhook listener)
```

**Caddy config must route to 8787:**
```
openclaw.arif-fazil.com {
    handle /telegram-webhook {
        reverse_proxy 127.0.0.1:8787
    }
    handle {
        reverse_proxy 127.0.0.1:18789
    }
}
```

**If Caddy proxies to 18789:** The main gateway serves HTML (200), not the webhook handler. Telegram sees "Wrong response: 404 Not Found". Updates silently queue (pending_update_count rises) then drop.

**Verification:**
```bash
# Webhook listener (correct)
curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:8787/telegram-webhook
# Expected: 401 (secret token check)

# Main gateway (wrong for webhooks)
curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:18789/telegram-webhook
# Expected: 404 or HTML
```

**After fixing Caddy, re-register webhook:**
```bash
source /root/.secrets/vault.flat.env
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  --data-urlencode "url=https://openclaw.arif-fazil.com/telegram-webhook" \
  --data-urlencode "secret_token=${TELEGRAM_WEBHOOK_SECRET}" \
  --data-urlencode 'allowed_updates=["message","edited_message","callback_query","message_reaction"]'
```

## AAA Group Mention Rules (Multi-bot pattern)

AAA group chat_id: `-1003753855708`

**Goal:** Arif talks freely (no @mention). Agents must @mention each other.

**OpenClaw config (`openclaw.json`):**
```json
{
  "channels": {
    "telegram": {
      "groupAllowFrom": ["267378578"],
      "groups": {"-1003753855708": {}}
    }
  },
  "messages": {
    "groupChat": {
      "mentionPatterns": ["@AGI_ASI_bot", "@AGI_ASI_bot\\b"]
    }
  }
}
```

**Hermes config (`~/.hermes/config.yaml`):**
```yaml
telegram:
  require_mention: true
  free_response_chats: ["267378578"]
```

**777-FORGE (`bot.py`):** `should_respond_in_group()` checks `ALLOWED_USER_ID` bypass + @mention patterns.

## 000-999 Reality Loop Commands

| Cmd | Stage | Meaning |
|-----|-------|---------|
| `/000` | INIT | Reset session, fresh identity boot |
| `/111` | OBSERVE | MCP tools, scan, discover |
| `/222` | THINK | Reason, plan, critique |
| `/333` | ROUTE | Organ status, routing |
| `/444` | ACT | Execute action (governed) |
| `/555` | VERIFY | Reality check, GEOX anchor |
| `/666` | HEART | Risk, ethics, critique |
| `/777` | FORGE | Build, deploy, code |
| `/888` | JUDGE | Verdict, seal, hold |
| `/999` | VAULT | Receipt, seal, memory |

Plus: `/status`, `/model`, `/image`, `/email`

Both OpenClaw (`customCommands` in openclaw.json) and777-FORGE (`COMMANDS` list + `CommandHandler` in bot.py) register these.

## How to Verify Bot Identity

```bash
source /root/.secrets/vault.flat.env 2>/dev/null
for var in ASI_BOT_TOKEN TELEGRAM_BOT_TOKEN FORGE_BOT_TOKEN; do
  val=$(printenv "$var" 2>/dev/null)
  [ -n "$val" ] && curl -s "https://api.telegram.org/bot${val}/getMe" | jq -r ".result | \"@\(.username) (\(.first_name)) ← $var\""
done
```

## Token-to-Process Mapping

All three processes inherit ALL token env vars from shared `vault.flat.env`. The **code** determines which token is used:

| Process | Token Source | Delivery |
|---|---|---|
| OpenClaw gateway (Node.js) | `TELEGRAM_BOT_TOKEN` env var | Webhook → `:8787` |
| Hermes gateway (Python) | `HERMES_TELEGRAM_BOT_TOKEN` env var | Hermes internal |
| OpenCode bot.py (Python) | File `/root/.secrets/tokens/telegram-opencode-bot` (NOT env var) | Polling |

## Pitfalls

1. **Terminal redaction trap.** The terminal tool redacts paths/strings containing "token", "secret", "key". A TOKEN_PATH showing as `"...ot"` is NOT broken — it's redacted. Verify with Python exec, not terminal display.

2. **Don't trust docstrings for bot handle mapping.** Only `getMe` is authoritative.

3. **All processes inherit all tokens.** Seeing TELEGRAM_BOT_TOKEN in opencode-bot's `/proc/<pid>/environ` does NOT mean it uses that token. The bot.py reads from TOKEN_PATH file, not env vars.

4. **Webhook ≠ polling.** OpenClaw uses webhook (port 8787). Don't assume polling conflict when webhook routing is broken.

5. **SHA256 comparison for token uniqueness:**
   ```bash
   for var in ASI_BOT_TOKEN TELEGRAM_BOT_TOKEN FORGE_BOT_TOKEN; do
     val=$(printenv "$var" 2>/dev/null)
     [ -n "$val" ] && echo "$var sha256=$(echo -n "$val" | sha256sum | cut -c1-8)"
   done
   ```
