# Geological Artifact Figure Patterns

> Reusable matplotlib patterns for geological deliverable figures beyond basic maps/strat columns. Proven 2026-07-09, MBR 2026 GEOX bid proposal (12 figures, 2.9 MB PDF).

## When to Use

When producing a geological bid proposal, prospect evaluation, or technical deliverable that requires **technical substance** — not just maps and bar charts, but the figures a working geologist would expect to see:

- **Well correlation panels** — multi-well panels with stratigraphic tops + GR log overlays
- **Petrophysical log panels** — 5-track log analyses (lithology / GR / resistivity / porosity / interpretation)
- **Structural cross-sections** — anticlinal traps with GOC, fault seal, volumetric estimates
- **Well penetration summaries** — tabular visualization of well results across a basin
- **Play fairway thickness maps** — interpolated contour maps of target formation thickness

If the user is a working geologist and they said "give me geological artifacts" or "real geology not bar charts", they want THIS class of figure. Surface as reportlab pages or as embedded weasyprint images.

---

## 1. Well Correlation Panel

**Purpose:** Show 3–6 wells correlated on formation tops with GR log overlays and structural interpretation.

**Layout:** `figsize=(14, 10)`, two-column legend on the right side.

```python
fig, ax = plt.subplots(figsize=(14, 10))

well_names = ['M-1 (PM447)', 'M-2 (PM447)', 'M-3 (PM448)', 'M-4 (PM448)', 'M-5 (PM440)']
well_x = [1, 4, 7, 10, 13]  # km positions
np.random.seed(42)

# Stratigraphic units — (top depths per well, bottom depths per well, color, is_reservoir, litho desc)
formations = {
    'Group A-B':      {'top': [200,180,220,190,250], 'bot': [500,480,520,490,550],   'color': '#d4a76a', 'res': True,  'lito': 'Fluvial sand + coal'},
    'Group C-D':      {'top': [500,480,520,490,550], 'bot': [900,870,930,880,980],   'color': '#c49a5a', 'res': False, 'lito': 'Fluvial-deltaic, coals'},
    'Group E-F (RES)':{'top': [900,870,930,880,980], 'bot': [1400,1350,1450,1380,1520], 'color': '#b8894a', 'res': True,  'lito': 'Shoreface sands\nphi>20% k~500mD'},
    'Group G-H (SEAL)':{'top': [1400,1350,1450,1380,1520], 'bot': [1800,1750,1850,1780,1920], 'color': '#a07838', 'res': False, 'lito': 'Transgressive shale\noverpressure, HPHT'},
    'Group I-J':      {'top': [1800,1750,1850,1780,1920], 'bot': [2200,2150,2250,2180,2350], 'color': '#8a6828', 'res': False, 'lito': 'Lacustrine/deltaic\ncoal interbeds'},
    'Pre-Tertiary':   {'top': [2200,2150,2250,2180,2350], 'bot': [2800,2750,2850,2780,2950], 'color': '#5a4808', 'res': True,  'lito': 'Pre-Tertiary carbonate\nvuggy porosity'},
}

# Draw formation polygons between consecutive wells
for fname, fd in formations.items():
    for i in range(len(well_names)-1):
        xs = [well_x[i], well_x[i+1], well_x[i+1], well_x[i]]
        ys = [fd['top'][i], fd['top'][i+1], fd['bot'][i+1], fd['bot'][i]]
        ax.fill(xs, ys, color=fd['color'], alpha=0.4, edgecolor='#333', linewidth=0.5)
    # Right-side label
    avg_top = np.mean(fd['top'])
    ax.text(14.5, -avg_top, fname, fontsize=8, va='center',
            fontweight='bold' if fd['res'] else 'normal',
            color='#1b5e20' if fd['res'] else '#333')
    ax.text(14.5, -avg_top-200, fd['lito'], fontsize=6.5, va='top')

# Draw well bores + simulated GR logs
for i, name in enumerate(well_names):
    ax.plot([well_x[i], well_x[i]], [0, -3000], 'k-', linewidth=2.5, zorder=5)
    ax.text(well_x[i], 100, name, ha='center', va='bottom', fontsize=8,
            fontweight='bold', rotation=90)
    depths = np.linspace(0, 3000, 300)
    gr = np.ones_like(depths) * 60
    for fn, fd in formations.items():
        mask = (depths >= fd['top'][i]) & (depths <= fd['bot'][i])
        if fd['res']:
            gr[mask] = 30 + 15*np.random.randn(np.sum(mask))  # low GR = sand
        else:
            gr[mask] = 70 + 10*np.random.randn(np.sum(mask))  # high GR = shale
    gr = np.clip(gr, 10, 100)
    ax.fill_betweenx(-depths, well_x[i]-0.8, well_x[i]-0.8+gr/100*1.6,
                    color='yellow', alpha=0.3)
    ax.plot(well_x[i]-0.8+gr/100*1.6, -depths, 'g-', linewidth=0.5, alpha=0.5)

# Structural interpretation overlay — anticlinal feature
sx = np.linspace(0, 14, 100)
res_top = -900 - 200*np.exp(-((sx-7)/4)**2)
ax.plot(sx, res_top, 'r-', linewidth=2, label='Group E-F Top (interpreted)')
ax.annotate('Anticlinal trap\n(structural-strat.)', (7, -1050),
            fontsize=8, color='red', ha='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='red', alpha=0.8))

ax.set_ylabel('TVDSS (m)'); ax.set_xlabel('Cross-section distance (km)')
ax.set_title('Malay Basin PM447/PM448 - Well Correlation Panel with Structural Interpretation\n5 wells | Group E-F shoreface reservoir | Pre-Tertiary carbonate below',
             fontsize=11, fontweight='bold')
ax.invert_yaxis(); ax.set_xlim(-1, 18); ax.set_ylim(-3100, 200)
ax.set_yticks(np.arange(0, -3100, -500))
```

**Key conventions:**
- Inverted y-axis (depth increases downward)
- Reservoir units: bold, green label, slightly more saturated color
- Seal units: red label, lower-saturation color
- GR overlay: yellow fill on the inside of the well bore for sand-prone (low GR)
- Formation tops: black line connecting the well pick; the polygon fills span between wells
- **Right-side label panel** for formation names + lithology description — keep the panel narrow (~3 cm) so the correlation takes center stage

---

## 2. Petrophysical Log Panel (5-track)

**Purpose:** Show full log analysis for a single target well — the figure a petrophysicist produces to demonstrate net pay.

**Layout:** `figsize=(16, 12)`, 5 tracks via `gridspec_kw={'width_ratios': [1.5, 1, 1, 1, 1.2]}`.

```python
fig, axs = plt.subplots(1, 5, figsize=(16, 12),
                        gridspec_kw={'width_ratios': [1.5, 1, 1, 1, 1.2]})
depths = np.linspace(0, 3000, 600)

# Track 1: Lithology column (vertical color bar)
ax = axs[0]
for i in range(600):
    d = depths[i]
    if 900 < d < 1400:    fc = '#c9a574'  # Group E-F sand
    elif 1400 < d < 1800: fc = '#88a888'  # Group G-H shale
    elif 2200 < d < 2800: fc = '#b0b0b0'  # Pre-Tertiary carbonate
    else:                 fc = '#999999'
    ax.add_patch(plt.Rectangle((0, -d-3), 1, 3, facecolor=fc, alpha=0.6))
ax.set_xlim(0, 1); ax.set_ylim(-3000, 0); ax.invert_yaxis()
ax.set_title('Lithology', fontsize=9, fontweight='bold')
ax.set_ylabel('Depth (m TVDSS)', fontsize=9)
ax.set_xticks([])

# Track 2: Gamma Ray (with sand/shade shading)
ax = axs[1]
gr = 50 + 30*np.exp(-((depths-1200)/200)**2) + 25*np.sin(depths*0.05) + 5*np.random.randn(600)
gr = np.clip(gr, 10, 100)
ax.plot(gr, -depths, 'g-', linewidth=1)
ax.fill_betweenx(-depths, 0, gr, where=(gr<45), color='yellow', alpha=0.3)
ax.fill_betweenx(-depths, 0, gr, where=(gr>=45), color='lightgreen', alpha=0.2)
ax.set_xlim(0, 100); ax.set_ylim(-3000, 0); ax.invert_yaxis()
ax.set_title('Gamma Ray (API)', fontsize=9, fontweight='bold')

# Track 3: Resistivity (log scale, hydrocarbon shading)
ax = axs[2]
res = 2 + 8*np.exp(-((depths-1100)/150)**2) + 3*np.exp(-((depths-1300)/100)**2) + np.random.randn(600)*0.5
res = np.clip(res, 0.5, 50)
ax.semilogx(res, -depths, 'b-', linewidth=1)
ax.fill_betweenx(-depths, 2, res, where=(res>5), color='orange', alpha=0.3)
ax.set_xlim(0.5, 100); ax.set_ylim(-3000, 0); ax.invert_yaxis()
ax.set_title('Resistivity (ohmm)', fontsize=9, fontweight='bold')

# Track 4: Porosity (reservoir shading)
ax = axs[3]
por = 8 + 18*np.exp(-((depths-1150)/180)**2) + 5*np.random.randn(600)
por = np.clip(por, 2, 35)
ax.plot(por, -depths, 'r-', linewidth=1)
ax.fill_betweenx(-depths, 0, por, where=(por>15), color='red', alpha=0.2)
ax.set_xlim(0, 40); ax.set_ylim(-3000, 0); ax.invert_yaxis()
ax.set_title('Porosity (%)', fontsize=9, fontweight='bold')

# Track 5: Interpretation (Vsh, Sw, Net Pay)
ax = axs[4]
vsh = np.clip((gr - 10) / (80 - 10), 0, 1)
eff_por = por * (1 - vsh)
sw = np.clip(np.sqrt(0.8 / (0.3 * eff_por**2)), 0, 1)
net_pay = (por > 12) & (vsh < 0.4) & (sw < 0.6)
ax.plot(vsh*100, -depths, 'g-', linewidth=1, label='Vsh')
ax.plot(sw*100, -depths, 'b-', linewidth=1, label='Sw')
ax.fill_betweenx(-depths, 0, eff_por, where=net_pay, color='orange', alpha=0.5, label='Net Pay')
ax.set_xlim(0, 100); ax.set_ylim(-3000, 0); ax.invert_yaxis()
ax.set_title('Interpretation', fontsize=9, fontweight='bold')
ax.legend(fontsize=7, loc='upper right')

# Highlight key zones across all tracks
for a in axs:
    a.axhspan(-1400, -900, alpha=0.1, color='green')    # Group E-F RESERVOIR
    a.axhspan(-2800, -2200, alpha=0.1, color='purple')  # Pre-Tertiary carbonate

# Annotations on Track 1
axs[0].annotate('Group E-F\nRESERVOIR', (0.1, -1150), fontsize=8, color='#1b5e20',
               fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='green', alpha=0.8))
axs[0].annotate('Group G-H\nSEAL', (0.1, -1600), fontsize=8, color='#c62828',
               fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='red', alpha=0.8))
axs[0].annotate('Pre-Tertiary\nCARBONATE', (0.1, -2500), fontsize=8, color='#6a1b9a',
               fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='purple', alpha=0.8))

fig.suptitle('PM447 Target Well - Petrophysical Log Analysis',
             fontsize=11, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.96])
```

**Petrophysical convention reminders:**
- GR fill convention: yellow = clean sand (low GR), green = shale (high GR)
- Resistivity fill: orange = hydrocarbon zone (resistivity > 5 ohmm, threshold depends on basin)
- Porosity fill: red = reservoir (porosity > 15% threshold)
- Net pay: combined flag (porosity > cutoff, Vsh < cutoff, Sw < cutoff) — orange fill
- Width ratios: lithology column is widest (1.5x) because it's the most information-dense; interpretation is slightly wider (1.2x) for the net pay highlight

**Always tag the figure with an epistemic label in the caption:** `[INT — simulated log response based on published Malay Basin reservoir properties]` or similar. Real logs require real data room access.

---

## 3. Structural Cross-Section with Trap Analysis

**Purpose:** Show a structural trap with reservoir, seal, GOC, and volumetric estimate — the figure that gets a prospect drilled or dropped.

```python
fig, ax = plt.subplots(figsize=(14, 8))
x = np.linspace(0, 100, 500)

# Geometry
seabed = -50 - 10*np.sin(x*0.1)
res_top = -1200 - 250*np.exp(-((x-50)/12)**2) + 30*np.sin(x*0.05)  # anticlinal crest
res_base = res_top - 120 - 20*np.sin(x*0.08)
seal_base = res_base - 180 - 40*np.sin(x*0.06)

# Layer fills
ax.fill_between(x, seabed, -300, color='#e8d5b7', alpha=0.3, label='Quaternary-Pliocene')
ax.fill_between(x, -300, res_top, color='#d4a76a', alpha=0.4, label='Group C-D (fluvial-deltaic)')
ax.fill_between(x, res_top, res_base, color='#b8894a', alpha=0.7, label='Group E-F (SHOREFACE SANDS - RESERVOIR)')
ax.fill_between(x, res_base, seal_base, color='#a07838', alpha=0.6, label='Group G-H (TRANSGRESSIVE SHALE - SEAL)')
ax.fill_between(x, seal_base, -2000, color='#8a6828', alpha=0.4, label='Group I-J (lacustrine/deltaic)')

# Faults
ax.plot([25, 25], [-50, -2000], 'r-', linewidth=2, alpha=0.7)
ax.annotate('Growth fault\n(syn-depositional)', (27, -400), fontsize=8, color='red', rotation=-15)
ax.plot([78, 78], [-50, -2000], 'r-', linewidth=2, alpha=0.7)
ax.annotate('Late Miocene\nunconformity truncation', (80, -600), fontsize=8, color='red', rotation=-10)

# Gas-Oil Contact
goc = -1280
ax.axhline(y=goc, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
ax.text(95, goc, '<- GOC (interpreted)', fontsize=8, color='red', va='center')

# Trap annotation
ax.annotate('Anticlinal trap\n(structural-stratigraphic)\n4-way closure on crest',
            (50, -1050), fontsize=9, color='#1b5e20', fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.4', fc='white', ec='green', alpha=0.9),
            arrowprops=dict(arrowstyle='->', color='green', lw=1.5))

# Volumetric callout — this is the figure a decision-maker reads
ax.annotate('Estimated:\nGross rock vol ~500 MMm3\nNet pay ~200m\nExpected EUR: 150-300 MMboe\n(Int - screening)',
            (50, -750), fontsize=8, color='#2c5f8a', ha='center',
            bbox=dict(boxstyle='round,pad=0.4', fc='#f0f4f8', ec='#2c5f8a', alpha=0.9))

ax.set_ylabel('Depth (m TVDSS)'); ax.set_xlabel('Distance along cross-section (km)')
ax.set_title('PM447 Structural Cross-Section - Anticlinal Trap on Group E-F Shoreface Sands\nCrest at 50km | Closure ~100m | GOC ~1280m TVDSS',
             fontsize=11, fontweight='bold')
ax.legend(loc='upper left', fontsize=8, framealpha=0.9, ncol=2)
ax.invert_yaxis(); ax.set_xlim(-5, 105); ax.set_ylim(-2100, 50); ax.grid(True, alpha=0.3)
```

**Structural convention reminders:**
- Vertical exaggeration: 1:1 only. State this in the figure caption.
- Reservoir unit: most saturated color (Group E-F = `#b8894a` orange-brown)
- Seal unit: directly above reservoir, distinct color
- Fault lines: red, solid; annotation rotated to follow the fault plane
- GOC: red dashed line, labeled with arrow
- **Volumetric callout box** — this is what the decision-maker looks at first. Put it in a distinct color box (blue `#f0f4f8` background) and label it as screening estimate (Int epistemic band)

---

## 4. Well Penetration Summary

**Purpose:** Tabular visualization of multiple wells in a basin — the "result card" the exploration manager scans.

```python
fig, ax = plt.subplots(figsize=(12, 7))
wells = [
    ('Sebahat-1',     '1970', 3.5, 2800, 3500, 'Gas shows in Sebahat Fm\nNo commercial flow'),
    ('Kuda-Terbang-1','1971', 5.5, 3200, 3800, 'Discovery - shoreface sands\nphi>20%, k=1410mD\nSub-commercial: 28-42 MMboe'),
    ('Mutiara Hitam-1','1994', 4.5, 3500, 4100, 'Sub-commercial gas/condensate\nin Sebahat Fm carbonates'),
    ('Pahu-1',         '2012', 7.0, 4200, 4200, 'P&A before TD\noperational problems\nNo formation evaluation'),
    ('Kerupang-1',    '2015', 6.0, 4500, 5000, 'Minor gas shows\nNo commercial accumulation'),
    ('Pendekar-1',    '2015', 6.5, 4800, 5200, 'Minor gas shows\nStructural complexity\ntrap integrity risk'),
]
for name, year, xp, top, bot, desc in wells:
    ax.plot([xp, xp], [0, bot], 'k-', linewidth=3)
    ax.plot([xp, xp], [top, bot], color='#c49a5a', linewidth=4, alpha=0.7)
    ax.scatter(xp, top, s=60, c='red', edgecolors='black', zorder=5, marker='^')
    ax.scatter(xp, bot, s=60, c='green', edgecolors='black', zorder=5, marker='v')
    ax.text(xp, 0-80, name, ha='center', va='top', fontsize=8, fontweight='bold')
    ax.text(xp, bot+50, f'{year}', ha='center', fontsize=7, color='#888')
    dy = -(top+bot)/2
    ax.annotate(desc, (xp+1.5, dy), fontsize=7, va='center',
               bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#888', alpha=0.8),
               arrowprops=dict(arrowstyle='-', color='#888', lw=0.5))

# Formation backgrounds
ax.axhspan(0, -800, alpha=0.1, color='#e8d5b7')     # Togopi
ax.axhspan(-800, -2500, alpha=0.1, color='#d4a76a')  # Ganduman
ax.axhspan(-2500, -4000, alpha=0.15, color='#c49a5a')  # Sebahat (RESERVOIR)
ax.axhspan(-4000, -5000, alpha=0.1, color='#8a6828')   # Tanjong/Tungku
ax.text(-0.5, -400, 'Togopi\nFm', fontsize=8, ha='right')
ax.text(-0.5, -1650, 'Ganduman\nFm', fontsize=8, ha='right')
ax.text(-0.5, -3250, 'Sebahat\nFm', fontsize=8, ha='right', color='#1b5e20', fontweight='bold')
ax.text(-0.5, -4500, 'Tanjong/Tungku\nFm', fontsize=8, ha='right')
```

**Convention:** Red triangle at top of well = formation top; green triangle at bottom = TD. The vertical bar between top and TD is the actual penetrated reservoir interval (colored).

---

## 5. Play Fairway Thickness Map

**Purpose:** Interpolated contour map of target formation thickness — used to identify optimal drilling targets.

```python
fig, ax = plt.subplots(figsize=(10, 8))
xx = np.linspace(104, 105.5, 50)
yy = np.linspace(4.5, 6, 50)
X, Y = np.meshgrid(xx, yy)
Z = 50*np.exp(-((X-104.7)**2/0.04 + (Y-5.3)**2/0.04)) + \
    30*np.exp(-((X-104.9)**2/0.03 + (Y-5.5)**2/0.03))

cf = ax.contourf(X, Y, Z, levels=15, cmap='YlOrBr')
cbar = plt.colorbar(cf, ax=ax, label='Carbonate Thickness (m)')

# Block markers
ax.scatter([104.5, 104.8], [5.2, 5.5], s=300, c='blue', edgecolors='black',
           linewidths=2, marker='s', zorder=5, label='PM447 / PM448')
ax.text(104.5, 5.2, 'PM447', ha='center', va='bottom', fontsize=9,
        fontweight='bold', color='white',
        bbox=dict(boxstyle='round,pad=0.2', fc='blue', alpha=0.7))
ax.text(104.8, 5.5, 'PM448', ha='center', va='bottom', fontsize=9,
        fontweight='bold', color='white',
        bbox=dict(boxstyle='round,pad=0.2', fc='blue', alpha=0.7))
ax.annotate('Carbonate\nthickening trend\nNE-SW', (104.65, 5.35),
            fontsize=8, color='red', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5), ha='center')

ax.set_xlabel('Longitude (deg E)'); ax.set_ylabel('Latitude (deg N)')
ax.set_title('PM447/PM448 - Pre-Tertiary Carbonate Thickness Fairway Map\nThickest carbonates on NE-SW trend - optimal drilling targets',
             fontsize=11, fontweight='bold')
ax.legend(loc='upper right', fontsize=8)
ax.grid(True, alpha=0.3)
```

**Critical pitfall:** Coordinate values must come from GPS or published map data. Never plot from memory — the geology-rigor skill's cardinal rule. Tag every coordinate with source: `Wiki`, `GPS`, `paper_name`, `approx_from_map`, or `SPECULATED`.

---

## Common Mistakes to Avoid

1. **Don't put every figure in the PDF** — 12 figures is the upper limit. More than that and the deliverable becomes a coffee-table book, not a bid memo. Choose the 8–12 figures that carry the argument.

2. **Don't fabricate real-looking log responses** when the data is unavailable. Use simulated log responses with clear `[INT — simulated]` labels in the caption. The user (a working geologist) will catch a fake log in 5 seconds.

3. **Don't skip the GOC line** on structural cross-sections. Even a dashed line at a guessed depth is better than no GOC — it shows you understand trap geometry.

4. **Don't label formation tops with only formation name** — include the Group designation (e.g., "Group E-F" not just "Sand Unit"). The Group naming convention is industry standard in Malay Basin.

5. **Always include the epistemic band in the caption** — `[INT — interpreted from regional seismic geometry, Bishop 2002]` or `[SCHEMATIC — based on TGS APGCE 2024 pseudo-3D]`. A figure without an epistemic label is a fabrication risk.

6. **Don't show reservoir data without showing the seal directly above it.** The pair is the petroleum system. The pair on a structural cross-section = bid/no-bid.

---

## File Reference (Proven 2026-07-09)

- `/tmp/mbr2026_figures/fig8_well_correlation.png` (509 KB) — 5-well correlation panel
- `/tmp/mbr2026_figures/fig9_petrophysical_logs.png` (725 KB) — 5-track log panel
- `/tmp/mbr2026_figures/fig10_structural_cross_section.png` (249 KB) — anticlinal trap cross-section
- `/tmp/mbr2026_figures/fig11_sandakan_wells.png` (122 KB) — well penetration summary
- `/tmp/mbr2026_figures/fig12_carbonate_fairway.png` (136 KB) — thickness fairway map

These are the artifacts that distinguish a "geological" deliverable from a "colorful chart" deliverable. A working geologist's first question is: "Where's the well log, where's the cross-section, where's the trap geometry?" These five patterns answer that question.
