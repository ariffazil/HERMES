# SVG Geological Cross-Section Generator

> Proven 2026-07-28: Aliff's House Lenggeng cross-section — hand-built SVG rendered to PNG via Playwright.

## When to Use

When you need a geological cross-section but:
- matplotlib/GEOX patterns aren't available or suitable
- You want dark theme / federation-style visual language
- The audience is a geologist colleague (Aliff-level) — needs proper lithology symbols, fault markers, depth scale
- You want to deliver as image (PNG) via Telegram/chat, not just HTML

## The Approach: Hand-Built SVG → Playwright Screenshot

```
1. Write HTML+SVG file with complete cross-section geometry
2. Use Playwright to open the file and screenshot to PNG
3. Deliver via MEDIA:/path/to/screenshot.png
```

## Required SVG Elements for Geological Credibility

A cross-section a geologist will accept needs:

| Element | SVG Technique |
|---|---|
| **Lithology patterns** | SVG `<pattern>` with circles for granite, dots for sand, dashes for shale |
| **Topographic profile** | `<path>` with gentle undulations along top edge |
| **Unit boundaries** | Wavy `<path>` lines (use bezier curves: `C x1 y1, x2 y2, endx endy`) |
| **Faults** | Bold line + sawteeth/ticks on hanging wall (use `<path>` with half-arrows for movement) |
| **Joints/fractures** | Thin dashed lines orthogonal to fault zone |
| **Water table** | Dashed blue line: `stroke-dasharray="5,3"` |
| **Scale bar** | Horizontal line with tick marks at 0, 2km, 4km intervals |
| **Depth labels** | Text along left side |
| **VE label** | "VE ~3×" — vertical exaggeration |
| **Legend** | Separate grid below the SVG showing all patterns |
| **Title block** | Location W–E, approximate coordinates, vertical exaggeration |

## Lithology SVG Pattern Templates

### Granite (fresh bedrock)
```svg
<pattern id="granite" patternUnits="userSpaceOnUse" width="20" height="20">
  <rect width="20" height="20" fill="#3a2a1a"/>
  <!-- Quartz crystals -->
  <circle cx="4" cy="5" r="1.2" fill="#5a4a3a" opacity="0.6"/>
  <circle cx="14" cy="12" r="0.8" fill="#2a1a0a" opacity="0.5"/>
  <!-- Feldspar laths -->
  <rect x="10" y="2" width="1.5" height="0.5" fill="#8a7a5a" opacity="0.3" transform="rotate(30 11 2)"/>
  <!-- Biotite flakes -->
  <rect x="2" y="10" width="1" height="0.4" fill="#8a7a5a" opacity="0.3" transform="rotate(-20 2 10)"/>
</pattern>
```

### Saprolite (weathered granite)
```svg
<pattern id="saprolite" patternUnits="userSpaceOnUse" width="12" height="12">
  <rect width="12" height="12" fill="#8a6a3a"/>
  <rect x="0" y="0" width="12" height="12" fill="none" stroke="#a08050" stroke-width="0.3" stroke-dasharray="2,3"/>
  <circle cx="3" cy="3" r="0.8" fill="#b09050" opacity="0.5"/>
  <circle cx="9" cy="8" r="0.6" fill="#705030" opacity="0.4"/>
</pattern>
```

### Alluvium (sand + gravel)
```svg
<pattern id="alluvium" patternUnits="userSpaceOnUse" width="8" height="8">
  <rect width="8" height="8" fill="#c8b070"/>
  <circle cx="2" cy="2" r="0.5" fill="#d8c080"/>
  <circle cx="6" cy="6" r="0.4" fill="#b89850"/>
  <circle cx="2" cy="6" r="0.3" fill="#d8c080"/>
</pattern>
```

### Fault zone
```svg
<pattern id="fault" patternUnits="userSpaceOnUse" width="6" height="6">
  <rect width="6" height="6" fill="#2a1a0a"/>
  <line x1="0" y1="0" x2="6" y2="6" stroke="#4a3a2a" stroke-width="0.5" opacity="0.4"/>
  <line x1="6" y1="0" x2="0" y2="6" stroke="#4a3a2a" stroke-width="0.5" opacity="0.4"/>
</pattern>
```

## Key SVG Techniques

### Wavy formation boundary with bezier curves
```svg
<path d="M 30,230 L 970,230 L 970,370 Q 800,365 600,370 Q 400,375 200,368 L 30,370 Z"
      fill="url(#saprolite)" opacity="0.8"/>
```

### Fault with movement indicators
```svg
<line x1="290" y1="190" x2="285" y2="620" stroke="#8a3a2a" stroke-width="1.5" opacity="0.6"/>
<!-- Half-arrows showing motion -->
<path d="M 275,350 L 268,345 L 275,345 Z" fill="#aa4a3a" opacity="0.3"/>
```

### House/building marker on surface
```svg
<line x1="610" y1="145" x2="610" y2="195" stroke="#d4a847" stroke-width="1.5" stroke-dasharray="2,2"/>
<polygon points="610,140 604,155 616,155" fill="#d4a847"/>
<rect x="598" y="165" width="24" height="18" rx="2" fill="#1a1a0a" stroke="#d4a847" stroke-width="0.8"/>
```

### Water table (dashed blue)
```svg
<path d="M 30,285 Q 200,295 400,290 Q 600,285 800,295 Q 900,290 970,292"
      fill="none" stroke="#4a8ab4" stroke-width="0.7" stroke-dasharray="5,3" opacity="0.6"/>
```

## Playwright Screenshot Pipeline

```bash
#!/bin/bash
# Render SVG cross-section to PNG

OUTDIR="/root/.hermes/artifacts/geology"
mkdir -p "$OUTDIR"

cat << 'PYEOF' | python3 -
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1200, "height": 900})
        await page.goto(f"file:///root/.hermes/artifacts/geology/lenggeng-cross-section.html")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="/root/.hermes/artifacts/geology/lenggeng-cross-section.png", full_page=True)
        await browser.close()
        print("✅ Screenshot saved")

asyncio.run(main())
PYEOF
```

## Deliver to User

```bash
echo "MEDIA:/root/.hermes/artifacts/geology/lenggeng-cross-section.png"
```

The image appears inline on supported platforms (Telegram). Provide geological explanation in the message body.

## Pitfalls

- **SVG viewBox must match actual drawing area.** If your coordinates go from x=30 to x=970, set `viewBox="0 0 1000 620"`.
- **Dark theme contrast.** White text on dark background = readable. Avoid pure black (#000) — use #0a0a0a.
- **Pattern fills may not scale.** Use `patternUnits="userSpaceOnUse"` so patterns tile consistently.
- **Playwright requires chromium binary.** Check with `which chromium-browser`.
- **Screenshot timing.** Add `wait_for_timeout(1000)` after goto to ensure fonts render.
- **Full page vs viewport.** `full_page=True` captures entire scroll; needed for tall cross-sections.
