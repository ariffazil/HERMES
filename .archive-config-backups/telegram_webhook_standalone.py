#!/usr/bin/env python3
"""
Standalone Telegram Webhook Receiver — bypasses Hermes gateway's broken initialize().
Receives webhook updates from Telegram, forwards to Hermes A2A, sends replies back.
Listens: 127.0.0.1:8444 (Caddy reverse-proxies arifos.arif-fazil.com/telegram/webhook)
"""

import json, os, sys, logging, hmac, hashlib, asyncio
from datetime import datetime, timezone
from aiohttp import web

logging.basicConfig(level=logging.INFO, format="[webhook] %(message)s")
log = logging.getLogger("telegram-webhook")

TOKEN = os.environ.get("ASI_ARIFOS_BOT_TOKEN", "")
SECRET = os.environ.get("TELEGRAM_WEBHOOK_SECRET", "hermes_webhook_secret_2026")
API = f"https://api.telegram.org/bot{TOKEN}"
A2A_URL = "http://127.0.0.1:18089/v1/a2a"


async def send_telegram(chat_id: int, text: str, reply_to: int = None):
    import aiohttp

    payload = {"chat_id": chat_id, "text": text[:4000], "parse_mode": "HTML"}
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    async with aiohttp.ClientSession() as s:
        async with s.post(
            f"{API}/sendMessage", json=payload, timeout=aiohttp.ClientTimeout(15)
        ) as r:
            result = await r.json()
            if result.get("ok"):
                log.info(f"Reply sent to {chat_id}")
            else:
                log.error(f"Send failed: {result}")


async def ask_hermes_agent(text: str, user_id: str) -> str:
    """Forward message to Hermes agent via A2A and get reply."""
    import aiohttp

    payload = {
        "prompt": text,
        "mode": "ask",
        "user_context": {"user_id": str(user_id), "platform": "telegram"},
    }
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(
                A2A_URL, json=payload, timeout=aiohttp.ClientTimeout(120)
            ) as r:
                result = await r.json()
                reply = result.get("reply", "")
                if isinstance(reply, dict):
                    reply = reply.get("text", json.dumps(reply))
                return str(reply) if reply else "Maaf, tak dapat jawapan dari Hermes."
    except Exception as e:
        log.error(f"A2A error: {e}")
        return f"Ralat: {str(e)[:200]}"


async def handle_webhook(request: web.Request):
    """Handle incoming Telegram webhook."""
    # Verify secret token
    token = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if not hmac.compare_digest(token, SECRET):
        log.warning("Invalid secret token")
        return web.Response(status=403, text="Forbidden")

    try:
        data = await request.json()
    except Exception:
        return web.Response(status=400, text="Bad JSON")

    log.info(f"Webhook received: {json.dumps(data, default=str)[:500]}")

    # Extract message
    message = data.get("message") or data.get("edited_message")
    if not message:
        return web.Response(text="OK")  # not a message, acknowledge

    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text") or message.get("caption", "")
    user = message.get("from", {})
    user_id = user.get("id", "unknown")
    msg_id = message.get("message_id")

    if not chat_id or not text:
        return web.Response(text="OK")

    log.info(f"Message from {user_id} in chat {chat_id}: {text[:100]}")

    # Send typing indicator
    import aiohttp

    async with aiohttp.ClientSession() as s:
        await s.post(
            f"{API}/sendChatAction",
            json={"chat_id": chat_id, "action": "typing"},
            timeout=aiohttp.ClientTimeout(5),
        )

    # Ask hermes
    reply = await ask_hermes_agent(text, str(user_id))
    await send_telegram(chat_id, reply, reply_to=msg_id)

    return web.Response(text="OK")


async def health(request: web.Request):
    return web.Response(text="OK")


async def main():
    app = web.Application()
    app.router.add_post("/telegram/webhook", handle_webhook)
    app.router.add_get("/health", health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 8444)
    await site.start()
    log.info("Webhook server listening on 127.0.0.1:8444/telegram/webhook")
    # Keep running
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
