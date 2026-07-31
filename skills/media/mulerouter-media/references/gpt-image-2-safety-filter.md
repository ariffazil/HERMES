# GPT Image 2 Safety Filter — 2026-07-30

## Discovery

During a multi-engine image generation comparison (2026-07-30), the MuleRouter GPT Image 2 endpoint rejected a fitness/bodybuilding prompt with shirtless content:

**Prompt:** `"Handsome Southeast Asian Malay man, attractive face, sharp jawline, chiseled athletic physique, defined chest and abs, gym workout, shirtless, studio photography, soft dramatic lighting, masculine, confident smile, high fashion fitness aesthetic, 8K photorealistic"`

**Response:** HTTP 200 (task accepted), then polling returned:
```json
{"code": 2001, "title": "Parameter validation failed",
 "detail": "Input content was rejected by safety inspection. Please adjust your input."}
```

## Trigger Words

The safety filter appears to be triggered by any combination of:
- `shirtless`
- `bodybuilding` / `bodybuilder`
- `gym workout` / `fitness`
- `sweat` / `sweat glistening`
- `muscular` / `muscle definition` / `chiseled`
- `pecs` / `chest` (in context of showing)

## Workarounds

### 1. Use Wan 2.6 T2I instead (no safety filter)

```bash
source /root/.secrets/kunci-mas.env
/root/HERMES/scripts/mulerouter-image.py \
  --prompt "Handsome Malay man, muscular chest, gym, fitness" \
  --model wan --size 1024x1024 --output /tmp/result.png
```

✅ **Confirmed working:** Wan 2.6 T2I generated shirtless fitness content without safety filter rejection.

### 2. Dress the subject for GPT Image 2

Replace "shirtless" with clothing that still shows physique:
- `"fitted white tank top"`
- `"tight athletic shirt"`
- `"sleeveless gym top"`

### 3. Use MiniMax image-01 (best quality)

MiniMax handles fitness/bodybuilding content professionally without safety filter issues:
```bash
mmx image generate --prompt "Southeast Asian Malay muscular man, shirtless, gym, studio lighting" --aspect-ratio 1:1 --non-interactive
```

## Safety Filter Comparison Across Engines

| Engine | Shirtless Allowed? | Notes |
|--------|-------------------|-------|
| MiniMax image-01 | ✅ Yes | Professional fitness aesthetic |
| MuleRouter Wan 2.6 T2I | ✅ Yes | Fast, good quality |
| MuleRouter GPT Image 2 | ❌ Blocked | Input safety filter |
| Pollinations FLUX (free) | ✅ Yes | No filter on free tier |
| Pollinations SANA (free) | ✅ Yes | No filter on free tier |
| Mage-Flow | ✅ Yes (not tested) | Down during session |

## Principle

This is a **provider-level safety filter**, not a model-level limitation. The same base model (GPT Image 2) may produce different outputs depending on the provider's infrastructure layer. Never claim universal model behavior — always attribute to the specific provider and endpoint tested.