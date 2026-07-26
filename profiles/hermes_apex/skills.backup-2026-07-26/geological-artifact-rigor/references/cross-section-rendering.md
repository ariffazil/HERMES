# Geological Cross-Section Rendering with Matplotlib

> **Built 2026-07-20 for NW Sabah crustal models (6-panel comparison).**
> Companion to `geological-artifact-rigor` Rule 2: "No cartoon geometry."

## Why This Reference Exists

geological-artifact-rigor says "don't draw cartoon sine-wave basin shapes." This reference shows HOW to render proper geological cross-sections with distinct lithology patterns, fault symbols, and professional annotation — all programmatically via matplotlib.

## The Pattern Library

Each lithology gets a distinct pattern, not just a flat color. This scales from simple Q&A to publication-quality panels.

```python
import matplotlib.patches as mpatches
import numpy as np

# ── Sand / Clastic Sediments (dots) ──
def sand_pattern(ax, x, y, w, h, color='#C4A46C'):
    rect = mpatches.Rectangle((x,y), w, h, facecolor=color, alpha=0.3, lw=0)
    ax.add_patch(rect)
    for dx in np.arange(x+0.1, x+w-0.1, 0.3):
        for dy in np.arange(y+0.15, y+h-0.15, 0.3):
            if np.random.random() > 0.5:
                ax.plot(dx, dy, '.', color=color, markersize=1.5, alpha=0.6)

# ── Shale / Mudstone (horizontal lines) ──
def shale_pattern(ax, x, y, w, h, color='#6B5B4D'):
    rect = mpatches.Rectangle((x,y), w, h, facecolor=color, alpha=0.35, lw=0)
    ax.add_patch(rect)
    for dy in np.arange(y+0.1, y+h-0.1, 0.2):
        ax.plot([x+0.05, x+w-0.05], [dy, dy], '-', color=color, lw=0.5, alpha=0.4)

# ── Limestone / Carbonate (brick pattern) ──
def limestone_pattern(ax, x, y, w, h, color='#4A90A4'):
    rect = mpatches.Rectangle((x,y), w, h, facecolor=color, alpha=0.4, lw=0)
    ax.add_patch(rect)
    for row, dy in enumerate(np.arange(y+0.1, y+h-0.1, 0.35)):
        offset = 0.15 if row % 2 == 0 else 0
        for dx in np.arange(x+offset+0.1, x+w-0.1, 0.6):
            ax.plot([dx, dx+0.4], [dy, dy], '-', color=color, lw=1, alpha=0.5)
            ax.plot([dx, dx], [dy, dy+0.25], '-', color=color, lw=1, alpha=0.5)

# ── Oceanic Crust / Basalt (vertical streaks) ──
def ocean_crust_pattern(ax, x, y, w, h, color='#4A6B8A'):
    rect = mpatches.Rectangle((x,y), w, h, facecolor=color, alpha=0.5, lw=0)
    ax.add_patch(rect)
    for dx in np.arange(x+0.15, x+w-0.1, 0.4):
        ax.plot([dx, dx], [y+0.05, y+h-0.05], '-', color='#6BAAD0', lw=0.8, alpha=0.3)

# ── Continental Crust / Granitic (cross-hatch) ──
def cont_crust_pattern(ax, x, y, w, h, color='#D4956A'):
    rect = mpatches.Rectangle((x,y), w, h, facecolor=color, alpha=0.45, lw=0)
    ax.add_patch(rect)
    for dx in np.arange(x+0.1, x+w-0.1, 0.5):
        ax.plot([dx-0.15, dx+0.15], [y+h*0.3, y+h*0.7], '-', color=color, lw=0.8, alpha=0.3)
        ax.plot([dx+0.15, dx-0.15], [y+h*0.3, y+h*0.7], '-', color=color, lw=0.8, alpha=0.3)

# ── Accretionary Prism (chaotic hash) ──
def accretionary_pattern(ax, x, y, w, h, color='#5C6B4A'):
    rect = mpatches.Rectangle((x,y), w, h, facecolor=color, alpha=0.3, lw=0)
    ax.add_patch(rect)
    for _ in range(int(w*h*15)):
        x0 = np.random.uniform(x+0.05, x+w-0.05)
        y0 = np.random.uniform(y+0.05, y+h-0.05)
        angle = np.random.uniform(0, np.pi)
        ax.plot([x0, x0+0.15*np.cos(angle)], [y0, y0+0.15*np.sin(angle)],
                '-', color=color, lw=0.5, alpha=0.5)

# ── Magma / Pluton (cross markers) ──
def magmatic_pattern(ax, x, y, w, h, color='#CC4422'):
    rect = mpatches.Rectangle((x,y), w, h, facecolor=color, alpha=0.6, lw=0)
    ax.add_patch(rect)
    for _ in range(int(w*h*8)):
        ax.plot(np.random.uniform(x+0.1, x+w-0.1), np.random.uniform(y+0.1, y+h-0.1),
                '+', color='#FF6644', markersize=4, alpha=0.5)
```

## Fault Symbols

```python
def draw_thrust(ax, x, y_top, y_bot):
    """Thrust fault with teeth on hanging wall"""
    ax.plot([x, x+0.3], [y_top, y_bot], '-', color='#FF8844', lw=1.5, alpha=0.8)
    for i in range(3):
        t = (i+1)/4
        ax.plot([x+0.3*t-0.04, x+0.3*t], 
                [y_top-(y_top-y_bot)*t-0.04, y_top-(y_top-y_bot)*t],
                '-', color='#FF8844', lw=1, alpha=0.6)
```

## Dark Theme Color Palette

```python
COLORS = {
    'water': '#1a3a5c',       # Deep ocean
    'post_dru': '#8B7355',    # Post-DRU sediments
    'turbidites': '#C4A46C',  # Deepwater sands
    'shale': '#6B5B4D',       # Mobile shale / NSPW
    'minibasin': '#9B8B70',   # Mini-basin fill
    'accretionary': '#5C6B4A',# Accretionary prism
    'nido': '#4A90A4',        # Nido Limestone
    'cont_crust': '#D4956A',  # Continental crust
    'ocean_crust': '#4A6B8A', # Oceanic crust
    'mantle_lith': '#3A2A1A', # Mantle lithosphere
    'asthenosphere': '#8B2020',# Asthenosphere
    'magma': '#CC4422',       # Magma / pluton
    'moho_line': '#FF6644',   # True Moho
    'fake_moho': '#FFAA44',   # False/disputed Moho
}
```

## Multi-Panel Layout Pattern

For comparison diagrams (multiple models side by side), use `fig.add_axes()` with fractional coordinates:

```python
fig = plt.figure(figsize=(22, 28), facecolor='#08080f')

# Each panel gets its own axes via [left, bottom, width, height]
ax = fig.add_axes([x0/fig_w, y0, panel_w/fig_w, panel_h])

# After all panels, add a global legend strip
legend_ax = fig.add_axes([0.05, 0.015, 0.90, 0.03])
```

## Status Badges

For model comparison panels, use colored badges:

```python
def status_badge(ax, x, y, text, color):
    bbox = dict(boxstyle='round,pad=0.25', facecolor=color+'30', 
                edgecolor=color, lw=1.2)
    ax.text(x, y, text, color=color, fontsize=9, ha='center', va='center',
            fontweight='bold', fontfamily='monospace', bbox=bbox)

# Usage:
status_badge(ax, 8.5, 6.5, 'NOT FALSIFIED ✓', '#44FF44')
status_badge(ax, 8.5, 6.5, 'FALSIFIED ✗', '#FF4444')
```

## Proven Workflow (2026-07-20)

Full 6-panel crustal model comparison script: `/root/forge_work/2026-07-20/render_6panel.py`

Output: 839KB PNG at 200 DPI, dark theme, 12 lithology patterns, fault symbols, Moho markers, status badges, global legend, coordinate labels.

**Key lesson:** matplotlib with custom patterns + `fig.add_axes()` gives far more geological authenticity than SVG/HTML approaches. The random element in sand/accretionary patterns creates natural-looking texture that flat shapes can't match.
