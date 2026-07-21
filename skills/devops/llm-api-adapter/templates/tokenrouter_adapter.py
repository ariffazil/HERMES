"""
TokenRouter Adapter — Chat Completions ↔ Responses API bridge
Hermes → localhost:9999/v1/chat/completions → TokenRouter API

ΔS ≤ 0: Reversible adapter, no permanent state, keys never leave this process.

Usage:
    TOKENROUTER_API_KEY=sk-... \\
    DEEPSEEK_API_KEY=sk-... \\
    ANTHROPIC_API_KEY=sk-ant-... \\
    python3 adapter.py

Then configure Hermes:
    hermes config set model.provider "custom:adapter"
    hermes config set model.base_url "http://127.0.0.1:9999/v1"
    hermes config set model.api_key "none"
"""

import os
import httpx
from fastapi import FastAPI, Request, HTTPException

app = FastAPI(title="TokenRouter Adapter", version="1.0.0")

TOKENROUTER_URL = os.getenv("TOKENROUTER_URL", "https://api.tokenrouter.com/v1/responses")
TOKENROUTER_API_KEY = os.getenv("TOKENROUTER_API_KEY", "")


@app.get("/health")
async def health():
    """Health check for Hermes to probe."""
    return {"status": "ok", "adapter": "tokenrouter-bridge", "target": TOKENROUTER_URL}


@app.post("/v1/chat/completions")
async def proxy_chat_completions(request: Request):
    """Translate OpenAI Chat Completions → TokenRouter Responses API."""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload from Hermes")

    # ── 1. EMD Translate: Chat Completions → Responses API ──
    messages = body.get("messages", [])
    prompt_parts = []
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        if isinstance(content, list):
            text_parts = [p.get("text", "") for p in content if p.get("type") == "text"]
            content = " ".join(text_parts)
        prompt_parts.append(f"[{role}]: {content}")

    system_msg = body.get("instructions", "")
    if system_msg:
        prompt_parts.insert(0, f"[system]: {system_msg}")

    prompt = "\n\n".join(prompt_parts)

    model = body.get("model", "auto:balance")
    # TokenRouter uses provider/model format (slash, not colon)
    # Only add auto: prefix if model has no routing prefix
    if ":" not in model and "/" not in model and model != "auto":
        model = f"auto:{model}"

    payload = {
        "model": model,
        "input": prompt,
    }

    for key in ("temperature", "max_tokens", "max_output_tokens"):
        if key in body:
            payload[key] = body[key]

    # ── 2. Header Injection (BYOK Sovereignty) ──
    # CRITICAL (2026-07-20): TokenRouter REQUIRES Accept + User-Agent headers.
    # Without them the server returns 500 (crash before auth), not 401.
    headers = {
        "Authorization": f"Bearer {TOKENROUTER_API_KEY}",
        "Accept": "application/json",
        "User-Agent": "Tokenrouter/Python 1.2.1",
    }

    for provider, env_var in [
        ("X-OpenAI-Key", "OPENAI_API_KEY"),
        ("X-Anthropic-Key", "ANTHROPIC_API_KEY"),
        ("X-Gemini-Key", "GEMINI_API_KEY"),
        ("X-Mistral-Key", "MISTRAL_API_KEY"),
        ("X-DeepSeek-Key", "DEEPSEEK_API_KEY"),
    ]:
        key = os.getenv(env_var, "")
        if key:
            headers[provider] = key

    # ── 3. Forward to TokenRouter ──
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            resp = await client.post(TOKENROUTER_URL, json=payload, headers=headers)
            resp.raise_for_status()
            tr_data = resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"TokenRouter returned error: {e.response.text[:500]}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=502,
                detail=f"TokenRouter unreachable: {str(e)}"
            )

    # ── 4. EMD Decode: Responses API → Chat Completions ──
    # TokenRouter returns output as nested array:
    # {"output":[{"type":"message","content":[{"type":"output_text","text":"..."}]}]}
    result_text = None

    raw_output = tr_data.get("output")
    if isinstance(raw_output, list):
        for item in raw_output:
            if isinstance(item, dict) and item.get("type") == "message":
                content_list = item.get("content", [])
                for c in content_list:
                    if isinstance(c, dict) and c.get("type") == "output_text":
                        result_text = c.get("text")
                        break
                if result_text:
                    break
        if result_text is None:
            result_text = str(raw_output)
    elif isinstance(raw_output, str):
        result_text = raw_output

    # Fallbacks
    if result_text is None:
        result_text = tr_data.get("response") or tr_data.get("text") or tr_data.get("content")

    if result_text is None and "choices" in tr_data:
        choices = tr_data.get("choices", [])
        if choices:
            msg = choices[0].get("message", {}) or choices[0].get("text", "")
            result_text = msg.get("content", str(msg)) if isinstance(msg, dict) else str(msg)

    if result_text is None and "data" in tr_data:
        result_text = str(tr_data["data"])

    if result_text is None:
        result_text = str(tr_data)

    model_used = (
        tr_data.get("model")
        or tr_data.get("routed_model")
        or body.get("model", "unknown")
    )

    return {
        "id": f"chatcmpl-tr-{tr_data.get('id', 'local')}",
        "object": "chat.completion",
        "created": tr_data.get("created", 0),
        "model": model_used,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": result_text,
            },
            "finish_reason": tr_data.get("finish_reason", "stop"),
        }],
        "usage": tr_data.get("usage", {}),
        "_tokenrouter": {
            "cost_usd": tr_data.get("cost_usd"),
            "latency_ms": tr_data.get("latency_ms"),
            "provider": tr_data.get("provider"),
        },
    }


@app.get("/v1/models")
async def list_models():
    """Passthrough model list from TokenRouter."""
    headers = {"Authorization": f"Bearer {TOKENROUTER_API_KEY}"} if TOKENROUTER_API_KEY else {}
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(
                TOKENROUTER_URL.replace("/v1/responses", "/v1/models"),
                headers=headers,
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
    return {"object": "list", "data": []}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999, log_level="info")
