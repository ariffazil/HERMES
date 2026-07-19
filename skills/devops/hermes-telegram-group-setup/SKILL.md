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

Adding a new Telegram group or user to the Hermes bot requires config changes
to THREE fields and a gateway restart. Miss any step = bot silent.

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
export TELEGRAM_BOT_TOKEN="$ASI_ARIFOS_BOT_TOKEN"
hermes send -t telegram:-NEW_GROUP_ID "Test message"
```

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
