---
name: hermes-telegram-group-setup
description: >
  Add new Telegram groups and users to Hermes Agent config — allowed_chats,
  free_response_chats, bot_token_env. Covers the hermes config set YAML-as-JSON
  pitfall, group migration to supergroups, and bot_token_env mismatch.
  USE WHEN: "add group to bot", "allow this chat", "bot not replying in group",
  "new Telegram group", "add user to bot", "make bot work in group",
  "group migrated to supergroup".
---

# Hermes Telegram Group Setup

Adding a new Telegram group, channel, or user to the Hermes bot requires config changes
to THREE fields and a gateway restart. Miss any step = bot silent.

**Channels:** Channels use the same `allowed_chats`/`free_response_chats` mechanism.
They're one-way broadcast — `free_response_chats` doesn't change behavior but should
be populated for consistency. For full multi-system channel wiring (Hermes + OpenClaw +
777-FORGE), see `openclaw-channel-config` skill → `references/telegram-channel-three-system-wiring.md`.

## The Three Fields

| Field | What | Format |
|---|---|---|
| `telegram.allowed_chats` | Chat IDs the bot will process | YAML list of strings |
| `telegram.free_response_chats` | Chat IDs where bot responds without @mention | YAML list of strings |
| `telegram.bot_token_env` | Env var name holding the bot token | String |

## Step-by-Step

### 1. Get the chat/user IDs

From Telegram, the user sends `/start` to the bot. The gateway logs show the chat ID.
Or use: `hermes send --list telegram` to see known targets.

Group IDs are negative (e.g., `-5316953867`). User IDs are positive (e.g., `5316953867`).

### 2. Add to config

```bash
# Use hermes config set for each field
hermes config set telegram.allowed_chats '["-1003753855708", "-NEW_GROUP_ID"]'
hermes config set telegram.free_response_chats '["existing...", "NEW_USER_ID"]'
```

### 3. CRITICAL: Fix the YAML-as-JSON pitfall

`hermes config set` serializes lists as JSON strings, NOT YAML lists.
After setting, the config will contain:

```yaml
allowed_chats: '["-100...", "-NEW"]'  # ← WRONG: JSON string, not YAML list
```

The gateway can't parse this. Fix with Python:

```python
import yaml
with open('/root/.hermes/config.yaml') as f:
    data = yaml.safe_load(f)

# Fix allowed_chats
import json
ac = data['telegram']['allowed_chats']
if isinstance(ac, str):
    data['telegram']['allowed_chats'] = json.loads(ac)

# Same for free_response_chats
frc = data['telegram']['free_response_chats']
if isinstance(frc, str):
    data['telegram']['free_response_chats'] = json.loads(frc)

with open('/root/.hermes/config.yaml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
```

### 4. Check bot_token_env

If `hermes send` fails with "You must pass the token you received from BotFather",
the `bot_token_env` doesn't match your actual env var name.

```bash
# Check what's in .env
grep -i bot /root/.hermes/.env

# If the var is ASI_ARIFOS_BOT_TOKEN but config says TELEGRAM_BOT_TOKEN:
hermes config set telegram.bot_token_env ASI_ARIFOS_BOT_TOKEN
```

### 5. Restart gateway

```bash
hermes gateway restart
```

If you're INSIDE the gateway (running as Hermes), you can't restart from within.
Use: `kill -HUP $(pgrep -f "hermes gateway" | head -1)` for config reload,
or SSH from outside.

### 6. Test

Always verify the token controls the expected bot before testing routing:

```bash
set -a
source /root/.secrets/vault.env 2>/dev/null
set +a
python3 - <<'PY'
import json
import os
import urllib.request

token = os.environ.get("TELEGRAM_BOT_TOKEN")
if not token:
    raise SystemExit("TELEGRAM_BOT_TOKEN is unset")

with urllib.request.urlopen(
    f"https://api.telegram.org/bot{token}/getMe", timeout=5
) as response:
    result = json.load(response)["result"]
print(f"✅ @{result['username']}")
PY
```

If the bot returned is not what you expect, see `references/telegram-bot-token-verification.md` — duplicate env var definitions can shadow the intended token.

```bash
# Direct curl is the ground truth (bypasses token name mismatch):
source /root/.secrets/vault.flat.env
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=<CHAT_ID>" -d "text=Test" | python3 -c \
  "import json,sys; r=json.load(sys.stdin); print('✅' if r.get('ok') else f'❌ {r.get(\"description\")}')"

# If using hermes send, you must export the right token name:
export TELEGRAM_BOT_TOKEN="$ASI_ARIFOS_BOT_TOKEN"
hermes send -t telegram:-NEW_GROUP_ID "Test message"
```

## Pitfall: `hermes send` token mismatch

`hermes send` reads `TELEGRAM_BOT_TOKEN` from the environment directly — it does NOT
resolve `bot_token_env` from `config.yaml`. If your env has `ASI_ARIFOS_BOT_TOKEN`
(not `TELEGRAM_BOT_TOKEN`), the CLI fails with "You must pass the token."

**Fix:** Either export the mapping (`export TELEGRAM_BOT_TOKEN="$ASI_ARIFOS_BOT_TOKEN"`)
or use direct Telegram API curl (preferred — always works, bypasses both gateways).

## Pitfall: Group Migrated to Supergroup

When a Telegram group becomes a supergroup, the chat ID changes.
The bot will get: `Group migrated to supergroup. New chat id: -100XXXXXXXXXX`

**Fix:** Replace the old group ID with the new one in BOTH `allowed_chats`
and `free_response_chats`.

## Pitfall: allowed_chats vs free_response_chats

- `allowed_chats`: bot PROCESSES messages from these chats
- `free_response_chats`: bot responds WITHOUT needing @mention

A group in `allowed_chats` but NOT in `free_response_chats` will only respond
when users @mention the bot. For natural conversation, add to BOTH.

## Pitfall: User IDs in allowed_chats

`allowed_chats` is for CHAT IDs (groups, channels). User IDs belong in
`free_response_chats` only. Putting user IDs in `allowed_chats` won't break
anything but is semantically wrong.

## Pitfall: Cron job delivering to bot's own ID (bot-to-bot spam)

When a cron job is created in a session where the origin is the bot itself, the job's `deliver: "origin"` resolves to the bot's own Telegram ID. Since Telegram forbids bots from messaging themselves, every delivery attempt fails with `Forbidden: the bot can't send messages to the bot`.

**Symptoms:** Every N minutes: `live adapter send failed: Forbidden: the bot can't send messages to the bot; live adapter delivery to telegram:8410138119 failed`

**Diagnosis:**
```bash
python3 -c "
import json
with open('/root/.hermes/cron/jobs.json') as f:
    data = json.load(f)
for j in data.get('jobs', []):
    err = str(j.get('last_delivery_error', ''))
    if 'bot' in err.lower():
        print(f'JOB: {j.get(\"id\")} — {j.get(\"name\")}')
        print(f'  deliver: {j.get(\"deliver\")}')
        print(f'  enabled: {j.get(\"enabled\")}')
"
```

**Fix:** Pause the job by setting `enabled: false` in jobs.json, or change its `deliver` target to a valid channel like the AAA group or Arif's DM. **Proven 2026-07-24** — `arifs24-telemetry` job was delivering to bot ID 8410138119 every 10 minutes.

## Pitfall: Live Location Spam Loop

When a Telegram user shares **live location** in a group, Telegram sends location
updates every few seconds. Each update hits `_handle_location_message` in the
adapter, which converts it to text and routes to the LLM. If the group has
`free_response` enabled, the bot responds to EVERY location ping → response
flood → Telegram rate limits → interrupt-chain → crash loop.

**Symptoms:** "⚡ Interrupting current task" spam, "📍🫡" repeated responses,
gateway crash loop with "Too many requests" (429 flood control).

**Root cause:** Telegram live-location API doesn't distinguish between one-shot
pins and continuous updates. Both arrive as `filters.LOCATION` messages.

**Fix:** Add rate-limiting to `_handle_location_message` in the installed
adapter at `/usr/local/lib/hermes-agent/plugins/platforms/telegram/adapter.py`:

```python
# Add class-level rate limit tracker (place before the method)
_last_location_ts: dict[tuple[int, int], float] = {}
_LOCATION_RATE_LIMIT_SECS = 60  # max one response per minute per user per chat

# At the top of _handle_location_message method body (after msg validation):
chat_id = getattr(getattr(msg, "chat", None), "id", 0)
user_id = getattr(getattr(msg, "from_user", None), "id", 0)
import time as _time
now = _time.monotonic()
key = (chat_id, user_id)
last = self._last_location_ts.get(key, 0)
if now - last < self._LOCATION_RATE_LIMIT_SECS:
    logger.debug(...)
    return
self._last_location_ts[key] = now
```

**After patching:** Requires gateway restart (`hermes gateway restart` from
outside the gateway). One-shot location pins still work. Continuous live-location
updates are silently rate-limited.

**Proven 2026-07-21:** User "No name" in SADO group shared live location for
hours. ~146 location messages processed before patch. After patch: stopped.

**Note:** This patch lives in the installed venv copy, not the source repo.
It will be overwritten on `hermes update`. The patch should be re-applied
ahead of updates until upstream adds built-in rate-limiting.

## Pitfall: Systemd Drop-In Token Mismatch

OpenClaw's token can be hardcoded in a **systemd drop-in** at `/etc/systemd/system/openclaw-gateway.service.d/`. This shadows whatever vault.env carries because systemd drop-ins are applied *after* EnvironmentFile:

```ini
# /etc/systemd/system/openclaw-gateway.service.d/agi-bot-token.conf
[Service]
Environment="TELEGRAM_BOT_TOKEN=8149595687:REDACTED"   # ← dead/stale token
```

Even if vault.env has the right token (e.g., `8410138119:VALID`), the systemd drop-in wins. The service runs with the wrong token silently — neither `journalctl` nor `systemctl status` shows a warning.

**Detection — check the running process, not vault.env:**
```bash
# Live process env and API identity (ground truth; token is never printed)
pid="$(systemctl show openclaw-gateway.service -p MainPID --value)"
PID="$pid" python3 - <<'PY'
import json
import os
import urllib.request
from pathlib import Path

pid = os.environ["PID"]
entries = Path(f"/proc/{pid}/environ").read_bytes().split(b"\0")
process_env = dict(item.split(b"=", 1) for item in entries if b"=" in item)
token = process_env.get(b"TELEGRAM_BOT_TOKEN")
if not token:
    raise SystemExit("TELEGRAM_BOT_TOKEN is absent from the running process")

with urllib.request.urlopen(
    f"https://api.telegram.org/bot{token.decode()}/getMe", timeout=5
) as response:
    result = json.load(response)["result"]
print(f"✅ running token controls @{result['username']}")
PY

# Presence-only drop-in check; never print the assignment
if grep -ql 'TELEGRAM_BOT_TOKEN=' /etc/systemd/system/openclaw-gateway.service.d/*.conf; then
  echo "TELEGRAM_BOT_TOKEN override is present"
else
  echo "No TELEGRAM_BOT_TOKEN override found"
fi

# The Python probe above verifies the effective running token via Telegram API.
```

**Fix:**
```bash
sed -i 's/<OLD_TOKEN_ID>:/<NEW_TOKEN_ID>:/g' \
  /etc/systemd/system/openclaw-gateway.service.d/agi-bot-token.conf
systemctl daemon-reload
systemctl restart openclaw-gateway.service
```

**Pitfall: daemon-reload is mandatory.** Editing the drop-in file without `systemctl daemon-reload` keeps the cached stale version. The file on disk changes but the running service never picks it up. Verified 2026-07-23.

## Pitfall: Duplicate Env Var Definitions in vault.env

`vault.env` can have **multiple lines defining the same env var**. Example found in production:

```
export TELEGRAM_BOT_TOKEN="8410138119:VALID"      # line 139
export TELEGRAM_BOT_TOKEN="8410138119:VALID"      # line 140 (duplicate)
export TELEGRAM_BOT_TOKEN=8149595687:REDACTED      # line 377 (dead)
```

**Behaviour:** Bash `source` resolves to the **last definition** — the redacted one shadows the valid ones. Meanwhile `grep` shows all matches, making it look like the token is fine.

**Diagnosis:** After sourcing, always verify via the Telegram API:

```bash
source /root/.secrets/vault.env 2>/dev/null
# Verify the token controls the right bot
curl -sf -m 5 "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe" \
  | python3 -c "import sys,json; r=json.load(sys.stdin); print(f'@{r[\"result\"][\"username\"]}')"
```

**Fix:** Remove duplicate lines and restore any redacted tokens from backup (`vault.flat.env.bak-*`).

## Bot Profile Photo Management

### setMyProfilePhoto (Bot API 10.x)

The `setMyProfilePhoto` endpoint allows programmatic profile photo changes. It requires an `InputProfilePhotoStatic` JSON object with `attach://` file reference in multipart format:

```python
import requests, json

with open("/tmp/bot_photo.jpg", "rb") as photo:
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/setMyProfilePhoto",
        data={"photo": json.dumps({"type": "static", "photo": "attach://myfile"})},
        files={"myfile": ("logo.jpg", photo, "image/jpeg")},
        timeout=15
    )
# → {"ok": true, "result": true}
```

### Common format mistakes

- **Wrong method name**: `setMyPhoto` → 404. Use `setMyProfilePhoto`.
- **Wrong file format**: `-F "photo=@file"` → `"photo isn't specified"`. Must use JSON `{"type": "static", "photo": "attach://myfile"}` + multipart file.
- **Wrong JSON key**: `{"type": "static"}` without `"photo"` key → `"can't find field 'photo'"`.
- **Mismatched attach key**: `attach://myfile` in JSON must match the key in `files=` dict.

### Remove profile photo

```bash
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/removeMyProfilePhoto"
```

### @BotFather fallback

If the bot's API version doesn't support `setMyProfilePhoto`:
1. Open @BotFather
2. Send `/setuserpic`
3. Select the bot
4. Upload the image (square, 512x512 recommended, PNG/JPEG)

### Reference file

See `references/telegram-bot-token-verification.md` for:
- Full three-bot architecture mapping (Hermes/OpenClaw/Forge)
- Token verification workflow with API probes
- Redacted token detection and recovery from backups
- Profile photo management (check, download, **setMyPhoto 404 pitfall**, @BotFather fallback)
- Webhook health diagnosis (502 vs 401)
- Comprehensive pitfalls for multi-bot identity management

## Webhook Debugging

When a Telegram bot responds to `getMe` but doesn't receive messages, the issue is
usually the webhook, not the token.

### 502 vs 401 — Critical Distinction

| Error | What it means | Action |
|-------|--------------|--------|
| **401 Unauthorized** (on `getMe`) | Token is invalid/revoked | Regenerate from @BotFather, update env files |
| **502 Bad Gateway** (in webhook) | Gateway process is running but rejecting the connection | Check Caddy proxy → gateway process → port binding |
| **404 Not Found** (on `setMyProfilePhoto`) | Wrong method name — use `setMyProfilePhoto` not `setMyPhoto` | Check endpoint name and JSON format |

### Webhook Diagnosis Flow

```bash
# 1. Verify token is valid
curl -sf -m 5 "https://api.telegram.org/bot${TOKEN}/getMe"

# 2. Check webhook status from Telegram's perspective
curl -sf -m 5 "https://api.telegram.org/bot${TOKEN}/getWebhookInfo" \
  | python3 -c "
import sys,json
d = json.load(sys.stdin)['result']
print(f'URL: {d.get(\"url\")}')
print(f'Pending: {d.get(\"pending_update_count\")}')
print(f'Last error: {d.get(\"last_error_message\")}')
print(f'Max connections: {d.get(\"max_connections\")}')
"

# 3. Check local gateway process and port
ps aux | grep -i openclaw | grep -v grep
ss -tlnp | grep <PORT>

# 4. Check reverse proxy (Caddy) config
grep -A10 '<domain>' /etc/caddy/Caddyfile
```

### Common Webhook Pitfalls

- **Webhook error is a lagging indicator**: Telegram reports the LAST error, which could
  be from hours ago. The current state may be healthy. Check `pending_update_count` — if 0,
  the webhook is likely working now.
- **Gateway restart clears webhook state**: After a restart, `last_error_message` may still
  show the old error until the next Telegram inbound. This is not a live defect.
- **Caddy reverse proxy must point to the correct local port**: Verify the `handle` block
  in Caddyfile matches the gateway's listening port.
- **Gateway webhook secret** (if configured): Some gateways require a `TELEGRAM_WEBHOOK_SECRET`
  in requests. A missing or wrong secret returns `unauthorized` from the gateway, not Telegram.

## Reference: Telegram Bot Token Verification

See `references/telegram-bot-token-verification.md` for:
- Full three-bot architecture mapping (Hermes/OpenClaw/Forge)
- Token verification workflow with API probes
- Redacted token detection and recovery from backups
- Profile photo management (check, download, set via API, 404 pitfall)
- Webhook health diagnosis
- Comprehensive pitfalls for multi-bot identity management
