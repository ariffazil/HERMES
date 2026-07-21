# Geological Cross-Section Generation with Matplotlib

> Proven pattern for generating publication-quality geological cross-sections in Python.
> Born from the NW Sabah crustal models session (2026-07-20).

## Principle

Rule #2 of geological-artifact-rigor says "No Cartoon Geometry." Flat rectangular blocks → wavy irregular boundaries. The jump from "schematic" to "looks like a cross-section" is boundary irregularity + proper hatch patterns + fault symbols.

## Proven Pattern

### Layer Boundary Generation

Use sine waves with random noise, NOT flat lines:

```python
def wavy_line(x_start, x_end, base_y, amplitude=0.3, n_waves=8, noise=0.15):
    n = 200
    xs = np.linspace(x_start, x_end, n)
    ys = base_y + amplitude * np.sin(np.linspace(0, n_waves * 2*np.pi, n))
    ys += np.random.normal(0, noise, n)
    return xs, ys
```

### Layer Polygon

Each geological unit is a `matplotlib.patches.Polygon` with wavy top and bottom:

```python
def layer_polygon(x_left, x_right, y_top_base, y_bot_base, amp_top=0.2, amp_bot=0.2, n_waves=6):
    xs_top, ys_top = wavy_line(x_left, x_right, y_top_base, amplitude=amp_top, n_waves=n_waves)
    xs_bot, ys_bot = wavy_line(x_left, x_right, y_bot_base, amplitude=amp_bot, n_waves=n_waves+1)
    verts = list(zip(xs_top, ys_top)) + list(zip(xs_bot[::-1], ys_bot[::-1]))
    return Polygon(verts, closed=True)
```

Then set facecolor, alpha, hatch per lithology:

```python
poly.set_facecolor('#E67E22')   # continental crust - orange-brown
poly.set_alpha(0.85)
poly.set_hatch('ooo')           # continental crust pattern
ax.add_patch(poly)
```

### Fault Symbols

**Thrust faults** — sawtooth markers on hanging wall:

```python
def draw_thrust(ax, x, y_top, y_bot):
    dx, dy = 0.15, 0.2
    n_teeth = int((y_top - y_bot) / dy)
    for i in range(n_teeth):
        yi = y_top - i * dy
        ax.plot([x-dx/2, x, x+dx/2], [yi+dy/4, yi-dy/4, yi+dy/4], 
               color='#FFD700', linewidth=1.5)
```

**Normal faults** — tick marks on hanging wall side.

### Hatch Pattern Reference

| Lithology | Hatch | Color (dark) | Color (light) |
|---|---|---|---|
| Ocean | None | `#0D2137` | `#D4E6F1` |
| Sediments (post-DRU) | `....` | `#C4A46C` | `#D4C4A8` |
| Turbidites | `..` | `#D4B896` | `#E8D5B7` |
| Mobile shale (NSPW) | `///` | `#5D4037` | `#8D6E63` |
| Mini-basin fill | `\\\\` | `#8D7B5A` | `#A09075` |
| Accretionary prism | `+++` | `#607D4A` | `#8FAA6A` |
| Nido Limestone | `xx` | `#5DADE2` | `#85C1E9` |
| Continental crust | `ooo` | `#E67E22` | `#F0B27A` |
| Oceanic crust | `\|\|\|` | `#2C3E50` | `#5D6D7E` |
| Mantle lithosphere | `---` | `#922B21` | `#C0392B` |
| Asthenosphere | `***` | `#D35400` | `#E67E22` |

### Moho Conventions

- **Moho**: thick dashed line, gold or red, labeled with depth range
- **True Moho vs Fake Moho**: in models where a mid-crustal reflector is MISIDENTIFIED as Moho, use RED solid for true Moho and GREY dotted for the fake reflector
- **Continental-Ocean Boundary (COB)**: green vertical line

## Background Choice

- **Dark theme**: good for presentations, websites, public communication. Reads as "infographic."
- **Light/white**: required for academic journals, peer review. Reads as "scientific figure."
- Choose based on audience. Arif's use case is public — dark is appropriate.

## Common Pitfall

The first attempt will use `Rectangle` patches (flat blocks). This violates Rule #2. Always use wavy polygons for geological layers. The `layer_polygon` helper above makes this a one-line replacement.

## Verification Check

After generating, ask: "Would Raja accept this as geological content, or would he say tak cukup geology?" If the boundaries are rectangular, the answer is no.
