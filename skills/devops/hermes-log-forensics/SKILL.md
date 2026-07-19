---
name: hermes-log-forensics
description: "When session_search misses messages or sessions, raw gateway logs are the authoritative fallback. Covers log locations, grep patterns, and the session DB vs raw log discrepancy."
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

## Decision Tree

```
Need to find past messages?
├── session_search finds them? → Use session_search (faster, richer context)
└── session_search empty?
    ├── User confirms messages exist? → Search raw logs immediately
    ├── Evidence suggests contact? → Search raw logs as verification
    └── No evidence either way? → Search raw logs to confirm absence
```
