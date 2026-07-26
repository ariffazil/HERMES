# Tectono-Stratigraphic Multi-Panel Evolution Diagram

Multi-column, multi-row grid showing geological evolution through time. Each column = time stage, each row = depth panel. Used for tectonic evolution stories (subduction → collision → basin formation).

## Grid Layout (matplotlib gridspec)

```python
gs = fig.add_gridspec(4, 5,  # 4 rows (header + 3 depth) × 5 columns (stages)
    height_ratios=[0.4, 2.5, 3.5, 3.5],  # header row shorter
    hspace=0.08, wspace=0.05, left=0.03, right=0.97, top=0.95, bottom=0.03)
```

## Row Structure

- Row 0: Stage headers — colored boxes with stage name, time label, subtitle
- Row 1: Deep lithosphere — mantle, slab, drip processes
- Row 2: Crust/Wedge — continental crust, mobile shale, underthrust
- Row 3: Basin/Stratigraphy — reservoirs, mini-basins, charge events

## Key Patterns

- Geological units: `ax.fill(x_coords, y_coords, color=color, alpha=0.5, edgecolor=color)` — polygon fills with distinct colors per lithology
- Subduction/slab: dark blue (#1a5276) with alpha, dashed edges for fossil/stagnant
- Continental crust: amber (#b7950b), alpha 0.4-0.6
- Mobile shale/NSPW: red (#c0392b), alpha 0.4-0.7, thicker edge (linewidth=2)
- Mud canopy: bright red (#e74c3c), alpha 0.3, prominent labels
- Reservoir sands: orange (#f39c12), alpha 0.5-0.7
- Water column: light blue (#aed6f1), alpha 0.2
- Process arrows: `ax.annotate('', xy=target, xytext=source, arrowprops=dict(arrowstyle='->', color=color, lw=2))`
- Overpressure indicators: 'P!' text labels in red at key locations
- Regime transition bar at bottom: `fig.text()` with italic description spanning full width
- Row labels on far left: rotated 90°, positioned at vertical center of each row
- Each subplot: `ax.set_aspect('equal')`, hide ticks and spines

## Color Semantics

```
Slab (active):   #1a5276, alpha=0.5
Slab (fossil):   #1a5276, alpha=0.15-0.3, ls=':'
Slab drip:       #e74c3c, alpha=0.4-0.5
Continental:     #b7950b, alpha=0.4-0.6
NSPW (forming):  #c0392b, alpha=0.4
NSPW (mobile):   #c0392b, alpha=0.6-0.7
Mud canopy:      #e74c3c, alpha=0.3
Reservoir:       #f39c12, alpha=0.5-0.7
Setap/detach:    #7f8c8d, alpha=0.5-0.6
Water:           #aed6f1, alpha=0.2
```

## Workflow

1. Define `plt.rcParams` with white-bg serif theme (same as other geological figures)
2. Create `fig` with `plt.figure(figsize=(20, 14))` — large for 5-column layout
3. Add gridspec with height_ratios for header + 3 depth rows
4. Draw column headers (Row 0) as colored boxes with stage info
5. For each stage column, create 3 subplots (one per depth row)
6. In each subplot: set xlim/ylim, hide ticks/spines, fill geological units
7. Add annotations (arrows, labels, callout boxes) for key processes
8. Add regime transition bar at bottom via `fig.text()`
9. Save at 200 DPI, bbox_inches='tight'

## Pitfalls

- **Equal aspect ratio is critical.** Without `ax.set_aspect('equal')`, geological cross-sections will be distorted and unreadable.
- **Hide ALL spines and ticks.** The panels are cartoons, not plots — axis lines add nothing.
- **Alpha values must differ by lithology.** If all fills have the same alpha, the figure becomes a blob. Use 0.15 for background (mantle), 0.3-0.5 for major units, 0.6-0.7 for active/mobile features.
- **Large figsize needed.** 5 columns × 3 rows requires at least (20, 14) inches. Smaller figures will have unreadable labels.
- **Polygon coordinates must close.** `ax.fill()` closes automatically, but `ax.fill_between()` does not — ensure x-ranges span the intended area.

## Provenance

- **2026-07-07**: NSPW Mud Canopy Evolution, deepwater Sabah. 5 stages (Eocene–Present), 3 depth panels. 490 KB PNG. Illustrated PSCS subduction → Dangerous Grounds collision → NSPW overpressure → mini-basin province → mud canopy burst.
