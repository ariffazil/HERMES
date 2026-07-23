# Telegram Channel Three-System Wiring

Recipe for wiring a new Telegram channel across all three arifOS federation systems:
Hermes, OpenClaw, and 777-FORGE (OpenCode bot). Proven 2026-07-23 with @arifos999 (`-1004446358629`).

## Pre-flight: Verify bot admin status

Channel = broadcast only. Bot MUST be admin. Check before touching any config:

```bash
source /root/.secrets/vault.flat.env

# Which bot? Check all three
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getChatAdministrators" \
  -d "chat_id=<CHANNEL_ID>" | python3 -c "
import json,sys; r=json.load(sys.stdin)
if r.get('ok'):
    for a in r['result']:
        u = a['user']; print(f'  @{u.get(\"username\",\"?\")} id={u[\"id\"]} is_bot={u.get(\"is_bot\")} role={a[\"status\"]}')
else:
    print(f'NOT in channel: {r.get(\"description\",r)}')
"
```

If bot not admin, Arif must add it in Telegram (Channel → Add Member → grant admin).

## Step 1: Hermes config

```python
import yaml

CHANNEL_ID = "-1004446358629"

with open('/root/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)

t = cfg.setdefault('telegram', {})
for key in ['allowed_chats', 'free_response_chats']:
    val = t.get(key, [])
    if isinstance(val, str):  # fix YAML-as-JSON pitfall
        val = json.loads(val)
    if CHANNEL_ID not in val:
        val.append(CHANNEL_ID)
    t[key] = val

with open('/root/.hermes/config.yaml', 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
```

Restart: `hermes gateway restart`

## Step 2: OpenClaw config

```python
import json

CHANNEL_ID = "-1004446358629"

with open('/root/.openclaw/openclaw.json') as f:
    oc = json.load(f)

# Add to groups dict
groups = oc['channels']['telegram']['groups']
if CHANNEL_ID not in groups:
    groups[CHANNEL_ID] = {}

# Add binding (peer.kind MUST be "channel", not "group")
existing_ids = {
    b['match'].get('peer', {}).get('id')
    for b in oc.get('bindings', [])
}
if CHANNEL_ID not in existing_ids:
    oc['bindings'].append({
        'agentId': 'main',
        'match': {
            'channel': 'telegram',
            'peer': {'kind': 'channel', 'id': CHANNEL_ID}
        }
    })

with open('/root/.openclaw/openclaw.json', 'w') as f:
    json.dump(oc, f, indent=2)
```

Restart: `systemctl restart openclaw-gateway.service`

## Step 3: 777-FORGE (OpenCode) bot

Bot: `@arifOS_bot` (id 8727562763), token at `/root/.secrets/tokens/telegram-opencode-bot`
Code: `/root/.openclaw/workspace/bots/opencode-bot/bot.py`
Service: `opencode-bot.service`

### 3a: Check if bot is already admin

```bash
FORGE_TOKEN=$(cat /root/.secrets/tokens/telegram-opencode-bot)
curl -s "https://api.telegram.org/bot${FORGE_TOKEN}/getChatAdministrators" \
  -d "chat_id=<CHANNEL_ID>"
```

If `chat not found`, Arif must add @arifOS_bot to channel first.

### 3b: Patch bot.py

Add after `AAA_GROUP_ID`:

```python
ARIFOS_CHANNEL_ID = -1004446358629  # @arifos999 — federation broadcast channel
ALLOWED_CHAT_IDS: set[int] = {
    AAA_GROUP_ID,
    ARIFOS_CHANNEL_ID,
}
```

Add after `_reply_filtered()`:

```python
async def post_to_channel(application, text: str) -> bool:
    """Post a message to the arifOS broadcast channel (@arifos999).
    Bot must be admin of the channel. Add @arifOS_bot via Telegram first.
    """
    try:
        await application.bot.send_message(
            chat_id=ARIFOS_CHANNEL_ID,
            text=text[:REPLY_CHAR_CAP],
        )
        log.info(f"CHANNEL POST: {len(text)} chars to {ARIFOS_CHANNEL_ID}")
        return True
    except Exception as e:
        log.error(f"CHANNEL POST FAILED: {e}")
        return False
```

### 3c: Restart

```bash
systemctl restart opencode-bot.service && systemctl is-active opencode-bot.service
```

## Step 4: Verify

```bash
source /root/.secrets/vault.flat.env

# Test via @ASI_arifos_bot (Hermes/OpenClaw)
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=<CHANNEL_ID>" -d "text=🔗 Channel wired" | python3 -c \
  "import json,sys; r=json.load(sys.stdin); print('✅' if r.get('ok') else f'❌ {r.get(\"description\")}')"

# Test via @arifOS_bot (777-FORGE) — only AFTER bot added as admin
FORGE_TOKEN=$(cat /root/.secrets/tokens/telegram-opencode-bot)
curl -s -X POST "https://api.telegram.org/bot${FORGE_TOKEN}/sendMessage" \
  -d "chat_id=<CHANNEL_ID>" -d "text=🔨 777-FORGE channel ready" | python3 -c \
  "import json,sys; r=json.load(sys.stdin); print('✅' if r.get('ok') else f'❌ {r.get(\"description\")}')"
```

## Pitfalls

1. **`peer.kind` must be `"channel"` not `"group"`** in OpenClaw bindings
2. **`hermes send` won't work** — uses `TELEGRAM_BOT_TOKEN`, not `ASI_ARIFOS_BOT_TOKEN`. Use curl instead.
3. **777-FORGE is polling-based** — no webhook. Bot must be admin + bot.py patched + service restarted.
4. **Channel is one-way** — don't waste time configuring `unmentionedInbound` or `free_response_chats` behavior. They don't apply.
