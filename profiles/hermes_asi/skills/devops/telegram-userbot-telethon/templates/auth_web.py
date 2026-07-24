#!/usr/bin/env python3
"""One-shot auth web form for Telethon userbot login.
Usage:
  1. Run: python3 auth_web.py
  2. Opens http://0.0.0.0:9876 — Telegram sends code to user's phone
  3. User opens URL in BROWSER (not Telegram), enters code
  4. Session saved, server exits

CRITICAL: Code must NOT be sent via Telegram chat — Telegram auto-blocks it.
"""
import asyncio
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from telethon import TelegramClient
from urllib.parse import parse_qs

API_ID = 37046798         # Replace with your api_id
API_HASH = "YOUR_HASH"    # Replace with your api_hash
PHONE = "+60123456789"    # Replace with phone number
SESSION = "/root/userbot/ari_session"
STATE_FILE = "/root/userbot/auth_state.json"
PORT = 9876

def make_html(msg="", cls=""):
    """HTML with CSS — uses .format() safe braces (no f-string conflict)."""
    return (
        '<!DOCTYPE html><html><head>'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Telegram Auth</title><style>'
        'body{font-family:system-ui;max-width:400px;margin:60px auto;padding:20px;background:#0f0f0f;color:#fff}'
        'h2{color:#2AABEE}'
        'input{width:100%;padding:12px;font-size:24px;text-align:center;'
        'border:2px solid #2AABEE;border-radius:8px;background:#1a1a1a;color:#fff;margin:10px 0;letter-spacing:8px}'
        'button{width:100%;padding:14px;font-size:18px;background:#2AABEE;color:#fff;'
        'border:none;border-radius:8px;cursor:pointer;margin-top:10px}'
        '.ok{color:#4CAF50} .err{color:#f44336}'
        '</style></head><body>'
        '<h2>Telegram Login</h2>'
        '<p>Enter the code Telegram sent you:</p>'
        '<form method="POST">'
        '<input name="code" placeholder="12345" autofocus required>'
        '<button type="submit">Login</button>'
        '</form>'
        '<p class="{cls}">{msg}</p>'
        '</body></html>'
    ).format(cls=cls, msg=msg)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(make_html().encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)
        code = params.get("code", [""])[0]

        msg, cls = "", ""
        try:
            with open(STATE_FILE) as f:
                state = json.load(f)
            loop = asyncio.new_event_loop()
            async def do_auth():
                client = TelegramClient(SESSION, API_ID, API_HASH)
                await client.connect()
                try:
                    await client.sign_in(
                        PHONE, code,
                        phone_code_hash=state["phone_code_hash"]
                    )
                    me = await client.get_me()
                    return f"Auth OK: {me.first_name} (@{me.username})", "ok"
                except Exception as e:
                    return f"Error: {e}", "err"
                finally:
                    await client.disconnect()
            msg, cls = loop.run_until_complete(do_auth())
        except Exception as e:
            msg, cls = f"Error: {e}", "err"

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(make_html(msg, cls).encode())

    def log_message(self, format, *args):
        pass


async def send_code():
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()
    sent = await client.send_code_request(PHONE)
    with open(STATE_FILE, "w") as f:
        json.dump({"phone_code_hash": sent.phone_code_hash}, f)
    await client.disconnect()


print("Sending login code to your Telegram...")
asyncio.run(send_code())
print(f"Code sent! Open: http://localhost:{PORT}")
print("Waiting for code entry...")

server = HTTPServer(("0.0.0.0", PORT), Handler)
server.serve_forever()
