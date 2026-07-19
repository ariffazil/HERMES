# editForumTopic Probing Strategy

## Purpose
Discover existing forum topic IDs when Telethon is unavailable (no API_ID/API_HASH).

## How It Works
The Bot API has NO `getForumTopics`. But `editForumTopic` returns:
- `ok: true` — topic exists and was edited
- `ok: false` with error — topic doesn't exist or bot lacks permission

By trying `editForumTopic` with candidate thread_ids, you can detect which topics exist.

## CRITICAL WARNING
**This MUTATES the topic name.** You MUST revert immediately after each probe.

## Working Pattern (bash)

```bash
BOT_TOKEN="$HERMES_TELEGRAM_BOT_TOKEN"
CHAT_ID="-1003753855708"

for tid in 1 2 3 100 108109; do
  result=$(curl -s "https://api.telegram.org/bot${BOT_TOKEN}/editForumTopic" \
    -H "Content-Type: application/json" \
    -d "{\"chat_id\": $CHAT_ID, \"message_thread_id\": $tid, \"name\": \"PROBE\"}")
  ok=$(echo "$result" | python3 -c "import sys,json; print(json.load(sys.stdin).get('ok', False))")
  if [ "$ok" = "True" ]; then
    echo "FOUND: Thread $tid"
    # REVERT IMMEDIATELY
    curl -s "https://api.telegram.org/bot${BOT_TOKEN}/editForumTopic" \
      -H "Content-Type: application/json" \
      -d "{\"chat_id\": $CHAT_ID, \"message_thread_id\": $tid, \"name\": \"General\"}" >/dev/null 2>&1
  fi
done
```

## ID Range Patterns
- General topic: thread_id = 1
- Early topics: small integers (1-100)
- Later topics: large numbers (100000+, 108000+)
- No predictable pattern — brute force is the only option

## Limitations
- Mutates topic names (must revert)
- Rate-limited by Telegram (~30 req/s per group)
- Can't discover the original name — only that the topic exists
- If bot isn't admin with `can_manage_topics`, all probes return false

## Better Alternative
Use Telethon with `GetForumTopicsRequest` if API_ID/API_HASH are available.
See `telethon-topic-enumeration.md` for the working script.
