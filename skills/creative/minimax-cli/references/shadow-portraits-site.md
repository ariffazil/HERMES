# Shadow Institutional Portraits for arif-fazil.com

Pattern for generating dark-themed institutional portraits for the Shadow Decoder at `/politics/shadow/`.

## When to use

Adding individual portraits to the Shadow PM profiles (or any institutional figure profile on the site). Uses MiniMax image-01 as primary engine for Malaysian/SEA phenotypes.

## Prompt formula

```
[person description] + dark charcoal background + amber #d4a574 accent lighting
+ chiaroscuro moody + hyperrealistic skin pores + no AI artifacts
+ shadow institutional portrait
```

Key: the dark background + amber accent (#d4a574, the arif-fazil.com institutional palette) creates visual consistency across all portraits. Chiaroscuro lighting elevates from generic AI portrait to shadow decoder style.

## Generation workflow

1. **Batch sequentially** — MiniMax image-01 cannot be called in parallel from CLI (overwrites `image_001.jpg` each time). Generate one, copy output, then next:
   ```bash
   source /root/.secrets/kunci-mas.env
   mmx image generate --prompt "..." --aspect-ratio 1:1 --non-interactive
   cp image_001.jpg /tmp/shadow-pm-images/{slug}.jpg
   ```
2. **Distinguishing features** — each PM needs unique descriptors. Don't just say "Malay man in suit." Add: glasses, build, facial hair, age, expression.
3. **Deploy to** `/var/www/html/arif/politics/shadow/images/{slug}.jpg`
4. **Register in JSON** — add `"image": "images/{slug}.jpg"` to the PM's entry in `shadow-decoder.json`

## CSS for display

```css
.pm-portrait{width:200px;height:200px;border-radius:50%;
  border:2px solid var(--accent);object-fit:cover;
  box-shadow:0 0 30px rgba(212,167,116,0.2)}
```
Thumbnail variant: `.thumb{width:36px;height:36px;border-radius:50%}`

## Known limitations

- **Not photorealistic** — AI cannot generate accurate portraits of specific real historical figures. Outputs are stylized archetypes that capture era/mood/features, not recognizable faces.
- **Pollinations SANA rate-limit** — sequential calls to the free tier trigger aggressive rate-limiting (consecutive requests return JSON errors). MiniMax image-01 is the reliable path.
- **MiniMax overwrites** — `mmx image generate` always saves to `image_001.jpg` regardless of `--output` flag. Must copy immediately after each generation.
- **Tunku portrait** — generated via Pollinations SANA (768×768, 50KB) due to rate-limit constraints on MiniMax batch. Acceptable quality for thumbnail but visibly lower resolution than other 9 portraits.

## Proven 2026-08-03

Generated all 10 Malaysian PM portraits for Shadow Decoder deployment. MiniMax image-01 produced 9 portraits at 1024×1024 (~110-160KB each). Tunku Abdul Rahman used Pollinations SANA fallback.
