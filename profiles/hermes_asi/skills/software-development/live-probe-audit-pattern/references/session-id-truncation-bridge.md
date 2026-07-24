# Session ID Truncation Bug — arifOS → GEOX Bridge

**Discovered:** 2026-07-19
**Severity:** High — blocks strict-binding GEOX tools from `arif_route` bridge
**Status:** Documented, awaiting F13 authorization to investigate root cause

## The Pattern

`arif_init` produces session IDs of this shape:

```
SEAL-XXXXXXXXXXXXXXXX   (22 chars: SEAL- + 16 hex chars)
```

When this session_id is passed through `arif_route` → `arif_bridge` → GEOX MCP, the
downstream organ receives a **truncated** session_id:

```
SEAL-XXXXXXXXXXX        (19 chars: SEAL- + 13 hex chars)
```

The downstream organ rejects with `SESSION_INVALID`.

## Reproduction

```bash
# Step 1: init session, capture ID
SESS=$(curl -s -X POST http://localhost:8088/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"arif_init","params":{"actor_id":"HERMES"}}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['session_birth']['session_id'])")
echo "init returned: $SESS (len=${#SESS})")

# Expected: SEAL-XXXXXXXXXXXXXXXX (len=22)
# If len < 22, arif_init itself is truncating — different bug

# Step 2: pass through arif_route bridge
curl -s -X POST http://localhost:8088/mcp \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"arif_route\",\"params\":{
    \"intent\":\"Sabah basin test\",
    \"organ\":\"GEOX\",
    \"organ_tool\":\"geox_basin\",
    \"arguments\":{\"mode\":\"profile\",\"name\":\"Sabah\"},
    \"session_id\":\"$SESS\"
  }}"
# Look for: "arifOS rejected session_id (unknown, expired, or forged): SEAL-..."
# Truncated ID in the error message will be 19 chars
```

## What works vs what fails (through bridge)

| Tool | Binding | Status |
|------|---------|--------|
| `geox_basin(mode=profile)` | low | ✅ works through bridge |
| `geox_basin(mode=macrostrat)` | low | ✅ works through bridge |
| `geox_prospect(mode=screen)` | low | ✅ works through bridge |
| `geox_deep_time_state` | low | ✅ works through bridge |
| `geox_petrophysics(mode=*)` | strict | ❌ SESSION_INVALID |
| `geox_seismic_compute(mode=*)` | strict | ❌ SESSION_INVALID |
| `geox_well_desk(mode=*)` | strict | ❌ SESSION_INVALID |
| `geox_claim(mode=*)` | strict | ❌ SESSION_INVALID |

## Workarounds (until root-cause fixed)

1. **Use low-binding tools only** through bridge. `geox_deep_time_state` is the workhorse —
   it has minimal session requirements and works through `arif_route`.
2. **Call GEOX directly via curl**, bypassing `arif_route` bridge entirely. This needs
   the full session_id (22 chars) passed directly. Most reliable path for strict-binding tools.
3. **Generate a synthetic cube** at the GEOX layer without session, since petrophysics
   has `use_synth_cube=True` default — this lets you run petrophysics computation
   without a real well, sidestepping the session binding.

## Root cause hypothesis (unverified)

Likely site: `arifosmcp/runtime/rest_routes/rest_routes.py` or
`arifosmcp/kernel/interceptor.py` in arifOS repo. The bridge passes the session_id
through a path that has implicit string-bound truncation. Search candidate:

```python
session_id = session_id[:19]   # or
if len(session_id) > 19: session_id = session_id[:19]   # or
session_id = session_id.split('-')[0] + '-' + session_id.split('-')[1][:13]
```

## Why this matters

- **~88% of GEOX tools** (counting strict-binding) are unreachable through the federation bridge
- Agents using `arif_route` for geoscience work get locked out of the highest-value tools
- The bridge is the canonical path; bypassing it violates F1 AMANAH (no audit trail)

## Required actions (888_HOLD)

1. **Investigate** the actual truncation site in arifOS code — read rest_routes.py
   and interceptor.py line by line around session_id handling.
2. **Confirm** the hypothesis by reproducing with controlled inputs.
3. **Fix** in-place with a patch + test (regression test that 22+ char session_ids
   pass through unchanged).
4. **Commit** per federation git-first deploy pattern, push, redeploy arifOS.
5. **Seal** the fix with arif_seal.

Do NOT auto-investigate without F13 authorization. Session handling is
constitutional-adjacent (governance plumbing).