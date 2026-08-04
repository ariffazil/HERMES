# FED Routing Gap Fix — Session 2026-08-05

## Problem
qwen-token-plan-team was LIVE (6 models, 480ms, all HEALTH= LIVE) but never appeared in `fed_route` output. Track A was deepseek-only (single point of failure).

## Root Cause
`fed_route_engine()` in `/root/AAA/scripts/fed_router.py` only considers providers listed in the `MODEL_ROUTES` dictionary. qwen-token-plan-team was NOT in `MODEL_ROUTES` despite being fully operational.

## Diagnosis Path
```
fed_route → returns only deepseek + mulerouter
→ grep "qwen-token-plan-team" fed_router.py → NOT in MODEL_ROUTES
→ grep in pricing table only → confirmed missing
→ ROOT CAUSE: routing dict, not health/balance
```

## Fix Applied
1. Added 4 new MODEL_ROUTES entries: `qwen3.6-flash`, `qwen3.7-plus`, `kimi-k2.7-code`, plus `qwen-token-plan-team` as P2 for `deepseek-v4-pro` and `deepseek-v4-flash`
2. Updated FED DB balance: $0 → $150 (seat-based, 3 seats × $50)
3. Promoted track: B → A
4. Restarted fed-router.service
5. Verified via fed_route MCP tool

## Balance Gate False Positive
qwen-token-plan-team showed $0 balance = token consumption, not capacity. FED balance gate applied `LOW_BALANCE_SOFT` demotion. Fix: update `providers.balance_usd` to reflect seat value.

## Verification Commands
```bash
# Check if provider is in MODEL_ROUTES
sed -n '/^MODEL_ROUTES/,/^}/p' /root/AAA/scripts/fed_router.py | grep "PROVIDER_NAME"

# Check FED DB state
sqlite3 /root/.local/share/arifos/token_bank.db \
  "SELECT provider_name, track_type, balance_usd, confidence_score FROM providers;"

# Syntax check after patch
python3 -c "import py_compile; py_compile.compile('/root/AAA/scripts/fed_router.py', doraise=True)"

# Restart
systemctl restart fed-router.service
```

## OpenRouter Conscious Archive
$0.50, ARCHIVED, BLIND, not in litellm-config or MODEL_ROUTES. FLAME covers free-tier as Tier-3 fallback. Conscious decision to leave archived — low value, no action needed.

## Final Track A State
| Provider | Track | Balance | Models | Latency |
|----------|-------|---------|--------|---------|
| deepseek | A | $13.81 | deepseek-v4-pro, deepseek-v4-flash | 592ms |
| qwen-token-plan-team | A | $150.00 | qwen3.6-flash, deepseek-v4-pro, glm-5.2, qwen3.7-plus, deepseek-v4-flash, kimi-k2.7-code | 480ms |
