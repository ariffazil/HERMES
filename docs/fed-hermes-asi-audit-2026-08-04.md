# FED + Hermes-ASI Audit — 2026-08-04

> Sovereign: Arif (F13)
> Agents: Hermes (ASI🪽) + Kimi K3/FI-008
> Duration: 22:01 – 23:34 MYT
> Verdict: DITEMPA BUKAN DIBERI ⚒️

---

## Executive Summary

Full audit of multimodal capabilities across the federation's AI stack. Found that **hermes-asi is text-only at the LiteLLM layer** despite MiMo V2.5 docs claiming multimodal support. Root cause: `mimo-v2.5-pro` (text-only deep-thinking variant) is bound to the alias, not `mimo-v2.5` (multimodal base). Additionally, MiniMax auxiliary vision was dead due to key expiry.

**Resolution:** Config patched (3 new multimodal aliases), MiniMax key refreshed, capability doc created. All verified live.

---

## Key Findings

### 1. Multimodal Architecture (the core discovery)

```
hermes-asi → mimo-v2.5-pro (TEXT-ONLY)
              ↓
           MiniMax-M3 (auxiliary vision: image→text→chat LLM)
              ↓
           DEAD (key expired)
```

**Reality:** hermes-asi processes images via auxiliary vision path (MiniMax-M3 describes → text → chat LLM), not native multimodal. This path was broken because MiniMax pay-as-you-go key had expired.

### 2. LiteLLM Proxy ≠ Production Traffic

- All 169 LiteLLM POSTs in 30 min came from 100.64.0.2 (same network namespace)
- No external agent traffic through LiteLLM
- Agents call providers **direct** via Hermes provider catalog
- LiteLLM serves as health probe target + FED route metadata source only

### 3. MiMo V2.5 Model Variants

| Model | Multimodal | Deep Thinking | Notes |
|---|---|---|---|
| `mimo-v2.5` | ✅ image/audio/video | ✅ (default ON) | Base multimodal model |
| `mimo-v2.5-pro` | ❌ text only | ✅ (default ON) | Deep-thinking variant |

### 4. MiniMax Key Expiry (actual root cause of "intermittent multimodal failures")

MiniMax pay-as-you-go key was expired. Symptoms misattributed to config:
- "image returned but no img_tokens" → M3 returning partial data / 401
- "rotation hits non-multimodal entries" → routing hit dead M3 endpoint
- "NotFoundError: no endpoints support image input" → M3 401 surfaced as routing failure

---

## Configuration Changes Applied

### A. litellm-config.yaml (+32 lines)

New aliases (verified live):

| Alias | Backend | Modality | Verified |
|---|---|---|---|
| `hermes-asi-vision` | mimo-v2.5 + qwen3.7-plus | image | ✅ img_tokens=1024 |
| `asi-555-audio` | mimo-v2.5 | audio | ✅ audio_tokens=25 |
| `asi-555-video` | mimo-v2.5 | video | ✅ total=1459 |

Backup: `/root/forge_work/backups/litellm-config-20260804T142000Z.yaml`

### B. ~/.hermes/config.yaml (MiniMax provider)

- Added MiniMax-M2.7 model (200K ctx, agentic, $0.30/$1.20 per M tokens)
- Added capabilities block: `[chat, function_calling, reasoning]`
- Updated provider name: "MiniMax M3 (1M Context Flagship) — pay-as-you-go"
- Backup: `~/.hermes/config.yaml.bak.*`

### C. FED token_bank.db

- Updated MiniMax notes: "pay-as-you-go — verified LIVE 2026-08-04"
- Was mislabeled as "Token Plan"

### D. FLAME skill path fix

- Canonical: `/root/.local/share/flame/flame_state.json` (5296 bytes live)
- Compat symlink: `/root/.local/share/arifos/flame_state.json` → canonical
- FLAME skill paths rewritten

---

## Service Status (22:48 MYT)

| Service | Port | Status |
|---|---|---|
| arifFLOW | 7073 | ✅ LIVE — FQ=2.0 BALANCED |
| FLAME | 18901 | ✅ LIVE — RM0 free-loop |
| FED | 7074 | ✅ LIVE — MCP v3.1.0-zen (no HTTP /health, 404 expected) |
| A-FORGE API | 7071 | ✅ LIVE |
| A-FORGE MCP | 7072 | ✅ LIVE |
| AAA | 3001 | ✅ LIVE |

---

## FED Provider State

| Provider | Balance | Track | Status |
|---|---|---|---|
| deepseek | $13.81 | A (auto-probed) | ✅ LIVE |
| bailian-token-plan | $25.00 | B (manual) | ✅ LIVE |
| mimo-platform | $10.00 | B (manual) | ⚠️ never live-probed |
| minimax | $0.00 (pay-as-you-go) | B | ✅ LIVE (key works, balance in MiniMax account) |
| mulerouter | $49.93 | B | ARCHIVED — orphaned from litellm |
| openrouter | $0.50 | B | ARCHIVED — BLIND (no credit balance visible) |
| qwen-token-plan-team | $0.00 | B | ✅ LIVE (seat 2/3 = ariffazil) |
| tokenrouter | $59.94 | B | ARCHIVED — orphaned from litellm |

Archived total: ~$110 stranded.

---

## Capability Matrix

### MiMo V2.5 (via Token Plan SGP)

| Capability | Model | Status |
|---|---|---|
| Text chat | mimo-v2.5-pro | ✅ |
| Deep thinking | mimo-v2.5-pro | ✅ default ON |
| Image understanding | mimo-v2.5 (NOT -pro) | ✅ |
| Audio understanding | mimo-v2.5 | ✅ |
| Video understanding | mimo-v2.5 | ✅ |
| Structured output (JSON) | mimo-v2.5-pro | ✅ |
| Web search | mimo-v2.5-pro | ⚠️ needs Console plugin activation ($5/1K) |
| Function calling | both | ✅ OpenAI-compatible |

### MiniMax M3 (via api.minimax.io)

| Capability | Model | Price |
|---|---|---|
| Text chat (1M ctx) | MiniMax-M3 | $0.30/$1.20 per M tokens (50% off) |
| Text chat (200K ctx) | MiniMax-M2.7 | $0.30/$1.20 per M tokens |
| TTS | speech-2.8-hd/turbo | $60-$100/M characters |
| Music | music-3.0 | $0.15/5min |
| Image gen | image-01 | $0.0035/image |
| Web search | server tool | $0.01/request |

### MiniMax Token Plan Tiers

| Tier | Price | Coverage |
|---|---|---|
| Plus | $20/mo | M3/M2.7/image/speech/music (NO H3 video) |
| Max | $50/mo | 4-5 agents, daily multimodal |
| Ultra | $120/mo | 6-7 agents, heavy workflows |

---

## Lessons Learned

1. **Docs ≠ Reality.** MiMo docs claim multimodal on `mimo-v2.5` but `hermes-asi` was bound to `mimo-v2.5-pro` (text-only). Always test live.

2. **Probe substrate, not proxy.** LiteLLM 404 ≠ service down. MCP health worked fine. Proxy just doesn't expose HTTP /health.

3. **Check keys first.** Symptoms that look like config issues may actually be key expiry. M3 "intermittent failures" were dead endpoint, not routing.

4. **Auxiliary vision ≠ native multimodal.** Hermes processes images through MiniMax-M3 → text → chat LLM, not through the chat model's native vision capability.

---

## Open Followups

1. **Archived providers** — withdraw or tombstone ~$110 stranded (mulerouter, tokenrouter, openrouter)
2. **Web Search plugin** — activate in MiMo Console for real-time search capability
3. **Periodic provider health checks** — 5min cron probing each API key directly
4. **Hermes auxiliary audio/video** — unverified whether path exists for non-image modalities
5. **FLAME false-demote** — S5 state-only fix (promote 5 tiers, observe self-heal)

---

*Generated: 2026-08-04 23:34 MYT*
*Source: Live T0 probes + litellm-config.yaml + MiMo/MiniMax official docs*
*Witnesses: Hermes ASI, Kimi K3/FI-008*
