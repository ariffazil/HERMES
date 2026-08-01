---
name: telegram-webhook-recovery
description: "Diagnose and fix broken Telegram bot webhooks — 502 Bad Gateway, 401 Unauthorized, pending update backlogs, and gateway restart procedures. Covers the full diagnostic flow from symptom to resolution."
triggers:
  - "telegram bot not responding"
  - "webhook broken"
  - "webhook 502"
  - "webhook 401"
  - "pending updates"
  - "bot not receiving messages"
  - "getWebhookInfo"
  - "telegram not working"
---

# Telegram Webhook Recovery

## Philosophy

When a Telegram bot stops receiving messages, the webhook is the first suspect. The diagnostic flow is deterministic: error code → root cause → fix. Don't guess — the Telegram API tells you exactly what's broken.

## Diagnostic Flow

```
Bot silent? → getWebhookInfo → check error/last_error_message
├── "502 Bad Gateway"      → Gateway/upstream down → restart + verify ports
├── "401 Unauthorized"     → Missing secret_token → re-register WITH secret
├── url=""                 → Webhook unset → setWebhook
├── pending_updates > 0    → Backlog draining (healthy) or stuck (check error)
└── No error, pending=0    → Webhook OK; problem is elsewhere
```

## Step-by-Step Recovery

### Step 1: Get Webhook State

```bash
source /root/.secrets/vault.env && curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo" | python3 -c "
import sys,json
d=json.load(sys.stdin)
r=d['result']
print(f'url={r[\"url\"]}')
print(f'pending={r[\"pending_update_count\"]}')
print(f'error={r.get(\"last_error_message\",\"none\")}')
print(f'last_error_date={r.get(\"last_error_date\",\"none\")}')
print(f'secret_ok={r.get(\"has_custom_certificate\",\"?\")}')
"
```

### Step 2: Diagnose Error Code

| Error | Root Cause | Fix |
|-------|-----------|-----|
| `502 Bad Gateway` | Gateway/upstream process not running | Restart OpenClaw gateway; verify ports :8787 + :18789 |
| `401 Unauthorized` | Webhook registered WITHOUT `secret_token` | Delete + re-set WITH `secret_token=$TELEGRAM_WEBHOOK_SECRET` |
| `url=""` | Webhook never set or deleted | Call `setWebhook` |
| `pending_updates` growing + 401/502 | Dead webhook; Telegram retrying | Fix error, then pending drains automatically |

### Step 3a: Fix 502 — Gateway Down

```bash
# Check listeners
ss -tlnp | grep -E "18789|8787"

# If no listeners: restart gateway
# Check which process starts it (may be masked in systemd)
systemctl is-active openclaw-gateway  # may be "masked" or "inactive"

# If masked, start directly:
cd /root/.openclaw && nohup /usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway > /var/log/openclaw-gateway.log 2>&1 &

# Wait for ports to come up (can take 10-15s)
sleep 10 && ss -tlnp | grep -E "18789|8787"
```

### Step 3b: Fix 401 — Missing Secret Token

**This is the most common and most subtle error.** The webhook URL was set correctly, but without the `secret_token` parameter. The OpenClaw gateway validates the `X-Telegram-Bot-Api-Secret-Token` header from Telegram — if the webhook was registered without a secret, this header is missing, and the gateway returns 401.

```bash
source /root/.secrets/vault.env

# 1. Delete the broken webhook
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/deleteWebhook"

# 2. Re-register WITH secret_token
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"https://openclaw.arif-fazil.com/telegram-webhook\",\"secret_token\":\"${TELEGRAM_WEBHOOK_SECRET}\",\"max_connections\":100}"

# 3. Verify: pending should start draining immediately
sleep 5 && curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo" | python3 -c "
import sys,json; r=json.load(sys.stdin)['result']
print(f'pending={r[\"pending_update_count\"]} error={r.get(\"last_error_message\",\"none\")}')
"
```

### Step 4: Verify Recovery

After fixing, the pending count should drop. 30+ pending can drain in under a minute.

```bash
# Watch pending count drop
for i in 1 2 3; do
  sleep 5
  curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['pending_update_count'])"
done
```

## Bot Token Mapping

| Token | Bot | Port | Purpose |
|-------|-----|------|---------|
| `TELEGRAM_BOT_TOKEN` | @AGI_ASI_bot | :8787 → Caddy | OpenClaw gateway |
| `ASI_BOT_TOKEN` | @ASI_arifos_bot | :8787 → Caddy | Hermes/ASI main bot |
| `FORGE_BOT_TOKEN` | @arifOS_bot | varies | FORGE/OpenCode |

Webhook URL pattern: `https://openclaw.arif-fazil.com/telegram-webhook`
Caddy routes this to `127.0.0.1:8787` (webhook receiver).

## Gateway Log Inspection

When diagnosing, check the gateway log for webhook registration and inbound activity:

```bash
# Recent gateway activity
tail -50 /var/log/openclaw-gateway.log | grep -iE "webhook|telegram|error|401|unauth"

# Webhook registration confirmation
grep "webhook" /var/log/openclaw-gateway.log | tail -5
```

Healthy log shows:
- `[telegram] webhook local listener on http://127.0.0.1:8787/telegram-webhook`
- `[telegram] webhook advertised to telegram on https://openclaw.arif-fazil.com/telegram-webhook`
- `[telegram] outbound send ok` (outbound messages working)

## Pitfalls

- **Gateway restart wipes secret_token.** When the OpenClaw gateway restarts, it may re-register the webhook WITHOUT the secret_token. Always verify `getWebhookInfo` after a gateway restart — if 401 appears, re-run Step 3b. The gateway log shows it "advertises" the webhook but doesn't confirm whether secret_token was included. **Proven 2026-07-31:** Gateway was down (502), restarted manually, then webhook showed 401 because re-registration missed the secret.

- **Don't confuse 200 on :18789 with webhook health.** Port 18789 is the main gateway (HTTP 200 on GET /). Port 8787 is the webhook receiver (POST /telegram-webhook only). The webhook receiver returns 401 on direct curl (expected — no HMAC), but the Telegram API error tells you the real status.

- **`deleteWebhook` then `setWebhook` is the canonical reset.** Don't just call `setWebhook` again with the same URL — it may not update the secret_token. Always delete first, then set fresh.

- **Pending > 0 with no last_error is healthy.** Telegram batches updates. Pending count draining means the webhook is working. Only intervene when pending is growing AND last_error is set.

- **secret_token is stored in vault.env as `TELEGRAM_WEBHOOK_SECRET`.** Always source vault.env before running webhook commands. If `$TELEGRAM_WEBHOOK_SECRET` is empty, the 401 will persist.

## Caddy Context

The Caddy route:
```
handle /telegram-webhook {
    reverse_proxy 127.0.0.1:8787
}
```

## Related Skills

- `hermes-cron-rhythm` — heartbeat jobs that may detect webhook failures
- `agentic-infrastructure-ops` — self-healing VPS patterns
- `well-operations` — WELL organ diagnostics (separate from webhook)
