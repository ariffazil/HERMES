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
after updates until upstream adds built-in rate-limiting.
