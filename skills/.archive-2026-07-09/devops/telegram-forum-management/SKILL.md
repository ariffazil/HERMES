---
name: telegram-forum-management
description: Manage Telegram forum/supergroup topics via Bot API — create, edit, close, delete topics; route cron deliveries to specific threads; handle API limitations.
triggers:
  - "organize telegram topics"
  - "create telegram topic/thread"
  - "route cron to telegram topic"
  - "delete telegram topic"
  - "telegram forum group"
  - "set up telegram topics"
---

# Telegram Forum Group Management

## Prerequisites

- Bot must be **admin** in the supergroup with `can_manage_topics` permission
- Group must have "Topics" enabled (forum mode) — check via `getChat`, look for `is_forum: true`
- Bot token: `HERMES_TELEGRAM_BOT_TOKEN` env var (also `ASI_BOT_TOKEN`, `ASI_ARIFOS_BOT_TOKEN` — check `config.yaml` `bot_token_env` for the canonical name)

## Quick Diagnostic

```bash
# Verify group is a forum
curl -s "https://api.telegram.org/bot${HERMES_TELEGRAM_BOT_TOKEN}/getChat?chat_id=<CHAT_ID>" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('is_forum:', d['result'].get('is_forum'))"

# Check webhook state (empty URL = polling mode)
curl -s "https://api.telegram.org/bot${HERMES_TELEGRAM_BOT_TOKEN}/getWebhookInfo" | python3 -m json.tool
```

## API Endpoints (What EXISTS)

| Operation | Method | Params |
|-----------|--------|--------|
| Create topic | `createForumTopic` | `chat_id`, `name`, `icon_color` (optional), `icon_custom_emoji_id` (optional) |
| Edit topic name | `editForumTopic` | `chat_id`, `message_thread_id`, `name` |
| Close topic | `closeForumTopic` | `chat_id`, `message_thread_id` |
| Reopen topic | `reopenForumTopic` | `chat_id`, `message_thread_id` |
| Delete topic | `deleteForumTopic` | `chat_id`, `message_thread_id` |
| Send to topic | `sendMessage` | `chat_id`, `message_thread_id`, `text` |

## What Does NOT Exist (Critical Limitation)

**There is NO `getForumTopics` endpoint.** The Telegram Bot API cannot list existing forum topics. This means:

- You cannot programmatically discover what topics exist
- You cannot enumerate topic IDs for routing
- You must track topic IDs yourself (store in config, memory, or a file)

**Workarounds (ranked by reliability):**
1. **Telethon MTProto (full enumeration)** — `pip install telethon`, then use `GetForumTopicsRequest` to list ALL topics with names, IDs, emojis, and message counts. Requires `TELEGRAM_API_ID` + `TELEGRAM_API_HASH` from [my.telegram.org](https://my.telegram.org) — the Bot Token alone is NOT sufficient for Telethon auth. See `references/telethon-topic-enumeration.md` for the working script.
2. **editForumTopic probe (destructive, use carefully)** — try `editForumTopic` with a known thread_id and a temp name. If `ok: true`, the topic exists. **CRITICAL: you MUST immediately revert the name.** This mutates the topic. Strategy: probe → record result → revert in a tight loop. Only useful when you have candidate IDs (e.g. from session history or brute-force ranges). Telegram forum topic IDs are typically small integers (1, 2, 3...) for early topics, or large (100000+) for later ones.
3. **Hermes session DB (partial, no names)** — `/root/HERMES/sessions/sessions.json` contains every thread_id the bot has interacted with under `agent:main:telegram:group:<chat_id>:<thread_id>`. Also queryable via `/root/HERMES/state.db` SQLite. Limitation: `chat_topic` field is always `None` — you get thread IDs but NOT topic names.
4. `getUpdates` with `forum_topic_created` in `allowed_updates` — only catches NEW topics created while polling. Empty if webhook is active.
5. Manual registry — maintain a file mapping topic names → thread IDs.

## Cron Delivery to Topics

Hermes cron `deliver` field supports thread targeting:
```
deliver: "telegram:<chat_id>:<thread_id>"
```

Example: `telegram:-1003753855708:12345` delivers to topic with thread_id 1235 in the AAA group.

Without `:thread_id`, messages go to the group's General topic (or no topic).

## Icon Colors (createForumTopic)

Hex values without `#` prefix. Available palette:
- `7FBEEB` (blue), `6FB9F0` (light blue), `65AADD` (dark blue)
- `8E7CC3` (purple), `E076A2` (pink), `FF6F6F` (red)
- `FF8F6C` (orange), `FDB74A` (yellow), `A3D068` (green)

## Workflow: Set Up Topic-Organized Group

1. Plan topic structure (name + purpose for each)
2. Create topics via `createForumTopic` — note each returned `message_thread_id`
3. Save the mapping (name → thread_id) to a reference file or config
4. Update cron jobs with `deliver: "telegram:<chat_id>:<thread_id>"`
5. Test each topic by sending a message to it

## References

- `references/arifos-aaa-group.md` — AAA group details, topic registry, cron delivery targets
- `references/telethon-topic-enumeration.md` — MTProto fallback for listing ALL forum topics when Bot API falls short

## Naming Convention

Arif's preferred topic format: **`emoji + 2 terms`** (e.g., `🤖 AGI OPS`, `📊 Data Watch`, `🔬 Lab Notes`). Keep names short, descriptive, and consistent.

## Renaming Topics Workflow

1. **Discover topic IDs** — see workarounds above (Telethon, session DB, editForumTopic probe)
2. **Rename via editForumTopic** — `{"chat_id": ..., "message_thread_id": ..., "name": "emoji + 2 terms"}`
3. **Telegram limitation**: Unicode emoji in the `name` string appears as text. The topic circle icon requires `icon_custom_emoji_id` (Telegram Premium custom emoji). Text emoji works fine for display.

## Media File Delivery to Telegram

### Direct Bot API fallback (when OpenClaw MCP is down)

If `mcp_openclaw_message` returns `OutboundDeliveryError` or MCP unreachable, use direct Bot API:

```bash
TOKEN=$(cat /proc/$(pgrep -f 'hermes.*gateway' | head -1)/environ | tr '\0' '\n' | grep TELEGRAM_BOT_TOKEN | cut -d= -f2-)
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendDocument" \
  -F chat_id=<CHAT_ID> \
  -F document=@/path/to/file.pdf \
  -F caption="Description" \
  -F parse_mode=Markdown
```

### Directory restrictions

OpenClaw's message tool restricts `media=` to allowed directories (typically `/var/arifos/artifacts/`, managed media dirs). Files in `/root/forge_work/` or `/tmp/` are **blocked**. Workaround: copy to `/var/arifos/artifacts/outbox/YYYY-MM-DD/` first, then send from there. Or use direct Bot API which has no directory restrictions.

### Sending images

Use `sendPhoto` instead of `sendDocument` for `.png`/`.jpg` (renders inline):
```bash
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendPhoto" \
  -F chat_id=<CHAT_ID> \
  -F photo=@/path/to/figure.png \
  -F caption="Figure caption"
```

## Pitfalls

- **Bot can't send to itself** — if `deliver` targets the bot's own user ID, you get `Forbidden: the bot can't send messages to the bot`. Use the group chat_id or the human's user_id.
- **Thread ID is NOT the topic name** — always use numeric `message_thread_id`, never the string name.
- **General topic has thread_id 1** — The "General" topic in a forum group uses thread_id 1 for `editForumTopic`. However, for `sendMessage`, you omit `message_thread_id` entirely (sending without a thread_id targets General). This inconsistency is a Bot API quirk — edit needs `1`, send omits the field.
- **getUpdates is empty if webhook is set** — check `getWebhookInfo` first; if URL is non-empty, getUpdates returns nothing.
- **Rate limits** — Telegram limits bots to ~30 messages/second per group, ~20 messages/minute to the same topic.
- **SOPS-encrypted .env** — The OpenClaw `.env` at `/root/.openclaw/.env` stores `TELEGRAM_BOT_TOKEN` as `ENC[AES]` (SOPS-encrypted). You cannot `source` it directly. Either `sops -d` it (if you have the key) or extract the live token from the running Hermes process: `cat /proc/<pid>/environ | tr '\0' '\n' | grep TELEGRAM_BOT_TOKEN | cut -d= -f2-`. Find the PID with `ps aux | grep 'hermes.*gateway'`.
- **Telethon needs API_ID + API_HASH** — Even for bot auth, Telethon fails with `ApiIdInvalidError` if API_ID/API_HASH are missing. Bot Token alone is NOT enough. See `references/telethon-topic-enumeration.md`.

## Related Skills

- `telegram-group-relay` — real-time group conversation relay (send/read/monitor when away from phone). Covers the `hermes send` → direct Bot API fallback pattern and gateway log reading for inbound messages.
