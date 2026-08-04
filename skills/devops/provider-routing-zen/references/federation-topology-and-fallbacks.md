---
name: provider-routing-zen — Federation Topology & Fallback Semantics
description: Reference for provider-routing-zen. Federation node topology, wawabot location ground truth, and LiteLLM fallback chain semantics (why chains order the way they do).
---

# Federation Topology & Fallback Chain Semantics

This is a **reference** for the `provider-routing-zen` skill. The canonical
SKILL.md covers constitutional role mapping and CQT dials. This file
captures the **physical federation topology** and **why fallback chains order
the way they do** — both of which are non-obvious from the SKILL.md alone.

## 1. Federation Node Topology — Read Before Routing Decisions

The federation is **NOT localhost-only**. Routing decisions that ignore
multi-node topology quietly break remote agents (wawabot is the most common
casualty).

| Node | Tailscale IP | Role | Hermes profile |
|---|---|---|---|
| af-forge | 100.64.0.2 | Brain (FORGE) — full stack, LiteLLM, arifOS | forge/asi/apex |
| azwaos | 100.64.0.4 | Voice (wawabot) — Telegram bot for adek Arif | azwaos |
| arifs-s24 | 100.64.0.1 | Arif's phone (frequently offline, ignore) | — |

Verify before assuming:

```bash
tailscale status | grep -E "af-forge|azwaos|arifs-s24"
```

### Pitfall — Treating federation as localhost

The default Hermes-AI agent on FORGE runs on 127.0.0.1 and treats everything
as local. If you remove `master_key` from LiteLLM thinking "only I use it"
in a multi-node federation, you silently break wawabot.

**Test before removing auth:**

```bash
# If removing master_key, check wawabot first
ssh root@100.64.0.4 "cat ~/.hermes/config.yaml | grep -E 'provider|base_url'"
```

If wawabot points to FED, do NOT remove master_key without a replacement
(Tailscale-only listener, scoped keys, or Caddy proxy with auth).

### Pitfall — Misremembering wawabot's location

Wawabot hostname morphs over time. Don't trust older memory:

| Date | Hostname | Tailscale IP | Notes |
|---|---|---|---|
| Jul 2026 | `srv1642546` | n/a | FLOW VPS, decommissioned |
| Aug 2026 | `azwaos` | 100.64.0.4 | adek Arif's machine, NOT wife |

**Wawabot is operated by adek Arif (sister), NOT wife.** Always grep
`tailscale status` for ground truth, don't rely on prior memory.

## 2. Fallback Chain Semantics — Why DeepSeek → MiniMax, Not vice versa

The LiteLLM config at `/root/A-FORGE/litellm-config.yaml` orders providers
per `model_name`. The order is **NOT** "best to worst" — it's **cheapest
first, most expensive last as safety net**:

```
deepseek-v4-pro  → cheapest reasoning, primary
mimo-v2.5-pro   → token-plan credit, medium-tier
MiniMax-M3      → most expensive, "no other choice" lane
```

### Why fall to MiniMax?

When `allowed_fails: 1` + `cooldown_time: 259200` (72h) trigger, LiteLLM
auto-failovers to the **next provider in the chain**, not the "best" one.

So MiniMax is reached when:
1. DeepSeek failed once (rate limit, timeout, quota exhausted)
2. MiMo also failed OR is in 72h cooldown
3. Only MiniMax has capacity left

**MiniMax is NOT "optimized for the task"** — it's the **safety net** for
the model_name chain. The actual optimization lives in the **model_name**
selection (`opencode` vs `apex-888` vs `hermes-asi`), which maps
constitutional roles to provider chains.

### Circuit breaker — why chains appear to "skip" providers

`cooldown_time: 259200` = 72h disables a provider after quota exhaustion.
Auto-re-enables when cooldown expires. During a 72h window, the chain
appears to skip failed providers entirely rather than retry them.

To inspect current cooldowns:

```bash
sqlite3 /root/.local/share/arifos/token_bank.db \
  "SELECT provider_name, balance_usd, last_updated, notes FROM providers;"
```

If a provider shows `notes = 'BLIND'` or `confidence_score < 0.5`, it's in
cooldown and routing will skip it.

### How to interpret "the agent fell to MiniMax"

When you see `provider=minimax` in a trace, it means **the chain ran out
of cheaper options**, not that MiniMax was preferred. The actual cause is
upstream — check route_latency table for which provider failed first:

```bash
sqlite3 /root/.local/share/arifos/token_bank.db \
  "SELECT provider_name, model_id, p50_ms, p95_ms, sample_count FROM route_latency ORDER BY provider_name;"
```

### Pitfall — new providers rank low despite fast latency

The FED route engine applies `INSUFFICIENT_TELEMETRY` demotion to any
route with < 10 samples. A freshly-added provider with 450ms latency
and 1 sample will rank BELOW a 592ms provider with 3 samples, because
the telemetry gate penalizes untested routes.

**This is correct behavior** — don't fight it. Let traffic accumulate.
After ~10 calls, the latency gate takes over and the faster provider
ranks appropriately.

**Workaround if urgent:** manually seed latency samples:
```bash
# Seed a few route_latency entries to clear INSUFFICIENT_TELEMETRY
sqlite3 /root/.local/share/arifos/token_bank.db "
INSERT OR REPLACE INTO route_latency (provider_name, model_id, p50_ms, p95_ms, sample_count, last_sample)
VALUES ('your-provider', 'model-id', 450.0, 500.0, 10, datetime('now'));"
```

### Pitfall — conscious archive vs fix

Not every provider gap needs fixing. Before attempting repair, check:
1. **Is it in MODEL_ROUTES?** If no → invisible to routing anyway
2. **Is there a better alternative already live?** If yes → archive
3. **Is the balance near-empty AND BLIND?** If yes → can't probe, can't fix

When archiving, mark clearly in `providers.notes`:
```
ARCHIVED (conscious decision YYYY-MM-DD): reason. No re-track needed — [alternative] covers this.
```
This prevents future agents from re-discovering the "gap" and wasting
cycles on a provider that was intentionally excluded.

## 6. Quick diagnostic — which provider is the agent actually using?

Three ways to ground truth:

```bash
# 1. Live: tail the litellm log
tail -f /tmp/litellm.log | grep -E "provider|model"

# 2. Federated: query the route_health table
sqlite3 /root/.local/share/arifos/token_bank.db \
  "SELECT * FROM route_health WHERE last_used > datetime('now', '-1 hour');"

# 3. Specific: ask FED which model it routes to
curl -s http://127.0.0.1:4000/v1/models | jq -r '.data[].id'
```

## 4. FED MCP Router — MODEL_ROUTES (the hidden gate)

The FED MCP server (`fed_router.py` on port 7074) has its own routing layer
**separate from LiteLLM**. The `fed_route` tool returns ranked routes, but
**only for providers listed in the `MODEL_ROUTES` dictionary** in
`/root/AAA/scripts/fed_router.py`.

### Pitfall — Provider LIVE but invisible in fed_route

A provider can be LIVE in `route_health`, have good latency in `route_latency`,
and be configured in Hermes config — but **never appear in fed_route output**
if it's not in `MODEL_ROUTES`.

**Diagnosis:**
```bash
# Check if a provider has routes defined
sed -n '/^MODEL_ROUTES/,/^}/p' /root/AAA/scripts/fed_router.py | \
  grep -c "your-provider-name"
# 0 = NOT in MODEL_ROUTES = invisible to fed_route
```

**Fix:** Add entries to `MODEL_ROUTES` in `fed_router.py`, then restart:
```bash
systemctl restart fed-router.service
```

### Seat-based vs token-based balance

FED's balance gate demotes providers with balance < $5.00 (soft) or < $1.00
(hard). For **seat-based plans** (e.g., Qwen Token Plan Team), the FED
`providers.balance_usd` must reflect **seat value**, not token consumption.

| Plan type | Balance meaning | Fix if $0 |
|-----------|----------------|-----------|
| PAYG (DeepSeek) | Actual API credit | Top up or leave as-is |
| Seat-based (Qwen Team) | Seat allocation value | Set to `seats × $50/mo` |
| Free tier (Groq, FLAME) | N/A | Set to high value (999) |

```bash
# Update seat-based provider balance
sqlite3 /root/.local/share/arifos/token_bank.db \
  "UPDATE providers SET balance_usd = 150.0 WHERE provider_name = 'qwen-token-plan-team';"
```

### Track A/B promotion

Track A = primary routing pool. Track B = secondary/fallback. Promotion
is a metadata update in the `providers` table:

```bash
sqlite3 /root/.local/share/arifos/token_bank.db \
  "UPDATE providers SET track_type = 'A' WHERE provider_name = 'your-provider';"
```

## 5. Decision tree — adding a new provider to the chain

Before adding a new provider to a model_name chain:

1. **Is the provider sovereign?** (ZDR check — does data leave Malaysia?)
   - If no → not for F1-F13 paths, only for F14 peripheral work
2. **Does it have a quota profile?** (token-plan credit vs pay-as-you-go)
   - Token-plan credit: place early in chain (cheap, bounded)
   - PAYG: place after credit providers
3. **Is it 72h-circuit-breakable?**
   - Quota-bounded providers → eligible for cooldown
   - Fixed-fee providers (e.g. flat key) → no cooldown needed
4. **Where does it fit in the constitutional role map?**
   - Reasoning → deepseek family
   - Vision → MiMo multimodal, Qwen VL
   - Judgment → apex-888 (DeepSeek + MiniMax)
   - Compression → MiniMax (text compression)

### Pitfall — cascade insertion renumbers ALL downstream priorities

When adding a new provider between existing entries in `MODEL_ROUTES`,
you MUST renumber every downstream provider's `priority` field. The
FED route engine sorts by priority — wrong numbers = wrong cascade order.

**Pattern (from 2026-08-05 qwen-token-plan-team fix):**

```
BEFORE deepseek-v4-pro:
  deepseek       → P1
  mulerouter     → P2
  tokenrouter    → P3

AFTER adding qwen as P2:
  deepseek       → P1  (unchanged)
  qwen-team      → P2  (NEW)
  mulerouter     → P3  (was P2, renumbered)
  tokenrouter    → P4  (was P3, renumbered)
```

**Rule:** Insert the new entry at the right position, then increment
priority by +1 for every entry that comes after it. Never leave gaps
(1,2,4,5) — the engine sorts numerically and gaps cause no bug but
are confusing during debugging.

**Verify after patch:**
```bash
# Confirm new provider appears in route output
curl -s http://127.0.0.1:7074/mcp -d '{"method":"tools/call","params":{"name":"fed_route","arguments":{"model":"deepseek-v4-pro"}}}' | python3 -m json.tool
# Should show new provider in ranked routes
```

### Pitfall — constitutional flag must not change

When inserting routes for an existing model, preserve the `constitutional`
flag on the original primary route. DeepSeek direct is `constitutional: True`
because it handles F1-F13 governance paths. New providers added alongside
it must be `constitutional: False` unless explicitly approved by F13.
