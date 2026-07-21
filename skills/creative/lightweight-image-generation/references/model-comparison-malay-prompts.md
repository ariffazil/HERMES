# MiniMax vs Pollinations — Same Malay Prompt Comparison

**Date:** 2026-07-20  
**Prompt (Malay):** "Lelaki Melayu sado bertelanjang dada, badan berotot macam bodybuilder, six-pack abs jelas, bahu lebar, muka hensem garang, rambut pendek hitam, cahaya dramatik gym, peluh berkilat di badan, fotorealistik, 4K"

## Results

| Metric | MiniMax `image-01` | Pollinations (FLUX) |
|--------|-------------------|---------------------|
| Resolution | 1024×1024 ✅ | 768×768 |
| File size | 184KB ✅ | 73KB |
| Malay phenotype | Strong SEA reading ✅ | Ambiguous / generic |
| Skin texture | Natural, studio-grade ✅ | Plastic, AI-exaggerated |
| Lighting | Professional Rembrandt | Inconsistent, harsh |
| Muscle proportions | Athletic, believable | Cartoonish, impossible |
| Prompt understanding | Nailed "abang sado" ✅ | Generic buff guy |
| Cost | Token Plan quota | Free |

## Earlier comparison (English prompt)

| Metric | MiniMax `image-01` | Pollinations (FLUX) |
|--------|-------------------|---------------------|
| Resolution | 1024×1024 ✅ | 768×768 |
| File size | 217KB ✅ | 54KB |
| Phenotype | Latin/Mediterranean reading | SEA reading but plastic |
| Professional quality | Bodybuilding editorial ✅ | Stock image |

## Key Findings

1. **MiniMax wins consistently** — 3-4× larger file size, better lighting, more realistic skin
2. **Malay prompt + MiniMax = best Malay phenotype** — using actual BM ("lelaki Melayu sado") rather than English ("handsome muscular Malay man") produced clearer SEA features on MiniMax
3. **Pollinations struggles with ethnicity** — even with explicit "Melayu" in prompt, output was ambiguous or defaulted to generic features
4. **Pollinations quality gap** — outputs consistently look AI-generated (plastic skin, exaggerated anatomy) vs MiniMax's photorealistic output
5. **Slang works** — "abang sado" was correctly interpreted by both models

## Recommended chain

```
Malay/SEA phenotype → MiniMax image-01 (BM prompt) → Pollinations (free fallback)
Generic prompts → MiniMax image-01 → Qwen image-2.0 → Pollinations
```
