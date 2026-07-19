# Data-Driven Cross-Section Pattern

> Learned: 2026-07-05 (Sabah Semporna→Dangerous Ground NE-SW cross-section)
> Use when: building a cross-section from an existing document's structural data, not from first principles.

## Pattern

When the source is a **document** (PDF, synthesis paper) rather than raw well/seismic data:

1. **Extract structural data from the document** via `pdftotext` (not `web_extract` — that's blocked for local files).
2. **Identify the key structural elements** and their spatial positions along the transect:
   - Surface topography / bathymetry (peaks, shelves, deep water)
   - Moho depth (from gravity inversion, receiver functions)
   - Basement surface
   - Sedimentary layer boundaries (Neogene, Paleogene, etc.)
   - Igneous bodies (granite plutons, volcanic arc)
   - Mobile shale / mud canopy extent
   - Fault systems (active faults with Mw/year)
   - Detachment surfaces
3. **Build piecewise numpy arrays** for each surface — use `np.piecewise(x, [cond1, cond2, ...], [lambda1, lambda2, ...])` where the conditions define structural domains along the transect.
4. **Layer fills with `ax.fill_between()`** — top surface, bottom surface, condition mask, color, alpha, zorder.
5. **Label every structural element** with `path_effects=[pe.withStroke(linewidth=3, foreground='white')]` for readability.
6. **Include source citations** in the bottom-right annotation.

## Pitfalls

- **`np.piecewise` with lambdas that call another piecewise function fails silently.** Define each surface as an independent array, not as a function of another surface. If you need surface-to-surface relationships, compute both arrays first, then use `np.minimum`/`np.maximum` on the arrays.
- **`surface/1000.0` conversion** — topography is often in meters, Moho in km. Convert to consistent units BEFORE plotting.
- **The granite body should be clipped** — `np.clip(gt, -12, 5)` prevents the inverted teardrop from going out of bounds.
- **Invert y-axis** — geological cross-sections show depth increasing downward. Use `ax.invert_yaxis()` or set ylim with negative values.
- **Moho label placement** — use `ax.annotate` with arrow, not just `ax.text`, so the reader knows which line is Moho.

## Sabah Example (2026-07-05)

Transect: NE (Semporna, 0 km) → Lahad Datu (80 km) → Crocker Range (120-160 km) → Mt Kinabalu (185-215 km) → NSPW (250-310 km) → Dangerous Ground (350+ km)

Key data points from synthesis PDF:
- Crocker Range: crust >40 km (Madon et al. 2025)
- Kinabalu: granite 7.85 Ma, 360°C/Myr cooling, crust 30-35 km (Cottam et al. 2013)
- NSPW: ~50 mud volcano centres, ~1,900 km² mud canopy (Morley et al. 2022)
- 2015 Mw 6.0 fault system (Wang et al. 2017)
- Dangerous Ground: extended crust ~26 km

Output: `/root/sabah_xsection_SENW.png` (600 KB, 5578×2778 px, 200 dpi)
