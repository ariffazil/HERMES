---
name: federation-fed-routing-patch
description: Apply patches to FED MODEL_ROUTES (qwen-token-plan-team routes, OpenRouter re-track/archive). Use when user wants to add/reorder/remove provider routes in /root/AAA/scripts/fed_router.py.
---

# Federation FED Routing Patch Workflow

> **When to use:** User asks to add a new provider route to FED, change priority, or modify existing MODEL_ROUTES cascade.

## Canonical Source of Truth

- **FED router code:** `/root/AAA/scripts/fed_router.py`
- **FED DB:** `/root/.local/share/arifos/token_bank.db` (SQLite, tables: providers, route_health, route_latency, token_bank_spend, shadow_ledger)
- **Model routes dictionary:** `MODEL_ROUTES` (line ~184)
- **Route engine:** `fed_route_engine()` (line ~429)
- **Status check:** `systemctl status fed-router.service` (port 7074, MCP)
- **DB schema:** `track_type` ∈ {A, B}, `confidence_score` ∈ [0.0, 1.0], `balance_usd` REAL

## Critical Patch Workflow (Review-Before-Apply Pattern)

**Arif's rule:** Never blind-patch FED. Show patch dulu, tunggu "apply"/"go" sebelum execute.

### Step 1: Read current state

```bash
sed -n '/^MODEL_ROUTES/,/^}/p' /root/AAA/scripts/fed_router.py | head -200
sqlite3 /root/.local/share/arifos/token_bank.db "SELECT provider_name, track_type, balance_usd, confidence_score, notes FROM providers;"
sqlite3 /root/.local/share/arifos/token_bank.db "SELECT * FROM route_health WHERE provider_name='X';"
```

### Step 2: Verify provider health before adding

Don't add routes for dead/ARCHIVED providers. Check:
- `route_health.status = LIVE` (not DEGRADED/DEAD)
- `last_sample` recent
- `notes` tidak ada "ARCHIVED", "BLIND", "DEAD"

### Step 3: Draft the patch (TEXT FIRST, no execute)

Present exact diff to user. Include:
- For each new entry: provider, router (direct/gateway), class, constitutional, shadow, priority
- For each modified entry: priority renumbering (1→2→3→4)
- **NEVER delete** existing routes — cascade only
- Keep `constitutional: True` on primary direct provider (e.g., deepseek-v4-pro)

### Step 4: Offer Option 1/2/3

```
Option 1 — Apply patch now via patch tool
Option 2 — Let me apply manually — give me the file path
Option 3 — Hold — need to verify [specific concern]
```

### Step 5: After apply — verify

```bash
# Syntax check
python3 -c "import py_compile; py_compile.compile('/root/AAA/scripts/fed_router.py', doraise=True)"

# Verify routes present in MODEL_ROUTES section only
sed -n '/^MODEL_ROUTES/,/^}/p' /root/AAA/scripts/fed_router.py | grep -n "provider-name"

# Restart service
systemctl restart fed-router.service
sleep 2

# Test route via MCP
mcp__fed__fed_route(model="X", agent_id="hermes")
```

### Step 6: Balance gate check (LOW_BALANCE_SOFT demotion)

If provider returns `balance_flag: LOW_BALANCE_SOFT` despite being LIVE, check:

- **Token-based provider** ($0 = exhausted): update balance_usd if you topped up, or accept demotion
- **Seat-based provider** (Qwen Token Plan, RM0 marginal): $0 ≠ no capacity. Update balance to reflect seat value (e.g., $150 for 3 seats × $50/seat) and notes to clarify "seat-based, NOT token-based"

### Step 7: Track promotion (Track B → Track A)

If asked to promote to Track A:

```bash
sqlite3 /root/.local/share/arifos/token_bank.db "UPDATE providers SET track_type='A' WHERE provider_name='X';"
```

Track A = primary route for constitutional work. Don't promote lightly — Track A is intentional redundancy layer.

## Pitfalls

- **Sandbox vs host**: `/root/AAA/scripts/fed_router.py` not in Hermes sandbox. Always patch via `patch` tool (which writes to host directly), not via `terminal` or sandbox `read_file`.
- **Priority renumbering**: When inserting a new P2 entry between existing P1 and P2, must renumber existing P2→P3, P3→P4. Easy to miss.
- **Vision models**: Don't override existing vision-specific routes (qwen-vl-max, qwen3-vl-plus) — they have intentional mulerouter priority for VL capability.
- **constitutional flag**: Only `deepseek-v4-pro` has `constitutional: True` for now. Don't blanket-set True on new routes — constitutional gate uses this for tier ≥ 666 routing.
- **OpenRouter blind spot**: If `/auth/key` returns usage but no credit balance, don't try to "fix" — conscious archive. Update `notes` with "ARCHIVED (conscious decision YYYY-MM-DD)" marker.

## Federation State (as of 2026-08-05)

| Provider | Track | Balance | Routes |
|----------|-------|---------|--------|
| deepseek | A | $13.81 | deepseek-v4-pro, deepseek-v4-flash |
| qwen-token-plan-team | A | $150 (seat) | 6 models (P1 or P2) |
| mulerouter | B | $49.93 | gateway fallback (ARCHIVED) |
| openrouter | B | $0.50 | ARCHIVED (conscious) |

Reference: Session 2026-08-05 00:11-00:39 UTC. Patch verified live after restart.