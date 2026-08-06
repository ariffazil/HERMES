#!/usr/bin/env python3
"""
arifFlow Ingest Bridge — Hermes/OpenClaw/OpenCode → arifFlow metabolic nerve.

Routes through A-FORGE MCP (:7072) with arifOS SCT session token.
Emits flow receipts so FQ measures the FULL federation metabolism.

Usage:
  python3 /root/HERMES/scripts/arifflow_ingest.py \
    --actor "hermes-gateway" --session "hermes-auto" \
    --step_type "Route" --epistemic "Observation" --floor_verdict "Pass"

Forged: 2026-08-06 by 333-AGI Δ MIND — "make arifFlow feel every organ"
DITEMPA BUKAN DIBERI
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

ARIFOS_MCP = "http://127.0.0.1:8088/mcp"
AFORGE_MCP = "http://127.0.0.1:7072/mcp"
SCT_CACHE = "/root/.local/share/arifos/current_sct.txt"


def get_sct():
    """Get SCT from cache or fresh arif_init."""
    if os.path.exists(SCT_CACHE):
        try:
            with open(SCT_CACHE) as f:
                token = f.read().strip()
                if token.startswith("sct_v1."):
                    return token
        except Exception:
            pass
    try:
        payload = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "arif_init",
                    "arguments": {
                        "actor_id": "hermes-gateway",
                        "intent": "arifFlow metabolic bridge",
                        "mode": "light",
                    },
                },
            }
        ).encode()
        req = urllib.request.Request(
            ARIFOS_MCP, data=payload, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            inner = json.loads(json.loads(resp.read())["result"]["content"][0]["text"])
            sct = inner.get("session_token", "")
            if sct:
                os.makedirs(os.path.dirname(SCT_CACHE), exist_ok=True)
                with open(SCT_CACHE, "w") as f:
                    f.write(sct)
                return sct
    except Exception:
        pass
    return None


def ingest_flow(actor, session, step_type, step_number, epistemic, verdict):
    """Ingest via A-FORGE MCP which proxies to arifFlow with SCT."""
    sct = get_sct()
    payload = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "arifflow_flow_ingest",
                "arguments": {
                    "actor_id": actor,
                    "session_id": session,
                    "step_type": step_type,
                    "step_number": step_number,
                    "epistemic_label": epistemic,
                    "floor_verdict": verdict,
                    "session_token": sct,
                    "witness_organs": ["hermes"],
                },
            },
        }
    ).encode()
    try:
        req = urllib.request.Request(
            AFORGE_MCP, data=payload, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read())
            r = result.get("result", {})
            if r.get("isError"):
                return {"status": "REJECTED", "detail": r["content"][0]["text"][:120]}
            return {"status": "INGESTED", "detail": "ok"}
    except urllib.error.HTTPError as e:
        return {"status": "HTTP_ERROR", "detail": str(e.code)}
    except Exception as e:
        return {"status": "ERROR", "detail": str(e)[:120]}


def main():
    parser = argparse.ArgumentParser(description="arifFlow metabolic bridge")
    parser.add_argument("--actor", default="hermes-gateway")
    parser.add_argument("--session", default="hermes-auto")
    parser.add_argument(
        "--step_type",
        default="Execute",
        choices=["Execute", "Verify", "Cool", "Seal", "Barrier", "Merge", "Route"],
    )
    parser.add_argument("--step_number", type=int, default=1)
    parser.add_argument(
        "--epistemic",
        default="Observation",
        choices=[
            "Observation",
            "Derivation",
            "Interpretation",
            "Specification",
            "Seal",
        ],
    )
    parser.add_argument(
        "--floor_verdict", default="Pass", choices=["Pass", "Caution", "Hold", "Void"]
    )
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    result = ingest_flow(
        args.actor,
        args.session,
        args.step_type,
        args.step_number,
        args.epistemic,
        args.floor_verdict,
    )

    if not args.quiet:
        print(
            f"arifFlow: {result['status']} | actor={args.actor} step={args.step_type}"
        )

    return 0  # Never fail — arifFlow is augmentation


if __name__ == "__main__":
    sys.exit(main())
