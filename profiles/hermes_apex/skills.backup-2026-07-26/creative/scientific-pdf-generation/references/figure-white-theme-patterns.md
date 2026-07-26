# Figure Regeneration — White Theme Pattern

## Problem
Figures generated with matplotlib dark theme (GitHub dark mode colors) look terrible in scientific PDFs. The dark background clashes with white PDF pages, and monospace fonts look like code.

## Solution
Regenerate all figures with a clean scientific matplotlib style before assembling the PDF.

## Matplotlib rcParams Override

```python
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#fafafa",
    "text.color": "#1a1a1a",
    "axes.labelcolor": "#1a1a1a",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "axes.edgecolor": "#666666",
    "grid.color": "#cccccc",
    "grid.alpha": 0.5,
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Liberation Serif", "Times New Roman"],
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})
```

## Publication Color Palette (Muted)

```python
COLORS = {
    "blue": "#2c5f8a",
    "red": "#8b2500",
    "green": "#2e7d32",
    "amber": "#e65100",
    "purple": "#6a1b9a",
    "teal": "#00695c",
    "gray": "#666666",
}
```

## Figure Patterns Used

### Tectonic Map (fig1)
- Simplified coastline with fill (#e8e8e8)
- Study area highlight with blue fill (alpha=0.12)
- GPS vectors via `ax.quiver()`
- Stress domain labels with `bbox=dict(boxstyle="round", facecolor="white")`
- Muted legend with `framealpha=0.9`

### Depth Cross-Section (fig2)
- Horizontal bars (`ax.barh`) for depth layers
- Background colors per layer (e.g., `#e8f5e9` for sedimentary)
- Layer labels centered on each bar
- Process descriptions below labels in italic

### Cooling Path (fig3)
- Line plot with markers (`"o-"`)
- Annotation boxes with `bbox=dict(boxstyle="round", facecolor="white")`
- Cooling rate annotations along curve segments
- Partial annealing zone as `ax.axhspan()`

### Kill Matrix (fig6)
- Grid of colored rectangles via `ax.add_patch(plt.Rectangle(...))`
- Color coding: green (#c8e6c9) = PASS, yellow (#fff9c4) = REVIEW, red (#ffcdd2) = KILL
- Use ASCII letters P/R/K instead of Unicode symbols (✓/?/✗) — DejaVu Serif may lack glyphs
- Equal aspect ratio for square cells

## Pitfalls
- **Unicode glyphs missing**: DejaVu Serif lacks ✓ (U+2713) and ✗ (U+2717). Use P/R/K or PASS/REVIEW/KILL.
- **pyrolite.mplstyle conflict**: If you see "Bad key legend.bbox_to_anchor" warning, it's a stale user matplotlibrc. Harmless — ignore.
- **Color-vision accessibility**: Muted palette above has sufficient contrast for deuteranopia. Avoid red-green-only schemes.
