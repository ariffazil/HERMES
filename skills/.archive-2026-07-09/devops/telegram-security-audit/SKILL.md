---
name: telegram-security-audit
description: >
  Automated TREE777 security checks for Telegram bot tokens, webhook isolation,
  bot permission scope, and A2A bridge security. USE WHEN: "telegram audit",
  "bot security", "webhook check", "token isolation", "TREE777 check",
  "telegram permissions".
---

# Telegram Security Audit (TREE777)

**Automated Telegram bot security checks — token isolation, webhook exposure, permission scope.**

## TREE777 Protocol Checks

### T1 — Token Isolation
```bash
# Check if bot tokens are properly isolated from other services
# arifOS_bot token should be in openclaw.json only
# @ASI_arifos_bot token should be in hermes-agent env only
# They should NEVER appear in git-tracked files

# Scan for leaked tokens
grep -r "tg\|telegram\|bot" /root/.openclaw/openclaw.json 2>/dev/null | grep -i token | wc -l
grep -r "tg\|telegram" /root/AAA/ 2>/dev/null | grep -i token | wc -l
grep -r "tg\|telegram" /root/arifOS/ 2>/dev/null | grep -i token | wc -l
```

### T2 — Webhook Exposure
```bash
# Check webhook is NOT publicly exposed without auth
# Webhook URL: https://openclaw.arif-fazil.com/webhook/telegram
# Local listener: http://127.0.0.1:8787/telegram-webhook

# Verify webhook has bot-specific token
curl -s "https://api.telegram.org/bot$(cat /root/.openclaw/tg_token 2>/dev/null)/getWebhookInfo" \
  | jq '{url: .result.url, has_custom_certificate: .result.has_custom_certificate}'

# Check local webhook is NOT port-forwarded
ss -tlnp | grep 8787
```

### T3 — Bot Permissions
```bash
# Audit bot permission scope — least privilege
BOT_TOKEN=$(cat /root/.openclaw/tg_token 2>/dev/null)
curl -s "https://api.telegram.org/bot$BOT_TOKEN/getMe" | jq '{username: .result.username, can_join_groups: .result.can_join_groups, can_read_all_group_messages: .result.can_read_all_group_messages, supports_inline_queries: .result.supports_inline_queries}'

# Check group membership
curl -s "https://api.telegram.org/bot$BOT_TOKEN/getChat?chat_id=-1003753855708" | jq '.result.username'
```

### T4 — A2A Bridge Security
```bash
# hermes-a2a.py bridge — verify token isolation
# Bridge token: aaa-a2a-token-dev
# Should only be accessible from localhost:18001

ss -tlnp | grep 18001
curl -s -o /dev/null -w "%{http_code}" http://localhost:18001/.well-known/agent-card.json

# Verify a2a token NOT exposed externally
curl -s https://openclaw.arif-fazil.com:18001 2>/dev/null | head -c 50
```

### T5 — Bot Separation
```bash
# @AGI_ASI_bot (OPENCLAW) vs @ASI_arifos_bot (Hermes)
# Should be separate processes, separate tokens, separate contexts
ps aux | grep -E "hermes|openclaw|telegram" | grep -v grep
```

### T6 — Log Exposure
```bash
# Check logs don't contain plaintext tokens
grep -r "67[0-9]" /root/.openclaw/logs/ 2>/dev/null | grep -i token | wc -l
grep -r "bot[0-9]" /root/.openclaw/logs/ 2>/dev/null | grep -i token | wc -l
```

### T7 — Rate Limiting
```bash
# Verify Telegram rate limits are respected
# @AGI_ASI_bot: mention-triggered only
# @ASI_arifos_bot: ambient polling

# Check for 429 errors in logs
grep -r "429\|Too Many Requests" /root/.openclaw/logs/ 2>/dev/null | tail -5
```

## TREE777 Report

```
TREE777 TELEGRAM SECURITY AUDIT
═══════════════════════════════════════
Time: YYYY-MM-DD HH:MM UTC

✅/❌ T1 Token Isolation
  - openclaw.json tokens: N found (should be 0 in git)
  - hermes env tokens: N found
  - AAA repo tokens: N found (should be 0)

✅/❌ T2 Webhook Exposure
  - Local webhook on 127.0.0.1: ✅/❌
  - Public port 8787 exposed: ✅/❌
  - Webhook has auth: ✅/❌

✅/❌ T3 Bot Permissions
  - can_join_groups: YES (⚠️ check if needed)
  - can_read_all_group_messages: YES (⚠️ privacy)
  - supports_inline_queries: YES/NO

✅/❌ T4 A2A Bridge
  - Port 18001 localhost only: ✅/❌
  - a2a token not external: ✅/❌

✅/❌ T5 Bot Separation
  - Separate PIDs: ✅/❌
  - Separate tokens: ✅/❌

✅/❌ T6 Log Exposure
  - Plaintext tokens in logs: N found

✅/❌ T7 Rate Limits
  - 429 errors: N found

OVERALL: ✅ PASS | ⚠️ WARNINGS | ❌ FAIL
═══════════════════════════════════════
```
