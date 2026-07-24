# Dark-Themed Figure Patterns (Mode B)

Matplotlib rcParams for dark-themed intelligence dossier figures.

## rcParams (copy-paste)

```python
plt.rcParams.update({
    'figure.facecolor': '#0d1117',
    'axes.facecolor': '#0d1117',
    'text.color': '#e6edf3',
    'axes.labelcolor': '#e6edf3',
    'xtick.color': '#8b949e',
    'ytick.color': '#8b949e',
    'axes.edgecolor': '#30363d',
    'grid.color': '#21262d',
    'font.family': 'DejaVu Sans',
    'font.size': 10,
})
```

## Color Assignments (semantic)

| Purpose | Hex | Usage |
|---------|-----|-------|
| Structure/anticlines | `#7ee787`, `#56d364`, `#3fb950` | Green gradient for geological features |
| Risk/warning | `#f85149` | Faults, thrust arrows, decline curves |
| Data/info | `#58a6ff` | Production curves, seismic data |
| Highlight | `#f0a500` | Key annotations, Block P markers |
| Secondary | `#ffa657` | Subheadings, secondary features |
| Fill (structural) | `#2d5016`, `#1a3a2e`, `#0d2818` | Dark green fills for anticline volumes |
| Fill (stratigraphic) | `#d29922` | Amber for reservoir sand packages |
| Fill (source/seal) | `#2ea043` | Green for source rock intervals |

## Text Label Readability

Over colored fills, use path effects for legibility:

```python
import matplotlib.patheffects as pe
ax.text(x, y, 'Label', color='#f0a500',
        path_effects=[pe.withStroke(linewidth=3, foreground='#0d1117')])
```

## Table Styling (reportlab)

```python
from reportlab.lib.colors import HexColor

DARK_BG = HexColor('#0d1117')
PANEL_BG = HexColor('#161b22')
GOLD = HexColor('#f0a500')
BORDER = HexColor('#30363d')
TEXT_LIGHT = HexColor('#e6edf3')

t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a2332')),  # header
    ('TEXTCOLOR', (0, 0), (-1, 0), GOLD),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8.5),
    ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_LIGHT),
    ('BACKGROUND', (0, 1), (-1, -1), PANEL_BG),
    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [PANEL_BG, HexColor('#1a1f28')]),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
```

## Figure Types Tested (2026-07-07)

1. **Schematic cross-section** — structural trend with anticlines, thrust faults, seafloor
2. **Side-by-side comparison** — pre-kinematic vs syn-kinematic reservoir models
3. **Map view** — mud canopy extent with volcano centers, structural axes, field locations
4. **Stratigraphic column** — petroleum systems chart with source/reservoir/seal/trap
5. **Timeline** — structural evolution phases with key events
6. **Production curve** — decline profile with capacity lines and event markers

All rendered at 200 DPI, saved as PNG, embedded in reportlab via `Image(path, width=16*cm, height=N*cm)`.

## Pitfalls

- Dark figures embedded in dark PDF look seamless. White figures embedded in dark PDF look broken — always use dark rcParams when generating for Mode B.
- Grid lines should be very subtle (`alpha=0.1` to `0.15`) — heavy grids overwhelm dark backgrounds.
- Avoid pure white text (`#ffffff`) — use near-white (`#e6edf3`) for less eye strain.
- Matplotlib `savefig()` needs `facecolor` set explicitly if you override the figure-level facecolor after creation.
