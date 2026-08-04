# Provider Capability Audit Pattern

> Source: MiMo + MiniMax audit session (2026-08-04, Kimi K3 + Hermes)
> Core lesson: "Probe the substrate, not the proxy."

## The Three-Layer Problem

Provider capabilities exist at three independent layers. All three must match for features to work:

| Layer | What it checks | Failure mode |
|---|---|---|
| **Docs** | Vendor documentation | Docs say image understanding but model variant is text-only |
| **Config** | litellm-config.yaml + hermes config.yaml | Alias declared but capability flag missing → proxy rejects |
| **Runtime** | Actual API calls | Key expired, quota exhausted, wrong key type |

**Key insight:** A capability passing docs check but failing runtime check is NOT a config problem. It is a credentials/quota problem. Check keys before config.

## Worked Example: MiMo + MiniMax Audit (2026-08-04)

### What happened

1. MiMo docs confirmed mimo-v2.5 supports image/audio/video
2. Config declared hermes-asi → mimo-v2.5-pro (different model variant)
3. mimo-v2.5-pro is text-only on Token Plan SGP (confirmed via direct curl)
4. hermes-asi alias in LiteLLM rejected all multimodal requests with NotFoundError
5. MiniMax-M3 was the actual auxiliary vision provider, but key had expired
6. Expired key surfaced as NotFoundError indistinguishable from config failure

### Root cause chain

Docs say mimo-v2.5 = multimodal
  → Config says hermes-asi → mimo-v2.5-pro (text-only variant)
  → LiteLLM proxy inspects capability metadata and rejects
  → Meanwhile MiniMax-M3 key expired → fallback dead
  → All multimodal paths blocked, but error message blames routing

### Audit sequence (correct)

1. Read MiMo docs → mimo-v2.5 = multimodal, mimo-v2.5-pro = text-only
2. Read litellm-config.yaml → hermes-asi points at -pro not base
3. curl direct to mimo-v2.5-pro + image → REJECTED (text-only confirmed)
4. curl direct to MiniMax-M3 → 401 (key expired)
5. Conclusion: key expiry was the real blocker

### Key lesson

When all hypotheses point to config, check credentials. Key expiry manifests as routing failure.

## Provider Gotchas: MiMo

- mimo-v2.5 ≠ mimo-v2.5-pro: Base = multimodal. Pro = deep thinking text-only.
- Two endpoints: api.xiaomimimo.com/v1 (docs) vs token-plan-sgp.xiaomimimo.com/v1 (Token Plan). Both reach mimo-v2.5.
- Deep thinking locks params: thinking.type=enabled forces temperature/top_p to 1.0/0.95.
- reasoning_content echo: Multi-turn MUST pass back reasoning_content. Missing → 400.
- Web search: $5/1K overseas + token fees. Requires Console plugin activation.
- Cold start 30-60s: First hit per modality on Token Plan SGP.

## Provider Gotchas: MiniMax

- Two key types: API Key (pay-as-you-go sk-*) vs Subscription Key (Token Plan). NOT interchangeable.
- Token Plan does NOT cover: H3 video, voice design, rapid voice cloning.
- Balance $0 does NOT mean key dead: Pay-as-you-go may still work. FED balance is cached.
- M3 permanent 50% off: Input $0.30/M, output $1.20/M.
- Anthropic compat: api.minimax.io/anthropic vs api.minimax.io/v1. Same key, different SDKs.
- M3 context pricing step: 512k threshold = 2x rate above it.

## Diagnostic Commands

```bash
# Verify key works
curl -s "ENDPOINT/v1/models" -H "Authorization: Bearer $KEY" | python3 -m json.tool

# Test image modality
curl -s "ENDPOINT/v1/chat/completions" -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d '{"model":"MODEL","messages":[{"role":"user","content":[{"type":"text","text":"hi"},{"type":"image_url","image_url":{"url":"https://httpbin.org/image/png"}}]}],"max_tokens":50}'

# Check FED balance
sqlite3 /root/.local/share/arifos/token_bank.db "SELECT provider_name,balance_usd,last_updated FROM providers WHERE provider_name='PROVIDER';"

# Compare config declarations
grep -A20 'minimax:' ~/.hermes/config.yaml
grep -B1 -A8 'minimax' /root/A-FORGE/litellm-config.yaml
```

## Cost Reference (2026-08-04)

MiMo: mimo-v2.5 (multimodal), mimo-v2.5-pro (text deep thinking).

MiniMax pay-as-you-go: M3 $0.30/$1.20 per M tokens (50% off). M2.7 $0.30/$1.20. TTS $60-$100/M chars. Image $0.0035. Music $0.15/5min. Web search $0.01/req.

MiniMax Token Plan: Plus $20/mo (M3/M2.7/image/speech/music). Max $50/mo. Ultra $120/mo. Does NOT cover H3 video.

MiniMax Credits: 1000 credits = $1. Valid 365 days.
