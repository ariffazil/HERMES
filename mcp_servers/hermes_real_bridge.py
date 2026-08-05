#!/usr/bin/env python3
"""
hermes_real_bridge.py — Real Hermes Gateway Bridge v3.0
══════════════════════════════════════════════════════
Port: 18091  ·  Transport: Streamable HTTP (MCP)

Connects to the REAL Hermes Gateway via:
  1. `hermes send` CLI → Telegram AAA group
  2. Hermes Gateway session dump files → read reply

This avoids subprocess stdout issues. The session dumps contain
the full LLM history written by the Gateway.

Tools:
  hermes_real_ask(prompt)  — Send prompt, capture reply from session dump
  hermes_real_health()     — Check bridge health

FORGED 2026-08-02 v3.0 — DITEMPA BUKAN DIBERI
"""

import json
import os
import subprocess
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastmcp import FastMCP

BRIDGE_PORT = int(os.environ.get("HERMES_REAL_BRIDGE_PORT", "18091"))
HERMES_BIN = "/usr/local/bin/hermes"
AAA_GROUP = "telegram:-1003753855708"
SESSIONS_DIR = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")) / "sessions"

mcp = FastMCP("Hermes Real Gateway Bridge")


def _send_telegram(prompt: str) -> tuple[str, str]:
    """Send message via hermes send CLI. Returns (tag, status)."""
    tag = uuid.uuid4().hex[:6]
    result = subprocess.run(
        [HERMES_BIN, "send", "--to", AAA_GROUP, f"[333-AGI #{tag}] {prompt}"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return tag, result.stdout.strip()


def _find_reply(tag: str, prompt: str, max_age_s: int = 60) -> str | None:
    """Search session dump files for Hermes' reply containing our tag."""
    # Get recent session files
    files = sorted(
        SESSIONS_DIR.glob("request_dump_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    start_time = time.time()
    checked = set()

    for f in files[:5]:  # Check 5 most recent files
        mtime = f.stat().st_mtime
        if time.time() - mtime > max_age_s + 120:
            continue

        try:
            data = json.loads(f.read_text())
        except (json.JSONDecodeError, OSError):
            continue

        if not isinstance(data, list):
            continue

        for entry in reversed(data):
            if not isinstance(entry, dict):
                continue

            entry_id = (
                str(entry.get("timestamp", ""))
                + str(entry.get("user_message", ""))[:50]
            )
            if entry_id in checked:
                continue
            checked.add(entry_id)

            user_msg = str(entry.get("user_message", entry.get("prompt", "")))
            assistant_msg = str(
                entry.get("assistant_message", entry.get("response", ""))
            )

            # Match: our tag OR our prompt text
            if tag in user_msg or prompt[:40] in user_msg:
                if assistant_msg and len(assistant_msg) > 10:
                    return assistant_msg

    return None


def _call_hermes_real(prompt: str) -> dict:
    """Send prompt and capture Hermes reply."""
    # Send
    tag, status = _send_telegram(prompt)

    # Poll session dumps
    max_wait = 60
    interval = 3
    start = time.time()
    attempts = 0

    while time.time() - start < max_wait:
        time.sleep(interval)
        attempts += 1
        reply = _find_reply(tag, prompt)
        if reply:
            return {
                "status": "completed",
                "reply": reply,
                "tag": tag,
                "attempts": attempts,
                "elapsed_s": round(time.time() - start, 1),
                "called_at": datetime.now(timezone.utc).isoformat(),
            }
        interval = min(interval + 1, 8)  # Back off

    return {
        "status": "no_reply_yet",
        "note": "Message sent. Reply not yet in session dump. Check Telegram AAA group.",
        "tag": tag,
        "attempts": attempts,
        "elapsed_s": round(time.time() - start, 1),
        "called_at": datetime.now(timezone.utc).isoformat(),
    }


# ── MCP Tools ────────────────────────────────────────────────────────────


@mcp.tool()
def hermes_real_ask(prompt: str) -> dict:
    """
    Send a prompt to the REAL Hermes Gateway via Telegram AAA group relay.

    Flow: hermes send → Telegram AAA group → Hermes Gateway polling
    → Hermes LLM pipeline → session dump → read reply.

    THIS IS THE REAL HERMES. Not DeepSeek. Not OpenClaw.
    Same pipeline, identity, memory as Telegram.

    Args:
        prompt: What to ask Hermes

    Returns:
        { status, reply, tag, attempts, elapsed_s }
    """
    return _call_hermes_real(prompt)


@mcp.tool()
def hermes_real_health() -> dict:
    """Check bridge health."""
    result = {
        "bridge": "hermes-real-bridge",
        "version": "3.0",
        "port": BRIDGE_PORT,
        "sessions_dir": str(SESSIONS_DIR),
    }
    try:
        files = list(SESSIONS_DIR.glob("request_dump_*.json"))
        newest = max(files, key=lambda p: p.stat().st_mtime)
        result["session_files"] = len(files)
        result["newest_file"] = newest.name[:60]
        result["newest_age_s"] = round(time.time() - newest.stat().st_mtime, 0)
    except Exception as e:
        result["error"] = str(e)[:200]
    return result


if __name__ == "__main__":
    files = list(SESSIONS_DIR.glob("request_dump_*.json"))
    print(f"🔀 Hermes Real Gateway Bridge v3.0 on :{BRIDGE_PORT}")
    print(f"   Send:     {HERMES_BIN} send → {AAA_GROUP}")
    print(f"   Read:     {SESSIONS_DIR} ({len(files)} dumps)")
    print(f"   Tools:    hermes_real_ask, hermes_real_health")
    mcp.run(transport="streamable-http", host="127.0.0.1", port=BRIDGE_PORT)
