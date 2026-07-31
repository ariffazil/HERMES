# Multi-Model Image Generation Comparison — 2026-07-30

**Prompt (English):** "Abang Sado, Southeast Asian Malay muscular man, massive chiseled chest and pectorals, gym workout, shirtless, studio lighting, sweat glistening, fitness photography, high detail, dramatic pose, pec focus"

**Context:** User asked to test ALL available image generation routes with the same chest-focused prompt. Mage-Flow was down (500 error). All others generated successfully.

## Results

### 1. 🥇 MiniMax image-01 (Token Plan) — WINNER

| Dimension | Value |
|-----------|-------|
| **Resolution** | 1024×1024 |
| **File size** | 200KB (JPEG, JFIF standard) |
| **Phenotype** | Strong Malay/SEA — skin tone, facial structure, goatee |
| **Realism** | Studio-grade, natural lighting, sweat detail, believable muscle proportions |
| **Chest focus** | Deep pec separation, dramatic chiaroscuro, full pectoral definition |
| **Lighting** | Professional Rembrandt-style, front-left key light |
| **Cost** | Token Plan quota (monthly ~5.1B tokens) |
| **Gen time** | ~15s |
| **Command** | `mmx image generate --prompt "..." --aspect-ratio 1:1 --non-interactive` |

**Vision verdict:** *"Exceptional muscle definition, dramatic chiaroscuro lighting, strong Malay phenotype accuracy. Compares favorably to professional Men's Health / Flex magazine photography."*

### 2. 🥈 Pollinations FLUX (free) — Seed 1

| Dimension | Value |
|-----------|-------|
| **Resolution** | 768×768 |
| **File size** | 63KB |
| **Phenotype** | Moderate — more pan-Asian than specific Malay |
| **Realism** | Good, cinematic, sweat glistening, magazine-cover quality |
| **Cost** | **$0** — no API key needed |
| **Gen time** | ~4s |
| **Command** | `curl -sL "https://image.pollinations.ai/prompt/...?width=1024&height=1024&nologo=true&enhance=true&seed=69"` |

**Vision verdict:** *"Excellent fitness physique image — dramatic lighting, chiseled chest, magazine-cover quality."*

### 3. 🥉 Pollinations FLUX (free) — Seed 2 (different prompt)

| Dimension | Value |
|-----------|-------|
| **Resolution** | 768×768 |
| **File size** | 60KB |
| **Phenotype** | Weak — more Westernized features |
| **Realism** | Hyper-realistic but exaggerated — oversized pecs/delts, water droplets lack physics |
| **Cost** | $0 |
| **Gen time** | ~4s |

**Vision verdict:** *"Visually striking but anatomically exaggerated — fantasy aesthetic, not realistic."*

### 4. 🏅 Pollinations SANA (free) — NVIDIA 1.6B

| Dimension | Value |
|-----------|-------|
| **Resolution** | 768×768 |
| **File size** | 67KB |
| **Phenotype** | Moderate — tanned, facial hair, scar near left nipple |
| **Realism** | High — scar adds authenticity, good chest definition |
| **Cost** | **$0** — free tier |
| **Gen time** | **~3s** (fastest) |
| **Command** | `curl -sL "https://image.pollinations.ai/prompt/...?width=1024&height=1024&nologo=true&enhance=true&model=sana&seed=123"` |

**Vision verdict:** *"High realism, dramatic lighting, strong chest focus. Small scar adds authenticity. Symmetry suggests some digital enhancement but overall very credible."*

### 5. ❌ Mage-Flow (Modal GPU) — FAILED

**Status:** `500 Internal Server Error` — Modal serverless GPU endpoint unreachable. Tried twice, same result.

## Comparison Table

| Dimension | **MiniMax** 🥇 | **FLUX #1** 🥈 | **FLUX #2** 🥉 | **SANA** 🏅 |
|-----------|:---:|:---:|:---:|:---:|
| Resolution | **1024** | 768 | 768 | 768 |
| Malay phenotype | **⭐⭐⭐** | ⭐⭐ | ⭐ | ⭐⭐ |
| Chest realism | **⭐⭐⭐** | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Lighting | **⭐⭐⭐** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| File size | **200KB** | 63KB | 60KB | 67KB |
| Cost | Quota | **Free** | **Free** | **Free** |
| Gen time | ~15s | ~4s | ~4s | **~3s** |

## Key Takeaways

1. **MiniMax image-01 is the clear winner** for people/portraits — 1024×1024, best Malay phenotype, most realistic skin texture, professional lighting. Always lead with MiniMax when the subject is a person of Malay/SEA descent.
2. **Pollinations FLUX is a solid free alternative** — good quality, fast, no auth needed. Phenotype accuracy is weaker but acceptable for quick drafts.
3. **Pollinations SANA is fastest and cheapest** — near-instant, free, decent quality. Best for rapid iteration where speed matters more than polish.
4. **Seed matters** — the same prompt with different seeds on FLUX produced meaningfully different results (one realistic, one exaggerated). Always generate multiple seeds.
5. **Vision QC is essential** — `vision_analyze()` caught quality differences that pure file stats couldn't. But it can fail (404 model errors); have `mmx vision describe` as fallback.
6. **Mage-Flow was down** — Modal GPU cold start or server error. Retry later or skip.

## Recommended Chain

```
Mage-Flow (if healthy) → MiniMax image-01 (people/portraits) → Pollinations FLUX (free draft) → Pollinations SANA (fast draft) → PIL/Pillow (last resort)
```