# MuleRouter Image Generation Results — 2026-07-30

**Prompt (GPT Image 2):** "Handsome Southeast Asian Malay man, attractive face, sharp jawline, athletic build, wearing a fitted white tank top that shows muscular chest and arms, gym background, studio lighting, confident smile, masculine, high fashion fitness aesthetic, photorealistic"
**Prompt (Wan 2.6 T2I):** "Handsome Southeast Asian Malay man, attractive face, sharp jawline, athletic muscular build, defined chest, gym workout, fitness, studio lighting, confident, masculine"

## MuleRouter GPT Image 2

| Dimension | Value |
|-----------|-------|
| **Resolution** | 1024×1024 |
| **File size** | 1.3MB (PNG) |
| **Phenotype** | Moderate SE Asian — light brown skin, strong jawline |
| **Realism** | High — professional fitness portrait quality, natural skin texture |
| **Chest focus** | Fitted white tank top showing defined chest and arms |
| **Face attractiveness** | 8.5/10 — symmetrical, warm smile, strong jawline |
| **Safety filter** | ✅ Blocked shirtless prompt — required clothed version |
| **Cost** | MuleRouter API key (credit-based) |
| **Gen time** | ~2min (task queued, safety filter added delay) |
| **Command** | `mulerouter-image.py --model gpt --size 1024x1024 --format png` |

**Vision verdict:** *"Professional fitness portrait — 8.5/10 handsome, symmetrical face, warm smile, realistic lighting, high-quality studio photography."*

## MuleRouter Wan 2.6 T2I

| Dimension | Value |
|-----------|-------|
| **Resolution** | 1280×1280 |
| **File size** | 2.3MB (PNG) |
| **Phenotype** | Moderate SE Asian — tanned skin, facial hair |
| **Realism** | High — shirtless, defined six-pack, broad chest, warm smile |
| **Chest focus** | Shirtless — full chest, abs, vascular arms |
| **Face attractiveness** | 8.5/10 — symmetrical, confident smile, warm expression |
| **Safety filter** | ❌ No safety filter — shirtless content allowed |
| **Cost** | MuleRouter API key (credit-based) |
| **Gen time** | ~10s (fastest of the two MuleRouter models) |
| **Command** | `mulerouter-image.py --model wan --size 1024x1024 --format png` |

**Vision verdict:** *"Shirtless bodybuilder — 8.5/10 handsome, defined six-pack, broad chest, gym background, warm expression. High realism but idealized proportions."*

## Key Takeaways

1. **Safety filter differs by model** — GPT Image 2 has input safety filter (blocks shirtless), Wan 2.6 T2I does not. Always check which model allows your content type.
2. **Wan 2.6 T2I is faster** — ~10s vs GPT Image 2's ~2min. For shirtless/fitness content, Wan is the better MuleRouter choice.
3. **MiniMax image-01 is still better** — better Malay phenotype (9.5/10 handsome vs 8.5/10), more realistic skin texture, no safety filter issues. MuleRouter is a secondary option.
4. **Higher resolution** — Wan 2.6 T2I produced 1280×1280 (largest of all engines tested), GPT Image 2 produced 1024×1024 (same as MiniMax).
5. **Parameter format matters** — --size requires exact format like 1024x1024, not square. --format requires png, jpeg, or webp, not jpg.