# WEALTH Session Auth Gate — L11 AUTH Blocked Hermes FI-001

**Date:** 2026-07-29
**Agent:** Hermes Agent (FI-001, model=deepseek-v4-flash)
**Organ:** WEALTH (port 18083)
**Source task:** OpenCode entropy watch resolution — commit dirty files, route PETRONAS article

## The attempt

```
arif_init(mode='light', actor_id='Hermes-Agent-FI-001')
  → session_id='unknown', session_token=sct_v1.{...}, authority=OBSERVER

capital_market(mode='commodity', commodity='brent_crude',
               session_id='unknown', trace_id='trc-729dca675d29')
  → L11 AUTH: session_id required for all WEALTH tools (FORGE 2026-07-18: anonymous reads blocked)

wealth_institutional_stress_index(org_name='PETRONAS', ..., session_id='unknown')
  → L11 AUTH: session_id required

capital_entropy(mode='institutional', decision_makers=[...], ..., session_id='unknown')
  → L11 AUTH: session_id required

arif_route(intent='PETRONAS analysis...', organ='WEALTH', organ_tool='capital_market',
           arguments={...}, session_token='<sct_v1...>')
  → routing decision only (no bridge execution)
```

## Key findings

1. **`arif_init(mode='light')` → session_id='unknown'** — this is insufficient for WEALTH tools. The light mode doesn't bind a real session; it just returns a placeholder.
2. **WEALTH organ runs independent session gate** — `wealth-session-gate` is NOT the arifOS kernel's interceptor. It's the WEALTH organ's own middleware that checks for a valid session_id before any computation.
3. **Even with session_token passed, it doesn't help** — the WEALTH tools accept `session_id` and `session_token` parameters, but passing an 'unknown' session_id with a valid token still fails. Both are required.
4. **arif_route bridge mode is non-functional** — The schema exposes `organ_tool` + `arguments` for bridge calls, but the dispatcher doesn't execute them. Schema-reality gap.

## What would fix it

A real session requires either:
- `arif_init(mode='init', actor_id='ARIF', requested_authority='SOVEREIGN')` with Ed25519 signature → returns real session_id with SOVEREIGN authority
- Or use `arif-bind.py` / `sovereign-lease.py` which auto-generate the nonce + sign + init in one atomic step

## PETRONAS article data (captured for deferred WEALTH analysis)

See `/root/entropy-watch-seal-receipt-2026-07-29.md` for the complete structured data.

Key metrics:
| Metric | Budget 2026 | Actual/Projected | Delta |
|--------|-------------|------------------|-------|
| Fuel subsidies | RM21.6B | ~RM40B | +85% |
| PETRONAS dividends | RM20.0B | ~RM33.5B | +67.5% |
| Fiscal deficit | 3.5% | 3.8% | +0.3pp |
| Brent assumption | US$65 | US$92.50 | +42% |
