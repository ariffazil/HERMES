# Wolf Cabinet Model — Provider Selection as Constitutional Architecture

> **Forged:** 2026-07-30, by Arif (F13 SOVEREIGN)
> **EUREKA class:** DOMAIN vs DOMAIN (Class 5) — multimodal perception domain vs constitutional judgment domain
> **Seal candidate:** Operationalized in AGENT_MODEL_MAP.json + federation_model_router.py
> **Seal hash:** f5e3481f

## The Contradiction

| Commitment A | Commitment B |
|---|---|
| Swarm needs a unified multimodal surface with fixed pricing | Constitutional reasoning cannot risk single-provider failure |
| 14 agents need vision, omni, TTS, image gen. OpenRouter has 211 vision models but no TTS/music/video, floating prices, $5 minimum | DeepSeek V4 Pro serves 666_JUDGE and 999_SEAL. OpenRouter has 4+ providers for it. MuleRouter has 1. |

**Contradiction class:** DOMAIN vs DOMAIN — you cannot pick ONE surface for everything.

## The Compression

Old frame: "Pick the best API provider for your models."
Why it fails: Forces a choice between multimodal capability and constitutional redundancy.

New structure:

```
Δ (PERCEPTION)  → MuleRouter      (vision, omni, TTS, image — one key, fixed price)
Ω (JUDGMENT)    → OpenRouter      (constitutional DeepSeek V4 Pro — multi-provider)
Ψ (SURVIVAL)    → Ollama          (local qwen3:8b — zero cost, sovereign)
```

This maps DIRECTLY onto the Δ·Ω·Ψ multimodal cognition architecture. Provider selection IS constitutional architecture, not ops preference.

## Routing Rules (Priority Order)

1. **Vision** (any agent) → MuleRouter (qwen-vl-max / qwen3-vl-plus / qwen3-omni-flash)
2. **Fast chat** (Hermes daily) → MuleRouter deepseek-v4-flash (fixed price)
3. **Constitutional reasoning** (888-APEX, 999-SEAL) → OpenRouter deepseek-v4-pro ONLY
4. **Deep code/reasoning** (OpenCode, 333-AGI) → OpenRouter deepseek-v4-pro
5. **Research/omni** (555-ASI) → MuleRouter qwen3-max (fixed pricing)
6. **ALL CLOUD FAIL** → Ollama local recovery (qwen3:8b)

## Why Floor-Mapped

| Layer | Provider | Risk if down | Floor | Recovery |
|---|---|---|---|---|
| Δ Perception | MuleRouter | Reversible — can retry | F1 SAFE | HOLD + retry |
| Ω Judgment | OpenRouter | Irreversible — constitutional | F1 HARD | Multi-provider failover |
| Ψ Survival | Ollama | Zero — always available | F13 SOVEREIGN | Always ready |

## AGENT_MODEL_MAP Entry

MuleRouter is the 17th provider in `/root/AAA/registries/models/AGENT_MODEL_MAP.json`:
```json
{
  "provider_id": "mulerouter",
  "provider_name": "MuleRouter (multimodal surface)",
  "status": "ACTIVE"
}
```

## Implementation

```bash
# Any agent in the swarm can route:
python3 /root/AAA/scripts/federation_model_router.py \
  -t "describe this image" -a opencode --json
# → {"provider": "mulerouter", "model": "mulerouter/qwen-vl-max", ...}

python3 /root/AAA/scripts/federation_model_router.py \
  -t "judge deploy readiness" -a 888-apex --json
# → {"provider": "openrouter", "model": "deepseek-v4-pro", ...}
```

## Key Verification Lesson (for future agent sessions)

**When evaluating a new provider's model catalog, always call `/v1/models` directly.** On 2026-07-30, searching MuleRouter's documentation returned zero DeepSeek results. But the API endpoint `https://api.mulerouter.ai/vendors/openai/v1/models` returned 31 models including deepseek-v4-flash and deepseek-v4-pro. Commercial aggregators update faster than their docs. API response is evidence; doc search results are not.

## One Breath

> Provider bukan kedai runcit model. Provider adalah lapisan perlembagaan. Δ merasa, Ω menghakimi, Ψ bertahan. Tiga layer, satu swarm.
