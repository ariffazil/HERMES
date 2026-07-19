# Telethon Topic Enumeration — Working Pattern

## Why Telethon

The Telegram Bot API has NO `listForumTopics` / `getForumTopics` endpoint.
The MTProto API (via Telethon) has `GetForumTopicsRequest` which returns ALL topics
with names, IDs, emoji, color, and message counts in one call.

## Requirements

- `TELEGRAM_API_ID` (int) + `TELEGRAM_API_HASH` (string) from https://my.telegram.org
- Bot must be admin in the target group
- `pip install telethon`

**Critical:** Telethon CANNOT authenticate with just a Bot Token. It needs
API_ID + API_HASH even for bot login. If these aren't in the environment,
the script will fail with `ApiIdInvalidError`.

## Working Script

```python
import asyncio, json
from telethon import TelegramClient
from telethon.tl.functions.channels import GetForumTopicsRequest

async def list_topics(api_id, api_hash, bot_token, chat_id):
    client = TelegramClient('bot', api_id=api_id, api_hash=api_hash)
    await client.start(bot_token=bot_token)
    try:
        result = await client(GetForumTopicsRequest(
            channel=chat_id,
            offset_date=None, offset_id=0,
            offset_topic_id=0, limit=100
        ))
        topics = []
        for t in sorted(result.topics, key=lambda x: x.id):
            topics.append({
                'id': t.id, 'title': t.title,
                'icon_color': t.icon_color,
                'icon_emoji': getattr(t, 'icon_emoji', None),
                'top_message': t.top_message,
            })
            print(f"[{t.id:>6}] {getattr(t, 'icon_emoji', '')} \"{t.title}\"")
        with open('/tmp/topics.json', 'w') as f:
            json.dump(topics, f, indent=2)
        print(f"\nTotal: {result.count}, saved {len(topics)}")
        if result.count > 100:
            print(f"  ... {result.count - 100} more (paginate with offset_topic_id)")
    finally:
        await client.disconnect()

asyncio.run(list_topics(API_ID, API_HASH, BOT_TOKEN, -1003753855708))
```

## Pagination

`GetForumTopicsRequest` returns max 100 per call. For groups with >100 topics:
use `offset_topic_id=last_topic_id` and `offset_topic_id` param in subsequent calls.

## Batch Delete Pattern

After listing, delete unwanted topics:

```python
from telethon.tl.functions.channels import DeleteForumTopicRequest
for topic_id in to_delete:
    await client(DeleteForumTopicRequest(channel=chat_id, topic_id=topic_id))
```

Or use Bot API directly (no MTProto needed for delete if you know the thread_id):

```bash
curl -s "https://api.telegram.org/bot${TOKEN}/deleteForumTopic" \
  -d chat_id=<CHAT_ID> -d message_thread_id=<THREAD_ID>
```

## API_ID/API_HASH Discovery

Check these locations (in order):
1. Process env: `cat /proc/<hermes_pid>/environ | tr '\0' '\n' | grep TELEGRAM_API`
2. `.env` files: `/root/.openclaw/.env`, `/root/HERMES/.env`, `/root/.hermes/.env`
3. SOPS-encrypted: `sops -d /root/.openclaw/.env | grep API`
4. Hermes config: `~/.hermes/config.yaml` telegram section

If NONE found → ask user to register at my.telegram.org and provide them.
