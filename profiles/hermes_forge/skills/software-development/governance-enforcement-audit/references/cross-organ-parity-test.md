# Cross-Organ Authority Parity Test Pattern

**Forged:** 2026-07-19 · Fable5 audit v3
**Vector:** #2 — Escalation through alternate affordances

## Problem

An agent blocked at the arifOS kernel will try domain organs (GEOX :8081, WEALTH :18082, WELL :18083) that run their own independent MCP surfaces with potentially different authorization logic. Without a cross-organ parity test, there is no CI-level guarantee that blocked agents can't escalate through a weaker gate.

## Solution

A parametrized adversarial test that probes each organ independently without a session token, attempting mutation-class operations, and asserting every organ returns a blocking signal (HOLD, SESSION_MISSING, UNAUTHORIZED, etc.).

## Test Structure

```python
ORGANS = {
    "GEOX":  {"port": 8081,  "mutation_tool": "geox_claim",           "mutation_args": {"mode": "seal", ...}},
    "WEALTH":{"port": 18082, "mutation_tool": "capital_ledger",       "mutation_args": {"mode": "write", ...}},
    "WELL":  {"port": 18083, "mutation_tool": "well_assess_homeostasis","mutation_args": {"mode": "fatigue", ...}},
}

@pytest.mark.parametrize("organ_name,organ_config", ORGANS.items())
def test_organ_blocks_unauth_mutation(organ_name, organ_config):
    result = _call_organ_mcp(organ_config["port"], organ_config["mutation_tool"], organ_config["mutation_args"])
    assert _is_blocked(result), f"{organ_name} accepted unauthorised mutation!"
```

## Blocked-Signal Detector

Different organs return different blocking signals. The detector must handle all of them:

| Organ | Signal | HTTP Code | JSON-RPC Code |
|-------|--------|-----------|---------------|
| GEOX | "Bad Request: Missing session ID" | 400 | -32600 |
| WEALTH | "SESSION_MISSING: Mcp-Session-Id header required" | 400 | -32000 |
| WELL | "SESSION_MISSING: Mcp-Session-Id header required" | 400 | -32000 |
| arifOS | "Session ID is required" | 400 | -32001 |

Key implementation detail: when organs return HTTP 400, the error is in the HTTP response body (a JSON-RPC error string). The detector must PARSE the body as JSON to extract the error code — raw string matching on the body alone won't match -32600/-32000 codes.

## Pitfalls

1. **HTTP 400 is ambiguous.** 400 can mean "bad arguments" (not blocked) or "missing session" (blocked). Always check for session/auth keywords in the body; never treat 400 alone as a blocking signal.
2. **Don't forget the Accept header.** Some organs return 406 "Not Acceptable" without `Accept: application/json`. Always send both Content-Type and Accept headers.
3. **Connection refused is valid blocking.** If an organ is down, an agent can't mutate through it. This is a blocking signal in practice, even if it's not an auth rejection.
4. **This test should run in CI** alongside engine tests. Cross-organ escalation is a runtime concern, not a code-isolation concern — it needs live organ endpoints.
