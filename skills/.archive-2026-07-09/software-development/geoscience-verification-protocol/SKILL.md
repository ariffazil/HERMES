---
name: geoscience-verification-protocol
description: >
  Mandatory verification protocol for geoscience deliverables — coordinates, block names,
  stratigraphic picks, structural labels. Prevents F2 TRUTH violations in exploration context.
  "Location location location" — wrong coordinates = wrong well = millions lost.
triggers:
  - geological map or cross-section generation
  - PSC block name references
  - coordinate plotting for well locations, mud volcanoes, fields, prospects
  - stratigraphic column or biostratigraphic zone assignments
  - structural trend naming (e.g. L-B-P, fold-thrust belt features)
  - PDF/dossier generation with geological content
---

# Geoscience Verification Protocol

> **"Biggest flaw ever!!! Location location. Location!!! That's the foundation for GeOX.
> Can you imagine u AI give wrong drill location!!!"** — Arif, 2026-07-07

## The Rule

**NEVER plot coordinates from memory. NEVER assume block names from structural labels.
Every coordinate and every name in a geological deliverable MUST have a source.**

## Three Classes of Geoscience Identifiers

### 1. Coordinates (lat/lon)
- **OBSERVED**: GPS measurement, published in peer-reviewed paper with coordinates stated
- **DERIVED**: Read from published map figure (approximate, state uncertainty)
- **ESTIMATE**: From regional context or adjacent features
- **SPECULATED**: From memory or assumption — **NEVER USE IN DELIVERABLES**

### 2. Block/PSC Names
- **VERIFIED**: Confirmed in PETRONAS MPM bid round, PSC signing announcement, or operator website
- **INFerRED**: Structural feature name mapped to block via published paper (state evidence)
- **UNVERIFIED**: User-provided name not found in public literature — **LABEL EXPLICITLY**

### 3. Structural/Stratigraphic Labels
- **Published**: Named in peer-reviewed literature (e.g. "L-B-P Ridge" from Khamis et al. 2017)
- **Internal**: Operator-specific designation — **DO NOT assume = public PSC block name**
- **User-provided**: Treat as UNVERIFIED until confirmed

## Pre-Delivery Checklist (MANDATORY)

Before generating ANY geological deliverable (map, cross-section, dossier, PDF):

```
□ Every coordinate has source citation (paper, GPS, map figure)
□ Every block name verified against PETRONAS MPM or operator public disclosure
□ Structural trend names NOT mapped to block names without evidence
□ Epistemic labels on every data point (OBSERVED/DERIVED/ESTIMATE/SPECULATED)
□ Coordinate accuracy disclaimer on maps showing verification level per feature
□ "SCHEMATIC" label on any structural line not from survey-grade data
□ Offshore features flagged as APPROXIMATE unless from published well coordinates
```

## Known Sabah Deepwater PSC Blocks (Public, as of 2026)

| Block | Operator | Key Fields | Source |
|---|---|---|---|
| Block G | ConocoPhillips | Limbayong, Malikai | ConocoPhillips website |
| Block J | ConocoPhillips | — | ConocoPhillips website |
| Block H | PTTEP | Rotan, Buluh | PETRONAS MPM |
| Block K | PTTEP | Kikeh, SNP, Gumusut | PTTEP/Murphy acquisition |
| Block N | — | Tepat-1 (2018) | PETRONAS MPM |
| Block R | JX Nippon | — | Jong et al. 2014a |
| Block X | — | Bestari | ResearchGate/Khamis |
| Block 2K | TotalEnergies/Shell/PCSB | — | oedigital.com |
| Block 2V, 2W | Various | — | PETRONAS MPM |

**"Block P" does NOT appear in any public PSC designation.** The "P" in "L-B-P" is a
structural trend label from Khamis et al. 2017/2018, NOT a PSC block name.

## Pitfalls Encountered

### Pitfall 1: Plotting coordinates from memory
**What happened**: Mud volcano map created with coordinates from memory. Lipad MV was
0.5° longitude off, Maliau Basin was 0.67° latitude off, Ranau was 0.34° longitude off.
**Fix**: Every coordinate must have a source. If no source found, label as "approximate"
with uncertainty radius, or DON'T PLOT.

### Pitfall 2: Mapping structural trend letters to block names
**What happened**: "L-B-P" trend → assumed L=Limbayong(Block G), B=Bestari(Block X),
P="Block P". None of these mappings were verified.
**Fix**: Structural trend names ≠ PSC block names. A field can exist in any block.
Don't map without explicit published evidence.

### Pitfall 3: Building entire dossier on unverified block name
**What happened**: 10-page PDF dossier built around "Block P" which doesn't exist as
a public PSC designation. Required full rebuild when discovered.
**Fix**: Verify block/PSC name BEFORE building any deliverable. If unverifiable,
build on structural trend name (e.g. "L-B-P Trend") without block attribution.

## Coordinate Source Priority

1. **Published well coordinates** (PETRONAS MPM, operator press releases)
2. **Peer-reviewed paper with stated GPS coordinates**
3. **Published map figure with scale bar** (derive with stated uncertainty)
4. **Wikipedia/Gazetteer** (good for cities, NOT for geological features)
5. **User input** (treat as UNVERIFIED — ask for source)
6. **NEVER from memory**

## Template: Coordinate Verification Table

When building geological maps or deliverables, always include:

```
| Feature | Lat | Lon | Source | Epistemic | Uncertainty |
|---|---|---|---|---|---|
| City X | 5.98 | 116.07 | Wikipedia | OBSERVED | ±0.01° |
| MV Y | 5.19 | 118.50 | GPS paper (ref) | OBSERVED | ±0.005° |
| Block Z | — | — | UNVERIFIED | — | — |
| Structural line | — | — | Schematic | SCHEMATIC | ±5km |
```

## References
- Coordinate accuracy incident: 2026-07-07, Sabah mud volcano map (0.5° error on Lipad MV)
- Block naming incident: 2026-07-07, "Block P" dossier (block doesn't exist in public PSC)
- Khamis et al. 2017/2018: L-B-P Ridge structural trend (GSM Bulletin)
- Morley et al. 2023: NSPW mud canopy system (Geosphere)
