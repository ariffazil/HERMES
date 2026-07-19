# Sabah NE-SW Cross-Section SVG Template

> Proven: 2026-07-05 (Semporna → Kinabalu → Crocker Range → Dangerous Ground)
> Use when: building a schematic/interpretive cross-section from document data.

## When to use SVG vs matplotlib

- **SVG→Playwright→PNG**: Interpretive cross-sections where you control symbology (patterns, annotations, strain arrows, depth-partitioned layers). No coordinate data needed — you draw from concept.
- **matplotlib→PNG**: Data-driven cross-sections with real well picks, seismic horizons, GPS vectors. Needs numpy arrays and coordinate systems.

**Decision rule:** Drawing from a model/interpretation → SVG. Drawing from data → matplotlib.

## The template structure

```html
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>body { margin: 0; padding: 20px; background: #fff; font-family: 'Times New Roman', serif; }</style>
</head><body>
<svg width="1100" height="700" viewBox="0 0 1100 700" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- 1. PATTERNS: one per lithology -->
    <pattern id="sediment" width="4" height="4" patternUnits="userSpaceOnUse">
      <line x1="0" y1="2" x2="4" y2="2" stroke="#8B8378" stroke-width="0.5" opacity="0.5"/>
    </pattern>
    <pattern id="granite" width="6" height="6" patternUnits="userSpaceOnUse">
      <circle cx="3" cy="3" r="1.2" fill="#A0522D" opacity="0.4"/>
    </pattern>
    <pattern id="lithMantle" width="8" height="8" patternUnits="userSpaceOnUse">
      <line x1="0" y1="8" x2="8" y2="0" stroke="#8B7355" stroke-width="0.5" opacity="0.4"/>
    </pattern>
    <pattern id="astheno" width="12" height="12" patternUnits="userSpaceOnUse">
      <circle cx="6" cy="6" r="2" fill="#D2691E" opacity="0.25"/>
    </pattern>
    <!-- 2. ARROW MARKERS -->
    <marker id="arrowComp" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#C0392B"/>
    </marker>
    <marker id="arrowExt" markerWidth="8" markerHeight="6" refX="0" refY="3" orient="auto">
      <polygon points="8 0, 0 3, 8 6" fill="#2980B9"/>
    </marker>
  </defs>

  <!-- 3. LAYERS as filled <path> with curved Moho -->
  <!-- Vertical: 0km = y:60, 100km = y:660. Scale: 6px/km -->
  <!-- Moho varies: >40km (Crocker) → 32km (Kinabalu) → 28km (Dangerous Ground) -->
  <path d="M50,240 L300,252 L500,312 L680,252 L920,228 L1050,228 L1050,620 L50,620 Z"
        fill="url(#lithMantle)" stroke="#8B7355" stroke-width="1"/>
  
  <!-- 4. KEY FEATURES as positioned elements -->
  <!-- Granite intrusion: <ellipse> with granite pattern -->
  <!-- Volcanic arc: <rect> with volcanic pattern + rx for rounded corners -->
  <!-- Mobile shale: <rect> with shale pattern -->
  <!-- Thrust front: <path> with triangle markers -->
  
  <!-- 5. STRAIN ARROWS: compression (red), extension (blue), drip (purple) -->
  <!-- 6. LEGEND: top-left box with all pattern swatches -->
  <!-- 7. DEPTH SCALE: left margin, 0/10/25/35/50/100 km ticks -->
  <!-- 8. HORIZONTAL SCALE: bottom bar with "~200 km (not to scale)" -->
  <!-- 9. GOVERNING SENTENCE: bottom-left, italic, bold -->
</svg>
</body></html>
```

## Rendering

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1200, 'height': 800})
    page.goto('file:///root/cross_section.html')
    page.wait_for_timeout(1000)
    page.screenshot(path='/root/cross_section.png', full_page=True)
    browser.close()
```

## Pitfalls

1. **SVG marker references are case-sensitive.** `url(#arrowEnd)` when the marker is `id="arrowExt"` → silent failure (no arrow rendered). Always verify marker IDs match.
2. **Playwright clips content outside viewBox.** Keep all elements within the viewBox bounds. Use negative y-values for labels above the surface (Kinabalu peak label at y:-20 needs viewBox to start at y=0 or use transform).
3. **Pattern fills don't scale with zoom.** `patternUnits="userSpaceOnUse"` means the pattern is in SVG coordinates. If you zoom the SVG, the pattern stays the same size. This is correct for geological patterns (grain size is absolute).
4. **`full_page=True` in Playwright captures the full page** including content below the viewport. Without it, you only get the viewport-sized crop.
5. **Serif fonts must be available on the system.** Use `'Times New Roman', 'DejaVu Serif', serif` as the font-family stack. DejaVu Serif is the fallback on Linux.

## Sabah cross-section data points

| Feature | Position (x) | Depth (y) | Source |
|---------|-------------|-----------|--------|
| Semporna volcanic arc | 60-160 | 0-70 | Pilia et al. 2023 |
| NSPW mobile shale | 350-470 | 65-115 | Morley et al. 2022 |
| Kinabalu granite | 495-565 | 45-155 | Cottam et al. 2013 |
| Crocker Range thrust | 680-710 | 35-48 | Madon et al. 2025 |
| 2015 Mw 6.0 earthquake | 450 | 140 | Wang et al. 2017 |
| Lithospheric drip | 125-175 | 370-430 | Pilia et al. 2023 |

Moho depths: ~30 km (Semporna), ~32 km (Kinabalu), >40 km (Crocker), ~28 km (Dangerous Ground).

Output: `/root/sabah_cross_section.png` (111 KB, 1100×700 SVG rendered via Playwright)
