#!/usr/bin/env python3
"""
Two-step Telethon auth for non-interactive environments.
Usage:
  Step 1: python3 two-step-auth.py          (sends code, saves hash)
  Step 2: python3 two-step-auth.py 12345    (verifies code with saved hash)
"""
import asyncio
import sys
import json
from telethon import TelegramClient

API_ID = 37046798
API_HASH = "1bd06b1c4c9252c05a64512b066b8986"
PHONE = "+60124910258"
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
