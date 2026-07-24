# Petroleum System Modeling Figure Patterns

> Proven: 2026-07-22 — GEOX PSM Sabah dossier (6 figures, matplotlib dark theme, Mode B).
> Reusable matplotlib patterns for basin modeling, burial-thermal history, and hydrocarbon generation timing.

## Figure 1 — Regional Basin Map

Polygon-fill basin outlines on coordinate axes:
```python
# Fill + dashed outline for each basin
ax.fill(basin_x, basin_y, alpha=0.25, color=COLOR, label='Basin Name')
ax.plot(basin_x, basin_y, color=COLOR, linewidth=1.5, linestyle='--')
# Discoveries: scatter + annotate
ax.scatter(x, y, s=60, color=color, edgecolors='white', linewidth=0.8, zorder=5)
ax.annotate(name, (x,y), xytext=(x+0.05, y+0.08), fontsize=6, color=color)
```

## Figure 2 — Contrasting Stratigraphic Columns

Side-by-side `barh` columns for two basins:
```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 7))
# Each formation as a horizontal bar
for name, top_ma, base_ma, color, desc in formations:
    ax.barh((top+base)/2, 1.0, base-top, color=color, edgecolor=BORDER, alpha=0.85)
    ax.text(0.55, (top+base)/2, name, fontsize=7, va='center', fontweight='bold')
ax.invert_yaxis()  # oldest at bottom
```

## Figure 3 — Burial History + Thermal Maturity

**Left panel — Burial curves:**
```python
ax.fill_between(time_ma, depth_top, depth_base, alpha=0.25, color=GREEN, label='Source Rock')
ax.plot(time_ma, depth_top, color=GREEN, linewidth=1.5)
ax.invert_xaxis()  # time runs right-to-left (present on right)
ax.invert_yaxis()  # depth increases downward
```

**Right panel — Ro vs depth:**
```python
ax.plot(ro_values, depth_km, color=GREEN, linewidth=2.5, marker='o', markersize=5)
ax.axvspan(0.6, 1.0, alpha=0.12, color=AMBER)  # oil window
ax.axvspan(1.0, 1.35, alpha=0.12, color=RED)   # wet gas window
ax.invert_yaxis()
```

**Key annotations:**
- MMU marker: `ax.axvline(x=15.9, color=RED, linestyle='--')`
- Oil window entry: `ax.axhline(y=2.5, color=AMBER, linestyle=':')`
- Reservoir horizon as separate curve
- Source rock depth band: `ax.axhspan(top, base, alpha=0.12, color=GREEN)`

## Figure 4 — Hydrocarbon Generation Timing

Gaussian-like generation rate curves:
```python
time_ma = np.linspace(35, 0, 200)
oil_rate = np.exp(-((time_ma - peak_oil_ma)**2) / (2 * sigma**2))
gas_rate = np.exp(-((time_ma - peak_gas_ma)**2) / (2 * sigma**2))
ax.fill_between(time_ma, oil_rate, alpha=0.30, color=GREEN)
ax.fill_between(time_ma, gas_rate, alpha=0.25, color=RED)
ax.invert_xaxis()
```

**Key annotations:**
- Vertical lines for tectonic events (rifting, MMU, trap formation)
- `ax.axvspan` for trap formation window
- Text labels at each event line: `ax.text(t, height, label, fontsize=6, color=COLOR, ha='center', fontweight='bold')`
- Critical moment annotation box: `bbox=dict(boxstyle='round', facecolor=PANEL, edgecolor=GOLD)`

## Figure 5 — Basin Cross-Section

Sinusoidal horizons with structural deformation:
```python
seabed = -0.2 + 0.3*np.sin(x*0.06) + 0.15*np.sin(x*0.15+2)  # wavy seabed
mmu = seabed - 2.5 + 0.6*np.sin(x*0.04+1)                      # MMU horizon
basement = mmu - 6 + 0.5*np.sin(x*0.02)                         # basement
ax.fill_between(x, seabed, 5, alpha=0.12, color=BLUE)          # water column
```

**Fold-thrust structures:**
- Gaussian anticline shapes: `fold_y = base - 0.8 - 0.6*np.exp(-((x-cx)**2)/15)`
- Thrust fault lines connecting fold crests to deeper detachment
- Half-graben shapes for extensional side: `graben_y = base - 2.5 - np.exp(-((x-cx)**2)/8)`

**Pitfall:** `broken_barh` does NOT accept hatch strings in `facecolors`. Use `barh` with separate `hatch` kwarg instead.

## Figure 6 — PSM Toolchain Diagram

FancyBboxPatch flow diagram:
```python
from matplotlib.patches import FancyBboxPatch
box = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.1",
                      facecolor=PANEL, edgecolor=COLOR, linewidth=1.5, alpha=0.9)
ax.add_patch(box)
```
Arrows between tool boxes and output boxes:
```python
ax.annotate('', xy=(x_end, y), xytext=(x_start, y),
            arrowprops=dict(arrowstyle='->', color=DIM, lw=1.5))
```

## Mode B Dark Theme (matplotlib rcParams)

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
    'grid.alpha': 0.4,
    'font.family': 'DejaVu Sans',
    'font.size': 9,
    'figure.dpi': 200,
})
```

## Pitfalls (PSM-specific)

- **Emoji glyphs (🛢) are missing in DejaVu Sans.** Replace with plain text markers (e.g., "MEGAH-1" bold instead of oil drum icon). Harmless `UserWarning` — figure still renders.
- **GEOX tools may require governed session** (`LANE_ENFORCEMENT` — session_id required). When `geox_basin` / `geox_thermal_maturity` fail on lane enforcement, pivot to published data + forward modeling. The PSM workflow still works: web research for basin data, matplotlib for burial/generation curves. This is the standard fallback per geological-artifact-rigor §Artifact Workflow step 1.
- **Cross-section geometry:** Don't use `broken_barh` for lithology fills — use `fill_between` with wavy polygon boundaries. Falls under geological-artifact-rigor Rule 2 (no cartoon geometry).
- **Burial curve depth axes:** Always `invert_yaxis()` for depth and `invert_xaxis()` for geological time (present on right, past on left).
