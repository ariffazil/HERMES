# FED MODEL_ROUTES Gap — Fix Pattern

> Session: 2026-08-04. qwen-token-plan-team invisible in fed_route.

## Problem

Provider is LIVE, has models in `route_health`, has latency in `route_latency`,
is configured in Hermes config — but `fed_route` MCP tool never returns it.

## Root Cause

FED MCP router (`/root/AAA/scripts/fed_router.py`) uses `MODEL_ROUTES`
dictionary to determine routing cascades. Only providers listed in this
dictionary appear in `fed_route` output. The dictionary is **static Python**,
not read from the database.

## Diagnosis

```bash
# Check if provider has routes
sed -n '/^MODEL_ROUTES/,/^}/p' /root/AAA/scripts/fed_router.py | \
  grep -c "provider-name-here"
# 0 = NOT in MODEL_ROUTES = invisible

# Check what models the provider supports
sqlite3 /root/.local/share/arifos/token_bank.db \
  "SELECT model_id FROM route_health WHERE provider_name='provider-name' AND status='LIVE';"
```

## Fix Pattern

1. Add entries to `MODEL_ROUTES` for each model the provider supports
2. Set `router: "direct"` for direct API access, `router: "gateway"` for proxy
3. Set priority (lower = better). Existing providers get bumped up
4. `constitutional: False` for non-governed providers
5. Restart: `systemctl restart fed-router.service`
6. Verify: query `fed_route` for each model

### Balance fix for seat-based plans

FED balance gate demotes providers with balance < $5.00. Seat-based plans
need balance set to seat value:

```bash
sqlite3 /root/.local/share/arifos/token_bank.db \
  "UPDATE providers SET balance_usd = 150.0 WHERE provider_name = 'qwen-token-plan-team';"
```

### Track promotion

```bash
sqlite3 /root/.local/share/arifos/token_bank.db \
  "UPDATE providers SET track_type = 'A' WHERE provider_name = 'provider-name';"
```

## qwen-token-plan-team Specifics (2026-08-04)

**Models LIVE:** qwen3.6-flash, deepseek-v4-pro, glm-5.2, qwen3.7-plus,
deepseek-v4-flash, kimi-k2.7-code

**Routes added:**
- `deepseek-v4-pro`: qwen P2 (deepseek stays P1 for constitutional)
- `deepseek-v4-flash`: qwen P2
- `qwen3.6-flash`: qwen P1 (NEW entry, didn't exist)
- `qwen3.7-plus`: qwen P1 (NEW entry, didn't exist)
- `glm-5.2`: qwen P2 (tokenrouter stays P1, free)
- `kimi-k2.7-code`: qwen P1 (NEW entry, didn't exist)

**Balance:** $150 (3 seats × $50/mo seat value)
**Track:** Promoted B → A
