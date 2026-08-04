---
name: provider-routing-zen — FED Balance Probe Pattern
description: Reference for provider-routing-zen. How to probe FED provider state via MCP tools, interpret token_bank.db data, and identify gaps.
---

# FED Balance Probe Pattern

Run in parallel — these three MCP calls are independent and give a complete picture:

```
fed_health    → FED core status (port, version, DB path, table list)
fed_status    → Full provider table + latency + health + spend summary
fed_probe     → Track A balance probe (API-probed, not estimated)
```

## Interpreting fed_status Output

### Provider Tracks

| Track | Meaning | Confidence | Probe method |
|-------|---------|------------|-------------|
| A | API-probed (real balance) | 1.0 | `fed_probe` calls provider API |
| B | Manual estimate / token-plan | 0.5–0.95 | Human top-up, no live API |

**Only Track A gets live balance updates.** Track B balances go stale unless manually refreshed.

### Provider Status Fields

| Field | Meaning |
|-------|---------|
| `balance_usd` | Current balance (Track A = live, Track B = last known) |
| `confidence_score` | 0.0–1.0, how trustworthy the balance is |
| `last_updated` | ISO timestamp of last balance check |
| `last_probed_at` | When API was last called (null = never probed via API) |
| `notes` | Critical: look for "ARCHIVED", "BLIND", "needs_manual_reconciliation" |

### Red Flags in Notes

| Pattern | Meaning | Action |
|---------|---------|--------|
| `ARCHIVED` | Provider removed from litellm-config.yaml but still in DB | Consider cleanup |
| `BLIND` | Balance unknown (usage shown but no credit balance) | Manual reconciliation needed |
| `needs_manual_reconciliation` | Spend tracked but balance unverified | Check provider dashboard |
| `confidence_score < 0.5` | In cooldown or unreliable | Skip in routing |
| `balance_usd = 0.0` with status=LIVE | **Blocking gap** — routes will fail on first call | Top up or remove from chain |

### Latency Table Interpretation

The `route_latency` table in fed_status has **sparse samples** — most providers have 1–4 samples. Don't trust p95 with n<10. Use p50 as the signal.

```
p50 > 2000ms  → slow, consider timeout tuning
p95 > 5000ms  → likely hitting provider cold start or rate limit
sample_count = 1 → insufficient data, not actionable
```

### Health Table

All entries show `status: "LIVE"` by default. A provider in `route_health` with `status: "LIVE"` but `balance_usd: 0.0` is a **phantom** — routing will attempt it, fail, then circuit-break after `allowed_fails` (typically 1) with a 72h cooldown.

## Gap Classification Template

After probe, classify gaps:

| Severity | Condition |
|----------|-----------|
| HIGH | Balance = $0 but status = LIVE (phantom routing) |
| HIGH | Track A probe covers <50% of active providers |
| HIGH | Provider in chain but BLIND (no balance visibility) |
| MEDIUM | ARCHIVED providers still in DB (clutter) |
| MEDIUM | Latency samples < 5 per model (insufficient for p95) |
| LOW | Stale Track B balances (>7 days since last update) |

## Quick Commands

```bash
# Direct DB query (bypass MCP)
sqlite3 /root/.local/share/arifos/token_bank.db \
  "SELECT provider_name, track_type, balance_usd, confidence_score, notes FROM providers;"

# Check which providers are in active litellm config
cat /root/A-FORGE/litellm-config.yaml | grep -E 'model_name|litellm_params' | head -40

# Probe specific provider balance
sqlite3 /root/.local/share/arifos/token_bank.db \
  "SELECT provider_name, model_id, p50_ms, sample_count FROM route_latency ORDER BY provider_name;"
```
