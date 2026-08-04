# FED Routing Diagnostic Pitfalls

> Added: 2026-08-05 — Session: FED gap fix (qwen-token-plan-team Track A)
> Covers: MODEL_ROUTES disconnect, seat-based balance trap

## Pitfall #1: FED Provider LIVE ≠ Routable (MODEL_ROUTES Disconnect)

**Symptom:** `fed_status` shows provider as LIVE, `route_health` shows models as LIVE, but `fed_route` never returns that provider in route output.

**Root Cause:** `fed_route_engine()` in `/root/AAA/scripts/fed_router.py` only considers providers listed in the `MODEL_ROUTES` dictionary (line ~184). A provider can be LIVE in the FED database but have zero entries in `MODEL_ROUTES` — making it invisible to routing.

**Diagnostic Pattern:**
```
1. fed_status          → check provider exists + LIVE
2. fed_route (model)   → check if provider appears in route output
3. grep MODEL_ROUTES   → verify model has entries in fed_router.py
4. sqlite3 route_health → confirm model-health status
```

**Fix:** Add provider as route entry in `MODEL_ROUTES` dict in `fed_router.py`. Each model needs explicit `{provider, router, class, constitutional, shadow, priority}` entries. Service restart required after patch.

**Real case (2026-08-05):** qwen-token-plan-team had 6 LIVE models, 450ms latency, but ZERO routes in MODEL_ROUTES. FED never routed to it. Fixed by adding 6 route entries.

---

## Pitfall #2: Seat-Based Provider Balance Trap

**Symptom:** Provider shows `balance_usd: 0.0` with `balance_flag: LOW_BALANCE_SOFT` in `fed_route` output. Route gets demoted to rank 3+ despite being fast and healthy.

**Root Cause:** FED's balance gate (`fed_route_engine` Step 6) treats all providers as token-credit based. Seat-based providers (e.g., Qwen Token Plan Team) use allocated seats, not consumed tokens — `$0 balance` means zero tokens consumed, NOT zero capacity.

**Fix:** Update provider balance in `providers` table to reflect seat value:
```sql
UPDATE providers SET balance_usd = <seat_value_usd>
WHERE provider_name = '<provider>';
```
Seat value = seats × monthly_cost_per_seat. Example: 3 seats × $50/seat = $150.

**Verify:** Re-run `fed_route` — `balance_flag` should clear, rank should improve.

**Real case (2026-08-05):** qwen-token-plan-team at $0 balance triggered `LOW_BALANCE_SOFT`, pushing it to rank 3. Updated to $150 (seat value) → balance_flag cleared, rank improved to 2.

---

## MODEL_ROUTES Entry Template

When adding a new provider route, use this template:

```python
"model-name": [
    {
        "provider": "provider-name",
        "router": "direct",          # "direct" for API, "gateway" for proxy
        "class": "direct",           # "direct", "gateway", or "gateway_shadowed"
        "constitutional": False,     # True ONLY for judge/seal/critical paths
        "shadow": None,              # shadow ref ID or None
        "priority": 1,               # Lower = higher priority
    },
    {
        "provider": "fallback-provider",
        "router": "gateway",
        "class": "gateway",
        "constitutional": False,
        "shadow": None,
        "priority": 2,
    },
],
```

**Constitutional rules:**
- `constitutional: True` — ONLY for providers handling judge (666), seal (999), or sovereign data
- `constitutional: False` — all other routes
- DeepSeek direct routes retain `constitutional: True` for judge/seal paths

**Priority conventions:**
- P1: Primary direct route
- P2: Secondary direct or fast gateway
- P3+: Fallback gateways
- P8+: Heavily demoted (rate-limited, shadowed)

---

## FED Route Engine Steps (for reference)

The 10-step `fed_route_engine` in `fed_router.py`:

1. **FILTER** — remove DEAD providers
2. **HEALTH GATE** — skip DEGRADED, demote RATE_LIMITED
3. **RANK** — by priority class (direct > gateway > shadowed)
4. **BOOST** — vision modality → push VL-capable providers up
5. **DEGRADE** — constitutional ≥ 666 → direct ONLY
6. **BALANCE GATE** — dual-track (API hard, Token Bank soft, UNVERIFIABLE bypass)
7. **LATENCY GATE** — demote if p95 > 5s
8. **TELEMETRY GATE** — demote routes with <10 samples
9. **COST SURFACE** — attach estimated cost per 1K tokens
10. **RETURN** — top 3 routes with reasoning
