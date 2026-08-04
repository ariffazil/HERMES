# FED Routing Patch Workflow

> Session: 2026-08-05 — FED 3/3 gaps fix (qwen Track A + OpenRouter archive)

## File Locations

- **Route table**: `/root/AAA/scripts/fed_router.py` — `MODEL_ROUTES` dict (line ~184–400)
- **Service**: `fed-router.service` on port 7074 (MCP server)
- **State DB**: `/root/.local/share/arifos/token_bank.db` (providers, route_health, route_latency)

## Adding a New Provider Route

1. Read existing MODEL_ROUTES for target models
2. Add entries with: `provider`, `router` (direct/gateway), `class` (direct/gateway/gateway_shadowed), `constitutional` (True for sovereign), `shadow`, `priority`
3. Renumber existing priorities if inserting between
4. Update FED provider record in token_bank.db if needed
5. `systemctl restart fed-router.service`
6. Verify with `fed_route` MCP tool

## Seat-Based Provider Balance Fix

Providers with seat-based pricing (e.g., qwen-token-plan-team) show $0 balance. The routing engine's balance gate applies `LOW_BALANCE_SOFT`, pushing them below gateway providers.

**Fix**: Update `balance_usd` in providers table to reflect seat value (e.g., $50/seat × 3 seats = $150), not token consumption.

```sql
UPDATE providers 
SET balance_usd = 150.0, 
    notes = 'Seat-based, NOT token-based. Balance = seat value.'
WHERE provider_name = 'qwen-token-plan-team';
```

## Conscious Archive Pattern

If a provider is all of:
- ARCHIVED status
- Near-empty balance
- Not in litellm-config.yaml
- Not in MODEL_ROUTES
- BLIND (can't probe balance)

→ Update notes with conscious decision rationale. Don't waste time re-probing.

## Production Change Rule

**Always show exact patch for review before applying to fed_router.py.** User enforced 2026-08-05. Never blind-patch production routing files.

## FED Route Engine Filtering (10 steps)

1. FILTER: remove DEAD providers
2. HEALTH GATE: skip DEGRADED, demote RATE_LIMITED
3. RANK: by priority class (direct > gateway > shadowed)
4. BOOST: vision modality → push VL-capable providers up
5. DEGRADE: constitutional ≥ 666 → direct ONLY
6. BALANCE GATE: dual-track (API hard, Token Bank soft, UNVERIFIABLE bypass)
7. LATENCY GATE: demote if p95 > 5s
8. TELEMETRY GATE: demote routes with < 10 samples
9. COST SURFACE: attach estimated cost per 1K tokens
10. RETURN: top 3 routes with reasoning
