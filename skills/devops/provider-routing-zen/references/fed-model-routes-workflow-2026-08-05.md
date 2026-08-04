# FED MODEL_ROUTES Workflow — Session 2026-08-05

## Problem
qwen-token-plan-team had 6 LIVE models (450ms p50) but ZERO entries in `MODEL_ROUTES` dictionary in `/root/AAA/scripts/fed_router.py`. FED route engine only considers providers listed in MODEL_ROUTES — so qwen never appeared in route output.

## Root Cause
`fed_route_engine()` line: `routes = MODEL_ROUTES.get(model, MODEL_ROUTES.get("deepseek-v4-pro", []))` — if model not in dict, falls back to deepseek routes only. qwen models (qwen3.6-flash, qwen3.7-plus, glm-5.2, kimi-k2.7-code) were never added.

## Fix Applied (2026-08-05)

### Changes to MODEL_ROUTES in fed_router.py:
1. **deepseek-v4-pro**: Inserted qwen-token-plan-team as P2 (between deepseek P1 direct and mulerouter P3). deepseek retains `constitutional: True`.
2. **deepseek-v4-flash**: Same pattern — qwen as P2.
3. **NEW: qwen3.6-flash** — qwen P1 direct → mulerouter P2 gateway.
4. **NEW: qwen3.7-plus** — qwen P1 direct → mulerouter P2 gateway.
5. **glm-5.2**: Added qwen as P2 after existing tokenrouter P1 (free).
6. **NEW: kimi-k2.7-code** — qwen P1 direct → mulerouter P2 gateway.

### Route entry template:
```python
{
    "provider": "qwen-token-plan-team",
    "router": "direct",
    "class": "direct",
    "constitutional": False,
    "shadow": None,
    "priority": N,
},
```

### Balance gate fix:
qwen-token-plan-team showed $0 balance → `LOW_BALANCE_SOFT` demotion.
Seat-based provider: 3 seats × ~$50/seat = $150 value.
Fix: `UPDATE providers SET balance_usd=150.0 WHERE provider_name='qwen-token-plan-team';`
Promoted to Track A.

## Decision Framework: Fix vs Archive Provider

| Signal | Action |
|--------|--------|
| Provider LIVE, models available, but not in MODEL_ROUTES | Add routes |
| Provider LIVE but $0 balance (seat-based) | Update balance to seat value |
| Provider ARCHIVED, <$1 balance, BLIND probe, not in litellm-config | Conscious archive |
| Provider in FLAME free-tier as fallback | No FED route needed |

## Verification Commands
```bash
# Check if model has routes
grep -A10 '"MODEL_NAME"' /root/AAA/scripts/fed_router.py

# Test routing via MCP
# fed_route tool with model parameter

# Restart after patch
systemctl restart fed-router.service
```

## Pitfall: Review before apply
User explicitly requested seeing the exact patch before applying to production FED files. Always show the diff first — `fed_router.py` is production infrastructure.
