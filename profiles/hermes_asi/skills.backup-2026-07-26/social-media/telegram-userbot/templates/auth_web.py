#!/usr/bin/env python3
"""Telethon userbot auth web form.
Run: python3 auth_web.py
Opens http://0.0.0.0:9876 — user enters Telegram login code in browser.
After auth, server auto-exits.
"""
import asyncio
import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from telethon import TelegramClient

# --- CONFIG (edit these) ---
API_ID = int(os.environ.get("TG_API_ID", "0"))
API_HASH = os.environ.get("TG_API_HASH", "")
PHONE = os.environ.get("TG_PHONE", "")
SESSION_PATH = os.environ.get("TG_SESSION", "/root/userbot/ari_session")
PORT = int(os.environ.get("TG_AUTH_PORT", "9876"))
STATE_FILE = os.path.join(os.path.dirname(SESSION_PATH), "auth_state.json")
# ---------------------------

FORM_HTML = """<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Telegram Auth</title>
<style>
body{font-family:system-ui;max-width:400px;margin:60px auto;padding:20px;background:#0f0f0f;color:#fff}
h2{color:#2AABEE}
input{width:100%;padding:12px;font-size:24px;text-align:center;
  border:2px solid #2AABEE;border-radius:8px;background:#1a1a1a;color:#fff;
  margin:10px 0;letter-spacing:8px}
button{width:100%;padding:14px;font-size:18px;background:#2AABEE;color:#fff;
  border:none;border-radius:8px;cursor:pointer;margin-top:10px}
button:hover{background:#1d8bc4}
.ok{color:#4CAF50}.err{color:#f44336}
</style></head>
<body>
<h2>🔐 Telegram Login</h2>
<p>Enter the code Telegram sent you:</p>
<form method="POST">
<input name="code" placeholder="12345" autofocus required>
<button type="submit">Login</button>
</form>
<p class="%s">%s</p>
</body></html>"""

result_msg = ""
result_class = ""
auth_done = False

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write((FORM_HTML % ("", "")).encode())

    def do_POST(self):
        global result_msg, result_class, auth_done
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        code = body.split("code=")[-1].strip().replace("+", "") if "code=" in body else ""

        try:
            with open(STATE_FILE) as f:
                state = json.load(f)

            loop = asyncio.new_event_loop()

            async def do_auth():
                client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
                await client.connect()
                try:
                    await client.sign_in(PHONE, code, phone_code_hash=state["phone_code_hash"])
                    me = await client.get_me()
                    return f"✅ Auth OK: {me.first_name} (@{me.username})"
                except Exception as e:
                    return f"❌ {e}"
                finally:
                    await client.disconnect()

            result_msg = loop.run_until_complete(do_auth())
            result_class = "ok" if "✅" in result_msg else "err"
            if "✅" in result_msg:
                auth_done = True
        except Exception as e:
            result_msg = f"❌ {e}"
            result_class = "err"

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write((FORM_HTML % (result_class, result_msg)).encode())

    def log_message(self, format, *args):
        pass

async def send_code():
    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    await client.connect()
    sent = await client.send_code_request(PHONE)
    with open(STATE_FILE, "w") as f:
        json.dump({"phone_code_hash": sent.phone_code_hash}, f)
    await client.disconnect()

def main():
    if not all([API_ID, API_HASH, PHONE]):
        print("Set TG_API_ID, TG_API_HASH, TG_PHONE env vars or edit the script.")
        sys.exit(1)

    print("Sending login code to your Telegram...")
    asyncio.run(send_code())
    print(f"Code sent! Open: http://localhost:{PORT}")
    print("Waiting for code entry...")

    server = HTTPServer(("0.0.0.0", PORT), Handler)
    while not auth_done:
        server.handle_request()
    print("\nAuth complete! Shutting down web server.")
    # Clean up state file
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

if __name__ == "__main__":
    main()
