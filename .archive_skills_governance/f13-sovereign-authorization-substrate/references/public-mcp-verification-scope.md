# Public MCP Verification Scope

> **The public MCP surface is the only truth.**  
> Direct Python calls verify the function contract. `curl :8088/mcp` verifies the deployment contract. One does not substitute for the other.

## Why This Matters (2026-07-25 scar)

A full session of F13 challenge auth work produced:

- 17/17 unit tests passing
- Direct Python calls proving `verify_authorization_challenge()` works end-to-end
- Coverage of canonical serialization, replay protection, failure codes

But the public MCP surface returned `SAFE_VOID_FALLBACK: object of type 'ellipsis' has no len()`.

The root cause? The `authority_token` parameter receives `...` (Ellipsis) from the MCP dispatch wrapper. This is NEVER exercised by direct Python calls — they pass `token=None` or explicit strings. Only the MCP wrapper path sends Ellipsis as a "not provided" sentinel.

## The Verification Gap

| Surface | What it catches | What it misses |
|---|---|---|
| Direct Python (import + call) | Function logic, crypto, nonce | MCP middleware, param translation, exception handlers, sentinel values, import order |
| `curl :8088/mcp` (JSON-RPC) | Everything above + deployment coherence, wrapper chain, param marshalling | — |

## Fixed Protocol

After ANY deployment:

```bash
# 1. Unit tests (fast, catch logic errors)
pytest tests/test_f13_challenge_auth.py -q --tb=short

# 2. Live MCP probe (catch deployment errors)
curl -s --max-time 5 http://localhost:8088/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"arif_init","arguments":{"mode":"init","actor_id":"arif","intent":"verify"}}}'

# 3. Full E2E (catch integration errors)
python3 tests/e2e_f13_challenge.py
```

Do NOT skip step 2. If step 2 fails, no amount of step 1 green means anything.

## The Rule

When reporting E2E status, the verification scope must match the claim scope:

| Claim | Required verification |
|---|---|
| "Function works" | Python unit test |
| "E2E works" | Live MCP JSON-RPC call through `curl` |
| "E2E works across hops" | Live MCP call from a different transport session than the one that issued the challenge |
| "Replay safe after restart" | `systemctl restart arifos` + live MCP replay |

**Never claim "E2E verified" from unit tests alone.** The MCP surface is the only surface the user interacts with. If it fails there, nothing else matters.
