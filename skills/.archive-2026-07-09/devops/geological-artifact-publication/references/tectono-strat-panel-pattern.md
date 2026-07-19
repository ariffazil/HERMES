# Tectono-Stratigraphic Multi-Panel Layout

Last proven: 2026-07-07, NW Sabah PSCS→NSPW→mud canopy→Rotan reservoirs.

## The Pattern

A 2D grid showing multi-stage tectonic evolution:
- **Columns** = time slices (typically 4-6 stages from oldest to youngest)
- **Rows** = vertical scale levels (typically 3: lithosphere, crust/wedge, basin/stratigraphy)

Each cell is a mini cross-section showing that vertical level at that time step.

## Implementation (matplotlib)

```python
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np

# Dark theme
plt.rcParams.update({
    'figure.facecolor': '#0d1117',
    'axes.facecolor': '#0d1117',
    'text.color': '#e6edf3',
    'axes.edgecolor': '#30363d',
    'grid.color': '#21262d',
    'font.family': 'DejaVu Sans',
    'font.size': 9,
})

fig, axes = plt.subplots(3, 5, figsize=(20, 12),
                          gridspec_kw={'height_ratios': [1.2, 1, 0.8],
                                       'hspace': 0.15, 'wspace': 0.08})

stage_titles = [
    'Stage 1\n~35–20 Ma\nEvent Name',
    'Stage 2\n~20–15 Ma\nEvent Name',
    # ... one per column
]
row_labels = ['LITHOSPHERE\n(Mantle + Slab)', 'CRUST / WEDGE\n(Unit + Detachment)',
              'BASIN / STRATIGRAPHY\n(Reservoir + Charge)']

# Each cell:
for col in range(5):
    for row in range(3):
        ax = axes[row, col]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_xticks([])
        ax.set_yticks([])
        # Draw geological shapes using fill_between with Gaussian profiles
        # Use path_effects for ALL labels

# Titles and labels
for col in range(5):
    axes[0, col].set_title(stage_titles[col], fontsize=11, fontweight='bold', color='#f0a500')
for row in range(3):
    axes[row, 0].set_ylabel(row_labels[row], fontsize=10, fontweight='bold')

# Time arrow at bottom
fig.text(0.5, 0.01, 'TIME  →  (oldest to youngest)', ha='center', fontsize=9, color='#8b949e')
fig.suptitle('Title', fontsize=16, fontweight='bold', color='#f0a500', y=0.98)

plt.savefig('/tmp/panel.png', dpi=200, bbox_inches='tight', facecolor='#0d1117')
```

## NW Sabah Example (5 stages × 3 rows)

**Stage 1 (35-20 Ma):** PSCS oceanic slab subduction
- Lithosphere: descending oceanic plate, arc volcano, Borneo continental block
- Crust: accretionary wedge with imbricate thrusts, deep-marine shales
- Basin: trench fill (shales + MTDs), deep ocean

**Stage 2 (20-15 Ma):** Collision & underthrusting of Dangerous Grounds
- Lithosphere: DG continental block arriving, PSCS slab consumed
- Crust: NSPW shale wedge born above Setap Shale detachment, flexural loading
- Basin: deepwater sedimentation, source rock depositing

**Stage 3 (15-11 Ma):** Wedge loading & overpressure
- Lithosphere: fossil slab at rest, slab drip/breakoff
- Crust: overpressure building under deltaic load, source rock cooking
- Basin: gas generation window, early turbidites

**Stage 4 (11-10.5 Ma):** Mini-basin province
- Lithosphere: fossil slab dormant
- Crust: mobile NSPW with mini-basins, growth faults, turbidite fill
- Basin: Rotan-type reservoirs in mini-basins, charge migrating

**Stage 5 (10.5 Ma):** Mud canopy event
- Lithosphere: overpressure release
- Crust: ~50 mud volcano centres, ~1,900 km² canopy, vent complexes
- Basin: canopy topography controls reservoir distribution, ponded sands

## Color Coding (consistent across all cells)

| Unit | Color | Hex |
|---|---|---|
| Oceanic crust/slab | Brown | #8b4513 |
| Fossil slab | Dark brown | #5c3317 |
| Continental crust | Tan | #3d2e1e |
| Mantle | Dark brown | #2d1f0e |
| NSPW (mobile shale) | Dark green | #2d5016 |
| Mud canopy | Bright green | #4a6e2a |
| Turbidite reservoirs | Gold | #d29922 |
| Source rock | Green | #2ea043 |
| Faults | Red | #f85149 |
| Gas/fluid | Amber | #ffa657 |
| Water column | Dark blue | #1a3a5c |
| Seafloor | Blue | #2a5a8a |

## Style Rules

1. **No axes ticks** — the grid is conceptual, not to-scale
2. **Stage titles** on row 0: age range + event name, GOLD color
3. **Row labels** on column 0: vertical scale description
4. **Gaussian profiles** for structural shapes: `amp * np.exp(-((x - center) / sigma)**2)`
5. **Arrows** for convergence, extension, fluid flow
6. **path_effects stroke** on ALL labels: `pe.withStroke(linewidth=3, foreground='#0d1117')`
7. **Time arrow** at figure bottom with citations
8. **suptitle** describing the full evolution chain

## v2: Epistemic-Labeled Governance-Grade Panel (proven 2026-07-07)

The v2 panel adds **epistemic confidence tags per cell** with source citations and a color-coded legend, making it suitable for EGS governance and board-level decks.

### Epistemic Label System

| Label | Color | Hex | Meaning |
|---|---|---|---|
| CLAIM | Green | #3fb950 | Well supported by published data |
| PLAUSIBLE | Blue | #58a6ff | Consistent, not uniquely constrained |
| ESTIMATE | Amber | #d29922 | Timing/numbers approximate |
| HYPOTHESIS | Red | #f85149 | Conceptually sound, not proven at scale |
| SCHEMATIC | Gray | #8b949e | Simplified cartoon |

### Implementation: epistemic tag per cell

```python
# Define epistemic labels per cell [row][col]
epistemic = [
    # Row 0: Lithosphere
    [('CLAIM', 'Hall et al.\nGSM 2009'), ('PLAUSIBLE', 'nBOSS'), ...],
    # Row 1: Crust/Wedge
    [('CLAIM', 'Morley 2023'), ('CLAIM', 'Morley +\npetroleum sys'), ...],
    # Row 2: Basin/Strat
    [('SCHEMATIC', 'General\nmodel'), ('ESTIMATE', 'Petroleum\nsystem'), ...],
]

EPI = {
    'CLAIM': '#3fb950', 'PLAUSIBLE': '#58a6ff', 'ESTIMATE': '#d29922',
    'HYPOTHESIS': '#f85149', 'SCHEMATIC': '#8b949e',
}

def draw_epistemic_tag(ax, label, ref, x=0.97, y=0.95):
    """Draw epistemic confidence tag in corner of each cell."""
    color = EPI.get(label, '#8b949e')
    ax.text(x, y, f' {label} ', transform=ax.transAxes, fontsize=7,
            fontweight='bold', color='#0d1117', ha='right', va='top',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=color, edgecolor=color, alpha=0.9))
    ax.text(x, y - 0.12, ref, transform=ax.transAxes, fontsize=5.5,
            color='#8b949e', ha='right', va='top', style='italic')

# In cell loop:
draw_epistemic_tag(ax, label, ref)
```

### Legend bar at figure bottom

```python
legend_ax = fig.add_axes([0.35, 0.001, 0.4, 0.025])
legend_ax.set_xlim(0, 1); legend_ax.set_ylim(0, 1)
legend_ax.set_xticks([]); legend_ax.set_yticks([])
legend_ax.set_facecolor('#0d1117')
for spine in legend_ax.spines.values():
    spine.set_visible(False)
tags = ['CLAIM', 'PLAUSIBLE', 'ESTIMATE', 'HYPOTHESIS', 'SCHEMATIC']
descs = ['Well supported', 'Consistent, not unique', 'Timing/numbers approx', 'Conceptual, not proven', 'Simplified cartoon']
for i, (tag, desc) in enumerate(zip(tags, descs)):
    x_pos = i * 0.2 + 0.05
    legend_ax.add_patch(plt.Rectangle((x_pos, 0.55), 0.03, 0.3,
                                       facecolor=EPI[tag], edgecolor='none', transform=legend_ax.transAxes))
    legend_ax.text(x_pos + 0.04, 0.7, tag, fontsize=7, fontweight='bold',
                   color=EPI[tag], va='center', transform=legend_ax.transAxes)
    legend_ax.text(x_pos + 0.04, 0.4, desc, fontsize=5.5, color='#8b949e',
                   va='center', transform=legend_ax.transAxes)
```

### 888_HOLD flagging

HYPOTHESIS boxes should be flagged for human confirmation before irreversible decisions. In the JSON model, set `requires_888_hold: true` and `888_hold_reason` explaining what needs confirmation. See `references/geox-egs-claim-minting.md` for the full JSON schema and EGS registration workflow.

### Deep time state integration

Use `geox_deep_time_state` for each time window to provide climate/ocean context (CO₂, temperature, sea level). These become external consistency checks on your tectonic narrative. Store the VAULT999 seal ID as `deep_time_state_ref` in each box.

## When to Use

- "Show me the story from mantle to reservoir" requests
- Explaining basin evolution to a working geologist
- Multi-stage geological process explanation
- Conference poster layout for tectonic synthesis
- Competitive intelligence context (what the basin went through)
- Board-level decks needing epistemic governance tags

## Pitfalls

1. **Don't make it to-scale** — this is a conceptual panel, not a cross-section. The power is in showing the temporal evolution, not exact geometry.
2. **Consistent colors across ALL cells** — NSPW must be the same green in every cell where it appears. Break this and the reader loses the thread.
3. **Each cell must be self-explanatory** — the reader should understand that cell without reading others. But the grid structure makes the evolution story clear when read left-to-right.
4. **Gaussian peaks for structural shapes** — don't draw complex geometries. Simple bell curves with `fill_between` communicate the idea without getting bogged down in exact geometry.
5. **The "wow" is in the middle row** — crust/wedge level is where the action is. Give it the most detail and annotation.
6. **HYPOTHESIS ≠ wrong** — it means "conceptually sound but not uniquely constrained at this scale." Label it clearly; don't hide it. The hypothesis is often the interesting part (what drives timing?).
7. **Deep time state integration** — use `geox_deep_time_state` for each time window to provide climate/ocean context. These become external consistency checks.
8. **Source citations per cell** — each epistemic tag should reference the specific paper/data source. The footer should list all sources.
9. **Legend bar must not overlap content** — place at figure bottom with `fig.add_axes([0.35, 0.001, 0.4, 0.025])`.
