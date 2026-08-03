# Qwen Token Plan — Multi-Seat Zen Architecture

> **Zen mapping forged 2026-08-03.** All 4 seats wired into independent fallback chain.
> **Previous audit (2026-08-03 early):** Seat 2 unmapped, Seat 2+1 sharing same key, Seat 3 idle.

Qwen Token Plan (Bailian/Model Studio on Alibaba Cloud) issues separate API keys
per seat — each seat is an independent subscription with its own quota, rate limit,
and model access. A seat is NOT a "team member" on one account — it's a distinct
billing entity.

## Zen Lane Map (2026-08-03)

```
LANE           PROVIDER                       KEY ENV                   SEAT           MODELS
──────────────┼──────────────────────────────┼────────────────────────┼──────────────┼──────
PRIMARY        qwen-token-plan                QWEN_HERMES_API_KEY      Team Pro 1/3   16
FALLBACK 1     qwen-token-plan-standard       QWEN_API_KEY             Team Std 2/3    16
FALLBACK 2     qwen-token-plan-team-owner     QWEN_TEAM_OWNER_API_KEY  Team Owner 3/3 16
INDIVIDUAL     qwen-token-plan-individual     QWEN_INDIVIDUAL_API_KEY  Individual Pro  7
CROSS-PROV     minimax                        MINIMAX_API_KEY          Cross-provider  2
```

All Qwen seats share the same endpoint:
`https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

## Design Rules

1. **Every seat gets its own provider block.** No two providers share a `key_env`.
2. **Fallback chain uses the same model across different seats before crossing to a different provider.** This eats independent quota pools before falling to minimax.
3. **Multi-seat same-provider fallback is valid** because each seat has an independent quota + rate-limit bucket. Same-provider ≠ same-key. The "same-provider=theatre" rule applies to shared keys, not shared endpoints.
4. **Rate limits are per-seat.** 429 on one seat doesn't affect others — the fallback chain jumps to the next seat's quota pool.
5. **Individual seat is reserved** for special access (preview models, image/TTS, multimodal) — not in the main fallback chain.

## Audit Procedure (proven 2026-08-03)

When Arif asks about Qwen seat mapping, do this BEFORE proposing changes:

1. **Enumerate all QWEN keys** in shell env + kunci-mas vault
2. **Probe each key** with `/models` endpoint — get the actual model list per seat
3. **Cross-reference** config providers → key_env → actual key access
4. **Identify gaps**: unmapped seats (key exists, no provider), shared keys (two providers same key_env), stale model lists
5. **Report findings** as a gap analysis table
6. **Propose minimal fix** — only then touch the config

**Correction (Arif, 2026-08-03):** I jumped to "create new provider" before finishing the full inventory. Arif: "audit first apa ada and then fix whatever needed to be fix." The right sequence is: full audit → report → propose → fix.

## Pre-Zen Gap Analysis (2026-08-03 morning)

```
KUNCI (4 seats)                     PROVIDER CONFIG (3 blocks)
══════════════════════════════════  ═══════════════════════════════
Seat 1 Team Pro                     qwen-token-plan              ✅ key betul
Seat 2 Team Standard                qwen-token-plan-standard     ❌ leak guna Seat 1 key
Seat 3 Team Owner                   — TIADA PROVIDER —            ❌ idle
Seat 4 Individual Pro               qwen-token-plan-individual   ✅ key betul
```

**Gap 1:** Standard sharing Seat 1's key → drains same quota, Seat 2 idle
**Gap 2:** Seat 3 completely unmapped → 22 models idle, paid but unused

## Fix Applied (2026-08-03)

1. `qwen-token-plan-standard` → `key_env` changed from `QWEN_HERMES_API_KEY` to `QWEN_API_KEY` (Seat 2)
2. Created `qwen-token-plan-team-owner` → `key_env: QWEN_TEAM_OWNER_API_KEY` (Seat 3)
3. Fallback chain: Seat 1 → Seat 2 → Seat 3 → minimax (4 independent layers)
4. Model lists synced to 16 core chat models per seat (from `/models` live probe)
5. hermes-gateway-api.service + hermes-real-bridge.service restarted to pick up rotated keys

## Related Pitfalls

- **Stale gateway after key rotation:** After updating kunci-mas.flat.env, running services hold old keys in process memory. `systemctl restart hermes-gateway-api hermes-real-bridge` is required.
- **model list drift:** Config model lists drift from `/models` reality over time. Image/TTS/audio models appear but should be excluded from text-only providers.
- **429 = valid key:** Rate-limit 429 proves auth succeeded. 401 = invalid/rotated key.