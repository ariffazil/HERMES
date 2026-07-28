---
name: hermes-log-forensics
description: "When session_search misses messages or sessions, raw gateway logs are the authoritative fallback"
version: 1.0.0
author: Hermes-Prime
metadata:
  hermes:
    tags: [debugging, forensics, session-search, gateway-logs, investigation]
    related_skills: [systematic-debugging, agent-memory-bridge]
---

# Hermes Log Forensics

## When to Use

- `session_search` returns empty but user (or evidence) confirms messages exist
- User says "I saw them text the bot" or "that happened" but session DB has nothing
- Investigating whether a specific user ever contacted the bot
- Sovereign asks "how often does X message me?" — frequency/activity audit
- Sovereign asks "who are my most active users?" — ranking by channel
- Reconstructing a conversation that predates session DB indexing
- Audit trail for DM activity, group messages, or cron deliveries

## The Core Problem

`session_search` queries the **session SQLite DB** (FTS5-indexed). This DB can lose entries when:
- OpenClaw crash-looped (741 restarts observed 2026-07-16) — sessions corrupted or never written
- Gateway restarted mid-message — inbound logged but session never persisted
- Session cache eviction — idle sessions evicted, messages only in raw logs
- First-boot or migration events — DB schema changed, old entries dropped

**Raw gateway logs are append-only and survive DB corruption.**

## Authoritative Log Locations

```
/root/.hermes/logs/gateway.log        # Current gateway log
/root/.hermes/logs/gateway.log.1      # Rotated (older)
/root/.hermes/logs/gateway.log.2      # Rotated (older still)
/root/.hermes/logs/agent.log          # Current agent log
/root/.hermes/logs/agent.log.1        # Rotated
/root/.hermes/logs/agent.log.2        # Rotated
/root/.hermes/logs/errors.log         # Errors only
```

Logs rotate. `gateway.log` is newest, `.log.1` is previous, etc. Always search ALL rotated files.

## Search Patterns

### Find all inbound messages from a specific user (by chat ID)
```bash
grep "inbound.*chat=<CHAT_ID>" /root/.hermes/logs/gateway.log* /root/.hermes/logs/agent.log* 2>/dev/null | sort | uniq
```

### Find all inbound messages in a specific group
```bash
grep "chat=<GROUP_ID>.*inbound" /root/.hermes/logs/gateway.log* /root/.hermes/logs/agent.log* 2>/dev/null | sort | uniq
```

### Find bot responses to a user
```bash
grep "<CHAT_ID>" /root/.hermes/logs/gateway.log* /root/.hermes/logs/agent.log* 2>/dev/null | grep -i "response\|sending\|flushing" | sort | uniq
```

### Find cron deliveries to a destination
```bash
grep "delivered to.*<DESTINATION>" /root/.hermes/logs/gateway.log* /root/.hermes/logs/agent.log* 2>/dev/null | sort | uniq
```

### Find all activity for a Telegram username
```bash
grep -ri "<username>" /root/.hermes/logs/ --include="*.log*" 2>/dev/null | sort | uniq
```

### Count total messages from a user
```bash
grep "inbound.*chat=<CHAT_ID>" /root/.hermes/logs/gateway.log* /root/.hermes/logs/agent.log* 2>/dev/null | sort | uniq | wc -l
```

## Log Format Reference

### Inbound message
```
INFO gateway.run: inbound message: platform=telegram user=<NAME> chat=<ID> msg='<TEXT>' reply_to_id=<ID> reply_to_text='<TEXT>'
```

### Bot response
```
INFO gateway.run: response ready: platform=telegram chat=<ID> time=<SECONDS>s api_calls=<N> response=<N> chars
INFO gateway.platforms.base: [Telegram] Sending response (<N> chars) to <ID>
```

### Session flush (bot sending to group)
```
INFO hermes_plugins.telegram_platform.adapter: [Telegram] Flushing text batch <SESSION_KEY> (<N> chars)
INFO hermes_plugins.telegram_platform.adapter: [Telegram] Flushing photo batch <SESSION_KEY>:photo-burst with <N> image(s)
```

### Cron delivery
```
INFO cron.scheduler: Job '<JOB_ID>': delivered to telegram:<ID> via live adapter
```

### Session eviction
```
INFO gateway.run: Agent cache idle-TTL evict: session=<SESSION_KEY> (idle=<SECONDS>s)
```

## Case Study: Syed's Missing DMs (2026-07-16)

**User claim:** "I saw him live text the bot"
**session_search result:** Empty — 0 sessions from user 1042200555
**Raw log result:** 40 inbound DM messages across Jul 3, 13, 14, 15

Root cause: OpenClaw crash-looped 741 times. Session DB entries for Syed's DMs were never persisted or were corrupted. Raw gateway logs (append-only) survived.

Key grep that found them:
```bash
grep "inbound.*1042200555" /root/.hermes/logs/agent.log* /root/.hermes/logs/gateway.log* 2>/dev/null | sort | uniq
```

## Pitfalls

1. **Only checking current log file.** Always search `*.log*` (all rotations).
2. **Trusting session_search as exhaustive.** It's a secondary index, not the source of truth.
3. **Not sorting/uniqing.** Rotated logs can overlap at boundaries.
4. **Searching by username only.** Telegram usernames can change. Chat IDs are stable. Search both.
5. **Assuming "no session = no contact."** The session DB is lossy. Logs are authoritative.
6. **Confidently asserting absence from session_search alone.** NEVER say "no, they never contacted the bot" based solely on session_search returning empty. The session DB is a lossy index. Raw logs are the source of truth. If a human witness (especially the sovereign) says "I saw it happen," that overrides session_search. Check raw logs before asserting absence. Saying "no" confidently and being wrong is worse than saying "let me verify."
7. **Searching only DM logs.** A user may interact in GROUPS, not DMs. Search both `chat=<USER_ID>` (DM) AND group activity where the user's session key contains their ID (e.g., `group:<GROUP_ID>:<USER_ID>`).
8. **session_search matches name mentions, not just that user's messages.** A query like `session_search("Izzu")` returns sessions where "Izzu" appears in the assistant's own response too — not just messages FROM Izzu. This creates false positives for "did X message the bot?" Always cross-check against the `user=` field in raw gateway logs before concluding someone messaged.
9. **Log parser truncates display names at first space.** The gateway log's `user=` field stops at the first space. So "🦞 AGI" becomes `user=🦞`, "777 FORGE 🔥🧠" becomes `user=777`, "No name" becomes `user=No`. Cross-reference `chat=<ID>` against `sessions.json` to resolve full names. See `references/telegram-identity-map.md` for this federation's known identities.
10. **Use sessions.json to resolve chat IDs to names.** When you have a Telegram chat ID from a log line: `grep -A10 '"chat_id": "<ID>"' /root/.hermes/sessions/sessions.json` shows the `display_name` field. This resolves "who is user=al at chat 1024343313" without guessing from truncated log names.

## Gateway Restart Loop Diagnosis

When the gateway appears to be restarting or crash-looping, check logs in this order:

### 1. Identify the restart pattern
```bash
grep -E "Starting Hermes Gateway|Gateway stopped|SIGTERM|SIGKILL|Stopping gateway" /root/.hermes/logs/gateway.log | tail -40
```

### 2. Check for shutdown crash triggers
The `Event loop is closed` RuntimeError during shutdown (exit code 75/TEMPFAIL) is a known arifOS pattern — the MCP tool's `_wait_for_reconnect_or_shutdown` races with event loop teardown. This causes systemd to restart the gateway on a loop. Look for:
```bash
grep -A5 "Event loop is closed" /root/.hermes/logs/gateway.log
```

### 3. Check systemd unit timeout mismatch
The gateway logs `Stale systemd unit detected` when `TimeoutStopSec` in the running systemd unit doesn't match the gateway's `drain_timeout`. The fix is a daemon-reload (not a unit file edit — the file is often already correct):
```bash
systemctl show hermes-asi-gateway.service -p TimeoutStopUSec  # check current
systemctl daemon-reload                                        # reload unit files
systemctl show hermes-asi-gateway.service -p TimeoutStopUSec  # verify (should show 3min 30s = 210s)
```

### 4. Check for overlapping gateway instances
```bash
ps aux | grep "hermes.*gateway" | grep -v grep
```
Multiple gateway processes (especially with different session storage paths like `/root/HERMES/sessions` vs `/root/.hermes/sessions`) indicate two systemd units or two instances fighting. The `--replace` flag on the current process means it's replacing a previous instance.

### 5. Verify stability
```bash
systemctl status hermes-asi-gateway.service
ps -o etime= -p <PID>  # check uptime
```

### 6. Check for recurring bot-to-bot delivery errors
The `Forbidden: the bot can't send messages to the bot` error at regular intervals (e.g., every 10 minutes) is a cron job delivering to the bot's own Telegram ID. Not a crash trigger, but clutters logs. See `hermes-cron-rhythm` skill for the fix pattern (check `~/.hermes/cron/jobs.json` `last_delivery_error` field).

## User Activity & Frequency Analysis

When the sovereign asks "how often does X message me?" — go beyond "yes they exist." Reconstruct frequency, channel preference, and behavioral pattern.

### Step 0: Verify the user has actually messaged (not just been mentioned)

**Critical distinction:** `session_search("Izzu")` returns sessions where "Izzu" appears ANYWHERE — including the ASSISTANT's own response mentioning the name, or other users' messages that talk about them. This means session_search can return **false positives** for the question "did X message the bot?" FTS5 indexes every word in every message, not just the `user=` sender field.

**Definitive check — enumerate every unique sender from raw gateway logs:**

```bash
# ALL Telegram senders ever (across all rotations)
cat /root/.hermes/logs/gateway.log* 2>/dev/null \
  | grep "inbound message.*platform=telegram" \
  | grep -oP 'user=[^ ]+' | sort -u
```

If the user's name does not appear in any `user=` field of an `inbound message:` line, they have **never sent a message to the bot**. Every mention of their name in session_search is either (a) another user talking about them, or (b) an assistant response to someone else.

**Group vs DM breakdown:**
```bash
# See every unique sender+destination combo
cat /root/.hermes/logs/gateway.log* 2>/dev/null \
  | grep "inbound message.*platform=telegram" \
  | grep -oP 'user=[^ ]+ chat=[^ ]+' | sort -u
```

DM chats are positive integers (the user's Telegram ID). Group chats start with `-`.

**Sweep all non-sovereign users (strip agent and self traffic):**
```bash
cat /root/.hermes/logs/gateway.log* 2>/dev/null \
  | grep "inbound message.*platform=telegram" \
  | grep -v "user=ARIF" | grep -v "user=🦞" | grep -v "user=FORGE" | grep -v "user=777" \
  | grep -oP 'user=[^ ]+' | sort -u | grep -v '^user=$'
```

This strips ARIF's own messages plus agent-to-agent traffic, leaving only real human users.

**Warning — truncated display names:** The log parser truncates Telegram names at the first space. `"🦞 AGI"` becomes `user=🦞`, `"777 FORGE 🔥🧠"` becomes `user=777`, `"No name"` becomes `user=No`. Cross-reference with `chat=<ID>` against `sessions.json` to resolve real names.

### Step 1: Count total inbound messages per user

```bash
grep "inbound message.*chat=<CHAT_ID>" /root/.hermes/logs/gateway.log* 2>/dev/null | sort -u | wc -l
```

Exclude your own test sends if you sent them from the user's chat (user=ARIF in the log line but chat=<OTHER_USER_ID>).

### Step 2: Break down by channel

DM is `chat=<USER_ID>` (no minus sign). Group is `chat=<GROUP_ID>` (starts with `-`).

```bash
# DM only
grep "inbound message.*chat=<USER_ID>" /root/.hermes/logs/gateway.log | grep -v "chat=-"
# AIA group specifically
grep "group:-1003521544074:<USER_ID>" /root/.hermes/logs/gateway.log | grep "Flushing text batch\|inbound"
```

Note: On Jul 27-29, the gateway.log pattern showed that DM inbound messages are logged as `chat=<USER_ID>` directly. Group messages may appear as `Flushing text batch agent:main:telegram:group:<GROUP_ID>:<USER_ID>` in the logs without a corresponding `inbound message:` line — count these as group messages too.

### Step 3: Break down by day

```bash
for day in $(seq -w 1 31); do
  count=$(grep "inbound message.*chat=<CHAT_ID>" /root/.hermes/logs/gateway.log* 2>/dev/null | grep "2026-07-$day" | wc -l)
  [ "$count" -gt 0 ] && echo "July $day: $count messages"
done
```

**Quick overview: active dates** (which days the user messaged):
```bash
cat /root/.hermes/logs/gateway.log* 2>/dev/null \
  | grep "inbound message.*chat=<CHAT_ID>" \
  | grep -oP '^[0-9-]+' | sort -u
```

For multiple days on month boundaries, adjust July → August etc.

### Step 3.5: User ranking (who are the most active people?)

When the sovereign asks "who are my most active users?" — rank all non-sovereign, non-agent human users:

```bash
cat /root/.hermes/logs/gateway.log* 2>/dev/null \
  | grep "inbound message.*platform=telegram" \
  | grep -v "user=ARIF" | grep -v "user=🦞" | grep -v "user=FORGE" | grep -v "user=777" \
  | grep -v "user=AGI" \
  | grep -oP 'user=[^ ]+' | sort | uniq -c | sort -rn
```

This outputs: `count userName`. To also get their chat ID for DM vs group breakdown:

```bash
cat /root/.hermes/logs/gateway.log* 2>/dev/null \
  | grep "inbound message.*platform=telegram" \
  | grep -v "user=ARIF" | grep -v "user=🦞" | grep -v "user=FORGE" | grep -v "user=777" \
  | grep -v "user=AGI" \
  | grep -oP 'user=[^ ]+ chat=[^ ]+' | sort | uniq -c | sort -rn
```

Present as a ranked table:

```markdown
| Rank | User (display name) | Total Msgs | DM / Group | Active Since | Pattern |
|---|---|---|---|---|---|
| 🥇 | Syed (No name, chat 1042200555) | 964 | DM + Group | 3 Jul | Heavy daily |
| 🥈 | Izzu (Mohd, chat 1237635275) | 18 | 13 DM + 5 Group | 27 Jul | Burst |
| 🥉 | Aliff (al, chat 1024343313) | 8 | DM only | 28 Jul | New |
```

Key resolution hints (the log truncates display names at first space):
- `user=No` = Telegram display name "No name" — often Syed
- `user=Mohd` = could be Izzu (display name alias)
- `user=al` = usually Aliff
- Cross-reference with `sessions.json` to confirm.

### Step 4: Extract actual message content (not just counts)

```bash
grep "inbound message.*chat=<CHAT_ID>" /root/.hermes/logs/gateway.log | grep -v "user=ARIF" | sed 's/.*msg=/→ /'
```

This gives you the actual words the user typed — useful for categorising their intent (test, casual, serious).

### Step 5: Identify pattern

Categorise the user's behaviour:

| Pattern | Signal | Shape |
|---------|--------|-------|
| **Burst user** | All messages in <30 min then silence | Steep spike, flat tail |
| **Daily user** | 1-3 messages/day steady | Low-amplitude plateau |
| **Heavy user** | 10+ messages/day across days | Sustained high volume |
| **Passive user** | Only in groups, never DMs | Group-only footprint |
| **Ghost user** | Registered in channel_directory, never messaged | Zero inbound |

### Step 6: Present as a clean summary table

| Metric | Value |
|--------|:-----:|
| Total messages | N (N DM + N group) |
| Active days | X out of Y days since access |
| Latest activity | Date, channel |
| Pattern | Burst / Daily / Ghost |

Also show the top-3 topics/themes from the message content so the sovereign knows what they're asking about.

### Log pattern examples (Jul 2026 real data)

```
# DM from Mohd (chat=1237635275 is Mohd's Telegram user ID, DM means chat_id == user_id)
2026-07-27 15:27:02 inbound message: user=Mohd chat=1237635275 msg='Who are you'

# Group message from Mohd in AIA group (detected via flush)
2026-07-28 12:07:31 Flushing text batch agent:main:telegram:group:-1003521544074:1237635275 (164 chars)

# Blocked user (before access was granted)
2026-07-27 15:19:28 Blocked unauthorized user 1237635275 in chat 1237635275
```

**Note:** Telegram display names in the `user=` field are **not actual identity** — they are whatever the user set as their Telegram profile name. "Mohd" could be Izzu, "No name" could be Syed. Always confirm identity with the sovereign or cross-reference message content before asserting who someone is.

## Decision Tree

```
Need to find past messages?
├── session_search finds them? → Use session_search (faster, richer context)
└── session_search empty?
    ├── User confirms messages exist? → Search raw logs immediately
    ├── Evidence suggests contact? → Search raw logs as verification
    └── No evidence either way? → Search raw logs to confirm absence

Need to audit user activity?
├── Sovereign asks "how often does X message?" → Follow User Activity & Frequency Analysis (steps 1-6)
├── Sovereign asks "what does X talk about?" → Extract message content (step 4)
└── Sovereign asks "is X active?" → Check DM+Group activity (step 2+3)
```
