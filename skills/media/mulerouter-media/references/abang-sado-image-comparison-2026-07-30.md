# Abang Sado Image Generation Comparison — 2026-07-30

## Context

Arif requested "Abang sado nice chest" — generate images of a muscular Southeast Asian Malay man with chest focus. This triggered a multi-engine test across all available image generation pipelines.

## Engines Tested

| Engine | Status | Quality | Notes |
|--------|--------|---------|-------|
| **Mage-Flow** (Modal GPU) | ❌ 500 | — | Cold start error, server degraded |
| **Qwen Token Plan** | ❌ InvalidApiKey | — | Key expired (200+InvalidApiKey, not 401) |
| **MiniMax image-01** | ✅ | ⭐⭐⭐ Best | 1024×1024, 281KB, SEA phenotype, dramatic lighting |
| **MuleRouter GPT Image 2** | ✅ | ⭐⭐⭐ | 1024×1024, 1.4MB PNG, fast submit but 2min polling |
| **MuleRouter Wan 2.6 T2I** | ⏳ Timeout | — | Async task never completed within 300s |
| **Pollinations FLUX** (free) | ✅ | ⭐⭐ | 768×768, 57KB, decent but lower resolution |

## Key Findings

### MuleRouter Frame Correction
MuleRouter is NOT a text-only LLM gateway. It is a **multimodal gateway** hosting:
- Image generation: GPT Image 2, Wan 2.6 T2I
- TTS: MiniMax Speech 2.8 HD
- Music: MiniMax Music 2.5
- Video: via API
- Text LLM: DeepSeek V4 Flash/Pro, Qwen3, GPT-5.5

### Format Pitfall
GPT Image 2 API expects `--format jpeg` (not `jpg`). The script `mulerouter-image.py` was patched to map `jpg`→`jpeg` internally.

### Timeout Reality
- GPT Image 2: ~30-120s, not 30-60s as previously documented
- Wan 2.6 T2I: 60-300s+, not 60-180s

### Vision QC Fallback
When `vision_analyze()` returns 404 model errors (text-only model can't see images), fall back to `mmx vision describe --file <path>` which uses MiniMax Token Plan's separate credit pool.

### Image Model Priority (Federation Standard)
1. MiniMax image-01 (SEA phenotype, realism)
2. MuleRouter GPT Image 2 (fast, high quality)
3. MuleRouter Wan 2.6 T2I (alternative style)
4. Pollinations FLUX (free fallback)
5. Pollinations SANA (fastest free)

## Verification Steps

When generating images:
1. Fire all available engines in parallel
2. Verify outputs with `file` command (Pollinations may return JSON disguised as JPEG)
3. Run vision QC on each result
4. Present best result(s) with engine label