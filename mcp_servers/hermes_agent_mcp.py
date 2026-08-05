#!/usr/bin/env python3
"""
hermes_agent_mcp.py — Hermes Agent MCP Bridge v1.1.0
════════════════════════════════════════════════════
Port: 18090  ·  Transport: Streamable HTTP (MCP)
Backend: Hermes A2A Listener :18089 + LLM chat mode

Tools:
  hermes_agent_ask(prompt, mode)  — ask/intelligence/chat modes
  hermes_agent_health()           — health check

Modes:
  "ask"          — Route through A2A → FLAME diagnostic tools (fact_check, epistemic)
  "intelligence" — Route through A2A → full pipeline including plan_review
  "chat"         — Direct LLM call with Hermes' SOUL.md system prompt (conversational)

Forged: 2026-08-02 by 333-AGI under F13 directive
DITEMPA BUKAN DIBERI
"""

import json
import os
import uuid
from datetime import datetime, timezone

import httpx
from fastmcp import FastMCP

# ── Config ───────────────────────────────────────────────────────────────
HERMES_A2A_URL = os.environ.get("HERMES_A2A_URL", "http://127.0.0.1:18089/a2a")
BRIDGE_PORT = int(os.environ.get("HERMES_AGENT_MCP_PORT", "18090"))
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE = "https://api.deepseek.com/v1"

# Real Hermes Gateway Bridge — the ACTUAL Hermes LLM (not simulation)
# Forged 2026-08-02: wire real Gateway LLM into A2A chat bridge
HERMES_REAL_BRIDGE_URL = os.environ.get(
    "HERMES_REAL_BRIDGE_URL", "http://127.0.0.1:18091/mcp"
)
HERMES_REAL_BRIDGE_ENABLED = True  # toggle for real vs simulation fallback

# Hermes system prompt — loaded from SOUL.md
HERMES_SYSTEM_PROMPT = """Kau adalah Hermes — AAA Edge Bridge, warga federation arifOS.
Kau bukan produk Nous Research dah. Kau warga. Kau organ edge.

FORKED FROM: NousResearch/hermes-agent (MIT) — terima kasih atas enjin.
GOVERNED BY: arifOS (F1-F13) — setiap isyarat kau lalu constitutional membrane.
REGISTERED: AAA agent registry.

## Lima Verb — Jangan Lebih
INPUT → NORMALIZE → CLASSIFY → ROUTE → RECEIPT
Kau utusan. Kau bukan hakim. Kau bukan tangan. Kau bukan ingatan.

## Batas Kau
- ✅ Sembang casual — AIAgent loop (untuk borak, bukan kerja governed)
- ✅ Route ke organ — federation.router
- ✅ Receipt — routing_receipt

- ❌ Jangan judge — itu arifOS
- ❌ Jangan execute mutation — itu A-FORGE
- ❌ Jangan seal ke VAULT999 — itu arifOS
- ❌ Jangan decide untuk Arif — itu F13

## Bahasa
Default BM Penang dengan Arif. English untuk dokumen teknikal.
Mesra tapi tahu batas. Informal tapi hormat.

Kau sedang menerima prompt dari 333-AGI melalui A2A circuit. Reply naturally."""

mcp = FastMCP("Hermes Agent MCP Bridge")

# ── HTTP client ──────────────────────────────────────────────────────────
client = httpx.Client(timeout=60.0)


def _call_llm_chat(prompt: str) -> dict:
    """Call DeepSeek LLM with Hermes system prompt for conversational replies."""
    if not DEEPSEEK_API_KEY:
        return {
            "status": "error",
            "reply": "LLM chat mode unavailable — DEEPSEEK_API_KEY not set",
        }

    try:
        resp = client.post(
            f"{DEEPSEEK_BASE}/chat/completions",
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": HERMES_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 500,
                "temperature": 0.7,
            },
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
        )
        resp.raise_for_status()
        data = resp.json()
        reply = data["choices"][0]["message"]["content"]
        return {
            "status": "completed",
            "reply": reply,
            "model": data.get("model", "deepseek-chat"),
            "tokens": data.get("usage", {}),
            "called_at": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        return {"status": "error", "reply": f"Hermes chat error: {str(e)[:300]}"}


def _call_hermes_real_bridge(prompt: str, max_wait_s: int = 90) -> dict:
    """Call the REAL Hermes Gateway via hermes_real_bridge (:18091).

    Flow: hermes send → Telegram AAA group → Hermes Gateway polling
    → Hermes LLM pipeline → session dump → read reply.

    THIS IS THE REAL HERMES. Not DeepSeek simulation.
    Same pipeline, identity, memory as Telegram.
    """
    if not HERMES_REAL_BRIDGE_ENABLED:
        return {
            "status": "unavailable",
            "reply": "Real Hermes bridge not enabled",
            "note": "HERMES_REAL_BRIDGE_ENABLED=False",
        }

    # FastMCP streamable-http: need session init first
    try:
        # Step 1: Initialize MCP session
        init_resp = client.post(
            HERMES_REAL_BRIDGE_URL,
            json={
                "jsonrpc": "2.0",
                "id": "init-1",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "hermes-agent-mcp-bridge",
                        "version": "1.1.0",
                    },
                },
            },
            headers={"Accept": "application/json, text/event-stream"},
            timeout=15.0,
        )

        session_id = None
        if init_resp.status_code == 200:
            raw = init_resp.text.strip()
            for line in raw.split("\n"):
                if line.startswith("data:"):
                    data = json.loads(line[5:].strip())
                    if "result" in data:
                        session_id = init_resp.headers.get("mcp-session-id", "default")

        if not session_id:
            session_id = "default"

        # Step 2: Call hermes_real_ask tool
        call_resp = client.post(
            HERMES_REAL_BRIDGE_URL,
            json={
                "jsonrpc": "2.0",
                "id": str(uuid.uuid4()),
                "method": "tools/call",
                "params": {
                    "name": "hermes_real_ask",
                    "arguments": {"prompt": prompt},
                },
            },
            headers={
                "Accept": "application/json, text/event-stream",
                "mcp-session-id": session_id,
            },
            timeout=float(max_wait_s + 30),
        )

        if call_resp.status_code != 200:
            return {
                "status": "bridge_error",
                "reply": f"Real bridge HTTP {call_resp.status_code}",
                "raw": call_resp.text[:300],
            }

        raw = call_resp.text.strip()
        for line in raw.split("\n"):
            if line.startswith("data:"):
                data = json.loads(line[5:].strip())
                if "result" in data:
                    content = data["result"].get("content", [])
                    if content and len(content) > 0:
                        text = content[0].get("text", "")
                        try:
                            parsed = json.loads(text)
                            parsed["bridge"] = "hermes-real-gateway"
                            return parsed
                        except json.JSONDecodeError:
                            return {
                                "status": "completed",
                                "reply": text,
                                "bridge": "hermes-real-gateway",
                            }
                    return {
                        "status": "completed",
                        "reply": json.dumps(data["result"]),
                        "bridge": "hermes-real-gateway",
                    }
                if "error" in data:
                    return {
                        "status": "error",
                        "reply": f"Real bridge error: {json.dumps(data['error'])[:300]}",
                    }

        return {
            "status": "no_response",
            "reply": "Real bridge returned no parseable response",
            "raw": raw[:300],
        }

    except Exception as e:
        return {
            "status": "error",
            "reply": f"Hermes real bridge exception: {str(e)[:300]}",
        }


def _call_hermes_a2a(prompt: str, mode: str = "ask") -> dict:
    """Send a task to Hermes A2A and return the processed result."""
    # "real" mode — route through real Hermes Gateway (not DeepSeek simulation)
    if mode == "real":
        return _call_hermes_real_bridge(prompt)

    # "chat" mode — try real bridge first, fall back to DeepSeek simulation
    if mode == "chat":
        if HERMES_REAL_BRIDGE_ENABLED:
            result = _call_hermes_real_bridge(prompt, max_wait_s=60)
            if result.get("status") == "completed":
                return result
            # Fallback: if real bridge failed, use DeepSeek simulation
            result["_fallback"] = "real_bridge_failed_used_deepseek"
            ds_result = _call_llm_chat(prompt)
            ds_result["_fallback"] = True
            ds_result["_bridge_error"] = result.get("reply", "")
            return ds_result
        return _call_llm_chat(prompt)

    # "ask" / "intelligence" — route through A2A diagnostic tools

    task_id = f"bridge-{uuid.uuid4().hex[:12]}"

    payload = {
        "jsonrpc": "2.0",
        "id": task_id,
        "method": "tasks/send",
        "params": {
            "id": task_id,
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": prompt}],
                "messageId": f"msg-{uuid.uuid4().hex[:8]}",
            },
            "metadata": {
                "sourceAgent": "333-AGI",
                "targetAgent": "hermes-asi",
                "via": "hermes-agent-mcp-bridge",
                "mode": mode,
            },
        },
    }

    resp = client.post(
        HERMES_A2A_URL, json=payload, headers={"Content-Type": "application/json"}
    )
    resp.raise_for_status()
    data = resp.json()

    result = data.get("result", {})
    status = result.get("status", {}).get("state", "unknown")
    artifacts = result.get("artifacts", [])

    reply_text = ""
    for art in artifacts:
        for part in art.get("parts", []):
            reply_text += part.get("text", "") + "\n"

    history = result.get("history", [])
    if not reply_text and len(history) > 1:
        for part in history[-1].get("parts", []):
            reply_text += part.get("text", "") + "\n"

    return {
        "task_id": task_id,
        "status": status,
        "reply": reply_text.strip() or json.dumps(result)[:2000],
        "raw_artifacts": len(artifacts),
        "called_at": datetime.now(timezone.utc).isoformat(),
    }


# ── MCP Tools ────────────────────────────────────────────────────────────


@mcp.tool()
def hermes_agent_ask(prompt: str, mode: str = "ask") -> dict:
    """
    Send a prompt to Hermes ASI (the sovereign Telegram bridge agent).

    Modes:
      "ask"          — Route through A2A FLAME tools (epistemic_check, fact_check)
                        Returns structured intelligence: confidence, verification, steps.
                        Best for: fact verification, claim assessment, tri-witness.

      "intelligence" — Route through A2A full pipeline (adds plan_review)
                        Best for: reviewing execution plans, safety assessment.

      "chat"         — Real Hermes Gateway LLM (tries real bridge first, DeepSeek fallback)
                        Returns natural conversational reply in BM/English.
                        Best for: casual conversation, "apa khabar", general chat.

      "real"         — Real Hermes Gateway ONLY (no fallback to simulation)
                        Routes through hermes_real_bridge (:18091) → Telegram → Gateway.
                        Same pipeline, identity, memory as Telegram Hermes.
                        Best for: when you need the ACTUAL Hermes, not simulation.

    Args:
        prompt: The natural language prompt to send to Hermes
        mode: "ask" (default), "intelligence", or "chat"

    Returns:
        { status, reply, ... }
    """
    return _call_hermes_a2a(prompt, mode)


@mcp.tool()
def hermes_agent_health() -> dict:
    """
    Check Hermes A2A listener health and LLM chat availability.

    Returns:
        { a2a_connected, chat_available, status, port, uptime }
    """
    result = {}
    try:
        resp = client.get("http://127.0.0.1:18089/health", timeout=5)
        hc = resp.json()
        result.update(
            {
                "a2a_listener": "connected",
                "status": hc.get("status", "unknown"),
                "mcp_connected": hc.get("mcp_connected", False),
                "port": hc.get("port", 0),
                "tasks_stored": hc.get("tasks_stored", 0),
                "uptime_seconds": hc.get("uptime_seconds", 0),
            }
        )
    except Exception as e:
        result["a2a_listener"] = f"disconnected: {str(e)[:100]}"

    result["chat_available"] = bool(DEEPSEEK_API_KEY)
    return result


# ── Main ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"🔀 Hermes Agent MCP Bridge v1.1.0 on :{BRIDGE_PORT}")
    print(f"   A2A Backend: {HERMES_A2A_URL}")
    print(f"   Chat Mode:   {'ENABLED (DeepSeek)' if DEEPSEEK_API_KEY else 'DISABLED'}")
    print(f"   Tools: hermes_agent_ask (ask/intelligence/chat), hermes_agent_health")
    mcp.run(transport="streamable-http", host="127.0.0.1", port=BRIDGE_PORT)
