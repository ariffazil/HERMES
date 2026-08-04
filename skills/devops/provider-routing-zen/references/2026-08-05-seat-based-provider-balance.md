# Seat-Based Provider Balance — FED Pitfall (2026-08-05)

## Problem

FED `fed_route_engine` balance gate demotes providers based on `balance_usd`:
- `< $1.00` → hard demotion (skipped)
- `< $5.00` → soft demotion (`LOW_BALANCE_SOFT` flag, pushed to lower rank)

Seat-based providers (e.g., Qwen Token Plan Team) show `$0.00` because the token consumption balance is zero — but the provider has active seats ($50/seat/mo value).

## Symptoms

- `fed_route` output shows `balance_flag: "LOW_BALANCE_SOFT"` for a LIVE provider
- Provider rank drops below gateway providers despite being direct + fast
- Example: qwen-token-plan-team (480ms, direct) ranked below mulerouter (2400ms, gateway) due to $0 balance

## Fix

```bash
# Update FED provider balance to reflect seat value
sqlite3 /root/.local/share/arifos/token_bank.db \
  "UPDATE providers SET balance_usd = 150.0, 
   notes = 'Seat-based plan. Balance = seat value, NOT token consumption.'
   WHERE provider_name = 'qwen-token-plan-team';"
```

After update, verify:
```bash
# Check route rank
# fed_route output should show no LOW_BALANCE_SOFT flag
```

## Key Distinction

| Metric | Meaning | Where |
|--------|---------|-------|
| `balance_usd` | Credit/seat value — used by balance gate | `providers` table |
| Token consumption | How much consumed — informational only | `route_health`, notes |

Don't confuse token consumption ($0) with credit balance ($150 seat value).

## Adding Routes to MODEL_ROUTES

When adding a new provider to FED routing cascade, edit `/root/AAA/scripts/fed_router.py`:

```python
# Pattern: add provider entry in MODEL_ROUTES dict
"model-name": [
    {
        "provider": "new-provider",
        "router": "direct",      # "direct" or "gateway"
        "class": "direct",       # "direct", "gateway", "gateway_shadowed"
        "constitutional": False, # True ONLY for deepseek-v4-pro
        "shadow": None,
        "priority": 1,           # Lower = better
    },
    {
        "provider": "existing-provider",
        "router": "gateway",
        "class": "gateway",
        "constitutional": False,
        "shadow": None,
        "priority": 2,           # Renumber existing entries
    },
],
```

After edit:
```bash
systemctl restart fed-router.service
```

Verify with `fed_route` MCP tool — should show new provider in cascade.
