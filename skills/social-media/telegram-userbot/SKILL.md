---
name: telegram-userbot
description: >
  Telethon-based Telegram userbot — run as the user's actual account to manage
  ALL chats (DMs, groups, channels). Unlike bot-based approaches, userbot sees
  everything the user sees. Requires api_id + api_hash from my.telegram.org/apps
  and phone auth via Telethon.
triggers:
  - "userbot"
  - "manage all telegram chats"
  - "telethon"
  - "my telegram account"
  - "telegram as me"
  - "read all my messages"
  - "telegram user account"
  - "mtproto login"
---

# Telegram Userbot (Telethon)

## When to Use

User wants Hermes to manage ALL their Telegram chats — DMs, groups, channels — as their actual account, not a bot account. Bot-based approach only sees chats the bot is added to; userbot sees everything.

## Prerequisites

1. **api_id + api_hash** — from https://my.telegram.org/apps
   - User logs in with phone number + code from Telegram
   - Creates app: Platform = Desktop, title/short name = anything
   - Save both values (api_id is integer, api_hash is 32-char hex)

2. **Phone number** — with country code (e.g. +60124910258)

3. **Telethon** — `pip install telethon` (or `pip install --break-system-packages telethon` on system Python)

## Auth Flow (Critical Pitfall Inside)

### ⚠️ Telegram BLOCKS codes shared in chat

Telegram's security system detects when a login code is shared in a Telegram message and **blocks the login attempt**. You'll get this message:

> "sign in was not allowed, because this code was previously shared by your account"

**This means you CANNOT send the code to the user via Telegram and have them reply it back in the same chat.** The auth will always fail.

### Workaround: Web Form on Server

Run a tiny HTTP server on the VPS that accepts the code via browser form. User opens the URL in their phone/desktop browser (NOT Telegram) and types the code there.

### Step 1: Two-Step Auth Script

The auth requires saving `phone_code_hash` between the "send code" and "verify code" steps. Single script approach:

```python
#!/usr/bin/env python3
"""Telethon auth - saves phone_code_hash between steps."""
import asyncio, sys, json
from telethon import TelegramClient

API_ID = <your_api_id>
API_HASH = "<your_api_hash>"
PHONE = "+<your_phone>"
SESSION = "/root/userbot/ari_session"
STATE_FILE = "/root/userbot/auth_state.json"

async def send_code():
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()
    sent = await client.send_code_request(PHONE)
    with open(STATE_FILE, "w") as f:
        json.dump({"phone_code_hash": sent.phone_code_hash}, f)
    print("CODE_SENT")
    await client.disconnect()

async def verify(code):
    with open(STATE_FILE) as f:
        state = json.load(f)
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()
    try:
        await client.sign_in(PHONE, code, phone_code_hash=state["phone_code_hash"])
        me = await client.get_me()
        print(f"AUTH_OK: {me.first_name} (@{me.username})")
    except Exception as e:
        print(f"AUTH_FAIL: {e}")
    finally:
        await client.disconnect()

if len(sys.argv) > 1:
    asyncio.run(verify(sys.argv[1].strip()))
else:
    asyncio.run(send_code())
```

### Step 2: Web Form for Code Entry

Build a simple HTTP server (port 9876 or similar) with a form that:
1. On GET: shows a text input + submit button
2. On POST: calls the Telethon verify function with the submitted code
3. Shows success/failure result

```python
# Key points:
# - Use http.server (stdlib), no extra deps
# - Dark themed form for mobile usability
# - asyncio.new_event_loop() for running Telethon from sync handler
# - Open firewall port: iptables -I INPUT -p tcp --dport 9876 -j ACCEPT
```

### Step 3: Send URL to User (via Telegram)

Send the public URL (http://<VPS_IP>:<port>) to the user via Telegram. They open it in BROWSER, not Telegram. Enter code → auth completes.

**After auth succeeds, shut down the web server and close the port.** The session file persists — no need to re-auth unless the session file is deleted.

## Session File

Telethon saves the session as a `.session` file (SQLite). Location: `/root/userbot/ari_session.session`. This file IS the authentication — protect it like a password. If deleted, re-auth required.

## Integration with Hermes

Once authenticated, the userbot runs as a background process that:
- Listens to all incoming messages across all chats
- Can respond as the user
- Can be integrated with Hermes via NATS, file-based IPC, or direct Python calls

## Architecture

```
Telegram Cloud ←→ Telethon (userbot process) ←→ Hermes Agent
                  [as Arif's actual account]    [AI processing]
```

vs bot-based:

```
Telegram Cloud ←→ Bot API (@ASI_arifos_bot) ←→ Hermes Agent
                  [bot account, limited scope] [AI processing]
```

## Pitfalls

- **NEVER share login codes via Telegram chat** — Telegram blocks the login. Use web form or SSH terminal.
- **phone_code_hash is one-time** — must be saved between send_code and sign_in steps. Can't reuse.
- **Codes expire in ~2 minutes** — user must enter quickly. Tell them to have browser ready before you send the code.
- **Session file = credentials** — treat `/root/userbot/ari_session.session` like a private key. Don't commit to git.
- **IPv6 may not work** — some mobile carriers don't support IPv6. Use IPv4 for the auth web form URL.
- **Firewall port** — the auth web form port must be open. Close it after auth is done.
- **Two-step auth** — Telethon's `client.start()` handles the flow automatically in interactive mode, but in non-interactive/server mode you MUST split into send_code + sign_in with saved phone_code_hash.
- **2FA accounts** — if the user has 2FA enabled, `sign_in` will need the password too. Use `client.sign_in(password=...)` after the code step.

## Cleanup Checklist

After auth succeeds:
- [ ] Kill the web form server
- [ ] Close the firewall port: `iptables -D INPUT -p tcp --dport <PORT> -j ACCEPT`
- [ ] Delete auth_state.json (phone_code_hash no longer needed)
- [ ] Verify session file exists: `ls -la /root/userbot/ari_session.session`
- [ ] Test connection: quick script that does `client.get_me()` and prints the result
