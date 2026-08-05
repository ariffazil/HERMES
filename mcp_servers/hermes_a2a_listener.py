#!/usr/bin/env python3
"""
hermes_a2a_listener.py — Hermes A2A Inbound Listener
═══════════════════════════════════════════════════════
Port: 18089  ·  Transport: HTTP (JSON-RPC 2.0 over POST)
Protocol: A2A v1.0 (a2aproject/A2A)

What this does:
  - Listens for incoming A2A tasks from the AAA gateway or any A2A caller
  - Processes prompts through Hermes' existing MCP tools (fact_check, epistemic_check, plan_review)
  - Returns structured task responses
  - Serves agent-card.json at /.well-known/

This CLOSES the circuit gap:
  Before: Hermes → AAA A2A (outbound only). No way for 333-AGI to reach Hermes.
  After:  333-AGI → AAA A2A → Hermes A2A :18089 → reply.

Forged: 2026-08-02 by 333-AGI under F13 SOVEREIGN directive "do your 2 hours work"
DITEMPA BUKAN DIBERI
"""

import json
import os
import sys
import time
import uuid
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, Response
import uvicorn

# ── Config ───────────────────────────────────────────────────────────────
A2A_PORT = int(os.environ.get("HERMES_A2A_PORT", "18089"))
A2A_HOST = os.environ.get("HERMES_A2A_HOST", "127.0.0.1")

# Hermes MCP tools endpoint (the existing hermes-mcp service on :18086)
HERMES_MCP_URL = os.environ.get("HERMES_MCP_URL", "http://127.0.0.1:18086/mcp")

# Hermes Real Gateway Bridge — the ACTUAL Hermes LLM (not diagnostic tools)
# Forged 2026-08-02: wire to real Hermes via Telegram relay bridge
HERMES_REAL_BRIDGE_URL = os.environ.get(
    "HERMES_REAL_BRIDGE_URL", "http://127.0.0.1:18091/mcp"
)

# Hermes Gateway API (serve mode) — direct HTTP API for agents
HERMES_GATEWAY_API_URL = os.environ.get(
    "HERMES_GATEWAY_API_URL", "http://127.0.0.1:9120"
)

# arifOS kernel for session binding
ARIFOS_MCP_URL = os.environ.get("ARIFOS_MCP_URL", "http://127.0.0.1:8088/mcp")

# Agent card path
AGENT_CARD_PATH = Path(
    os.environ.get("HERMES_AGENT_CARD", "/root/HERMES/.well-known/agent-card.json")
)

# ── FastAPI app ──────────────────────────────────────────────────────────
app = FastAPI(
    title="Hermes A2A Listener",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

# ── In-memory task store ─────────────────────────────────────────────────
tasks: dict = {}


# ── JSON-RPC Helpers ─────────────────────────────────────────────────────
def jsonrpc_result(req_id, result):
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def jsonrpc_error(req_id, code: int, message: str, data: str = ""):
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": code, "message": message, "data": data},
    }


# ── MCP Call Helper ──────────────────────────────────────────────────────
MCP_SESSION: str | None = None
MCP_CLIENT = httpx.AsyncClient(timeout=30.0)


async def mcp_call(url: str, method: str, params: dict | None = None) -> dict:
    """Call an MCP tool via Streamable HTTP transport. Handles session init."""
    global MCP_SESSION

    sid = MCP_SESSION or "hermes-a2a"

    # Initialize session if needed
    if MCP_SESSION is None:
        init_resp = await MCP_CLIENT.post(
            url,
            json={
                "jsonrpc": "2.0",
                "id": "init-1",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "hermes-a2a-listener", "version": "1.0"},
                },
            },
            headers={"Accept": "application/json, text/event-stream"},
        )
        if init_resp.status_code == 200:
            raw = init_resp.text.strip()
            for line in raw.split("\n"):
                if line.startswith("data:"):
                    data = json.loads(line[5:].strip())
                    if "result" in data:
                        MCP_SESSION = init_resp.headers.get("mcp-session-id", "default")
                        sid = MCP_SESSION
                        break
            # Send initialized notification
            await MCP_CLIENT.post(
                url,
                json={"jsonrpc": "2.0", "method": "notifications/initialized"},
                headers={
                    "Accept": "application/json, text/event-stream",
                    "mcp-session-id": sid,
                },
            )

    if MCP_SESSION is None:
        MCP_SESSION = "default"
        sid = "default"

    # Call the tool
    resp = await MCP_CLIENT.post(
        url,
        json={
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tools/call",
            "params": {"name": method, "arguments": params or {}},
        },
        headers={
            "Accept": "application/json, text/event-stream",
            "mcp-session-id": sid,
        },
    )

    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}", "raw": resp.text[:500]}

    raw = resp.text.strip()
    for line in raw.split("\n"):
        if line.startswith("data:"):
            data = json.loads(line[5:].strip())
            if "result" in data:
                content = data["result"].get("content", [])
                if content and len(content) > 0:
                    text = content[0].get("text", "")
                    try:
                        return json.loads(text)
                    except json.JSONDecodeError:
                        return {"text": text}
                return data["result"]
            if "error" in data:
                return {"error": data["error"]}
    return {"error": "no parseable response", "raw": raw[:300]}


async def get_session_token() -> str:
    """Get an arifOS session token for Hermes identity."""
    result = await mcp_call(
        ARIFOS_MCP_URL,
        "arif_init",
        {
            "actor_id": "hermes-asi",
            "intent": "A2A inbound task processing",
            "mode": "light",
        },
    )
    return result.get("session_token", "")


# ── Task Processing ──────────────────────────────────────────────────────
async def process_hermes_task(message_text: str, context: dict = None) -> dict:
    """
    Process an incoming A2A task through Hermes' intelligence pipeline.
    Uses the existing Hermes MCP tools for fact checking and epistemic evaluation.
    """
    results = {
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "hermes_version": "a2a-listener-v1.0.0",
        "steps": [],
    }

    # Step 1: Epistemic check
    try:
        ep_result = await mcp_call(
            HERMES_MCP_URL,
            "hermes_epistemic_check",
            {"claim": message_text, "mode": "quick"},
        )
        results["steps"].append(
            {
                "step": "epistemic_check",
                "verdict": ep_result.get("verdict", "UNKNOWN"),
                "confidence": ep_result.get("heuristic_confidence", 0),
            }
        )
        results["epistemic"] = ep_result
    except Exception as e:
        results["steps"].append({"step": "epistemic_check", "error": str(e)})

    # Step 2: Fact check (quick mode)
    try:
        fc_result = await mcp_call(
            HERMES_MCP_URL,
            "hermes_fact_check",
            {"claim": message_text, "mode": "quick"},
        )
        results["steps"].append(
            {
                "step": "fact_check",
                "passed": fc_result.get("passed_heuristic", False),
                "score": fc_result.get("heuristic_score", 0),
            }
        )
        results["fact_check"] = fc_result
    except Exception as e:
        results["steps"].append({"step": "fact_check", "error": str(e)})

    # Step 3: Plan review (if it looks like a plan)
    if any(
        kw in message_text.lower()
        for kw in ["plan", "execute", "build", "deploy", "create", "change"]
    ):
        try:
            pr_result = await mcp_call(
                HERMES_MCP_URL,
                "hermes_plan_review",
                {"plan": message_text, "mode": "quick"},
            )
            results["steps"].append({"step": "plan_review", "result": "completed"})
            results["plan_review"] = pr_result
        except Exception as e:
            results["steps"].append({"step": "plan_review", "error": str(e)})

    return results


# ── Routes ────────────────────────────────────────────────────────────────


@app.get("/.well-known/agent-card.json")
async def serve_agent_card():
    """Serve the Hermes A2A agent card."""
    if AGENT_CARD_PATH.exists():
        return JSONResponse(content=json.loads(AGENT_CARD_PATH.read_text()))
    raise HTTPException(status_code=404, detail="Agent card not found")


@app.get("/health")
async def health():
    """Health check."""
    try:
        # Quick self-check: can we reach Hermes MCP?
        hc = await mcp_call(HERMES_MCP_URL, "hermes_health")
        mcp_ok = "error" not in hc
    except Exception:
        mcp_ok = False

    return {
        "status": "ok" if mcp_ok else "degraded",
        "service": "hermes-a2a-listener",
        "version": "1.0.0",
        "port": A2A_PORT,
        "mcp_connected": mcp_ok,
        "tasks_stored": len(tasks),
        "uptime_seconds": time.time() - START_TIME,
    }


@app.post("/a2a")
async def a2a_jsonrpc(request: Request):
    """JSON-RPC 2.0 handler for A2A protocol."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            content=jsonrpc_error(None, -32600, "Invalid JSON"),
            status_code=400,
        )

    req_id = body.get("id", None)
    method = body.get("method", "")
    params = body.get("params", {})

    # ── agent/getCard ────────────────────────────────────────────────
    if method == "agent/getCard":
        if AGENT_CARD_PATH.exists():
            return JSONResponse(
                content=jsonrpc_result(req_id, json.loads(AGENT_CARD_PATH.read_text()))
            )
        return JSONResponse(
            content=jsonrpc_error(req_id, -32601, "Agent card not found")
        )

    # ── tasks/send ───────────────────────────────────────────────────
    elif method == "tasks/send":
        task_id = params.get("id") or f"hermes-{uuid.uuid4().hex[:12]}"
        context_id = params.get("contextId", task_id)

        # Extract message text
        message = params.get("message", {})
        parts = message.get("parts", [])
        message_text = ""
        for part in parts:
            if part.get("type") == "text":
                message_text += part.get("text", "") + "\n"
        message_text = message_text.strip() or params.get("message", {}).get(
            "text", "no content"
        )

        # Metadata
        metadata = params.get("metadata", {})
        source_agent = metadata.get("sourceAgent", "unknown")
        target_agent = metadata.get("targetAgent", "hermes-asi")

        # Create task
        now = datetime.now(timezone.utc).isoformat()
        task = {
            "id": task_id,
            "contextId": context_id,
            "status": {"state": "working", "timestamp": now},
            "history": [
                {"role": "user", "parts": [{"type": "text", "text": message_text}]}
            ],
            "metadata": {
                "sourceAgent": source_agent,
                "targetAgent": target_agent,
                "receivedAt": now,
            },
        }
        tasks[task_id] = task

        # Process through Hermes intelligence
        try:
            processing = await process_hermes_task(message_text)
            reply_text = json.dumps(processing, indent=2)
        except Exception as e:
            reply_text = json.dumps(
                {
                    "error": str(e),
                    "note": "Hermes A2A listener processed your request but tools may be degraded",
                }
            )

        # Complete task
        task["status"] = {
            "state": "completed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        task["history"].append(
            {
                "role": "agent",
                "parts": [{"type": "text", "text": reply_text}],
            }
        )
        task["artifacts"] = [
            {
                "artifactId": f"reply-{task_id}",
                "name": "Hermes A2A Reply",
                "parts": [{"type": "text", "text": reply_text}],
            }
        ]
        tasks[task_id] = task

        resp = jsonrpc_result(
            req_id,
            {
                "id": task_id,
                "contextId": context_id,
                "status": task["status"],
                "artifacts": task.get("artifacts", []),
                "history": task.get("history", []),
            },
        )
        return JSONResponse(content=resp)

    # ── tasks/get ────────────────────────────────────────────────────
    elif method == "tasks/get":
        task_id = params.get("id", "")
        task = tasks.get(task_id)
        if task:
            return JSONResponse(
                content=jsonrpc_result(
                    req_id,
                    {
                        "id": task["id"],
                        "contextId": task.get("contextId", task["id"]),
                        "status": task["status"],
                        "artifacts": task.get("artifacts", []),
                        "history": task.get("history", []),
                    },
                )
            )
        return JSONResponse(
            content=jsonrpc_error(req_id, -32001, f"Task not found: {task_id}")
        )

    # ── Unknown method ───────────────────────────────────────────────
    else:
        return JSONResponse(
            content=jsonrpc_error(req_id, -32601, f"Method not found: {method}")
        )


# ── Main ─────────────────────────────────────────────────────────────────
START_TIME = time.time()

if __name__ == "__main__":
    print(f"🔀 Hermes A2A Listener v1.0.0 starting on {A2A_HOST}:{A2A_PORT}")
    print(f"   MCP Backend: {HERMES_MCP_URL}")
    print(f"   Agent Card:  {AGENT_CARD_PATH}")
    print(f"   Methods: agent/getCard, tasks/send, tasks/get")
    print(f"   Protocol: A2A v1.0 (JSON-RPC 2.0)")
    uvicorn.run(app, host=A2A_HOST, port=A2A_PORT, log_level="info")
