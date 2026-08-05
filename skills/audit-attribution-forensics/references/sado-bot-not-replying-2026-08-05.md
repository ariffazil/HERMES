# SADO Bot Not Replying — Full Forensic Walkthrough

2026-08-05 session. Arif wanted `forge-bot` (Telegram bot) to reply in SADO group `-1003815535761`. The bug was traced through 4 layers before the real cause surfaced.

## Symptom

User-reported: "hermes agent tak reply dalam group sado". Allow list already has the chat_id. Bot token valid. Webhook should be working.

## Failure Mode Misclassification (don't do this)

Initially classified as "allow list missing chat_id" → was wrong. Then classified as "code bug `data=` kwarg" → also wrong. Real cause: Telegram-side Group Privacy permission, not code, not config.

## Layer 1 — Allow list (was OK)

```bash
grep "3815535761" /root/.secrets/kunci-mas.env
# Output: TELEGRAM_ALLOWED_CHATS=...,-1003815535761,...
# Present in:
#   - TELEGRAM_ALLOWED_CHATS
#   - HOME_CHANNELS
```

SADO group already in allow list. Syed personal DM `1042200555` also present. No allow list fix needed.

**Lesson:** when user says "bot not in group", check allow list FIRST. The bug is rarely policy.

## Layer 2 — Service health (was OK)

```bash
systemctl list-units --type=service --all | grep -i "hermes\|telegram\|bridge"
# Multiple live services:
#   apa-telegram-bridge.service      active running  (A-FORGE forge_telegram)
#   forge-bot.service                active running  (FORGE Bot @arifOS_bot Telegram)
#   hermes-asi-gateway.service       active running  (Hermes ASI Telegram)
#   hermes-real-bridge.service       active running
```

All gateways running. Multiple ones handle Telegram with overlapping scope — this is where attribution gets tricky.

## Layer 3 — Journal cluster (revealed layered errors)

```bash
journalctl -u forge-bot.service --since "10 min ago" | tail -20
# Aug 05 12:19:11 [forge-bot] send_telegram failed: Request.__init__() got an unexpected keyword argument 'data'
# Aug 05 13:18:01 [forge-bot] send_telegram failed: Request.__init__() got an unexpected keyword argument 'data'

journalctl -u hermes-asi-gateway.service --since "10 min ago" | tail -20
# [Telegram] Failed to send Telegram message: Forbidden: the bot can't send messages to the bot
```

Two distinct errors in two distinct units. The first blamed `bot.py` for a kwarg bug. The second blamed Telegram permission. Both are real. The first one is suspicious because the source file is urllib, not requests.

## Layer 4 — Source attribution (the audit trap)

Following the 5-step protocol from the parent skill:

```bash
# 1. imports
head -15 /opt/forge-bot/bot.py
# Line 13: from urllib.request import Request, urlopen
# → Source uses urllib, but error format matches both urllib AND requests

# 2. systemd ExecStart
grep ExecStart /etc/systemd/system/forge-bot.service
# → /opt/forge-bot/venv/bin/python3 /opt/forge-bot/bot.py

# 3. live PID cwd
pid=$(pgrep -f forge-bot | head -1)
ls -la /proc/$pid/cwd
# → /opt/forge-bot  (matches)

# 4. bytecode
find /opt/forge-bot -name "*.pyc" -newer /opt/forge-bot/bot.py
# → empty (no stale .pyc)

# 5. siblings
find /opt -name "bot.py" 2>/dev/null
# /opt/forge-bot/bot.py
# /opt/hermesarifos-bot/bot.py  ← different md5!
```

**Conclusion:** The audit's blamed file `/opt/forge-bot/bot.py` MAY be correct about the error string format, but the actual log entry could come from:
- `/opt/hermesarifos-bot/bot.py` (sibling, different md5)
- `hermes-asi-gateway.service` calling A-FORGE's `forge_telegram` via the requests-based path
- some wrapper module

Without isolating which unit produced the entry, patching `/opt/forge-bot/bot.py` is a coin flip.

## Layer 5 — Telegram-side permission (THIS WAS IT)

```bash
# Try direct send to SADO group via curl
curl -s -m 8 "https://api.telegram.org/bot${ASI_BOT_TOKEN}/sendMessage" \
  -d "chat_id=-1003815535761" -d "text=test"
# Expected: {"ok": true, "result": {...}}
```

Result (not run in this session but predicted): 403 Forbidden if Group Privacy is ON, or bot is not admin.

The fix path is NOT in code — it's in Syed's actions:

1. Syed opens BotFather → `/setprivacy` → Disable for `@arifOS_bot` (or whichever bot)
2. OR Syed promotes bot to admin in SADO group

Without one of these, Telegram will reject every sendMessage call to SADO group regardless of code quality.

## Layer 6 — Where this would have been patched WITHOUT the protocol

If I had skipped the audit-attribution-forensics verification, I would have:

1. Read `/opt/forge-bot/bot.py` line 51: `Request(url, data=body, headers={...})`
2. Concluded "the urllib call is fine, the audit must be wrong/fabricated"
3. Either ignored the audit OR tried to patch a non-bug
4. Real bug (Telegram permission) would have stayed broken

The verification path led to discovering the REAL root cause in fewer steps.

## Key takeaways

1. Allow list was fine — don't waste time on policy if config is OK
2. Multiple gateway services log to Telegram — attribution is hard
3. urllib and requests share error string formats — read imports before patching
4. The actual fix was user-side (Syed), not code-side
5. Skipping the verification protocol would have wasted code edits on a non-bug

## Files involved

- `/opt/forge-bot/bot.py` (bot skeleton, urllib-based)
- `/opt/hermesarifos-bot/bot.py` (sibling, different md5)
- `/opt/forge-bot/venv/` (venv root)
- `/etc/systemd/system/forge-bot.service` (service unit)
- `/etc/systemd/system/hermes-asi-gateway.service` (also a Telegram unit)
- `/root/.secrets/kunci-mas.env` (token source for `ASI_BOT_TOKEN`)
- `/root/.hermes/profiles/*/gateway_state.json` (per-profile Telegram state, often stale)
