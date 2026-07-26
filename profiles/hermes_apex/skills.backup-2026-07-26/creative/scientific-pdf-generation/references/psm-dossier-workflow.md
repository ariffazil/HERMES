# Petroleum System Modeling Dossier — Rapid Generation Pattern

> Proven: 2026-07-22. Two complete PSM intelligence dossiers (Sabah + Timor-Leste),
> 12 matplotlib figures, 0 render failures, ~90s total generation time each.

## When to Use

When Arif asks for a PSM showcase dossier for a petroleum basin — the pattern
is "Tell me everything about GEOX and PSM in [basin/country]" followed by
"Do one PDF to showcase this." Audience is typically a working geologist
(Beicip, PETRONAS, operator).

## End-to-End Pipeline (5 stages, ~90 seconds)

### Stage 1 — Parallel Research (1 call, ~5s)

```python
# Three parallel web searches + one Hound fetch for detailed geology
web_search("basin geology petroleum system [region]")
web_search("basin stratigraphy source rock reservoir seal [region]")
web_search("field discoveries reserves status [region] 2025 2026")
mcp__hound__mcp_smart_fetch(url="key geological paper URL")
```

### Stage 2 — Figure Planning (no tool calls needed)

Pick exactly 6 figures that cover the PSM workflow:
1. **Regional map** — basin boundaries, discoveries, structural domains
2. **Stratigraphic column** — formation ages, reservoir/seal/source labeled, properties
3. **Burial history + Ro profile** — twin panel: depth vs time + Ro vs depth
4. **Hydrocarbon generation timing** — oil/gas rate vs time, key events annotated
5. **Cross-section** — schematic NW-SE showing structural domains, traps, discoveries
6. **GEOX toolchain diagram** — input tools → GEOX engine → outputs, with arifOS audit gate

### Stage 3 — Figure Generation (single Python script, ~15s)

Write one script (`/tmp/basin_figs.py`) that generates all 6 figures:
- `fig1_regional_map()` — matplotlib with fill_between for basins, scatter for discoveries
- `fig2_strat_column()` — barh charts, one per basin (twin panel), annotated with properties
- `fig3_burial_history()` — two-panel: fill_between for burial + plot for Ro/depth
- `fig4_generation_timing()` — Gaussian-shaped generation curves, axvline for events
- `fig5_cross_section()` — schematic with fill_between, annotations, labels
- `fig6_geox_toolchain()` — FancyBboxPatch boxes, arrows, central GEOX engine block

**All figures use Mode B dark theme colors** (BG=#0d1117, GOLD=#f0a500, etc.).

### Stage 4 — PDF Assembly (single reportlab script, ~10s)

Use the geological dossier template pattern from `templates/geological_dossier.py`
but adapted for Mode B (dark theme). Key structure:

```
Cover (title, metadata table, core proposition callout)
Section 1 — Executive Summary
Section 2 — Regional Basin Architecture + fig1
Section 3 — Stratigraphy + fig2 + properties table
Section 4 — Burial History & Thermal Maturity + fig3
Section 5 — Generation Timing + fig4
Section 6 — Cross-Section + fig5
Section 7 — Commercial Context (PSC table, operators, reserves)
Section 8 — Data Gaps & Upgrade Paths (hypothesis → data needed table)
Section 9 — GEOX Toolchain + fig6 + competitive comparison table
Section 10 — References + Epistemic Band Reference
```

### Stage 5 — Delivery

```python
# Verify page count
pdfinfo output.pdf | grep Pages

# Deliver
# MEDIA:/path/to/output.pdf
```

## Critical Rules for Geological PSM Dossiers

### Data Quality
- Every formation age must have a published source (cite in reference list)
- Reservoir properties: quote ranges (porosity, perm, NTG), not point values
- Source rock: TOC, kerogen type, HI, Ro — if no well data, tag SPEC
- Discoveries: reserves figures must have source attribution

### Terminology
- Never conflate PSC block names with structural trend names
- Never conflate formation names with field names
- Distinguish OBS (press release, official data) from DER (modeled) from SPEC (estimated)

### Epistemic Discipline
- Every figure caption carries an epistemic label: `[OBS]`, `[DER]`, `[INT]`, `[SCHEMATIC]`
- The cross-section is always SCHEMATIC unless built from real seismic data
- Burial curves are DER unless calibrated with well-specific Ro/Tmax data
- Source rock parameters without Rock-Eval data are SPEC

### Competitive Framing
- Acknowledge commercial PSM tools (TemisFlow, PetroMod) as physics engines
- Position GEOX as the audit/falsification layer — not a replacement
- Include a comparison table (GEOX vs TemisFlow vs PetroMod) on auditability/falsification/governance
- Close with an invitation to the audience's data: "What happens when GEOX reads your project files?"

## Figure Quick Reference

| Fig | What | Matplotlib pattern | Key gotcha |
|---|---|---|---|
| 1 | Regional map | fill_between + scatter + annotate | Basin boundaries are approximate — tag INT |
| 2 | Strat column | barh (flipped), twin panels | Align y-axes for age comparison |
| 3 | Burial + Ro | fill_between (burial) + plot (Ro) | Oil window entry line must be labeled with age |
| 4 | Generation | fill_between + plot, Gaussian shape | Peak oil BEFORE peak gas in oil-prone systems; AFTER in gas-prone |
| 5 | Cross-section | fill_between + plot, schematic | Always tag SCHEMATIC, not INT |
| 6 | Toolchain | FancyBboxPatch + arrows | Include arifOS gate (falsification) as separate block |

## Pitfalls Observed

- **Stratigraphic column age ranges:** Modeled ages (e.g., Plover Fm as "28-42 Ma") vs actual geological ages (175-160 Ma Jurassic). Use the modeled age range for the chart (it's what the basin model uses) but note the discrepancy.
- **S/R detection on short data:** 48 candles may only produce 1-2 S/R levels after clustering. Accept sparse output rather than fabricating levels.
- **RSI dict-array gotcha:** Gold-api returns `[{'time': ts, 'value': v}]` not `[v]`. Must extract `.value`.
- **`$` in matplotlib text:** Use `$4,129` → triggers LaTeX math parser crash. Replace with `USD` or use `plt.rcParams.update({'text.usetex': False})`.
